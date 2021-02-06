import sys

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDialog, QStyle, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QComboBox, QHBoxLayout, \
    QWidget, QStackedLayout, QApplication

from UI.Graphs.ChartEmotion import ChartEmotions
from UI.PageWindow import PageWindow
from UI.dataAsTable import myWindow


class MyInsightsWindow(PageWindow):
    def __init__(self):
        super().__init__()
        self.form_widget = MyInsightsWidget()
        self.setWindowTitle("MyInsightsWindow")
        self.setCentralWidget(self.form_widget)

class MyInsightsWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle('Window1')
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))

        # label1 = QLabel(value)
        self.button = QPushButton()
        self.button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.button.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        self.button.setIconSize(QSize(200, 200))

        layoutV = QVBoxLayout()

        # close button
        self.pushButton = QPushButton(self)
        self.pushButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.pushButton.setText('Click me! (close page)')
        self.pushButton.clicked.connect(self.goMainWindow)
        layoutV.addWidget(self.pushButton)

        # close button
        self.archiveButton = QPushButton(self)
        self.archiveButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.archiveButton.setText('Go To Archive')
        self.archiveButton.clicked.connect(self.goToArchive)
        layoutV.addWidget(self.archiveButton)

        # export json
        self.exportButton = QPushButton(self)
        self.exportButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.exportButton.setText('export')
        self.exportButton.clicked.connect(self.exportJson)
        layoutV.addWidget(self.exportButton)

        # show improvment
        self.comparisonButton = QPushButton(self)
        self.comparisonButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.comparisonButton.setText('comparison improvement')
        self.comparisonButton.clicked.connect(self.compareImprovments)
        layoutV.addWidget(self.comparisonButton)


        #filter as table button
        self.filter_table_window = myWindow()
        self.filter_table_button = QPushButton("Filter as table")
        self.filter_table_button.clicked.connect(self.filterAsTableButton)

        #show graph
        self.showGraphButton = QPushButton("Show Graph")
        self.showGraphButton.clicked.connect(self.showGraph)

        #dropdown choosing
        combo = QComboBox(self)
        combo.addItem("Emotions")
        combo.addItem("Faces")
        combo.addItem("Sentiments")
        combo.move(50, 50)

        #call chart
        #chartClass = ChartEmotions()


        #not neccesrily need
        self.qlabel = QLabel(self)
        self.qlabel.move(50, 16)

        combo.activated[str].connect(self.onChanged)


        #button switch
        self.button_switch()

        # layout and
        layoutH = QHBoxLayout()
        # layoutH.addWidget(label1)
        # layoutH.addWidget(self.button)
        layoutH.addWidget(combo)
        layoutH.addWidget(self.filter_table_button)
        layoutH.addWidget(self.showGraphButton)
        widget = ChartEmotions()

        layoutH.addWidget(widget)
        #layoutH.addWidget(chartClass.chartView)
        layoutV.addLayout(layoutH)
        self.setLayout(layoutV)

    def goMainWindow(self):
        self.parent().goto("media")
        # self.close()

    def onChanged(self, text):
        self.qlabel.setText(text)
        self.qlabel.adjustSize()

    def switch_wids(self):

        # LOGIC TO SWITCH
        if self.front_wid == 1:
            self.wid1.hide()
            self.wid2.show()
            self.front_wid = 2
        else:
            self.wid1.show()
            self.wid2.hide()
            self.front_wid = 1

    def button_switch(self):
        # CENTRAL WIDGET
        self.central_wid = QWidget()
        self.layout_for_wids = QStackedLayout()

        # BUTTON TO SWITCH BETWEEN WIDGETS
        self.btn_switch = QPushButton("Switch")
        self.btn_switch.clicked.connect(self.switch_wids)
        self.btn_switch.setFixedSize(50, 50)
        # self.btn_switch

        # 2 WIDGETS
        self.wid1 = QWidget()
        self.wid1.setStyleSheet("""background: blue;""")
        self.wid1.setFixedSize(200, 200)
        self.wid1.move(100, 100)
        self.wid2 = QWidget()
        self.wid2.setStyleSheet("""background: green;""")
        self.wid2.setFixedSize(200, 200)
        self.wid2.move(100, 100)

        # LAYOUT CONTAINER FOR WIDGETS AND BUTTON
        self.layout_for_wids.addWidget(self.btn_switch)
        self.layout_for_wids.addWidget(self.wid1)
        self.layout_for_wids.addWidget(self.wid2)

        # ENTERING LAYOUT
        self.central_wid.setLayout(self.layout_for_wids)

        # CHOOSE YOUR CENTRAL WIDGET
        # self.setCentralWidget(self.central_wid)

        # WHICH WIDGET IS ON THE FRONT
        self.front_wid = 1

    def filterAsTableButton(self):
        self.filter_table_window.show()

    def exportJson(self):
        pass

    def compareImprovments(self):
        pass

    def showGraph(self):
        pass

    def goToArchive(self):
        self.parent().goto('archive')

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyInsightsWindow()
    window.show()

    sys.exit(app.exec_())