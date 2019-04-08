# For controlling experiments for the ion trap lab led by Prof. Yiheng Lin
# The code is written by Yintai Zhang, School of Physical Sciences, USTC
# Last updated: March 4th, 2019

from PyQt5 import QtWidgets, QtCore, QtGui
import pylint
import sys
from Ui_DDSMonitor import Ui_DDSMonitor
import DataType
import DDS
import Functions

class DDSMonitor(QtWidgets.QTabWidget, Ui_DDSMonitor):

    def __init__(self, dds_list):

        self.DDSMonitor_Dialog = QtWidgets.QDialog()
        super(DDSMonitor, self).__init__()
        self.setupUi(self.DDSMonitor_Dialog)
        self._translate = QtCore.QCoreApplication.translate
        self.testmode = False

        self.dds_list = dds_list
        self.setDDSComboBox()
        self.ChooseDDS_ComboBox.setCurrentIndex(-1)
        self.currentIndex = -1

        self.ChooseDDS_ComboBox.currentIndexChanged.connect(self.DDSChange)
        self.Current_Button.clicked.connect(self.Current)
        

    def setDDSComboBox(self):
        for dds in self.dds_list:
            self.ChooseDDS_ComboBox.addItem(dds.name)
    
    def Current(self):

        dds_index = self.ChooseDDS_ComboBox.currentIndex()
        state = Functions.GetNowTime() + "<p>" + "Current DDS: " + self.dds_list[dds_index].name + "<p>"
        for i in range(0, self.dds_list[dds_index].channels):
            state = state + self.getcurrentinformation(dds_index, i)
        
        self.SetText(state)

    def getcurrentinformation(self, dds_index, channel):
        if DDS.isChannelOn(dds_index, channel):
            f, amp = DDS.GetData(dds_index, channel)
            return "Channel No. " + str(channel) + " is on! f = " + str(f) + ", amp = " + str(amp) + "<p>"
        else:
            return "Channel No." + str(channel) + " is off! <p>"
    
    def DDSChange(self):
        self.current_dds = self.ChooseDDS_ComboBox.currentIndex()

    def SetText(self, text):
        self.Monitor_TextBrowser.setHtml(self._translate("DDSMonitor", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:16pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">" + "---DDS Monitor---\n<p>" + text + "</p></body></html>"))
##--------------------------------------------------------------------------------

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    dds1 = DataType.Device("dds1", 0, "COM1", 0, 5)
    dds2 = DataType.Device("dds2", 1, "COM2", 0, 5)
    win = DDSMonitor([dds1, dds2])
    win.DDSMonitor_Dialog.show()
    sys.exit(app.exec_())