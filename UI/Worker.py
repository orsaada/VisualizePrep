from PyQt5.QtCore import QObject, pyqtSignal
import time


class Worker(QObject):
    workRequested = pyqtSignal()
    finished = pyqtSignal()
    relay = pyqtSignal(int)
    # added
    the_work = None

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.x = 0

    def request_work(self):
        self.workRequested.emit()

    def add_tabs(self):
        self.x = 0
        for i in range(10):
            # Do any processing
            for i in range(10000):
                i*i
            time.sleep(1)
            self.x += 1
            self.relay.emit(self.x)
        self.finished.emit()
