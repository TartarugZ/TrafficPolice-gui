# import re
#
#
# def check(email):
#     regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
#     # pass the regular expression
#     # and the string into the fullmatch() method
#     if re.fullmatch(regex, email):
#         print("Valid Email")
#
#     else:
#         print("Invalid Email")
#
#
# check('e.sss@list.ru')
import json
from network_error import *
import requests

URL = 'http://25.39.214.241:8080'
session = requests.Session()
username = None
password = None
access_token = None


def update_tokens_policeman(callback, **args):
    global access_token
    body = {
        'username': 'П-516942',
        'password': 'qwerty'
    }
    response = session.post(url=f'{URL}/auth/token/policeman', json=body, timeout=7)
    response = json.loads(response.text)
    print(response)

    access_token = response['token']
    session.headers.update(
        {'Authorization': f'Bearer {access_token}'})
    return callback(**args)


def get_articles():
    try:
        response = session.get(
            url=f'{URL}/api/policeman/articles', timeout=7)
        if response.status_code == 401:
            raise NeedRefreshToken
        print(response.json())
        print('Articles info')
        return response.json()
    except NeedRefreshToken:
        update_tokens_policeman(get_articles)


def article_type_parser(article):
    temp = article[1:-1]
    temp = temp.split(',')
    state = 'ст. '
    point = 'п. '
    if temp[0] != '0':
        state = state + temp[0]
    if temp[1] != '0':
        if len(state) > 4:
            state = state + '.'
        state = state + temp[1]
    if temp[2] != '0':
        if len(state) > 4:
            state = state + '.'
        state = state + temp[2]
    if temp[3] != '0':
        point = point + temp[3]
    if temp[4] != '0':
        if len(point) > 3:
            point = point + '.'
        point = point + temp[4]
    return state + ' ' + point

get_articles()

