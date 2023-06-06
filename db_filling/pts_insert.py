import string
import json
import csv
import psycopg2
import datetime
from datetime import timedelta
import random

from dateutil.relativedelta import relativedelta
from russian_names import RussianNames

connection = psycopg2.connect(database="TrafficPolice", user="admin", password="root", host="25.39.214.241", port=5432)
cursor = connection.cursor()

cursor.execute("SELECT pts_num from car")
record = cursor.fetchall()
print("pTS from Database:- ", record)
pts_car = []
for i in record:
    pts_car.append(i[0])

cursor.execute("SELECT pts_id from pts")
record = cursor.fetchall()
print("Licenses from Database:- ", record)
pts_exist = []
for i in record:
    pts_exist.append(i[0])

for i in record:
    pts_exist.append(i[0])

for i in range(len(pts_car)):
    if pts_car[i] not in pts_exist:
        pts = pts_car[i]
        pts_temp = '\'' + pts + '\''

        start_date = datetime.date(2000, 7, 1)
        end_date = datetime.date(2023, 1, 23)
        num_days = (end_date - start_date).days
        rand_days = random.randint(1, num_days)
        date_of_issue = start_date + datetime.timedelta(days=rand_days)

        result = '(\'' + str(pts) + '\',\'' + str(date_of_issue) + '\'' + ')'
        print(result)

        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO pts (pts_id, date_of_issue) values {result}")
        connection.commit()
