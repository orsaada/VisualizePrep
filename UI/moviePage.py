import os
import sys

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QApplication

from UI.Graphs.comparisonGraph import ComparisonGraph
from UI.PageWindow import PageWindow
import json


# Movie Page
class MyMovie(PageWindow):
    def __init__(self):
        super().__init__()
        self.form_widget = MyMovieWidget()
        self.resize(500, 500)
        self.setCentralWidget(self.form_widget)


class MyMovieWidget(QWidget):
    def gotoBack(self):
        self.parent().goto("archive")

    def __init__(self):
        super().__init__()
        dlgLayout = QVBoxLayout()
        # Create a form layout and add widgets
        formLayout = QFormLayout()
        with open('./../config.json', 'r') as f:
            data = json.load(f)
        name = data["SpecificMoviePage"]
        formLayout.addRow(name + " Page - Menu", QLabel())
        dlgLayout.addLayout(formLayout)

        algo_buttons_list = list(map(lambda x: QPushButton, range(4)))
        self.btn_algo1 = QPushButton()
        self.btn_algo1.setText('algo 1')
        self.btn_algo1.clicked.connect(lambda: self.compareGraph('algo 1'))

        self.btn_algo2 = QPushButton()
        self.btn_algo2.setText('algo 2')
        self.btn_algo2.clicked.connect(lambda: self.compareGraph('algo 2'))

        self.btn_algo3 = QPushButton()
        self.btn_algo3.setText('algo 3')
        self.btn_algo3.clicked.connect(lambda: self.compareGraph('algo 3'))

        self.btn_algo4 = QPushButton()
        self.btn_algo4.setText('algo 4')
        self.btn_algo4.clicked.connect(lambda: self.compareGraph('algo 4'))

        self.insights = QPushButton()
        self.insights.setText('insights graphs')
        self.insights.clicked.connect(self.gotToInsights)
        # self.comparisonGraph = QPushButton()
        # self.comparisonGraph.setText('comparison Graph')
        # self.comparisonGraph.clicked.connect(self.compareGraph)

        dlgLayout.addWidget(self.btn_algo1)
        dlgLayout.addWidget(self.btn_algo2)
        dlgLayout.addWidget(self.btn_algo3)
        dlgLayout.addWidget(self.btn_algo4)
        dlgLayout.addWidget(self.insights)
        # dlgLayout.addWidget(self.comparisonGraph)

        self.btnBackBox = QPushButton()
        self.btnBackBox.setText('Back')
        self.btnBackBox.clicked.connect(self.gotoBack)
        dlgLayout.addWidget(self.btnBackBox)
        self.setLayout(dlgLayout)

    def compareGraph(self, algo_name):
        with open('./../config.json', 'r') as f:
            data = json.load(f)
            data["algo"] = algo_name
        os.remove('./../config.json')
        with open('./../config.json', 'w') as f:
            json.dump(data, f, indent=4)
        self.parent().goto("comparison")

    def gotToInsights(self):
        self.parent().goto("insights")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyMovie()
    window.show()

    sys.exit(app.exec_())