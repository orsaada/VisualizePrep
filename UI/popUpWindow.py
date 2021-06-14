import PyQt5
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QMessageBox


class MyPopup(QWidget):
    def __init__(self, parent, popup_text):
        # super(MyPopup, self).__init__(parent)
        super(MyPopup, self).__init__()

        frameGm = self.frameGeometry()
        screen = PyQt5.QtWidgets.QApplication.desktop().screenNumber(
            PyQt5.QtWidgets.QApplication.desktop().cursor().pos())
        centerPoint = PyQt5.QtWidgets.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())
        QWidget.__init__(self)

    def popup_message(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setText("This is a message box")
        msg.setInformativeText("This is additional information")
        msg.setWindowTitle("MessageBox demo")
        msg.setDetailedText("The details are as follows:")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.msgbtn)

        retval = msg.exec_()

    def msgbtn(i):
        print
        "Button pressed is:", i.text()


if __name__ == '__main__':
    w = MyPopup(QWidget(),'tt')
    # w.show()
    w.popup_message()
