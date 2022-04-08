# -*- coding: utf-8 -*-
"""
Program for ENF detector GUI
"""
# import required packages
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QWidget
import matplotlib.pyplot as plt
import scipy.io.wavfile as wav
from PIL import Image
import cv2
import numpy as np
import testingCLI



class Ui_Detector(object):
    def setupUi(self, Detector):
        Detector.setObjectName("Detector")
        Detector.setFixedSize(1120, 687)
        Detector.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(Detector)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 550, 106, 30))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.switch_view)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 550, 106, 30))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.refresh)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 50, 1061, 401))
        self.label.setFrameShape(QtWidgets.QFrame.Box)
        self.label.setText("")
        self.label.setObjectName("label")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(290, 550, 106, 30))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.save_img)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(780, 520, 301, 61))
        self.label_2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(900, 490, 131, 21))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(500, 20, 200, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 480, 500, 30))
        self.label_5.setObjectName("label_5")
        self.label_5.setFrameShape(QtWidgets.QFrame.Box)
        self.label_5.setText("")
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

        self.menuInput.addAction(self.actionSelect_Audio)
        self.menuSave.addAction(self.actionSpectrogram)

        self.menubar.addAction(self.menuInput.menuAction())
        self.menubar.addAction(self.menuSave.menuAction())
        self.file = None
        self.save_out = None
        self.save_name = None
        self.spect = None
        self.logic = 1
        self.actionSelect_Audio.triggered.connect(self.browse_file)
        self.actionSpectrogram.triggered.connect(self.save_img)
        self.menuSave.setDisabled(True)
        self.retranslateUi(Detector)
        QtCore.QMetaObject.connectSlotsByName(Detector)



    def browse_file(self):
        """
        function to browse audio file from disk to use as input
         """
        self.label.clear()
        self.pushButton.setDisabled(True)
        self.pushButton_3.setDisabled(True)
        self.actionSelect_Audio.setDisabled(False)
        self.menuSave.setDisabled(False)
        self.label_2.setText("")
        self.pushButton_2.setDisabled(True)
        self.label_5.setText("")
        self.label_4.setText("")

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None, "Select Audio(wav Format) ", "",
                                                  "Audio Files (*.wav)", options=options)

        if fileName:
            self.pushButton.setDisabled(False)
            self.file = fileName
            self.actionSelect_Audio.setDisabled(False)
            fname = fileName[10:]
            self.label_5.setVisible(True)
            self.label_5.setText(fname)

        else:
            self.pushButton.setDisabled(True)

        self.main_code(fileName)

    def main_code(self, file):
        """

        Code for ENF detection in an audio file
        """
        self.pushButton_2.setDisabled(False)
        self.pushButton_3.setDisabled(False)
        fs1, audio1 = wav.read(self.file)  # 'H:/python-projects/audio/01_mic1_table_enf.wav'

        # condition for taking only one channel of stereo audio
        if len(audio1.shape) == 2:
            snd = audio1[:, 1]
        else:
            snd = audio1

        # plotting spectrum and saving as image
        fig = plt.figure(figsize=(10, 5))
        plt.specgram(snd, Fs=fs1, NFFT=32768, scale_by_freq=100, noverlap=900)
        plt.ylim([0, 200])
        plt.xlabel('Time')
        plt.ylabel('Frequency')
        plt.set_cmap('Dark2_r')
        plt.title('Audio Spectrum ')
        plt.xlabel('time')
        plt.ylabel('frequency')
        fig.savefig('0-spec1.jpg', bbox_inches='tight', dpi=250)

        # Create an Image Object from an Image
        im = Image.open('0-spec1.jpg')
        self.spect = im


        cropped = im.crop((400, 700, 2000, 900))

        # save cropped image
        cropped.save('1-crop.jpg')


        # reading crop image
        image1 = cv2.imread('1-crop.jpg')

        # copying imaage for final display
        real_img = image1.copy()

        # Edge detection in an image
        edges = cv2.Canny(image1, 100, 200, apertureSize=3)
        cv2.imwrite('2-edges.jpg', edges)

        # Line detection in an image after edge detection
        lines = cv2.HoughLinesP(edges, rho=1, theta=1 * np.pi / 180, threshold=100, minLineLength=145, maxLineGap=80)

        # loop to draw line on image
        # comment sse: This should draws only one line
        for x1, y1, x2, y2 in lines[0]:
            cv2.line(image1, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imwrite('3-lines.jpg', image1)

        # Green color range
        lower2 = [0, 0, 0]
        upper2 = [0, 255, 0]

        # converting color range into numpy array
        lower2 = np.array(lower2, dtype="uint8")
        upper2 = np.array(upper2, dtype="uint8")

        # creating mask
        mask2 = cv2.inRange(image1, lower2, upper2)  # mask for green color
        cv2.imwrite('4-mask.jpg', mask2)

        # putting mask on image
        output = cv2.bitwise_and(image1, image1, mask=mask2)
        cv2.imwrite('5-mask+image.jpg', output)
        # show the resulted image

        # finding contour
        ret, thresh = cv2.threshold(mask2, 40, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) != 0:
            # draw in blue the contours that were founded
            cv2.drawContours(output, contours, -1, 255, 3)

            # find the biggest countour (c) by the area
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)

            # condition for false positive
            if 100 > y > 20:
                # draw the biggest contour (c) in red
                cv2.rectangle(output, (x, y), (x + w, y + h), (0, 0, 255), 1)
            else:
                cv2.rectangle(output, (x, y), (x + w, y + h), (0, 0, 0), 3)

        cv2.imwrite('6-result.jpg', output)
        im_final = Image.open('6-result.jpg')
        width, height = im_final.size

        line_len = 0.987 * width

        # condition for ENF detection
        if 100 > y > 20 and w != 0:
            stat = " ENF Detected \n "
        else:
            stat = " ENF Not Detected \n "

        # condition for tempering detecion
        if 100 > y > 20 and w < line_len:
            temp = "Audio File is Tempered"
        else:
            temp = ""

        self.img_show(np.asanyarray(im_final))
        self.label_2.setText(stat+temp)
        self.pushButton.setDisabled(False)
        self.save_out = output
        self.logic = 2
        self.label_4.setText("ENF Line")

    def img_show(self, inp, window=1):
        """
        function to display on GUI
        """
        qformat = QtGui.QImage.Format_RGB888
        display_width = int(1060)
        display_height = int(400)
        h, w, ch = inp.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(inp.data, w, h, bytes_per_line, qformat)
        p = convert_to_Qt_format.scaled(display_width, display_height)
        self.label.setPixmap(QtGui.QPixmap.fromImage(p))
        QtWidgets.QApplication.processEvents()
        self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def switch_view(self, spec):
        if self.logic == 2:
            self.img_show(np.asanyarray(self.spect))
            self.label_4.setText("Audio Spectrogram")
            self.logic= 1
        elif self.logic == 1:
            self.main_code(self.file)
            self.label_4.setText("ENF Line")
            self.logic = 2

    def refresh(self):
        """
        function to restart the applicaiton
         """
        self.label.clear()
        self.pushButton.setDisabled(True)
        self.pushButton_3.setDisabled(True)
        self.actionSelect_Audio.setDisabled(False)
        self.menuSave.setDisabled(True)
        self.label_2.setText("")
        self.pushButton_2.setDisabled(True)
        self.label_5.setText("")
        self.label_4.setText("")

    def save_img(self, save_out):
        """
        function to save image
        """
        if self.logic == 1:
            name, _ = QFileDialog.getSaveFileName(None, 'Save File')
            if name:
                self.save_name = name
            cv2.imwrite(self.save_name + ".jpg", self.save_out)
            self.pushButton_3.setDisabled(True)

        elif self.logic == 2:
            name, _ = QFileDialog.getSaveFileName(None, 'Save File')
            if name:
                self.save_name = name
            #cv2.imwrite(self.save_name + ".jpg", self.spect)
            self.spect.save(name+".jpg")
            self.pushButton_3.setDisabled(True)

    def retranslateUi(self, Detector):
        _translate = QtCore.QCoreApplication.translate
        Detector.setWindowTitle(_translate("Detector", "ENF-Detector"))
        self.pushButton.setText(_translate("Detector", "Switch View"))
        self.pushButton_2.setText(_translate("Detector", "Refresh"))
        self.pushButton_3.setText(_translate("Detector", "Save Image"))
        self.label_3.setText(_translate("Detector", "Status"))
        self.label_4.setText(_translate("Detector", ""))
        self.menuInput.setTitle(_translate("Detector", "File"))
        self.actionSelect_Audio.setText(_translate("Detector", "Select Audio"))
        self.menuSave.setTitle(_translate("Detector", "Save Image"))
        self.actionSpectrogram.setText(_translate("Detector", "Browse"))

        self.pushButton.setDisabled(True)
        self.pushButton_2.setDisabled(True)
        self.pushButton_3.setVisible(False)
        self.label_5.setVisible(False)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Detector = QtWidgets.QMainWindow()
    ui = Ui_Detector()
    ui.setupUi(Detector)
    Detector.show()
    sys.exit(app.exec_())

