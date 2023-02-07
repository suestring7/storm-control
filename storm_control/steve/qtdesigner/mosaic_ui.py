# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mosaic.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(902, 846)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.mosaicFrame = QtWidgets.QFrame(Form)
        self.mosaicFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mosaicFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mosaicFrame.setObjectName("mosaicFrame")
        self.horizontalLayout_2.addWidget(self.mosaicFrame)
        self.widget = QtWidgets.QWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setMinimumSize(QtCore.QSize(0, 0))
        self.widget.setMaximumSize(QtCore.QSize(16777215, 100000))
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.positionsGroupBox = QtWidgets.QGroupBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.positionsGroupBox.sizePolicy().hasHeightForWidth())
        self.positionsGroupBox.setSizePolicy(sizePolicy)
        self.positionsGroupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.positionsGroupBox.setMaximumSize(QtCore.QSize(10000, 10000))
        self.positionsGroupBox.setObjectName("positionsGroupBox")
        self.verticalLayout_2.addWidget(self.positionsGroupBox)
        self.tilesGroupBox_2 = QtWidgets.QGroupBox(self.widget)
        self.tilesGroupBox_2.setMinimumSize(QtCore.QSize(300, 150))
        self.tilesGroupBox_2.setMaximumSize(QtCore.QSize(300, 300))
        self.tilesGroupBox_2.setObjectName("tilesGroupBox_2")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.tilesGroupBox_2)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.startingPositionLabel_4 = QtWidgets.QLabel(self.tilesGroupBox_2)
        font = QtGui.QFont()
        font.setBold(False)
        self.startingPositionLabel_4.setFont(font)
        self.startingPositionLabel_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.startingPositionLabel_4.setObjectName("startingPositionLabel_4")
        self.verticalLayout_6.addWidget(self.startingPositionLabel_4)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.xPosLabel_4 = QtWidgets.QLabel(self.tilesGroupBox_2)
        self.xPosLabel_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.xPosLabel_4.setObjectName("xPosLabel_4")
        self.horizontalLayout_20.addWidget(self.xPosLabel_4)
        self.posCenterSpinX = QtWidgets.QDoubleSpinBox(self.tilesGroupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.posCenterSpinX.sizePolicy().hasHeightForWidth())
        self.posCenterSpinX.setSizePolicy(sizePolicy)
        self.posCenterSpinX.setMinimum(-5000000.0)
        self.posCenterSpinX.setMaximum(5000000.0)
        self.posCenterSpinX.setObjectName("posCenterSpinX")
        self.horizontalLayout_20.addWidget(self.posCenterSpinX)
        self.verticalLayout_6.addLayout(self.horizontalLayout_20)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.yPosLabel_4 = QtWidgets.QLabel(self.tilesGroupBox_2)
        self.yPosLabel_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.yPosLabel_4.setObjectName("yPosLabel_4")
        self.horizontalLayout_21.addWidget(self.yPosLabel_4)
        self.posCenterSpinY = QtWidgets.QDoubleSpinBox(self.tilesGroupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.posCenterSpinY.sizePolicy().hasHeightForWidth())
        self.posCenterSpinY.setSizePolicy(sizePolicy)
        self.posCenterSpinY.setMinimum(-5000000.0)
        self.posCenterSpinY.setMaximum(5000000.0)
        self.posCenterSpinY.setObjectName("posCenterSpinY")
        self.horizontalLayout_21.addWidget(self.posCenterSpinY)
        self.verticalLayout_6.addLayout(self.horizontalLayout_21)
        self.horizontalLayout_19.addLayout(self.verticalLayout_6)
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.gridDimLabel_3 = QtWidgets.QLabel(self.tilesGroupBox_2)
        font = QtGui.QFont()
        font.setBold(False)
        self.gridDimLabel_3.setFont(font)
        self.gridDimLabel_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.gridDimLabel_3.setObjectName("gridDimLabel_3")
        self.verticalLayout_12.addWidget(self.gridDimLabel_3)
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.numXLabel_3 = QtWidgets.QLabel(self.tilesGroupBox_2)
        self.numXLabel_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.numXLabel_3.setObjectName("numXLabel_3")
        self.horizontalLayout_22.addWidget(self.numXLabel_3)
        self.posGridSpinX = QtWidgets.QSpinBox(self.tilesGroupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.posGridSpinX.sizePolicy().hasHeightForWidth())
        self.posGridSpinX.setSizePolicy(sizePolicy)
        self.posGridSpinX.setMinimum(1)
        self.posGridSpinX.setSingleStep(2)
        self.posGridSpinX.setProperty("value", 5)
        self.posGridSpinX.setObjectName("posGridSpinX")
        self.horizontalLayout_22.addWidget(self.posGridSpinX)
        self.verticalLayout_12.addLayout(self.horizontalLayout_22)
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        self.numYLabel_3 = QtWidgets.QLabel(self.tilesGroupBox_2)
        self.numYLabel_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.numYLabel_3.setObjectName("numYLabel_3")
        self.horizontalLayout_23.addWidget(self.numYLabel_3)
        self.posGridSpinY = QtWidgets.QSpinBox(self.tilesGroupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.posGridSpinY.sizePolicy().hasHeightForWidth())
        self.posGridSpinY.setSizePolicy(sizePolicy)
        self.posGridSpinY.setMinimum(1)
        self.posGridSpinY.setSingleStep(2)
        self.posGridSpinY.setProperty("value", 5)
        self.posGridSpinY.setObjectName("posGridSpinY")
        self.horizontalLayout_23.addWidget(self.posGridSpinY)
        self.verticalLayout_12.addLayout(self.horizontalLayout_23)
        self.horizontalLayout_19.addLayout(self.verticalLayout_12)
        self.verticalLayout_11.addLayout(self.horizontalLayout_19)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.tilesGroupBox_2)
        self.label.setObjectName("label")
        self.horizontalLayout_11.addWidget(self.label)
        self.positionGridSpacing = QtWidgets.QDoubleSpinBox(self.tilesGroupBox_2)
        self.positionGridSpacing.setMaximum(2000.0)
        self.positionGridSpacing.setProperty("value", 200.0)
        self.positionGridSpacing.setObjectName("positionGridSpacing")
        self.horizontalLayout_11.addWidget(self.positionGridSpacing)
        self.verticalLayout_11.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.getStagePosPosButton = QtWidgets.QPushButton(self.tilesGroupBox_2)
        self.getStagePosPosButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.getStagePosPosButton.setObjectName("getStagePosPosButton")
        self.horizontalLayout_24.addWidget(self.getStagePosPosButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_24.addItem(spacerItem1)
        self.genPosButton = QtWidgets.QPushButton(self.tilesGroupBox_2)
        self.genPosButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.genPosButton.setObjectName("genPosButton")
        self.horizontalLayout_24.addWidget(self.genPosButton)
        self.verticalLayout_11.addLayout(self.horizontalLayout_24)
        self.verticalLayout_2.addWidget(self.tilesGroupBox_2)
        self.tilesGroupBox = QtWidgets.QGroupBox(self.widget)
        self.tilesGroupBox.setMinimumSize(QtCore.QSize(300, 150))
        self.tilesGroupBox.setMaximumSize(QtCore.QSize(300, 300))
        self.tilesGroupBox.setObjectName("tilesGroupBox")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tilesGroupBox)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.startingPositionLabel = QtWidgets.QLabel(self.tilesGroupBox)
        font = QtGui.QFont()
        font.setBold(False)
        self.startingPositionLabel.setFont(font)
        self.startingPositionLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.startingPositionLabel.setObjectName("startingPositionLabel")
        self.verticalLayout_3.addWidget(self.startingPositionLabel)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.xPosLabel = QtWidgets.QLabel(self.tilesGroupBox)
        self.xPosLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.xPosLabel.setObjectName("xPosLabel")
        self.horizontalLayout_4.addWidget(self.xPosLabel)
        self.xStartPosSpinBox = QtWidgets.QDoubleSpinBox(self.tilesGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xStartPosSpinBox.sizePolicy().hasHeightForWidth())
        self.xStartPosSpinBox.setSizePolicy(sizePolicy)
        self.xStartPosSpinBox.setMinimum(-5000000.0)
        self.xStartPosSpinBox.setMaximum(5000000.0)
        self.xStartPosSpinBox.setObjectName("xStartPosSpinBox")
        self.horizontalLayout_4.addWidget(self.xStartPosSpinBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.yPosLabel = QtWidgets.QLabel(self.tilesGroupBox)
        self.yPosLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.yPosLabel.setObjectName("yPosLabel")
        self.horizontalLayout_6.addWidget(self.yPosLabel)
        self.yStartPosSpinBox = QtWidgets.QDoubleSpinBox(self.tilesGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.yStartPosSpinBox.sizePolicy().hasHeightForWidth())
        self.yStartPosSpinBox.setSizePolicy(sizePolicy)
        self.yStartPosSpinBox.setMinimum(-5000000.0)
        self.yStartPosSpinBox.setMaximum(5000000.0)
        self.yStartPosSpinBox.setObjectName("yStartPosSpinBox")
        self.horizontalLayout_6.addWidget(self.yStartPosSpinBox)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_8.addLayout(self.verticalLayout_3)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.gridDimLabel = QtWidgets.QLabel(self.tilesGroupBox)
        font = QtGui.QFont()
        font.setBold(False)
        self.gridDimLabel.setFont(font)
        self.gridDimLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.gridDimLabel.setObjectName("gridDimLabel")
        self.verticalLayout_7.addWidget(self.gridDimLabel)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.numXLabel = QtWidgets.QLabel(self.tilesGroupBox)
        self.numXLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.numXLabel.setObjectName("numXLabel")
        self.horizontalLayout_5.addWidget(self.numXLabel)
        self.xSpinBox = QtWidgets.QSpinBox(self.tilesGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.xSpinBox.sizePolicy().hasHeightForWidth())
        self.xSpinBox.setSizePolicy(sizePolicy)
        self.xSpinBox.setMinimum(1)
        self.xSpinBox.setSingleStep(2)
        self.xSpinBox.setProperty("value", 5)
        self.xSpinBox.setObjectName("xSpinBox")
        self.horizontalLayout_5.addWidget(self.xSpinBox)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.numYLabel = QtWidgets.QLabel(self.tilesGroupBox)
        self.numYLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.numYLabel.setObjectName("numYLabel")
        self.horizontalLayout_7.addWidget(self.numYLabel)
        self.ySpinBox = QtWidgets.QSpinBox(self.tilesGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ySpinBox.sizePolicy().hasHeightForWidth())
        self.ySpinBox.setSizePolicy(sizePolicy)
        self.ySpinBox.setMinimum(1)
        self.ySpinBox.setSingleStep(2)
        self.ySpinBox.setProperty("value", 3)
        self.ySpinBox.setObjectName("ySpinBox")
        self.horizontalLayout_7.addWidget(self.ySpinBox)
        self.verticalLayout_7.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8.addLayout(self.verticalLayout_7)
        self.verticalLayout_8.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.getStagePosButton = QtWidgets.QPushButton(self.tilesGroupBox)
        self.getStagePosButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.getStagePosButton.setObjectName("getStagePosButton")
        self.horizontalLayout_10.addWidget(self.getStagePosButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem2)
        self.imageGridButton = QtWidgets.QPushButton(self.tilesGroupBox)
        self.imageGridButton.setMaximumSize(QtCore.QSize(150, 16777215))
        self.imageGridButton.setObjectName("imageGridButton")
        self.horizontalLayout_10.addWidget(self.imageGridButton)
        self.verticalLayout_8.addLayout(self.horizontalLayout_10)
        self.verticalLayout_2.addWidget(self.tilesGroupBox)
        self.objectivesGroupBox = ObjectivesGroupBox(self.widget)
        self.objectivesGroupBox.setMinimumSize(QtCore.QSize(250, 50))
        self.objectivesGroupBox.setMaximumSize(QtCore.QSize(300, 300))
        self.objectivesGroupBox.setObjectName("objectivesGroupBox")
        self.verticalLayout_2.addWidget(self.objectivesGroupBox)
        self.miscGroupBox = QtWidgets.QGroupBox(self.widget)
        self.miscGroupBox.setMinimumSize(QtCore.QSize(0, 20))
        self.miscGroupBox.setObjectName("miscGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.miscGroupBox)
        self.verticalLayout.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.trackStageCheckBox = QtWidgets.QCheckBox(self.miscGroupBox)
        self.trackStageCheckBox.setObjectName("trackStageCheckBox")
        self.horizontalLayout.addWidget(self.trackStageCheckBox)
        self.scaleLabel = QtWidgets.QLabel(self.miscGroupBox)
        self.scaleLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.scaleLabel.setObjectName("scaleLabel")
        self.horizontalLayout.addWidget(self.scaleLabel)
        self.scaleLineEdit = QtWidgets.QLineEdit(self.miscGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scaleLineEdit.sizePolicy().hasHeightForWidth())
        self.scaleLineEdit.setSizePolicy(sizePolicy)
        self.scaleLineEdit.setMaximumSize(QtCore.QSize(100, 16777215))
        self.scaleLineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.scaleLineEdit.setObjectName("scaleLineEdit")
        self.horizontalLayout.addWidget(self.scaleLineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.cursorPosition = QtWidgets.QLabel(self.miscGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cursorPosition.sizePolicy().hasHeightForWidth())
        self.cursorPosition.setSizePolicy(sizePolicy)
        self.cursorPosition.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.cursorPosition.setObjectName("cursorPosition")
        self.horizontalLayout_9.addWidget(self.cursorPosition)
        self.mosaicLabel = QtWidgets.QLabel(self.miscGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mosaicLabel.sizePolicy().hasHeightForWidth())
        self.mosaicLabel.setSizePolicy(sizePolicy)
        self.mosaicLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.mosaicLabel.setObjectName("mosaicLabel")
        self.horizontalLayout_9.addWidget(self.mosaicLabel)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.verticalLayout_2.addWidget(self.miscGroupBox)
        self.horizontalLayout_2.addWidget(self.widget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.positionsGroupBox.setTitle(_translate("Form", "Positions"))
        self.tilesGroupBox_2.setTitle(_translate("Form", "Generate Positions"))
        self.startingPositionLabel_4.setText(_translate("Form", "Center"))
        self.xPosLabel_4.setText(_translate("Form", "X:"))
        self.yPosLabel_4.setText(_translate("Form", "Y:"))
        self.gridDimLabel_3.setText(_translate("Form", "Grid Size"))
        self.numXLabel_3.setText(_translate("Form", "# X:"))
        self.numYLabel_3.setText(_translate("Form", "# Y:"))
        self.label.setText(_translate("Form", "Spacing"))
        self.getStagePosPosButton.setText(_translate("Form", "Get Stage Position"))
        self.genPosButton.setText(_translate("Form", "Create"))
        self.tilesGroupBox.setTitle(_translate("Form", "Tile Settings"))
        self.startingPositionLabel.setText(_translate("Form", "Center"))
        self.xPosLabel.setText(_translate("Form", "X:"))
        self.yPosLabel.setText(_translate("Form", "Y:"))
        self.gridDimLabel.setText(_translate("Form", "Grid Size"))
        self.numXLabel.setText(_translate("Form", "# X:"))
        self.numYLabel.setText(_translate("Form", "# Y:"))
        self.getStagePosButton.setText(_translate("Form", "Get Stage Position"))
        self.imageGridButton.setText(_translate("Form", "Acquire"))
        self.objectivesGroupBox.setTitle(_translate("Form", "Objective Settings"))
        self.miscGroupBox.setTitle(_translate("Form", "Misc"))
        self.trackStageCheckBox.setText(_translate("Form", "Track Stage"))
        self.scaleLabel.setText(_translate("Form", "Scale:"))
        self.scaleLineEdit.setText(_translate("Form", "1.0"))
        self.cursorPosition.setText(_translate("Form", "Cursor:"))
        self.mosaicLabel.setText(_translate("Form", "TextLabel"))
from storm_control.steve.objectives import ObjectivesGroupBox


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
