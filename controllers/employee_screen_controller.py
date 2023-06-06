import datetime
import json
import re
from py_ui.employee_screen import Ui_EmployeeScreen
from controllers.change_article_controller import ChangeArticle
from PyQt5 import QtWidgets
from network_error import *


class EmployeeScreen(QtWidgets.QMainWindow, Ui_EmployeeScreen):
    def __init__(self, menu, net):
        try:
            super().__init__()
            self.setupUi(self)
            self.menu = menu
            self.network = net
            self.add_af = None
            self.delete_af = None
            self.car_users = {}
            self.cases = {}
            self.complaints = {}
            self.frame_car.hide()
            self.frame_driver.hide()
            self.frame_find_case.hide()
            self.frame_create_case.hide()
            self.frame_output.hide()
            self.complaint_frame.hide()
            self.find_car.clicked.connect(self.find_car_pressed)
            self.find_driver.clicked.connect(self.find_driver_pressed)
            self.find_case.clicked.connect(self.find_case_pressed)
            self.create_case.clicked.connect(self.create_case_pressed)
            self.create_case_submit.clicked.connect(self.create_submit_pressed)
            self.search_case.clicked.connect(self.search_case_pressed)
            self.delete_case.clicked.connect(self.delete_case_pressed)
            self.back.clicked.connect(self.back_pressed)
            self.submit_car_btn.clicked.connect(self.get_car_info_pressed)
            self.choose_cb.currentIndexChanged.connect(self.cb_choose_selected)
            self.submit_driver_btn.clicked.connect(self.submit_driver_pressed)
            self.find_comlaint.clicked.connect(self.find_complaint_pressed)
            self.choose_cb.addItem('-')
            self.add_article_fine.clicked.connect(self.add_article_fine_pressed)
            self.delete_article_fine.clicked.connect(self.delete_article_fine_pressed)
            self.submit_find_complaint.clicked.connect(self.submit_find_complaint_pressed)
            self.submit_find_complaint_2.clicked.connect(self.submit_find_complaint_2_pressed)
            self.good.clicked.connect(self.good_pressed)
            self.bad.clicked.connect(self.bad_pressed)
            self.setGeometry(100, 100, 1018, 647)
            self.articles = self.network.get_articles()
            self.added_articles = {}
        except Exception as e:
            print(e)

    def good_pressed(self):
        self.complaint_message.setText('')
        try:
            if self.choose_cb.currentText() != '-':
                self.network.update_complaint(self.choose_cb.currentText(), self.output_cb.toPlainText(), True)
                self.complaint_message.setText('Успешно изменено')
        except Exception as e:
            print(e)

    def bad_pressed(self):
        self.complaint_message.setText('')
        try:
            if self.choose_cb.currentText() != '-':
                self.network.update_complaint(self.choose_cb.currentText(), self.output_cb.toPlainText(), False)
                self.complaint_message.setText('Успешно изменено')
        except Exception as e:
            print(e)

    def submit_find_complaint_2_pressed(self):
        self.find_comp(2)

    def submit_find_complaint_pressed(self):
        self.find_comp(1)

    def find_comp(self, status):
        self.complaint_message.setText('')
        try:
            self.output.setText(f'Было найдено жалоб: 0')
            self.complaints = {}
            self.choose_cb.clear()
            self.choose_cb.addItem('-')
            if self.complaint_id.text().strip() != '' or self.case_id.text().strip() != '' \
                    or self.passport.text().strip() != '' or status == 2:
                complaints = []
                if status == 1:
                    complaints = self.network.get_complaints_policeman(self.complaint_id.text(), self.case_id.text(),
                                                                       self.passport.text())
                elif status == 2:
                    complaints = self.network.get_unseen_complaints()
                print(complaints)
                if len(complaints) > 0:
                    self.output.setText(f'Было найдено жалоб: {len(complaints)}')
                else:
                    self.output.setText(f'Было найдено жалоб: 0')

                for i in complaints:
                    temp = i['complaint_id']
                    reply_temp = str(i).replace('\"', '\\"')
                    reply_temp = reply_temp.replace('\'', '\"')
                    reply_temp = reply_temp.replace('None', '\"None\"')
                    reply_temp = reply_temp.replace('True', '\"True\"')
                    reply_temp = reply_temp.replace('False', '\"False\"')
                    complaint = json.loads(reply_temp)
                    parsing_complaint = []
                    for (key, value) in complaint.items():
                        key_temp = key
                        value_temp = value
                        if key == 'complaint_id':
                            key_temp = 'Номер жалобы'
                        if key == 'case_id':
                            key_temp = 'Номер дела'
                        if key == 'passport_number':
                            key_temp = 'Серия и номер паспорта'
                        if key == 'date_of_submission':
                            key_temp = 'Дата подачи жалобы'
                        if key == 'date_of_review':
                            key_temp = 'Дата рассмотрения жалобы'
                        if key == 'verdict':
                            key_temp = 'Решение по жалобе'
                        if key == 'full_justification':
                            key_temp = 'Жалоба была подана на полное обжалование'
                        if key == 'was_a_driver':
                            key_temp = 'Был ли гражданин, подавший жалобу, водителем в момент нарушения'
                        if key == 'reason_text':
                            key_temp = 'Причина подачи жалобы'
                        if key == 'verdict_boolean':
                            key_temp = 'Была ли одобрена жалоба'
                        if key == 'case_reason':
                            key_temp = 'Причина штрафования'
                        if value_temp == 'True':
                            value_temp = 'Да'
                        elif value_temp == 'False':
                            value_temp = 'Нет'

                        parsing_complaint.append(str(key_temp) + ':\n' + str(value_temp) + '\n\n')

                    self.complaints[f'{temp}'] = ''.join(parsing_complaint)
                for jk, jv in self.complaints.items():
                    self.choose_cb.addItem(str(jk))
        except Exception as e:
            print(e)

    def add_article_fine_pressed(self):
        self.add_af = ChangeArticle(net=self.network, exist_articles=self.added_articles, status=0, window=self,
                                    articles=self.articles)
        self.add_af.show()

    def delete_article_fine_pressed(self):
        self.delete_af = ChangeArticle(net=self.network, exist_articles=self.added_articles, status=1, window=self,
                                       articles=self.articles)
        self.delete_af.show()

    def search_case_pressed(self):
        self.car_users = {}
        self.cases = {}
        self.choose_cb.clear()
        self.choose_cb.addItem('-')
        try:
            if self.find_case_id.text().strip() != '' or self.find_case_passport.text().strip() != '' \
                    or self.find_case_police_id.text().strip() != '' or self.find_case_vin.text().strip() != '':

                cases = self.network.find_protocol(case_id=self.find_case_id.text(),
                                                   passport=self.find_case_passport.text(),
                                                   police_id=self.find_case_police_id.text(),
                                                   vin=self.find_case_vin.text())
                print(cases)
                print(len(cases))
                self.output.setText(f'Было найдено дел: {len(cases)}')
                for i in cases:
                    temp = i['case_id']
                    self.choose_cb.addItem(str(temp))
                    reply_temp = str(i).replace('\"', '\\"')
                    reply_temp = reply_temp.replace('\'', '\"')
                    reply_temp = reply_temp.replace('None', '\"None\"')
                    print('Already here')
                    case = json.loads(reply_temp)
                    parsing_case = []
                    full_name = ''
                    for (key, value) in case.items():
                        key_temp = key
                        value_temp = value
                        if key == 'case_id':
                            key_temp = 'Номер дела'
                        if key == 'vin':
                            key_temp = 'Номер VIN'
                        if key == 'passport_number':
                            key_temp = 'Серия и номер паспорта'
                        if key == 'date_of_case':
                            key_temp = 'Дата составления протокола'
                        if key == 'case_address':
                            key_temp = 'Адрес места оформления'
                        if key == 'camera_id':
                            key_temp = 'Номер камеры, зафиксировавшей нарушение'
                        if key == 'case_reason':
                            key_temp = 'Причина составления протокола'
                        if key == 'case_verdict':
                            key_temp = 'Вердикт по делу'
                        if key == 'police_id':
                            key_temp = 'ID сотрудника ГИБДД, оформившего дело'
                        if key == 'job_info':
                            key_temp = 'Информация о работе владельца ТС'
                        if key == 'date_of_birth':
                            key_temp = 'Дата рождения владельца ТС'
                        if key == 'unit':
                            key_temp = 'Кем выдан паспорт'
                        if key == 'place_of_registr':
                            key_temp = 'Место прописки'
                        if key == 'full_name':
                            key_temp = 'ФИО сотрудника ГИБДД, оформившего дело'
                        if key == 'post':
                            key_temp = 'Должность'
                        if key == 'rank':
                            key_temp = 'Звание'
                        if key == 'number':
                            key_temp = 'Номера машины'
                        if key == 'region_code':
                            key_temp = 'Регион номеров'
                        if key == 'articles':
                            key_temp = 'Статья'
                            king_in_the_castle = ''
                            for j in value:
                                temp_article = article_type_parser(str(j['article_id']))
                                king_in_the_castle = king_in_the_castle + ' ' + temp_article
                            value_temp = king_in_the_castle
                        if key == 'fines':
                            key_temp = 'Штраф'
                            king_in_the_castle = ''
                            for t in value_temp:
                                json_temp = json.loads(str(t).replace('\'', '\"'))
                                for (jk, jv) in json_temp.items():
                                    if jk == 'date_start':
                                        jk = 'Дата начисления штрафа'
                                    if jk == 'date_end':
                                        jk = 'Дата истечения штрафа'
                                    if jk == 'date_payment':
                                        jk = 'Дата оплаты штрафа'
                                    if jk == 'sum':
                                        jk = 'Сумма штрафа'
                                    king_in_the_castle = king_in_the_castle + str(jk) + '\n' + str(jv) + '\n'
                                king_in_the_castle = king_in_the_castle + '\n'
                            value_temp = king_in_the_castle
                        if key == 'person_name':
                            full_name = full_name + ' ' + value
                            key_temp = 'Имя владельца ТС'
                        if key == 'surname':
                            full_name = full_name + ' ' + value
                            key_temp = 'Фамилия владельца ТС'
                        if key == 'patronymic':
                            full_name = full_name + ' ' + value
                            key_temp = 'Отчество владельца ТС'
                        if key != 'person_name' and key != 'surname' and key != 'patronymic':
                            if value_temp == "None":
                                value_temp = '-'
                            parsing_case.append(str(key_temp) + ':\n' + str(value_temp) + '\n\n')
                    parsing_case.insert(0, 'Обвиняемый: ' + '\n' + full_name + '\n\n')

                    self.cases[f'{temp}'] = ''.join(parsing_case)

        except Exception as e:
            print(e)

    def find_complaint_pressed(self):
        self.hide_all()
        self.complaint_frame.show()
        self.find_comlaint.setEnabled(False)
        self.output_cb.setReadOnly(False)
        self.label.show()
        self.output_cb.setPlaceholderText('Введите комментарий к апелляции')
        self.label.setText('Аппеляции выбранного гражданина:')
        self.choose_cb.show()
        self.output_cb.show()
        self.frame_output.show()

    def submit_driver_pressed(self):
        self.car_users = {}
        self.cases = {}
        try:
            if self.driver_passport.text().strip() != '' or self.driver_lisence.text().strip() != '':
                reply = self.network.get_info_by_person(self.driver_passport.text(), self.driver_lisence.text())
                reply_temp = str(reply).replace('\'', '\"')
                print(reply)
                print('Already here')
                if is_json(reply_temp):
                    print('I am JSON')
                    person = reply
                    print(person)
                    parsing_person = []
                    full_name = ''
                    for (key, value) in person.items():
                        key_temp = key
                        value_temp = value
                        if key == 'passport_number':
                            key_temp = 'Серия и номер паспорта'
                        if key == 'driver_license':
                            key_temp = 'Номер водительского удостоверения'
                        if key == 'date_of_issue':
                            key_temp = 'Дата выдачи прав'
                        if key == 'phone_number':
                            key_temp = 'Номер телефона'
                        if key == 'job_info':
                            key_temp = 'Информация о работе'
                        if key == 'date_of_birth':
                            key_temp = 'Дата рождения'
                        if key == 'place_of_registr':
                            key_temp = 'Место прописки'
                        if key == 'person_name':
                            full_name = full_name + ' ' + value
                            key_temp = 'Имя владельца ТС'
                        if key == 'surname':
                            full_name = full_name + ' ' + value
                            key_temp = 'Фамилия владельца ТС'
                        if key == 'patronymic':
                            full_name = full_name + ' ' + value
                            key_temp = 'Отчество владельца ТС'
                        if key != 'person_name' and key != 'surname' and key != 'patronymic':
                            parsing_person.append(str(key_temp) + ': ' + str(value_temp) + '\n')
                    parsing_person.insert(0, 'Владелец: ' + full_name + '\n')
                    reply = parsing_person
                else:
                    reply = 'О данном человеке нет информации в базе данных'
                self.output.setText(''.join(reply))
        except Exception as e:
            print(e)

    def cb_choose_selected(self):
        try:
            if self.choose_cb.currentText() != '-':
                if not self.find_car.isEnabled():
                    self.output_cb.setText(self.car_users[self.choose_cb.currentText()])
                if not self.find_case.isEnabled():
                    self.output.setText(self.cases[self.choose_cb.currentText()])
                if not self.find_comlaint.isEnabled():
                    self.output.setText(self.complaints[self.choose_cb.currentText()])
        except Exception as e:
            print(e)

    def get_car_info_pressed(self):
        self.car_users = {}
        self.cases = {}
        try:
            reply = self.network.get_info_by_car(self.car_vin.text(), self.car_gosnumber.text(),
                                                 self.car_region.text())
            print('BASE')
            print(reply)
            print('BASE')
            reply_temp = str(reply).replace('\'', '\"')
            print(reply)
            print('Already here')
            if is_json(reply_temp):
                print('I am JSON')
                output_car = reply['car']
                print(output_car)
                parsing_car = []
                full_name = ''
                for (key, value) in output_car.items():
                    key_temp = key
                    value_temp = value
                    if key == 'vin':
                        key_temp = 'VIN'
                    if key == 'driver_license':
                        key_temp = 'Номер водительского удостоверения'
                    if key == 'mark_and_model':
                        key_temp = 'Марка и модель'
                    if key == 'color':
                        key_temp = 'Цвет'
                    if key == 'car_type':
                        key_temp = 'Тип ТС'
                    if key == 'category':
                        key_temp = 'Категория ТС'
                    if key == 'engine_info':
                        key_temp = 'Информация о двигателе'
                    if key == 'sts_num':
                        key_temp = 'Номер СТС'
                    if key == 'pts_num':
                        key_temp = 'Номер ПТС'
                    if key == 'person_name':
                        full_name = full_name + ' ' + value
                        key_temp = 'Имя владельца ТС'
                    if key == 'surname':
                        full_name = full_name + ' ' + value
                        key_temp = 'Фамилия владельца ТС'
                    if key == 'patronymic':
                        full_name = full_name + ' ' + value
                        key_temp = 'Отчество владельца ТС'
                    if key == 'number':
                        key_temp = 'Гос номер ТС'
                    if key == 'region_code':
                        key_temp = 'Регион гос номера ТС'
                    if key != 'person_name' and key != 'surname' and key != 'patronymic':
                        parsing_car.append(str(key_temp) + ':\n' + str(value_temp) + '\n')
                parsing_car.insert(0, 'Владелец: ' + full_name + '\n')
                output_car = reply['car_users']
                print(output_car)
                for u in output_car:
                    full_name = ''
                    info = ''
                    for (key, value) in u.items():
                        # key_temp = key
                        # value_temp = value
                        if key == 'person_name':
                            full_name = full_name + ' ' + value
                            # key_temp = 'Имя доверенного лица'
                        if key == 'surname':
                            full_name = full_name + ' ' + value
                            # key_temp = 'Фамилия доверенного лица'
                        if key == 'patronymic':
                            full_name = full_name + ' ' + value
                            # key_temp = 'Отчество доверенного лица'
                        if key == 'license_number':
                            key_temp = 'Номер водительского удостоверения'
                            info = info + (str(key_temp) + ':\n' + str(value) + '\n')
                    self.car_users[f'{full_name}'] = info
                    self.choose_cb.addItem(full_name)
                reply = parsing_car
            else:
                reply = 'О данной машине нет информации в базе данных'
            self.output.setText(''.join(reply))

        except Exception as e:
            print(e)

    def find_car_pressed(self):
        self.hide_all()
        self.find_car.setEnabled(False)
        self.frame_car.show()
        self.label.show()
        self.label.setText('Водители, указанные в страховке:')
        self.choose_cb.show()
        self.output_cb.show()
        self.frame_output.show()

    def find_driver_pressed(self):
        self.hide_all()
        self.find_driver.setEnabled(False)
        self.frame_driver.show()
        self.label.hide()
        self.choose_cb.hide()
        self.output_cb.hide()
        self.frame_output.show()

    def find_case_pressed(self):
        self.hide_all()
        self.find_case.setEnabled(False)
        self.frame_find_case.show()
        self.label.setText('Дела выбранного гражданина:')
        self.label.show()
        self.choose_cb.show()
        self.output_cb.show()
        self.frame_output.show()

    def create_case_pressed(self):
        self.hide_all()
        self.setGeometry(100, 100, 1803, 647)
        self.create_case.setEnabled(False)
        self.frame_create_case.show()

    def hide_all(self):
        self.setGeometry(100, 100, 1018, 647)
        self.car_users = {}
        self.output_cb.setPlaceholderText('......')
        self.cases = {}
        self.frame_car.hide()
        self.frame_driver.hide()
        self.frame_find_case.hide()
        self.frame_create_case.hide()
        self.frame_output.hide()
        self.complaint_frame.hide()
        self.find_car.setEnabled(True)
        self.find_driver.setEnabled(True)
        self.find_case.setEnabled(True)
        self.create_case.setEnabled(True)
        self.find_comlaint.setEnabled(True)
        self.output_cb.setReadOnly(True)
        self.output.clear()
        self.output_cb.clear()
        self.choose_cb.clear()
        self.choose_cb.addItem('-')

    def back_pressed(self):
        self.network.logout()
        self.menu.show()
        self.menu.password_line.clear()
        self.close()

    def create_submit_pressed(self):
        try:
            sum_fine = 0
            for k, v in self.added_articles.items():
                for jk, jv in v.items():
                    if jk == 'Штраф':
                        sum_fine += int(jv)
            fines = []
            date_today = datetime.date.today()
            date_60 = date_today + datetime.timedelta(days=60)
            fine = {"date_start": date_today, "date_end": date_60, "date_payment": None, "sum": sum_fine}
            fines.append(fine)

            articles = []
            print('Base')
            temp_articles = self.articles
            for nm in temp_articles:
                for (nk, nj) in self.added_articles.items():
                    if nm['description'] == nj['Description']:
                        articles.append({'article_id': nm['article_id']})
            print(fines)
            print(articles)
            d_of_b = self.create_case_date_of_birth.text()
            d_of_b = d_of_b.split('.')
            d_of_b = str(d_of_b[2] + '-' + d_of_b[1] + '-' + d_of_b[0])

            d_o_c = self.create_case_date_of_case.text()
            d_o_c = d_o_c.split('.')
            d_o_c = str(d_o_c[2] + '-' + d_o_c[1] + '-' + d_o_c[0])
            try:
                self.network.create_case(vin=self.create_case_vin.text(), passport=self.create_case_passport.text(),
                                         date_of_case=d_o_c,
                                         case_address=self.create_case_address.text(),
                                         camera_id=self.create_case_camera_id.text(),
                                         case_reason=self.create_case_reason.text(),
                                         case_verdict=self.create_case_case_verdict.text(),
                                         police_id=self.create_case_police_id.text(),
                                         person_name=self.create_case_name.text(),
                                         surname=self.create_case_surname.text(),
                                         patron=self.create_case_patronymic.text(),
                                         phone=self.create_case_phone.text(), job=self.create_case_job.text(),
                                         date_of_birth=d_of_b,
                                         unit=self.create_case_unit.text(),
                                         place_of_reg=self.create_case_place_of_registr.text(),
                                         full_name=self.create_case_full_name.text(),
                                         post=self.create_case_post.text(), rank=self.create_case_rank.text(),
                                         m_m=self.create_case_mark_and_model.text(),
                                         number=self.create_case_gosnumber.text(),
                                         region=self.create_case_region.text(), articles=articles, fines=fines)
            except EmptyField as e:
                self.message.setText(e.__str__())
            print('Protocol sent')
        except Exception as e:
            print(e)

    def delete_case_pressed(self):
        a = self.network.delete_protocol(self.find_case_id.text())
        if "you deleted" in a:
            print('Super')


def check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def pase_persons(persons):
    if len(persons) > 0:
        my_dict = {}
        for p in persons:
            json_temp = str(p).replace('\"', '\\"')
            json_temp = json_temp.replace('\'', '\"')
            json_temp = json.loads(json_temp)
            line = ''
            p_n = ''
            for (k, v) in json_temp.items():
                if k == 'passport_number':
                    p_n = v
                else:
                    line = line + ' ' + v
            my_dict[p_n] = line
        return my_dict
    else:
        return {}


def article_type_parser(article):
    temp = article[1:-1]
    temp = temp.split(',')
    state = 'ст. '
    point = ' п. '
    if temp[0] != '0':
        state = state + temp[0]
    if temp[1] != '0':
        if len(state) > 4:
            state = state + '.'
        state = state + temp[1]
    if temp[2] != '0':
        if len(state) > 4:
            state = state + '.'
        state = state + temp[2]
    if temp[3] != '0':
        point = point + temp[3]
    if temp[4] != '0':
        if len(point) > 3:
            point = point + '.'
        point = point + temp[4]
    return state + ' ' + point


def is_json(myjson):
    try:
        json.loads(myjson)
    except ValueError as e:
        print(e)
        return False
    return True
