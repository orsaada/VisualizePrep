import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from BussinesLayer.Data.data import extract_attribute_to_df
from UI.Graphs.MplCanvas.MplCanvas import MplCanvas


class topicsGraph(QMainWindow):

    def __init__(self):
        super().__init__()
        self.resize(1000,1000)
        self.sc = self.init_chart(1)
        # layout = QVBoxLayout()
        # layout.addWidget(self.sc)
        # layout.setContentsMargins(100,100,100,100)
        # widget = QWidget()
        # widget.setLayout(layout)
        # self.setCentralWidget(widget)
        self.setCentralWidget(self.sc)

        # self.show()

    def init_chart(self, path):
        df = extract_attribute_to_df("topics")
        x = list(df['name'])
        y = list(df['confidence'])

        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.bar(x, y)
        sc.axes.set_xticks(x)
        sc.axes.set_xticklabels(x, rotation=90, rotation_mode="default")

        sc.axes.set_xlabel('name')
        sc.axes.set_ylabel('confidence')
        sc.axes.title.set_text('')

        return sc


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = topicsGraph()
    w.show()
    app.exec_()
