# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Z:\Users\Yintai Zhang\Research\ExperimentManger_Test_2\DDSMonitor.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DDSMonitor(object):
    def setupUi(self, DDSMonitor):
        DDSMonitor.setObjectName("DDSMonitor")
        DDSMonitor.resize(1179, 846)
        self.Monitor_TextBrowser = QtWidgets.QTextBrowser(DDSMonitor)
        self.Monitor_TextBrowser.setGeometry(QtCore.QRect(20, 90, 1141, 731))
        self.Monitor_TextBrowser.setObjectName("Monitor_TextBrowser")
        self.ChooseDDS_ComboBox = QtWidgets.QComboBox(DDSMonitor)
        self.ChooseDDS_ComboBox.setGeometry(QtCore.QRect(100, 30, 181, 22))
        self.ChooseDDS_ComboBox.setObjectName("ChooseDDS_ComboBox")
        self.ChooseDDS_label = QtWidgets.QLabel(DDSMonitor)
        self.ChooseDDS_label.setGeometry(QtCore.QRect(30, 30, 61, 16))
        self.ChooseDDS_label.setObjectName("ChooseDDS_label")
        self.RefreshTime_label = QtWidgets.QLabel(DDSMonitor)
        self.RefreshTime_label.setGeometry(QtCore.QRect(310, 30, 71, 16))
        self.RefreshTime_label.setObjectName("RefreshTime_label")
        self.RefreshTime_SpinBox = QtWidgets.QDoubleSpinBox(DDSMonitor)
        self.RefreshTime_SpinBox.setGeometry(QtCore.QRect(390, 30, 101, 22))
        self.RefreshTime_SpinBox.setObjectName("RefreshTime_SpinBox")
        self.Start_Button = QtWidgets.QPushButton(DDSMonitor)
        self.Start_Button.setGeometry(QtCore.QRect(530, 30, 75, 23))
        self.Start_Button.setObjectName("Start_Button")
        self.Stop_Button = QtWidgets.QPushButton(DDSMonitor)
        self.Stop_Button.setGeometry(QtCore.QRect(620, 30, 75, 23))
        self.Stop_Button.setObjectName("Stop_Button")
        self.Current_Button = QtWidgets.QPushButton(DDSMonitor)
        self.Current_Button.setGeometry(QtCore.QRect(710, 30, 75, 23))
        self.Current_Button.setObjectName("Current_Button")

        self.retranslateUi(DDSMonitor)
        QtCore.QMetaObject.connectSlotsByName(DDSMonitor)

    def retranslateUi(self, DDSMonitor):
        _translate = QtCore.QCoreApplication.translate
        DDSMonitor.setWindowTitle(_translate("DDSMonitor", "DDS Monitor"))
        self.Monitor_TextBrowser.setHtml(_translate("DDSMonitor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">---DDS Monitor---</span></p></body></html>"))
        self.ChooseDDS_label.setText(_translate("DDSMonitor", "Choose DDS"))
        self.RefreshTime_label.setText(_translate("DDSMonitor", "Refresh Time"))
        self.Start_Button.setText(_translate("DDSMonitor", "Start"))
        self.Stop_Button.setText(_translate("DDSMonitor", "Stop"))
        self.Current_Button.setText(_translate("DDSMonitor", "Current"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DDSMonitor = QtWidgets.QDialog()
    ui = Ui_DDSMonitor()
    ui.setupUi(DDSMonitor)
    DDSMonitor.show()
    sys.exit(app.exec_())

