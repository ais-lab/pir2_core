# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'top.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_top(object):
    def setupUi(self, Form):
        Form.setObjectName("Menu")
        Form.resize(1012, 727)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(360, 120, 321, 491))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.widget)
        self.pushButton_4.setAutoDefault(False)
        self.pushButton_4.setFlat(False)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(Form.execute)
        self.pushButton_2.clicked.connect(Form.create)
        self.pushButton_3.clicked.connect(Form.slam)
        self.pushButton_4.clicked.connect(QtCore.QCoreApplication.instance().quit)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Menu"))
        self.pushButton.setText(_translate("Form", "Execute "))
        self.pushButton_2.setText(_translate("Form", "Create"))
        self.pushButton_3.setText(_translate("Form", "SLAM"))
        self.pushButton_4.setText(_translate("Form", "Exit"))
