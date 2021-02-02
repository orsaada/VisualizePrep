from PyQt5 import QtCore, QtGui, QtWidgets
# from PageWindow import PageWindow
# from UI.mediaplayerex import MediaWindow
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton

from UI.PageWindow import PageWindow
from UI.mediaplayerex import MediaWindow, MyMainWindow


class MainWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.form_widget = MainWidg()
        self.setCentralWidget(self.form_widget)

    def initUI(self):
        self.UiComponents()

    def UiComponents(self):
        self.searchButton = QtWidgets.QPushButton("", self)
        self.searchButton.clicked.connect(
            self.make_handleButton("searchButton")
        )
        self.searchButton1 = QtWidgets.QPushButton("", self)
        self.searchButton1.clicked.connect(
            self.make_handleButton("searchButton")
        )

    def make_handleButton(self, button):
        def handleButton():
            if button == "searchButton":
                self.goto("search")
        return handleButton


# class SearchWindow(PageWindow):
#     def __init__(self):
#         super().__init__()
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle("Search for something")
#         self.UiComponents()
#
#     def goToMain(self):
#         self.goto("main")
#
#     def UiComponents(self):
#         self.backButton = QtWidgets.QPushButton("BackButton", self)
#         self.backButton.setGeometry(QtCore.QRect(10, 5, 100, 20))
#         self.backButton.clicked.connect(self.goToMain)
#


class MainWidg(QWidget):
    def func(self):
        self.parent().goto("search")

    def __init__(self):
        super().__init__()
        #self.initUI()
        self.setWindowTitle("MainWindow")
        dlgLayout = QVBoxLayout()
        # Create a form layout and add widgets
        formLayout = QFormLayout()
        formLayout.addRow("Login Page", QLabel())
        formLayout.addRow("Name:", QLineEdit())
        formLayout.addRow("Password:", QLineEdit())
        # Add a button box
        self.btnLoginBox = QPushButton()
        self.btnLoginBox.setText('Login')
        self.btnLoginBox.clicked.connect(self.func)

        self.btnRegisterBox = QPushButton()
        self.btnRegisterBox.setText('Register')
        self.btnRegisterBox.clicked.connect(self.func)
        # Set the layout on the dialog
        dlgLayout.addLayout(formLayout)
        dlgLayout.addWidget(self.btnLoginBox)
        dlgLayout.addWidget(self.btnRegisterBox)
        self.setLayout(dlgLayout)



class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.m_pages = {}

        self.register(MainWindow(), "main")
        self.register(MyMainWindow(), "search")

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
    w.show()
    sys.exit(app.exec_())
