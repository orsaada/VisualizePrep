import os
import sys
import json

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QDialog, QStyle, QLabel, QPushButton, QSizePolicy, QVBoxLayout, QComboBox, QHBoxLayout, \
    QWidget, QStackedLayout, QApplication, QTableView

from BussinesLayer.Data.data import check_attributes_exists
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
        # video_id = get_movie_id(username, video_name)
        self.button = QPushButton()
        self.button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.button.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        self.button.setIconSize(QSize(200, 200))

        layoutV = QVBoxLayout()

        # close button
        self.archiveButton = QPushButton(self)
        self.archiveButton.setStyleSheet('background-color: red;')
        self.archiveButton.setText('Back To Movie')
        self.archiveButton.clicked.connect(self.goToMovie)

        movie_name_label = QLabel()
        movie_name_label.setText(f'Video Name: {video_name}')
        layoutV.addWidget(movie_name_label)

        # graphs
        all_graph_attributes = ['faces', 'labels', 'brands', 'namedLocations', 'topics', 'sentiments']
        ROOT_DIR = os.path.abspath(os.curdir)
        ttmovie_number = data['ttMovie']
        path = os.path.join(ROOT_DIR + '/../BussinesLayer/Algorithms/Visualize/vi_json/', f'{ttmovie_number}.json')
        attributes_in_json = check_attributes_exists(path)
        print(f'attributes_in_json: {attributes_in_json}')
        all_graph_attributes = [x for x in all_graph_attributes if x in attributes_in_json]
        print(all_graph_attributes)
        self.child = SpeakersGraph()
        self.graphs = {"speakers": SpeakersGraph,
                       "emotions": ChartEmotions,
                       "namedPeople": NamedPeopleGraph,
                       "keywords": KeywordGraph,
                       "shots": shotsGraph}
        for i in list(self.graphs.keys()):
            if i not in attributes_in_json:
                del self.graphs[i]
        self.graphs = {k: v() for k, v in self.graphs.items()}
        print(self.graphs)
        for i in all_graph_attributes:
            self.graphs[i] = allGraphC(i)

        print(f'this is graphs: {self.graphs}')
        self.showingGraphName = list(self.graphs.keys())[0]

        # dropdown choosing
        combo = QComboBox(self)
        for k in self.graphs.keys():
            combo.addItem(k)
        combo.move(50, 50)
        # not necessarily need
        self.qlabel = QLabel(self)
        self.qlabel.move(50, 16)

        combo.activated[str].connect(self.onChanged)

        # button switch
        self.button_switch()

        # layout and
        self.layoutH = QHBoxLayout()
        self.layoutH.addWidget(combo)
        self.layoutH.addWidget(self.child)
        layoutV.addLayout(self.layoutH)
        layoutV.addWidget(self.archiveButton)
        self.setLayout(layoutV)

    def goMainWindow(self):
        self.parent().goto("media")

    def onChanged(self, text):
        self.showingGraphName = text
        self.layoutH.removeWidget(self.child)
        self.child.setParent(None)
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
        self.layoutH.removeWidget(self.child)
        self.child.setParent(None)
        self.child = QLabel("bar", self)
        self.layoutH.addWidget(self.child)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyInsightsWindow()
    window.show()

    sys.exit(app.exec_())
