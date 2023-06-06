import string
import json
import csv
import psycopg2
import datetime
from datetime import timedelta
import random
from russian_names import RussianNames

marks = []
models = []
colors = []

with open("cars.csv", encoding='utf-8') as r_file:
    file_reader = csv.DictReader(r_file, delimiter=",")
    for row in file_reader:
        marks.append(row["mark"])
        models.append(row["model"])
        colors.append(row["color"])

marks = list(set(marks))
models = list(set(models))
colors = list(set(colors))

car_types = ["Легковой автомобиль", "Грузовой автомобиль", "Автобус", "Мотоцикл"]
car_categories = ['A', 'B', 'C', 'D']

connection = psycopg2.connect(database="TrafficPolice", user="admin", password="root", host="25.39.214.241", port=5432)
cursor = connection.cursor()

cursor.execute("SELECT vin from car")
record = cursor.fetchall()
print("Car from Database:- ", record)
vins = []
for i in record:
    vins.append(i[0])

cursor.execute("SELECT sts_num from car")
record = cursor.fetchall()
print("STS from Database:- ", record)
sts_exist = []
for i in record:
    sts_exist.append(i[0])

cursor.execute("SELECT pts_num from car")
record = cursor.fetchall()
print("Licenses from Database:- ", record)
pts_exist = []
for i in record:
    pts_exist.append(i[0])

n = 0
for i in range(n):

    vin = ''.join(random.sample(string.ascii_letters, 2)).upper() + ''.join(
        random.sample(string.digits, 1)) + ''.join(random.sample(string.ascii_letters, 2)).upper() + ''.join(
        random.sample(string.digits, 6)) + ''.join(
        random.sample(string.digits, 6))
    if vin not in vins:

        mark_and_model = str(
            marks[random.randint(0, len(marks) - 1)] + ' ' + models[random.randint(0, len(models) - 1)])

        color = colors[random.randint(0, len(colors) - 1)]

        car_type = car_types[random.randint(0, len(car_types) - 1)]

        car_category = car_categories[random.randint(0, len(car_categories) - 1)]

        if car_type == 'Легковой автомобиль':
            car_category = 'B'
        elif car_type == 'Грузовой автомобиль':
            car_category = 'C'
        elif car_type == 'Мотоцикл':
            car_category = 'A'
        elif car_type == 'Автобус':
            car_category = 'D'

        engine_info = certificate = ''.join(random.sample(string.ascii_letters, 2)).upper() + ''.join(
            random.sample(string.digits, 1)) + ''.join(
            random.sample(string.ascii_letters, 1)).upper() + ''.join(
            random.sample(string.digits, 6))

        sts = ''.join(random.sample(string.digits, 10))
        while sts in sts_exist or sts[0] == '0':
            sts = ''.join(random.sample(string.digits, 10))
        sts_exist.append(sts)

        pts = ''.join(random.sample(string.digits, 2)) + ''.join(
            random.sample(string.ascii_letters, 2)).upper() + ''.join(
            random.sample(string.digits, 6))
        while pts in pts_exist or pts[0] == '0':
            pts = ''.join(random.sample(string.digits, 2)) + ''.join(
                random.sample(string.ascii_letters, 2)).upper() + ''.join(
                random.sample(string.digits, 6))
        pts_exist.append(pts)

        for o in range(len(marks)):
            while mark_and_model == marks[o] + ' ' + models[0]:
                mark_and_model = str(
                    marks[random.randint(0, len(marks) - 1)] + ' ' + models[random.randint(0, len(models) - 1)])

        result = '(\'' + str(vin) + '\',\'' + str(mark_and_model) + '\',\'' + str(
            color) + '\',\'' + str(car_type) + '\',\'' + str(car_category) + '\',\'' + str(
            engine_info) + '\',\'' + str(
            sts) + '\',\'' + str(pts) + '\')'
        print(result)

        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO car (vin, mark_and_model, color, car_type, category, engine_info, sts_num, pts_num) values {result}")
        connection.commit()
