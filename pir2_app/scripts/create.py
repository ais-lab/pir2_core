# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_create(object):
    def setupUi(self, Form):
        Form.setObjectName("Create Mode")
        Form.resize(1366, 768)

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

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(313, 120, 200, 31))
        self.label.setObjectName("label")
        self.label.setText('acceleration value')
        self.label.setStyleSheet('background-color: #c0c0c0	')

        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(481, 155, 142, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setVisible(True)

        self.label2 = QtWidgets.QLabel(Form)
        self.label2.setGeometry(QtCore.QRect(491, 120, 200, 31))
        self.label2.setObjectName("label2")
        self.label2.setText('target speed')
        self.label2.setStyleSheet('background-color: #c0c0c0')

        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(659, 155, 142, 25))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setVisible(False)

        self.label3 = QtWidgets.QLabel(Form)
        self.label3.setGeometry(QtCore.QRect(669, 120, 200, 31))
        self.label3.setObjectName("label3")
        # self.label3.setText('target speed')
        self.label3.setStyleSheet('background-color: #c0c0c0')
        self.label3.setVisible(False)

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

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(951, 155, 120, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet('background-color:#ff4500')

        self.pushButton2 = QtWidgets.QPushButton(Form)
        self.pushButton2.setGeometry(QtCore.QRect(1140, 155, 120, 25))
        self.pushButton2.setObjectName("pushButton")
        self.pushButton2.setStyleSheet('background-color:#87ceeb')

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(Form.adding)
        self.pushButton2.clicked.connect(Form.saving)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Create Mode"))
        self.radioButton.setText(_translate("Form", "left"))
        self.radioButton_2.setText(_translate("Form", "right"))
        self.pushButton.setText(_translate("Form", "Add"))
        self.pushButton2.setText(_translate("Form", "Save"))

    def onActivated(self, text):

        self.lineEdit.setVisible(False)
        self.lineEdit_2.setVisible(False)
        self.lineEdit_3.setVisible(False)
        self.widget.setVisible(False)
        self.label.setVisible(False)
        self.label2.setVisible(False)
        self.label3.setVisible(False)

        if text == "acceleration":
            self.lineEdit.setVisible(True)
            self.lineEdit_2.setVisible(True)
            self.label.setText('acceleration value')
            self.label2.setText('target speed')
            self.label.setVisible(True)
            self.label2.setVisible(True)

        elif text == "forward":
            self.lineEdit.setVisible(True)
            self.lineEdit_2.setVisible(True)
            self.label.setText('velocity value')
            self.label2.setText('target distance')
            self.label.setVisible(True)
            self.label2.setVisible(True)
        elif text == "rotation":
            self.lineEdit.setVisible(True)
            self.lineEdit_2.setVisible(True)
            self.label.setText('angular value')
            self.label2.setText('target angle')
            self.label.setVisible(True)
            self.label2.setVisible(True)
        elif text == "turning":
            self.lineEdit.setVisible(True)
            self.lineEdit_2.setVisible(True)
            self.lineEdit_3.setVisible(True)
            self.widget.setVisible(True)
            self.label.setText('velocity value')
            self.label2.setText('radius')
            self.label3.setText('target distance')
            self.label.setVisible(True)
            self.label2.setVisible(True)
            self.label3.setVisible(True)
        elif text == "pause":
            self.lineEdit.setVisible(True)
            self.label.setText('pause time')
            self.label.setVisible(True)
        elif text == "stop":
            pass
        elif text == "slowstop":
            self.lineEdit.setVisible(True)
            self.label.setText('decceleration value')
            self.label.setVisible(True)
        elif text == "detect":
            self.lineEdit.setVisible(True)
            self.label.setText('distance')
            self.label.setVisible(True)
        elif text == "e":
            # self.lineEdit.setVisible(True)
            pass
        elif text == "end":
            pass
        else:
            pass
