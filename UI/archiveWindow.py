import sys

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLabel, QLineEdit, QPushButton, QApplication

from DB.DB import get_movieId
from UI.PageWindow import PageWindow
from BussinesLayer.Services.VideoInsights import get_my_uploaded_videos
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

    def gotoMovie(self, video_name):
        with open('./../config.json', 'r') as f:
            data = json.load(f)
            print(get_movieId(data['UserLoggedIn'], video_name))
            data['SpecificMoviePage'] = video_name
            data['ttMovie'] = get_movieId(data['UserLoggedIn'], video_name)[0][0]
        os.remove('./../config.json')
        with open('./../config.json', 'w') as f:
            json.dump(data, f, indent=4)
        # changed
        # self.parent().goto("insights")
        self.parent().goto("movie")

    def __init__(self):
        super().__init__()
        dlgLayout = QVBoxLayout()
        # Create a form layout and add widgets
        formLayout = QFormLayout()
        with open('./../config.json', 'r') as f:
            data = json.load(f)
        name = data["UserLoggedIn"]
        title = "Archive Info Movies Of: " + name
        formLayout.addRow(title, QLabel())
        my_videos = get_my_uploaded_videos(name)
        buttons = []
        for video in my_videos:
            self.btnBox = QPushButton()
            self.btnBox.setText(video[0])
            self.btnBox.clicked.connect(lambda state, x=video[0]: self.gotoMovie(x))
            buttons.append(self.btnBox)

        self.btnBackBox = QPushButton()
        self.btnBackBox.setText('Back')
        self.btnBackBox.clicked.connect(self.gotoBack)
        # Set the layout on the dialog
        dlgLayout.addLayout(formLayout)
        for btn in buttons:
            dlgLayout.addWidget(btn)
        dlgLayout.addWidget(self.btnBackBox)
        self.setLayout(dlgLayout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyArchive()
    w.show()
    sys.exit(app.exec_())
