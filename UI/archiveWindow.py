import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QApplication, QScrollArea

from DB.db_api import get_movieId
from UI.PageWindow import PageWindow
from BussinesLayer.Services.VideoInsights import get_my_uploaded_videos, get_insights
import json
import os


# Archive Page
class MyArchive(PageWindow):
    def __init__(self):
        super().__init__()
        self.form_widget = MyArchiveWidget()
        self.setCentralWidget(self.form_widget)


class MyArchiveWidget(QWidget):
    def gotoBack(self):
        self.parent().goto("media")

    def pop_message(self, text):
        msg = QWidget.QMessageBox()
        msg.setText("{}".format(text))
        msg.exec_()

    def gotoMovie(self, video_name):
        with open('./../config.json', 'r') as f:
            data = json.load(f)
            data['SpecificMoviePage'] = video_name
            data['ttMovie'] = get_movieId(data['UserLoggedIn'], video_name)[0][0]
            json_insights_need_check = get_insights(data['ttMovie'])
            if json_insights_need_check['state'] == 'Processing':
                # need to alert ('Until Processing, please wait!')
                self.parent().goto("archive")
            elif json_insights_need_check['state'] == 'Processed':
                ROOT_DIR = os.path.abspath(os.curdir)
                ttmovie_number = data['ttMovie']
                path = os.path.join(ROOT_DIR+'/../BussinesLayer/Algorithms/Visualize/vi_json/', f'{ttmovie_number}.json')
                with open(path, 'w') as f:
                    json.dump(json_insights_need_check, f)
                self.parent().goto("movie")
        os.remove('./../config.json')
        with open('./../config.json', 'w') as f:
            json.dump(data, f, indent=4)


    def __init__(self):
        super().__init__()
        dlgLayout = QVBoxLayout()
        # Create a form layout and add widgets
        formLayout = QFormLayout()
        with open('./../config.json', 'r') as f:
            data = json.load(f)
        name = data["UserLoggedIn"]
        title = "Archive Info Movies Of: " + name
        qlabel_title = QLabel()
        qlabel_title.setText(title)
        # formLayout.addRow(title, QLabel())
        my_videos = get_my_uploaded_videos(name)
        buttons = []
        # for video in my_videos:
        #     self.btnBox = QPushButton()
        #     self.btnBox.setText(video[0])
        #     self.btnBox.clicked.connect(lambda state, x=video[0]: self.gotoMovie(x))
        #     buttons.append(self.btnBox)

        self.btnBackBox = QPushButton()
        self.btnBackBox.setText('Back')
        self.btnBackBox.clicked.connect(self.gotoBack)
        self.btnBackBox.setStyleSheet("background-color: red;")

        # Scrolling
        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        for video in my_videos:
            self.btnBox = QPushButton()
            self.btnBox.setText(video[0])
            self.btnBox.clicked.connect(lambda state, x=video[0]: self.gotoMovie(x))
            self.vbox.addWidget(self.btnBox)

        self.widget.setLayout(self.vbox)
        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        # self.setCentralWidget(self.scroll)


        # Set the layout on the dialog

        dlgLayout.addLayout(formLayout)
        # for btn in buttons:
        #     dlgLayout.addWidget(btn)
        dlgLayout.addWidget(qlabel_title)
        dlgLayout.addWidget(self.scroll)
        dlgLayout.addWidget(self.btnBackBox)


        self.setLayout(dlgLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyArchive()
    w.show()
    sys.exit(app.exec_())
