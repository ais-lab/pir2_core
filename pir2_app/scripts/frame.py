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
import math


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

        # setting backgroud color
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(p)

        # initialze parameter
        self.cmd = ""
        self.filename_out_mts=""
        self.x_rb = 0
        self.y_rb = 0
        self.theta_rb = 0
        self.lorr = "left"
        self.last_vel = 0.0

        # Loading images
        img_path = rospkg.RosPack().get_path('pir2_app') + '/scripts/image/ind3.png'
        mask_path  =rospkg.RosPack().get_path('pir2_app') + '/scripts/image/alpha.png'
        mask = Image.open(mask_path)
        self.rb = Image.open(img_path)

        # image information
        self.img_height = 460
        self.img_width = 460
        self.size = self.img_height, self.img_width, 3
        self.resolution = float(10) / float(self.img_height)

        # add signals
        self.uic.pushButton.clicked.connect(self.adding)
        self.uic.pushButton2.clicked.connect(self.saving)
        self.uic.pushButton3.clicked.connect(self.reset)
        self.uic.pushButton5.clicked.connect(self.select)

        # for naviagtion
        self.nav_x = 0
        self.nav_y = 0

        #initialize Imagelabel
        self.init_drawing()


    def mousePressEvent(self, event):
        if self.uic.cmd_text == "navigation":
            self.nav_x = event.pos().x() - 200
            self.nav_y = event.pos().y() - 220
            set_img = np.copy(self.raw_img)
            self.rb_drawing(set_img, self.x_rb, self.y_rb, self.theta_rb, self.nav_x, self.nav_y)

    def adding(self):
        if self.uic.cmd_text == "turning":
            if str(self.uic.radioButton.isChecked()) == "True":
                self.lorr = "left"
                self.cmd += self.uic.cmd_text + " " + self.uic.lineEdit.text() + " " + self.uic.lineEdit_2.text() + " " + self.uic.lineEdit_3.text() + " left" + "\n"
            else:
                self.lorr = "right"
                self.cmd += self.uic.cmd_text + " " + self.uic.lineEdit.text() + " " + self.uic.lineEdit_2.text() + " " + self.uic.lineEdit_3.text() + " right" + "\n"
        elif self.uic.cmd_text == "e":
            self.filename_out_mts = str(self.filename).split('.')[0]
            self.cmd += self.uic.cmd_text + " " + self.filename_out_mts + "\n"
        else:
            self.cmd += self.uic.cmd_text + " " + self.uic.lineEdit.text() + " " + self.uic.lineEdit_2.text() + " " + self.uic.lineEdit_3.text() + "\n"
        self.uic.label4.setText(self.cmd)
        self.drawing(self.uic.cmd_text)

    def drawing(self, text):
        current_x = self.x_rb
        current_y = self.y_rb
        if self.uic.lineEdit_2.text():
            if text == "forward":
                distance = int(float(self.uic.lineEdit_2.text()) / 1000.0 / self.resolution)
                self.last_vel = float(self.uic.lineEdit.text()) / 1000.0
                if float(self.uic.lineEdit.text()) > 0.0:
                    self.x_rb += int(distance * math.cos(math.radians(self.theta_rb + 90)))
                    self.y_rb -= int(distance * math.sin(math.radians(self.theta_rb + 90)))
                else:
                    self.x_rb -= int(distance * math.cos(math.radians(self.theta_rb + 90)))
                    self.y_rb += int(distance * math.sin(math.radians(self.theta_rb + 90)))
                self.raw_img = cv2.line(self.raw_img,(current_x,current_y),(self.x_rb,self.y_rb),(255,0,0),2)
            elif text == "acceleration":
                acc = float(self.uic.lineEdit.text()) / 1000.0
                vel = float(self.uic.lineEdit_2.text()) / 1000.0
                distance = int((vel * vel - self.last_vel * self.last_vel) / 2 / acc)
                self.last_vel = vel
                if vel > 0.0:
                    self.x_rb += int(distance * math.cos(math.radians(self.theta_rb + 90)))
                    self.y_rb -= int(distance * math.sin(math.radians(self.theta_rb + 90)))
                else:
                    self.x_rb += int(distance * math.cos(math.radians(self.theta_rb + 90)))
                    self.y_rb -= int(distance * math.sin(math.radians(self.theta_rb + 90)))
                self.raw_img = cv2.line(self.raw_img,(current_x,current_y),(self.x_rb,self.y_rb),(255,0,0),2)
            elif text == "turning":
                radius = int(float(self.uic.lineEdit_2.text()) / 1000.0 / self.resolution)
                distance = int(float(self.uic.lineEdit_3.text()) / 1000.0 / self.resolution)
                angle = int(distance * 360 / 2/ math.pi / radius)
                self.last_vel = float(self.uic.lineEdit.text()) / 1000.0
                if self.lorr == "right":
                    center_x = self.x_rb - int(radius * math.sin(math.radians(self.theta_rb + 90)) * math.sin(math.radians(-90)))
                    center_y = self.y_rb - int(radius * math.cos(math.radians(self.theta_rb + 90)) * math.sin(math.radians(-90)))
                    self.raw_img = cv2.ellipse(self.raw_img,(center_x,center_y),(radius, radius),  180-self.theta_rb,0, angle, (255,0,0), 2)
                    diff_x, diff_y = self.cal_dis(radius, 180-self.theta_rb, angle)
                    self.x_rb -= diff_x
                    self.y_rb -= diff_y
                    self.theta_rb -= angle
                else:
                    center_x = self.x_rb - int(radius * math.sin(math.radians(self.theta_rb + 90)) * math.sin(math.radians(90)))
                    center_y = self.y_rb - int(radius * math.cos(math.radians(self.theta_rb + 90)) * math.sin(math.radians(90)))
                    self.raw_img = cv2.ellipse(self.raw_img,(center_x,center_y),(radius, radius), -self.theta_rb, 0, -angle, (255,0,0), 2)
                    diff_x, diff_y = self.cal_dis(radius, -self.theta_rb, -angle)
                    self.x_rb -= diff_x
                    self.y_rb -= diff_y
                    self.theta_rb += angle
            elif text == "rotation":
                angle = int(self.uic.lineEdit_2.text())
                self.theta_rb += angle
            set_img = np.copy(self.raw_img)
            self.rb_drawing(set_img, self.x_rb, self.y_rb, self.theta_rb, -100, -100)

        elif text == "navigation":
            self.raw_img = cv2.line(self.raw_img, (current_x, current_y), (self.nav_x, self.nav_y), (0,255,255), 2)
            self.x_rb = self.nav_x
            self.y_rb = self.nav_y
            set_img = np.copy(self.raw_img)
            self.rb_drawing(set_img, self.x_rb, self.y_rb, self.theta_rb, -100, -100)

        else:
            pass

    def Lighten(self, in_img, bk_img):
        for width in range(in_img.shape[1]):
            for height in range(in_img.shape[0]):

                if bk_img[width][height][0] < 50 and bk_img[width][height][1] < 50 and bk_img[width][height][2] < 50:
                    # in_img[width][height] = in_img[width][height]
                    pass
                else:
                    in_img[width][height] = bk_img[width][height]
        return in_img

    def rb_drawing(self, in_img, x, y, theta, x2, y2):
        show_img = np.zeros(in_img.shape, dtype=np.uint8)
        show_img.fill(255)
        mask_img = np.zeros(in_img.shape, dtype=np.uint8)
        rb_img = np.copy(self.rb)
        rb_x, rb_y, c = rb_img.shape

        rb_img = Image.fromarray(np.uint8(rb_img))
        rb_img = rb_img.rotate(theta, expand=True)

        # for navigation point and robot icon
        mask_img = cv2.circle(mask_img,(x2,y2), 5, (0,255,255), -1)
        mask_img = Image.fromarray(np.uint8(mask_img))
        mask_img.paste(rb_img , (x - rb_x/2, y - rb_y/2))

        mask_img = np.asarray(mask_img)
        show_img = self.Lighten(in_img, mask_img)

        qimg = QImage(show_img, show_img.shape[1], show_img.shape[0], QImage.Format_RGB888)
        # self.uic.imageLabel.setWindowOpacity(0.8)
        self.uic.imageLabel.setPixmap(QPixmap.fromImage(qimg))

    def cal_dis(self, radius, start_angle, angle):
        start_x = int(radius * math.cos(math.radians(start_angle)) - 0 * math.sin(math.radians(start_angle)))
        start_y = int(radius * math.sin(math.radians(start_angle)) + 0 * math.cos(math.radians(start_angle)))
        end_x = int(radius * math.cos(math.radians(start_angle + angle)) - 0 * math.sin(math.radians(start_angle + angle)))
        end_y = int(radius * math.sin(math.radians(start_angle + angle)) + 0 * math.cos(math.radians(start_angle + angle)))
        return start_x - end_x, start_y - end_y

    def init_drawing(self):
        self.raw_img = np.zeros(self.size, dtype=np.uint8)
        self.raw_img.fill(255)
        img = np.zeros(self.raw_img.shape, dtype=np.uint8)
        img.fill(255)
        self.x_rb = self.img_height / 2
        self.y_rb = self.img_width / 2
        self.theta_rb = 0
        self.rb_drawing(img, self.x_rb, self.y_rb, 0, -100, -100)

    def saving(self):
        text, ok = QInputDialog.getText(self, '---Input Dialog---', 'Enter file name:')
        path_w = rospkg.RosPack().get_path('pir2_control') + '/motion/' + text + '.mts'
        with open(path_w, mode='w') as f:
            f.write(self.cmd)

    def reset(self):
        self.uic.label4.setText("")
        self.cmd = ""
        self.init_drawing()

    def select(self):
        path = rospkg.RosPack().get_path('pir2_control') + '/motion'
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', path)
        self.filename = QFileInfo(fname).fileName()

        self.uic.label5.setVisible(True)
        self.uic.label5.setText(str(self.filename))

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
