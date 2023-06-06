import csv
import psycopg2
import datetime
import random
from dateutil.relativedelta import relativedelta
from faker import Faker

fms = []
with open("fms_unit.csv", encoding='utf-8') as r_file:
    file_reader = csv.DictReader(r_file, delimiter=",")
    for row in file_reader:
        fms.append((row["code"], row["name"]))

connection = psycopg2.connect(database="TrafficPolice", user="admin", password="root", host="25.39.214.241", port=5432)
cursor = connection.cursor()

cursor.execute("SELECT passport_number from person")
record = cursor.fetchall()
print("Passports from Database:- ", record)
person_passports = []
for i in record:
    person_passports.append(i[0])

cursor.execute("SELECT passport_number from passport")
record = cursor.fetchall()
print("Passports from Database:- ", record)
passport_passports = []
for i in record:
    passport_passports.append(i[0])

fake = Faker("ru_RU")

for i in range(len(person_passports)):
    if person_passports[i] not in passport_passports:

        passport_number = person_passports[i]

        start_date = datetime.date(1955, 7, 1)
        end_date = datetime.date(1995, 7, 1)
        num_days = (end_date - start_date).days
        rand_days = random.randint(1, num_days)
        date_of_birth = start_date + datetime.timedelta(days=rand_days)

        this_fms = fms[random.randint(0, len(fms)-1)]
        unit, unit_code = this_fms[1], this_fms[0]

        registration = fake.address()

        start_date = date_of_birth + relativedelta(years=18)
        end_date = datetime.date(2023, 6, 1)
        num_days = (end_date - start_date).days
        rand_days = random.randint(1, num_days)
        date_of_issue = start_date + datetime.timedelta(days=rand_days)

        result = '(' + str(passport_number) + ',\'' + str(date_of_birth) + '\',\'' + str(unit) + '\',' + str(
            unit_code) + ',\'' + str(registration) + '\',\'' + str(date_of_issue) + '\')'
        print(result)

        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO passport (passport_number, date_of_birth, unit, unit_code, place_of_registr, date_of_issue) values {result}")
        connection.commit()
