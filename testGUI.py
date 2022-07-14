# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'testGUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(551, 297)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButtonSave = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSave.setGeometry(QtCore.QRect(230, 40, 83, 29))
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.lineEditP1 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditP1.setGeometry(QtCore.QRect(90, 110, 113, 28))
        self.lineEditP1.setObjectName("lineEditP1")
        self.lineEditP2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditP2.setGeometry(QtCore.QRect(330, 110, 113, 28))
        self.lineEditP2.setObjectName("lineEditP2")
        self.labelP1 = QtWidgets.QLabel(self.centralwidget)
        self.labelP1.setGeometry(QtCore.QRect(100, 80, 91, 20))
        self.labelP1.setObjectName("labelP1")
        self.labelP2 = QtWidgets.QLabel(self.centralwidget)
        self.labelP2.setGeometry(QtCore.QRect(350, 80, 81, 20))
        self.labelP2.setObjectName("labelP2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 551, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButtonSave.setText(_translate("MainWindow", "Save Data"))
        self.labelP1.setText(_translate("MainWindow", "Parameter 1"))
        self.labelP2.setText(_translate("MainWindow", "Parameter 2"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
