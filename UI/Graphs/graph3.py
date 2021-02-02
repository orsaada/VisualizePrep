import sys, random
from pathlib import Path
from time import mktime

from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter
import re
from datetime import datetime
import dateutil.parser

from BussinesLayer.Data.data import extract_emotions


def format_time(str):
    return dateutil.parser.parse(str)
    # return datetime.strptime(str, "%H:%M:%S.%f")


def to_integer(dt_time):
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day


class ChartEmotions(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)

        # print(extract_emotions("/Users/orsaada/Documents/programming development/אוניברסיטה/פרויקט גמר/visPrep/BussinesLayer/Algorithms/Visualize/vi_json/tt0988595.json"))

        base_path = Path(__file__).parent.parent
        file_path = (base_path / "../DB/jsonsFolder/tt0988595.json").resolve()
        emotions = extract_emotions(file_path)
        sets = []
        ranges = []
        for idx2, i in enumerate(emotions):
            sets.append(QBarSet(i['type']))
            # print(i['type'])
            # arr = []
            sum_time = 0
            for idx, val in enumerate(i['instances']):
                range_time = mktime(format_time(val['end']).timetuple())-mktime(format_time(val['start']).timetuple())
                # print(mktime(format_time(val['end']).timetuple())-mktime(format_time(val['start']).timetuple()))
                sum_time = sum_time + range_time
                # format_time(val['end'])-format_time(val['start'])
            ranges.append(sum_time)
        set0 = sets[0]
        set1 = sets[1]
        set2 = sets[2]

        # 1:29:37.79 regex
        # re.search("", "%H:%m:%S")
        # time.
        x = datetime.strptime("1:29:37.79", "%H:%M:%S.%f")
        # print(x)
        # x = time.strptime("30 Nov 00", "%d %b %y")
        # print(x)
        # print(ranges)
        #
        # set0 = QBarSet('X0')
        # set1 = QBarSet('X1')
        # set2 = QBarSet('X2')
        # set3 = QBarSet('X3')
        # set4 = QBarSet('X4')
        # print([random.randint(0, 10) for i in range(6)])
        set0.append(ranges[0])
        set1.append(ranges[1])
        set2.append(ranges[2])
        # set3.append([random.randint(0, 10) for i in range(6)])
        # set4.append([random.randint(0, 10) for i in range(6)])

        series = QBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        # series.append(set3)
        # series.append(set4)

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

        self.chartView = QChartView(chart)
        self.setCentralWidget(self.chartView)

def chart(self):
    return self.chartView


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = ChartEmotions()
    window.show()

    sys.exit(app.exec_())
