import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtChart import QChart, QChartView, QBarSet, QHorizontalPercentBarSeries, QBarCategoryAxis, QValueAxis
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter

from BussinesLayer.Data.data import extract_emotions


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(600, 400)

        print(extract_emotions("/Users/orsaada/Documents/programming development/אוניברסיטה/פרויקט גמר/visPrep/BussinesLayer/Algorithms/Visualize/vi_json/tt0988595.json"))
        emotions = extract_emotions("/Users/orsaada/Documents/programming development/אוניברסיטה/פרויקט גמר/visPrep/BussinesLayer/Algorithms/Visualize/vi_json/tt0988595.json")
        for i in emotions:
            print(i['type'])
            for j in i['instances']:
                print(j)
        set0 = QBarSet('X0')
        set1 = QBarSet('X1')
        set2 = QBarSet('X2')
        set3 = QBarSet('X3')
        set4 = QBarSet('X4')

        set0.append([1, 2, 3, 4, 5, 6])
        set1.append([5, 0, 0, 4, 0, 7])
        set2.append([3, 5, 8, 13, 8, 5])
        set3.append([5, 6, 7, 3, 4, 5])
        set4.append([9, 7, 5, 3, 1, 2])

        series = QHorizontalPercentBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)
        series.append(set4)

        chart = QChart()
        chart.setTitle('% Horizontal Bar Chart')
        chart.addSeries(series)

        chart.setAnimationOptions(QChart.SeriesAnimations)

        months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun')
        axisY = QBarCategoryAxis()
        axisY.append(months)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        axisX = QValueAxis()
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        self.chartView = QChartView(chart)
        self.setCentralWidget(self.chartView)


def chart(self):
    return self.chartView


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
