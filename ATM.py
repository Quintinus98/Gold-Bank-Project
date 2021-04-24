import pandas as pd
import sys


filePath = r".\{}.csv".format("atm")


def welcome(pos):
    print("\n" + "-" * 15 + "WELCOME" + "-" * 15)
    data = pd.read_csv(filePath, dtype={'contact': str})

    fullName = str(data['firstName'][pos] + " " + data['lastName'][pos])
    print("Dear {}, welcome to Gold Bank.".format(fullName))
    print("At Gold Bank, your investments are safe.\nWe offer "
          "the following services:")
    print("1. Deposit \n2. Withdrawal \n3. Transfer \n4. Balance \n5. Exit")
    response = None
    try:
        response = int(input("Select an Option (1 - 5): "))
    except ValueError:
        print("Incorrect value entered, try again")
        welcome(pos)

    mode = ['Deposit', 'Withdrawal']
    if response == 1:
        depositAndWithdrawal(pos, mode[0])
    elif response == 2:
        depositAndWithdrawal(pos, mode[1])
    elif response == 3:
        transfer(pos)
    elif response == 4:
        balance(pos)
    elif response == 5:
        sys.exit()
    else:
        print("Your option does not exist. Try again.")
        welcome(pos)
    return None


def handleDepositWithdrawal(pos, mode):
    data = pd.read_csv(filePath, dtype={'contact': str})

    if mode == "Withdrawal":
        maxWithdrawal = data.loc[pos, 'Balance']
        print("Max withdrawal is N{}".format(maxWithdrawal))
        withdraw_deposit = float(input("How much %s do you want to make: " % mode))
        if withdraw_deposit < 0:
            print("\nNo negative withdrawals.\n")
            return handleDepositWithdrawal(pos, mode)
        elif withdraw_deposit > maxWithdrawal:
            print("\nYou cannot withdraw more than N{}\n".format(maxWithdrawal))
            return handleDepositWithdrawal(pos, mode)
        return withdraw_deposit
    elif mode == 'Deposit':
        print("Max deposit is N5million")
        withdraw_deposit = float(input("How much %s do you want to make: " % mode))
        maxDeposit = 5000000
        if withdraw_deposit < 0:
            print("\nNo negative deposits.")
            return handleDepositWithdrawal(pos, mode)
        elif withdraw_deposit > maxDeposit:
            print("\nYou cannot deposit more than N5million at once.")
            print("...This feature is coming soon...\n")
            return handleDepositWithdrawal(pos, mode)
        return withdraw_deposit
    print("Just to fulfill, return 0")
    return 0


def depositAndWithdrawal(pos, mode):
    print("\n" + "-" * 15 + "{}".format(mode) + "-" * 15)
    data = pd.read_csv(filePath, dtype={'contact': str})

    withdraw_deposit = float(handleDepositWithdrawal(pos, mode))

    print("\nYour {} of N{} was successful".format(mode, withdraw_deposit))
    if mode == "Withdrawal":
        withdraw_deposit *= -1

    data.loc[pos, 'Balance'] += withdraw_deposit

    print("Available Balance: N{}".format(data.loc[pos, 'Balance']))
    data.to_csv(filePath, index=False)
    response = input("\nWould you like to perform another transaction? (yes/no): ")

    if response in ['y', 'yes', 'Yes']:
        welcome(pos)
    elif response in ['n', 'no', 'No']:
        print("You have been logged out!")
        from AtmAccount import main
        main()
    else:
        sys.exit()


def balance(pos):
    data = pd.read_csv(filePath, dtype={'contact': str})
    accountBalance = data.loc[pos, 'Balance']
    print("\nCurrent Balance: N" + str(accountBalance))

    response = input("\nWould you like to perform another transaction? (yes/no): ")

    if response in ['y', 'yes', 'Yes']:
        welcome(pos)
    elif response in ['n', 'no', 'No']:
        print("You have been logged out!")
        from AtmAccount import main
        main()
    else:
        sys.exit()


def transfer(pos):
    print("\n" + "-" * 15 + "Transfer" + "-" * 15)
    from Validate import validateLogin

    transferAccount = input("Enter Transfer account number: ")
    boolValue, posTransfer = validateLogin(accountNumber=transferAccount)
    data = pd.read_csv(filePath, dtype={'contact': str})

    if boolValue:
        maxTransfer = data.loc[pos, 'Balance']
        print("\nMaximum allowable transfer is N{}".format(maxTransfer))
        transferValue = 0
        for _ in range(3):
            transferValue = float(input("Enter transfer amount: "))
            if transferValue < 0:
                print("No negative transfers.")
            elif transferValue > maxTransfer:
                print("You cannot transfer more than you have (N{})".format(maxTransfer))
            else:
                print("Transfer of N{} was successful".format(transferValue))
                break
        data.loc[posTransfer, 'Balance'] += transferValue
        data.loc[pos, 'Balance'] -= transferValue
        data.to_csv(filePath, index=False)
    else:
        print("You entered an Invalid account number")
    return welcome(pos)
