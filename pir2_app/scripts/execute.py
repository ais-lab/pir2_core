# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'execute.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_exe(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1059, 773)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(180, 10, 861, 701))
        self.groupBox.setObjectName("groupBox")

        self.label3 = QtWidgets.QTextBrowser(self.groupBox)
        self.label3.setGeometry(QtCore.QRect(100, 180, 681, 441))
        self.label3.setObjectName("textBrowser_2")

        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(140, 120, 291, 25))
        self.pushButton.setObjectName("pushButton")

        self.label2 = QtWidgets.QLabel(self.groupBox)
        self.label2.setGeometry(QtCore.QRect(460, 120, 256, 31))
        self.label2.setObjectName("textBrowser")

        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 640, 301, 25))
        self.pushButton_2.setObjectName("pushButton_2")

        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(460, 90, 141, 17))
        self.label.setObjectName("label")
        self.label.setStyleSheet('color: gray')

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(Form.select)
        self.pushButton_2.clicked.connect(Form.launch)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Launch program"))
        self.pushButton.setText(_translate("Form", "Plese select Motion Script File"))
        self.pushButton_2.setText(_translate("Form", "Launch"))
        self.label.setText(_translate("Form", "Selected file name"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_exe()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())