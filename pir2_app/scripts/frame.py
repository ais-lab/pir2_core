#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os.path

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from top import Ui_top
from create import Ui_create
from execute import Ui_exe

import rospy
import rospkg

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter


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
        self.theta_rb = 60

        img_path = rospkg.RosPack().get_path('pir2_app') + '/scripts/image/ind2.png'
        mask_path  =rospkg.RosPack().get_path('pir2_app') + '/scripts/image/alpha.png'
        path  =rospkg.RosPack().get_path('pir2_app') + '/scripts/image/ind2.png'
        self.rb = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        mask = Image.open(mask_path)
        rb = Image.open(img_path)
        # self.bg = Image.new("RGBA", rb.size, (0, 0, 0, 0))
        # self.bg.paste(rb,(0,0),mask.split()[0])
        self.bg = rb
        # self.rb.show()
        self.img_height = 460
        self.img_width = 460
        size = self.img_height, self.img_width, 3
        self.raw_img = np.zeros(size, dtype=np.uint8)
        self.raw_img.fill(255)
        img = np.copy(self.raw_img)
        self.uic.init_drawing(img)


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
            if self.uic.lineEdit_2.text():
                pixel = int(float(self.uic.lineEdit_2.text()) / 1000.0 / self.uic.resolution)
                self.uic.raw_img = cv2.line(self.uic.raw_img,(self.uic.y_rb,self.uic.x_rb),(self.uic.y_rb,self.uic.x_rb - pixel),(255,0,0),2)
                self.uic.y_rb -= pixel
        else:
            pass

        self.rb_drawing(self.uic.raw_img)

    def saving(self):
        text, ok = QInputDialog.getText(self, '---Input Dialog---', 'Enter file name:')
        path_w = rospkg.RosPack().get_path('pir2_control') + '/motion/' + text + '.mts'
        with open(path_w, mode='w') as f:
            f.write(self.cmd)

    def reset(self):
        self.uic.label4.setText("")
        self.cmd = ""
        self.reset_img()

    def rb_drawing(self, in_img):
        # h, w = self.rb.shape
        M = cv2.getRotationMatrix2D(center=(self.rb.shape[1] / 2, self.rb.shape[0] / 2), angle=self.theta_rb, scale=1.0)
        # h, w, c = in_img.shape
        combined = cv2.warpAffine(self.rb, M, dsize=(in_img.shape[1], in_img.shape[0]), dst=in_img, borderMode=cv2.BORDER_TRANSPARENT)

        self.bg = self.bg.rotate(self.theta_rb, expand=True)
        in_img = Image.fromarray(np.uint8(in_img))
        in_img.paste(self.bg , (self.uic.x_rb-14, self.uic.y_rb-12))
        # back_im.save('data/dst/rocket_pillow_paste_pos.jpg', quality=95)
        in_img = np.asarray(in_img)
        qimg = QImage(in_img, in_img.shape[1], in_img.shape[0], QImage.Format_RGB888)
        self.uic.imageLabel.setPixmap(QPixmap.fromImage(qimg))



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
        self.uic.x_rb = self.uic.img_height/2
        self.uic.y_rb = self.uic.img_width/2
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
