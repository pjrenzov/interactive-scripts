from web3 import Web3
import json,os,pathlib
from web3.middleware import geth_poa_middleware
from functions.CreateAcc import createWeb3Account

def Register():

    with open("config.json") as file:
        config = json.load(file)

    w3 = Web3(Web3.HTTPProvider(config["URL"]["ropsten"]))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)

    print("Honored to know you want to be a part of community!!!\n")
    print("-------------------------------------------------------")
    response = str(input("To begin please tell us if you have web3 account?y/n:\t"))

    if response == "n":
        
        print("No worries let us make an account for you....")
        user_addr, user_private_key = createWeb3Account(w3)
        print("We have created your web3 account---")
        print(f"Account Address : {user_addr}")
        print(f"Private Key : {user_private_key}")
        print("Make sure to keep details secure.\n Please add some funds to it and repeat the process.\n We respect your privacy and do not possess any details of it!")
        return
        
    else:
        user_private_key = str(input("Great! please enter your private key :"))
    
    username = str(input("Enter your prefered username : \t"))
    
    acc = w3.eth.account.privateKeyToAccount(user_private_key)

    with open("bin/contracts/GameV2.json") as file:
        abi = json.load(file)
        abi = abi["abi"]

    contract = w3.eth.contract(config["contract_addr"], abi=abi)

    tx_dict = {
        'from' : acc.address,
        'nonce' : w3.eth.getTransactionCount(acc.address),
        'value' : w3.toWei(2, 'Gwei'),
        "gasPrice": w3.eth.gas_price,
        #'maxFeePerGas':3000000000,
        #'maxPriorityFeePerGas':2000000000,
        #'gas':100000,
    }

    tx = contract.functions.registerAsClient(contract.caller.currentClientCount()).buildTransaction(tx_dict)
    sign_tx = w3.eth.account.sign_transaction(tx,private_key=user_private_key)
    tx_hash = w3.eth.send_raw_transaction(sign_tx.rawTransaction)
    i = w3.eth.wait_for_transaction_receipt(tx_hash)
    tx_id = w3.toHex(tx_hash)

    with open(f"data/Clients/sample.json") as file:
        sample = json.load(file)

    with open(f"data/Clients/{username}.json", "w") as file:
        sample["name"] = username
        sample["ID"] = contract.caller.currentClientCount()
        sample["ID"] -=1
        sample["public_address"] = acc.address
        user_id = sample["ID"]
        json.dump(sample, file)
        
    print(f"Congrats you have been registered. You Client ID is {user_id}")
    return