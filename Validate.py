import pandas as pd
import numpy as np

filePath = r".\{}.csv".format("atm")


def validateDetails2(**details):
    data = pd.read_csv(filePath, dtype=str)
    storeBool = True
    print("")
    method = list(details.values())
    detail = list(details.keys())
    for i in range(len(detail)):
        if method[i] in data[detail[i]].values:
            print("The {} already exists".format(detail[i]))
            storeBool = False
    return storeBool


def validateLogin(**details):
    data = pd.read_csv(filePath, dtype=str)

    storeBool = True
    userPosition = None
    print("")
    method = list(details.values())     # get values of the dict details
    detail = list(details.keys())       # get keys of the dict details
    for i in range(len(detail)):        # iterate over the data's keys to find the values of the dictionary
        if method[i] not in data[detail[i]].values:
            print("{} not Found\n".format(detail[i].upper()))
            storeBool = False
    if storeBool:
        userPosition = int(np.where(data[detail[0]] == method[0])[0])
    return storeBool, userPosition
