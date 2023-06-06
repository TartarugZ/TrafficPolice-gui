import string
import json
import csv
import psycopg2
import datetime
from datetime import timedelta
import random
from russian_names import RussianNames

companies = []
with open('jobs.txt', 'r', encoding='utf-8') as f:
    save = f.readlines()

    for p in save:
        p = p[:-1]
        while '\'' in p:
            p = p.replace('\'', '')
        if p == 'Яндек':
            p = 'Яндекс'
        companies.append(p)

codes = [900, 901, 902, 903, 904, 905, 906, 908, 909, 910, 911, 912, 913, 914, 915, 916, 917, 918, 919, 920, 921, 922,
         923, 924, 925, 926, 927, 928, 929, 930, 931, 932, 933, 934, 936, 937, 938, 939, 941, 950, 951, 952, 953, 955,
         956, 958, 960, 961,
         962, 963, 964, 965, 966, 967, 968, 969, 970, 971, 977, 978, 980, 981, 982, 983, 984, 985, 986, 987, 988, 989,
         991, 992, 993, 994, 995, 996, 997, 999]

connection = psycopg2.connect(database="TrafficPolice", user="admin", password="root", host="25.39.214.241", port=5432)
cursor = connection.cursor()

cursor.execute("SELECT driver_license from person")
record = cursor.fetchall()
print("Licenses from Database:- ", record)
licenses = []
for i in record:
    licenses.append(i[0])

cursor.execute("SELECT passport_number from person")
record = cursor.fetchall()
print("Passports from Database:- ", record)
passports = []
for i in record:
    passports.append(i[0])

cursor.execute("SELECT phone_number from person")
record = cursor.fetchall()
print("Phone number from Database:- ", record)
phones = []
for i in record:
    phones.append(i[0])

n = 0
for i in range(n):

    passport_number = ''.join(random.sample(string.digits, 10))
    while passport_number in passports or passport_number[0] == '0':
        passport_number = ''.join(random.sample(string.digits, 10))
    passports.append(passport_number)

    license_number = ''.join(random.sample(string.digits, 10))
    while license_number in licenses or license_number[0] == '0':
        license_number = ''.join(random.sample(string.digits, 10))
    licenses.append(license_number)

    phone_number = '8' + str(codes[random.randint(0, len(codes)-1)]) + ''.join(random.sample(string.digits, 7))
    while phone_number in phones:
        phone_number = ''.join(random.sample(string.digits, 10))
    phones.append(phone_number)

    job_info = '8' + str(codes[random.randint(0, len(codes)-1)]) + ''.join(random.sample(string.digits, 7)) + ',' + \
               companies[
                   random.randint(0, len(companies))]

    full_name = RussianNames().get_person()
    full_name = full_name.split(' ')
    print(full_name)
    name = full_name[0]
    pytr = full_name[1]
    surname = full_name[2]

    result = '(' + str(passport_number) + ',' + str(license_number) + ',' + str(phone_number) + ',\'' + str(
        job_info) + '\',\'' + pytr + '\',\'' + name + '\',\'' + surname + '\')'
    print(result)

    cursor = connection.cursor()
    cursor.execute(
        f"INSERT INTO person (passport_number, driver_license, phone_number, job_info, patronymic, person_name, surname) values {result}")
    connection.commit()
