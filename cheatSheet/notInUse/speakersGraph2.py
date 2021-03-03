import sys
import dateutil.parser
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries
from PyQt5.QtCore import Qt
from BussinesLayer.Data.data import analyze_speakers_graph
from UI.Graphs.Graph import GraphBar


def format_time(str_s):
    return dateutil.parser.parse(str_s)


def to_integer(dt_time):
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day


class speakersGraph2(QMainWindow, GraphBar):

    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        chart = self.init_chart(1)
        self.chartView = QChartView(chart)
        self.setCentralWidget(self.chartView)

    def init_chart(self, path):
        sets, ranges,labelX = analyze_speakers_graph()
        sets_arr = []
        for i in range(len(sets)):
            sets_arr.append(sets[i])
            sets_arr[i].append(ranges[i])

        series_arr = []
        for ele in sets_arr:
            series = QBarSeries()
            series.append(ele)
            series_arr.append(series)
        chart = QChart()
        for i in series_arr:
            chart.addSeries(i)
        chart.setTitle('Bar Chart Speakers')
        chart.setAnimationOptions(QChart.SeriesAnimations)

        months = labelX

        axisX = QBarCategoryAxis()
        axisX.append(months)
        axisX.setLabelsAngle(-90)  # <--------

        axisY = QValueAxis()

        axisY.setRange(0, max(ranges))
        axisY.setTitleText("instances")

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
        return chart

    def get_df(self):
        return self.df


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = speakersGraph2()
    window.show()

    sys.exit(app.exec_())
