from web3 import Web3
import json,os,pathlib
from web3.middleware import geth_poa_middleware
from functions.uploadMetadata import makeMetaData

def Mint():
    print("Nice so we will be seeing another NFT class!")
    username = str(input("Before proceeding please enter your username: "))

    with open("config.json") as file:
        config = json.load(file)

    with open(f"data/Clients/{username}.json") as file:
        client_data = json.load(file)

    w3 = Web3(Web3.HTTPProvider(config["URL"]["ropsten"]))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    tokenName = str(input("Enter the name of token class: "))
    totalSupply = int(input("Enter supply: "))
    discription = str(input("Enter token discription: "))
    image = str(input("Enter image URL: "))

    Private_key = os.getenv("PRIVATE_KEY")
    acc = w3.eth.account.privateKeyToAccount('485d182a600718da0c56756f808367a1faf223d48b4a9386bace972da8df53d7')
    
    tx_dict = {
    'from' : acc.address,
    'nonce' : w3.eth.getTransactionCount(acc.address),
    'value' : w3.toWei(2, 'Gwei'),
    "gasPrice": w3.eth.gas_price,
    #'maxFeePerGas':3000000000,
    #'maxPriorityFeePerGas':2000000000,
    #'gas':100000,
    }

    with open("bin/contracts/GameV2.json") as file:
        abi = json.load(file)
        abi = abi["abi"]

    contract = w3.eth.contract(config["contract_addr"], abi=abi)

    makeMetaData(tokenName, discription, image, str(contract.caller.currentTokenCount()))
    
    tx = contract.functions.mintClass(w3.toChecksumAddress(client_data["public_address"]),totalSupply,tokenName).buildTransaction(tx_dict)
    sign_tx = w3.eth.account.sign_transaction(tx,private_key=acc.key)
    tx_id = w3.eth.send_raw_transaction(sign_tx.rawTransaction)
    i = w3.eth.wait_for_transaction_receipt(tx_id)

    with open(f"data/Tokens/sample.json") as file:
        sample = json.load(file)
    with open(f"data/Tokens/{tokenName}.json", "w") as file:
        sample['name'] = tokenName
        sample['totalSupply'] = totalSupply
        sample['ID'] = contract.caller.getCurrentTokenCount() - 1
        sample['owner'] = client_data['public_address']
        json.dump(sample, file)
    with open(f"data/Clients/{username}.json", "a") as file:
        client_data = json.load(file)
        client_data["tokens"][tokenName] = contract.caller.getCurrentTokenCount() - 1
        json.dump(client_data, file)
    return
