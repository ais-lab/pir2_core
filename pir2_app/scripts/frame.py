#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from top import Ui_top
from create import Ui_create
from execute import Ui_exe
import rospy
import rospkg
import os.path
import cv2
import numpy as np


class Menu(QDialog):
    def __init__(self,parent=None):
        super(Menu, self).__init__(parent)
        self.ui = Ui_top()
        self.ui.setupUi(self)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(p)

    def execute(self):
        # window3.showMaximized()
        window3.show()

    def create(self):
        # window2.showMaximized()
        window2.show()

    def slam(self):
        ROS_PROGRAM = QProcess(self)
        print "Launching..."
        program = 'roslaunch pir2_description pir2_description.launch'
        ROS_PROGRAM.start(program)

class Create(QDialog):
    def __init__(self,parent=None):
        super(Create, self).__init__(parent)
        self.uic = Ui_create()
        self.uic.setupUi(self)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(p)
        self.cmd = ""
        self.filename_out_mts=""
    def adding(self):

        if self.uic.cmd_text == "turning":
            if str(self.uic.radioButton.isChecked()) == "True":
                self.cmd += self.uic.cmd_text + " " + self.uic.lineEdit.text() + " " + self.uic.lineEdit_2.text() + " " + self.uic.lineEdit_3.text() + " left" + "\n"
            else:
                self.cmd += self.uic.cmd_text + " " + self.uic.lineEdit.text() + " " + self.uic.lineEdit_2.text() + " " + self.uic.lineEdit_3.text() + " right" + "\n"
        elif self.uic.cmd_text == "e":
            self.filename_out_mts = str(self.filename).split('.')[0]
            self.cmd += self.uic.cmd_text + " " + self.filename_out_mts
        else:
            self.cmd += self.uic.cmd_text + " " + self.uic.lineEdit.text() + " " + self.uic.lineEdit_2.text() + " " + self.uic.lineEdit_3.text() + "\n"
        self.uic.label4.setText(self.cmd)
        # print self.uic.lineEdit.text()
        self.drawing(self.uic.cmd_text)

    def drawing(self, text):
        if text == "forward":
            pixel = int(float(self.uic.lineEdit_2.text()) / 1000.0 / self.uic.resolution)
            self.uic.img = cv2.line(self.uic.img,(self.uic.now_height,self.uic.now_width),(self.uic.now_height,self.uic.now_width - pixel),(255,0,0),2)
        else:
            pass
        qimg = QImage(self.uic.img.data, self.uic.img.shape[1], self.uic.img.shape[0], QImage.Format_RGB888)
        self.uic.imageLabel.setPixmap(QPixmap.fromImage(qimg))
        # self.uic.imageLabel.move(200,220)


    def saving(self):
        text, ok = QInputDialog.getText(self, '---Input Dialog---', 'Enter file name:')
        path_w = rospkg.RosPack().get_path('pir2_control') + '/motion/' + text + '.mts'
        with open(path_w, mode='w') as f:
            f.write(self.cmd)
        # if ok:
        #     self.le.setText(str(text))

    def reset(self):
        self.uic.label4.setText("")
        self.cmd = ""
        self.reset_img()

    def select(self):
        path = rospkg.RosPack().get_path('pir2_control') + '/motion'
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', path)
        self.filename = QFileInfo(fname).fileName()

        self.uic.label5.setVisible(True)
        self.uic.label5.setText(str(self.filename))

        # if fname:
        #     test_data = open(fname, "r")
        #     contents = test_data.read()
        #     self.uie.label3.setText(str(contents))
        #     test_data.close()
    def reset_img(self):
        size = self.uic.img_height, self.uic.img_width, 3
        self.uic.img = np.zeros(size, dtype=np.uint8)
        self.uic.img.fill(255)
        cv2.drawMarker(self.uic.img, (self.uic.img_height/2, self.uic.img_width/2), color=(255, 0, 0),
                   markerType=cv2.MARKER_TRIANGLE_UP, markerSize=10,thickness=2)
        self.uic.now_height = self.uic.img_height/2
        self.uic.now_width = self.uic.img_width/2
        qimg = QImage(self.uic.img.data, self.uic.img.shape[1], self.uic.img.shape[0], QImage.Format_RGB888)
        self.uic.imageLabel.setPixmap(QPixmap.fromImage(qimg))
        self.uic.imageLabel.move(200,220)

class Execute(QDialog):
    def __init__(self,parent=None):
        super(Execute, self).__init__(parent)
        self.uie = Ui_exe()
        self.uie.setupUi(self)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(p)
        self.filename=""

    def select(self):
        path = rospkg.RosPack().get_path('pir2_control') + '/motion'
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', path)
        self.filename = QFileInfo(fname).fileName()

        # self.uie.label2.setStyleSheet('color: red')
        self.uie.label2.setFont(QFont("Times", 12, QFont.Bold))
        self.uie.label2.setText(str(self.filename))

        if fname:
            test_data = open(fname, "r")
            contents = test_data.read()
            self.uie.label3.setText(str(contents))
            test_data.close()

    def launch(self):
        ROS_PROGRAM = QProcess(self)
        self.filename, ext = os.path.splitext(self.filename)
        program = 'roslaunch pir2_control pir2_control.launch file:=' + self.filename
        #program = 'roslaunch pir2_description pir2_description.launch'
        ROS_PROGRAM.start(program)

if __name__ == '__main__':
    rospy.init_node('gui_frame')
    app = QApplication(sys.argv)
    window = Menu()
    window2 = Create()
    window3 = Execute()
    # window.showMaximized()
    window.show()
    sys.exit(app.exec_())
