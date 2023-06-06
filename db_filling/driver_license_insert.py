import string
import json
import csv
import psycopg2
import datetime
from datetime import timedelta
import random
from russian_names import RussianNames

connection = psycopg2.connect(database="TrafficPolice", user="admin", password="root", host="25.39.214.241", port=5432)
cursor = connection.cursor()

cursor.execute("SELECT driver_license from person")
record = cursor.fetchall()
print("Licenses from Database:- ", record)
person_licenses = []
for i in record:
    person_licenses.append(i[0])

cursor.execute("SELECT license_number from driver_license")
record = cursor.fetchall()
print("Licenses from Database:- ", record)
driver_licenses = []

for i in record:
    driver_licenses.append(i[0])

for i in range(len(person_licenses)):
    if person_licenses[i] not in driver_licenses:
        license_number = person_licenses[i]

        unit_code = ''.join(random.sample(string.digits, 4))
        while unit_code[0] == '0':
            unit_code = ''.join(random.sample(string.digits, 4))

        start_date = datetime.date(2013, 7, 1)
        end_date = datetime.date(2023, 5, 23)
        num_days = (end_date - start_date).days
        rand_days = random.randint(1, num_days)
        random_date = start_date + datetime.timedelta(days=rand_days)

        result = '(' + str(license_number) + ',' + str(unit_code) + ',\'' + str(
            random_date) + '\')'
        print(result)

        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO driver_license (license_number, unit_code, date_of_issue) values {result}")
        connection.commit()
