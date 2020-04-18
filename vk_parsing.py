from pprint import pprint
from urllib.parse import urlencode
import requests
import time
import json
import os
import vk_params

VERSION = '5.67'
API_GET_GROUP = 'https://api.vk.com/method/groups.get'
API_GET_FRIENDS = 'https://api.vk.com/method/friends.get'
AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
ERROR_REQUESTS = 6
ERROR_PAGES = 18
APP_ID = 6166373


# Получаем ссылку на токен
def get_token(file_name):
    token_file_path = os.path.realpath(file_name)
    if os.path.exists(token_file_path) is False:

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

# Запрос статуса страницы
# test = requests.get(api_get_friends, make_vk_params())
# print('Статус страницы - {}'.format(test.status_code))

# Обработка возникающих ошибок
def do_request(url, params):
    while True:
        res = requests.get(url, params).json()
        if 'error' in res:
            if res['error']['error_code'] == ERROR_REQUESTS:
                time.sleep(0.04)
                continue
            elif res['error']['error_code'] == ERROR_PAGES:
                return None
            else:
                print('{}'.format(res['error']['error_msg']))
                break
        else:
            return res

# Получаем список моих друзей
def get_friends_list():
    params = {
        'extended': 1,
        'fields': 'members_count',
    }
    params_for_me = vk_params.make_vk_params(**params)
    friends_list = []
    response_get_my_friends = do_request(API_GET_FRIENDS, params_for_me)
    for friend in response_get_my_friends['response']['items']:
        friends_list.append(friend['id'])
    return friends_list

# Получаем список моих групп
def get_groups():
    groups = []
    params = {'extended': 1,
              'fields':'members_count',
              'id': 63364192
              }
    params_for_me = vk_params.make_vk_params(**params)
    response_get_my_groups = do_request(API_GET_GROUP, params_for_me)
    for group in response_get_my_groups['response']['items']:
        groups.append({'Name': group['name'], 'id': group['id'], 'members_count': group['members_count']})
    return groups

# Получаем список групп моих друзей
def get_groups_friends():
    friends_groups_list = []
    friends_list = get_friends_list()
    friends_count = len(friends_list)
    for i, friend in enumerate(friends_list):
        params = {
            'count': 1000,
            'user_id': friend
        }
        params_for_friends = vk_params.make_vk_params(**params)
        excess = friends_count - i
        print('Всего друзей - {}. Осталось проверить - {}'.format(friends_count, excess))
        response_friends_group = do_request(API_GET_GROUP, params_for_friends)
        if response_friends_group is None:
            continue
        else:
            friends_groups_list.extend(response_friends_group['response']['items'])
    friends_groups_set = set(friends_groups_list)
    return friends_groups_set

# Основная функция
def main():
    get_token(vk_params.file_name())
    private_groups = []
    friends_groups_set = get_groups_friends()
    my_groups = get_groups()
    for group_one in my_groups:
        if group_one['id'] not in friends_groups_set:
            private_groups.append({'id': group_one['id'], 'Name': group_one['Name'], 'members_count': group_one['members_count']})
    with open('new_file.json', 'w') as f:
        json.dump(private_groups, f)
    return private_groups


main()



