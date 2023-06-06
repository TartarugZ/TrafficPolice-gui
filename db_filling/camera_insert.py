import random
import string
import json
import csv
import psycopg2

connection = psycopg2.connect(database="TrafficPolice", user="admin", password="root", host="25.39.214.241", port=5432)
cursor = connection.cursor()

cursor.execute("SELECT area_id from area")
record = cursor.fetchall()
print("Area_id from Database:- ", record)

areas = []
for i in record:
    areas.append(i[0])

cursor = connection.cursor()
cursor.execute("SELECT camera_id from camera")
record = cursor.fetchall()
print("Camera_id from Database:- ", record)

cameras = []
for i in record:
    cameras.append(i[0])

cursor = connection.cursor()
cursor.execute("SELECT certificate from camera")
record = cursor.fetchall()
print("Certificate from Database:- ", record)

certificates = []
for i in record:
    certificates.append(i[0])

n = 50
for i in range(n):

    certificate = 'CN.' + ''.join(random.sample(string.ascii_letters, 2)).upper() + ''.join(
        random.sample(string.digits, 2)) + '.' + ''.join(random.sample(string.ascii_letters, 1)).upper() + ''.join(
        random.sample(string.digits, 5))
    while certificate in certificates:
        certificate = 'CN.' + ''.join(random.sample(string.ascii_letters, 2)).upper() + ''.join(
            random.sample(string.digits, 2)) + '.' + ''.join(random.sample(string.ascii_letters, 1)).upper() + ''.join(
            random.sample(string.digits, 5))
    certificates.append(certificate)

    camera_id = ''.join(random.sample(string.digits, 8))
    while camera_id in cameras:
        camera_id = ''.join(random.sample(string.digits, 8))
    cameras.append(camera_id)

    random_area = random.randrange(0, len(areas))
    area = areas[random_area]

    print('(' + str(camera_id) + ',\'' + str(certificate) + '\',' + str(areas[random_area]) + '),')
    result = '(' + str(camera_id) + ',\'' + str(certificate) + '\',' + str(area) + ')'

    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO camera (camera_id, certificate,  area_id) values {result}")
    connection.commit()