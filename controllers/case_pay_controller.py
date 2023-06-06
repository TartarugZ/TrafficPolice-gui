import json
from py_ui.case_pay import Ui_CasePay
from controllers.add_driver_controller import AddDriver
from controllers.delete_driver_controller import DeleteDriver
from controllers.complaint_controller import Complaint
from controllers.confirm_controller import Confirm
from controllers.find_protocol_controller import FindProtocol
from PyQt5 import QtWidgets


class CasePay(QtWidgets.QMainWindow, Ui_CasePay):
    def __init__(self, menu, net):
        try:
            super().__init__()
            self.setupUi(self)
            self.menu = menu
            self.network = net
            self.case_id = None
            self.confirm_screen = None
            self.find_screen = None
            self.complaint_screen = None
            self.delete_driver = None
            self.add_driver = None
            self.cases = {}
            self.fines = {}
            self.sum_fine_pay.clicked.connect(self.sum_pay_pressed)
            self.case_fine_pay.clicked.connect(self.case_pay_pressed)
            self.add_person.clicked.connect(self.add_p_pressed)
            self.delete_person.clicked.connect(self.delete_p_pressed)
            self.back.clicked.connect(self.back_pressed)
            self.complain.clicked.connect(self.complain_pressed)
            self.find_complaint.clicked.connect(self.find_complaint_pressed)
            self.cb_person.addItem('-')
            self.cb_case.addItem('-')
            self.cb_case.currentTextChanged.connect(self.case_selected)
            self.cb_person.currentTextChanged.connect(self.person_selected)
            self.del_acc.clicked.connect(self.del_acc_pressed)
            self.existed_drivers = pase_persons(self.network.get_person())
            self.put_drivers()
        except Exception as e:
            print(e)

    def find_complaint_pressed(self):
        self.find_screen = FindProtocol(self.network)
        self.find_screen.show()

    def put_drivers(self):
        if len(self.existed_drivers) > 0:
            self.cb_person.clear()
            self.cb_person.addItem('-')
            for key, value in self.existed_drivers.items():
                self.cb_person.addItem(str(key) + str(value))
            if len(self.fines) > 0:
                self.case_fine_value.setText(self.fines[self.cb_case.currentText()])

    def del_acc_pressed(self):
        self.confirm_screen = Confirm(self.network, menu=self.menu, case_screen=self)
        self.confirm_screen.show()

    def case_selected(self):
        try:
            if self.cb_case.currentText() != '-' and self.cb_case.count() > 1:
                sum_fine = self.network.get_sum_fines(self.cb_person.currentText()[:10])
                self.sum_fine_value.setText(str(sum_fine['count_fines_sum']))
                self.case_te.setText(self.cases[self.cb_case.currentText()])
                if len(self.fines) > 0:
                    try:
                        if self.fines[self.cb_case.currentText()] != '0' or self.fines[self.cb_case.currentText()] != 0:
                            self.case_fine_value.setText(str(self.fines[self.cb_case.currentText()]))
                        else:
                            self.case_fine_value.setText('0')
                    except Exception:
                        self.case_fine_value.setText('0')
                else:
                    self.case_fine_value.setText('0')
            else:
                self.case_te.setText('')
                self.case_fine_value.setText('0')
        except Exception as e:
            print(e)

    def person_selected(self):
        self.cases = {}
        self.fines = {}
        self.cb_case.clear()
        self.cb_case.addItem('-')
        try:
            if self.cb_person.currentText() != '-' and self.cb_person.count() > 1:
                cases = self.network.find_protocol_citizen(passport=self.cb_person.currentText()[:10])
                if len(cases) > 0:
                    self.case_te.setText(f'Было найдено дел: {len(cases)}')
                else:
                    self.case_te.setText(f'Было найдено дел: 0')
                for i in cases:
                    temp = i['case_id']
                    self.cb_case.addItem(str(temp))
                    reply_temp = str(i).replace('\"', '\\"')
                    reply_temp = reply_temp.replace('\'', '\"')
                    reply_temp = reply_temp.replace('None', '\"None\"')
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
                        if key == 'mark_and_model':
                            key_temp = 'Марка и модель ТС'
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
                                king_in_the_castle = king_in_the_castle + ' ' + temp_article + '   '
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
                                        if jv is None or jv == 'None':
                                            jv = 'Не оплачено'
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
                sum_fine = self.network.get_sum_fines(self.cb_person.currentText()[:10])
                self.sum_fine_value.setText(str(sum_fine['count_fines_sum']))
        except Exception as e:
            print(e)

    def complain_pressed(self):
        self.comp_message.setText('')
        if self.cb_case.currentText() != '-':
            self.complaint_screen = Complaint(self.network, self.cb_case.currentText())
            self.complaint_screen.show()
        else:
            self.comp_message.setText('Дело не выбрано')

    def back_pressed(self):
        try:
            self.network.logout()
            self.menu.show()
            self.menu.password_line.clear()
            self.close()
        except Exception as e:
            print(e)

    def sum_pay_pressed(self):
        try:
            if self.cb_case.count() > 1:
                all_cases = [self.cb_case.itemText(i) for i in range(self.cb_case.count())]
                for i in all_cases:
                    if i != '-':
                        if int(self.fines[i]) > 0:
                            a = self.network.pay_single(int(i), int(self.fines[i]))
                            if 'successful payment' in a:
                                self.case_fine_value.setText('0')
                                self.sum_fine_value.setText('0')
        except Exception as e:
            print(e)

    def case_pay_pressed(self):
        try:
            if self.cb_case.currentText() != '-' and int(self.case_fine_value.text()) > 0:
                print('Paying')
                a = self.network.pay_single(int(self.cb_case.currentText()), int(self.case_fine_value.text()))
                fine = int(self.case_fine_value.text())
                if 'successful payment' in a:
                    self.case_fine_value.setText('0')
                    self.sum_fine_value.setText(str(int(self.sum_fine_value.text()) - fine))
        except Exception as e:
            print(e)

    def add_p_pressed(self):
        self.add_driver = AddDriver(self.network, self)
        self.add_driver.show()

    def delete_p_pressed(self):
        self.delete_driver = DeleteDriver(self.network, self)
        self.delete_driver.show()


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
