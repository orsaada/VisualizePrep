# from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, \
#     QSlider, QStyle, QSizePolicy, QFileDialog
import datetime
import json
import os
import sys

from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette, QPixmap
from PyQt5 import QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from BussinesLayer.Services.VideoInsights import load_video, update_insights_in_db
from UI.PageWindow import PageWindow
from UI.dataAsTable import myWindow


def find_diffrence_temp():
    with open('/Users/orsaada/Documents/programming development/אוניברסיטה/פרויקט גמר/visualizePrep-master/BussinesLayer/Algorithms/Visualize/mg/py3loader/diff.json') as json_file:
        data = json.load(json_file)
        # for p in data['people']:
        #     print('Name: ' + p['name'])
        #     print('Website: ' + p['website'])
        #     print('From: ' + p['from'])
        #     print('')
        return data


class MyMainWindow(PageWindow):
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.form_widget = MediaWindow(self)
        self.setCentralWidget(self.form_widget)


class MediaWindow(QWidget):
    def __init__(self, value, parent=None):
        super().__init__()
        self.ind = 0
        self.setWindowTitle("VisualizeBGU")
        self.setGeometry(350, 100, 700, 500)
        self.setWindowIcon(QIcon('player.png'))

        p = self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.video_name = ''

        self.init_ui()

        # new window opening for qwidget
        self.newindow = Window1(self)

        # if want to check start app only from the mediaplayer cancell the comment
        self.show()

    def init_ui(self):

        # create media player object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # create videowidget object
        videowidget = QVideoWidget()

        # create open button
        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.open_file)

        # insights button
        # gotoInsights = QPushButton('Go to insights')
        # gotoInsights.clicked.connect(self.btn_clk)

        # self.lineEdit1 = QLineEdit("Type here what you want to transfer for [Window1].", self)

        # create button for playing
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        # create slider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # create label
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # position label
        duration = self.mediaPlayer.duration()
        seconds = (duration / 1000) % 60
        minutes = (duration / 60000) % 60
        hours = (duration / 3600000) % 24
        # print(duration)
        QTime(hours, minutes, seconds)
        self.positionLabel = QLabel('00:00:000')
        self.positionLabel.setStyleSheet("background-color: lightgreen")

        # logout button
        self.logoutButton = QPushButton(self)
        self.logoutButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.logoutButton.setText('Log out')
        self.logoutButton.clicked.connect(self.goMainWindow)

        # diff button
        # self.diffButton = QPushButton(self)
        # self.diffButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        # self.diffButton.setText('Diff!')
        # self.diffButton.clicked.connect(self.fi        # self.diffButton = QPushButton(self)
        #         # self.diffButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        #         # self.diffButton.setText('Diff!')
        #         # self.diffButton.clicked.connect(self.find_diffrence)nd_diffrence)

        # archive button
        self.archiveButton = QPushButton(self)
        self.archiveButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.archiveButton.setText('My Archive')
        self.archiveButton.clicked.connect(self.goMyArchive)

        # goback button
        self.goBackButton = QPushButton(self)
        self.goBackButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.goBackButton.setText('GO BACK')
        self.goBackButton.clicked.connect(self.goMediaWindow)

        # volume
        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setFocusPolicy(Qt.NoFocus)
        # self.sld.setGeometry(30, 40, 100, 30)
        self.sld.valueChanged[int].connect(self.changeValue)

        self.sldlabel = QLabel(self)
        self.sldlabel.setPixmap(QPixmap('mid.png'))
        # self.sldlabel.setGeometry(160, 40, 80, 30)

        # create hbox layout
        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(0, 0, 0, 0)

        #set widgets to the hbox layout
        hboxLayout.addWidget(openBtn)
        hboxLayout.addWidget(self.playBtn)
        hboxLayout.addWidget(self.slider)
        # hboxLayout.addWidget(gotoInsights)
        hboxLayout.addWidget(self.positionLabel)
        hboxLayout.addWidget(self.logoutButton)
        # hboxLayout.addWidget(self.diffButton)
        hboxLayout.addWidget(self.archiveButton)
        hboxLayout.addWidget(self.goBackButton)
        hboxLayout.addWidget(self.sld)
        # hboxLayout.addWidget(self.sldlabel)

        #create vbox layout
        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(videowidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(self.label)


        self.setLayout(vboxLayout)

        self.mediaPlayer.setVideoOutput(videowidget)


        #media player signals

        self.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.mediaPlayer.positionChanged.connect(self.position_changed)
        self.mediaPlayer.durationChanged.connect(self.duration_changed)

    # @pyqtSlot()
    # def buttonWindow1_onClick(self):
    #     # self.statusBar().showMessage("Switched to window 1")
    #     # self.cams = Window1(self.lineEdit1.text())
    #     self.cams.show()
    #     self.close()

    def goMainWindow(self):
        with open('./../config.json', 'r') as f:
            data = json.load(f)
            data['UserLoggedIn'] = ""
        print(data['UserLoggedIn'])
        os.remove('./../config.json')
        with open('./../config.json', 'w') as f:
            json.dump(data, f, indent=4)
        self.parent().goto('main')

    def goMyArchive(self):
        self.parent().goto('archive')

    def goMediaWindow(self):
        self.parent().goto('media')

    def logout(self):
        self.mediaPlayer.stop()
        self.parent().goto('main')

    def find_diffrence(self):
        data = find_diffrence_temp()
        self.mediaPlayer.setPosition(data[self.ind][0]*1000)
        self.ind += 1
        # print(str(data[self.ind][0]) + '   ' + str(data[self.ind][1]))

    def setInterval(self, path, start, end):
        """
            path: path of video
            start: time in ms from where the playback starts
            end: time in ms where playback ends
        """
        self.mediaPlayer.stop()
        self.mediaPlayer.setMedia(QMediaContent(QtCore.QUrl.fromLocalFile(self.video_name)))
        self.mediaPlayer.setPosition(start)
        # self._end = end
        self.mediaPlayer.play()

    def changeValue(self, value):
        self.mediaPlayer.setVolume(value)
        if value == 0:
            self.label.setPixmap(QPixmap('mute.png'))
        elif value > 0 and value <=30:
            self.label.setPixmap(QPixmap('min.png'))
        elif value >30 and value <= 80:
            self.label.setPixmap(QPixmap('mid.png'))
        else:
            self.label.setPixmap(QPixmap('max.png'))

    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Video")
        if filename != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.playBtn.setEnabled(True)
            self.video_name = filename
            with open('./../config.json') as f:
                data = json.load(f)
            if data["ENV_MODE"] == 'production':
                username = data["UserLoggedIn"]
                name = os.path.splitext(os.path.basename(filename))[0]
                vid_id = load_video(filename, name)
                update_insights_in_db(username, name, vid_id)
            elif data["ENV_MODE"] == 'development':
                i = 0  # to delete jsut to example

    def play_video(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()

        else:
            self.mediaPlayer.play()
            self.sld.setSliderPosition(50)
            self.mediaPlayer.setVolume(50)

    def mediastate_changed(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause)

            )

        else:
            self.playBtn.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay)

            )

    def position_changed(self, position):
        self.slider.setValue(position)
        # seconds = (duration / 1000) % 60
        # minutes = (duration / 60000) % 60
        import pandas as pd
        print(pd.to_datetime(position, unit='ms').to_pydatetime())
        # time = pd.to_datetime(position, unit='ms').to_pydatetime().seconds
        # print(time)
        # print(datetime.datetime.fromtimestamp(position/1000.0))
        hours = (position / 3600000) % 24
        # print(hours)



    def duration_changed(self, duration):
        self.slider.setRange(0, duration)
        # print(duration)


    def set_position(self, position):
        self.mediaPlayer.setPosition(position)


    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())


class Window1(QDialog):
    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.resize(800, 600)
        self.setWindowTitle('Window1')
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView))

        label1 = QLabel(value)
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

        #filter as table button
        self.filter_table_window = myWindow()
        self.filter_table_button = QPushButton("Filter as table")
        self.filter_table_button.clicked.connect(self.filterAsTableButton)


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
        layoutH.addWidget(label1)
        # layoutH.addWidget(self.button)
        layoutH.addWidget(combo)
        layoutH.addWidget(self.filter_table_button)
        #layoutH.addWidget(chartClass.chartView)
        layoutV.addLayout(layoutH)
        self.setLayout(layoutV)

    def goMainWindow(self):
        self.goto("main")
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
        self.btn_switch

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

    # @QtCore.pyqtSlot('qint64')
    # def on_positionChanged(self, position):
    #     if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
    #         if position > self._end:
    #             self.mediaPlayer.stop()

    # def btn_clk(self):
    #     self.mediaPlayer.stop()
    #     self.parent().goto('insights')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MediaWindow(1)
    sys.exit(app.exec_())
