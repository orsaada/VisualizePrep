from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton
from UI.PageWindow import PageWindow
from UI.mediaplayerex import MyMainWindow
from UI.archiveWindow import MyArchive
from BussinesLayer.Services.Login import log_in
from BussinesLayer.Services.Register import registration
import json
import os

# Register Page
class MyRegister(PageWindow):
    def __init__(self):
        super().__init__()
        self.form_widget = MyRegisterWidget()
        self.setCentralWidget(self.form_widget)


class MyRegisterWidget(QWidget):
    def pop_message(self, text):
        msg = QtWidgets.QMessageBox()
        msg.setText("{}".format(text))
        msg.exec_()

    def cleanFields(self):
        self.name.setText('')
        self.lastname.setText('')
        self.phone.setText('')
        self.email.setText('')
        self.username.setText('')
        self.password.setText('')

    def gotoBack(self):
        self.parent().goto("main")

    def gotoMedia(self):
        res = registration(self.name.text(), self.lastname.text(), self.phone.text(), self.email.text(),
                           self.username.text(), self.password.text())
        if res == 'Successfully Registration':
            self.pop_message('Successfully Registration')
            with open('./../config.json', 'r') as f:
                data = json.load(f)
                data['UserLoggedIn'] = self.username.text()
            os.remove('./../config.json')
            with open('./../config.json', 'w') as f:
                json.dump(data, f, indent=4)
            self.cleanFields()
            self.parent().goto("media")
        else:
            self.pop_message(res)

    def __init__(self):
        super().__init__()
        dlgLayout = QVBoxLayout()
        # Create a form layout and add widgets
        formLayout = QFormLayout()
        self.name = QLineEdit()
        self.lastname = QLineEdit()
        self.phone = QLineEdit()
        self.email = QLineEdit()
        self.username = QLineEdit()
        self.password = QLineEdit()
        formLayout.addRow("Register Page", QLabel())
        formLayout.addRow("Name:", self.name)
        formLayout.addRow("Last Name:", self.lastname)
        formLayout.addRow("Phone:", self.phone)
        formLayout.addRow("Email:", self.email)
        formLayout.addRow("Username:", self.username)
        formLayout.addRow("Password:", self.password)
        # Add a button box

        self.btnRegisterBox = QPushButton()
        self.btnRegisterBox.setText('Send')
        self.btnRegisterBox.clicked.connect(self.gotoMedia)

        self.btnBackBox = QPushButton()
        self.btnBackBox.setText('Back')
        self.btnBackBox.clicked.connect(self.gotoBack)
        # Set the layout on the dialog
        dlgLayout.addLayout(formLayout)
        dlgLayout.addWidget(self.btnRegisterBox)
        dlgLayout.addWidget(self.btnBackBox)
        self.setLayout(dlgLayout)


# Login Page
class MainWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.form_widget = MainWidg()
        self.setCentralWidget(self.form_widget)


class MainWidg(QWidget):

    def pop_message(self, text):
        msg = QtWidgets.QMessageBox()
        msg.setText("{}".format(text))
        msg.exec_()

    def cleanFields(self):
        self.username.setText('')
        self.password.setText('')

    def gotoMedia(self):
        if len(self.username.text()) < 1 or len(self.password.text()) < 1:
            self.pop_message('Empty fields')
        else:
            res = log_in(self.username.text(), self.password.text())
            if res == "Successfully Login":
                self.pop_message('Successfully Login')
                with open('./../config.json', 'r') as f:
                    data = json.load(f)
                    data['UserLoggedIn'] = self.username.text()
                os.remove('./../config.json')
                with open('./../config.json', 'w') as f:
                    json.dump(data, f, indent=4)
                self.cleanFields()
                self.parent().goto("media")
            else:
                self.pop_message(res)

    def gotoRegister(self):
        self.cleanFields()
        self.parent().goto("register")

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MainWindow")
        dlgLayout = QVBoxLayout()
        # Create a form layout and add widgets
        formLayout = QFormLayout()
        self.username = QLineEdit()
        self.password = QLineEdit()
        formLayout.addRow("Login Page", QLabel())
        formLayout.addRow("Username:", self.username)
        formLayout.addRow("Password:", self.password)

        # Add a button login
        self.btnLoginBox = QPushButton()
        self.btnLoginBox.setText('Login')
        self.btnLoginBox.clicked.connect(self.gotoMedia)

        self.btnRegisterBox = QPushButton()
        self.btnRegisterBox.setText('Register')
        self.btnRegisterBox.clicked.connect(self.gotoRegister)
        # Set the layout on the dialog
        dlgLayout.addLayout(formLayout)
        dlgLayout.addWidget(self.btnLoginBox)
        dlgLayout.addWidget(self.btnRegisterBox)
        self.setLayout(dlgLayout)


# App Window
class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.m_pages = {}

        self.register(MainWindow(), "main")
        self.register(MyMainWindow(), "media")
        self.register(MyRegister(), "register")
        self.register(MyArchive(), "archive")
        self.goto("main")

    def register(self, widget, name):
        self.m_pages[name] = widget
        self.stacked_widget.addWidget(widget)
        if isinstance(widget, PageWindow):
            widget.gotoSignal.connect(self.goto)

    @QtCore.pyqtSlot(str)
    def goto(self, name):
        if name in self.m_pages:
            widget = self.m_pages[name]
            self.stacked_widget.setCurrentWidget(widget)
            self.setWindowTitle(widget.windowTitle())


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.resize(400, 400)
    w.show()
    sys.exit(app.exec_())
