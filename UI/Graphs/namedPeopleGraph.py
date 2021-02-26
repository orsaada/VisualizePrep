import sys


from PyQt5.QtWidgets import QMainWindow

import numpy as np
from BussinesLayer.Data.data import extract_namedPeople, manage_config

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

    def init_chart(self, path):
        file_path = manage_config()
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
        sc.axes.bar(x, y)
        sc.axes.tick_params(labelbottom=False)
        sc.axes.set_xlabel('named People')
        sc.axes.set_ylabel('confidence')
        sc.axes.title.set_text('confidence per named people')

        return sc


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = NamedPeopleGraph()
    w.show()
    app.exec_()
