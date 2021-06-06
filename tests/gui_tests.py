import pytest

from PyQt5 import QtCore

from UI.mainPage import mainWindow

@pytest.fixture
def app(qtbot):
    test_hello_app = mainWindow()
    qtbot.addWidget(test_hello_app)
    return test_hello_app

def test_label():
    pass