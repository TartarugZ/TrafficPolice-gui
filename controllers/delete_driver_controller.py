import json
from py_ui.delete_driver import Ui_DeleteDriver
from PyQt5 import QtWidgets


class DeleteDriver(QtWidgets.QMainWindow, Ui_DeleteDriver):
    def __init__(self, net, case_pay):
        try:
            super().__init__()
            self.setupUi(self)
            self.network = net
            self.case_pay = case_pay
            self.delete_driver_btn.clicked.connect(self.delete_driver_pressed)
            self.cb_drivers.addItem('-')
            if len(self.case_pay.existed_drivers) > 0:
                for key, value in self.case_pay.existed_drivers.items():
                    self.cb_drivers.addItem(str(key) + str(value))
        except Exception as e:
            print(e)

    def delete_driver_pressed(self):
        if self.cb_drivers.currentText() != '-':
            self.network.delete_person(self.cb_drivers.currentText()[:10])
            self.case_pay.existed_drivers = pase_persons(self.network.get_person())
            self.case_pay.put_drivers()
            self.close()


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