from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QLineEdit, QPushButton
from PyQt5 import uic
import sys
import SQL_Test
import numpy




Ui_MainWindow,junk = uic.loadUiType('testGUI.ui')


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        #load ui
        # uic.loadUi("testGUI.ui", self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #show app
        self.show()


        self.setup_conn()


        self.parameter1 = 0
        self.parameter2 = 0

    def setup_conn(self):
        self.ui.pushButtonSave.clicked.connect(self.saveData)


        #setting up defualts
        self.ui.lineEditP1.setPlaceholderText('0')
        self.ui.lineEditP2.setPlaceholderText('0')

        #must press enter after done editing a parameter now
        self.ui.lineEditP1.editingFinished.connect(self.updateScanNum1)
        self.ui.lineEditP2.editingFinished.connect(self.updateScanNum2)

    def updateScanNum1(self):
        self.parameter1 = int(self.ui.lineEditP1.text())

    def updateScanNum2(self):
        self.parameter2 = int(self.ui.lineEditP2.text())

    def saveData(self):
        sql = SQL_Test.SQL_object()
        sql.insert(self.parameter1, self.parameter2)
        # this is where pgadmin stuff comes in

# Initialize the app
if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = UI()
    UIWindow.show()
    app.exec_()



