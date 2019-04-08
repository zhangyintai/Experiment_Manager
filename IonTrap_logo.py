import device
import numpy as np
import time

fpga = device.FPGA(1, False)
fpga.initial_dds()
raw_data_list = []
ch_list = [0, 39]
for i in range (0, 500):
    raw_data_list.append([])
    raw_data_list[i].append(-2 -2)
    raw_data_list[i].append(2.5 - 2 * i / 1000)

for i in range (500, 1500):
    raw_data_list.append([])
    raw_data_list[i].append(0.5 * np.sin(2 * np.pi * i / 1000) - 2)
    raw_data_list[i].append(0.5 * np.cos(2 * np.pi * i / 1000) + 2)

for i in range (1500, 2000):
    raw_data_list.append([])
    raw_data_list[i].append(2 - 2)
    raw_data_list[i].append(2.5 - 2 * (i - 1500) / 1000)

for i in range (2000, 2500):
    raw_data_list.append([])
    raw_data_list[i].append(2 +  2 * (i - 2000) / 1000 - 2)
    raw_data_list[i].append(2.5 - 2 * (i - 2000) / 1000)

for i in range (2500, 3000):
    raw_data_list.append([])
    raw_data_list[i].append(3 - 2)
    raw_data_list[i].append(2.5 - 2 * (i - 2500) / 1000)

for i in range (3000, 3500):
    raw_data_list.append([])
    raw_data_list[i].append(5 - 2)
    raw_data_list[i].append(2.5 - 2 * (i - 3000) / 1000)

for i in range (3500, 4000):
    raw_data_list.append([])
    raw_data_list[i].append(4.5 + (i - 3500) / 500 - 2)
    raw_data_list[i].append(2.5 )

for i in range (4000, 4500):
    raw_data_list.append([])
    raw_data_list[i].append(6.5 - 2)
    raw_data_list[i].append(2.5 - 2 * (i - 4000) / 1000)

for i in range (4500, 5000):
    raw_data_list.append([])
    raw_data_list[i].append(6.5 + 1.5 *(i - 4500) / 1000 - 2)
    raw_data_list[i].append(2 - (i - 4500) / 1000)

for i in range (5000, 5500):
    raw_data_list.append([])
    raw_data_list[i].append(6.5 + (i - 5000) / 1000 - 2)
    raw_data_list[i].append(2)

for i in range (5500, 6000):
    raw_data_list.append([])
    raw_data_list[i].append(6.5 + (i - 5500) / 1000 - 2)
    raw_data_list[i].append(2.5)

for i in range (6000, 6500):
    raw_data_list.append([])
    raw_data_list[i].append(7 + 0.25 * np.sin(2 * np.pi * i / 1000) - 2)
    raw_data_list[i].append(0.25 + 0.25 * np.cos(2 * np.pi * i / 1000) + 2)

for i in range (6500, 7000):
    raw_data_list.append([])
    raw_data_list[i].append(8+ 1 * (i -6500) / 1000 - 2)
    raw_data_list[i].append(1.5 +2 * (i -6500) / 1000)

for i in range (7000, 7500):
    raw_data_list.append([])
    raw_data_list[i].append(8.5 + 1 * (i -7000) / 1000 - 2)
    raw_data_list[i].append(2.5 -2 * (i -7000) / 1000)

for i in range (7500, 8000):
    raw_data_list.append([])
    raw_data_list[i].append(8 + 0.75 * (i -7000) / 1000 - 2)
    raw_data_list[i].append(1.75)

for i in range (8000, 8500):
    raw_data_list.append([])
    raw_data_list[i].append(10 - 2)
    raw_data_list[i].append(2.5 - 2 * (i-8000) / 1000)

for i in range (8500, 9000):
    raw_data_list.append([])
    raw_data_list[i].append(10 + (i - 8500) / 1000 - 2)
    raw_data_list[i].append(2)

for i in range (9000, 9500):
    raw_data_list.append([])
    raw_data_list[i].append(10 + (i - 9000) / 1000 - 2)
    raw_data_list[i].append(2.5)

for i in range (9500, 10000):
    raw_data_list.append([])
    raw_data_list[i].append(10.5 - 0.25 * np.sin(2 * np.pi * i / 1000) - 2)
    raw_data_list[i].append(0.25 - 0.25 * np.cos(2 * np.pi * i / 1000) + 2)



fpga.ad5371_play(ch_list, raw_data_list)
