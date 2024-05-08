import setuptools

from safe_cli.version import version

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="fs_attestation_safe_cli",
    version=version,
    author="Mohan",
    author_email="mohan@ethlas.com",
    description="Modified Command Line Interface for FailSafe Attestation Service to administrate Gnosis Safe Wallets and FailSafe Attestation Guard Contracts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gnosis/safe-cli",
    download_url="https://github.com/gnosis/safe-cli/releases",
    license="MIT",
    test_suite="tests",
    install_requires=[
        "art>=6",
        "colorama>=0.4",
        "prompt_toolkit>=3",
        "pygments>=2",
        "requests>=2",
        "fs-attestation-safe-eth-py==1.0.3",
        "tabulate>=0.8",
    ],
    extras_require={"ledger": ["ledgereth==0.9.1"], "trezor": ["trezor==0.13.8"]},
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "fs-attestation-safe-cli=safe_cli.main:main",
            "safe-creator=safe_cli.safe_creator:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
