import json
from py_ui.find_protocol import Ui_FindComplaint
from PyQt5 import QtWidgets


class FindProtocol(QtWidgets.QMainWindow, Ui_FindComplaint):
    def __init__(self, net):
        try:
            super().__init__()
            self.setupUi(self)
            self.network = net
            self.delete_btn.clicked.connect(self.delete_pressed)
            self.submit_find_complaint.clicked.connect(self.submit_find_complaint_pressed)
            self.choose_cb.currentIndexChanged.connect(self.cb_choose_selected)
            self.complaints = {}
            self.choose_cb.addItem('-')
        except Exception as e:
            print(e)

    def delete_pressed(self):
        self.message.setText('')
        try:
            if self.case_id.text() is not None and self.case_id.text().strip() != '' \
                    and int(self.case_id.text()) > 0:
                a = self.network.delete_complaint(self.case_id.text())
                if "you deleted your beautifull complaint, dear" in a:
                    self.message.setText('Успешно удалено')
        except Exception as e:
            print(e)

    def cb_choose_selected(self):
        try:
            if self.choose_cb.currentText() != '-':
                self.output.setText(self.complaints[self.choose_cb.currentText()])
        except Exception as e:
            print(e)

    def submit_find_complaint_pressed(self):
        try:
            self.choose_cb.clear()
            self.choose_cb.addItem('-')
            if self.complaint_id.text().strip() != '' \
                    and self.case_id.text().strip() != '' \
                    and self.passport.text().strip() != '':
                complaints = self.network.get_complaints_citizen(self.complaint_id.text(), self.case_id.text(),
                                                                 self.passport.text())
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
                    print('Already here')
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
