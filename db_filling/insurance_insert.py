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

cursor.execute("SELECT vin from car")
record = cursor.fetchall()
print("Licenses from Database:- ", record)
car_vins = []
for i in record:
    car_vins.append(i[0])

cursor.execute("SELECT vin from insurance")
record = cursor.fetchall()
print("Licenses from Database:- ", record)
insurance_vins = []
for i in record:
    insurance_vins.append(i[0])

cursor.execute("SELECT osago from insurance")
record = cursor.fetchall()
print("Licenses from Database:- ", record)
osagos = []
for i in record:
    osagos.append(i[0])

cursor.execute("SELECT kasko from insurance")
record = cursor.fetchall()
print("Licenses from Database:- ", record)
kaskos = []
for i in record:
    kaskos.append(i[0])

for i in range(len(car_vins)):
    if car_vins[i] not in insurance_vins:
        vin = car_vins[i]

        osago = ''.join(random.sample(string.ascii_letters, 3)).upper() + ''.join(random.sample(string.digits, 10))
        while osago in osagos or osago[0] == '0':
            osago = ''.join(random.sample(string.ascii_letters, 3)).upper() + ''.join(random.sample(string.digits, 10))
        osagos.append(osago)

        kasko = ''.join(random.sample(string.digits, 4)) + ''.join(random.sample(string.digits, 9))
        kaskos.append(kasko)

        vin_temp = '\'' + vin + '\''
        cursor.execute(
            f"SELECT date_of_birth from person join passport using(passport_number) join car using(driver_license) where vin = {vin_temp}")
        record = cursor.fetchall()
        print("Licenses from Database:- ", record)
        start_date = 0
        for p in record:
            start_date = p[0]

        start_date = start_date + relativedelta(years=18)
        end_date = datetime.date(2023, 5, 23)
        num_days = (end_date - start_date).days
        rand_days = random.randint(1, num_days)
        date_of_issue_osago = start_date + datetime.timedelta(days=rand_days)

        random_period = [30, 60, 180, 360]

        date_expire_osago = random_period[random.randint(0, len(random_period) - 1)]

        num_days = (end_date - start_date).days
        rand_days = random.randint(1, num_days)
        date_of_issue_kasko = start_date + datetime.timedelta(days=rand_days)

        random_period = [30, 60, 180, 360]

        date_expire_kasko = random_period[random.randint(0, len(random_period) - 1)]

        result = '(\'' + str(vin) + '\',\'' + str(osago) + '\',\'' + str(kasko) + '\',\'' + str(
            date_of_issue_osago) + '\',' + str(
            date_expire_osago) + ',\'' + str(
            date_of_issue_kasko) + '\',' + str(
            date_expire_kasko) + ')'
        print(result)

        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO insurance (vin, osago, kasko, date_osago_start, osago_expiration_day, date_kasko_start, kasko_expiration_day) values {result}")
        connection.commit()
