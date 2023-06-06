import json
from py_ui.add_driver import Ui_AddDriver
from PyQt5 import QtWidgets


class AddDriver(QtWidgets.QMainWindow, Ui_AddDriver):
    def __init__(self, net, case_pay):
        try:
            super().__init__()
            self.setupUi(self)
            self.network = net
            self.case_pay = case_pay
            self.add_driver_btn.clicked.connect(self.add_driver_pressed)
        except Exception as e:
            print(e)

    def add_driver_pressed(self):
        try:
            if self.add_driver_passport.text() is not None and self.add_driver_passport.text().strip() != '' \
                    and len(self.add_driver_passport.text()) == 10:
                self.network.add_person(self.add_driver_passport.text())
                self.case_pay.existed_drivers = pase_persons(self.network.get_person())
                self.case_pay.put_drivers()
                self.close()
        except Exception as e:
            print(e)


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
