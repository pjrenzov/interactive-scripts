from functions.access import check, getBalance
from functions.transactions import used, tranfer


def main():
    print("Welcome to stimulation!")
    acc = str(input("Please enter your account address: "))
    if check(acc, "User")==False:
        print("Not a user")
        return
    print("Nice to have you back")
    print(f'You have Gold - {getBalance(acc, "Gold")} ')
    print(f'You have GoldBonus - {getBalance(acc, "GoldBonus")} ')
    print("Enter 1 to use x1 gold")
    print("Enter 2 to use Bonus")
    res = int(input("Response: "))
    if res == 1:
        used(acc, "Gold", 1)
        print(f'your new Gold balance is {getBalance(acc, "Gold")}')
    else:
        if check(acc, "GoldBonus") == False:
            print("You do not have gold bonus")
            return
        tranfer("0x6970A5a3a188D176BB2AE6bb7CE1b4bdD40bfacA",acc, 10, "Gold")
        used(acc, "GoldBonus", 1)
        print("Bonus used. Wait for 20 mins to see changes")

main()