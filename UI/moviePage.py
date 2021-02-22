import sys

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QApplication

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
        formLayout.addRow(name + " Page - Menu", QLabel())
        dlgLayout.addLayout(formLayout)

        self.btnEmotions = QPushButton()
        self.btnEmotions.setText('show Emotions')
        self.btnCharacters = QPushButton()
        self.btnCharacters.setText('show Characters')
        self.btnKeywords = QPushButton()
        self.btnKeywords.setText('show Keywords')
        self.insights = QPushButton()
        self.insights.setText('insights graphs')
        self.insights.clicked.connect(self.gotToInsights)
        self.comparisonGraph = QPushButton()
        self.comparisonGraph.setText('comparison Graph')
        self.comparisonGraph.clicked.connect(self.compareGraph)


        dlgLayout.addWidget(self.btnEmotions)
        dlgLayout.addWidget(self.btnCharacters)
        dlgLayout.addWidget(self.btnKeywords)
        dlgLayout.addWidget(self.insights)
        dlgLayout.addWidget(self.comparisonGraph)

        self.btnBackBox = QPushButton()
        self.btnBackBox.setText('Back')
        self.btnBackBox.clicked.connect(self.gotoBack)
        dlgLayout.addWidget(self.btnBackBox)
        self.setLayout(dlgLayout)

    def compareGraph(self):
        self.parent().goto("comparison")
        print(1)

    def gotToInsights(self):
        self.parent().goto("insights")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MyMovie()
    window.show()

    sys.exit(app.exec_())