import requests

API_URL = 'http://127.0.0.1:5000'

item_name = 'test-item'
endpoint = '{}/{}'.format(API_URL, item_name)

if __name__ == '__main__':
    response = requests.get(endpoint)
    if not response.ok:
        print('item does not exist')

    response = requests.put(endpoint, data={'content': 'Design 2nd Assignment'})
    if response.ok:
        print('item created')

    response = requests.get(endpoint)
    if response.ok:
        content = response.json()
        print('item content: {}'.format(content))
