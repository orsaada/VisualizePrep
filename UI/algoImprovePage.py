import json
import os
from pathlib import Path

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QLabel, QTableView
import pandas as pd

from BussinesLayer.Algorithms.Visualize.mg.py3loader.algorithm import create_faces_list
from BussinesLayer.Algorithms.Visualize.mg.py3loader.algorithms_without_mg import algorithm_1_without_mg, \
    algorithm_2_improved_without_mg, algorithm_faces_speakers_without_mg
from BussinesLayer.Services.VideoInsights import get_analyzed_data, get_transcript_algo
from UI.Graphs.comparisonGraph import ComparisonGraph
from UI.Graphs.MplCanvas.pandasWindow import pandasModel
from UI.PageWindow import PageWindow
import sys
from PyQt5.QtWidgets import (QPushButton, QApplication)

from UI.tableWidget import TableView


class AlgoImprovePage(PageWindow):

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

        details_dictionary = {
            'algo 1': 'transfer unknown character between two appearances of the same character',
            'algo 2': 'transfer unknown character between two appearances only in the same shot of the same character',
            'algo 3': 'we took the times which speaker talk and tagged the character in the same scene by this data',
            'algo 4': 'pipeline of the algo1, algo2 and algo 3',
            'transcript': 'check similarity between video indexer transcript and the srt file',
            'algo 5': ' check',
        }

        base_path = Path(__file__).parent.parent
        with open((base_path / 'config.json').resolve(), 'r') as f:
            data = json.load(f)

        details = QLabel("Details about algorithm: " + details_dictionary[data['algo']])

        layout.addWidget(details)

        if data["ttMovie"] == '':
            return
        elif data['algo'] == 'transcript':
            a = [0] * 4
            b = get_transcript_algo(data["ttMovie"])
            b = list(map(float, b))
            b = [i for i in b]
            d = {'col1': [1, 2], 'col2': [3, 4]}
            df = pd.DataFrame(d)
            model = pandasModel(df)
            view = QTableView()
            view.setModel(model)
            b3 = ComparisonGraph('transcript', a, b)
            b3.update()
            label_values1 = QLabel()
            label_values2 = QLabel()
            label_values2.setText(str(b))
            layout.addWidget(b3)
            layout.addWidget(label_values2)
            # self.setCentralWidget(widget)
        else:
            self.table = QTableView()
            ROOT_DIR = Path(__file__).parent.parent
            movie_path = ROOT_DIR / "BussinesLayer/Algorithms/Visualize/vi_json/{}.json".format(data['ttMovie'])
            result = []
            if data['algo'] == 'algo 1':
                result = algorithm_1_without_mg(movie_path, create_faces_list(movie_path))
            elif data['algo'] == 'algo 2':
                result = algorithm_2_improved_without_mg(movie_path, create_faces_list(movie_path))
            elif data['algo'] == 'algo 3':
                result = algorithm_faces_speakers_without_mg(movie_path, create_faces_list(movie_path))
            result = [list(i) for i in result]

            if result:
                self.table = TableView(result, ['Scene Start Time', 'Scene End Time', 'Before Improvement Algorithm',
                                                'After Improvement Algorithm'], len(result), 4)
                # self.table.setModel(self.model)
                layout.addWidget(self.table)
                # self.setCentralWidget(self.table)
        self.setCentralWidget(widget)
        layout.addWidget(b1)

        widget.setLayout(layout)

    def goToMovie(self):
        self.parent().parent().goto('movie')


def main():
    app = QApplication(sys.argv)
    window = AlgoImprovePage("wow")
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
