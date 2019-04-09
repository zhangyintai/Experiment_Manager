<h1>Experiment Manager</h1>
<h3>This Experiment_Manager is used for IonTrap Team of Prof. Yiheng Lin only!</h3><br>

# Some basic features:
  - Using the grammer of python directly.
  - Direct control of the DDS.
  - Scalable user-defined functions.
  - Robustness for user's hecking<br>
 
# Requirements:
  - Microsoft Windows operating system
  - Python 3.6.x
  - The driver for the DDS
  - numpy, scipy, matplotlib module (for interface development, pyqt5 module is required)

# Usage:
## Configure the experiment by GUI
### Configure the subwindow of the experiment
1. Install the driver of the DDS
   1. Switch on the the DDS with waveform generator and the power source well-set.
2. Generate the configuration file for a subexperiment
  1. Build the variable list by "SubExperimentConfigureFileGenerator_Template.py". <br>Set the name of the experiment and the filename with suffix ".zyt". Notice that
     1. The variables should be classified by types (FVar, TVar, AmpVar, PhVar, OVar).
     2. Variable should not be named as "None".
     3. The define of the variable should follow such format("type_of_the_variable"_list.append(name_of_the_var,lb, ub, var, llb, uub))
  2. Run the script
3. Run the "subexperiment.py" and import the configuration file which was generated previously. Adjust the parameters and save the adjusted parameters to the directory that the script for the program will be contained in.
4. Write the script file of the experiment.
   1. import "Functions.py"
   2. import the script that contains parameters, which is often named "NameOfTheExperiment_para.py"
   3. import "device.py"
   4. Check the output by oscilloscope. 
5. Import the script file to the window of the subexperiment that was just configured.
6. Run the script.
