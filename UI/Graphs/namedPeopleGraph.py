import sys
from pathlib import Path

import matplotlib.pyplot as plt
from PyQt5.QtChart import QChartView
from PyQt5.QtWidgets import QVBoxLayout, QMainWindow
from matplotlib import rcParams
import matplotlib.ticker as mticker
import numpy as np
from BussinesLayer.Data.data import extract_speakers, extract_keywords, extract_namedPeople

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


class NamedPeopleGraph(QMainWindow):

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
        named_people = extract_namedPeople(file_path)
        df1 = pd.DataFrame()
        for y in named_people:
            if not isinstance(y, str):
                df1 = df1.append(y, ignore_index=True)
            else:
                pass
        print(df1.columns)
        x = np.arange(len(df1['confidence']))
        y = df1['confidence']


        # Create the maptlotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.plot(x, y)
        # sc.axes.set_xticks(x)
        # sc.axes.set_xticklabels(x, rotation=90, rotation_mode="default")
        sc.axes.tick_params(labelbottom=False)
        sc.axes.set_xlabel('named People')
        sc.axes.set_ylabel('confidence')
        return sc


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = NamedPeopleGraph()
    app.exec_()
