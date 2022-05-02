from functions.mint import Mint
from functions.register import RegisterClient
#from brownie import accounts


def main():
    print("$____________________WELCOME TO THE PORTAL___________________________$")
    print("$_______________________MAKE YOUR CHOICE_____________________________$")
    print("1) Register as a Client")
    print("2) Mint a Token Class")
    choice = int(input("Enter Your choice here :"))
    if choice == 1:
        RegisterClient()
    else:
        Mint()

main()