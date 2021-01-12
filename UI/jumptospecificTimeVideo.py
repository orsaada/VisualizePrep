import json
import os
import time

from PyQt5 import QtCore, QtWidgets, QtMultimedia, QtMultimediaWidgets


def find_diffrence_temp():
    with open('/Users/orsaada/Documents/programming development/אוניברסיטה/פרויקט גמר/visualizePrep-master/BussinesLayer/Algorithms/Visualize/mg/py3loader/diff.json') as json_file:
        data = json.load(json_file)
        # for p in data['people']:
        #     print('Name: ' + p['name'])
        #     print('Website: ' + p['website'])
        #     print('From: ' + p['from'])
        #     print('')
        return data


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        video_widget = QtMultimediaWidgets.QVideoWidget()
        self.setCentralWidget(video_widget)
        self.player = QtMultimedia.QMediaPlayer(self, QtMultimedia.QMediaPlayer.VideoSurface)
        self.player.setVideoOutput(video_widget)
        # period of time that the change of position is notified
        self.player.setNotifyInterval(1)
        self.player.positionChanged.connect(self.on_positionChanged)


    def setInterval(self, path, start, end):
        """
            path: path of video
            start: time in ms from where the playback starts
            end: time in ms where playback ends
        """
        self.player.stop()
        self.player.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(path)))
        self.player.setPosition(start)
        self._end = end
        self.player.play()

    @QtCore.pyqtSlot('qint64')
    def on_positionChanged(self, position):
        if self.player.state() == QtMultimedia.QMediaPlayer.PlayingState:
            if position > self._end:
                self.player.stop()


if __name__ == '__main__':
    import sys
    data = find_diffrence_temp()
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    file = os.path.join(os.path.dirname(__file__), "/Users/orsaada/Documents/programming development/אוניברסיטה/פרויקט גמר/UI/videoplayer-master/video_analysis/test.mp4")
    ind = 0
    while():
        w.setInterval(file, data[ind][0]*1000, data[ind][1]*1000)
        ind +=1
        w.show()
        time.sleep(4)
        # if ind > len(data):
        #     break
    # w.setInterval(file, 30*1000, 33*1000)

    sys.exit(app.exec_())
