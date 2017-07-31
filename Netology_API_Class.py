from pprint import pprint
import requests
from urllib.parse import urlencode

import requests

AUTHORIZE_URL = 'https://oauth.yandex.ru/authorize'
APP_ID = '322df0d4993341be907ff3ca4bfb2b7a'

auth_data = {
    'response_type': 'token',
    'client_id': APP_ID
}

print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))

TOKEN = 'AQAAAAANIfuDAAR0dfPWw9ZBqEGnoiTSWQDgxLE'


def get_counter():
    url = 'https://api-metrica.yandex.ru/management/v1/counters'
    headers = {
        'Authorization': 'OAuth {}'.format(TOKEN),
        'Content-Type': 'application/x-yametrika+json'
    }
    response = requests.get(url, headers=headers)
    print(response.status_code)
    pprint(response.json())


get_counter()
