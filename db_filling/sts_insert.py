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

cursor.execute("SELECT passport_number from person")
record = cursor.fetchall()
print("Passports from Database:- ", record)
passports = []
for i in record:
    passports.append(i[0])

cursor.execute("SELECT sts_id from sts")
record = cursor.fetchall()
print("sts from Database:- ", record)
sts_exist = []
for i in record:
    sts_exist.append(i[0])

cursor.execute("SELECT sts_num from car")
record = cursor.fetchall()
print("car sts from Database:- ", record)
sts_car = []
for i in record:
    sts_car.append(i[0])

car_count = [0] * len(passports)
print(car_count)
y = 0
if len(passports) < len(sts_car):
    x = len(passports)
else:
    x = len(sts_car)
while y != x:
    car_count[random.randint(0, len(car_count) - 1)] += 1
    y += 1

for i in range(len(passports)):
    rand = random.randint(0, len(car_count) - 1)
    y = car_count[rand]
    car_count.pop(rand)

    for h in range(y):
        passport = passports[i]
        sts = sts_car[random.randint(0, len(sts_car) - 1)]
        while sts in sts_exist:
            sts = sts_car[random.randint(0, len(sts_car) - 1)]
        sts_exist.append(sts)

        cursor.execute(
            f"SELECT date_of_issue from person join driver_license on person.driver_license = driver_license.license_number where passport_number = {passport}")
        record = cursor.fetchall()
        start_date = 0
        for p in record:
            start_date = p[0]

        end_date = start_date + relativedelta(years=2)
        num_days = (end_date - start_date).days
        rand_days = random.randint(1, num_days)
        date_of_issue = start_date + datetime.timedelta(days=rand_days)

        while date_of_issue > datetime.date(2023, 5, 30):
            rand_days = random.randint(1, num_days)
            date_of_issue = start_date + datetime.timedelta(days=rand_days)

        result = '(\'' + str(sts) + '\',\'' + str(date_of_issue) + '\',' + str(passport) + ')'
        print(result)

        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO sts (sts_id, date_of_issue, passport_number) values {result}")
        connection.commit()
