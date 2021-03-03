import sys
import json

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDialog, QStyle, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QComboBox, QHBoxLayout, \
    QWidget, QStackedLayout, QApplication, QTableView
from BussinesLayer.Services.VideoInsights import get_movie_id
from UI.Graphs.MplCanvas.pandasWindow import pandasModel
from UI.Graphs.allGraph import allGraphC
from UI.Graphs.shotsGraph import shotsGraph
from UI.Graphs.emotionsGraph import ChartEmotions
from UI.Graphs.keyWordsGraph import KeywordGraph
from UI.Graphs.namedPeopleGraph import NamedPeopleGraph
from UI.Graphs.speakersGraph import SpeakersGraph
from UI.PageWindow import PageWindow


class MyInsightsWindow(PageWindow):
    def __init__(self):
        super().__init__()
        with open('./../config.json', 'r') as f:
            data = json.load(f)
        video_name = data["SpecificMoviePage"]
        if video_name != '':
            self.form_widget = MyInsightsWidget()
            self.setWindowTitle("MyInsightsWindow")
            self.setCentralWidget(self.form_widget)
        # self.form_widget.update()


class MyInsightsWidget(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle('Window1')
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))

        with open('./../config.json', 'r') as f:
            data = json.load(f)
        video_name = data["SpecificMoviePage"]
        username = data["UserLoggedIn"]
        video_id = get_movie_id(username, video_name)
        # label1 = QLabel(value)
        self.button = QPushButton()
        self.button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.button.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        self.button.setIconSize(QSize(200, 200))

        layoutV = QVBoxLayout()

        # close button
        # self.pushButton = QPushButton(self)
        # self.pushButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        # self.pushButton.setText('Back To Media Window')
        # self.pushButton.clicked.connect(self.goMainWindow)
        # layoutV.addWidget(self.pushButton)

        # close button
        self.archiveButton = QPushButton(self)
        self.archiveButton.setStyleSheet('background-color: red;')
        self.archiveButton.setText('Back To Movie')
        self.archiveButton.clicked.connect(self.goToMovie)
        # layoutV.addWidget(self.archiveButton)

        movie_name_label = QLabel()
        movie_name_label.setText(video_name)
        layoutV.addWidget(movie_name_label)
        # export json
        # self.exportButton = QPushButton(self)
        # self.exportButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        # self.exportButton.setText('export')
        # self.exportButton.clicked.connect(self.exportJson)
        # layoutV.addWidget(self.exportButton)

        # show improvment
        # self.comparisonButton = QPushButton(self)
        # self.comparisonButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        # self.comparisonButton.setText('comparison improvement')
        # self.comparisonButton.clicked.connect(self.compareImprovments)
        # layoutV.addWidget(self.comparisonButton)

        # filter as table button
        # self.filter_table_window = myWindow()
        # self.filter_table_button = QPushButton("Filter as table")
        # self.filter_table_button.clicked.connect(self.filterAsTable)

        # show graph
        # self.showGraphButton = QPushButton("Show Graph")
        # self.showGraphButton.clicked.connect(self.showGraph)

        # graphs
        all_graph_attributes = ['faces', 'labels', 'brands', 'namedLocations', 'topics', 'sentiments']
        self.child = SpeakersGraph()
        self.graphs = {"Speakers": SpeakersGraph,
                       "Emotions": ChartEmotions,
                       "Faces": NamedPeopleGraph,
                       "Keywords": KeywordGraph,
                       "Shots": shotsGraph}
        self.graphs = {k: v() for k, v in self.graphs.items()}
        for i in all_graph_attributes:
            self.graphs[i] = allGraphC(i)

        self.showingGraphName = list(self.graphs.keys())[0]

        # dropdown choosing
        combo = QComboBox(self)
        for k in self.graphs.keys():
            combo.addItem(k)
        combo.move(50, 50)
        # not neccesrily need
        self.qlabel = QLabel(self)
        self.qlabel.move(50, 16)

        combo.activated[str].connect(self.onChanged)

        # button switch
        self.button_switch()

        # layout and
        self.layoutH = QHBoxLayout()
        self.layoutH.addWidget(combo)
        # self.layoutH.addWidget(self.filter_table_button)
        # self.layoutH.addWidget(self.showGraphButton)
        self.layoutH.addWidget(self.child)
        layoutV.addLayout(self.layoutH)
        layoutV.addWidget(self.archiveButton)
        self.setLayout(layoutV)

    def goMainWindow(self):
        self.parent().goto("media")
        # self.close()

    def onChanged(self, text):
        self.showingGraphName = text
        self.layoutH.removeWidget(self.child)
        self.child.setParent(None)
        print(type(self.graphs[text]))
        # self.child = self.graphs[text]()
        self.child = self.graphs[text]
        self.layoutH.addWidget(self.child)

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

    # def filterAsTable(self):
    #     self.filter_table_window.show()
    #
    # def exportJson(self):
    #     pass
    #
    # def compareImprovments(self):
    #     pass

    def showGraph(self):
        df = self.graphs[self.showingGraphName].get_df()
        model = pandasModel(df)
        view = QTableView()
        view.setModel(model)
        view.resize(800, 600)
        view.show()

    def goToArchive(self):
        self.parent().goto('archive')

    def goToMovie(self):
        self.parent().goto('movie')

    # replace widget
    def update(self):
        # self.layout().removeWidget(self.child)
        # self.child.setParent(None)
        # self.child = QLabel("bar", self)
        # self.layout().addWidget(self.child)
        self.layoutH.removeWidget(self.child)
        self.child.setParent(None)
        self.child = QLabel("bar", self)
        self.layoutH.addWidget(self.child)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyInsightsWindow()
    window.show()

    sys.exit(app.exec_())
