"""
Deploy VeriVisionRegistry contract to 0G Galileo testnet
"""

import os
import sys
import json
from pathlib import Path

from web3 import Web3


CONTRACT_ABI = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "name": "recordId", "type": "bytes32"},
            {"indexed": False, "name": "imageHash", "type": "string"},
            {"indexed": False, "name": "hallucinationCount", "type": "uint256"},
            {"indexed": False, "name": "verifier", "type": "address"},
        ],
        "name": "VerificationStored",
        "type": "event",
    },
    {
        "inputs": [
            {"name": "imageHash", "type": "string"},
            {"name": "vlmModel", "type": "string"},
            {"name": "verifierModel", "type": "string"},
            {"name": "objectCount", "type": "uint256"},
            {"name": "hallucinationCount", "type": "uint256"},
        ],
        "name": "storeVerification",
        "outputs": [{"name": "", "type": "bytes32"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"name": "recordId", "type": "bytes32"}],
        "name": "getRecord",
        "outputs": [
            {
                "components": [
                    {"name": "imageHash", "type": "string"},
                    {"name": "vlmModel", "type": "string"},
                    {"name": "verifierModel", "type": "string"},
                    {"name": "objectCount", "type": "uint256"},
                    {"name": "hallucinationCount", "type": "uint256"},
                    {"name": "timestamp", "type": "uint256"},
                    {"name": "verifier", "type": "address"},
                    {"name": "exists", "type": "bool"},
                ],
                "name": "",
                "type": "tuple",
            }
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "getRecordCount",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"name": "recordId", "type": "bytes32"}],
        "name": "getHallucinationRate",
        "outputs": [{"name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
]

CONTRACT_BYTECODE = "0x608060405234801561001057600080fd5b5061076a806100206000396000f3fe608060405234801561001057600080fd5b506004361061004c5760003560e01c806318913a8014610051578063570b7f2014610071578063a8e05e0f14610091578063e6b7b2a0146100a4575b600080fd5b61006461005f3660046104a0565b6100c4565b6040519081526020015b60405180910390f35b61008461007f3660046104a0565b6101a5565b60405161006e919061052b565b61006461009f3660046104a0565b6102a0565b6100b76100b23660046104a0565b610331565b60405161006e9190610589565b60008060006100d184610331565b90506000816001600160a01b03166318913a8060e01b856040516024016040516020818303038152906040529060e01b6020820180516001600160e01b03838183161783525050505060405161012891906105e7565b600060405180830381855afa9150503d8060008114610163576040519150601f19603f3d011682016040523d82523d6000602084013e610168565b606091505b50915091508161017957602061017d565b60010b90505b9392505050565b60606000826001600160a01b031663a8e05e0f60e01b846040516024016040516020818303038152906040529060e01b6020820180516001600160e01b0383818316178352505050506040516101e291906105e7565b600060405180830381855afa9150503d806000811461021d576040519150601f19603f3d011682016040523d82523d6000602084013e610222565b606091505b509150915081610233576020610237565b60010b90505b925050505b919050565b600080826001600160a01b031663570b7f2060e01b846040516024016040516020818303038152906040529060e01b6020820180516001600160e01b03838183161783525050505060405161029c91906105e7565b600060405180830381855afa9150503d80600081146102d7576040519150601f19603f3d011682016040523d82523d6000602084013e6102dc565b606091505b5091509150600080600093509350935050509193905550565b600060208181529081526040808320815180830190925280546001600160a01b039092168083526001600160a01b0319909316602084015260408301939093526060820192909252608090910190565b600080836001600160a01b031663e6b7b2a060e01b856040516024016040516020818303038152906040529060e01b6020820180516001600160e01b0383818316178352505050506040516103a991906105e7565b600060405180830381855afa9150503d80600081146103e4576040519150601f19603f3d011682016040523d82523d6000602084013e6103e9565b606091505b509150915060006103fb82840184610606565b905060005b84518110156104685784818151811061041b5761041b6106ba565b60200260200101516001600160a01b0316856001600160a01b0316036104565784818151811061044c5761044c6106ba565b602002602001015190505b80610460816106e6565b915050610400565b50949350505050565b6001600160a01b038116811461048557600080fd5b50565b634e487b7160e01b600052604160045260246000fd5b6000806000606084860312156104b457600080fd5b83356104bf81610470565b925060208401359150604084013567ffffffffffffffff8111156104e257600080fd5b8401601f810186136104f357600080fd5b803567ffffffffffffffff81111561050d5761050d610488565b8601828101908210858211171561052657610526610488565b6020928301955093505084013590509250925092565b6020808252825182820181905260009190848201906040850190845b8181101561057c5783516001600160a01b031683529284019291840191600101610557565b50909695505050505050565b6020808252825182820181905260009190848201906040850190845b8181101561057c5783518352928401929184019160010161059f565b6000825160005b818110156105e057602081860181015185830152016105c6565b506000920191825250919050565b60006020828403121561060057600080fd5b5051919050565b6000808585111561061757600080fd5b8386111561062457600080fd5b5050820193919092039150565b634e487b7160e01b600052601160045260246000fd5b600181811c9082168061065a57607f821691505b60208210810361067a57634e487b7160e01b600052602260045260246000fd5b50919050565b601f8211156106b5576000816000526020600020601f850160051c810160208610156106a85750805b601f850160051c820191505b828110156106c7578281556001016106b4565b5050505b505050565b634e487b7160e01b600052603260045260246000fd5b6000600182016106f857634e487b7160e01b600052601160045260246000fd5b506001019056"


def deploy_contract(rpc_url: str, private_key: str, chain_id: int = 16602):
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    assert w3.is_connected(), f"Cannot connect to 0G testnet at {rpc_url}"

    account = w3.eth.account.from_key(private_key)
    print(f"Deployer: {account.address}")
    print(f"Balance: {w3.eth.get_balance(account.address) / 1e18:.4f} 0G")

    contract = w3.eth.contract(abi=CONTRACT_ABI, bytecode=CONTRACT_BYTECODE)

    nonce = w3.eth.get_transaction_count(account.address)
    tx = contract.constructor().build_transaction({
        "nonce": nonce,
        "gas": 2000000,
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
    })

    signed = account.sign_transaction(tx)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    print(f"TX Hash: {tx_hash.hex()}")

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    contract_address = receipt.contractAddress
    print(f"Contract Address: {contract_address}")
    print(f"Explorer: https://chainscan-galileo.0g.ai/address/{contract_address}")

    deploy_info = {
        "contract_address": contract_address,
        "tx_hash": tx_hash.hex(),
        "deployer": account.address,
        "chain_id": chain_id,
        "explorer_url": f"https://chainscan-galileo.0g.ai/address/{contract_address}",
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
        sys.exit(1)
    deploy_contract(rpc, key)
