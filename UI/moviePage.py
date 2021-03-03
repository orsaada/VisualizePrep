import os
import sys

from PyQt5.QtCore import QThread, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QApplication, \
    QProgressDialog

from BussinesLayer.Algorithms.Visualize.mg.py3loader.algorithm import get_progress_val
from UI.Graphs.comparisonGraph import ComparisonGraph
from UI.PageWindow import PageWindow
import json


# Movie Page
from UI.Worker import Worker


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

        # progress bar
        self.worker = Worker()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.worker.workRequested.connect(self.thread.start)
        self.thread.started.connect(self.worker.add_tabs)
        self.worker.finished.connect(self.on_finish)

        self.button = QPushButton("Add tabs")
        self.button.clicked.connect(self.on_button_click)

        # self.progress = QProgressDialog("Progress", "cancel", 0, 10)
        # self.progress.setCancelButton(None)

        self.worker.relay.connect(self.update_progress)

        dlgLayout.addWidget(self.button)

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

    # functions for progress bar: on_button_click, on_finish, update_progress, responsive
    def on_button_click(self):
        self.button.setEnabled(False)
        self.worker.request_work()
        self.progress.setValue(0)

    def on_finish(self):
        self.button.setEnabled(True)
        self.thread.quit()

    def update_progress(self, value):
        value = get_progress_val()
        self.progress.setValue(value)

    def create_progres_bar(self):
        self.progress = QProgressDialog("Progress", "cancel", 0, 10)
        self.progress.setCancelButton(None)

    def responsive(self):
        print("Yes!")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyMovie()
    window.show()

    sys.exit(app.exec_())
