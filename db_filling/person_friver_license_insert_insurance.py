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

cursor.execute(
    "SELECT license_number, category from car_user join insurance using(vin) join car using(vin)")
record = cursor.fetchall()
print("Licenses from Database:- ", record)
license_categories = []
for i in record:
    license_categories.append((i[0], i[1]))

cursor.execute("SELECT id, category_name from driver_license_categories")
record = cursor.fetchall()
print("Categories from Database:- ", record)
categories = []
for i in record:
    categories.append((i[0], i[1]))

cursor.execute("SELECT id, license_number from person_driver_license_categories")
record = cursor.fetchall()
print("exist_categories from Database:- ", record)
exist_categories = []
for i in record:
    exist_categories.append((i[0], i[1]))

for i in range(len(license_categories)):
    license_category = license_categories[i]
    category_letter = license_category[1]
    license_number = license_category[0]
    category_number = 0
    for p in categories:
        if p[1] == category_letter:
            category_number = p[0]
    if (category_number, license_number) not in exist_categories:
        license_number_temp = '\'' + str(license_number) + '\''
        cursor.execute(f"SELECT date_of_issue from driver_license where license_number = {license_number_temp}")
        record = cursor.fetchall()
        j = []
        for k in record:
            j.append(k[0])
        start_date = j[0]
        bb = j[0]
        for r in exist_categories:
            if r[1] == license_number:
                end_date = start_date + relativedelta(years=2)
                num_days = (end_date - start_date).days
                rand_days = random.randint(1, num_days)
                start_date = start_date + datetime.timedelta(days=rand_days)
        exist_categories.append((category_number, license_number))
        while start_date > datetime.date(2023, 6, 7):
            start_date = bb
            end_date = start_date + relativedelta(years=2)
            num_days = (end_date - start_date).days
            rand_days = random.randint(1, num_days)
            start_date = start_date + datetime.timedelta(days=rand_days)
        result = '(\'' + str(license_number) + '\',\'' + str(start_date) + '\',' + str(category_number) + ')'
        print(result)

        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO person_driver_license_categories (license_number, date_of_issue, id) values {result}")
        connection.commit()
