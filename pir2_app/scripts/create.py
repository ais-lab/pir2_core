# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_create(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(876, 696)

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(200, 40, 67, 17))
        self.label.setObjectName("label")

        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(111, 155, 150, 25))
        self.comboBox.setObjectName("comboBox")
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
        # self.combo.setGeometry(QtCore.QRect(300, 300, 300, 200))
        self.comboBox.activated[str].connect(self.onActivated)

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(303, 155, 142, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setVisible(True)

        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(481, 155, 142, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setVisible(True)

        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(659, 155, 142, 25))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setVisible(False)

        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(837, 141, 60, 54))
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

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.radioButton.setText(_translate("Form", "left"))
        self.radioButton_2.setText(_translate("Form", "right"))

    def onActivated(self, text):

        self.lineEdit.setVisible(False)
        self.lineEdit_2.setVisible(False)
        self.lineEdit_3.setVisible(False)
        self.widget.setVisible(False)

        if text == "acceleration":
            self.lineEdit.setVisible(True)
            self.lineEdit_2.setVisible(True)
        elif text == "forward":
            self.lineEdit.setVisible(True)
            self.lineEdit_2.setVisible(True)
        elif text == "rotation":
            self.lineEdit.setVisible(True)
            self.lineEdit_2.setVisible(True)
        elif text == "turning":
            self.lineEdit.setVisible(True)
            self.lineEdit_2.setVisible(True)
            self.lineEdit_3.setVisible(True)
            self.widget.setVisible(True)
        elif text == "pause":
            self.lineEdit.setVisible(True)
        elif text == "stop":
            pass
        elif text == "slowstop":
            self.lineEdit.setVisible(True)
        elif text == "detect":
            self.lineEdit.setVisible(True)
        elif text == "e":
            self.lineEdit.setVisible(True)
        elif text == "end":
            pass
        else:
            pass
