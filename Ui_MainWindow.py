# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\Users\Yintai Zhang\Research\ExperimentManger_Test_2\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1252, 877)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.TEST_Button = QtWidgets.QPushButton(self.centralwidget)
        self.TEST_Button.setGeometry(QtCore.QRect(1140, 790, 75, 23))
        self.TEST_Button.setObjectName("TEST_Button")
        self.ExperimentTree = QtWidgets.QTreeWidget(self.centralwidget)
        self.ExperimentTree.setGeometry(QtCore.QRect(10, 10, 311, 681))
        self.ExperimentTree.setObjectName("ExperimentTree")
        self.Type_LineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.Type_LineEdit.setGeometry(QtCore.QRect(50, 760, 171, 20))
        self.Type_LineEdit.setObjectName("Type_LineEdit")
        self.Type_Label = QtWidgets.QLabel(self.centralwidget)
        self.Type_Label.setGeometry(QtCore.QRect(20, 760, 47, 16))
        self.Type_Label.setObjectName("Type_Label")
        self.Name_Label = QtWidgets.QLabel(self.centralwidget)
        self.Name_Label.setGeometry(QtCore.QRect(20, 800, 47, 13))
        self.Name_Label.setObjectName("Name_Label")
        self.Name_LineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.Name_LineEdit.setGeometry(QtCore.QRect(50, 800, 171, 20))
        self.Name_LineEdit.setObjectName("Name_LineEdit")
        self.NewExperiment_Button = QtWidgets.QPushButton(self.centralwidget)
        self.NewExperiment_Button.setGeometry(QtCore.QRect(230, 780, 101, 23))
        self.NewExperiment_Button.setObjectName("NewExperiment_Button")
        self.CheckConfig_Button = QtWidgets.QPushButton(self.centralwidget)
        self.CheckConfig_Button.setGeometry(QtCore.QRect(20, 700, 141, 23))
        self.CheckConfig_Button.setObjectName("CheckConfig_Button")
        self.DeleteExperiment_Button = QtWidgets.QPushButton(self.centralwidget)
        self.DeleteExperiment_Button.setGeometry(QtCore.QRect(170, 700, 141, 23))
        self.DeleteExperiment_Button.setObjectName("DeleteExperiment_Button")
        self.DDSMonitor_Button = QtWidgets.QPushButton(self.centralwidget)
        self.DDSMonitor_Button.setGeometry(QtCore.QRect(1120, 20, 75, 23))
        self.DDSMonitor_Button.setObjectName("DDSMonitor_Button")
        self.DeviceConfigurationFile_label = QtWidgets.QLabel(self.centralwidget)
        self.DeviceConfigurationFile_label.setGeometry(QtCore.QRect(360, 20, 131, 21))
        self.DeviceConfigurationFile_label.setObjectName("DeviceConfigurationFile_label")
        self.DeviceConfig_LineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.DeviceConfig_LineEdit.setGeometry(QtCore.QRect(490, 20, 401, 20))
        self.DeviceConfig_LineEdit.setObjectName("DeviceConfig_LineEdit")
        self.DeviceConfigBrowse_Button = QtWidgets.QPushButton(self.centralwidget)
        self.DeviceConfigBrowse_Button.setGeometry(QtCore.QRect(910, 20, 75, 23))
        self.DeviceConfigBrowse_Button.setObjectName("DeviceConfigBrowse_Button")
        self.DeviceConfigSet_Button = QtWidgets.QPushButton(self.centralwidget)
        self.DeviceConfigSet_Button.setGeometry(QtCore.QRect(1000, 20, 75, 23))
        self.DeviceConfigSet_Button.setObjectName("DeviceConfigSet_Button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1252, 21))
        self.menubar.setObjectName("menubar")
        self.menuSubExperiment = QtWidgets.QMenu(self.menubar)
        self.menuSubExperiment.setObjectName("menuSubExperiment")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.AddSubExperiment = QtWidgets.QAction(MainWindow)
        self.AddSubExperiment.setObjectName("AddSubExperiment")
        self.menuSubExperiment.addAction(self.AddSubExperiment)
        self.menubar.addAction(self.menuSubExperiment.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.TEST_Button.setText(_translate("MainWindow", "TEST"))
        self.ExperimentTree.headerItem().setText(0, _translate("MainWindow", "All_Experiment"))
        self.Type_Label.setText(_translate("MainWindow", "Type"))
        self.Name_Label.setText(_translate("MainWindow", "Name"))
        self.NewExperiment_Button.setText(_translate("MainWindow", "New Experiment"))
        self.CheckConfig_Button.setText(_translate("MainWindow", "Check Configuration"))
        self.DeleteExperiment_Button.setText(_translate("MainWindow", "Delete Experiment"))
        self.DDSMonitor_Button.setText(_translate("MainWindow", "DDS Monitor"))
        self.DeviceConfigurationFile_label.setText(_translate("MainWindow", "Device Configuration File"))
        self.DeviceConfigBrowse_Button.setText(_translate("MainWindow", "Browse"))
        self.DeviceConfigSet_Button.setText(_translate("MainWindow", "Set"))
        self.menuSubExperiment.setTitle(_translate("MainWindow", "SubExperiment"))
        self.AddSubExperiment.setText(_translate("MainWindow", "New SubExperiment"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

