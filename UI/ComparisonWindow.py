import json
from pathlib import Path

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QTableView
import pandas as pd
from BussinesLayer.Services.VideoInsights import get_analyzed_data, get_transcript_algo
from UI.Graphs.comparisonGraph import ComparisonGraph
from UI.Graphs.MplCanvas.pandasWindow import pandasModel
from UI.PageWindow import PageWindow
import sys
from PyQt5.QtWidgets import (QPushButton, QApplication)


class ComparisonWindow(PageWindow):

    def __init__(self, algoName):
        super().__init__()
        self.setWindowTitle('My App')
        self.resize(500, 500)
        # Cannot set QxxLayout directly on the QMainWindow
        # Need to create a QWidget and set it as the central widget
        widget = QWidget()
        layout = QVBoxLayout()
        # for all algorithms:
        # loading 1/5 2/5 3/5 4/5 5/5
        b1 = QPushButton('Back To Movie Page')
        b1.setStyleSheet("background-color: red;")
        b1.clicked.connect(self.goToMovie)

        base_path = Path(__file__).parent.parent
        with open((base_path / 'config.json').resolve(), 'r') as f:
            data = json.load(f)
        if data["ttMovie"] == '':
            return
        elif data['algo'] == 'transcript':
            a = [0]*4
            b = get_transcript_algo(data["ttMovie"])
            b = list(map(float, b))
            b = [i for i in b]
        else:
            a, b = get_analyzed_data(data["ttMovie"], data["ttMovie"], int(data['algo'].split()[1]))
            a, b = list(map(float, a)), list(map(float, b))
            a[2] *= 100
            b[2] *= 100
        d = {'col1': [1, 2], 'col2': [3, 4]}
        df = pd.DataFrame(d)
        model = pandasModel(df)
        view = QTableView()
        view.setModel(model)
        b3 = ComparisonGraph(data['algo'], a, b)
        b3.update()

        label_values1 = QLabel()
        if data['algo'] != 'transcript':
            label_values1.setText(str(a))
        label_values2 = QLabel()
        label_values2.setText(str(b))

        details_dictionary = {
            'algo 1': 'transfer unknown character between two appearances of the same character',
            'algo 2': 'transfer unknown character between two appearances only in the same shot of the same character',
            'algo 3': 'we took the times which speaker talk and tagged the character in the same scene by this data',
            'algo 4': 'pipeline of the algo1, algo2 and algo 3',
            'transcript': 'check similarity between video indexer transcript and the srt file',
            'algo 5': ' check',
        }

        # details = QLabel("Details about algorithm: ")
        details = QLabel("Details about algorithm: " + details_dictionary[data['algo']])

        layout.addWidget(b3)
        if data['algo'] != 'transcript':
            layout.addWidget(label_values1)
        layout.addWidget(label_values2)
        # layout.addWidget(view)
        layout.addWidget(details)
        layout.addWidget(b1)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def goToMovie(self):
        self.parent().parent().goto('movie')


def main():
    app = QApplication(sys.argv)
    window = ComparisonWindow("wow")
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
