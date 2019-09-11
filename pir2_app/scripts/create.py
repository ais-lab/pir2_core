# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import rospkg
import cv2

class Ui_create(object):
    def setupUi(self, Form):
        Form.setObjectName("Create Mode")
        Form.resize(1366, 768)

        self.cmd_text = ""

        # self.groupBox = QtWidgets.QGroupBox(Form)
        # self.groupBox.setGeometry(QtCore.QRect(690, 20, 661, 701))
        # self.groupBox.setObjectName("groupBox")

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(200, 40, 67, 17))
        self.label.setObjectName("label")

        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(91, 135, 150, 25))
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
        # self.combo.setGeometry(QtCore.QRect(300, 300, 300, 200))
        self.comboBox.activated[str].connect(self.onActivated)

        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(283, 135, 142, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setVisible(True)

        self.pushButton5 = QtWidgets.QPushButton(Form)
        self.pushButton5.setGeometry(QtCore.QRect(283, 135, 271, 25))
        self.pushButton5.setObjectName("pushButton")
        self.pushButton5.setVisible(False)

        self.label5 = QtWidgets.QLabel(Form)
        self.label5.setGeometry(QtCore.QRect(574, 135, 141, 25))
        self.label5.setObjectName("label")
        # self.label5.setStyleSheet('color: gray')
        # self.label5.setText('acceleration value')
        self.label5.setVisible(False)

        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(293, 100, 200, 31))
        self.label.setObjectName("label")
        self.label.setText('acceleration value')
        self.label.setStyleSheet('background-color: #c0c0c0	')

        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(461, 135, 142, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setVisible(True)

        self.label2 = QtWidgets.QLabel(Form)
        self.label2.setGeometry(QtCore.QRect(471, 100, 200, 31))
        self.label2.setObjectName("label2")
        self.label2.setText('target speed')
        self.label2.setStyleSheet('background-color: #c0c0c0')

        self.lineEdit_3 = QtWidgets.QLineEdit(Form)
        self.lineEdit_3.setGeometry(QtCore.QRect(639, 135, 142, 25))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setVisible(False)

        self.label3 = QtWidgets.QLabel(Form)
        self.label3.setGeometry(QtCore.QRect(649, 100, 200, 31))
        self.label3.setObjectName("label3")
        # self.label3.setText('target speed')
        self.label3.setStyleSheet('background-color: #c0c0c0')
        self.label3.setVisible(False)

        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(817, 141, 60, 54))
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

        self.label4 = QtWidgets.QTextBrowser(Form)
        self.label4.setGeometry(QtCore.QRect(911, 230, 400, 441))
        self.label4.setObjectName("textBrowser_2")

        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(931, 135, 120, 25))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet('background-color:#ff4500')

        self.pushButton2 = QtWidgets.QPushButton(Form)
        self.pushButton2.setGeometry(QtCore.QRect(1120, 135, 120, 25))
        self.pushButton2.setObjectName("pushButton")
        self.pushButton2.setStyleSheet('background-color:#87ceeb')

        self.pushButton3 = QtWidgets.QPushButton(Form)
        self.pushButton3.setGeometry(QtCore.QRect(1211, 200, 100, 25))
        self.pushButton3.setObjectName("pushButton")

        path = rospkg.RosPack().get_path('pir2_navigation') + '/map/map.pgm'

        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height = img.shape[0]
        width = img.shape[1]
        img = img[(height/2)-100:(height/2)+100 , (width/2)-100:(width/2)+100]
        img = cv2.resize(img , (int(200*2.3), int(200*2.3)))
        qimg = QtGui.QImage(img.data, img.shape[1], img.shape[0], QtGui.QImage.Format_RGB888)
        # path = rospkg.RosPack().get_path('pir2_navigation') + '/map/map.pgm'
        self.imageLabel = QtWidgets.QLabel(Form)
        self.imageLabel.setPixmap(QtGui.QPixmap.fromImage(qimg))
        self.imageLabel.move(200,220)
        # self.imageLabel.setGeometry(QtCore.QRect(200, 220, int(200*2.3), int(200*2.3)))

        self.retranslateUi(Form)
        self.pushButton.clicked.connect(Form.adding)
        self.pushButton2.clicked.connect(Form.saving)
        self.pushButton3.clicked.connect(Form.reset)
        self.pushButton5.clicked.connect(Form.select)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Create Mode"))
        self.radioButton.setText(_translate("Form", "left"))
        self.radioButton_2.setText(_translate("Form", "right"))
        self.pushButton.setText(_translate("Form", "Add"))
        self.pushButton2.setText(_translate("Form", "Save"))
        self.pushButton3.setText(_translate("Form", "Reset"))
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
            self.pushButton5.setVisible(True)
        elif text == "end":
            pass
        else:
            pass
