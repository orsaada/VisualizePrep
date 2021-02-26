import sys

from PyQt5.QtWidgets import QVBoxLayout, QMainWindow, QWidget
from BussinesLayer.Data.data import extract_shots_or, manage_config
from collections import Counter
import matplotlib.pyplot as plt
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


class shotsGraph(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(1000,1000)
        self.sc = self.init_chart(1)
        layout = QVBoxLayout()
        layout.addWidget(self.sc)
        layout.setContentsMargins(100,100,100,100)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        # self.setCentralWidget(self.sc)

        # self.show()

    def init_chart(self, path):
        file_path = manage_config()
        keywords = extract_shots_or(file_path)
        df1 = pd.DataFrame()
        for y in keywords:
            if not isinstance(y, str):
                df1 = df1.append(y, ignore_index=True)
            else:
                pass
        print(df1)

        by_instance = pd.DataFrame(columns=['instance', 'start', 'end'])
        for instances, name in zip(df1['instances'], df1['tags']):
            for y in instances:
                by_instance = by_instance.append({'instance': name, 'start': y['start'],
                                                  'end': y['end']}, ignore_index=True)
        by_instance = by_instance.dropna()
        print(by_instance)
        counter = Counter()
        for ar in by_instance['instance']:
            counter.update(ar)
            # for a in ar:
            #   print(type(a))
            #   counter.update(a)
        # print(counter)
        plt.bar(counter.keys(), counter.values())
        plt.xticks(rotation=90)

        # print(counter.keys())
        # print(counter.values())
        x = list(counter.keys())
        y = list(counter.values())
        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.bar(x, y)
        # sc.axes.plot(x, y)
        sc.axes.set_xticks(x)
        sc.axes.set_xticklabels(x, rotation=90, rotation_mode="default")

        sc.axes.set_xlabel('locations')
        sc.axes.set_ylabel('appearances in shots')
        sc.axes.title.set_text('location per shots')

        return sc


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = shotsGraph()
    w.show()
    app.exec_()
