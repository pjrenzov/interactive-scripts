from web3 import Web3
import json,os
from web3.middleware import geth_poa_middleware

url = "https://polygon-mumbai.infura.io/v3/6e58cec88b6a447fb7d77bdf95a501ba"
w3 = Web3(Web3.HTTPProvider(url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract_addr = w3.toChecksumAddress(0xbFf293391b6798b9E2f3e80Deedc98B9f5da83Ad)
print(contract_addr)

account_addr = '0x447EC0076388DF3dDDCf86c5661F14f30422e5da'
Private_key = '485d182a600718da0c56756f808367a1faf223d48b4a9386bace972da8df53d7'



print("Connection: "+str(w3.isConnected()))
#private_key_hex = w3.toHex(Private_key)

acc = w3.eth.account.privateKeyToAccount(os.environ['PRIVATE_KEY'])
print(acc.address)

with open("bin/contracts/Game.json") as file:
    abi = json.load(file)
    abi = abi["abi"]

contract = w3.eth.contract(address=contract_addr, abi=abi)

tx = {
    'nonce' : w3.eth.getTransactionCount(account_addr),
    'value' : 1000
}
print("\n\n\n\n\n\n\n\n\n\n-----------------------------\n\n\n\n\n")
tx = contract.functions.registerAsClient(account_addr,1,"paras").buildTransaction(tx)

tx_hash = w3.eth.account.sign_transaction(tx,Private_key)
tx_id = w3.eth.send_raw_transaction(tx_hash.rawTransaction)
print(w3.toHex(tx_id))
