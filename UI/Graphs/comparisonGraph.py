import json
import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QMainWindow)
from PyQt5.QtChart import QChart, QChartView, QValueAxis, QBarCategoryAxis, QBarSet, QBarSeries
from BussinesLayer.Services.VideoInsights import get_analyzed_data


class ComparisonGraph(QMainWindow):
    def __init__(self, algo_name, a, b):
        super().__init__()
        self.resize(800, 600)

        if algo_name != 'transcript':
            set0 = QBarSet('Microsoft Video Indexer')
        set1 = QBarSet('Microsoft Video Indexer After Improvement Algorithm')

        # print(algo_name)
        # print(a)
        # print(b)

        series = QBarSeries()
        if algo_name != 'transcript':
            set0.append(a)
            series.append(set0)
        set1.append(b)
        series.append(set1)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle(algo_name + ' - Improvement Results Analytics')
        chart.setAnimationOptions(QChart.SeriesAnimations)

        months = ('Precision', 'Recall', 'Jaccard', 'F score')

        axisX = QBarCategoryAxis()
        axisX.append(months)

        axisY = QValueAxis()
        axisY.setRange(0, 100)

        chart.addAxis(axisX, Qt.AlignBottom)
        chart.addAxis(axisY, Qt.AlignLeft)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartView = QChartView(chart)
        self.setCentralWidget(chartView)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ComparisonGraph("algoName")
    window.show()
    sys.exit(app.exec_())
