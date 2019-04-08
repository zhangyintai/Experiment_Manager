# For controlling experiments for the ion trap lab led by Prof. Yiheng Lin
# The code is written by Yintai Zhang, School of Physical Sciences, USTC
# Last updated: March 4th, 2019

from PyQt5 import QtWidgets, QtCore, QtGui
from SubExperiment import SubExperiment
from DDSMonitor import DDSMonitor
import sys
import pylint
import Functions
import DataType
from Ui_MainWindow import Ui_MainWindow
from copy import deepcopy
import threading

class Main(QtWidgets.QWidget, Ui_MainWindow):

    def __init__(self):

        self.MainWindow = QtWidgets.QMainWindow()
        super(Main, self).__init__()
        self.setupUi(self.MainWindow)    
        self._translate = QtCore.QCoreApplication.translate

        self.typ_tree = []
        self.typ = []

        self.exp = []
        self.exp_tree = []
        self.exp_win = []
        self.ddsmonitor_win = []
        self.thread = []
        self.device_list = []
        self.channel_list = []

        self.ConfigCheck = False
        
        self.Name_LineEdit.setClearButtonEnabled(True)
        self.Type_LineEdit.setClearButtonEnabled(True)
        self.CheckConfig_Button.setDisabled(True)
        self.DeleteExperiment_Button.setDisabled(True)
        self.DeviceConfigSet_Button.setDisabled(True)

        self.TEST_Button.clicked.connect(self.TEST)
        self.NewExperiment_Button.clicked.connect(self.NewExperiment)
        self.CheckConfig_Button.clicked.connect(self.CheckConfig)
        self.DeleteExperiment_Button.clicked.connect(self.DeleteExperiment)
        self.DDSMonitor_Button.clicked.connect(self.newddsmonitor)
        self.DeviceConfigBrowse_Button.clicked.connect(self.DeviceConfigBrowse)
        self.DeviceConfigSet_Button.clicked.connect(self.DeviceConfigSet)

    def DeviceConfigBrowse(self):
        try:
            path = QtWidgets.QFileDialog.getOpenFileName(self, "Browse Device Configuration File", "explorer", "(*.zmd)")
            self.DeviceConfig_LineEdit.setText(path[0])
            self.DeviceConfigSet_Button.setEnabled(True)
        except:
            self.DeviceConfig_LineEdit.clear()
    
    def DeviceConfigSet(self):
        path = self.DeviceConfig_LineEdit.text()
        try:
            DeviceConfigFile = open(path, "r")
            lines = DeviceConfigFile.readlines()

            self.device_list.clear()
            self.channel_list.clear()
            
            for line in lines:
                test_input = Functions.StringSeparate(line)
                no = len(self.device_list)
                self.device_list.append(DataType.Device(test_input[0], no, test_input[1], int(test_input[2]), int(test_input[3])))
            
            ##set up channel list
            temp = 0
            for device in self.device_list:
                for i in range(0, device.channels):
                    self.channel_list.append(DataType.Channel(device.no, i))
                    device.channel_list.append(temp + i)
                    
                temp = temp + device.channels
            
        except:
            pass
        pass
    
    def WhichSelected(self):
        flag = False
        for i in range (0,len(self.exp_tree)):
            if self.exp_tree[i].isSelected():
                flag = True
                break
        if flag:
            return i
        else:
            return -1    

    def CheckConfig(self):

        i = self.WhichSelected()

        if i != -1:
            self.exp_win[i].SubExperiment_Dialog.show()
            self.exp[i].ReadVar(self.exp_win[i].FVar_list, self.exp_win[i].TVar_list, self.exp_win[i].AmpVar_list, self.exp_win[i].PhVar_list)
        
    def DeleteExperiment(self):

        i = self.WhichSelected()

        if i != -1:

            self.typ_tree[self.exp[i].typ_code].removeChild(self.exp_tree.pop(i))
            self.exp.pop(i)
            self.exp_win.pop(i)
    
    def NewExperiment(self):
        
        temp_name = Functions.RemoveSpace(self.Name_LineEdit.text())
        temp_type = Functions.RemoveSpace(self.Type_LineEdit.text())

        if temp_name != '' and temp_type != '':
            self.Add_Experiment(temp_type, temp_name)
    
    def Add_Experiment(self, typ, name):

        typ_new = True
        typ_code = 0

        ## typ existed?
        self.CheckConfig_Button.setEnabled(True)
        self.DeleteExperiment_Button.setEnabled(True)

        for i in range (0, len(self.typ)):
            if self.typ[i] == typ:
                typ_code = i
                typ_new = False
                break
        
        ##if not, build a new type
        if typ_new:
            self.typ.append(typ)
            typ_code = len(self.typ) - 1
            self.typ_tree.append(QtWidgets.QTreeWidgetItem())
            self.typ_tree[len(self.typ_tree) - 1].setText(0, typ)
            self.ExperimentTree.addTopLevelItem(self.typ_tree[len(self.typ_tree) - 1])

        ## Add experiment
        self.exp.append(DataType.Experiment(typ_code, typ, 0, name))
        self.exp_tree.append(QtWidgets.QTreeWidgetItem())
        self.exp_tree[len(self.exp_tree) - 1].setText(0, name)
        self.typ_tree[typ_code].addChild(self.exp_tree[len(self.exp_tree) - 1])  
        self.exp_win.append(SubExperiment(name))## add new window

    # for testing
    def TEST(self):
        for i in range(0, 50):
            self.Add_Experiment("Ramsay", "Ramsay" + str(i))
    
    def newddsmonitor(self):
        
        for i in range(0, len(self.ddsmonitor_win)):
            if not self.ddsmonitor_win[i].DDSMonitor_Dialog.isVisible():
                self.ddsmonitor_win.pop(i)
                
        i = len(self.ddsmonitor_win)

        dds_list = []
        
        for device in self.device_list:
            if device.typ_code == 0:
                dds_list.append(device)

        print(len(dds_list))
        self.ddsmonitor_win.append(DDSMonitor(dds_list))
        self.ddsmonitor_win[i].DDSMonitor_Dialog.show()
    
if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    win = Main()
    win.MainWindow.setCentralWidget(win.centralwidget)
    win.MainWindow.show()
    sys.exit(app.exec_())   
