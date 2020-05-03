import requests

API_URL = 'http://127.0.0.1:5000'

response = requests.get(API_URL)
if response.ok:
    result = response.json()
    secret = result['secret']
    print(secret)
