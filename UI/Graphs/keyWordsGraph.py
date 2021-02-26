import sys
from pathlib import Path

import matplotlib.pyplot as plt
from PyQt5.QtChart import QChartView
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow

from BussinesLayer.Data.data import extract_speakers, extract_keywords, analyze_keywords_graph

from PyQt5 import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.subplots_adjust(0.2, 0.3, 0.8, 0.8)  # left,bottom,right,top
        super(MplCanvas, self).__init__(fig)


class KeywordGraph(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(1000, 1000)
        self.sc = self.init_chart(1)
        self.setCentralWidget(self.sc)

    def init_chart(self, path):
        langs, students = analyze_keywords_graph()

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot(langs, students)
        sc.axes.set_xticks(langs)
        sc.axes.set_xticklabels(langs, rotation=90, rotation_mode="default")

        sc.axes.set_xlabel('keywords')
        sc.axes.set_ylabel('number of instances')
        sc.axes.title.set_text('number of instances per keyword')

        return sc


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = KeywordGraph()
    app.exec_()
