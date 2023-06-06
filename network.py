import re
import json
import requests
from network_error import *


def check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, email):
        return True
    else:
        return False


class Network:
    URL = 'https://25.39.214.241:6969'
    session = requests.Session()
    session.verify = False
    username = None
    password = None
    access_token = None

    def ping_server(self):
        self.session.get(url=f'{self.URL}', timeout=5)
        print('Ping, pong!')

    def update_tokens_citizen(self, callback, **args):
        body = {
            'username': self.username,
            'password': self.password
        }
        response = self.session.post(url=f'{self.URL}/auth/token/citizen', json=body, timeout=7)
        print(response.status_code)
        if response.status_code == 500:
            raise ServerError
        response = json.loads(response.text)
        print(response)
        self.access_token = response['token']
        self.session.headers.update(
            {'Authorization': f'Bearer {self.access_token}'})
        print('citizen token got')
        return callback(**args)

    def update_tokens_policeman(self, callback, **args):
        body = {
            'username': self.username,
            'password': self.password
        }
        response = self.session.post(url=f'{self.URL}/auth/token/policeman', json=body, timeout=7)
        print(response.text)
        print(response.status_code)
        if response.status_code == 500:
            raise ServerError

        response = json.loads(response.text)
        print(response)

        self.access_token = response['token']
        self.session.headers.update(
            {'Authorization': f'Bearer {self.access_token}'})
        print('policeman token got')
        return callback(**args)

    def get_info_by_car(self, vin, num, region):
        try:
            if vin is None:
                vin = ''
            if num is None:
                num = ''
            if region is None:
                region = ''
            response = self.session.get(url=f'{self.URL}/api/policeman/car?vin={vin}&number={num}&region_code={region}',
                                        timeout=7)
            if response.status_code == 401:
                print('refresh token')
                raise NeedRefreshToken
            elif response.status_code == 500:
                raise ServerError
            print(response.json())
            print('Car info')
            return response.json()
        except NeedRefreshToken:
            self.update_tokens_policeman(self.get_info_by_car, vin=vin, num=num, region=region)

    def get_info_by_person(self, passport, driver_license):
        try:
            if passport is None:
                passport = ''
            if driver_license is None:
                driver_license = ''
            response = self.session.get(
                url=f'{self.URL}/api/policeman/person?passport_number={passport}&driver_license={driver_license}',
                timeout=7)
            if response.status_code == 401:
                print('refresh token')
                raise NeedRefreshToken
            elif response.status_code == 500:
                raise ServerError
            print(response.json())
            print('Person info')
            return response.json()
        except NeedRefreshToken:
            self.update_tokens_policeman(self.get_info_by_person, passport=passport, driver_license=driver_license)

    def logout(self):

        response = self.session.post(
            url=f'{self.URL}/acc/logout',
            timeout=7)
        print(response.text)
        print('Logout')
        self.access_token = None
        self.username = None
        self.password = None

    def login_policeman(self, username, password):
        if self.username is None:
            self.username = username
            self.password = password
            try:
                self.update_tokens_policeman(self.login_policeman, username=username, password=password)
                print('Login ok')
                return True
            except Exception:
                self.username = None
                self.password = None
                return False

    def login_person(self, username, password):
        if self.username is None:
            self.username = username
            self.password = password
            try:
                self.update_tokens_citizen(self.login_person, username=username, password=password)
                print('Login ok')
                return True
            except Exception:
                self.username = None
                self.password = None
                return False

    def find_protocol(self, case_id, vin, police_id, passport):
        try:
            if case_id is None:
                case_id = ''
            if vin is None:
                vin = ''
            if police_id is None:
                police_id = ''
            if passport is None:
                passport = ''

            response = self.session.get(
                url=f'{self.URL}/api/policeman/protocol?passport_number={passport}&vin={vin}&case_id={case_id}&police_id={police_id}',
                timeout=17)
            if response.status_code == 401:
                print('refresh token')
                raise NeedRefreshToken
            elif response.status_code == 500:
                raise ServerError
            print(response.json())
            print('Protocol info')
            return response.json()
        except NeedRefreshToken:
            self.update_tokens_policeman(self.find_protocol, passport=passport, vin=vin, police_id=police_id,
                                         case_id=case_id)

    def registration(self, email, phone, username, password):
        try:
            if len(phone) > 10:
                phone = phone[-10:]

            body = {
                "email": email,
                "phone_number": phone,
                "username": username,
                "password": password
            }
            response = self.session.post(
                url=f'{self.URL}/acc/citizen', json=body, timeout=7)
            if response.status_code == 401:
                print('refresh token')
                raise NeedRefreshToken
            return response.text
        except NeedRefreshToken:
            self.update_tokens_citizen(self.registration, email=email, phone=phone, username=username,
                                       password=password)

    def delete_account(self, password):
        try:
            headers = {
                "password": password
            }
            response = self.session.delete(
                url=f'{self.URL}/acc/citizen', headers=headers, timeout=7)
            if response.status_code == 401:
                print('refresh token')
                raise NeedRefreshToken
            print(response.text)
            return response.text
        except NeedRefreshToken:
            self.update_tokens_citizen(self.delete_account, password=password)

    def get_articles(self):
        try:
            response = self.session.get(
                url=f'{self.URL}/api/policeman/articles', timeout=7)
            if response.status_code == 401:
                print('refresh token')
                raise NeedRefreshToken
            elif response.status_code == 500:
                raise ServerError
            print(response.json())
            print('Articles info')
            return response.json()
        except NeedRefreshToken:
            self.update_tokens_policeman(self.get_articles)

    def create_case(self, vin, passport, date_of_case, case_address, camera_id, case_reason, case_verdict, police_id,
                    person_name, surname, patron, phone, job, date_of_birth, unit, place_of_reg, full_name, post, rank,
                    m_m, number, region, articles, fines):
        try:
            body = {}
            if len(phone) > 10:
                phone = phone[-10:]
            body = {
                "vin": vin,
                "passport_number": passport,
                "date_of_case": date_of_case,
                "case_address": case_address,
                "camera_id": camera_id,
                "case_reason": case_reason,
                "case_verdict": case_verdict,
                "police_id": police_id,
                "person_name": person_name,
                "surname": surname,
                "patronymic": patron,
                "phone_number": phone,
                "job_info": job,
                "date_of_birth": date_of_birth,
                "unit": unit,
                "place_of_registr": place_of_reg,
                "full_name": full_name,
                "post": post,
                "rank": rank,
                "mark_and_model": m_m,
                "number": number,
                "region_code": region,
                "articles": articles,
                "fines": fines
            }
            if camera_id == '' or camera_id is None:
                del body['camera_id']
            if patron == '' or patron is None:
                del body['patronymic']
            for k, v in body.items():
                if v == '' or v is None:
                    raise EmptyField
            body = json.dumps(body, default=str)
            print(body)
            body = json.loads(body)
            response = self.session.post(
                url=f'{self.URL}/api/policeman/protocol', json=body, timeout=7)
            if response.status_code == 401:
                print('refresh token')
                raise NeedRefreshToken
            print(response.text)
            return response.text
        except NeedRefreshToken:
            self.update_tokens_citizen(self.create_case, vin=vin, passport=passport, date_of_case=date_of_case,
                                       case_address=case_address, camera_id=camera_id, case_reason=case_reason,
                                       case_verdict=case_verdict,
                                       police_id=police_id,
                                       person_name=person_name, surname=surname, patron=patron, phone=phone, job=job,
                                       date_of_birth=date_of_birth, unit=unit, place_of_reg=place_of_reg,
                                       full_name=full_name, post=post, rank=rank,
                                       m_m=m_m, number=number, region=region, articles=articles, fines=fines)

    def get_protocols(self):
        try:
            response = self.session.get(
                url=f'{self.URL}/api/citizen/protocol', timeout=15)
            if response.status_code == 401:
                print('refresh token')
                raise NeedRefreshToken
            elif response.status_code == 500:
                raise ServerError
            print(response.json())
            print('User protocols info')
            return response.json()
        except NeedRefreshToken:
            self.update_tokens_citizen(self.get_protocols)

    def find_protocol_citizen(self, passport):
        try:
            response = self.session.get(
                url=f'{self.URL}/api/citizen/protocol?passport_number={passport}')
            if response.status_code == 401:
                print('refresh token')
                raise NeedRefreshToken
            elif response.status_code == 500:
                raise ServerError
            print(response.json())
            print('Protocol citizen info')
            return response.json()
        except NeedRefreshToken:
            self.update_tokens_citizen(self.find_protocol_citizen, passport=passport)

    def add_person(self, passport):
        try:
            body = {
                "passport_number": passport,
            }
            response = self.session.post(
                url=f'{self.URL}/api/citizen/person', json=body, timeout=7)
            if response.status_code == 401:
                print('refresh token')
                raise NeedRefreshToken
            print(response.text)
            return response.text
        except NeedRefreshToken:
            self.update_tokens_citizen(self.add_person, passport=passport)

    def delete_person(self, passport):
        try:
            body = {
                "passport_number": passport,
            }
            response = self.session.delete(
                url=f'{self.URL}/api/citizen/person', json=body, timeout=7)
            if response.status_code == 401:
                print('refresh token')
                raise NeedRefreshToken
            elif response.status_code == 500:
                raise ServerError
            print(response.text)
            return response.text
        except NeedRefreshToken:
            self.update_tokens_citizen(self.delete_person, passport=passport)

    def get_person(self):
        try:
            response = self.session.get(
                url=f'{self.URL}/api/citizen/person',
                timeout=15)
            if response.status_code == 401:
                print('refresh token')
                raise NeedRefreshToken
            elif response.status_code == 500:
                raise ServerError
            print(response.json())
            print('Persons info')
            return response.json()
        except NeedRefreshToken:
            self.update_tokens_citizen(self.get_person)

    def pay_single(self, case_id, payment):
        try:
            body = {
                "case_id": case_id,
                "payment": payment
            }

            response = self.session.put(
                url=f'{self.URL}/api/citizen/payfine', json=body, timeout=7)
            if response.status_code == 401:
                print('refresh token')
                raise NeedRefreshToken
            print(response.text)
            return response.text
        except NeedRefreshToken:
            self.update_tokens_citizen(self.add_person, case_id=case_id, payment=payment)

    def get_complaints_policeman(self, complaint_id, case_id, passport_number):
        try:
            if case_id is None:
                case_id = ''
            if complaint_id is None:
                complaint_id = ''
            if passport_number is None:
                passport_number = ''

            response = self.session.get(
                url=f'{self.URL}/api/policeman/complaint?complaint_id={complaint_id}&case_id={case_id}&passport_number={passport_number}',
                timeout=7)
            if response.status_code == 401:
                print('refresh token')
                raise NeedRefreshToken
            elif response.status_code == 500:
                raise ServerError
            print(response.json())
            print('Complaints info')
            return response.json()
        except NeedRefreshToken:
            self.update_tokens_policeman(self.get_complaints_policeman, complaint_id=complaint_id, case_id=case_id, passport_number=passport_number)

    def update_complaint(self, complaint_id, verdict, verdict_boolean):
        try:
            body = {
                "complaint_id": complaint_id,
                "verdict": verdict,
                "verdict_boolean": verdict_boolean
            }

            response = self.session.put(
                url=f'{self.URL}/api/policeman/complaint', json=body, timeout=7)
            if response.status_code == 401:
                print('refresh token')
                raise NeedRefreshToken
            print(response.text)
            return response.text
        except NeedRefreshToken:
            self.update_tokens_policeman(self.update_complaint, complaint_id=complaint_id, verdict=verdict, verdict_boolean=verdict_boolean)

    def post_complaint(self, case_id, passport_number, full_justification, was_a_driver, reason_text):
        try:
            body = {
                "case_id": case_id,
                "full_justification": full_justification,
                "passport_number": passport_number,
                "was_a_driver": was_a_driver,
                "reason_text": reason_text,
            }
            response = self.session.post(
                url=f'{self.URL}/api/citizen/complaint', json=body, timeout=7)
            if response.status_code == 401:
                print('refresh token')
                raise NeedRefreshToken
            print(response.text)
            return response.text
        except NeedRefreshToken:
            self.update_tokens_citizen(self.post_complaint, case_id=case_id, passport_number=passport_number,
                                       full_justification=full_justification,
                                       was_a_driver=was_a_driver, reason_text=reason_text)

    def get_complaints_citizen(self, complaint_id, case_id, passport_number):
        try:
            if case_id is None:
                case_id = ''
            if complaint_id is None:
                complaint_id = ''
            if passport_number is None:
                passport_number = ''

            response = self.session.get(
                url=f'{self.URL}/api/citizen/complaint?complaint_id={complaint_id}&case_id={case_id}&passport_number={passport_number}',
                timeout=7)
            if response.status_code == 401:
                print('refresh token')
                raise NeedRefreshToken
            elif response.status_code == 500:
                raise ServerError
            print(response.json())
            print('Complaints info')
            return response.json()
        except NeedRefreshToken:
            self.update_tokens_citizen(self.get_complaints_citizen, complaint_id=complaint_id, case_id=case_id, passport_number=passport_number)

    def delete_complaint(self, complaint_id):
        try:
            body = {
                "complaint_id": complaint_id,
            }
            response = self.session.delete(
                url=f'{self.URL}/api/citizen/complaint', json=body, timeout=7)
            if response.status_code == 401:
                print('refresh token')
                raise NeedRefreshToken
            elif response.status_code == 500:
                raise ServerError
            print(response.text)
            return response.text
        except NeedRefreshToken:
            self.update_tokens_citizen(self.delete_complaint, complaint_id=complaint_id)

    def delete_protocol(self, case_id):
        try:
            body = {
                'case_id': case_id,
            }
            response = self.session.delete(
                url=f'{self.URL}/api/policeman/protocol', json=body, timeout=7)
            if response.status_code == 401:
                print('refresh token')
                raise NeedRefreshToken
            elif response.status_code == 500:
                raise ServerError
            print(response.text)
            return response.text
        except NeedRefreshToken:
            self.update_tokens_policeman(self.delete_protocol, case_id=case_id)

    def get_unseen_complaints(self):
        try:
            response = self.session.get(
                url=f'{self.URL}/api/policeman/unseencomplaint',
                timeout=7)
            if response.status_code == 401:
                print('refresh token')
                raise NeedRefreshToken
            elif response.status_code == 500:
                raise ServerError
            print(response.json())
            print('Complaints info')
            return response.json()
        except NeedRefreshToken:
            self.update_tokens_policeman(self.get_unseen_complaints)

    def get_sum_fines(self, passport):
        try:
            response = self.session.get(
                url=f'{self.URL}/api/citizen/sumfine?passport_number={passport}',
                timeout=7)
            if response.status_code == 401:
                print('refresh token')
                raise NeedRefreshToken
            elif response.status_code == 500:
                raise ServerError
            print(response.json())
            print('Complaints info')
            return response.json()
        except NeedRefreshToken:
            self.update_tokens_citizen(self.get_sum_fines, passport=passport)

















