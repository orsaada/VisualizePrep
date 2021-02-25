import json
from pathlib import Path

from PyQt5.QtWidgets import QApplication, QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QLabel

from BussinesLayer.Services.VideoInsights import get_analyzed_data
from UI.Graphs.comparisonGraph import ComparisonGraph
from UI.PageWindow import PageWindow
import sys
from PyQt5.QtWidgets import (QToolTip, QPushButton, QApplication)
from PyQt5.QtGui import QFont


class ComparisonWindow(PageWindow):

    def __init__(self, algoName):
        super().__init__()
        self.setWindowTitle('My App')
        self.resize(500, 500)
        # Cannot set QxxLayout directly on the QMainWindow
        # Need to create a QWidget and set it as the central widget
        widget = QWidget()
        layout = QVBoxLayout()
        # for all algorithms:
        # loading 1/5 2/5 3/5 4/5 5/5
        b1 = QPushButton('Back To Movie Page')
        b1.setStyleSheet("background-color: red;")
        b1.clicked.connect(self.goToMovie)

        base_path = Path(__file__).parent.parent
        with open((base_path / 'config.json').resolve(), 'r') as f:
            data = json.load(f)
        if data["ttMovie"] == '':
            return
        else:
            a, b = get_analyzed_data(data["ttMovie"], data["ttMovie"], int(data['algo'].split()[1]))
        a, b = list(map(float, a)), list(map(float, b))
        a[2] *= 100
        b[2] *= 100
        b3 = ComparisonGraph(data['algo'], a, b)
        b3.update()

        label_values1 = QLabel()
        label_values1.setText(str(a))
        label_values2 = QLabel()
        label_values2.setText(str(b))

        details = QLabel("Details about algorithm: ")
        layout.addWidget(b1)
        layout.addWidget(b3)
        layout.addWidget(label_values1)
        layout.addWidget(label_values2)
        layout.addWidget(details)

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
