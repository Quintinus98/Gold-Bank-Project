import os
import random
import sys

import pandas as pd

from ATM import welcome
from Validate import validateDetails2, validateLogin

filePath = r".\{}.csv".format("atm")
if not os.path.isfile(filePath) or os.path.getsize(filePath) == 0:
    df = pd.DataFrame({"firstName": [], "lastName": [], "email": [], "address": [], "accountNumber": [],
                       "password": [], "contact": []})
    df.to_csv(filePath, index=False)


def generateAccountNumber():
    accountNumber = random.randrange(1000000000, 9999999999)
    boolAccount = validateDetails2(accountNumber=accountNumber)  # Checks if account number has been used or not.

    if not boolAccount:  # Recreates account number until un-used account generated
        generateAccountNumber()
    print("Account number Validated!")
    return accountNumber  # Returns generated un-used account number.


def register():
    # To register, we need Name, Email, Account number, Password, Address, contact
    print("\n" + "-" * 15 + "REGISTRATION" + "-" * 15)
    welcomePrompt = "\nTake a few minutes to register an account with us.\n" \
                    "Please fill the following details as accurately as possible\n"
    print(welcomePrompt)
    firstName = input("Enter your First name: ")
    lastName = input("Enter your Last name: ")
    email = input("Enter your Email Address: ")
    address = input("Enter your Home Address: ")
    while True:             # Get contact until up to 11 digits is entered
        contact = input("Enter your Phone number: ")
        if len(contact) == 11:
            break
        else:
            print("Incorrect Phone number, try again.")
    boolValue = validateDetails2(contact=contact, email=email)  # Check if details exist
    if boolValue:
        print("\nGenerating Account Number...")
        accountNumber = str(generateAccountNumber())
        print("Your Account Number is", accountNumber)
        while True:
            password = input("Enter password (must be 8 digits or more): ")
            if len(password) >= 8:
                break
        print("\nPlease take note of your account number and password.\n")
        registration = {"firstName": firstName, "lastName": lastName, "email": email, "address": address,
                        "accountNumber": accountNumber, "password": password, "contact": contact, "Balance": 0}
        data = pd.read_csv(filePath, dtype=str)
        data = data.append(pd.DataFrame([registration]))
        data.to_csv(filePath, index=False)
        print("Registration Successful.\nRedirecting you to Login.")
    else:
        print("\nUser already exists, try login.")
    return login()


def login():
    print("\n" + "-" * 15 + "LOGIN" + "-" * 15)
    print("\nPlease fill in the following details.\n")
    accountNumber = input("Enter your account number: ")
    password = input("Enter your password: ")
    boolValue, userPosition = validateLogin(accountNumber=accountNumber, password=password)
    if boolValue:
        welcome(userPosition)
    else:
        retrieveAccount = input("Retrieve account number (yes/no): ")
        if retrieveAccount == 'yes':
            suggestion = retrieveAccountNumber()
            if suggestion:
                login()
            else:
                register()
    return main()


def retrieveAccountNumber():
    getEmail = input("Enter your email: ")
    getContact = input("Enter your Phone number: ")
    data = pd.read_csv(filePath, dtype=str)
    boolValue, pos = validateLogin(contact=getContact, email=getEmail)
    if boolValue:
        getAccount = data.loc[pos, "accountNumber"]
        print("Your account number is: {}".format(getAccount))
    else:
        print("Register an account!")
    return boolValue


def main():
    print("\n" + "-" * 15 + "GOLD BANK" + "-" * 15)
    print("Welcome to Gold Bank\n")

    print("1. Open an Account\n2. Login existing Account\n3. Exit")
    accountResponse = None
    try:
        accountResponse = int(input("\nSelect an option (1, 2, 3): "))
    except ValueError:
        print("Incorrect Value. Try again\n")

    if accountResponse == 1:
        register()
    elif accountResponse == 2:
        login()
    elif accountResponse == 3:
        sys.exit()
    else:
        main()


if __name__ == '__main__':          # start program
    main()
