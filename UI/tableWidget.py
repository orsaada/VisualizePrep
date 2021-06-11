# import sys
# from PyQt5 import QtCore, QtGui, QtWidgets
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QHeaderView
#
#
# class TableModel(QtCore.QAbstractTableModel):
#     def __init__(self, data):
#         super(TableModel, self).__init__()
#         self._data = data
#
#     def data(self, index, role):
#         if role == Qt.DisplayRole:
#             # See below for the nested-list data structure.
#             # .row() indexes into the outer list,
#             # .column() indexes into the sub-list
#             return self._data[index.row()][index.column()]
#
#     def rowCount(self, index):
#         # The length of the outer list.
#         return len(self._data)
#
#     def columnCount(self, index):
#         # The following takes the first sub-list, and returns
#         # the length (only works if all rows are an equal length)
#         return len(self._data[0])
#
#
# class MainWindow(QtWidgets.QMainWindow):
#     def __init__(self):
#         super().__init__()
#
#         self.table = QtWidgets.QTableView()
#         self.table.setHorizontalHeader(QHeaderView())
#         data = [
#           [4, 9, 2],
#           [1, 0, 0],
#           [3, 5, 0],
#           [3, 3, 2],
#           [7, 8, 9],
#         ]
#
#         self.model = TableModel(data)
#         self.table.setModel(self.model)
#
#         self.setCentralWidget(self.table)
#
#
# # app=QtWidgets.QApplication(sys.argv)
# # window=MainWindow()
# # window.show()
# # app.exec_()
# a_data = [('0:09:30.703', '0:09:38.177', 'Unknown', 'Jack Nicholson'), ('0:09:44.317', '0:09:50.656', 'Unknown', 'Jack Nicholson'), ('0:09:57.33', '0:10:01.601', 'Unknown', 'Jack Nicholson'), ('0:10:04.938', '0:10:07.24', 'Unknown', 'Jack Nicholson'), ('0:10:18.284', '0:10:20.753', 'Unknown', 'Jack Nicholson'), ('0:10:23.556', '0:10:24.524', 'Unknown', 'Jack Nicholson'), ('0:10:25.892', '0:10:31.631', 'Unknown', 'Jack Nicholson'), ('0:10:38.438', '0:10:41.908', 'Unknown', 'Jack Nicholson'), ('0:10:50.783', '0:10:52.285', 'Unknown', 'Jack Nicholson'), ('0:10:55.121', '0:10:57.757', 'Unknown', 'Jack Nicholson'), ('0:11:02.595', '0:11:09.168', 'Unknown', 'Jack Nicholson'), ('0:11:16.009', '0:11:22.315', 'Unknown', 'Jack Nicholson'), ('0:11:28.288', '0:11:30.022', 'Unknown', 'Jack Nicholson'), ('0:11:33.76', '0:11:42.501', 'Unknown', 'Jack Nicholson'), ('0:11:49.509', '0:11:52.778', 'Unknown', 'Jack Nicholson'), ('0:11:57.784', '0:12:00.853', 'Unknown', 'Jack Nicholson'), ('0:12:04.991', '0:12:13.966', 'Unknown', 'Jack Nicholson'), ('0:12:24.344', '0:12:32.752', 'Unknown', 'Jack Nicholson'), ('0:12:34.354', '0:12:38.157', 'Unknown', 'Jack Nicholson'), ('0:12:40.493', '0:12:47.533', 'Unknown', 'Jack Nicholson'), ('0:12:53.106', '0:12:58.511', 'Unknown', 'Jack Nicholson'), ('0:13:01.914', '0:13:07.953', 'Unknown', 'Jack Nicholson'), ('0:13:13.259', '0:13:21.934', 'Unknown', 'Jack Nicholson'), ('0:13:28.274', '0:13:31.977', 'Unknown', 'Jack Nicholson'), ('0:13:38.217', '0:13:42.822', 'Unknown', 'Jack Nicholson'), ('0:13:57.103', '0:13:57.97', 'Unknown', 'Louise Fletcher'), ('0:18:10.89', '0:18:20.599', 'Unknown', 'William Redfield'), ('0:19:12.685', '0:19:14.119', 'Unknown', 'William Redfield'), ('0:19:27.033', '0:19:29.034', 'Unknown', 'William Redfield'), ('0:19:30.77', '0:19:34.373', 'Unknown', 'William Redfield'), ('0:19:48.854', '0:19:49.988', 'Unknown', 'William Redfield'), ('0:20:02.068', '0:20:12.845', 'Unknown', 'Vincent Schiavelli'), ('0:22:43.095', '0:22:45.03', 'Unknown', 'Will Sampson'), ('0:30:18.216', '0:30:18.817', 'Unknown', 'William Redfield'), ('0:30:48.58', '0:30:51.649', 'Unknown', 'William Redfield'), ('0:32:02.32', '0:32:04.456', 'Unknown', 'Jack Nicholson'), ('0:32:11.263', '0:32:13.498', 'Unknown', 'Jack Nicholson'), ('0:40:22.62', '0:40:31.095', 'Unknown', 'Louise Fletcher'), ('0:40:31.963', '0:40:34.765', 'Unknown', 'Louise Fletcher'), ('0:40:36.768', '0:40:44.108', 'Unknown', 'Louise Fletcher'), ('0:40:47.979', '0:41:15.306', 'Unknown', 'Louise Fletcher'), ('0:49:29.366', '0:49:32.169', 'Unknown', 'Jack Nicholson'), ('0:50:09.607', '0:50:13.81', 'Unknown', 'Jack Nicholson'), ('0:50:17.681', '0:50:19.149', 'Unknown', 'Jack Nicholson'), ('0:50:22.486', '0:50:25.656', 'Unknown', 'Jack Nicholson'), ('0:50:29.693', '0:50:31.595', 'Unknown', 'Jack Nicholson'), ('0:50:36.567', '0:50:42.105', 'Unknown', 'Jack Nicholson'), ('0:50:46.31', '0:50:48.579', 'Unknown', 'Jack Nicholson'), ('0:51:00.858', '0:51:02.826', 'Unknown', 'Jack Nicholson'), ('1:07:01.284', '1:07:01.617', 'Unknown', 'Jack Nicholson'), ('1:10:13.076', '1:10:16.145', 'Unknown', 'Jack Nicholson'), ('1:10:20.95', '1:10:27.289', 'Unknown', 'Jack Nicholson'), ('1:12:32.215', '1:12:35.284', 'Unknown', 'Jack Nicholson'), ('1:13:29.605', '1:13:31.607', 'Unknown', 'Louise Fletcher'), ('1:16:52.408', '1:16:56.979', 'Unknown', 'Louise Fletcher'), ('1:17:03.819', '1:17:04.72', 'Unknown', 'Louise Fletcher'), ('1:17:31.18', '1:17:31.213', 'Unknown', 'Jack Nicholson'), ('1:27:58.54', '1:27:59.741', 'Unknown', 'Jack Nicholson'), ('1:34:04.906', '1:34:06.007', 'Unknown', 'Jack Nicholson'), ('1:34:12.38', '1:34:16.05', 'Unknown', 'Jack Nicholson'), ('1:34:20.054', '1:34:22.223', 'Unknown', 'Jack Nicholson'), ('1:39:23.024', '1:39:25.292', 'Unknown', 'Scatman Crothers'), ('1:39:28.563', '1:39:29.563', 'Unknown', 'Scatman Crothers'), ('1:39:32.767', '1:39:36.003', 'Unknown', 'Scatman Crothers'), ('1:39:38.706', '1:39:41.475', 'Unknown', 'Scatman Crothers'), ('1:39:43.644', '1:39:45.646', 'Unknown', 'Scatman Crothers'), ('1:39:59.66', '1:40:03.831', 'Unknown', 'Scatman Crothers'), ('1:40:15.409', '1:40:16.877', 'Unknown', 'Scatman Crothers'), ('1:51:58.579', '1:52:00.78', 'Unknown', 'Louise Fletcher'), ('1:52:04.585', '1:52:05.852', 'Unknown', 'Louise Fletcher'), ('1:54:29.796', '1:54:30.363', 'Unknown', 'Louise Fletcher'), ('1:56:15.702', '1:56:21.641', 'Unknown', 'Louise Fletcher'), ('1:56:29.583', '1:56:35.288', 'Unknown', 'Louise Fletcher'), ('1:56:37.123', '1:56:38.858', 'Unknown', 'Louise Fletcher'), ('1:57:01.014', '1:57:18.865', 'Unknown', 'Louise Fletcher'), ('1:58:14.821', '1:58:18.458', 'Unknown', 'Louise Fletcher'), ('1:58:21.094', '1:58:27.3', 'Unknown', 'Louise Fletcher'), ('2:03:36.609', '2:03:37.81', 'Unknown', 'William Duell'), ('2:03:42.815', '2:03:44.65', 'Unknown', 'William Duell'), ('2:05:51.744', '2:05:57.55', 'Unknown', 'Will Sampson'), ('2:07:20.099', '2:07:30.376', 'Unknown', 'Will Sampson')]
# a_data = [list(i) for i in a_data]
#
# print(a_data)

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import pyqtSlot
import sys

# data = {'col1': ['1', '2', '3', '4'],
#         'col2': ['1', '2', '1', '3'],
#         'col3': ['1', '1', '2', '1']}


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
                self.setItem(n,m, newitem)

        #
        # for n, key in enumerate(sorted(self.data.keys())):
        #     horHeaders.append(key)
        #     for m, item in enumerate(self.data[key]):
        #         newitem = QTableWidgetItem(item)
        #         self.setItem(m, n, newitem)
        self.setHorizontalHeaderLabels(self.headers)


def main(args):
    app = QApplication(args)
    table = TableView(data, 4, 3)
    table.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)