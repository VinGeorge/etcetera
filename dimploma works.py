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
    'v': VERSION
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

    params_for_me = {
    'access_token': TOKEN,
    'v': VERSION}

    # params_for_me['count'] = 10
    params_for_me['extended'] = 1
    params_for_me['fields'] = 'members_count'
    response_get_my_friends = requests.get(api_get_friends, params_for_me).json()
    friends_list = []

    try:
        for friend in response_get_my_friends['response']['items']:
            friends_list.append(friend['id'])
    except KeyError:
        if response_get_my_friends['error']['error_code'] == 18:
            print('Error_code : 18')
        elif response_get_my_friends['error']['error_code'] == 6:
            time.sleep(0.4)
            get_friends_list()
    return friends_list


# Получаем список моих групп
def get_groups():
    groups = []

    params_for_me = {
    'access_token': TOKEN,
    'v': VERSION}

    params_for_me['extended'] = 1
    params_for_me['fields'] = 'members_count'
    params_for_me['id'] = 63364192
    response_get_my_groups = requests.get(api_get_group, params_for_me).json()

    try:
        for group in response_get_my_groups['response']['items']:
            groups.append({'Name': group['name'], 'id': group['id'], 'members_count': group['members_count']})
    except KeyError:
        if response_get_my_groups['error']['error_code'] == 18:
            print('Error_code : 18')
        elif response_get_my_groups['error']['error_code'] == 6:
            time.sleep(0.4)
            get_groups()
    return groups

# Получаем список групп моих друзей
def get_groups_friends():
    friends_groups_list = []

    params_for_friends = {
    'access_token': TOKEN,
    'v': VERSION}

    friends_list = get_friends_list()

    for i, friend in enumerate(friends_list):
        params_for_friends['count'] = 1000
        params_for_friends['user_id'] = friend
        response_friends_group = requests.get(api_get_group, params_for_friends).json()
        i += 1
        excess = (int(len(get_friends_list())) - i)
        print('Всего друзей - {}. Осталось проверить - {}'.format(len(friends_list), excess))

        try:
            for friends_group in response_friends_group['response']['items']:
                friends_groups_list.append(friends_group)
        except KeyError:
            if response_friends_group['error']['error_code'] == 18:
                print('Error_code : 18')
            elif response_friends_group['error']['error_code'] == 6:
                time.sleep(0.4)
                exception(params_for_friends, friends_groups_list)

    friends_groups_list = set(friends_groups_list)
    return friends_groups_list

def finish():
    new_list = []
    friends_groups_set = get_groups_friends()
    my_groups = get_groups()
    for i, group_one in enumerate(my_groups):
        if group_one['id'] not in friends_groups_set:
            new_list.append({'id': group_one['id'], 'Name': group_one['Name'], 'members_count': group_one['members_count']})
            i += 1
            total_group = int(len(my_groups))
            count = (i*100 // total_group)
            if count % 5 == 0:
                print('Осталось проверить {} %'.format(100-count))
    return new_list

pprint(finish())

# pprint(get_friends_list())
# pprint(get_groups())
# pprint(get_groups_friends())

def exception(params, test):
    response_friends_group = requests.get(api_get_group, params).json()
    try:
        for friends_group in response_friends_group['response']['items']:
            test.append(friends_group)
    except KeyError:
        if response_friends_group['error']['error_code'] == 18:
            print('Error_code : 18')
        elif response_friends_group['error']['error_code'] == 6:
            time.sleep(0.4)
            exception(params_for_friends, friends_groups_list)
    return