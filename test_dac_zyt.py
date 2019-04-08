import device
import numpy as np
import time

fpga = device.FPGA(1, False)
fpga.initial_dds()
data_list = []
file = []
ch_list = []

# get data

for i in range (0, 10):
    file.append(open("Z:\\Installation for dds\\Python3\\Python_main\\" + str(i) + ".txt", "r"))
    data_list.append([])
    print("file", i, "has read!")
    lines = file[i].readlines()
    for line in lines:
        if line != '':
            data_list[i].append(float(line))

    ch_list.append(i)
fpga.ad5371_play(ch_list, [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], play_sign=True)
# generate raw_wave_list
raw_data_list = []

for i in range (0, len(data_list[0])):
    raw_data_list.append([])
    for j in range (0, 10):
        raw_data_list[i].append(data_list[j][i])

print(raw_data_list[0])
print(len(ch_list))

time.sleep(1)
fpga.ad5371_play(ch_list, raw_data_list)
