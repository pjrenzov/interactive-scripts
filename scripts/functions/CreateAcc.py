def createWeb3Account(w3):
    generated_account = w3.eth.account.create()
    account_addr = generated_account.address
    account_private_key = w3.toHex(generated_account.key)
    return account_addr, account_private_key