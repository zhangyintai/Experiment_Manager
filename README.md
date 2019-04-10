<h1>Experiment Manager</h1>
<h3>This Experiment Manager is used for IonTrap Team of Prof. Yiheng Lin only!</h3><br>

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
  - Install the driver of required boards.

# Usage:
## Install the driver of the DDS
1. Download the drivers from the "Drivers" folder of this repository.
2. Turn of the DDS and connect the DDS with the computer
3. Start the Device Manager
4. Right click at the device, install the driver manually.
   
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
   1. import "Functions.py". It's more convenient to use `from Functions import *` to import all the functions in the script.
   2. import the script that contains parameters, which is often named "NameOfTheExperiment_para.py". Use `from NameOfTheExperiment_para import *` for the same reason.
   3. import "device.py"
   4. Check the output by oscilloscope. 
5. Import the script file to the window of the subexperiment that was just configured.
6. Run the script.

## Initial the DDS
1. Import the device script: <br>`import device`
2. Set the fpga: <br>`fpga = device.FPGA(1, False)`<br> Here we only have one FPGA currently.
3. Initial the DDS: <br>`fpga.initial_dds()`

## Output a continuous waveform
After the DDS is initialized, use the command<br>`fpga.cw_play(channel, amplitude, frequency, phase)`<br>
Notice:
1. To stop the continuous waveform, set amplitude, frequency and phase all to 0 and clear the phase using the command<br>`fpga.phase_clear_dds([channel])`
2. If the channel is used to perform a series of pulses, the channel must be stopped from the continuous mode and clear the phase.
Example
```
# An example for a continuous waveform generation
import device
import time

channel = 0 # Use 0th channel
amplitude = 1 # The amplitude is set as 1
frequency = 1 # The frequency is 1 MHz
phase = 1 # The initial phase is pi

fpga = device.FPGA(1, False)
fpga.cw_play(channel, amplitude, frequency, phase) # Start the continuous waveform

time.sleep(1) # The waveform is a second long approximately.

fpga.cw_play(channel, 0, 0, 0) # Stop the continuous waveform
fpga.phase_clear_dds([channel]) # Clear the phase
```
   
## Build a series of pulses
To build a series of pulses, we will use some commands for multi-controlling
```
```
