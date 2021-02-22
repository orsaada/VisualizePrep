from PyQt5.QtWidgets import QApplication, QHBoxLayout, QPushButton, QVBoxLayout, QWidget

from UI.Graphs.comparisonGraph import ComparisonGraph
from UI.PageWindow import PageWindow
import sys
from PyQt5.QtWidgets import (QToolTip, QPushButton, QApplication)
from PyQt5.QtGui import QFont


class ComparisonWindow(PageWindow):

    def __init__(self, algoName):
        super().__init__()
        self.setWindowTitle('My App')
        self.resize(500,500)
        # Cannot set QxxLayout directly on the QMainWindow
        # Need to create a QWidget and set it as the central widget
        widget = QWidget()
        layout = QVBoxLayout()
        # for all algorithms:
        # loading 1/5 2/5 3/5 4/5 5/5
        b1 = QPushButton('Back To Movie Page')
        b1.setStyleSheet("background-color: red;")
        b1.clicked.connect(self.goToMovie)
        b3 = ComparisonGraph("name")
        layout.addWidget(b1)
        layout.addWidget(b3)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def goToMovie(self):
        self.parent().parent().goto('movie')


def main():
    app = QApplication(sys.argv)
    window = ComparisonWindow("wow")
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
