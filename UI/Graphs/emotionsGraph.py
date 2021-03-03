import json
import sys
import dateutil.parser
import pandas as pd
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries
from PyQt5.Qt import Qt
from datetime import datetime
from BussinesLayer.Data.data import extract_emotions, manage_config, analyze_emotions_graph


def format_time(str):
    return dateutil.parser.parse(str)
    # return datetime.strptime(str, "%H:%M:%S.%f")


def to_integer(dt_time):
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day


class ChartEmotions(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        file_path = manage_config()
        self.emotions = extract_emotions(file_path)
        self.df = pd.DataFrame(self.emotions)
        chart = self.init_chart(' ')
        self.chartView = QChartView(chart)
        self.setCentralWidget(self.chartView)

    def init_chart(self, path):
        sets, ranges = analyze_emotions_graph()
        print(sets)
        print(ranges)
        sets_arr = []
        for i in range(len(sets)):
            sets_arr.append(sets[i])
            sets_arr[i].append(ranges[i])

        series = QBarSeries()
        for ele in sets_arr:
            series.append(ele)
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Bar Chart Emotions')
        chart.setAnimationOptions(QChart.SeriesAnimations)

        months = 'Emotions'

        axisX = QBarCategoryAxis()
        axisX.append(months)

        axisY = QValueAxis()
        axisY.setRange(0, max(ranges))
        axisY.setTitleText("seconds")

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        return chart

    def get_df(self):
        return self.df


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = ChartEmotions()
    window.show()

    sys.exit(app.exec_())
