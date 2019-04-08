# For controlling experiments for the ion trap lab led by Prof. Yiheng Lin
# The code is written by Yintai Zhang, School of Physical Sciences, USTC
# Last updated: April 29th, 2019

from PyQt5 import QtWidgets, QtCore, QtGui
# import pylint
from Ui_SubExperiment import Ui_SubExperiment_Dialog
import sys
import os
import Functions
import DataType
import time
##-------------------------------------------------------------------------------

class SubExperiment(QtWidgets.QWidget, Ui_SubExperiment_Dialog):
    
    def __init__(self, exp_name):

        ##Configure window
        self.SubExperiment_Dialog = QtWidgets.QDialog()
        super(SubExperiment, self).__init__()
        self.setupUi(self.SubExperiment_Dialog)    
        self._translate = QtCore.QCoreApplication.translate

        ##Initiate Parametres
        self.FVar_num = 0
        self.TVar_num = 0
        self.AmpVar_num = 0
        self.PhVar_num = 0
        self.OVar_num = 0
        self.exp_name = exp_name
        #self.channels = 16 ## this number is for test

        self.FScan = 0
        self.TScan = 0
        self.AmpScan = 0
        self.PhScan = 0
        self.OScan = 0

        self.FScan_step = 0
        self.TScan_step = 0
        self.AmpScan_step = 0
        self.PhScan_step = 0
        self.OScan_step = 0
        
        self.name = ''
        self.exp_dir = ''
        self.script_dir = ''
        self.winconfig_dir = ''
        self.FVar_list = []
        self.TVar_list = []
        self.AmpVar_list = []
        self.PhVar_list = []
        self.OVar_list = []
        
        ##Initiate Widgets
        self.FVar_scan_CheckBox.setDisabled(True)
        self.TVar_scan_CheckBox.setDisabled(True)
        self.AmpVar_scan_CheckBox.setDisabled(True)
        self.PhVar_scan_CheckBox.setDisabled(True)
        self.OVar_scan_CheckBox.setDisabled(True)

        self.FVar_step_SpinBox.setDisabled(True)
        self.TVar_step_SpinBox.setDisabled(True)
        self.AmpVar_step_SpinBox.setDisabled(True)
        self.PhVar_step_SpinBox.setDisabled(True)
        self.OVar_step_SpinBox.setDisabled(True)

        self.FVar_lb_SpinBox.setDisabled(True)
        self.FVar_ub_SpinBox.setDisabled(True)
        self.FVar_var_SpinBox.setDisabled(True)
        self.OVar_lb_SpinBox.setDisabled(True)
        self.OVar_ub_SpinBox.setDisabled(True)
        self.OVar_var_SpinBox.setDisabled(True)
        self.TVar_lb_SpinBox.setDisabled(True)
        self.TVar_ub_SpinBox.setDisabled(True)
        self.TVar_var_SpinBox.setDisabled(True)
        self.AmpVar_lb_SpinBox.setDisabled(True)
        self.AmpVar_ub_SpinBox.setDisabled(True)
        self.AmpVar_var_SpinBox.setDisabled(True)
        self.PhVar_lb_SpinBox.setDisabled(True)
        self.PhVar_ub_SpinBox.setDisabled(True)
        self.PhVar_var_SpinBox.setDisabled(True)
        #self.FVarChannel_ComboBox.setDisabled(True)
        #self.AmpVarChannel_ComboBox.setDisabled(True)
        #self.TVarChannel_ComboBox.setDisabled(True)
        #self.PhVarChannel_ComboBox.setDisabled(True)
        self.ScriptSave_Button.setDisabled(True)
        self.ScriptDirectoryBrowse_Button.setDisabled(True)
        self.SetDir_Button.setDisabled(True)
        self.FVar_times_SpinBox.setDisabled(True)
        self.TVar_times_SpinBox.setDisabled(True)
        self.PhVar_times_SpinBox.setDisabled(True)
        self.AmpVar_times_SpinBox.setDisabled(True)
        self.OVar_times_SpinBox.setDisabled(True)
        self.ExpScriptRun_Button.setDisabled(True)
        self.ExpScriptView_Button.setDisabled(True)
        self.TitleConfirm_Button.setDisabled(True)
        self.WinConfigView_Button.setDisabled(True)
        self.ParaScriptView_Button.setDisabled(True)
        
        self.f1shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F1), self.FVar_Label)
        self.f1shortcut.activated.connect(self.bilibili)
        self.f5shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F5), self.FVar_Label)
        self.f5shortcut.activated.connect(self.ExpScriptRun)
        self.f2shortcut = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_F2), self.FVar_Label)
        self.f2shortcut.activated.connect(self.arxiv)

        ##

        self.SubExperiment_Dialog.setWindowTitle("Experiment Name: " + self.exp_name + "[*]")

        ##Connect Widgets
        self.ConfigFileBrowse_Button.clicked.connect(self.ConfigFileBrowse)
        self.ConfigFileConfirm_Button.clicked.connect(self.ConfigFileConfirm)
        self.ScriptDirectoryBrowse_Button.clicked.connect(self.ScriptDirectoryBrowse)
        self.SetDir_Button.clicked.connect(self.SetDir)
        self.ScriptSave_Button.clicked.connect(self.ScriptSave)

        self.FVar_ComboBox.currentIndexChanged.connect(self.FVarIndexChanged)
        self.TVar_ComboBox.currentIndexChanged.connect(self.TVarIndexChanged)
        self.AmpVar_ComboBox.currentIndexChanged.connect(self.AmpVarIndexChanged)
        self.PhVar_ComboBox.currentIndexChanged.connect(self.PhVarIndexChanged)
        self.OVar_ComboBox.currentIndexChanged.connect(self.OVarIndexChanged)


        self.FVar_lb_SpinBox.valueChanged.connect(self.FVar_lbChanged)    
        self.FVar_ub_SpinBox.valueChanged.connect(self.FVar_ubChanged)
        self.FVar_var_SpinBox.valueChanged.connect(self.FVar_varChanged)
        self.FVar_step_SpinBox.valueChanged.connect(self.FVar_stepChanged)
        self.FVar_scan_CheckBox.stateChanged.connect(self.FVar_scanChanged)

        self.OVar_lb_SpinBox.valueChanged.connect(self.OVar_lbChanged)    
        self.OVar_ub_SpinBox.valueChanged.connect(self.OVar_ubChanged)
        self.OVar_var_SpinBox.valueChanged.connect(self.OVar_varChanged)
        self.OVar_step_SpinBox.valueChanged.connect(self.OVar_stepChanged)
        self.OVar_scan_CheckBox.stateChanged.connect(self.OVar_scanChanged)
        
        self.TVar_lb_SpinBox.valueChanged.connect(self.TVar_lbChanged)
        self.TVar_ub_SpinBox.valueChanged.connect(self.TVar_ubChanged)
        self.TVar_var_SpinBox.valueChanged.connect(self.TVar_varChanged)
        self.TVar_step_SpinBox.valueChanged.connect(self.TVar_stepChanged)
        self.TVar_scan_CheckBox.stateChanged.connect(self.TVar_scanChanged)

        self.AmpVar_lb_SpinBox.valueChanged.connect(self.AmpVar_lbChanged)
        self.AmpVar_ub_SpinBox.valueChanged.connect(self.AmpVar_ubChanged)
        self.AmpVar_var_SpinBox.valueChanged.connect(self.AmpVar_varChanged)
        self.AmpVar_step_SpinBox.valueChanged.connect(self.AmpVar_stepChanged)
        self.AmpVar_scan_CheckBox.stateChanged.connect(self.AmpVar_scanChanged)

        self.PhVar_lb_SpinBox.valueChanged.connect(self.PhVar_lbChanged)
        self.PhVar_ub_SpinBox.valueChanged.connect(self.PhVar_ubChanged)
        self.PhVar_var_SpinBox.valueChanged.connect(self.PhVar_varChanged)
        self.PhVar_step_SpinBox.valueChanged.connect(self.PhVar_stepChanged)
        self.PhVar_scan_CheckBox.stateChanged.connect(self.PhVar_scanChanged)

        #self.FVarChannel_ComboBox.currentIndexChanged.connect(self.FVarChannel_Change)
        #self.TVarChannel_ComboBox.currentIndexChanged.connect(self.TVarChannel_Change)
        #self.AmpVarChannel_ComboBox.currentIndexChanged.connect(self.AmpVarChannel_Change)
        #self.PhVarChannel_ComboBox.currentIndexChanged.connect(self.PhVarChannel_Change)

        self.FVar_times_SpinBox.valueChanged.connect(self.FVar_timesChanged)
        self.TVar_times_SpinBox.valueChanged.connect(self.TVar_timesChanged)
        self.AmpVar_times_SpinBox.valueChanged.connect(self.AmpVar_timesChanged)
        self.PhVar_times_SpinBox.valueChanged.connect(self.PhVar_timesChanged)
        self.OVar_times_SpinBox.valueChanged.connect(self.OVar_timesChanged)

        
        self.ExpDirBrowse_Button.clicked.connect(self.ExpDirBrowse)
        self.ExpDirSet_Button.clicked.connect(self.ExpDirSet)
        self.ExpScriptView_Button.clicked.connect(self.ExpScriptView)
        self.ExpScriptRun_Button.clicked.connect(self.ExpScriptRun)
        self.WinConfigView_Button.clicked.connect(self.WinConfigView)
    
        self.TitleConfirm_Button.clicked.connect(self.TitleConfirm)
        self.Help_Button.clicked.connect(self.bilibili)
        self.ParaScriptView_Button.clicked.connect(self.ParaScriptView)
    
    def arxiv(self):
        os.system("explorer https://arxiv.org/")
    
    def bilibili(self):
        os.system("explorer https://www.bilibili.com/")
        

    def TitleConfirm(self):
        try:
            text = self.Title_LEdit.text()
            if text != '':
                text = Functions.RemoveSpace(text)
                self.Title_LEdit.setText(text)
                self.name = text
            else:
                self.Title_LEDit.setText(self.name)
        except:
            pass
    
    def test(self):
        print("test passed!")

    def ConfigFileBrowse(self):
        try:
            path = QtWidgets.QFileDialog.getOpenFileName(self, "Browse Configuration File", "explorer", "(*.zyt)")
            self.ConfigFile_LEdit.setText(path[0])
            if os.path.exists(path[0]):
                self.WinConfigView_Button.setEnabled(True)
                self.winconfig_dir = path[0]
            else:
                self.WinConfigView_Button.setDisabled(True)
        except:
            self.ConfigFile_LEdit.clear()

    def ExpDirBrowse(self):
        try:
            path = QtWidgets.QFileDialog.getOpenFileName(self, "Browse Experiment Script Directory", "explorer", "(*.py)")
            print(path)
            self.ExpDir_LineEdit.setText(path[0])
        except:
            self.ExpDir_LineEdit.clear()

    def ScriptDirectoryBrowse(self):
        try:
            path = QtWidgets.QFileDialog.getExistingDirectory(self, "Browse Parameters Script Directory", "explorer")
            print(path)
            self.ScriptDirectory_LineEdit.setText(path)
            self.script_dir = path
            self.ParaScriptView_Button.setEnabled(True)

        except:
            self.ScriptDirectory_LineEdit.clear()
            self.ParaScriptView_Button.setDisabled(True)
    
    def ParaScriptView(self):
        try:
            print(self.script_dir + "/" + self.name + "_para.py")
            if (os.path.exists(self.script_dir + "/" + self.name + "_para.py")):
                print("exists!")
                os.system("notepad " + self.script_dir + "/" + self.name + "_para.py")
        except:
            pass

    
    def SetDir(self):
        directory = self.ScriptDirectory_LineEdit.text()
        
        if os.path.exists(directory):
            self.ScriptSave_Button.setEnabled(True)
        else:
            self.ScriptSave_Button.setDisabled(True)
    
    def ConfigFileConfirm(self):##Read Configuration File
        if not os.path.exists(self.ConfigFile_LEdit.text()):
            self.FVar_step_SpinBox.setDisabled(True)
            self.OVar_step_SpinBox.setDisabled(True)
            self.TVar_step_SpinBox.setDisabled(True)
            self.AmpVar_step_SpinBox.setDisabled(True)
            self.PhVar_step_SpinBox.setDisabled(True)
            self.FVar_lb_SpinBox.setDisabled(True)
            self.FVar_ub_SpinBox.setDisabled(True)
            self.FVar_var_SpinBox.setDisabled(True)
            self.OVar_lb_SpinBox.setDisabled(True)
            self.OVar_ub_SpinBox.setDisabled(True)
            self.OVar_var_SpinBox.setDisabled(True)
            self.TVar_lb_SpinBox.setDisabled(True)
            self.TVar_ub_SpinBox.setDisabled(True)
            self.TVar_var_SpinBox.setDisabled(True)
            self.AmpVar_lb_SpinBox.setDisabled(True)
            self.AmpVar_ub_SpinBox.setDisabled(True)
            self.AmpVar_var_SpinBox.setDisabled(True)
            self.PhVar_lb_SpinBox.setDisabled(True)
            self.PhVar_ub_SpinBox.setDisabled(True)
            self.PhVar_var_SpinBox.setDisabled(True)
            #self.FVarChannel_ComboBox.setDisabled(True)
            #self.TVarChannel_ComboBox.setDisabled(True)
            #self.AmpVarChannel_ComboBox.setDisabled(True)
            #self.PhVarChannel_ComboBox.setDisabled(True)
            self.FVar_times_SpinBox.setDisabled(True)
            self.OVar_times_SpinBox.setDisabled(True)
            self.TVar_times_SpinBox.setDisabled(True)
            self.AmpVar_times_SpinBox.setDisabled(True)
            self.PhVar_times_SpinBox.setDisabled(True)
            self.TitleConfirm_Button.setDisabled(True)
            self.ScriptDirectoryBrowse_Button.setDisabled(True)
            self.SetDir_Button.setDisabled(True)
        
        try:
            inputfilename = self.ConfigFile_LEdit.text()
            inputfile = open(inputfilename, 'r+')
            text = inputfile.readlines()

            flag = 0
            flag_another = 0

            self.FVar_list.clear()
            self.OVar_list.clear()
            self.TVar_list.clear()
            self.AmpVar_list.clear()
            self.PhVar_list.clear()
            
            for line in text:
                if flag == 0:
                    self.name = line.replace("\n", "")
                    self.Title_LEdit.setText(self.name)
                    flag = flag + 1
                else:
                    try:
                        num = int(line)

                        if flag_another == 0:
                            self.FVar_num = num
                        elif flag_another == 1:
                            self.TVar_num = num
                        elif flag_another == 2:
                            self.AmpVar_num = num
                        elif flag_another == 3:
                            self.PhVar_num = num
                        elif flag_another == 4:
                            self.OVar_num = num
                        else:
                            pass
                        
                        flag_another = flag_another + 1

                    except:
                        if True:
                            s_list = Functions.StringSeparate(line)
                            name = s_list[0]
                            lb = float(s_list[1])
                            ub = float(s_list[2])
                            var = float(s_list[3])
                            llb = float(s_list[4])
                            uub = float(s_list[5])
                            ##print(flag_another)

                            if flag_another == 1:
                                self.FVar_list.append(DataType.FVar(name, lb, ub, var, llb, uub))
                            elif flag_another == 2:
                                self.TVar_list.append(DataType.TVar(name, lb, ub, var, llb, uub))
                            elif flag_another == 3:
                                self.AmpVar_list.append(DataType.AmpVar(name, lb, ub, var, llb, uub))
                            elif flag_another == 4:
                                self.PhVar_list.append(DataType.PhVar(name, lb, ub, var, llb, uub))
                            elif flag_another == 5:
                                self.OVar_list.append(DataType.OVar(name, lb, ub, var, llb, uub))
                                
            print("Input Finished!")
            self.ScriptDirectoryBrowse_Button.setEnabled(True)
            self.SetDir_Button.setEnabled(True)
            self.VarCombo_Init()
                            ##break
            inputfile.close()

        except:
            pass
    
    def VarCombo_Init(self):

        #self.FVarChannel_ComboBox.clear()
        #self.TVarChannel_ComboBox.clear()
        #self.AmpVarChannel_ComboBox.clear()
        #self.PhVarChannel_ComboBox.clear()
        self.FVar_ComboBox.clear()
        self.TVar_ComboBox.clear()
        self.AmpVar_ComboBox.clear()
        self.PhVar_ComboBox.clear()
        self.OVar_ComboBox.clear()

        #for i in range(0, self.channels):
            #self.FVarChannel_ComboBox.addItem(str(i))
            #self.TVarChannel_ComboBox.addItem(str(i))
            #self.AmpVarChannel_ComboBox.addItem(str(i))
            #self.PhVarChannel_ComboBox.addItem(str(i))
            ##pass
        ##Add items to each combobox
        ##The index of each combobox starts from 0
        for fvar in self.FVar_list:
            var = fvar.var
            ub = fvar.ub
            lb = fvar.lb
            step = fvar.step
            scan = fvar.scan
           
            self.FVar_ComboBox.addItem(fvar.name)
            fvar.var = var
            fvar.ub = ub    
            fvar.lb = lb
            fvar.step = step
            fvar.scan = scan
            ##print(self.FVar_list[0].ub, self.FVar_list[0].lb)
        
        
        for tvar in self.TVar_list:
            var = tvar.var
            ub = tvar.ub
            lb = tvar.lb
            step = tvar.step
            scan = tvar.scan
            self.TVar_ComboBox.addItem(tvar.name)
            
            tvar.var = var
            tvar.ub = ub    
            tvar.lb = lb
            tvar.step = step
            tvar.scan = scan

        for ampvar in self.AmpVar_list:
            var = ampvar.var
            ub = ampvar.ub
            lb = ampvar.lb
            step = ampvar.step
            scan = ampvar.scan
            self.AmpVar_ComboBox.addItem(ampvar.name)
            ampvar.var = var
            ampvar.ub = ub    
            ampvar.lb = lb
            ampvar.step = step
            ampvar.scan = scan
        
        for phvar in self.PhVar_list:
            var = phvar.var
            ub = phvar.ub
            lb = phvar.lb
            step = phvar.step
            scan = phvar.scan
            self.PhVar_ComboBox.addItem(phvar.name)
            phvar.var = var
            phvar.ub = ub    
            phvar.lb = lb
            phvar.step = step
            phvar.scan = scan

        for ovar in self.OVar_list:
            var = ovar.var
            ub = ovar.ub
            lb = ovar.lb
            step = ovar.step
            scan = ovar.scan
            self.OVar_ComboBox.addItem(ovar.name)
            
            ovar.var = var
            ovar.ub = ub    
            ovar.lb = lb
            ovar.step = step
            ovar.scan = scan
        
        ##Initiate the rest part
        self.FVar_step_SpinBox.setEnabled(True)
        self.TVar_step_SpinBox.setEnabled(True)
        self.AmpVar_step_SpinBox.setEnabled(True)
        self.PhVar_step_SpinBox.setEnabled(True)
        self.OVar_step_SpinBox.setEnabled(True)

        self.FVar_lb_SpinBox.setEnabled(True)
        self.FVar_ub_SpinBox.setEnabled(True)
        self.FVar_var_SpinBox.setEnabled(True)
        self.TVar_lb_SpinBox.setEnabled(True)
        self.TVar_ub_SpinBox.setEnabled(True)
        self.TVar_var_SpinBox.setEnabled(True)
        self.AmpVar_lb_SpinBox.setEnabled(True)
        self.AmpVar_ub_SpinBox.setEnabled(True)
        self.AmpVar_var_SpinBox.setEnabled(True)
        self.PhVar_lb_SpinBox.setEnabled(True)
        self.PhVar_ub_SpinBox.setEnabled(True)
        self.PhVar_var_SpinBox.setEnabled(True)
        self.OVar_lb_SpinBox.setEnabled(True)
        self.OVar_ub_SpinBox.setEnabled(True)
        self.OVar_var_SpinBox.setEnabled(True)
        #self.FVarChannel_ComboBox.setEnabled(True)
        #self.TVarChannel_ComboBox.setEnabled(True)
        #self.AmpVarChannel_ComboBox.setEnabled(True)
        #self.PhVarChannel_ComboBox.setEnabled(True)
        self.FVar_times_SpinBox.setEnabled(True)
        self.TVar_times_SpinBox.setEnabled(True)
        self.AmpVar_times_SpinBox.setEnabled(True)
        self.PhVar_times_SpinBox.setEnabled(True)
        self.TitleConfirm_Button.setEnabled(True)
        self.OVar_times_SpinBox.setEnabled(True)

        try:
            self.FVarIndexChanged(0)
        except:
            pass

        try:
            self.TVarIndexChanged(0)
        except:
            pass
            
        try:
            self.AmpVarIndexChanged(0)
        except:
            pass

        try:
            self.PhVarIndexChanged(0)
        except:
            pass

        try:
            self.OVarIndexChanged(0)
        except:
            pass

    
    def FVarIndexChanged(self, i):
        
        self.FVar_lb_SpinBox.setMinimum(self.FVar_list[i].llb)
        self.FVar_lb_SpinBox.setMaximum(self.FVar_list[i].uub)
        self.FVar_ub_SpinBox.setMinimum(self.FVar_list[i].llb)
        self.FVar_ub_SpinBox.setMaximum(self.FVar_list[i].uub)
        self.FVar_var_SpinBox.setMaximum(self.FVar_list[i].uub)
        self.FVar_var_SpinBox.setMinimum(self.FVar_list[i].llb)

        ##print(self.FVar_list[i].lb, self.FVar_list[i].ub, self.FVar_list[i].var)
        self.FVar_lb_SpinBox.setValue(self.FVar_list[i].lb)
        self.FVar_ub_SpinBox.setValue(self.FVar_list[i].ub)
        self.FVar_var_SpinBox.setValue(self.FVar_list[i].var)
        self.FVar_times_SpinBox.setValue(self.FVar_list[i].times)

        self.FVar_lb_SpinBox.setMinimum(self.FVar_list[i].llb)
        self.FVar_lb_SpinBox.setMaximum(self.FVar_list[i].ub)
        self.FVar_ub_SpinBox.setMinimum(self.FVar_list[i].lb)
        self.FVar_ub_SpinBox.setMaximum(self.FVar_list[i].uub)
        self.FVar_var_SpinBox.setMaximum(self.FVar_list[i].ub)
        self.FVar_var_SpinBox.setMinimum(self.FVar_list[i].lb)

        self.FVar_step_SpinBox.setValue(self.FVar_list[i].step)
        self.FVar_step_SpinBox.setMaximum(self.FVar_list[i].uub - self.FVar_list[i].llb)
        self.FVar_step_SpinBox.setMinimum(-(self.FVar_list[i].uub - self.FVar_list[i].llb))
        
        if self.FVar_list[i].step == 0:
            self.FVar_scan_CheckBox.setDisabled(True)
        else:
            self.FVar_scan_CheckBox.setEnabled(True)
            self.FVar_scan_CheckBox.setCheckState(self.FVar_list[i].scan)
        
        #self.FVarChannel_ComboBox.setCurrentIndex(self.FVar_list[i].channel)
        
    def TVarIndexChanged(self, i):
        self.TVar_lb_SpinBox.setMinimum(self.TVar_list[i].llb)
        self.TVar_lb_SpinBox.setMaximum(self.TVar_list[i].uub)
        self.TVar_var_SpinBox.setMaximum(self.TVar_list[i].uub)
        self.TVar_var_SpinBox.setMinimum(self.TVar_list[i].llb)
        self.TVar_ub_SpinBox.setMinimum(self.TVar_list[i].llb)
        self.TVar_ub_SpinBox.setMaximum(self.TVar_list[i].uub)

        self.TVar_lb_SpinBox.setValue(self.TVar_list[i].lb)
        self.TVar_ub_SpinBox.setValue(self.TVar_list[i].ub)
        self.TVar_var_SpinBox.setValue(self.TVar_list[i].var)
        self.TVar_times_SpinBox.setValue(self.TVar_list[i].times)
    
        self.TVar_lb_SpinBox.setMinimum(self.TVar_list[i].llb)
        self.TVar_lb_SpinBox.setMaximum(self.TVar_list[i].ub)
        self.TVar_var_SpinBox.setMaximum(self.TVar_list[i].ub)
        self.TVar_var_SpinBox.setMinimum(self.TVar_list[i].lb)
        self.TVar_ub_SpinBox.setMinimum(self.TVar_list[i].lb)
        self.TVar_ub_SpinBox.setMaximum(self.TVar_list[i].uub)


        self.TVar_step_SpinBox.setValue(self.TVar_list[i].step)
        self.TVar_step_SpinBox.setMaximum(self.TVar_list[i].uub - self.TVar_list[i].llb)
        self.TVar_step_SpinBox.setMinimum(-(self.TVar_list[i].uub - self.TVar_list[i].llb))
        if self.TVar_list[i].step == 0:
            self.TVar_scan_CheckBox.setDisabled(True)
        else:
            self.TVar_scan_CheckBox.setEnabled(True)
            self.TVar_scan_CheckBox.setCheckState(self.TVar_list[i].scan)
        
        # self.TVarChannel_ComboBox.setCurrentIndex(self.TVar_list[i].channel)
    
    def AmpVarIndexChanged(self, i):
        self.AmpVar_lb_SpinBox.setMinimum(self.AmpVar_list[i].llb)
        self.AmpVar_lb_SpinBox.setMaximum(self.AmpVar_list[i].uub)
        self.AmpVar_var_SpinBox.setMaximum(self.AmpVar_list[i].uub)
        self.AmpVar_var_SpinBox.setMinimum(self.AmpVar_list[i].llb)
        self.AmpVar_ub_SpinBox.setMinimum(self.AmpVar_list[i].llb)
        self.AmpVar_ub_SpinBox.setMaximum(self.AmpVar_list[i].uub)

        self.AmpVar_lb_SpinBox.setValue(self.AmpVar_list[i].lb)
        self.AmpVar_ub_SpinBox.setValue(self.AmpVar_list[i].ub)
        self.AmpVar_var_SpinBox.setValue(self.AmpVar_list[i].var)
        self.AmpVar_times_SpinBox.setValue(self.AmpVar_list[i].times)

        self.AmpVar_lb_SpinBox.setMinimum(self.AmpVar_list[i].llb)
        self.AmpVar_lb_SpinBox.setMaximum(self.AmpVar_list[i].ub)
        self.AmpVar_var_SpinBox.setMaximum(self.AmpVar_list[i].ub)
        self.AmpVar_var_SpinBox.setMinimum(self.AmpVar_list[i].lb)
        self.AmpVar_ub_SpinBox.setMinimum(self.AmpVar_list[i].lb)
        self.AmpVar_ub_SpinBox.setMaximum(self.AmpVar_list[i].uub)

        self.AmpVar_step_SpinBox.setMaximum(self.AmpVar_list[i].uub - self.AmpVar_list[i].llb)
        self.AmpVar_step_SpinBox.setMinimum(-(self.AmpVar_list[i].uub - self.AmpVar_list[i].llb))
        if self.AmpVar_list[i].step == 0:
            self.AmpVar_scan_CheckBox.setDisabled(True)
        else:
            self.AmpVar_scan_CheckBox.setEnabled(True)
            self.AmpVar_scan_CheckBox.setCheckState(self.AmpVar_list[i].scan)
        
        # self.AmpVarChannel_ComboBox.setCurrentIndex(self.AmpVar_list[i].channel)
    
    def PhVarIndexChanged(self, i):

        self.PhVar_lb_SpinBox.setMinimum(self.PhVar_list[i].llb)
        self.PhVar_lb_SpinBox.setMaximum(self.PhVar_list[i].uub)
        self.PhVar_ub_SpinBox.setMinimum(self.PhVar_list[i].llb)
        self.PhVar_ub_SpinBox.setMaximum(self.PhVar_list[i].uub)
        self.PhVar_var_SpinBox.setMaximum(self.PhVar_list[i].uub)
        self.PhVar_var_SpinBox.setMinimum(self.PhVar_list[i].llb)

        self.PhVar_lb_SpinBox.setValue(self.PhVar_list[i].lb)
        self.PhVar_ub_SpinBox.setValue(self.PhVar_list[i].ub)
        self.PhVar_var_SpinBox.setValue(self.PhVar_list[i].var)
        self.PhVar_times_SpinBox.setValue(self.PhVar_list[i].times)
    
        self.PhVar_lb_SpinBox.setMinimum(self.PhVar_list[i].llb)
        self.PhVar_lb_SpinBox.setMaximum(self.PhVar_list[i].ub)
        self.PhVar_ub_SpinBox.setMinimum(self.PhVar_list[i].lb)
        self.PhVar_ub_SpinBox.setMaximum(self.PhVar_list[i].uub)
        self.PhVar_var_SpinBox.setMaximum(self.PhVar_list[i].ub)
        self.PhVar_var_SpinBox.setMinimum(self.PhVar_list[i].lb)


        self.PhVar_step_SpinBox.setMaximum(self.PhVar_list[i].uub - self.PhVar_list[i].llb)
        self.PhVar_step_SpinBox.setMinimum(-(self.PhVar_list[i].uub - self.PhVar_list[i].llb))
        if self.PhVar_list[i].step == 0:
            self.PhVar_scan_CheckBox.setDisabled(True)
        else:
            self.PhVar_scan_CheckBox.setEnabled(True)
            self.PhVar_scan_CheckBox.setCheckState(self.PhVar_list[i].scan)
        
        # self.PhVarChannel_ComboBox.setCurrentIndex(self.PhVar_list[i].channel)

    def OVarIndexChanged(self, i):
        self.OVar_lb_SpinBox.setMinimum(self.OVar_list[i].llb)
        self.OVar_lb_SpinBox.setMaximum(self.OVar_list[i].uub)
        self.OVar_var_SpinBox.setMaximum(self.OVar_list[i].uub)
        self.OVar_var_SpinBox.setMinimum(self.OVar_list[i].llb)
        self.OVar_ub_SpinBox.setMinimum(self.OVar_list[i].llb)
        self.OVar_ub_SpinBox.setMaximum(self.OVar_list[i].uub)

        self.OVar_lb_SpinBox.setValue(self.OVar_list[i].lb)
        self.OVar_ub_SpinBox.setValue(self.OVar_list[i].ub)
        self.OVar_var_SpinBox.setValue(self.OVar_list[i].var)
        self.OVar_times_SpinBox.setValue(self.OVar_list[i].times)
    
        self.OVar_lb_SpinBox.setMinimum(self.OVar_list[i].llb)
        self.OVar_lb_SpinBox.setMaximum(self.OVar_list[i].ub)
        self.OVar_var_SpinBox.setMaximum(self.OVar_list[i].ub)
        self.OVar_var_SpinBox.setMinimum(self.OVar_list[i].lb)
        self.OVar_ub_SpinBox.setMinimum(self.OVar_list[i].lb)
        self.OVar_ub_SpinBox.setMaximum(self.OVar_list[i].uub)


        self.OVar_step_SpinBox.setValue(self.OVar_list[i].step)
        self.OVar_step_SpinBox.setMaximum(self.OVar_list[i].uub - self.OVar_list[i].llb)
        self.OVar_step_SpinBox.setMinimum(-(self.OVar_list[i].uub - self.OVar_list[i].llb))
        if self.OVar_list[i].step == 0:
            self.OVar_scan_CheckBox.setDisabled(True)
        else:
            self.OVar_scan_CheckBox.setEnabled(True)
            self.OVar_scan_CheckBox.setCheckState(self.TVar_list[i].scan)
    
    def FVarSelect(self):
        
        index = self.FVar_ComboBox.currentIndex()
        print("Current FVar index is", index)
        self.FVarIndexChange(index)

    def TVarSelect(self):
        index = self.TVar_ComboBox.currentIndex()
        self.TVarIndexChange(index)

    def AmpVarSelect(self):
        index = self.AmpVar_ComboBox.currentIndex()
        self.AmpVarIndexChange(index)

    def PhVarSelect(self):
        index = self.PhVar_ComboBox.currentIndex()
        self.PhVarIndexChange(index)

    def OVarSelect(self):
        
        index = self.OVar_ComboBox.currentIndex()
        print("Current OVar index is", index)
        self.OVarIndexChange(index)

    def FVar_lbChanged(self):
        try:
            index = self.FVar_ComboBox.currentIndex()
            self.FVar_list[index].set_lb(self.FVar_lb_SpinBox.value())
            if self.FVar_list[index].var < self.FVar_list[index].lb:
                self.FVar_list[index].set_var(self.FVar_list[index].lb)
                self.FVar_var_SpinBox.setValue(self.FVar_list[index].lb)
        
            self.FVar_var_SpinBox.setMinimum(self.FVar_list[index].lb)
            self.FVar_ub_SpinBox.setMinimum(self.FVar_list[index].lb)

        except:
            print("FVAR LB CHANGE Warning!")
    
    def FVar_ubChanged(self):
        try:
            index = self.FVar_ComboBox.currentIndex()
            self.FVar_list[index].set_ub(self.FVar_ub_SpinBox.value())
            if self.FVar_list[index].var > self.FVar_list[index].ub:
                self.FVar_list[index].set_var(self.FVar_list[index].ub)
                self.FVar_var_SpinBox.setValue(self.FVar_list[index].ub)

            self.FVar_var_SpinBox.setMaximum(self.FVar_list[index].ub)
            self.FVar_lb_SpinBox.setMaximum(self.FVar_list[index].ub)

        except:
            print("FVAR UB CHANGE Warning!")
    
    def FVar_varChanged(self):
        try:
            index = self.FVar_ComboBox.currentIndex()
            self.FVar_list[index].set_var(self.FVar_var_SpinBox.value())
        except:
            print("FVAR VAR CHANGE Warning!")
    
    def FVar_timesChanged(self):
        try:
            index = self.FVar_ComboBox.currentIndex()
            self.FVar_list[index].set_times(self.FVar_times_SpinBox.value())
        except:
            print("FVAR TIMES CHANGE Warning!")
    
    def FVar_stepChanged(self):
        try:
            index = self.FVar_ComboBox.currentIndex()
            self.FVar_list[index].set_step(self.FVar_step_SpinBox.value())
            if self.FVar_list[index].step == 0:
                self.FVar_scan_CheckBox.setDisabled(True)
                self.FVar_list[index].set_scan(0)
            else:
                self.FVar_scan_CheckBox.setEnabled(True)
                
        
            self.FVar_scan_CheckBox.setCheckState(self.FVar_list[index].scan)
        except:
            print("FVar step Warning!")
    
    def FVar_scanChanged(self):
        try:
            print("FVar scan changed")
            index = self.FVar_ComboBox.currentIndex()
            self.FVar_list[index].set_scan(self.FVar_scan_CheckBox.checkState())
        except:
            print("Fvar scan Warning!")



    def TVar_lbChanged(self):
        try:
            index = self.TVar_ComboBox.currentIndex()
            self.TVar_list[index].set_lb(self.TVar_lb_SpinBox.value())
            print(self.TVar_list[index].lb)
            if self.TVar_list[index].var < self.TVar_list[index].lb:
                self.TVar_list[index].set_var(self.TVar_list[index].lb)
                self.TVar_var_SpinBox.setValue(self.TVar_list[index].lb)
        
            self.TVar_var_SpinBox.setMinimum(self.TVar_list[index].lb)
            self.TVar_ub_SpinBox.setMinimum(self.TVar_list[index].lb)

        except:
            pass

    
    def TVar_ubChanged(self):
        try:
            index = self.TVar_ComboBox.currentIndex()
            self.TVar_list[index].set_ub(self.TVar_ub_SpinBox.value())
            if self.TVar_list[index].var > self.TVar_list[index].ub:
                self.TVar_list[index].set_var(self.TVar_list[index].ub)
                self.TVar_var_SpinBox.setValue(self.TVar_list[index].ub)

            self.TVar_var_SpinBox.setMaximum(self.TVar_list[index].ub)
            self.TVar_lb_SpinBox.setMaximum(self.TVar_list[index].ub)

        except:
            print("TVar ub change Warning!")
    
    def TVar_varChanged(self):
        try:
            index = self.TVar_ComboBox.currentIndex()
            self.TVar_list[index].set_var(self.TVar_var_SpinBox.value())
        except:
            print("TVar var change Warning!")

    def TVar_timesChanged(self):
        try:
            index = self.TVar_ComboBox.currentIndex()
            self.TVar_list[index].set_times(self.TVar_times_SpinBox.value())
        except:
            print("TVar var change Warning!")
    
    def TVar_stepChanged(self):
        try:
            index = self.TVar_ComboBox.currentIndex()
            self.TVar_list[index].set_step(self.TVar_step_SpinBox.value())
            if self.TVar_list[index].step == 0:
                self.TVar_scan_CheckBox.setDisabled(True)
                self.TVar_list[index].set_scan(0)
            else:
                self.TVar_scan_CheckBox.setEnabled(True)
        
            self.TVar_scan_CheckBox.setCheckState(self.TVar_list[index].scan)
        except:
            print("TVar step changeWarning!")
    
    def TVar_scanChanged(self):
        try:
            print("changed")
            index = self.TVar_ComboBox.currentIndex()
            self.TVar_list[index].set_scan(self.TVar_scan_CheckBox.checkState())
        except:
            print("TVar scan changed Warning!")

    def OVar_lbChanged(self):
        try:
            index = self.OVar_ComboBox.currentIndex()
            self.OVar_list[index].set_lb(self.OVar_lb_SpinBox.value())
            if self.OVar_list[index].var < self.OVar_list[index].lb:
                self.OVar_list[index].set_var(self.OVar_list[index].lb)
                self.OVar_var_SpinBox.setValue(self.OVar_list[index].lb)
        
            self.OVar_var_SpinBox.setMinimum(self.OVar_list[index].lb)
            self.OVar_ub_SpinBox.setMinimum(self.OVar_list[index].lb)

        except:
            print("OVar LB CHANGE Warning!")
    
    def OVar_ubChanged(self):
        try:
            index = self.OVar_ComboBox.currentIndex()
            self.OVar_list[index].set_ub(self.OVar_ub_SpinBox.value())
            if self.OVar_list[index].var > self.OVar_list[index].ub:
                self.OVar_list[index].set_var(self.OVar_list[index].ub)
                self.OVar_var_SpinBox.setValue(self.OVar_list[index].ub)

            self.OVar_var_SpinBox.setMaximum(self.OVar_list[index].ub)
            self.OVar_lb_SpinBox.setMaximum(self.OVar_list[index].ub)

        except:
            print("OVar UB CHANGE Warning!")
    
    def OVar_varChanged(self):
        try:
            index = self.OVar_ComboBox.currentIndex()
            self.OVar_list[index].set_var(self.OVar_var_SpinBox.value())
        except:
            print("OVar VAR CHANGE Warning!")
    
    def OVar_timesChanged(self):
        try:
            index = self.OVar_ComboBox.currentIndex()
            self.OVar_list[index].set_times(self.OVar_times_SpinBox.value())
        except:
            print("OVar TIMES CHANGE Warning!")
    
    def OVar_stepChanged(self):
        try:
            index = self.OVar_ComboBox.currentIndex()
            self.OVar_list[index].set_step(self.OVar_step_SpinBox.value())
            if self.OVar_list[index].step == 0:
                self.OVar_scan_CheckBox.setDisabled(True)
                self.OVar_list[index].set_scan(0)
            else:
                self.OVar_scan_CheckBox.setEnabled(True)
                
        
            self.OVar_scan_CheckBox.setCheckState(self.OVar_list[index].scan)
        except:
            print("OVar step Warning!")
    
    def OVar_scanChanged(self):
        try:
            print("OVar scan changed")
            index = self.OVar_ComboBox.currentIndex()
            self.OVar_list[index].set_scan(self.OVar_scan_CheckBox.checkState())
        except:
            print("OVar scan Warning!")

    def AmpVar_lbChanged(self):
        try:
            index = self.AmpVar_ComboBox.currentIndex()
            self.AmpVar_list[index].set_lb(self.AmpVar_lb_SpinBox.value())
            if self.AmpVar_list[index].var < self.AmpVar_list[index].lb:
                self.AmpVar_list[index].set_var(self.AmpVar_list[index].lb)
                self.AmpVar_var_SpinBox.setValue(self.AmpVar_list[index].lb)
        
            self.AmpVar_var_SpinBox.setMinimum(self.AmpVar_list[index].lb)
            self.AmpVar_ub_SpinBox.setMinimum(self.AmpVar_list[index].lb)

        except:
            print("AmpVar Warning!")
    
    def AmpVar_ubChanged(self):
        try:
            index = self.AmpVar_ComboBox.currentIndex()
            self.AmpVar_list[index].set_ub(self.AmpVar_ub_SpinBox.value())
            if self.AmpVar_list[index].var > self.AmpVar_list[index].ub:
                self.AmpVar_list[index].set_var(self.AmpVar_list[index].ub)
                self.AmpVar_var_SpinBox.setValue(self.AmpVar_list[index].ub)
            
        except:
            print("AmpVar Warning!")
    
    def AmpVar_varChanged(self):
        try:
            index = self.AmpVar_ComboBox.currentIndex()
            self.AmpVar_list[index].set_var(self.AmpVar_var_SpinBox.value())
        except:
            print("AmpVar Warning!")

    def AmpVar_timesChanged(self):
        try:
            index = self.AmpVar_ComboBox.currentIndex()
            self.AmpVar_list[index].set_times(self.AmpVar_times_SpinBox.value())
        except:
            print("AmpVar Warning!")

    def AmpVar_stepChanged(self):
        try:
            index = self.AmpVar_ComboBox.currentIndex()
            self.AmpVar_list[index].set_step(self.AmpVar_step_SpinBox.value())
            if self.AmpVar_list[index].step == 0:
                self.AmpVar_scan_CheckBox.setDisabled(True)
                self.AmpVar_list[index].set_scan(0)
            else:
                self.AmpVar_scan_CheckBox.setEnabled(True)
        
            self.AmpVar_scan_CheckBox.setCheckState(self.AmpVar_list[index].scan)
        except:
            print("AmpVar Warning!")
    
    def AmpVar_scanChanged(self):
        try:
            print("changed")
            index = self.AmpVar_ComboBox.currentIndex()
            self.AmpVar_list[index].set_scan(self.AmpVar_scan_CheckBox.checkState())
        except:
            print("AmpVar Warning!")


    def PhVar_lbChanged(self):
        try:
            index = self.PhVar_ComboBox.currentIndex()
            self.PhVar_list[index].set_lb(self.PhVar_lb_SpinBox.value())
            self.PhVar_var_SpinBox.setMinimum(self.PhVar_list[index].lb)
            self.PhVar_ub_SpinBox.setMinimum(self.PhVar_list[index].lb)

            if self.PhVar_list[index].var < self.PhVar_list[index].lb:
                self.PhVar_list[index].set_var(self.PhVar_list[index].lb)
                self.PhVar_var_SpinBox.setValue(self.PhVar_list[index].lb)
        

        except:
            print("PhVar Warning!")
    
    def PhVar_ubChanged(self):
        try:
            index = self.PhVar_ComboBox.currentIndex()
            self.PhVar_list[index].set_ub(self.PhVar_ub_SpinBox.value())
            self.PhVar_var_SpinBox.setMaximum(self.PhVar_list[index].ub)
            self.PhVar_lb_SpinBox.setMaximum(self.PhVar_list[index].ub)
            if self.PhVar_list[index].var > self.PhVar_list[index].ub:
                self.PhVar_list[index].set_var(self.PhVar_list[index].ub)
                self.PhVar_var_SpinBox.setValue(self.PhVar_list[index].ub)

        except:
            print("PhVar Warning!")
    
    def PhVar_varChanged(self):
        try:
            index = self.PhVar_ComboBox.currentIndex()
            self.PhVar_list[index].set_var(self.PhVar_var_SpinBox.value())
        except:
            print("PhVar Warning!")

    def PhVar_timesChanged(self):
        try:
            index = self.PhVar_ComboBox.currentIndex()
            self.PhVar_list[index].set_times(self.PhVar_times_SpinBox.value())
        except:
            print("PhVar Warning!")

    def PhVar_stepChanged(self):
        try:
            index = self.PhVar_ComboBox.currentIndex()
            self.PhVar_list[index].set_step(self.PhVar_step_SpinBox.value())
            if self.PhVar_list[index].step == 0:
                self.PhVar_scan_CheckBox.setDisabled(True)
                self.PhVar_list[index].set_scan(0)
            else:
                self.PhVar_scan_CheckBox.setEnabled(True)
        
            self.PhVar_scan_CheckBox.setCheckState(self.PhVar_list[index].scan)
        except:
            print("PhVar Warning!")
    
    def PhVar_scanChanged(self):
        try:
            print("changed")
            index = self.PhVar_ComboBox.currentIndex()
            self.PhVar_list[index].set_scan(self.PhVar_scan_CheckBox.checkState())
        except:
            print("PhVar Warning!")

    """
    def FVarChannel_Change(self):
        try:
            index = self.FVar_ComboBox.currentIndex()
            self.FVar_list[index].set_channel(self.FVarChannel_ComboBox.currentIndex())
        except:
            print("FVar Warning!")
    
    def TVarChannel_Change(self):
        try:
            index = self.TVar_ComboBox.currentIndex()
            self.TVar_list[index].set_channel(self.TVarChannel_ComboBox.currentIndex())
        except:
            print("TVar Channel Change Warning!")

    def AmpVarChannel_Change(self):
        try:
            index = self.AmpVar_ComboBox.currentIndex()
            self.AmpVar_list[index].set_channel(self.AmpVarChannel_ComboBox.currentIndex())
        except:
            print("AmpVar Warning!")

    def PhVarChannel_Change(self):
        try:
            index = self.PhVar_ComboBox.currentIndex()
            self.PhVar_list[index].set_channel(self.PhVarChannel_ComboBox.currentIndex())
        except:
            print("PhVar Warning!")
    """
    
    def Configure_change(self):
        print("Configure change Warning!")
    
    def ScriptSave(self):
        
        script_name = self.script_dir + "/" + self.name + "_para.py"

        try:
            script_file = open(script_name, "w")
            print("#This is a the list of all defined variables!", file = script_file)

            f_count = 0
            t_count = 0
            ph_count = 0
            amp_count = 0
            o_count = 0

            for var in self.FVar_list:
                if var.name != "None":
                    print(var.name, " = ", var.var, file = script_file)
                    print(var.name + "_lb", " = ", var.lb, file = script_file)
                    print(var.name + "_ub", " = ", var.ub, file = script_file)
                    #print(var.name + "_channel", " = ", var.channel, file = script_file)
                    print(var.name+"_times", " = ", var.times, file = script_file)
                    print(var.name + "_step", " = ", var.step, file = script_file)
                    print(var.name + "_type", " = \'fvar\'", file = script_file)
                    print(var.name + "_name = \'" + var.name + '\'', file = script_file)

                    if var.scan == 0:
                        print(var.name + "_scan = False", file = script_file)
                    else:
                        print(var.name + "_scan = True", file = script_file)
                    
                    f_count = f_count + 1
                
                print(file = script_file)
            
            print("n_fvar =", f_count, file = script_file)

            
            print(file = script_file)
            
            for var in self.TVar_list:
                if var.name != "None":
                    print(var.name, " = ", var.var, file = script_file)
                    print(var.name + "_lb", " = ", var.lb, file = script_file)
                    print(var.name + "_ub", " = ", var.ub, file = script_file)
                    #print(var.name + "_channel", " = ", var.channel, file = script_file)
                    print(var.name+"_times", " = ", var.times, file = script_file)
                    print(var.name + "_step", " = ", var.step, file = script_file)
                    print(var.name + "_type", " = \'tvar\'", file = script_file)
                    print(var.name + "_name = \'" + var.name + '\'', file = script_file)
                    
                    if var.scan == 0:
                        print(var.name + "_scan = False", file = script_file)
                    else:
                        print(var.name + "_scan = True", file = script_file)
                    
                    t_count = t_count + 1
                
                
                print(file = script_file)
            
            print("n_tvar =", t_count, file = script_file)

            print(file = script_file)

            for var in self.AmpVar_list:
                if var.name != "None":

                    print(var.name, " = ", var.var, file = script_file)
                    print(var.name + "_lb", " = ", var.lb, file = script_file)
                    print(var.name + "_ub", " = ", var.ub, file = script_file)
                    #print(var.name + "_channel", " = ", var.channel, file = script_file)
                    print(var.name+"_times", " = ", var.times, file = script_file)
                    print(var.name + "_step", " = ", var.step, file = script_file)
                    print(var.name + "_type", " = \'ampvar\'", file = script_file)
                    print(var.name + "_name = \'" + var.name + '\'', file = script_file)
                    
                    if var.scan == 0:
                        print(var.name + "_scan = False", file = script_file)
                    else:
                        print(var.name + "_scan = True", file = script_file)
                    
                    amp_count = amp_count + 1
                
                print(file = script_file)
            
            print("n_ampvar =", amp_count, file = script_file)



            print(file = script_file)

            for var in self.PhVar_list:
                print()

                if var.name != "None":

                    print(var.name, " = ", var.var, file = script_file)
                    print(var.name + "_lb", " = ", var.lb, file = script_file)
                    print(var.name + "_ub", " = ", var.ub, file = script_file)
                    #print(var.name + "_channel", " = ", var.channel, file = script_file)
                    print(var.name+"_times", " = ", var.times, file = script_file)
                    print(var.name + "_step", " = ", var.step, file = script_file)
                    print(var.name + "_type", " = \'phvar\'", file = script_file)
                    print(var.name + "_name = \'" + var.name + '\'', file = script_file)
                    
                
                    if var.scan == 0:
                        print(var.name + "_scan = False", file = script_file)
                    else:
                        print(var.name + "_scan = True", file = script_file)
                    
                    ph_count = ph_count + 1
                
                print("n_phvar =", ph_count, file = script_file)

                
                print(file = script_file)


            for var in self.OVar_list:
                
                if var.name != "None":

                    print(var.name, " = ", var.var, file = script_file)
                    print(var.name + "_lb", " = ", var.lb, file = script_file)
                    print(var.name + "_ub", " = ", var.ub, file = script_file)
                    #print(var.name + "_channel", " = ", var.channel, file = script_file)
                    print(var.name+"_times", " = ", var.times, file = script_file)
                    print(var.name + "_step", " = ", var.step, file = script_file)
                    print(var.name + "_type", " = \'ovar\'", file = script_file)
                    print(var.name + "_name = \'" + var.name + '\'', file = script_file)

                    if var.scan == 0:
                        print(var.name + "_scan = False", file = script_file)
                    else:
                        print(var.name + "_scan = True", file = script_file)
                    
                    o_count = o_count + 1
                
                print("n_ovar =", o_count, file = script_file)

                
                print(file = script_file)
            
            print(file = script_file)
            print("#___________________________________________", file = script_file)

            print ("var_list = [", end = '', file = script_file)
            
            for var in self.FVar_list:
                if var.name != "None":
                    print(var.name, ", ", sep = "", end = '', file = script_file)
            
            for var in self.TVar_list:
                if var.name != "None":
                    print(var.name, ", ", sep = "", end = '', file = script_file)
            
            for var in self.AmpVar_list:
                if var.name != "None":
                    print(var.name, ", ", sep = "", end = '', file = script_file)
            
            for var in self.PhVar_list:
                if var.name != "None":
                    print(var.name, ", ", sep = "", end = '', file = script_file)
            
            for var in self.OVar_list:
                if var.name != "None":
                    print(var.name, ", ", sep = "", end = '', file = script_file)
            
            print("]", file = script_file)

            print ("var_lb_list = [", end = '', file = script_file)
            
            for var in self.FVar_list:
                if var.name != "None":
                    print(var.name + "_lb", ", ", sep = "", end = '', file = script_file)
            
            for var in self.TVar_list:
                if var.name != "None":
                    print(var.name + "_lb", ", ", sep = "", end = '', file = script_file)
            
            for var in self.AmpVar_list:
                if var.name != "None":
                    print(var.name + "_lb", ", ", sep = "", end = '', file = script_file)
            
            for var in self.PhVar_list:
                if var.name != "None":
                    print(var.name + "_lb", ", ", sep = "", end = '', file = script_file)
            
            for var in self.OVar_list:
                if var.name != "None":
                    print(var.name + "_lb", ", ", sep = "", end = '', file = script_file)
            
            print("]", file = script_file)

            print ("var_ub_list = [", end = '', file = script_file)
            
            for var in self.FVar_list:
                if var.name != "None":
                    print(var.name + "_ub", ", ", sep = "", end = '', file = script_file)
            
            for var in self.TVar_list:
                if var.name != "None":
                    print(var.name + "_ub", ", ", sep = "", end = '', file = script_file)
            
            for var in self.AmpVar_list:
                if var.name != "None":
                    print(var.name + "_ub", ", ", sep = "", end = '', file = script_file)
            
            for var in self.PhVar_list:
                if var.name != "None":
                    print(var.name + "_ub", ", ", sep = "", end = '', file = script_file)
            
            for var in self.OVar_list:
                if var.name != "None":
                    print(var.name + "_ub", ", ", sep = "", end = '', file = script_file)
            
            print("]", file = script_file)

            print ("var_step_list = [", end = '', file = script_file)
            
            for var in self.FVar_list:
                if var.name != "None":
                    print(var.name + "_step", ", ", sep = "", end = '', file = script_file)
            
            for var in self.TVar_list:
                if var.name != "None":
                    print(var.name + "_step", ", ", sep = "", end = '', file = script_file)
            
            for var in self.AmpVar_list:
                if var.name != "None":
                    print(var.name + "_step", ", ", sep = "", end = '', file = script_file)
            
            for var in self.PhVar_list:
                if var.name != "None":
                    print(var.name + "_step", ", ", sep = "", end = '', file = script_file)
                    
            
            for var in self.OVar_list:
                if var.name != "None":
                    print(var.name + "_step", ", ", sep = "", end = '', file = script_file)                    
            
            print("]", file = script_file)

            print ("var_times_list = [", end = '', file = script_file)
            
            for var in self.FVar_list:
                if var.name != "None":
                    print(var.name + "_times", ", ", sep = "", end = '', file = script_file)
            
            for var in self.TVar_list:
                if var.name != "None":
                    print(var.name + "_times", ", ", sep = "", end = '', file = script_file)
            
            for var in self.AmpVar_list:
                if var.name != "None":
                    print(var.name + "_times", ", ", sep = "", end = '', file = script_file)
            
            for var in self.PhVar_list:
                if var.name != "None":
                    print(var.name + "_times", ", ", sep = "", end = '', file = script_file)
                    
            
            for var in self.OVar_list:
                if var.name != "None":
                    print(var.name + "_times", ", ", sep = "", end = '', file = script_file)                    
            
            print("]", file = script_file)

            print ("var_scan_list = [", end = '', file = script_file)
            
            for var in self.FVar_list:
                if var.name != "None":
                    print(var.name + "_scan", ", ", sep = "", end = '', file = script_file)                    
            
            for var in self.TVar_list:
                if var.name != "None":
                    print(var.name + "_scan", ", ", sep = "", end = '', file = script_file)  
            
            for var in self.AmpVar_list:
                if var.name != "None":
                    print(var.name + "_scan", ", ", sep = "", end = '', file = script_file)  
            
            for var in self.PhVar_list:
                if var.name != "None":
                    print(var.name + "_scan", ", ", sep = "", end = '', file = script_file)  
            
            for var in self.OVar_list:
                if var.name != "None":
                    print(var.name + "_scan", ", ", sep = "", end = '', file = script_file)  
            
            print("]", file = script_file)

            print ("var_type_list = [", end = '', file = script_file)
            
            for var in self.FVar_list:
                if var.name != "None":
                    print(var.name + "_type", ", ", sep = "", end = '', file = script_file)                    
            
            for var in self.TVar_list:
                if var.name != "None":
                    print(var.name + "_type", ", ", sep = "", end = '', file = script_file)  
            
            for var in self.AmpVar_list:
                if var.name != "None":
                    print(var.name + "_type", ", ", sep = "", end = '', file = script_file)  
            
            for var in self.PhVar_list:
                if var.name != "None":
                    print(var.name + "_type", ", ", sep = "", end = '', file = script_file)  
            
            for var in self.OVar_list:
                if var.name != "None":
                    print(var.name + "_type", ", ", sep = "", end = '', file = script_file)  

            
            print("]", file = script_file)

            print ("var_name_list = [", end = '', file = script_file)
            
            for var in self.FVar_list:
                if var.name != "None":
                    print(var.name + "_name", ", ", sep = "", end = '', file = script_file)                    
            
            for var in self.TVar_list:
                if var.name != "None":
                    print(var.name + "_name", ", ", sep = "", end = '', file = script_file)  
            
            for var in self.AmpVar_list:
                if var.name != "None":
                    print(var.name + "_name", ", ", sep = "", end = '', file = script_file)  
            
            for var in self.PhVar_list:
                if var.name != "None":
                    print(var.name + "_name", ", ", sep = "", end = '', file = script_file)  
            
            for var in self.OVar_list:
                if var.name != "None":
                    print(var.name + "_name", ", ", sep = "", end = '', file = script_file)  

            
            print("]", file = script_file)

            print("#____________________________________________", file = script_file)

            
            print("#END", file = script_file)
            
            script_file.close()

        except:
            print("SCRIPT SAVE Warning!")

    def ExpDirSet(self):
        try:
            directory = self.ExpDir_LineEdit.text()
            print(directory)
            if os.path.exists(directory):
                self.exp_dir = directory
                self.ExpScriptRun_Button.setEnabled(True)
                self.ExpScriptView_Button.setEnabled(True)
            else:
                self.ExpScriptRun_Button.setDisabled(True)
                self.ExpScriptView_Button.setDisabled(True)
        except:
            pass
    
    def ExpScriptView(self):
        time.sleep(0.001)
        try:
            if os.path.exists(self.exp_dir):
                os.system("notepad " + self.exp_dir)
        except:
            pass
    
    def WinConfigView(self):
        try:
            if os.path.exists(self.winconfig_dir):
                os.system("notepad " + self.winconfig_dir)
        except:
            pass
    
    def ExpScriptRun(self):
        print("~")
        try:
            
            if os.path.exists(self.exp_dir):
                print("python \" "+ self.exp_dir + "\"")
                os.system("python \""+ self.exp_dir + "\"")
        except:
            pass


##--------------------------------------------------------------------------------

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    win = SubExperiment("TEST")
    ##win.SubExperiment_Dialog.setCentralWidget(win.centralWidget)
    win.SubExperiment_Dialog.show()
    sys.exit(app.exec_())
