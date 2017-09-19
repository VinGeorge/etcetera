# Задача: Вывести список групп в ВК в которых состоит пользователь, но не состоит никто из его друзей.
# 1. Получить список групп в которых состоит пользователь
# 2. Получить список друзей пользователей
# 3. Получить список груп в которых состоят друзья пользователя
# 4. Совместить два списка: группы пользователя и группы друзей пользователя

from pprint import pprint
from urllib.parse import urlencode
import requests
import time
import json

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
print('Статус страницы - {}'.format(test.status_code))

def do_request(url, params):
    while True:
        res = requests.get(url, params).json()
        if 'error' in res:
            if res['error']['error_code'] == 6:
                time.sleep(0.4)
                continue
            elif res['error']['error_code'] == 18:
                return None
            else:
                print('{}'.format(res['error']['error_msg']))
                break
        else:
            return res

# params_for_one_friend = {
#     'access_token': TOKEN,
#     'v': VERSION,
#     'user_id': 2123372
# }


# Получаем список моих друзей
def get_friends_list():

    params_for_me = params

    # params_for_me['count'] = 100
    params_for_me['extended'] = 1
    params_for_me['fields'] = 'members_count'
    friends_list = []
    response_get_my_friends = do_request(api_get_friends, params_for_me)
    for friend in response_get_my_friends['response']['items']:
        friends_list.append(friend['id'])
    # if 'error' in response_get_my_friends:
    #     do_request(api_get_friends, params_for_me)
    # else:
    #     for friend in response_get_my_friends['response']['items']:
    #         friends_list.append(friend['id'])
    return friends_list


# Получаем список моих групп
def get_groups():
    groups = []

    params_for_me = params

    params_for_me['extended'] = 1
    params_for_me['fields'] = 'members_count'
    params_for_me['id'] = 63364192
    response_get_my_groups = do_request(api_get_group, params_for_me)
    for group in response_get_my_groups['response']['items']:
        groups.append({'Name': group['name'], 'id': group['id'], 'members_count': group['members_count']})
    # response_get_my_groups = requests.get(api_get_group, params_for_me).json()
    # if 'error' in response_get_my_groups:
        # do_request(api_get_group, params_for_me)
    # else:
        # for group in response_get_my_groups['response']['items']:
            # groups.append({'Name': group['name'], 'id': group['id'], 'members_count': group['members_count']})
    return groups

# Получаем список групп моих друзей
def get_groups_friends():
    friends_groups_list = []

    params_for_friends = {
    'access_token': TOKEN,
    'v': VERSION
    }

    friends_list = get_friends_list()

    for i, friend in enumerate(friends_list):
        params_for_friends['count'] = 1000
        params_for_friends['user_id'] = friend
        i += 1
        excess = (int(len(get_friends_list())) - i)
        print('Всего друзей - {}. Осталось проверить - {}'.format(len(friends_list), excess))
        response_friends_group = do_request(api_get_group, params_for_friends)
        # pprint(response_friends_group)
        if response_friends_group is None:
            continue
        else:
            for friends_group in response_friends_group['response']['items']:
                friends_groups_list.append(friends_group)
        # response_friends_group = requests.get(api_get_group, params_for_friends).json()
        # if 'error' in response_friends_group:
        #     do_request(api_get_group, params_for_friends)
        # else:
        #     for friends_group in response_friends_group['response']['items']:
        #         friends_groups_list.append(friends_group)

    friends_groups_list = set(friends_groups_list)
    return friends_groups_list

def finish():
    new_list = []
    friends_groups_set = get_groups_friends()
    my_groups = get_groups()
    for group_one in my_groups:
        if group_one['id'] not in friends_groups_set:
            new_list.append({'id': group_one['id'], 'Name': group_one['Name'], 'members_count': group_one['members_count']})
    with open('new_file.json', 'w') as f:
        json.dump(new_list, f)
    return new_list

pprint(finish())

# pprint(get_friends_list())
# pprint(get_groups())
# pprint(get_groups_friends())


# do_request(api_get_group, params)