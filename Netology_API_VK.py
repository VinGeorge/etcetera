from urllib.parse import urlencode
import requests
from pprint import pprint

AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.67'
APP_ID = 6119577


auth_data = {
    'client_id': APP_ID,
    'redirect_uri': 'https://oauth.vk.com/blank.html',
    'display': 'mobile',
    'scope': 'friends, notify, status, wall',
    'response_type': 'token',
    'v': VERSION
}

print(urlencode(auth_data))
print('?'.join(
    (AUTHORIZE_URL, urlencode(auth_data))
))

TOKEN = '4f283d226ff2d97c2eb93d2790e94f8799d8fd197f309670ba545861e16fcad317917134e614310f73c08'

params = {
    'access_token': TOKEN,
    'v': VERSION,
    'user_id': '63364192'
}

response = requests.get('https://api.vk.com/method/friends.get', params).json()

pprint(response)

