from DataType import FVar, TVar, AmpVar, PhVar, OVar
import Functions
import os

FVar_list = []
TVar_list = []
AmpVar_list = []
PhVar_list = []
OVar_list = []

OutputFileName = "Unknown.zyt"
Title = "Unknown"

def ToConfigFile():

    os.chdir(os.path.dirname(__file__))
    CurrentDir = (os.getcwd()) + "\\"
    print(CurrentDir)

    OutputFileName.replace(' ','')

    OutputFile = open(CurrentDir + OutputFileName, 'w+')

    if len(FVar_list) == 0:
        FVar_list.append(FVar("None", 0, 0, 0, 0, 0))
    
    if len(TVar_list) == 0:
        TVar_list.append(TVar("None", 0, 0, 0, 0, 0))

    if len(AmpVar_list) == 0:
        AmpVar_list.append(AmpVar("None", 0, 0, 0, 0, 0))

    if len(PhVar_list) == 0:
        PhVar_list.append(PhVar("None", 0, 0, 0, 0, 0))
    
    if len(OVar_list) == 0:
        OVar_list.append(OVar("None", 0, 0, 0, 0, 0))
    

    print(Title, file = OutputFile)    
    print(len(FVar_list), file = OutputFile)
    for i in range(0, len(FVar_list)):
        print(FVar_list[i].name, FVar_list[i].lb, FVar_list[i].ub, FVar_list[i].var, FVar_list[i].llb, FVar_list[i].uub, file = OutputFile)
    
    print(len(TVar_list), file = OutputFile)
    for i in range(0, len(TVar_list)):
        print(TVar_list[i].name, TVar_list[i].lb, TVar_list[i].ub, TVar_list[i].var, TVar_list[i].llb, TVar_list[i].uub, file = OutputFile)
    
    print(len(AmpVar_list), file = OutputFile)
    for i in range(0, len(AmpVar_list)):
        print(AmpVar_list[i].name, AmpVar_list[i].lb, AmpVar_list[i].ub, AmpVar_list[i].var, AmpVar_list[i].llb, AmpVar_list[i].uub, file = OutputFile)
    
    print(len(PhVar_list), file = OutputFile)
    for i in range(0, len(PhVar_list)):
        print(PhVar_list[i].name, PhVar_list[i].lb, PhVar_list[i].ub, PhVar_list[i].var, PhVar_list[i].llb, PhVar_list[i].uub, file = OutputFile)

    print(len(OVar_list), file = OutputFile)
    for i in range(0, len(OVar_list)):
        print(OVar_list[i].name, OVar_list[i].lb, OVar_list[i].ub, OVar_list[i].var, OVar_list[i].llb, OVar_list[i].uub, file = OutputFile)
    
    ##print ('--END--', sep = '', end = '', file = OutputFile)
    OutputFile.close()

## ---------------------Script Begin-----------------------------

FVar_list.append(FVar("f", 0, 100, 50, 0, 10000))
TVar_list.append(TVar("t1", 0, 40, 20, 0, 10000))
TVar_list.append(TVar("t2", 0, 60, 30, 0, 10000))
TVar_list.append(TVar("t3", 0, 80, 40, 0, 10000))
AmpVar_list.append(AmpVar("amp_ramsey", 0, 1, 1, 0, 1))
AmpVar_list.append(AmpVar("amp_detect", 0, 1, 1, 0, 1))
AmpVar_list.append(AmpVar("amp_pumping", 0, 1, 1, 0, 1))
PhVar_list.append(PhVar("phvar", 0, 2, 0, 0, 4))


## -----------------------Script End-----------------------------

Title = "Ramsey"
OutputFileName = "Ramsey.zyt" ##The spaces in the OutputFile will be diminished
ToConfigFile()

##DO NOT DELETE THE FOLLOWING SHARPS
##########