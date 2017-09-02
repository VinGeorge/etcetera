# Задача: Вывести список групп в ВК в которых состоит пользователь, но не состоит никто из его друзей.
# 1. Получить список групп в которых состоит пользователь
# 2. Получить список друзей пользователей
# 3. Получить список груп в которых состоят друзья пользователя
# 4. Совместить два списка: группы пользователя и группы друзей пользователя

from pprint import pprint
from urllib.parse import urlencode
import requests
import time

AUTHORIZE_URL = 'https://oauth.vk.com/authorize'
VERSION = '5.67'
APP_ID = 6166373

auth_data = {
    'client_id': APP_ID,
    'redirect_uri': 'https://oauth.vk.com/blank.html',
    'display': 'mobile',
    'scope': 'friends, notify, status, groups, wall',
    'response_type': 'token',
    'v': VERSION
}
print(urlencode(auth_data))
print('?'.join(
    (AUTHORIZE_URL, urlencode(auth_data))
))

TOKEN = '2dad8380aeec77a8b2ba128ab5aa773842110de1824faf8801385090b68316a4d1ea6e6859245fe3afb53'

params_for_me = {
    'access_token': TOKEN,
    'v': VERSION,
    'extended': 1,
    'fields': 'members_count',
    # 'count':
}

params_for_one_friend = {
    'access_token': TOKEN,
    'v': VERSION,
    'user_id': 2123372
}

# params для групп
params_for_friends = {
    'access_token': TOKEN,
    'v': VERSION,
    'count': 1000
}


# Получаем список моих друзей
def get_friends_list():
    response_get_my_friends = requests.get('https://api.vk.com/method/friends.get', params_for_me).json()
    friends_list = []
    for friend in response_get_my_friends['response']['items']:
        friends_list.append(friend['id'])
    return friends_list


# Получаем список моих групп
groups = []
response_get_my_groups = requests.get('https://api.vk.com/method/groups.get', params_for_me).json()
for group in response_get_my_groups['response']['items']:
    try:
        groups.append({'Name': group['name'], 'id': group['id'], 'members_count': group['members_count']})
    except Exception:
        time.sleep(2)


# Список групп одного друга
# friend_groups = []
# one_friends_group_list = requests.get('https://api.vk.com/method/groups.get', params_for_one_friend).json()
# friend_group_list = one_friends_group_list['response']['items']
# for id in friend_group_list:
#     try:
#         friend_groups.append(id)
#     except Exception:
#         time.sleep(2)


# Получаем список групп моих друзей
friends_groups_list = []
for friend in get_friends_list():
    params_for_friends['user_id'] = friend
    response_friends_group = requests.get('https://api.vk.com/method/groups.get', params_for_friends).json()
    print('...')
    try:
        for friends_group in response_friends_group['response']['items']:
            friends_groups_list.append(friends_group)
    except Exception:
        time.sleep(2)

new_list = []
for group_one in groups:
    if group_one['id'] not in friends_groups_list:
        new_list.append({'id': group_one['id'], 'Name': group_one['Name'], 'members_count': group_one['members_count']})

pprint(new_list)

# new_list = []
# for group_one in groups:
#     if group_one['id'] not in friend_groups:
#         new_list.append({'id': group_one['id'], 'Name': group_one['Name'], 'members_count': group_one['members_count']})
#
# pprint(new_list)