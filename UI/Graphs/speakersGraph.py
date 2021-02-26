import sys

import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from BussinesLayer.Data.data import extract_attribute_to_df

from PyQt5 import QtWidgets
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        fig.subplots_adjust(0.2, 0.3, 0.8, 0.8)  # left,bottom,right,top
        super(MplCanvas, self).__init__(fig)


class SpeakersGraph(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(1000,1000)
        self.sc = self.init_chart(1)
        layout = QVBoxLayout()
        layout.addWidget(self.sc)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        # self.setCentralWidget(self.sc)

    def init_chart(self, path):
        df = extract_attribute_to_df("speakers")

        by_instance = pd.DataFrame(columns=['instance', 'start', 'end'])
        if df.empty:
            a, b = [], []
        else:
            a, b = df['instances'], df['name']
        for instances, name in zip(a, b):
            for y in instances:
                by_instance = by_instance.append({'instance': name, 'start': y['start'],
                                                  'end': y['end']}, ignore_index=True)
        # print(by_instance)
        by_instance['start'] = pd.to_datetime(by_instance['start'])
        by_instance['end'] = pd.to_datetime(by_instance['end'])

        by_instance['range'] = by_instance['end'] - by_instance['start']
        by_instance = by_instance.groupby(['instance'])['range'].sum().reset_index(name='range')
        plt.plot(by_instance['instance'], by_instance['range'])
        plt.xticks(rotation=90)

        sets, ranges = list(by_instance['instance']), list(map(lambda x: x.total_seconds(), by_instance['range']))
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=5, dpi=100,)
        # sc.axes.plot(by_instance['instance'], by_instance['range'])
        sc.axes.bar(sets, ranges)

        sc.axes.set_xticks(by_instance['instance'])
        sc.axes.set_xticklabels(by_instance['instance'], rotation=45, rotation_mode="default")
        sc.axes.set_xlabel('speakers')
        sc.axes.set_ylabel('time spoke in seconds')
        sc.axes.title.set_text('time spoke per named people')

        return sc


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = SpeakersGraph()
    w.show()
    app.exec_()
