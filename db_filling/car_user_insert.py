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

cursor.execute("SELECT vin, license_number from car_user")
record = cursor.fetchall()
print("car_user from Database:- ", record)
car_users = []
for i in record:
    car_users.append((i[0], i[1]))

cursor.execute("SELECT vin from insurance")
record = cursor.fetchall()
print("VINs from insurance from Database:- ", record)
insurance_vins = []
for i in record:
    insurance_vins.append(i[0])

cursor.execute("SELECT driver_license from person")
record = cursor.fetchall()
print("License numbers from person from Database:- ", record)
license_numbers = []
for i in record:
    license_numbers.append(i[0])

for i in range(len(insurance_vins)):

    p = random.randint(0, 3)
    for j in range(p):
        vin = insurance_vins[i]
        license_number = license_numbers[random.randint(0, len(license_numbers) - 1)]
        license_number_temp = '\'' + str(license_number) + '\''
        cursor.execute(f"SELECT vin from insurance join car using(vin) join person using(driver_license) where driver_license={license_number_temp}")
        record = cursor.fetchall()
        temp = 0
        for x in record:
            temp = (x[0])
        while temp == vin:
            license_number = license_numbers[random.randint(0, len(license_numbers) - 1)]
            license_number_temp = '\'' + str(license_number) + '\''
            cursor.execute(
                f"SELECT vin from insurance join car using(vin) join person using(driver_license) where driver_license={license_number_temp}")
            record = cursor.fetchall()
            temp = 0
            for x in record:
                temp = (x[0])
        while (vin, license_number) in car_users:
            license_number = license_numbers[random.randint(0, len(license_numbers) - 1)]
            license_number_temp = '\'' + str(license_number) + '\''
            cursor.execute(
                f"SELECT vin from insurance join car using(vin) join person using(driver_license) where driver_license={license_number_temp}")
            record = cursor.fetchall()
            temp = 0
            for x in record:
                temp = (x[0])
            while temp == vin:
                license_number = license_numbers[random.randint(0, len(license_numbers) - 1)]
                license_number_temp = '\'' + str(license_number) + '\''
                cursor.execute(
                    f"SELECT vin from insurance join car using(vin) join person using(driver_license) where driver_license={license_number_temp}")
                record = cursor.fetchall()
                temp = 0
                for x in record:
                    temp = (x[0])
        car_users.append((vin, license_number))
        result = '(\'' + str(vin) + '\',' + str(license_number) + ')'
        print(result)

        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO car_user (vin, license_number) values {result}")
        connection.commit()
