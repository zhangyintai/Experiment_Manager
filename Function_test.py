from Functions import *
from Ramsey_para import *
import device
import time
from matplotlib import pyplot as plt
import numpy as np

fpga = device.FPGA(1, False)

IonTrap_Doppler(1, 1, fpga, 7, stop = True)

for i in range (0, len(var_list)):
    aver_result = []
    scan_list = scan_generate(10, 100, 10)
    print(scan_list)
    result = IonTrap_Ramsey(scan_list, [amp_ramsey, f, t1, t2, t3, phvar, 4], var_type_list[i], fpga, [4, 5, 6], scan_apply = var_scan_list[i], spin_echo = True, test_mode = True, test_channel = 8)
    print("################################################################################")
    if result != [[]]:

        print("The result of function_test is", result[2])
        aver_result = IonTrap_Average(result[2])[0]
        print(aver_result)

        fig1 = plt.figure()
        fig1 = plt.scatter(scan_list, aver_result)
        plt.xlabel(var_name_list[i])
        plt.ylabel("Test")
        plt.title("original data")
        plt.show()
        fit_param = IonTrap_PolyFit(1, scan_list, aver_result, init = [0, 0])[0]
        fig2 = plt.figure()
        fig2 = plt.plot(np.linspace(10, 100, num = 20), fit_param[0] + fit_param[1] * np.linspace(10, 100, num = 20))
        plt.ylabel("Test")
        plt.title("fitted data")
        plt.show()


    print("################################################################################")



IonTrap_Doppler(1, 1, fpga, 4)

