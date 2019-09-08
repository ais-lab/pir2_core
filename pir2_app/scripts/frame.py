#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from top import Ui_top
from create import Ui_create
import rospy
import rospkg


class Menu(QDialog):
    def __init__(self,parent=None):
        super(Menu, self).__init__(parent)
        self.ui = Ui_top()
        self.ui.setupUi(self)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(p)

    def execute(self):
        pass

    def create(self):
        window2.showMaximized()

    def slam(self):
        ROS_PROGRAM = QProcess(self)
        print "Launching..."
        program = 'roslaunch pir2_description pir2_description.launch'
        ROS_PROGRAM.start(program)

class Create(QDialog):
    def __init__(self,parent=None):
        super(Create, self).__init__(parent)
        self.ui = Ui_create()
        self.ui.setupUi(self)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(p)


if __name__ == '__main__':
    rospy.init_node('gui_frame')
    app = QApplication(sys.argv)
    window = Menu()
    window2 = Create()
    window.showMaximized()
    sys.exit(app.exec_())
