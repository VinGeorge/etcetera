from pprint import pprint
from urllib.parse import urlencode

import requests

AUTHORIZE_URL = 'https://oauth.yandex.ru/authorize'
APP_ID = 'a655eeac5d7c4b5b8c1f70ac42e43acd'

auth_data = {
    'response_type': 'token',
    'client_id': APP_ID
}

# print('?'.join((AUTHORIZE_URL, urlencode(auth_data))))

# TOKEN = 'AQAAAAANIfuDAAR0dfPWw9ZBqEGnoiTSWQDgxLE'


class ApiYandexMetrika:

    def __init__(self, TOKEN):
        self.TOKEN = TOKEN

    def get_headers(self):
        return {
            'Authorization': 'OAuth {}'.format(self.TOKEN),
            'Content-Type': 'application/x-yametrika+json'
        }

    def get_counters(self):
        url = 'https://api-metrica.yandex.ru/management/v1/counters'
        headers = self.get_headers()
        response = requests.get(url, headers=headers)
        counters = response.json()['counters']
        return counters

    def get_counter_data(self, counter_id):
        url = 'https://api-metrika.yandex.ru/stat/v1/data'
        headers = self.get_headers()
        params = {
            'id': counter_id,
            'metrics': 'ym:s:visits',
            # 'views': "ym:s:pageviews",
            # 'users': "ym:s:users"
        }
        response = requests.get(url, params, headers = headers)
        return response.json()


ym = ApiYandexMetrika('AQAAAAANIfuDAAR1CuoCLJJPYEkWiEPhL2bAoao')
counters = ym.get_counters()
ids = [c['id'] for c in counters]
pprint(ym.get_counter_data(ids[0]))

