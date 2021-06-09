import json
import os
from pathlib import Path

from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QComboBox, QLabel, QHBoxLayout

# from BussinesLayer.Algorithms.Visualize.mg.py3loader.action_recognition import get_action_recognition
from BussinesLayer.Algorithms.Visualize.mg.py3loader.split_movie import split_movie
from UI.PageWindow import PageWindow
import sys
from PyQt5.QtWidgets import (QPushButton, QApplication)

from UI.popUpWindow import MyPopup


class ActionRecognitionWindow(PageWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('My App')
        self.resize(500, 500)
        # Cannot set QxxLayout directly on the QMainWindow
        # Need to create a QWidget and set it as the central widget
        widget = QWidget()
        layout = QVBoxLayout()
        self.w = None
        b1 = QPushButton('Back To Movie Page')
        b1.setStyleSheet("background-color: red;")
        b1.clicked.connect(self.goToMovie)

        self.graphs = []
        with open('./../config.json') as f:
            data = json.load(f)
        if data['video_path'] != '':
            arr = [[('contact juggling', 39.15), ('dining', 17.6), ('bartending', 8.57), ('setting table', 3.75),
                    ('drinking', 3.29)],
                   [('zumba', 3.29), ('garbage collecting', 3.29), ('filling eyebrows', 3.29),
                    ('finger snapping', 3.29),
                    ('fixing hair', 3.29)]]
            action_result = self.analysis_action_reco()
            for scene in action_result:
                self.graphs.append(self.create_action_graph(scene))

        # dropdown choosing
        combo = QComboBox(self)
        for k in range(len(self.graphs)):
            combo.addItem(f'scene number {k + 1}')
        combo.move(50, 50)
        # not necessarily need
        self.qlabel = QLabel(self)
        self.qlabel.move(50, 16)

        combo.activated[str].connect(self.onChanged)

        # layout.addWidget(b1)
        # layout.addWidget(combo)
        # layout.addWidget(self.make_graph([1,2],[7,8]))
        # widget.setLayout(layout)

        if len(self.graphs) == 0:
            self.child = QWidget()
        else:
            self.child = self.graphs[0]

        layoutV = QVBoxLayout()

        self.layoutH = QHBoxLayout()
        self.layoutH.addWidget(combo)
        self.layoutH.addWidget(self.child)
        layoutV.addLayout(self.layoutH)
        widget.setLayout(layoutV)

        # else:
        #     self.w = MyPopup(self, 'you')
        #     self.w.setGeometry(QRect(100, 100, 400, 200))
        #     self.w.show()
        #     self.goToMovie()
        self.setCentralWidget(widget)

    def analysis_action_reco(self):
        try:
            pass
            with open('./../config.json') as f:
                data = json.load(f)
            video_path = data['video_path']
            ttmovie = data['ttMovie']
            head, tail = os.path.split(video_path)
            file_name = os.path.splitext(tail)[0]
            print(f'movie_path: {video_path}')
            print(f'name: {file_name}')
            # split_movie(video_path, ttmovie, file_name)
            # folder_splitted_path = 'BussinesLayer/Algorithms/Visualize/mg/py3loader/' + file_name
            # action_results = get_action_recognition()
            action_results = []
            return action_results
        except:
            self.w = MyPopup(self, 'you')
            self.w.setGeometry(QRect(100, 100, 400, 200))
            self.w.show()
            self.parent().goto('movie')

    def create_action_graph(self, arr):
        graphs_data = []
        for scene in arr:
            x = []
            y = []
            for action, percentage in scene:
                x.append(action)
                y.append(percentage)
            graphs_data.append(self.make_graph(x, y))
            # graphs_data.append((x,y))
        print(graphs_data)

    def make_graph(self, x, y):

        series = QPieSeries()
        series.setHoleSize(0.40)

        for ele_index in range(len(x)):
            series.append(f'{x[ele_index]} {y[ele_index]}', y[ele_index])
        series.append("Protein 4,3%", 4.3)

        my_slice = series.append("Fat 15.6%", 15.6)
        # my_slice.setExploded(True)
        my_slice.setLabelVisible(True)

        series.append("Other 30%", 30)
        series.append("Carbs 57%", 57)

        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Dount Chart")
        chart.setTheme(QChart.ChartThemeBlueCerulean)

        chartview = QChartView(chart)

        # vbox = QVBoxLayout()
        # vbox.addWidget(chartview)

        # self.setLayout(vbox)
        return chartview

    def goToMovie(self):
        self.goto('movie')

    def onChanged(self, text):
        self.showingGraphName = text
        self.layoutH.removeWidget(self.child)
        self.child.setParent(None)
        self.child = self.graphs[text]
        self.layoutH.addWidget(self.child)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ActionRecognitionWindow()
    window.show()
    sys.exit(app.exec_())
