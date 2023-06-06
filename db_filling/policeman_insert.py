import string
import json
import csv
import psycopg2
import datetime
from datetime import timedelta
import random
from russian_names import RussianNames

posts = ['Старший государственный инспектор безопасности дорожного движения',
         'Старший инспектор дорожно-патрульной службы', 'Государственный инспектор безопасности дорожного движения',
         'Инспектор дорожно-патрульной службы']

ranks = ['Мл. сержант', 'Сержант', 'Ст. сержант', 'Мл. сержант', 'Сержант', 'Ст. сержант', 'Мл. лейтенант', 'Лейтенант',
         'Ст. лейтенант', 'Капитан']

letters = ['А', 'Б', 'В', 'Г', 'Е', 'И', 'К', 'Л', 'М', 'П', 'С', 'Т', 'Ш', '', '', '', '', '', '']

connection = psycopg2.connect(database="TrafficPolice", user="admin", password="root", host="25.39.214.241", port=5432)
cursor = connection.cursor()

cursor.execute("SELECT full_name from policeman")
record = cursor.fetchall()
print("Full name number from Database:- ", record)
names = []
for i in record:
    names.append(i[0])

cursor.execute("SELECT area_id from area")
record = cursor.fetchall()
print("areas number from Database:- ", record)
areas = []
for i in record:
    areas.append(i[0])

cursor.execute("SELECT police_id from policeman")
record = cursor.fetchall()
print("ids from Database:- ", record)
ids = []
for i in record:
    ids.append(i[0])

n = 222
for i in range(n):
    police_id = letters[random.randint(0, len(letters) - 1 - round(len(letters) / 2))] + letters[
        random.randint(round(len(letters) / 2), len(letters) - 1)] + '-' + ''.join(
        random.sample(string.digits, 6))
    while police_id in ids:
        police_id = letters[random.randint(0, len(letters) - 1 - round(len(letters) / 2))] + letters[
            random.randint(round(len(letters) / 2), len(letters) - 1)] + '-' + ''.join(
            random.sample(string.digits, 6))

    full_name = RussianNames().get_person(gender=0.95)

    area_id = areas[random.randint(0, len(areas) - 1)]

    post = posts[random.randint(0, len(posts) - 1)]

    rank = ranks[random.randint(0, len(ranks) - 1)]

    result = '(\'' + str(police_id) + '\',' + str(area_id) + ',\'' + str(
        full_name) + '\',\'' + str(post) + '\',\'' + str(rank) + '\')'
    print(result)

    cursor = connection.cursor()
    cursor.execute(
        f"INSERT INTO policeman (police_id, area_id, full_name, post, rank) values {result}")
    connection.commit()
