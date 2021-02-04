# archiveWindow1.py
import sys
from PyQt5.QtWidgets import (
    QWidget, QLineEdit, QLabel, QPushButton, QScrollArea, QMainWindow,
    QApplication, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QCompleter
)
from PyQt5.QtCore import Qt

from BussinesLayer.Services.APIconnection import get_info_json_from_video
from customwidgets import OnOffWidget

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__()

        self.controls = QWidget()  # Controls container widget.
        self.controlsLayout = QVBoxLayout()   # Controls container layout.

        # List of names, widgets are stored in a dictionary by these keys.
        widget_names = [
            "Heater", "Stove", "Living Room Light", "Balcony Light",
            "Fan", "Room Light", "Oven", "Desk Light",
            "Bedroom Heater", "Wall Switch"
        ]




        self.widgets = []

        # Iterate the names, creating a new OnOffWidget for
        # each one, adding it to the layout and
        # and storing a reference in the self.widgets dict
        for name in widget_names:
            item = OnOffWidget(name)
            self.controlsLayout.addWidget(item)
            self.widgets.append(item)

        spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.controlsLayout.addItem(spacer)
        self.controls.setLayout(self.controlsLayout)

        # Scroll Area Properties.
        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.controls)

        # Go back
        self.gobackto = QPushButton('go back to')
        self.gobackto.setFixedWidth(250)
        self.gobackto.setFixedHeight(25)
        self.gobackto.clicked.connect(self.goBackFunc)


        # Search bar.
        self.searchbar = QLineEdit()
        self.searchbar.textChanged.connect(self.update_display)

        # Adding Completer.
        self.completer = QCompleter(widget_names)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchbar.setCompleter(self.completer)

        # Add the items to VBoxLayout (applied to container widget)
        # which encompasses the whole window.
        container = QWidget()
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(self.gobackto)
        containerLayout.addWidget(self.searchbar)
        containerLayout.addWidget(self.scroll)

        container.setLayout(containerLayout)
        self.setCentralWidget(container)

        self.setGeometry(600, 100, 800, 600)
        self.setWindowTitle('Archive Window')

    def update_display(self, text):

        for widget in self.widgets:
            if text.lower() in widget.name.lower():
                widget.show()
            else:
                widget.hide()

    def goBackFunc(self):
        return

    def openGraphData(self, name):
        # vid_id = get_vid_id_from_db(name)
        # json_file = get_info_json_from_video(vid_id)
        return

app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec_())
