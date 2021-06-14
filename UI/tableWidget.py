from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import pyqtSlot
import sys

class TableView(QTableWidget):
    def __init__(self, data, headers, *args):
        QTableWidget.__init__(self, *args)
        self.data = data
        self.headers = headers
        self.setData()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setDisabled(True)

    def setData(self):
        # horHeaders = []
        for n, row in enumerate(self.data):
            for m, column_data in enumerate(row):
                newitem = QTableWidgetItem(column_data)
                newitem.setForeground(QBrush(QColor(0, 255, 0)))
                self.setItem(n, m, newitem)
        self.setHorizontalHeaderLabels(self.headers)
