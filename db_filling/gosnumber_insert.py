import string
import json
import csv
import psycopg2
import datetime
from datetime import timedelta
import random

from dateutil.relativedelta import relativedelta
from russian_names import RussianNames

rus_alph = 'АВЕКМНОРСТУХ'
regions = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,
    29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44,
    45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60,
    61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76,
    77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91,
    92, 93, 94, 95, 96, 97, 98, 99, 102, 113, 116, 121, 122, 123, 124, 125,
    126, 134, 136, 138, 142, 147, 150, 152, 154, 155, 156, 159, 161, 163, 164, 173,
    174, 177, 178, 186, 190, 193, 196, 197, 198, 199, 702, 750, 716, 761, 763, 774,
    777, 790, 797, 799, 977]

connection = psycopg2.connect(database="TrafficPolice", user="admin", password="root", host="25.39.214.241", port=5432)
cursor = connection.cursor()

cursor.execute("SELECT number from gosnumber")
record = cursor.fetchall()
print("Numbers from Database:- ", record)
numbers = []
for i in record:
    numbers.append(i[0])

cursor.execute("SELECT vin from car")
record = cursor.fetchall()
print("Car vins from Database:- ", record)
vins = []
for i in record:
    vins.append(i[0])

cursor.execute("SELECT vin from gosnumber")
record = cursor.fetchall()
print("Gosnumber vins from Database:- ", record)
vins_exist = []
for i in record:
    vins_exist.append(i[0])

for i in range(len(vins)):
    if vins[i] not in vins_exist:
        vin = vins[i]

        number = rus_alph[random.randint(0, len(rus_alph) - 1)] + ''.join(random.sample(string.digits, 3)) + rus_alph[
            random.randint(0, len(rus_alph) - 1)] + rus_alph[random.randint(0, len(rus_alph) - 1)]

        region = regions[random.randint(0, len(regions) - 1)]

        result = '(\'' + str(number) + '\',' + str(region) + ',\'' + str(vin) + '\')'
        print(result)

        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO gosnumber (number, region_code, vin) values {result}")
        connection.commit()
