import sys
from random import randint

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication

from UI.Graphs.keyWordsGraph import MplCanvas


class MovingWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MovingWindow, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.canvas)

        n_data = 50
        self.xdata = list(range(n_data))
        # self.ydata = [randint(0, 10) for i in range(n_data)]
        self.ydata = [0 for i in range(n_data)]

        # We need to store a reference to the plotted line
        # somewhere, so we can apply the new data to it.
        self._plot_ref = None
        self.update_plot()

        self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        # Drop off the first y element, append a new one.
        # self.ydata = self.ydata[1:] + [randint(0, 10)]
        self.ydata = self.ydata[1:] + [self.get_face_confidence(1)]

        # Note: we no longer need to clear the axis.
        if self._plot_ref is None:
            # First time we have no plot reference, so do a normal plot.
            # .plot returns a list of line <reference>s, as we're
            # only getting one we can take the first element.
            plot_refs = self.canvas.axes.plot(self.xdata, self.ydata, 'r')
            self._plot_ref = plot_refs[0]
        else:
            # We have a reference, we can use it to update the data for that line.
            self._plot_ref.set_ydata(self.ydata)

        # Trigger the canvas to update and redraw.
        self.canvas.draw()

    def get_face_confidence(self, time):
        return 1
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MovingWindow()
    app.exec_()
