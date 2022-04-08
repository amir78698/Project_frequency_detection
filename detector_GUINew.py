# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'detector.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Detector(object):
    def setupUi(self, Detector):
        Detector.setObjectName("Detector")
        Detector.resize(1120, 687)
        Detector.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(Detector)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 550, 106, 30))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 550, 106, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 50, 1061, 401))
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(290, 550, 106, 30))
        self.pushButton_3.setObjectName("pushButton_3")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(780, 520, 301, 61))
        self.label_2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(900, 490, 131, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(500, 20, 131, 21))
        self.label_4.setObjectName("label_4")
        Detector.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Detector)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1120, 26))
        self.menubar.setObjectName("menubar")
        self.menuInput = QtWidgets.QMenu(self.menubar)
        self.menuInput.setObjectName("menuInput")
        self.menuSave = QtWidgets.QMenu(self.menubar)
        self.menuSave.setObjectName("menuSave")
        Detector.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Detector)
        self.statusbar.setObjectName("statusbar")
        Detector.setStatusBar(self.statusbar)
        self.actionSelect_Audio = QtWidgets.QAction(Detector)
        self.actionSelect_Audio.setObjectName("actionSelect_Audio")
        self.actionSpectrogram = QtWidgets.QAction(Detector)
        self.actionSpectrogram.setObjectName("actionSpectrogram")
        self.actionENF_Line = QtWidgets.QAction(Detector)
        self.actionENF_Line.setObjectName("actionENF_Line")
        self.menuInput.addAction(self.actionSelect_Audio)
        self.menuSave.addAction(self.actionSpectrogram)
        self.menuSave.addAction(self.actionENF_Line)
        self.menubar.addAction(self.menuInput.menuAction())
        self.menubar.addAction(self.menuSave.menuAction())

        self.retranslateUi(Detector)
        QtCore.QMetaObject.connectSlotsByName(Detector)

    def retranslateUi(self, Detector):
        _translate = QtCore.QCoreApplication.translate
        Detector.setWindowTitle(_translate("Detector", "ENF-Detector"))
        self.pushButton.setText(_translate("Detector", "Start"))
        self.pushButton_2.setText(_translate("Detector", "Refresh"))
        self.pushButton_3.setText(_translate("Detector", "Save Image"))
        self.label_3.setText(_translate("Detector", "Status"))
        self.label_4.setText(_translate("Detector", "Spectrogram"))
        self.menuInput.setTitle(_translate("Detector", "Input"))
        self.menuSave.setTitle(_translate("Detector", "Save"))
        self.actionSelect_Audio.setText(_translate("Detector", "Select Audio"))
        self.actionSpectrogram.setText(_translate("Detector", "Spectrogram"))
        self.actionENF_Line.setText(_translate("Detector", "ENF Line"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Detector = QtWidgets.QMainWindow()
    ui = Ui_Detector()
    ui.setupUi(Detector)
    Detector.show()
    sys.exit(app.exec_())

