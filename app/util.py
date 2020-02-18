import hashlib
import requests
import bcrypt

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def checkpw(password, password_hash):
    return bcrypt.checkpw(password, password_hash)

def get_price(ticker):
    with open("./credentials/credentials.txt","r") as file:
        credential = file.read()
        credential.strip()
        #TODO: get price from IEX Cloud API
        # print('https://cloud.iexapis.com/stable/tops?token={}symbols={}'.format(credential,ticker))
    response = requests.get('https://cloud.iexapis.com/stable/tops?token={}symbols={}'.format(credential,ticker))
    data = response.json()
    # print(data)
    # return 500.00/
    return data[0]["lastSalePrice"]
