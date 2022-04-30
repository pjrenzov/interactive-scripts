from web3 import Web3
import web3
import json,os
from web3.middleware import geth_poa_middleware

url = ["https://ropsten.infura.io/v3/6e58cec88b6a447fb7d77bdf95a501ba","http://127.0.0.1:8545"]
w3 = Web3(Web3.HTTPProvider(url[0]))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

if w3.isChecksumAddress(0x0B2A958E658F46148aC35710E18CEEf4b97fd3b2):
    contract_addr = 0x0B2A958E658F46148aC35710E18CEEf4b97fd3b2
if w3.isChecksumAddress(0x0B2A958E658F46148aC35710E18CEEf4b97fd3b2) == False:
    contract_addr = w3.toChecksumAddress('0x0B2A958E658F46148aC35710E18CEEf4b97fd3b2')

account_addr = w3.toChecksumAddress(0x825300CA897f56fFc91ee29dFC3B987B50177eb5)
Private_key = '485d182a600718da0c56756f808367a1faf223d48b4a9386bace972da8df53d7'

acc = w3.eth.account.privateKeyToAccount('485d182a600718da0c56756f808367a1faf223d48b4a9386bace972da8df53d7')
b = w3.eth.get_balance(acc.address)
print(f"\n\n\n\n\n\n\n\n\n\n-------------{b}----------------\n\n\n\n\n")

with open("bin/contracts/GameV2.json") as file:
    abi = json.load(file)
    abi = abi["abi"]

contract = w3.eth.contract(contract_addr, abi=abi)

tx_dict = {
    'from' : acc.address,
    'nonce' : w3.eth.getTransactionCount(acc.address),
    'value' : w3.toWei(2, 'Gwei'),
    "gasPrice": w3.eth.gas_price,
    #'maxFeePerGas':3000000000,
    #'maxPriorityFeePerGas':2000000000,
    #'gas':100000,
}
print("\n\n\n\n\n\n\n\n\n\n-----------------------------\n\n\n\n\n")
"""
tx = contract.functions.registerAsClient(1).buildTransaction(tx_dict)
sign_tx = w3.eth.account.sign_transaction(tx,private_key=Private_key)
tx_id = w3.eth.send_raw_transaction(sign_tx.rawTransaction)
i = w3.eth.wait_for_transaction_receipt(tx_id)
print(w3.toHex(tx_id))
"""

tx = contract.functions.mintClass(1000).buildTransaction(tx_dict)
sign_tx = w3.eth.account.sign_transaction(tx,private_key=Private_key)
tx_id = w3.eth.send_raw_transaction(sign_tx.rawTransaction)
i = w3.eth.wait_for_transaction_receipt(tx_id)
print(w3.toHex(tx_id))