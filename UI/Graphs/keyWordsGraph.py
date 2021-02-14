import sys
from pathlib import Path

import matplotlib.pyplot as plt
from PyQt5.QtChart import QChartView
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow
from matplotlib import rcParams
import matplotlib.ticker as mticker

from BussinesLayer.Data.data import extract_speakers, extract_keywords

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


class KeywordGraph(QMainWindow):

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
        keywords = extract_keywords(file_path)
        df1 = pd.DataFrame()
        for y in keywords:
            if not isinstance(y, str):
                df1 = df1.append(y, ignore_index=True)
            else:
                pass
        print(df1)
        number_of_instances = []
        for x in df1.instances:
            number_of_instances.append(len(x))
        df1['number_of_instances'] = number_of_instances

        import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        langs = df1['text']  # ['C', 'C++', 'Java', 'Python', 'PHP']
        students = df1['number_of_instances']  # [23,17,35,29,12]
        ax.bar(langs, students)
        # ax.set_xticks(ax.get_xticks()[::2])
        # plt.xticks(x[::5],  rotation='vertical')
        # plt.margins(0.2)
        plt.xticks(rotation=90)

        plt.show()



        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot(langs, students)
        sc.axes.set_xticks(langs)
        sc.axes.set_xticklabels(langs, rotation=90, rotation_mode="default")

        sc.axes.set_xlabel('named People')
        sc.axes.set_ylabel('time spoke')
        return sc


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = KeywordGraph()
    app.exec_()
