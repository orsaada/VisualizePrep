import datetime
import os
import sys

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QApplication

from BussinesLayer.Services.ExportInsights import export_json_of_video_to_file
from BussinesLayer.Services.VideoInsights import get_insights
from DB.db_api import get_movieId
from UI.Graphs.comparisonGraph import ComparisonGraph
from UI.PageWindow import PageWindow
import json


# Movie Page
class MyMovie(PageWindow):
    def __init__(self):
        super().__init__()
        self.form_widget = MyMovieWidget()
        self.resize(500, 500)
        self.setCentralWidget(self.form_widget)


class MyMovieWidget(QWidget):
    def gotoBack(self):
        self.parent().goto("archive")

    def __init__(self):
        super().__init__()
        dlgLayout = QVBoxLayout()

        # Create a form layout and add widgets
        formLayout = QFormLayout()
        with open('./../config.json', 'r') as f:
            data = json.load(f)
        name = data["SpecificMoviePage"]
        username = data['UserLoggedIn']

        formLayout.addRow(name + " Page - Menu", QLabel())
        dlgLayout.addLayout(formLayout)

        self.insights = QPushButton()
        self.insights.setText('insights graphs')
        self.insights.clicked.connect(self.gotToInsights)

        self.btn_algo1 = QPushButton()
        self.btn_algo1.setText('face recognition improvement algo 1')

        self.btn_algo2 = QPushButton()
        self.btn_algo2.setText('face recognition improvement algo 2')

        self.btn_algo3 = QPushButton()
        self.btn_algo3.setText('face recognition improvement algo 3')

        self.btn_algo5 = QPushButton()
        self.btn_algo5.setText('transcript comparison')

        if data['ttMovie'].startswith('tt'):
            algo_buttons_list = list(map(lambda x: QPushButton, range(4)))
            self.btn_algo4 = QPushButton()
            self.btn_algo4.setText('face recognition improvement algo 4')

            self.btn_algo1.clicked.connect(lambda: self.compareGraph('algo 1'))
            self.btn_algo2.clicked.connect(lambda: self.compareGraph('algo 2'))
            self.btn_algo3.clicked.connect(lambda: self.compareGraph('algo 3'))
            self.btn_algo4.clicked.connect(lambda: self.compareGraph('algo 4'))
            self.btn_algo5.clicked.connect(lambda: self.compareGraph('transcript'))
        else:
            self.btn_algo1.clicked.connect(lambda: self.algo_improve_algo('algo 1'))
            self.btn_algo2.clicked.connect(lambda: self.algo_improve_algo('algo 2'))
            self.btn_algo3.clicked.connect(lambda: self.algo_improve_algo('algo 3'))
            # self.btn_algo4.clicked.connect(lambda: self.algo_improve_algo('algo 4'))
            # self.btn_algo5.clicked.connect(lambda: self.algo_improve_algo('transcript'))

        # self.comparisonGraph = QPushButton()
        # self.comparisonGraph.setText('comparison Graph')
        # self.comparisonGraph.clicked.connect(self.compareGraph)

        self.exportButton = QPushButton()
        self.exportButton.setText('export data to JSON file')
        self.exportButton.clicked.connect(self.exportFunction)

        self.emotionAnalysisButton = QPushButton()
        self.emotionAnalysisButton.setText('action recognition external analysis')
        self.emotionAnalysisButton.clicked.connect(self.goToActionRecognition)

        dlgLayout.addWidget(self.insights)
        dlgLayout.addWidget(self.btn_algo1)
        dlgLayout.addWidget(self.btn_algo2)
        dlgLayout.addWidget(self.btn_algo3)
        if data['ttMovie'].startswith('tt'):
            dlgLayout.addWidget(self.btn_algo4)
            dlgLayout.addWidget(self.btn_algo5)
        dlgLayout.addWidget(self.emotionAnalysisButton)
        dlgLayout.addWidget(self.exportButton)

        # dlgLayout.addWidget(self.comparisonGraph)

        self.btnBackBox = QPushButton()
        self.btnBackBox.setText('Back')
        self.btnBackBox.setStyleSheet("background-color: red;")
        self.btnBackBox.clicked.connect(self.gotoBack)
        dlgLayout.addWidget(self.btnBackBox)
        self.setLayout(dlgLayout)

    def compareGraph(self, algo_name):
        with open('./../config.json', 'r') as f:
            data = json.load(f)
            data["algo"] = algo_name
        os.remove('./../config.json')
        with open('./../config.json', 'w') as f:
            json.dump(data, f, indent=4)
        self.parent().goto("comparison")

    def algo_improve_algo(self, algo_name):
        with open('./../config.json', 'r') as f:
            data = json.load(f)
            data["algo"] = algo_name
        os.remove('./../config.json')
        with open('./../config.json', 'w') as f:
            json.dump(data, f, indent=4)
        self.parent().goto("algoImprove")

    def gotToInsights(self):
        self.parent().goto("insights")

    def goToActionRecognition(self):
        self.parent().goto("actionRecognition")

    def exportFunction(self):
        with open('./../config.json', 'r') as f:
            data = json.load(f)
        export_json_of_video_to_file(data['ttMovie'], data['SpecificMoviePage'])

    # def generate_emotion_analysis(self):
    #     with open('./../config.json', 'r') as f:
    #         data = json.load(f)
    #     video_name = data["SpecificMoviePage"]
    #     print(video_name)
    #     ### temp - need change
    #     with open("./../BussinesLayer/Algorithms/Visualize/vi_json/tt0037884.json", 'r') as f:
    #         data = json.load(f)
    #         scenes = []
    #         for i in data['videos'][0]['insights']['scenes']:
    #             scene = i['instances'][0]
    #             t = try_parsing_date(scene['start'])
    #             delta1 = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second,microseconds=t.microsecond)
    #             t = try_parsing_date(scene['end'])
    #             delta2 = datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second,microseconds=t.microsecond)
    #             scenes.append((delta1, delta2))


def try_parsing_date(text):
    print(text)
    for fmt in ('%H:%M:%S', '%H:%M:%S.%f'):
        try:
            return datetime.datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyMovie()
    window.show()

    sys.exit(app.exec_())
