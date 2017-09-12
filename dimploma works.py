# Задача: Вывести список групп в ВК в которых состоит пользователь, но не состоит никто из его друзей.
# 1. Получить список групп в которых состоит пользователь
# 2. Получить список друзей пользователей
# 3. Получить список груп в которых состоят друзья пользователя
# 4. Совместить два списка: группы пользователя и группы друзей пользователя

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

params = {
    'access_token': TOKEN,
    'v': VERSION,
}

test = requests.get(api_get_friends, params)
print(test.status_code)


# params_for_one_friend = {
#     'access_token': TOKEN,
#     'v': VERSION,
#     'user_id': 2123372
# }


# Получаем список моих друзей
def get_friends_list():
    params_for_me = params
    params_for_me['count'] = 10
    params_for_me['extended'] = 1
    params_for_me['fields'] = 'members_count'
    response_get_my_friends = requests.get(api_get_friends, params_for_me).json()
    friends_list = []
    for friend in response_get_my_friends['response']['items']:
        friends_list.append(friend['id'])
    return friends_list


# Получаем список моих групп
def get_my_groups():
    groups = []
    params_for_me = params
    params_for_me['extended'] = 1
    params_for_me['fields'] = 'members_count'
    params_for_me['id'] = 63364192
    response_get_my_groups = requests.get(api_get_group, params_for_me).json()
    for group in response_get_my_groups['response']['items']:
        try:
            groups.append({'Name': group['name'], 'id': group['id'], 'members_count': group['members_count']})
        except Exception:
            time.sleep(0.400)
    return groups

# Получаем список групп моих друзей
def get_groups_friends():
    friends_groups_list = []
    params_for_friends = params
    # print(len(get_friends_list()))
    for i, friend in enumerate(get_friends_list()):
        params_for_friends['count'] = 1
        params['user_id'] = friend
        response_friends_group = requests.get(api_get_group, params_for_friends).json()
        # print(response_friends_group)
        # print('{} - {}'.format(i+1, friend))
        try:
            for friends_group in response_friends_group['response']['items']:
                friends_groups_list.append(friends_group)
        except KeyError:
            if response_friends_group['error']['error_code'] == 18:
                pass
            elif response_friends_group['error']['error_code'] == 6:
                time.sleep(1)
                continue
    return friends_groups_list

def get_set():
    test = []
    friends_group = get_groups_friends()
    for group in friends_group:
        test.append(group['id'])
    test = set(test)
    return test



def finish():
    new_list = []
    test = get_my_groups()
    for group_one in test:
        if group_one['id'] not in get_set():
            print('ВОООООТ ЭТОЙ ГРУППЫ НЕТ - {}'.format(group_one['Name']))
            new_list.append({'id': group_one['id'], 'Name': group_one['Name'], 'members_count': group_one['members_count']})
    return new_list

pprint(finish())


