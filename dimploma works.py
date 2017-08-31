# Задача: Вывести список групп в ВК в которых состоит пользователь, но не состоит никто из его друзей.
# 1. Получить список групп в которых состоит пользователь
# 2. Получить список друзей пользователей
# 3. Получить список груп в которых состоят друзья пользователя
# 4. Совместить два списка: группы пользователя и группы друзей пользователя

from pprint import pprint
from urllib.parse import urlencode
import requests

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

TOKEN = '2bcb0c9ad8fa316b02f9af34a2ac518721b1d1810a000a05d0a26d74257c0d977b81ba438da4518d0413e'

params = {
    'access_token': TOKEN,
    'v': VERSION,
    # 'user_id': 63364192
}

# Получаем список моих друзей
response_get_my_friends = requests.get('https://api.vk.com/method/friends.get', params).json()
friends_list = []
for friend in response_get_my_friends['response']['items']:
    friends_list.append(friend)

# Получаем список моих групп
response_get_my_groups = requests.get('https://api.vk.com/method/groups.get', params).json()
my_groups_list = []
for group in response_get_my_groups['response']['items']:
    my_groups_list.append(group)

# Получаем список групп моих друзей
friends_group_list = []
for friend in response_get_my_friends['response']['items']:
    params['user_id'] = friend
    response_friends_group = requests.get('https://api.vk.com/method/groups.get', params).json()
    for friends_group in response_friends_group['response']['items']:
        friends_group_list.append(friends_group)

print(len(friends_group_list))

        # params['user_id'] = "tim_leary"
    # get_friends = requests.get('https://api.vk.com/method/friends.get', params).json()
#     pprint(test)
    # pprint(get_friends)
    # print('{} | {}'.format(i, response['response']['items'])
    # for friends in get_friends['response']['items']:
    #     friends_list.append(friends)
    #     pprint(friends_list)