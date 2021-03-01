import json
import os

from PyQt5 import QtWidgets

from UI.mainPage import Window

if __name__ == "__main__":
    import sys
    with open('./config.json', 'r') as f:
        data = json.load(f)
    os.remove('./config.json')
    with open('./config.json', 'w') as f:
        data["UserLoggedIn"] = ""
        data["SpecificMoviePage"] = ""
        data["ttMovie"] = ""
        data["algo"] = ""
        data["ENV_MODE"] = 'development'
        json.dump(data, f, indent=4)
    app = QtWidgets.QApplication(sys.argv)
    # styleFile = './style2.qss'
    # qssStyle = CommonHelper.readQSS(styleFile)
    # app.setStyleSheet(qssStyle)
    w = Window()
    w.resize(1200, 700)
    w.show()
    sys.exit(app.exec_())