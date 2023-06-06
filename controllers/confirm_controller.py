import os

from py_ui.confirm import Ui_Confirm
from PyQt5 import QtWidgets, QtGui


class Confirm(QtWidgets.QMainWindow, Ui_Confirm):
    def __init__(self, net, menu, case_screen):
        try:
            super().__init__()
            self.setupUi(self)
            self.menu = menu
            self.case = case_screen
            self.network = net
            self.show_password.clicked.connect(self.show_password_pressed)
            self.delete_acc.clicked.connect(self.delete_acc_pressed)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(os.path.join(os.path.dirname(__file__), 'icons', "eye.png")),
                           QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.show_password.setIcon(icon)
        except Exception as e:
            print(e)

    def show_password_pressed(self):
        if self.password.echoMode() == 2:
            self.password.setEchoMode(0)
        elif self.password.echoMode() == 0:
            self.password.setEchoMode(2)

    def delete_acc_pressed(self):
        if self.password.text() is not None and self.password.text().strip() != '':
            response = self.network.delete_account(self.password.text())
            if 'you deleted, dear' in response:
                self.menu.show()
                self.case.close()
                self.close()
            else:
                self.label.setText('Неверные данные')
