# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'phaseretrieval.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ProjectionCalculator(object):
    def setupUi(self, ProjectionCalculator):
        ProjectionCalculator.setObjectName(_fromUtf8("ProjectionCalculator"))
        ProjectionCalculator.resize(808, 482)
        self.centralwidget = QtGui.QWidget(ProjectionCalculator)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.layoutWidget = QtGui.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(9, 9, 781, 431))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_figure = QtGui.QVBoxLayout()
        self.verticalLayout_figure.setObjectName(_fromUtf8("verticalLayout_figure"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.verticalLayout_figure.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout_figure, 0, 0, 1, 4)
        self.verticalSlider_BGlevel = QtGui.QSlider(self.layoutWidget)
        self.verticalSlider_BGlevel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.verticalSlider_BGlevel.setMaximum(3600)
        self.verticalSlider_BGlevel.setSingleStep(1)
        self.verticalSlider_BGlevel.setPageStep(100)
        self.verticalSlider_BGlevel.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_BGlevel.setTickPosition(QtGui.QSlider.NoTicks)
        self.verticalSlider_BGlevel.setTickInterval(1)
        self.verticalSlider_BGlevel.setObjectName(_fromUtf8("verticalSlider_BGlevel"))
        self.gridLayout.addWidget(self.verticalSlider_BGlevel, 0, 4, 1, 1)
        self.verticalSlider_satThresh = QtGui.QSlider(self.layoutWidget)
        self.verticalSlider_satThresh.setMaximum(3600)
        self.verticalSlider_satThresh.setSingleStep(10)
        self.verticalSlider_satThresh.setPageStep(100)
        self.verticalSlider_satThresh.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_satThresh.setObjectName(_fromUtf8("verticalSlider_satThresh"))
        self.gridLayout.addWidget(self.verticalSlider_satThresh, 0, 5, 1, 1)
        self.lineEdit_BGlevel = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_BGlevel.setObjectName(_fromUtf8("lineEdit_BGlevel"))
        self.gridLayout.addWidget(self.lineEdit_BGlevel, 1, 0, 1, 3)
        self.lineEdit_satThresh = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_satThresh.setObjectName(_fromUtf8("lineEdit_satThresh"))
        self.gridLayout.addWidget(self.lineEdit_satThresh, 1, 3, 1, 2)
        self.lbl_BGlevel = QtGui.QLabel(self.layoutWidget)
        self.lbl_BGlevel.setObjectName(_fromUtf8("lbl_BGlevel"))
        self.gridLayout.addWidget(self.lbl_BGlevel, 2, 0, 1, 2)
        self.lbl_satThresh = QtGui.QLabel(self.layoutWidget)
        self.lbl_satThresh.setObjectName(_fromUtf8("lbl_satThresh"))
        self.gridLayout.addWidget(self.lbl_satThresh, 2, 3, 1, 2)
        self.lbl_diffpat = QtGui.QLabel(self.layoutWidget)
        self.lbl_diffpat.setObjectName(_fromUtf8("lbl_diffpat"))
        self.gridLayout.addWidget(self.lbl_diffpat, 3, 0, 1, 2)
        self.lineEdit_diffpatFile = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_diffpatFile.setObjectName(_fromUtf8("lineEdit_diffpatFile"))
        self.gridLayout.addWidget(self.lineEdit_diffpatFile, 3, 2, 1, 2)
        self.btn_selectDiffpat = QtGui.QPushButton(self.layoutWidget)
        self.btn_selectDiffpat.setObjectName(_fromUtf8("btn_selectDiffpat"))
        self.gridLayout.addWidget(self.btn_selectDiffpat, 3, 4, 1, 1)
        self.line = QtGui.QFrame(self.layoutWidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 4, 0, 2, 5)
        self.btn_go = QtGui.QPushButton(self.layoutWidget)
        self.btn_go.setObjectName(_fromUtf8("btn_go"))
        self.gridLayout.addWidget(self.btn_go, 5, 1, 1, 3)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 3, 4)
        self.checkBox_takeSqrt = QtGui.QCheckBox(self.layoutWidget)
        self.checkBox_takeSqrt.setEnabled(True)
        self.checkBox_takeSqrt.setChecked(False)
        self.checkBox_takeSqrt.setObjectName(_fromUtf8("checkBox_takeSqrt"))
        self.gridLayout_2.addWidget(self.checkBox_takeSqrt, 1, 3, 1, 1)
        self.btn_refineCenter = QtGui.QPushButton(self.layoutWidget)
        self.btn_refineCenter.setObjectName(_fromUtf8("btn_refineCenter"))
        self.gridLayout_2.addWidget(self.btn_refineCenter, 2, 2, 1, 2)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.btn_savePattern = QtGui.QPushButton(self.layoutWidget)
        self.btn_savePattern.setObjectName(_fromUtf8("btn_savePattern"))
        self.horizontalLayout_2.addWidget(self.btn_savePattern)
        self.lineEdit_saveFilename = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_saveFilename.setObjectName(_fromUtf8("lineEdit_saveFilename"))
        self.horizontalLayout_2.addWidget(self.lineEdit_saveFilename)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lbl_BGfilename = QtGui.QLabel(self.layoutWidget)
        self.lbl_BGfilename.setObjectName(_fromUtf8("lbl_BGfilename"))
        self.horizontalLayout.addWidget(self.lbl_BGfilename)
        self.btn_BGfilename = QtGui.QPushButton(self.layoutWidget)
        self.btn_BGfilename.setObjectName(_fromUtf8("btn_BGfilename"))
        self.horizontalLayout.addWidget(self.btn_BGfilename)
        self.lineEdit_BGfilename = QtGui.QLineEdit(self.layoutWidget)
        self.lineEdit_BGfilename.setObjectName(_fromUtf8("lineEdit_BGfilename"))
        self.horizontalLayout.addWidget(self.lineEdit_BGfilename)
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 1, 1, 3)
        ProjectionCalculator.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(ProjectionCalculator)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 808, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        ProjectionCalculator.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(ProjectionCalculator)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        ProjectionCalculator.setStatusBar(self.statusbar)

        self.retranslateUi(ProjectionCalculator)
        QtCore.QMetaObject.connectSlotsByName(ProjectionCalculator)
        ProjectionCalculator.setTabOrder(self.lineEdit_BGlevel, self.lineEdit_satThresh)
        ProjectionCalculator.setTabOrder(self.lineEdit_satThresh, self.lineEdit_diffpatFile)
        ProjectionCalculator.setTabOrder(self.lineEdit_diffpatFile, self.btn_selectDiffpat)
        ProjectionCalculator.setTabOrder(self.btn_selectDiffpat, self.btn_go)

    def retranslateUi(self, ProjectionCalculator):
        ProjectionCalculator.setWindowTitle(_translate("ProjectionCalculator", "MainWindow", None))
        self.lbl_BGlevel.setText(_translate("ProjectionCalculator", "BG Level", None))
        self.lbl_satThresh.setText(_translate("ProjectionCalculator", "Saturation Threshold", None))
        self.lbl_diffpat.setText(_translate("ProjectionCalculator", "Diffraction Pattern Filename", None))
        self.btn_selectDiffpat.setText(_translate("ProjectionCalculator", "Browse", None))
        self.btn_go.setText(_translate("ProjectionCalculator", "Launch Reconstruction", None))
        self.checkBox_takeSqrt.setText(_translate("ProjectionCalculator", "Take Square Root", None))
        self.btn_refineCenter.setText(_translate("ProjectionCalculator", "Optimize Center", None))
        self.btn_savePattern.setText(_translate("ProjectionCalculator", "Save Pattern", None))
        self.lbl_BGfilename.setText(_translate("ProjectionCalculator", "BG Filename", None))
        self.btn_BGfilename.setText(_translate("ProjectionCalculator", "Browse", None))

