# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget
from PyQt5.QtCore import Qt
import rospkg
import cv2
import numpy as np

class Ui_create(object):
    def setupUi(self, Form):
        Form.setObjectName("Create Mode")
        Form.resize(1366, 768)
        Form.setMouseTracking(True)

        self.cmd_text = ""

        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setGeometry(QtCore.QRect(100, 20, 1160, 160))
        # self.groupBox.setStyleSheet('background-color: lightGray')

        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(10, 90, 150, 25))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("select command")
        self.comboBox.addItem("acceleration")
        self.comboBox.addItem("forward")
        self.comboBox.addItem("rotation")
        self.comboBox.addItem("turning")
        self.comboBox.addItem("pause")
        self.comboBox.addItem("stop")
        self.comboBox.addItem("slowstop")
        self.comboBox.addItem("detect")
        self.comboBox.addItem("e")
        self.comboBox.addItem("end")
        self.comboBox.addItem("navigation")
        self.comboBox.addItem("pan")
        self.comboBox.addItem("tilt")
        self.comboBox.addItem("yaw")
        # self.combo.setGeometry(QtCore.QRect(300, 300, 300, 200))
        self.comboBox.activated[str].connect(self.onActivated)

        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(190, 90, 145, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setVisible(True)
        self.lineEdit.setStyleSheet('background-color: White')

        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(400, 90, 145, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setVisible(True)
        self.lineEdit_2.setStyleSheet('background-color: White')

        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_3.setGeometry(QtCore.QRect(610, 90, 145, 25))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setVisible(False)
        self.lineEdit_3.setStyleSheet('background-color: White')

        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(190, 60, 200, 31))
        self.label.setObjectName("label")
        self.label.setText('acceleration value')
        # self.label.setStyleSheet('background-color: lightGray')

        self.label2 = QtWidgets.QLabel(self.groupBox)
        self.label2.setGeometry(QtCore.QRect(400, 60, 200, 31))
        self.label2.setObjectName("label2")
        self.label2.setText('target speed')
        # self.label2.setStyleSheet('background-color: lightGray')

        self.label3 = QtWidgets.QLabel(self.groupBox)
        self.label3.setGeometry(QtCore.QRect(610, 60, 200, 31))
        self.label3.setObjectName("label3")
        # self.label3.setText('target speed')
        # self.label3.setStyleSheet('background-color: lightGray')
        self.label3.setVisible(False)

        ### "e" select motoin file ###
        self.pushButton5 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton5.setGeometry(QtCore.QRect(190, 90, 271, 25))
        self.pushButton5.setObjectName("pushButton")
        self.pushButton5.setVisible(False)

        self.label5 = QtWidgets.QLabel(self.groupBox)
        self.label5.setGeometry(QtCore.QRect(520, 90, 141, 25))
        self.label5.setObjectName("label")
        self.label5.setVisible(False)

        ### for left or rught ###
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setGeometry(QtCore.QRect(820, 80, 60, 54))
        self.widget.setObjectName("widget")
        self.widget.setVisible(False)

        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.lorr = QtWidgets.QButtonGroup(Form)
        self.lorr.setObjectName("lorr")

        self.radioButton = QtWidgets.QRadioButton(self.widget)
        self.radioButton.setObjectName("radioButton")
        self.lorr.addButton(self.radioButton)
        self.verticalLayout.addWidget(self.radioButton)

        self.radioButton_2 = QtWidgets.QRadioButton(self.widget)
        self.radioButton_2.setObjectName("radioButton_2")
        self.lorr.addButton(self.radioButton_2)
        self.verticalLayout.addWidget(self.radioButton_2)

        ### label4 MTS command ###
        self.label4 = QtWidgets.QTextBrowser(Form)
        self.label4.setGeometry(QtCore.QRect(840, 230, 400, 441))
        self.label4.setObjectName("textBrowser_2")
        self.label4.setStyleSheet('background-color:#f5f5f5')

        ### label6 ~ label8 current_velocity ###
        self.label6 = QtWidgets.QLabel(Form)
        self.label6.setGeometry(QtCore.QRect(200, 690, 130, 25))
        self.label6.setObjectName("label6")
        self.label6.setText('current_velocity')

        self.label7 = QtWidgets.QLabel(Form)
        self.label7.setGeometry(QtCore.QRect(350, 690, 50, 25))
        self.label7.setObjectName("label7")

        self.label8 = QtWidgets.QLabel(Form)
        self.label8.setGeometry(QtCore.QRect(410, 690, 40, 25))
        self.label8.setObjectName("label8")
        # self.label8.setStylesheet('QLabel { color: red }')
        self.label8.setText('mm/s')

        ### label9 ~ label11 current_position ###
        self.label9 = QtWidgets.QLabel(Form)
        self.label9.setGeometry(QtCore.QRect(200, 725, 120, 25))
        self.label9.setObjectName("label9")
        self.label9.setText('current_position')

        self.label10 = QtWidgets.QLabel(Form)
        self.label10.setGeometry(QtCore.QRect(320, 725, 70, 25))
        self.label10.setObjectName("label10")
        self.label10.setText('(X : 0.0 m')

        self.label11 = QtWidgets.QLabel(Form)
        self.label11.setGeometry(QtCore.QRect(390, 725, 70, 25))
        self.label11.setObjectName("label11")
        self.label11.setText('Y : 0.0 m)')

        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(950, 80, 200, 40))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet('background-color:#ff4500')

        self.pushButton2 = QtWidgets.QPushButton(Form)
        self.pushButton2.setGeometry(QtCore.QRect(920, 690, 150, 25))
        self.pushButton2.setObjectName("pushButton2")
        self.pushButton2.setStyleSheet('background-color:#87ceeb')

        self.pushButton3 = QtWidgets.QPushButton(Form)
        self.pushButton3.setGeometry(QtCore.QRect(1100, 690, 100, 25))
        self.pushButton3.setObjectName("pushButton3")

        self.pushButton4 = QtWidgets.QPushButton(Form)
        self.pushButton4.setGeometry(QtCore.QRect(500, 690, 150, 25))
        self.pushButton4.setObjectName("pushButton4")
        self.pushButton4.setStyleSheet('background-color:#daa520')

        self.imageLabel = QtWidgets.QLabel(Form)
        self.imageLabel.move(200,220)
        self.imageLabel.setMouseTracking(True)
        # self.init_drawing(img)

        self.lineEdit.setVisible(False)
        self.lineEdit_2.setVisible(False)
        self.lineEdit_3.setVisible(False)
        self.label.setVisible(False)
        self.label2.setVisible(False)
        self.label3.setVisible(False)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Create Mode"))
        self.radioButton.setText(_translate("Form", "left"))
        self.radioButton_2.setText(_translate("Form", "right"))
        self.pushButton.setText(_translate("Form", "Add"))
        self.pushButton2.setText(_translate("Form", "Save"))
        self.pushButton3.setText(_translate("Form", "Reset"))
        self.pushButton4.setText(_translate("Form", "Loading Map"))
        self.pushButton5.setText(_translate("Form", "Plese select Motion Script File"))


    def onActivated(self, text):
        self.cmd_text = text

        self.lineEdit.setVisible(False)
        self.lineEdit_2.setVisible(False)
        self.lineEdit_3.setVisible(False)
        self.widget.setVisible(False)
        self.label.setVisible(False)
        self.label2.setVisible(False)
        self.label3.setVisible(False)
        self.label5.setVisible(False)
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_3.setText("")
        self.pushButton5.setVisible(False)

        if text == "acceleration":
            self.lineEdit.setVisible(True)
            self.lineEdit_2.setVisible(True)
            self.label.setText('acceleration value (mm^2/s)')
            self.label2.setText('target speed (mm/s)')
            self.label.setVisible(True)
            self.label2.setVisible(True)

        elif text == "forward":
            self.lineEdit.setVisible(True)
            self.lineEdit_2.setVisible(True)
            self.label.setText('velocity value (mm/s)')
            self.label2.setText('target distance (mm)')
            self.label.setVisible(True)
            self.label2.setVisible(True)
        elif text == "rotation":
            self.lineEdit.setVisible(True)
            self.lineEdit_2.setVisible(True)
            self.label.setText('angular value (rad/s)')
            self.label2.setText('target angle (degree)')
            self.label.setVisible(True)
            self.label2.setVisible(True)
        elif text == "turning":
            self.lineEdit.setVisible(True)
            self.lineEdit_2.setVisible(True)
            self.lineEdit_3.setVisible(True)
            self.widget.setVisible(True)
            self.label.setText('velocity value (mm/s)')
            self.label2.setText('radius (mm)')
            self.label3.setText('target distance (mm)')
            self.label.setVisible(True)
            self.label2.setVisible(True)
            self.label3.setVisible(True)
        elif text == "pan":
            self.lineEdit.setVisible(True)
            self.label.setText('angle (degree)')
            self.label.setVisible(True)
        elif text == "tilt":
            self.lineEdit.setVisible(True)
            self.label.setText('angle (degree)')
            self.label.setVisible(True)
        elif text == "yaw":
            self.lineEdit.setVisible(True)
            self.label.setText('angle (degree)')
            self.label.setVisible(True)
        elif text == "pause":
            self.lineEdit.setVisible(True)
            self.label.setText('pause time (sec)')
            self.label.setVisible(True)
        elif text == "stop":
            pass
        elif text == "slowstop":
            self.lineEdit.setVisible(True)
            self.label.setText('decceleration value (mm^2/s)')
            self.label.setVisible(True)
        elif text == "detect":
            self.lineEdit.setVisible(True)
            self.label.setText('distance (m)')
            self.label.setVisible(True)
        elif text == "e":
            # self.lineEdit.setVisible(True)
            self.pushButton5.setVisible(True)
        elif text == "end":
            pass
        else:
            pass
