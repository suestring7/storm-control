# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prism2-misc.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(322, 341)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(322, 341))
        Dialog.setMaximumSize(QtCore.QSize(322, 341))
        self.okButton = QtWidgets.QPushButton(Dialog)
        self.okButton.setGeometry(QtCore.QRect(240, 310, 75, 24))
        self.okButton.setObjectName("okButton")
        self.TIRFgroupBox = QtWidgets.QGroupBox(Dialog)
        self.TIRFgroupBox.setGeometry(QtCore.QRect(10, 10, 301, 291))
        self.TIRFgroupBox.setObjectName("TIRFgroupBox")
        self.positionText = QtWidgets.QLabel(self.TIRFgroupBox)
        self.positionText.setGeometry(QtCore.QRect(230, 40, 46, 14))
        self.positionText.setText("")
        self.positionText.setObjectName("positionText")
        self.EPIButton = QtWidgets.QPushButton(self.TIRFgroupBox)
        self.EPIButton.setGeometry(QtCore.QRect(10, 260, 61, 24))
        self.EPIButton.setObjectName("EPIButton")
        self.TIRFButton = QtWidgets.QPushButton(self.TIRFgroupBox)
        self.TIRFButton.setGeometry(QtCore.QRect(230, 260, 61, 24))
        self.TIRFButton.setObjectName("TIRFButton")
        self.motorWidget = QtWidgets.QWidget(self.TIRFgroupBox)
        self.motorWidget.setGeometry(QtCore.QRect(10, 20, 281, 231))
        self.motorWidget.setObjectName("motorWidget")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "HAL-4000 Miscellaneous Controls"))
        self.okButton.setText(_translate("Dialog", "Ok"))
        self.TIRFgroupBox.setTitle(_translate("Dialog", "TIRF Control"))
        self.EPIButton.setText(_translate("Dialog", "EPI"))
        self.TIRFButton.setText(_translate("Dialog", "TIRF"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

