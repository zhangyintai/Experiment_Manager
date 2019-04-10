<h1>Experiment Manager</h1>
<h3>This Experiment Manager is used for IonTrap Team of Prof. Yiheng Lin only!</h3><br>

# Some basic features:
  - Using the grammer of python directly.
  - Direct control of the DDS.
  - Scalable user-defined functions.
  - Robustness for user's hecking
  - A series of scans can be done by loops<br>
 
# Requirements:
  - Microsoft Windows operating system
  - Python 3.6.x
  - The driver for the DDS
  - numpy, scipy, matplotlib module (for interface development, pyqt5 module is required)
  - Install the driver of required boards.

# Usage:
## Install the driver of the DDS
1. Download the drivers from the "Drivers" folder of this repository.
2. Switch on the the DDS with waveform generator and the power source well-set.
3. Turn of the DDS and connect the DDS with the computer
4. Start the Device Manager
5. Right click at the device, install the driver manually.
   
## Configure the experiment by GUI
### Configure the subwindow of the experiment
1. Generate the configuration file for a subexperiment
  1. Build the variable list by "SubExperimentConfigureFileGenerator_Template.py". <br>Set the name of the experiment and the filename with suffix ".zyt". Notice that
     1. The variables should be classified by types (FVar, TVar, AmpVar, PhVar, OVar).
     2. Variable should not be named as "None".
     3. The define of the variable should follow such format("type_of_the_variable"_list.append(name_of_the_var,lb, ub, var, llb, uub))
  2. Run the script
2. Run the "subexperiment.py" and import the configuration file which was generated previously. Adjust the parameters and save the adjusted parameters to the directory that the script for the program will be contained in.
3. Write the script file of the experiment.
   1. import "Functions.py". It's more convenient to use `from Functions import *` to import all the functions in the script.
   2. import the script that contains parameters, which is often named "NameOfTheExperiment_para.py". Use `from NameOfTheExperiment_para import *` for the same reason.
   3. import "device.py"
   4. Check the output by oscilloscope. 
4. Import the script file to the window of the subexperiment that was just configured.
5. Run the script.

## Initial the DDS
1. Import the device script: <br>`import device`
2. Set the fpga: <br>`fpga = device.FPGA(1, False)`<br> Here we only have one FPGA currently.
3. Initial the DDS: <br>`fpga.initial_dds()`

## The units
  - Frequency: The unit of frequencies are MHz (not the circular frequency).
  - Time: The unit of times are microsecond.
  - Phase: The unit of phases are $\pi$.
  - Amplitude: The unit of the amplitudes are normalized to the maximum possible output of the given frequency. (The value of the amplitude takes from 0 to 1.)
  - Other variables: The units of other variables are defined by users according to their settings.

## Output a continuous waveform
After the DDS is initialized, use the command<br>`fpga.cw_play(channel, amplitude, frequency, phase)`<br>
Notice:
1. To stop the continuous waveform, set amplitude, frequency and phase all to 0 and clear the phase using the command<br>`fpga.phase_clear_dds([channel])`
2. If the channel is used to perform a series of pulses, the channel must be stopped from the continuous mode and clear the phase.
Example:
```
# An example for a continuous waveform generation
import device
import time

channel = 0 # Use 0th channel
amplitude = 1 # The amplitude is set as 1
frequency = 1 # The frequency is 1 MHz
phase = 1 # The initial phase is pi

fpga = device.FPGA(1, False)
fpga.initial_dds() # Initial the DDS
fpga.cw_play(channel, amplitude, frequency, phase) # Start the continuous waveform

time.sleep(1) # The waveform is a second long approximately.

fpga.cw_play(channel, 0, 0, 0) # Stop the continuous waveform
fpga.phase_clear_dds([channel]) # Clear the phase
```
   
## Build a series of pulses
To build a series of pulses, we will use some commands for multi-controlling:
  - `fpga.sequence_data_download(channel_list, data_list)`
  - `fpga.play([times, 0, 0])`
  - `fpga.phase_clear_dds(channel_list)`.
The command "sequence_data_download" is for downloading the data to the DDS. Notice that
  1. The lengths of the channel_list and the data_list should be the same.
  2. The elements in the data_list is a list. The format the element in the data_list is `[0, [amplitude, frequency, phase], [ttl_status], time]` where the first parameter 0 is fixed. `ttl_status` can be chosen from "high" and "low".
  3. The phases accumulate on the channels will be cleared automatically after the function `fpga.play([time, 0, 0])` returns.
  4. The phase will continue accumulating for an waveform whose amplitude is zero except its frequency is also set to zero.
  5. If the DDS stop working, please reset the DDS. (There's a reset button on the DDS.)<br>

Example:
```
# An example for DDS to play a set of waveforms

import device
import time

channel_list = [0, 1] # We use channel 0 and channel 1
data_list = [[], []]

fpga = device.FPGA(1, False)
fpga.initial_dds() # Initial the DDS

# The waveforms that are to be played by the two channels
data_list[0].append([0, [0, 0, 0], ['low', 20]])
data_list[0].append([0, [1, 1, 0], ['high', 20]])
data_list[0].append([0, [0, 0, 0], ['low', 20]])

data_list[1].append([0, [1, 1, 0], ['low', 20]])
data_list[1].append([0, [0, 0, 0], ['high', 20]])
data_list[1].append([0, [1, 1, 0], ['low', 20]])

fpga.sequency_data_download(channel_list, data_list)
fpga.play([5, 0, 0]) # Play 5 times and will get 5 results from the PMT.
```

## User-defined functions
The user-defined functions should be put in the "Functions.py" and should be named by: "IonTrap_*functionname*". For example:
```
def IonTrap_HelloWorld():
  
  print("Hello World!")
```
The format of the input variables should be marked out clearly in the comment. The information of the returned value of the function should also be given if possible.

## Running scans
There's a built-in Ramsey in the "Functions.py". The parameters are listed clearly in the file. A series of scans can be run at a time by loops. Notice that these lists are generated by the GUI after the parameters are saved to "*TheNameOfTheExperiment*_para.py"
```var_list```, ```var_lb_list```, ```var_ub_list```, ```var_step_list```, ```var_times_list```, ```var_scan_list```, ```var_type_list```, ```var_name_list```.

## Other functions
They are still under testing and developing. Coming soon.

## The control of the DAC
The control of the DAC is much easier than the control of DDS. The DAC is controlled by the FPGA on the DDS board. Here we use a DAC manufactured by Analog Device. Its model is EVAL-AD5371EBZ. The command for the DAC to operate the DAC is `fpga.ad5371_play(channel_list, data_list)`. The format of the `data_list` is a list of lists, namely`[[ch1_1, ch2_1, ..., ], [ch1_2, ch2_2, ..., ...], ..., ...]`. The inner list contains the voltages for different channels.

Example:
```
import device
import numpy as np
import time

#Initialize FPGA
fpga = device.FPGA(1, False)
fpga.initial_dds()

data_list = []
ch_list = [0, 39] # We use channel 0 and channel 39

# Create a set of points
for i in range (0, 500):
  data_list.append([])
  data_list[i].append(-4)
  data_list[i].append(-2 * i / 1000)

fpga.ad5371_play(ch_list, data_list) 
```
Notice that the refresh time of AD5371 is set by $T_{r}=(N_{ch}\times 107+59+113)\times 8$ ns. The range of the ouput is $-10$ V to $10$ V.

## Shortcuts:
Press F1 in the GUI guides you to http://www.bilibili.com/.<br>
Press F2 in the GUI guides you to https://arxiv.org/.

## Comments and suggestions
Mail to zhangyintai@hotmail.com or ustczyt@mail.ustc.edu.cn.

## Acknowledgement
The author expresses his appreciations to PyQt5 and Eric6 for their convenience. He also wants to thank Mingdong Zhu for the design of the DDS board and also the School of Physical Sciences of USTC and CAS Key Laboratory of Micro-scale Magnetic Resonance for equipments and financial supports.
