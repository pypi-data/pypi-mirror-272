import dataclasses
import json
import os
from functools import cached_property, wraps
from typing import List, Optional, Sequence, Set, Tuple

from ens import ENS
from eth_account import Account
from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from eth_utils import ValidationError
from hexbytes import HexBytes
from packaging import version as semantic_version
from prompt_toolkit import HTML, print_formatted_text
from web3 import Web3
from web3.contract import Contract
from web3.exceptions import BadFunctionCallOutput

from gnosis.eth import (
    EthereumClient,
    EthereumNetwork,
    EthereumNetworkNotSupported,
    TxSpeed,
)
from gnosis.eth.clients import EtherscanClient, EtherscanClientConfigurationProblem
from gnosis.eth.constants import NULL_ADDRESS, SENTINEL_ADDRESS
from gnosis.eth.contracts import (
    get_erc20_contract,
    get_erc721_contract,
    get_safe_V1_1_1_contract,
    get_sign_message_lib_contract,
)
from gnosis.eth.eip712 import eip712_encode
from gnosis.eth.utils import get_empty_tx_params
from gnosis.safe import InvalidInternalTx, Safe, SafeOperationEnum, SafeTx
from gnosis.safe.api import TransactionServiceApi
from gnosis.safe.multi_send import MultiSend, MultiSendOperation, MultiSendTx
from gnosis.safe.safe_deployments import safe_deployments

from safe_cli.ethereum_hd_wallet import get_account_from_words
from safe_cli.operators.exceptions import (
    AccountNotLoadedException
)
from safe_cli.safe_addresses import (
    get_default_fallback_handler_address,
    get_last_sign_message_lib_address,
    get_safe_contract_address,
    get_safe_l2_contract_address,
)
from safe_cli.utils import choose_option_from_list, get_erc_20_list, yes_or_no_question

from ..contracts import safe_to_l2_migration
from .hw_wallets.hw_wallet import HwWallet
from .hw_wallets.hw_wallet_manager import HwWalletType, get_hw_wallet_manager

import requests
import time

from safe_cli.operators.fs_attestation_auth import FailSafeAttestationServiceAuth

@dataclasses.dataclass
class SafeCliInfo:
    fs_attestation_service_api_base_url: str
    fs_attestation_service_attestation_authority_wallet_address: str
    fs_attestation_service_attestation_authority_wallet_address_balance: str

    def __str__(self):
        return (
            f"fs-attestation-service-api-base-url={self.fs_attestation_service_api_base_url} fs-attestation-service-attestation-authority-wallet-address={self.fs_attestation_service_attestation_authority_wallet_address} fs_attestation_service_attestation_authority_wallet_address_balance={self.fs_attestation_service_attestation_authority_wallet_address_balance} "
        )

class FailSafeAttestationServiceOperator:
    address: ChecksumAddress
    node_url: str
    ethereum_client: EthereumClient
    ens: ENS
    network: EthereumNetwork
    etherscan: Optional[EtherscanClient]
    safe_tx_service: Optional[TransactionServiceApi]
    safe: Safe
    safe_contract: Contract
    safe_contract_1_1_0: Contract
    accounts: Set[LocalAccount] = set()
    default_sender: Optional[LocalAccount]
    executed_transactions: List[str]
    _safe_cli_info: Optional[SafeCliInfo]
    require_all_signatures: bool

    def __init__(self, address: ChecksumAddress, node_url: str, safe_tx_service_base_url: str, fs_attestation_service_base_url: str):
        self.address = address
        self.node_url = node_url
        self.safe_tx_service_base_url = safe_tx_service_base_url
        self.fs_attestation_service_base_url = fs_attestation_service_base_url
        self.ethereum_client = EthereumClient(self.node_url)
        self.ens = ENS.from_web3(self.ethereum_client.w3)
        self.network: EthereumNetwork = self.ethereum_client.get_network()
        try:
            self.etherscan = EtherscanClient(self.network)
        except EtherscanClientConfigurationProblem:
            self.etherscan = None

        try:
            self.safe_tx_service = TransactionServiceApi.from_custom_safe_tx_service_base_url(
                self.ethereum_client,
                self.safe_tx_service_base_url
            )
        except EthereumNetworkNotSupported:
            self.safe_tx_service = None

        self.safe = Safe(address, self.ethereum_client)
        self.safe_contract = self.safe.contract
        self.safe_contract_1_1_0 = get_safe_V1_1_1_contract(
            self.ethereum_client.w3, address=self.address
        )
        self.accounts: Set[LocalAccount] = set()
        self.default_sender: Optional[LocalAccount] = None
        self.executed_transactions: List[str] = []
        self._safe_cli_info: Optional[SafeCliInfo] = None  # Cache for SafeCliInfo
        self.require_all_signatures = (
            True  # Require all signatures to be present to send a tx
        )
        self.hw_wallet_manager = get_hw_wallet_manager()

        self.safe_cli_info.fs_attestation_service_base_url = fs_attestation_service_base_url

    # This function assumes self.fs_attestation_service_auth is already initialized
    def fs_attestation_user_login_internal(self):
        try:
            # Perform Authentication with FailSafe Attestation Service and get the access token
            print_formatted_text(
                HTML("<ansigreen>Performing FailSafe Attestation Service Authentication. Please wait...</ansigreen>")
            )
            self.access_token = self.fs_attestation_service_auth.fs_attestation_user_login()
            self.last_login_time = int(time.time())
            response_text = HTML("<ansigreen>FailSafe Attestation Service Authentication flow completed successfully</ansigreen>")
            print_formatted_text(
                response_text
            )
        except Exception:
            response_text = HTML("<ansired>Some error occurred when performing FailSafe Attestation Service Authentication flow</ansired>")
            print_formatted_text(
                response_text
            )

    def fs_attestation_auth_decorator(func):
        @wraps(func)
        def auth_token_expiry_time_check_wrapper(self, *args, **kwargs):

            if not hasattr(self, 'last_login_time'):
                response_text = HTML("<ansired>No active session exists. Please log into FS Attestation Service by executing the command <b><ansigreen>fs_attestation_service_auth</ansigreen></b> and then try this command</ansired>")
                print_formatted_text(
                    response_text
                )
                return

            current_time = int(time.time())
            # The Auth token issued by the FailSafe Attestation Service is valid for 10 minutes
            # If the token is nearing expiry time (more than 9 minutes), let's re-authenticate with the FailSafe Attestation Service
            if current_time - self.last_login_time > 540:
                self.fs_attestation_user_login_internal()
            return func(self, *args, **kwargs)

        return auth_token_expiry_time_check_wrapper

    def fs_attestation_user_login(self, safe_cli_owner: str, safe_cli_owner_private_key: str) -> str:
        try:
            self.fs_attestation_service_auth = FailSafeAttestationServiceAuth(self.fs_attestation_service_base_url, self.network.value, self.address, safe_cli_owner, safe_cli_owner_private_key)
            self.fs_attestation_user_login_internal()
            self.fs_attestation_get_attestation_authority_wallet_address(silent_mode=True)
        except Exception:
            response_text = HTML("<ansired>Some error occurred when performing FailSafe Attestation Service Authentication flow</ansired>")
            print_formatted_text(
                response_text
            )

    @fs_attestation_auth_decorator
    def fs_attestation_service_enrolment(self) -> str:
        try:
            enrolment_url = "{}/{}".format(self.fs_attestation_service_base_url, "attestation-service/enrollment")
            headers = {'Authorization': 'Bearer {}'.format(self.access_token)}
            data = {'multisig_wallet_address': self.address, 'multisig_wallet_provider': 'gnosis_safe', 'chain_id': self.network.value}
            # Make the POST request
            response = requests.post(enrolment_url, json=data, headers=headers)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Print the response content
                response_json = json.loads(response.text)
                response_text = HTML("<ansigreen>{response_text}</ansigreen>").format(response_text=json.dumps(response_json, indent=4))
                print_formatted_text(
                    response_text
                )
                return response.text
            else:
                # Print an error message if the request was not successful
                response_text = HTML("<ansired>Status code {response_code}: {response_text}</ansired>").format(response_code=response.status_code, response_text=response.text)
                print_formatted_text(
                    response_text
                )
                return ""
        except Exception as error:
            response_text = HTML("<ansired>Some error occurred when performing FailSafe Attestation Service Enrolment</ansired>")
            print_formatted_text(
                response_text
            )

    @fs_attestation_auth_decorator
    def fs_attestation_service_deploy_guard_contract(self) -> str:
        try:
            deploy_guard_contract_url = "{}/{}".format(self.fs_attestation_service_base_url, "attestation-service/safe-guard-contract-deployment")
            headers = {'Authorization': 'Bearer {}'.format(self.access_token)}
            data = {'multisig_wallet_address': self.address, 'chain_id': self.network.value}
            # Make the POST request
            response = requests.post(deploy_guard_contract_url, json=data, headers=headers)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Print the response content
                response_json = json.loads(response.text)
                response_text = HTML("<ansigreen>{response_text}</ansigreen>").format(response_text=json.dumps(response_json, indent=4))
                print_formatted_text(
                    response_text
                )
                return response.text
            else:
                # Print an error message if the request was not successful
                response_text = HTML("<ansired>Status code {response_code}: {response_text}</ansired>").format(response_code=response.status_code, response_text=response.text)
                print_formatted_text(
                    response_text
                )
                return ""
        except Exception as error:
            response_text = HTML("<ansired>Some error occurred when deploying Guard Contract for the Safe Multi-Sig Wallet</ansired>")
            print_formatted_text(
                response_text
            )

    @fs_attestation_auth_decorator
    def fs_attestation_service_set_constraints(self, signer_ip_address_constraints: list, expiry_time_constrint: str, risk_score_threshold_constraint: float) -> str:
        try:
            set_constraints_url = "{}/{}".format(self.fs_attestation_service_base_url, "attestation-service/constraints")
            headers = {'Authorization': 'Bearer {}'.format(self.access_token)}
            data = {'multisig_wallet_address': self.address, 'chain_id': self.network.value, 'constraints':{
                'signers': signer_ip_address_constraints,
                'expiry_time': {"unit": "d", "value": str(expiry_time_constrint)},
                'risk_score': risk_score_threshold_constraint
            }}

            # Make the POST request
            response = requests.post(set_constraints_url, json=data, headers=headers)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Print the response content
                response_json = json.loads(response.text)
                response_text = HTML("<ansigreen>{response_text}</ansigreen>").format(response_text=json.dumps(response_json, indent=4))
                print_formatted_text(
                    response_text
                )
                return response.text
            else:
                # Print an error message if the request was not successful
                response_text = HTML("<ansired>Status code {response_code}: {response_text}</ansired>").format(response_code=response.status_code, response_text=response.text)
                print_formatted_text(
                    response_text
                )
                return ""
        except Exception as error:
            response_text = HTML("<ansired>Some error occurred when setting FailSafe Attestation constraints for the Safe Multi-Sig Wallet</ansired>")
            print_formatted_text(
                response_text
            )

    @fs_attestation_auth_decorator
    def fs_attestation_settings(self, contact_email_address: str, slack_url: str) -> str:
        try:
            set_constraints_url = "{}/{}".format(self.fs_attestation_service_base_url, "attestation-service/settings")
            headers = {'Authorization': 'Bearer {}'.format(self.access_token)}
            data = {'multisig_wallet_address': self.address, 'chain_id': self.network.value, 'contact_email_address': contact_email_address, 'slack_url': slack_url}

            # Make the POST request
            response = requests.post(set_constraints_url, json=data, headers=headers)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Print the response content
                response_json = json.loads(response.text)
                response_text = HTML("<ansigreen>{response_text}</ansigreen>").format(response_text=json.dumps(response_json, indent=4))
                print_formatted_text(
                    response_text
                )
                return response.text
            else:
                # Print an error message if the request was not successful
                response_text = HTML("<ansired>Status code {response_code}: {response_text}</ansired>").format(response_code=response.status_code, response_text=response.text)
                print_formatted_text(
                    response_text
                )
                return ""
        except Exception as error:
            response_text = HTML("<ansired>Some error occurred when updating the FailSafe Attestation Service settings for the Safe Multi-Sig Wallet</ansired>")
            print_formatted_text(
                response_text
            )

    @fs_attestation_auth_decorator
    def fs_attestation_get_attestation_authority_wallet_address(self, silent_mode=False) -> str:
        try:
            get_attestation_wallet_address_url = "{}/{}".format(self.fs_attestation_service_base_url, "attestation-service/get-attestation-key")
            headers = {'Authorization': 'Bearer {}'.format(self.access_token)}
            params = {'multisig_wallet_address': self.address, 'chain_id': self.network.value}
            # Make the GET request
            response = requests.get(get_attestation_wallet_address_url, params=params, headers=headers)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Print the response content
                response_json = json.loads(response.text)
                response_text = HTML("<ansigreen>{response_text}</ansigreen>").format(response_text=json.dumps(response_json, indent=4))

                self.safe_cli_info.fs_attestation_service_attestation_authority_wallet_address = response_json['attestationWalletAddress']
                self.safe_cli_info.fs_attestation_service_attestation_authority_wallet_address_balance = Web3.from_wei(
                    self.ethereum_client.get_balance(response_json['attestationWalletAddress']), "ether"
                )
                
                if not silent_mode:
                    print_formatted_text(
                        response_text
                    )
                    return response.text
                else:
                    return response_json['attestationWalletAddress']
            else:
                if not silent_mode:
                    # Print an error message if the request was not successful
                    response_text = HTML("<ansired>Status code {response_code}: {response_text}</ansired>").format(response_code=response.status_code, response_text=response.text)
                    print_formatted_text(
                        response_text
                    )
                    return ""
                else:
                    return ""
        except Exception as error:
            if not silent_mode:
                response_text = HTML("<ansired>Some error occurred when retrieving FailSafe Attestation Authority Wallet address</ansired>")
                print_formatted_text(
                    response_text
                )

    @fs_attestation_auth_decorator
    def fs_attestation_get_attestation_constraints(self) -> str:
        try:
            get_attestation_service_enrolment_url = "{}/{}".format(self.fs_attestation_service_base_url, "attestation-service/get-enrolment")
            headers = {'Authorization': 'Bearer {}'.format(self.access_token)}
            params = {'multisig_wallet_address': self.address, 'chain_id': self.network.value}
            # Make the GET request
            response = requests.get(get_attestation_service_enrolment_url, params=params, headers=headers)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Print the response content
                response_json = json.loads(response.text)
                response_text = HTML("<ansigreen>{response_text}</ansigreen>").format(response_text=json.dumps(response_json['enrolment']['constraints'], indent=4))
                print_formatted_text(
                    response_text
                )
                return response.text
            else:
                # Print an error message if the request was not successful
                response_text = HTML("<ansired>Status code {response_code}: {response_text}</ansired>").format(response_code=response.status_code, response_text=response.text)
                print_formatted_text(
                    response_text
                )
                return ""
        except Exception as error:
            print(error)
            response_text = HTML("<ansired>Some error occurred when retrieving FailSafe Attestation Constraints</ansired>")
            print_formatted_text(
                response_text
            )

    def print_info(self):
        if self.safe_cli_info.fs_attestation_service_api_base_url:
            print_formatted_text(
                HTML(
                    f"<b><ansigreen>FS Attestation Service API Base URL</ansigreen></b>="
                    f"<ansiblue>{self._safe_cli_info.fs_attestation_service_api_base_url}</ansiblue>"
                )
            )

        if self.safe_cli_info.fs_attestation_service_attestation_authority_wallet_address:
            print_formatted_text(
                HTML(
                    f"<b><ansigreen>FS Attestation Authority Wallet Address</ansigreen></b>="
                    f"<ansiblue>{self.safe_cli_info.fs_attestation_service_attestation_authority_wallet_address}</ansiblue>"
                )
            )
        else:
            print_formatted_text(
                HTML(
                    f"<b><ansigreen>FS Attestation Authority Wallet Address</ansigreen></b>="
                    f"<ansired>Execute <b>fs_attestation_service_auth</b> command and then execute <b>info</b> command to see this info</ansired>"
                )
            )

        if self.safe_cli_info.fs_attestation_service_attestation_authority_wallet_address_balance:
            print_formatted_text(
                HTML(
                    f"<b><ansigreen>FS Attestation Authority Wallet Address Balance</ansigreen></b>="
                    f"<ansiblue>{self.safe_cli_info.fs_attestation_service_attestation_authority_wallet_address_balance}</ansiblue>"
                )
            )
        else:
            print_formatted_text(
                HTML(
                    f"<b><ansigreen>FS Attestation Authority Wallet Address Balance</ansigreen></b>="
                    f"<ansired>Execute <b>fs_attestation_service_auth</b> command and then execute <b>info</b> command to see this info</ansired>"
                )
            )

        
    def get_safe_cli_info(self) -> SafeCliInfo:
        fs_attestation_service_api_base_url = self.fs_attestation_service_base_url
        fs_attestation_service_attestation_authority_wallet_address = ""
        fs_attestation_service_attestation_authority_wallet_address_balance = ""


        current_time = int(time.time())
        # The Auth token issued by the FailSafe Attestation Service is valid for 10 minutes
        # If the token is nearing expiry time is less than 9 minutes, lets fetch attestationWalletAddress from the FailSafe Attestation Service API
        if hasattr(self, 'last_login_time') and (current_time - self.last_login_time <= 540):
            self.fs_attestation_user_login_internal()
            fs_attestation_service_attestation_authority_wallet_address = self.fs_attestation_get_attestation_authority_wallet_address(silent_mode=True)
            fs_attestation_service_attestation_authority_wallet_address_balance = Web3.from_wei(
                self.ethereum_client.get_balance(self.address), "ether"
            )

        return SafeCliInfo(
            fs_attestation_service_api_base_url,
            fs_attestation_service_attestation_authority_wallet_address,
            fs_attestation_service_attestation_authority_wallet_address_balance
        )
    
    @property
    def safe_cli_info(self) -> SafeCliInfo:
        if not self._safe_cli_info:
            self._safe_cli_info = self.refresh_safe_cli_info()
        return self._safe_cli_info

    def refresh_safe_cli_info(self) -> SafeCliInfo:
        self._safe_cli_info = self.get_safe_cli_info()
        return self._safe_cli_info
