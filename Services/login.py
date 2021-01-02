from PyQt5 import QtCore

from Services.mediaplayerex import MediaWindow
from newuser import *
from BussinesLayer.Services.Login import log_in
from PyQt5 import QtWidgets

class Ui_Form(object):

    def openwindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Newuser()
        self.ui.setupUi(self.window)
        self.window.show()
        Form.hide()


    def setupUi(self, Form):
        self.mediawindo = MediaWindow(1)
        self.mediawindo.hide()
        Form.setObjectName("Form")
        Form.resize(650, 380)
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(150, 10, 361, 61))
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(100, 90, 431, 261))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.l_username = QtWidgets.QLabel(self.gridLayoutWidget)
        self.l_username.setObjectName("l_username")
        self.gridLayout.addWidget(self.l_username, 0, 0, 1, 1)
        self.l_password = QtWidgets.QLabel(self.gridLayoutWidget)
        self.l_password.setObjectName("l_password")
        self.gridLayout.addWidget(self.l_password, 1, 0, 1, 1)
        self.txt_password = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.txt_password.setObjectName("txt_password")
        self.gridLayout.addWidget(self.txt_password, 1, 1, 1, 1)
        self.txt_username = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.txt_username.setObjectName("txt_username")
        self.gridLayout.addWidget(self.txt_username, 0, 1, 1, 1)
        self.btn_submit = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_submit.setStyleSheet("background-color: rgb(27, 27, 27);\n"
                                      "color: \'white\';")
        self.btn_submit.setObjectName("btn_submit")
        self.gridLayout.addWidget(self.btn_submit, 2, 1, 1, 1)
        self.btn_newuser = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.btn_newuser.setStyleSheet("background-color: rgb(27, 27, 27);\n"
                                       "color: \'white\';")
        self.btn_newuser.setObjectName("btn_newuser")
        self.gridLayout.addWidget(self.btn_newuser, 3, 1, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        self.btn_newuser.clicked.connect(self.btn_newuser_handler)
        self.btn_submit.clicked.connect(self.btn_login_handler)


    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.textBrowser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                        "p, li { white-space: pre-wrap; }</style></head>\n"
                                                        "<body style=\" font-family:\'.Calibri\'; font-size:30pt;\">\n"
                                                        "<p align=\"center\">VisualizeBGU</p></body></html>"))
        self.l_username.setText(_translate("Form", "Username"))
        self.l_password.setText(_translate("Form", "Password"))
        self.btn_submit.setText(_translate("Form", "Connect"))
        self.btn_newuser.setText(_translate("Form", "Register"))


    def pop_window(self,text):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("{}".format(text))
        msg.setInformativeText('{}'.format(text))
        msg.setWindowTitle("{}".format(text))
        msg.exec_()


    def btn_newuser_handler(self):
        self.openwindow()


    def pop_message(self, text):
        msg = QtWidgets.QMessageBox()
        msg.setText("{}".format(text))
        msg.exec_()


    def btn_login_handler(self):
        if len(self.txt_password.text()) <= 1:
            self.pop_message('Enter Valid Data !')
        else:
            username = self.txt_username.text()
            password = self.txt_password.text()
            res = log_in(username, password)
            self.pop_message(res)
            # if res == Successfully Login -> jump load video
            if res == "Successfully Login":
                Form.hide()
                self.mediawindo.show()
            # ****  need to be logout button that back to login page  ****


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
