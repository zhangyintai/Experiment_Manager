from Functions import *
import numpy
from Experiment_scripts import Exp_Script_Dir
import os

for i in range (0,10):
    os.system(IonTrap_ToRunCommand(Exp_Script_Dir['name_change']))