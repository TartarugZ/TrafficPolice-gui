import csv
import psycopg2
import datetime
import random
from dateutil.relativedelta import relativedelta
from faker import Faker
reason_text = ['Это больше не повторится! Отпустите, пожалуйста!', 'За чо грабите народ родной?!', "Денег нет! Но вы держитесь!", "Доказательства спорные! А где презумпция невиновности!"]
case_verdict = ['Произошло нарушение, выписан штраф']

connection = psycopg2.connect(database="TrafficPolice", user="admin", password="root", host="25.39.214.241", port=5432)
cursor = connection.cursor()

cursor.execute("SELECT passport_number, vin, driver_license from person join sts using(passport_number) join car on sts.sts_id = car.sts_num")
record = cursor.fetchall()
print("pn vin from Database:- ", record)
pn_vin = []
for i in record:
    pn_vin.append(i)

cursor.execute("SELECT article_id, description from article")
record = cursor.fetchall()
print("art desc from Database:- ", record)
a_d = []
for i in record:
    a_d.append(i)

cursor.execute("SELECT police_id, address, camera_id from policeman join camera using(area_id) join area using(area_id)")
record = cursor.fetchall()
print("pac from Database:- ", record)
pac = []
for i in record:
    pac.append(i)

n = 10
for i in range(n):
    random_article = random.randint(0, len(a_d) - 1)
    random_area = random.randint(0, len(pac) - 1)
    p_vin = random.randint(0, len(pn_vin) - 1)
    passport_number = (pn_vin[p_vin])[0]
    vin = pn_vin[p_vin][1]
    case_address = pac[random_area][1]
    article_id = a_d[random_article][0]
    license_number = pn_vin[p_vin][2]
    license_number_temp = '\'' + str(license_number) + '\''
    cursor.execute(f"SELECT date_of_issue from driver_license where license_number = {license_number_temp}")
    record = cursor.fetchall()
    start_date = record[0][0]
    end_date = datetime.date(2023, 6, 8)
    num_days = (end_date - start_date).days
    rand_days = random.randint(1, num_days)
    date_of_case = start_date + datetime.timedelta(days=rand_days)

    rand_days = random.randint(1, 20)
    date_of_review = date_of_case + datetime.timedelta(days=rand_days)
    if date_of_case > datetime.date(2023, 5, 30):
        date_of_review = None
    camera_id = pac[random_area][2]
    case_reason = a_d[random_article][1]
    police_id = pac[random_area][0]
    randomist = random.randint(0, 1)

    if randomist == 0:
        protocol_result = '(\'' + str(vin) + '\',' + str(passport_number) + ',\'' + str(date_of_case) + '\',\'' + str(
            pac[random_area][1]) + '\',' + str(camera_id) + ',\'' + str(case_reason) + '\',\'' + str(police_id) + '\',\'' + case_verdict[0] + '\')'
        print(protocol_result)

        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO protocol (vin, passport_number, date_of_case, case_address, camera_id, case_reason, police_id, case_verdict) values {protocol_result}")
        connection.commit()

    else:
        protocol_result = '(\'' + str(vin) + '\',' + str(passport_number) + ',\'' + str(
            date_of_case) + '\',\'' + str(
            case_address) + '\',\'' + str(case_reason) + '\',\'' + str(police_id) + '\',\'' + case_verdict[0] + '\')'
        print(protocol_result)
        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO protocol (vin, passport_number, date_of_case, case_address, case_reason, police_id, case_verdict) values {protocol_result}")

        connection.commit()

    cursor = connection.cursor()
    cursor.execute(f"SELECT max(case_id) from protocol")
    record = cursor.fetchall()
    case_id = record[0][0]
    article_result = '(' + str(case_id) + ',\'' + str(article_id) + '\')'
    cursor = connection.cursor()
    cursor.execute(
        f"INSERT INTO case_article (case_id, article_id) values {article_result}")
    connection.commit()
    print(article_result)
    rand_driver = random.randint(0, 9)
    was_a_driver = True
    if rand_driver > 7 and camera_id is not None:
        was_a_driver = False
    else:
        was_a_driver = True
    full_justification = True
    if was_a_driver:
        full_justification = True
    else:
        full_justification = False

    if date_of_review is None:
        complaint_result = '(' + str(case_id) + ',' + str(passport_number) + ',\'' + str(date_of_case) + '\',' + \
                           str(full_justification) + ',' + str(was_a_driver) + ',\'' + reason_text[
                               random.randint(0, len(reason_text) - 1)] + '\')'
        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO complaint (case_id, passport_number, date_of_submission, full_justification, was_a_driver, reason_text) values {complaint_result}")
        connection.commit()
    else:
        bull = random.randint(0, 1)
        if bull == 0:
            verdict_boolean = False
        else:
            verdict_boolean = True

        if verdict_boolean:
            verdict = 'Аппеляция была рассмотрена. Вынесено положительное решение'
        else:
            verdict = 'Решение – отказать за недостатком опровергающих доказательств'

        complaint_result = '(' + str(case_id) + ',' + str(passport_number) + ',\'' + str(date_of_case) + '\',\'' + str(date_of_review) + '\',' +\
                           str(full_justification) + ',' + str(was_a_driver) + ',\'' + reason_text[
                               random.randint(0, len(reason_text) - 1)] + '\',\'' + verdict + '\',' + str(verdict_boolean) + ')'
        cursor = connection.cursor()
        cursor.execute(
            f"INSERT INTO complaint (case_id, passport_number, date_of_submission, date_of_review, full_justification, was_a_driver, reason_text, verdict, verdict_boolean) values {complaint_result}")
        connection.commit()
    print(complaint_result)
