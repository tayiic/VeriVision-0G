"""
Deploy VeriVisionRegistry to 0G Galileo Testnet (Chain ID: 16602)

Compiles from Solidity source at deploy time — no pre-compiled bytecode.
"""

import os
import sys
import json
from pathlib import Path

from web3 import Web3


def _compile_contract():
    """Compile VeriVisionRegistry.sol from source using solcx."""
    try:
        from solcx import compile_standard, install_solc, set_solc_version
    except ImportError:
        print("Installing py-solc-x...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "py-solc-x"])
        from solcx import compile_standard, install_solc, set_solc_version

    solc_version = "0.8.20"
    try:
        set_solc_version(solc_version)
    except Exception:
        print(f"Installing solc {solc_version}...")
        install_solc(solc_version)
        set_solc_version(solc_version)

    sol_path = Path(__file__).parent.parent / "contracts" / "VeriVisionRegistry.sol"
    if not sol_path.exists():
        print(f"ERROR: Contract not found at {sol_path}")
        sys.exit(1)

    source = sol_path.read_text(encoding="utf-8")

    compiled = compile_standard(
        {
            "language": "Solidity",
            "sources": {"VeriVisionRegistry.sol": {"content": source}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "evm.bytecode.object"]}
                },
                "optimizer": {"enabled": True, "runs": 200},
            },
        },
        solc_version=solc_version,
    )

    contract = compiled["contracts"]["VeriVisionRegistry.sol"]["VeriVisionRegistry"]
    abi = contract["abi"]
    bytecode = contract["evm"]["bytecode"]["object"]

    print(f"Compiled VeriVisionRegistry.sol (solc {solc_version})")
    print(f"  Bytecode size: {len(bytecode)//2} bytes")
    return abi, bytecode


def deploy_contract(rpc_url: str, private_key: str, chain_id: int = 16602):
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        print(f"ERROR: Cannot connect to 0G testnet at {rpc_url}")
        sys.exit(1)

    account = w3.eth.account.from_key(private_key)
    balance = w3.eth.get_balance(account.address)
    print(f"Deployer: {account.address}")
    print(f"Balance:  {balance / 1e18:.4f} 0G")

    if balance == 0:
        print("ERROR: Zero balance. Get testnet tokens from https://faucet.0g.ai/")
        sys.exit(1)

    abi, bytecode = _compile_contract()

    contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    nonce = w3.eth.get_transaction_count(account.address)
    gas_price = w3.eth.gas_price

    tx = contract.constructor().build_transaction({
        "nonce": nonce,
        "gas": 2000000,
        "gasPrice": gas_price,
        "chainId": chain_id,
    })

    estimated_gas = tx.get("gas", 2000000)
    estimated_cost = (estimated_gas * gas_price) / 1e18
    print(f"Estimated gas: {estimated_gas}  (cost: ~{estimated_cost:.6f} 0G)")

    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"TX Hash: {tx_hash.hex()}")

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = receipt.contractAddress
    explorer_url = f"https://chainscan-galileo.0g.ai/address/{contract_address}"

    print(f"Contract:  {contract_address}")
    print(f"Explorer:  {explorer_url}")

    deploy_info = {
        "contract_address": contract_address,
        "tx_hash": tx_hash.hex(),
        "deployer": account.address,
        "chain_id": chain_id,
        "explorer_url": explorer_url,
    }

    info_path = Path(__file__).parent / "deploy_info.json"
    with open(info_path, "w") as f:
        json.dump(deploy_info, f, indent=2)
    print(f"\nDeployment info saved to {info_path}")

    return contract_address


if __name__ == "__main__":
    rpc = os.environ.get("0G_RPC_URL", "https://evmrpc-testnet.0g.ai")
    key = os.environ.get("0G_PRIVATE_KEY", "")
    if not key:
        print("ERROR: Set 0G_PRIVATE_KEY environment variable")
        print("  PowerShell: $env:0G_PRIVATE_KEY='your_private_key_without_0x_prefix'")
        sys.exit(1)
    deploy_contract(rpc, key)
