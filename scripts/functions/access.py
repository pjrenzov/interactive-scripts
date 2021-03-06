from web3 import Web3
import json,os,pathlib
from web3.middleware import geth_poa_middleware

def check(account, tokenName, condition = 1):
    with open("config.json") as file:
            config = json.load(file)

    w3 = Web3(Web3.HTTPProvider(config["URL"]["ropsten"]))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    account = w3.toChecksumAddress(account)

    with open("bin/contracts/GameV2.json") as file:
        abi = json.load(file)
        abi = abi["abi"]

    contract = w3.eth.contract(config["contract_addr"], abi=abi)

    with open(f"data/Tokens/{tokenName}.json", "r") as file:
        id = json.load(file)
        id = id["ID"]

    if contract.caller.balanceOf(account,id) >= condition:
        return True
    return False

def getBalance(account, tokenName):
    with open("config.json") as file:
            config = json.load(file)

    w3 = Web3(Web3.HTTPProvider(config["URL"]["ropsten"]))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    account = w3.toChecksumAddress(account)

    with open("bin/contracts/GameV2.json") as file:
        abi = json.load(file)
        abi = abi["abi"]

    contract = w3.eth.contract(config["contract_addr"], abi=abi)

    with open(f"data/Tokens/{tokenName}.json", "r") as file:
        id = json.load(file)["ID"]
    
    return contract.caller.balanceOf(account,id)