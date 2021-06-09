import PyQt5
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget


class MyPopup(QWidget):
    def __init__(self, parent, popup_text):
        super(MyPopup, self).__init__(parent)
        frameGm = self.frameGeometry()
        screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(
            PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        QWidget.__init__(self)

    # def paintEvent(self, e):
    #     dc = QPainter(self)
    #     dc.drawLine(0, 0, 100, 100)
    #     dc.drawLine(100, 0, 0, 100)


if __name__ == '__main__':
    w = MyPopup()
    w.show()
