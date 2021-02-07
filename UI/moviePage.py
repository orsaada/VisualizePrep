from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton
from UI.PageWindow import PageWindow
import json


# Movie Page
class MyMovie(PageWindow):
    def __init__(self):
        super().__init__()
        self.form_widget = MyMovieWidget()
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
        dlgLayout.addWidget(self.btnEmotions)
        dlgLayout.addWidget(self.btnCharacters)
        dlgLayout.addWidget(self.btnKeywords)

        self.btnBackBox = QPushButton()
        self.btnBackBox.setText('Back')
        self.btnBackBox.clicked.connect(self.gotoBack)
        dlgLayout.addWidget(self.btnBackBox)
        self.setLayout(dlgLayout)

