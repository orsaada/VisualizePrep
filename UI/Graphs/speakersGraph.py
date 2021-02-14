import sys
from pathlib import Path

import matplotlib.pyplot as plt
from PyQt5.QtChart import QChartView
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow
from matplotlib import rcParams
import matplotlib.ticker as mticker

from BussinesLayer.Data.data import extract_speakers

# matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets
import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class SpeakersGraph(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(1000,1000)
        self.sc = self.init_chart(1)
        self.setCentralWidget(self.sc)
        self.show()

    def init_chart(self, path):
        # changes
        base_path = Path(__file__).parent.parent
        file_path = (base_path / "../BussinesLayer/Algorithms/Visualize/vi_json/tt0988595.json").resolve()
        speakers = extract_speakers(file_path)
        df = pd.DataFrame()
        for y in speakers:
            if not isinstance(y, str):
                df = df.append(y, ignore_index=True)
            else:
                pass
        instances_arr = df
        cp_df = instances_arr.copy()
        print(cp_df)

        by_instance = pd.DataFrame(columns=['instance', 'start', 'end'])
        for instances, name in zip(cp_df['instances'], cp_df['name']):
            for y in instances:
                by_instance = by_instance.append({'instance': name, 'start': y['start'],
                                                  'end': y['end']}, ignore_index=True)
        # print(by_instance)
        by_instance['start'] = pd.to_datetime(by_instance['start'])
        by_instance['end'] = pd.to_datetime(by_instance['end'])

        # by_instance['start'] =  pd.to_datetime(by_instance['start'], format='%H:%M:%S.%f')
        # print(by_instance)
        by_instance['range'] = by_instance['end'] - by_instance['start']
        # print(by_instance)
        by_instance = by_instance.groupby(['instance'])['range'].sum().reset_index(name='range')
        # print(by_instance)
        plt.plot(by_instance['instance'], by_instance['range'])
        plt.xticks(rotation=90)

        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot(by_instance['instance'], by_instance['range'])
        sc.axes.set_xticks(by_instance['instance'])
        sc.axes.set_xticklabels(by_instance['instance'], rotation=45, rotation_mode="default")
        sc.axes.set_xlabel('named People')
        sc.axes.set_ylabel('time spoke')
        return sc


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = SpeakersGraph()
    app.exec_()
