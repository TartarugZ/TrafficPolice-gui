from py_ui.complaint import Ui_Complaint
from PyQt5 import QtWidgets


class Complaint(QtWidgets.QMainWindow, Ui_Complaint):
    def __init__(self, net, case_id):
        try:
            super().__init__()
            self.setupUi(self)
            self.network = net
            self.case_id = case_id
            self.send_complaint.clicked.connect(self.send_complaint_pressed)
        except Exception as e:
            print(e)

    def send_complaint_pressed(self):
        self.network.post_complaint(self.case_id, self.passport.text(), self.full_justification.isChecked(),
                                    self.was_a_driver.isChecked(), self.comment.toPlainText())
