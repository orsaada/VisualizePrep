from PyQt5 import QtCore, QtGui, QtWidgets
from PageWindow import PageWindow

class MainWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("MainWindow")

    def initUI(self):
        self.UiComponents()

    def UiComponents(self):
        self.searchButton = QtWidgets.QPushButton("", self)
        self.searchButton.clicked.connect(
            self.make_handleButton("searchButton")
        )

    def make_handleButton(self, button):
        def handleButton():
            if button == "searchButton":
                self.goto("search")
        return handleButton







class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.m_pages = {}

        self.register(MainWindow(), "main")
        self.register(SearchWindow(), "search")

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