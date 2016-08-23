# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ProjectionCalculator_MainWindow.ui'
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
        ProjectionCalculator.resize(819, 1024)
        self.centralwidget = QtGui.QWidget(ProjectionCalculator)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_3 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.btn_clearModel = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_clearModel.sizePolicy().hasHeightForWidth())
        self.btn_clearModel.setSizePolicy(sizePolicy)
        self.btn_clearModel.setObjectName(_fromUtf8("btn_clearModel"))
        self.horizontalLayout_4.addWidget(self.btn_clearModel)
        self.btn_go = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_go.sizePolicy().hasHeightForWidth())
        self.btn_go.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(179, 179, 179))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(179, 179, 179))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(179, 179, 179))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        self.btn_go.setPalette(palette)
        self.btn_go.setObjectName(_fromUtf8("btn_go"))
        self.horizontalLayout_4.addWidget(self.btn_go)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 2, 0, 1, 4)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.verticalSlider_theta = QtGui.QSlider(self.centralwidget)
        self.verticalSlider_theta.setMaximum(3600)
        self.verticalSlider_theta.setSingleStep(10)
        self.verticalSlider_theta.setPageStep(100)
        self.verticalSlider_theta.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_theta.setObjectName(_fromUtf8("verticalSlider_theta"))
        self.horizontalLayout_6.addWidget(self.verticalSlider_theta)
        self.gridLayout.addLayout(self.horizontalLayout_6, 0, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 2, 0, 1, 1)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.verticalSlider_phi = QtGui.QSlider(self.centralwidget)
        self.verticalSlider_phi.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.verticalSlider_phi.setMaximum(3600)
        self.verticalSlider_phi.setSingleStep(1)
        self.verticalSlider_phi.setPageStep(100)
        self.verticalSlider_phi.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_phi.setTickPosition(QtGui.QSlider.NoTicks)
        self.verticalSlider_phi.setTickInterval(1)
        self.verticalSlider_phi.setObjectName(_fromUtf8("verticalSlider_phi"))
        self.horizontalLayout_5.addWidget(self.verticalSlider_phi)
        self.gridLayout.addLayout(self.horizontalLayout_5, 0, 0, 1, 1)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.verticalSlider_psi = QtGui.QSlider(self.centralwidget)
        self.verticalSlider_psi.setMaximum(360)
        self.verticalSlider_psi.setSingleStep(10)
        self.verticalSlider_psi.setPageStep(100)
        self.verticalSlider_psi.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_psi.setObjectName(_fromUtf8("verticalSlider_psi"))
        self.horizontalLayout_7.addWidget(self.verticalSlider_psi)
        self.gridLayout.addLayout(self.horizontalLayout_7, 0, 2, 1, 1)
        self.lineEdit_psi = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_psi.setObjectName(_fromUtf8("lineEdit_psi"))
        self.gridLayout.addWidget(self.lineEdit_psi, 1, 2, 1, 1)
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 2, 2, 1, 1)
        self.lineEdit_theta = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_theta.setObjectName(_fromUtf8("lineEdit_theta"))
        self.gridLayout.addWidget(self.lineEdit_theta, 1, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 2, 1, 1, 1)
        self.lineEdit_phi = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_phi.sizePolicy().hasHeightForWidth())
        self.lineEdit_phi.setSizePolicy(sizePolicy)
        self.lineEdit_phi.setObjectName(_fromUtf8("lineEdit_phi"))
        self.gridLayout.addWidget(self.lineEdit_phi, 1, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 3, 1, 1)
        self.verticalLayout_figure = QtGui.QVBoxLayout()
        self.verticalLayout_figure.setObjectName(_fromUtf8("verticalLayout_figure"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.verticalLayout_figure.addLayout(self.horizontalLayout_9)
        self.gridLayout_2.addLayout(self.verticalLayout_figure, 0, 1, 1, 2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEdit_modelFile = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_modelFile.setObjectName(_fromUtf8("lineEdit_modelFile"))
        self.horizontalLayout.addWidget(self.lineEdit_modelFile)
        self.btn_selectModel = QtGui.QPushButton(self.centralwidget)
        self.btn_selectModel.setObjectName(_fromUtf8("btn_selectModel"))
        self.horizontalLayout.addWidget(self.btn_selectModel)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 4)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        ProjectionCalculator.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(ProjectionCalculator)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 819, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        ProjectionCalculator.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(ProjectionCalculator)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        ProjectionCalculator.setStatusBar(self.statusbar)

        self.retranslateUi(ProjectionCalculator)
        QtCore.QMetaObject.connectSlotsByName(ProjectionCalculator)
        ProjectionCalculator.setTabOrder(self.lineEdit_phi, self.lineEdit_theta)
        ProjectionCalculator.setTabOrder(self.lineEdit_theta, self.lineEdit_psi)
        ProjectionCalculator.setTabOrder(self.lineEdit_psi, self.lineEdit_modelFile)
        ProjectionCalculator.setTabOrder(self.lineEdit_modelFile, self.btn_selectModel)

    def retranslateUi(self, ProjectionCalculator):
        ProjectionCalculator.setWindowTitle(_translate("ProjectionCalculator", "MainWindow", None))
        self.btn_clearModel.setText(_translate("ProjectionCalculator", "Clear Model", None))
        self.btn_go.setText(_translate("ProjectionCalculator", "Calculate Projection Series From Model", None))
        self.label_6.setText(_translate("ProjectionCalculator", "Phi", None))
        self.label_8.setText(_translate("ProjectionCalculator", "Psi", None))
        self.label_7.setText(_translate("ProjectionCalculator", "Theta", None))
        self.label_2.setText(_translate("ProjectionCalculator", "Model", None))
        self.btn_selectModel.setText(_translate("ProjectionCalculator", "Browse", None))
