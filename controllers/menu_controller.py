import os

import network
import json
import re
from py_ui.menu import Ui_Menu
from controllers.employee_screen_controller import EmployeeScreen
from controllers.case_pay_controller import CasePay
from PyQt5 import QtWidgets, QtGui, QtCore
from network_error import *


class Menu(QtWidgets.QMainWindow, Ui_Menu):
    def __init__(self):
        try:
            super().__init__()
            self.setupUi(self)
            self.network = network.Network()
            self.icon.setFocus()
            self.login_line.hide()
            self.password_line.hide()
            self.enter.hide()
            self.employee_screen = None
            self.case_pay = None
            self.restore_password = False
            self.register = False
            self.employee.clicked.connect(self.employee_pressed)
            self.citizen.clicked.connect(self.citizen_pressed)
            self.icon0 = QtGui.QIcon()
            self.icon0.addPixmap(
                QtGui.QPixmap(os.path.join(os.path.dirname(__file__), 'icons', "question.png")),
                QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.icon.setIcon(self.icon0)
            self.icon1 = QtGui.QIcon()
            self.icon1.addPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), 'icons', "police.png")),
                                 QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.icon2 = QtGui.QIcon()
            self.icon2.addPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), 'icons', "user.png")),
                                 QtGui.QIcon.Normal, QtGui.QIcon.Off)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), 'icons', "eye.png")),
                           QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.show_password.setIcon(icon)
            self.show_password.setIconSize(QtCore.QSize(21, 21))
            self.enter.clicked.connect(self.enter_pressed)
            self.forgot_password.clicked.connect(self.forgot_password_pressed)
            self.registration.clicked.connect(self.registration_pressed)
            self.back.clicked.connect(self.back_pressed)
            self.show_password.clicked.connect(self.show_password_pressed)
            self.registration.hide()
            self.forgot_password.hide()
            self.back.hide()
            self.show_password.hide()
            self.username.hide()
            self.phone.hide()
            self.login_line.setGeometry(20, 110, 331, 41)
            self.forgot_password.hide()

        except Exception as e:
            print(e)

    def show_password_pressed(self):
        if self.password_line.echoMode() == 2:
            self.password_line.setEchoMode(0)
        elif self.password_line.echoMode() == 0:
            self.password_line.setEchoMode(2)

    def back_pressed(self):
        self.back.hide()
        self.password_line.setText('')
        self.password_line.show()
        self.registration.show()
        self.employee.show()
        self.citizen.show()
        self.login_line.setGeometry(20, 110, 331, 41)
        self.username.hide()
        self.phone.hide()
        self.show_password.show()
        self.password_line.setEchoMode(2)
        self.enter.setText('Войти')
        self.login_line.setPlaceholderText('Имя пользователя')
        self.message.setText('')
        self.restore_password = False
        self.register = False
        self.password_line.clear()
        self.login_line.setText(self.username.text())
        self.username.clear()
        self.phone.clear()
        self.forgot_password.hide()

    def registration_pressed(self):
        self.register = True
        self.back.show()
        self.login_line.setGeometry(20, 160, 331, 41)
        self.username.show()
        self.phone.show()
        self.login_line.clear()
        self.password_line.clear()
        self.employee.hide()
        self.login_line.setPlaceholderText('Email')
        self.password_line.setEchoMode(2)
        self.citizen.hide()
        self.registration.hide()
        self.forgot_password.hide()
        self.show_password.show()
        self.message.setText('')
        self.enter.setText('Создать')

    def forgot_password_pressed(self):
        self.restore_password = True
        self.password_line.hide()
        self.back.show()
        self.employee.hide()
        self.login_line.setPlaceholderText('Имя пользователя')
        self.password_line.setEchoMode(2)
        self.citizen.hide()
        self.registration.hide()
        self.forgot_password.hide()
        self.show_password.hide()
        self.message.setText('')
        self.enter.setText('Отправить')

    def employee_pressed(self):
        self.employee.setDisabled(True)
        self.citizen.setEnabled(True)
        self.login_line.setPlaceholderText('ID сотрудника')
        self.login_line.setText('')
        self.message.setText('')
        self.login_line.show()
        self.password_line.show()
        self.icon.setIcon(self.icon1)
        self.registration.hide()
        self.show_password.show()
        self.password_line.setEchoMode(2)
        self.enter.show()
        self.password_line.clear()

    def citizen_pressed(self):
        self.registration.show()
        self.message.clear()
        self.login_line.setPlaceholderText('Имя пользователя')
        self.citizen.setDisabled(True)
        self.employee.setEnabled(True)
        self.login_line.show()
        self.password_line.show()
        self.icon.setIcon(self.icon2)
        self.show_password.show()
        self.password_line.setEchoMode(2)
        self.enter.show()
        self.login_line.clear()
        self.password_line.clear()

    def enter_pressed(self):
        self.message.clear()
        if self.register:
            if self.login_line.text().strip() == '' or self.password_line.text().strip() == '' \
                    or self.username.text().strip() == '' \
                    or self.phone.text().strip() == '':
                self.message.setText('Поля не должны быть пустыми!')
            elif not check(self.login_line.text()):
                self.message.setText('Почтовый адрес введен неверно!')
            else:
                response = self.network.registration(self.login_line.text(), self.phone.text(),
                                                     self.username.text(),
                                                     self.password_line.text())
                if 'you register, dear' in response:
                    self.password_line.setEchoMode(2)
                    self.back_pressed()
                else:
                    self.message.setText('Неправильно указаны данные')
        elif self.restore_password and self.password_line.isHidden():
            self.password_line.show()
            self.password_line.setText('')
            self.enter.setText('ОК')
            self.show_password.hide()
            self.login_line.setPlaceholderText('Код')
            self.password_line.setEchoMode(2)
            # TODO: Отправить код на почту
        elif self.restore_password and not self.password_line.isHidden():
            # TODO: Ввод нового пароля
            self.back_pressed()
            self.password_line.setEchoMode(2)
        elif self.citizen.isEnabled():
            try:
                if self.login_line.text().strip() != '' and self.password_line.text().strip() != '':
                    if self.network.login_policeman(self.login_line.text(), self.password_line.text()):
                        self.hide()
                        self.employee_screen = EmployeeScreen(self, self.network)
                        self.password_line.setEchoMode(2)
                        self.employee_screen.show()
                    else:
                        self.message.setText('Ошибка авторизации. Проверьте данные')
                else:
                    self.message.setText('Заполните поля, пожалуйста')
            except ServerError as e:
                self.message.setText(e.__str__())
            except Exception:
                self.message.setText('Непредвиденная ошибка. Тех. поддержка 88005553535')
        elif self.employee.isEnabled():
            try:
                if self.login_line.text().strip() != '' and self.password_line.text().strip() != '':
                    if self.network.login_person(self.login_line.text(), self.password_line.text()):
                        print('here')
                        self.hide()
                        self.case_pay = CasePay(self, self.network)
                        self.password_line.setEchoMode(2)
                        self.case_pay.show()
                    else:
                        self.message.setText('Ошибка авторизации. Проверьте данные')
                else:
                    self.message.setText('Заполните поля, пожалуйста')
            except ServerError as e:
                self.message.setText(e.__str__())
            except Exception:
                self.message.setText('Непредвиденная ошибка. Тех. поддержка 88005553535')


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
