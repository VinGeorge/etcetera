from pprint import pprint
from urllib.parse import urlencode
import requests
import time

with open('/Users/yvdsd/SandBox/TOKEN.py', 'rb') as f:
    TOKEN = f.read()

VERSION = '5.67'

api_get_group = 'https://api.vk.com/method/groups.get'
api_get_friends = 'https://api.vk.com/method/friends.get'

# Получаем токен
def get_token():
    AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
    APP_ID = 6166373

    auth_data = {
        'client_id': APP_ID,
        'redirect_uri': 'https://oauth.vk.com/blank.html',
        'display': 'mobile',
        'scope': 'friends, groups',
        'response_type': 'token',
        'v': VERSION
    }
    print(urlencode(auth_data))
    print('?'.join(
        (AUTHORIZE_URL, urlencode(auth_data))
    ))
    return

get_token()

params_all = {'access_token': TOKEN}

class CallAPI():
    def __init__(self, method, params):
        self.url =  'https://api.vk.com/method/'
        self.method = method
        self.params = params
        self.params['VERSION'] = '5.67'

    def response(self):
        try:
            response = requests.get(''.join([self.url, self.method]), self.params).json()
            if 'error' in response:
                if response['error']['error_code'] == 6:
                    time.sleep(0.4)
                    response(self)
                elif response['error']['error_code'] == 18:
                    raise Exception(response)
        except Exception:
            print('Critical error - {}'.format(response['error']['error_msg']))
            pass

        return response

def get_friends(user_id):
    params = params_all
    params['count'] = 10
    params['extended'] = 1
    method = 'friends.get'

    dict_response = CallAPI(method, params).response()

    friends_set = dict_response['response']

    return friends_set

def get_group(user_id):
    params = params_all
    params['extended'] = 1
    params['fields'] = 'members_count'
    params['user_id'] = user_id
    method = 'groups.get'

    groups_response = CallAPI(method, params).response()

    groups = groups_response['response']

    friends_groups=[]

    try:
        for group in groups[1:]:
            friends_groups.append({'id': group['gid'], 'Name': group['name'], 'members_count': group['members_count']})
    except KeyError:
        pass
        # if group['deactivated'] == True:

    return friends_groups


# pprint(get_group(123289))
# pprint(get_friends(6166373))

def get_friends_groups(id):
    new_list = []

    for friend_id in get_friends(id):
        # pprint(friend_id)
        # print(get_group(friend_id))
        for friend_groups in get_group(friend_id):
            pprint(friend_groups)
    return

get_friends_groups(6166373)
