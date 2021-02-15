from pathlib import Path

from PyQt5 import QtWidgets
from datetime import datetime
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


from BussinesLayer.Data.data import extract_speakers


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)


        # plot colab
        base_path = Path(__file__).parent.parent.parent
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
        # print(by_instance['range'])
        # print(np.array(['1','2','3']).astype(np.float))
        # # a = np.array(by_instance['instance']).astype(np.float)
        # b = np.array(by_instance['range']).astype(np.float)
        # self.graphWidget.plot(list(by_instance['instance']), b)
        print()





        # working plot
        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]

        # plot data: x, y values
        self.graphWidget.plot(hour, temperature)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()