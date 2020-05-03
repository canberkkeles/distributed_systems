import requests
from flask import Flask,request
from flask_restful import Resource,Api

API_URL = "http://10.36.54.157:5000/number_game/"

LEFT_BOUND = 0
RIGHT_BOUND = (2 ** 64) - 1
MID = (LEFT_BOUND + RIGHT_BOUND) // 2

# print(str(MID))
counter = 0
while True:
    response = requests.get(API_URL + str(MID))
    if response.ok:
        result = response.json()

        if result == "success":
            print(MID)
            break

        elif result == "greater" :
            # print("greater")
            LEFT_BOUND = MID

        elif result == "smaller" :
            # print("smaller")
            RIGHT_BOUND = MID

        MID = (LEFT_BOUND + RIGHT_BOUND) // 2
    """
    else:
        print("Response failed!")
        break
    """




