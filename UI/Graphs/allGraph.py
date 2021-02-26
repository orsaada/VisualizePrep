import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from BussinesLayer.Data.data import extract_attribute_to_df
from UI.Graphs.MplCanvas.MplCanvas import MplCanvas


class allGraphC(QMainWindow):

    def __init__(self,attr):
        # attribute = "namedLocations"
        super().__init__()
        self.resize(2000,1000)
        self.layout = QVBoxLayout()
        # self.layout.addWidget(self.sc)
        chart = self.init_chart(attr)
        # widget = QWidget()
        # widget.setLayout(self.layout)
        self.setCentralWidget(chart)

    def init_chart(self, attr):
        if attr == 'sentiments':
            return self.sentiment_graph()
        elif attr == 'topics':
            return self.topics_graph()
        elif attr == 'faces':
            return self.faces_graph()
        elif attr == 'labels':
            return self.labels_graph()
        elif attr == 'brands':
            return self.brands_graph()
        elif attr == 'namedLocations':
            return self.namedlocation_graph()
        elif attr == 'visualContentModeration':
            return self.visual_graph()
        # self.setCentralWidget(self.sc)
        # self.layout.addWidget(self.sc)
        #
        # return self.

    def faces_graph(self):
        df = extract_attribute_to_df("faces")
        x = np.arange(len(df['confidence']))
        y = df['confidence']
        sc = self.creatMplCanvas(x, y)
        sc.axes.tick_params(labelbottom=False)
        sc.axes.set_xlabel('faces')
        sc.axes.set_ylabel('confidence')
        sc.axes.title.set_text('faces graph')
        return sc

    def labels_graph(self):
        df = extract_attribute_to_df("labels")
        x = list(df['name'])
        y = [len(i) for i in list(df['instances'])]
        sc = self.creatMplCanvas(x, y)
        sc.axes.tick_params(labelbottom=False)
        sc.axes.set_xlabel('labels')
        sc.axes.set_ylabel('number of instances')
        sc.axes.title.set_text('labels graph')
        return sc

    def brands_graph(self):
        df = extract_attribute_to_df("brands")
        x = list(df['name'])
        y = [len(i) for i in list(df['instances'])]
        sc = self.creatMplCanvas(x, y)
        sc.axes.set_xlabel('brands')
        sc.axes.set_ylabel('number of instances')
        sc.axes.title.set_text('brands graph')
        return sc

    def namedlocation_graph(self):
        df = extract_attribute_to_df("namedLocations")
        x = list(df['name'])
        y = [len(i) for i in list(df['instances'])]
        sc = self.creatMplCanvas(x, y)
        sc.axes.set_xlabel('locations')
        sc.axes.set_ylabel('number of instances')
        sc.axes.title.set_text('locations graph')
        return sc

    def visual_graph(self):
        pass

    def topics_graph(self):
        df = extract_attribute_to_df("topics")
        x = list(df['name'])
        y = list(df['confidence'])
        sc = self.creatMplCanvas(x, y)
        sc.axes.set_xlabel('name')
        sc.axes.set_ylabel('confidence')
        sc.axes.title.set_text('topic graph')

        return sc

    def sentiment_graph(self):
        df = extract_attribute_to_df("sentiments")
        x = list(df['sentimentType'])
        y = list(df['averageScore'])
        sc = self.creatMplCanvas(x, y)
        sc.axes.set_xlabel('sentiments')
        sc.axes.set_ylabel('average Score')
        sc.axes.title.set_text('setiment graph')

        return sc

    def creatMplCanvas(self, x, y):
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        sc.axes.bar(x, y)
        sc.axes.set_xticks(x)
        sc.axes.set_xticklabels(x, rotation=90, rotation_mode="default")
        return sc


if __name__ == '__main__':
    app = QApplication(sys.argv)
    attribute = "namedLocations"
    w = allGraphC(attribute)
    w.show()
    app.exec_()
