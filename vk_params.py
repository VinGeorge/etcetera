

def read_token_file(file_name):
    file_opened = open(file_name, 'r')
    TOKEN = file_opened.read()
    return TOKEN

def file_name():
    token_file_name = input("THE TOKEN FILE NAME IS -> ")
    if token_file_name is None:
        token_file_name = 'TOKEN.py'
    return token_file_name

TOKEN = read_token_file(file_name())

def make_vk_params(**kwargs):
    VERSION = '5.67'

    params = {
        'access_token': TOKEN,
        'v': VERSION,
    }
    params.update(kwargs)
    return params