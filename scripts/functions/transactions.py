from web3 import Web3
import json,os,pathlib
from web3.middleware import geth_poa_middleware

def tranfer(source, destination, amount, tokenName):
    with open("config.json") as file:
            config = json.load(file)

    w3 = Web3(Web3.HTTPProvider(config["URL"]["ropsten"]))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    source = w3.toChecksumAddress(source)
    destination = w3.toChecksumAddress(destination)

    acc = w3.eth.account.privateKeyToAccount('485d182a600718da0c56756f808367a1faf223d48b4a9386bace972da8df53d7')

    tx_dict = {
    'from' : acc.address,
    'nonce' : w3.eth.getTransactionCount(acc.address),
    #'value' : w3.toWei(2, 'Gwei'),
    "gasPrice": w3.eth.gas_price,
    #'maxFeePerGas':3000000000,
    #'maxPriorityFeePerGas':2000000000,
    #'gas':100000,
    }

    with open("bin/contracts/GameV2.json") as file:
        abi = json.load(file)
        abi = abi["abi"]

    contract = w3.eth.contract(config["contract_addr"], abi=abi)

    tx = contract.functions.tranferToken(destination,source,tokenName,amount).buildTransaction(tx_dict)
    sign_tx = w3.eth.account.sign_transaction(tx,private_key=acc.key)
    tx_id = w3.eth.send_raw_transaction(sign_tx.rawTransaction)
    i = w3.eth.wait_for_transaction_receipt(tx_id)

    print("tranfer confirmed!")
    return

def used(account, tokenName, amount):
    with open("config.json") as file:
            config = json.load(file)

    w3 = Web3(Web3.HTTPProvider(config["URL"]["ropsten"]))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    acc = w3.eth.account.privateKeyToAccount('485d182a600718da0c56756f808367a1faf223d48b4a9386bace972da8df53d7')

    tx_dict = {
    'from' : acc.address,
    'nonce' : w3.eth.getTransactionCount(acc.address),
    #'value' : w3.toWei(2, 'Gwei'),
    "gasPrice": w3.eth.gas_price,
    #'maxFeePerGas':3000000000,
    #'maxPriorityFeePerGas':2000000000,
    #'gas':100000,
    }

    with open("bin/contracts/GameV2.json") as file:
        abi = json.load(file)
        abi = abi["abi"]

    with open(f"data/Tokens/{tokenName}.json", "w") as file:
        destination = w3.toChecksumAddress(json.load(file)["owner"])

    contract = w3.eth.contract(config["contract_addr"], abi=abi)

    tx = contract.functions.tranferToken(destination,w3.toChecksumAddress(account),tokenName,amount).buildTransaction(tx_dict)
    sign_tx = w3.eth.account.sign_transaction(tx,private_key=acc.key)
    tx_id = w3.eth.send_raw_transaction(sign_tx.rawTransaction)
    i = w3.eth.wait_for_transaction_receipt(tx_id)

