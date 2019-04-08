# coding=UTF-8
"""
--------------------------------------------------------
Copyright (c) ****-2018 ESR, Inc.  All rights reserved.
--------------------------------------------------------
Author: Mingdong Zhu
Date:  2019/03/07
Design Name: The user interface of the DDS software
Purpose: Design an UI and test function for DDS board
         using Python 3.6.3
--------------------------------------------------------
"""
# _name_ = 'main_process'
import time
import numpy as np
import dds


def num_to_bytes(num, bytenum, high_head=True):
    """To get the bytes format of a given decimal number
    (used for data_pro)

    :param num: A given number
    :type num: int
    :param bytenum: The number of` bytes (or len()) of the return word
    :type bytenum: int
    :param high_head: True/False -- big/little-endian; eg:num_to_bytes(1, 2, True/False)-->b'\x00\x01' or b'\x01\x00'
    :type high_head: bool

    :returns: Bytes for num, len() = bytenum
    :rtype: bytes
    """
    if high_head:
        return np.array([num], dtype='>u8').tobytes()[-bytenum:]  # big-endian
    else:
        return np.array([num], dtype='<u8').tobytes()[:bytenum]  # little-endian


def bytes_to_num(bytes_, signed_=True, big_=True):
    """To get the int format of a given bytes
    (used for data_pro)

    :param bytes_: A given bytes
    :type bytes_: bytes
    :param signed_: True for signed input
    :type signed_: bool
    :param big_: Same as the "high_head" in the function 'num_to_bytes'
    :type big_: bool

    :returns: Int for bytes
    :rtype: int
    """
    if not signed_:
        if big_:
            return int.from_bytes(bytes_, byteorder='big')
        else:
            return int.from_bytes(bytes_, byteorder='little')
    else:
        if big_:
            return int.from_bytes(bytes_, byteorder='big', signed=True)
        else:
            return int.from_bytes(bytes_, byteorder='little', signed=True)


def bytes_to_hexstr(bytes_, space=True):
    """To get the string format of a given bytes
    (used for print/debug)

    :param bytes_: A given bytes
    :type bytes_: bytes
    :param space: True for insert a ' ' per byte
    :type space: bool

    :returns: String for bytes
    :rtype: str
    """
    # ss = s_str.encode('hex') # original solution in Python2
    string = bytes_.hex() # original solution in Python2
    if space:
        string_with_space = [string[i:i + 2] for i in range(0, len(string), 2)]
        return ' '.join(string_with_space)
    else:
        return string


class FPGA(dds.HardWare):  # GenWave,
    """ A class used for integration, in other word, the final application """

    """To clarify the user-defined scan-sign ******
    
    var_type = [0, 1, 2, 3, 4], which is show the scan_para's variable type
               [0, 1, 2, 3, 4] represents ["no scan", "amp", "freq", "phase", "time"]
    scan_sign = [0, 1, 2, 3, 4] + 4*(para_num), which show the scan_para's type and group number
    para_num = 0, 1...; The group number for the scan_para 
    """

    def __init__(self, dev_index=0, test_mode=False):
        """ To launch the Instantiation of classes"""
        # GenWave.__init__(self)
        dds.HardWare.__init__(self, dev_index=dev_index, test_mode=test_mode)

    def cw_play(self, ch_num, amp, freq, phase):
        """Single channel setting for DDS
        (can be applied in spectrum test or non-sequence wave_play)

        :param ch_num: The number ch to be set, [0,1,...,15] is available
        :type ch_num: int
        :param amp: Amplitude of DDS, range:[0,1]
        :type amp: float
        :param freq: Frequency of DDS, unit: MHz
        :type freq: int or float
        :param amp: Phase of DDS, unit: pi, range: [0,2)
        :type amp: float

        :returns: unit: MHz, Hz
        :rtype: float, float
        """
        hp_channel, reg_wr = self.ch2identify(ch_num)
        ch_num_byte = num_to_bytes(2**ch_num, 2)

        dds_data_list = self.dds_data_form(hp_channel, amp, freq, phase)
        print(bytes_to_hexstr(dds_data_list[0]))
        self.l_configure(ch_num_byte, reg_wr, dds_data_list[0])
        """
        return specification:
        1--the real digital freq (set)
        2--the difference of freq (real - set)
        """
        return dds_data_list[1], dds_data_list[2]

    def ttl_set(self, ch_num, level):
        """To set the TTL manually

        :param ch_num: channel number of TTL, [0,1] correspond to TTL9,10 and 0x5/6 0,1
        :type ch_num: int
        :param level: 0/1 for low and high
        :type level: int

        :returns:
        :rtype:
        """
        word_in_num = 5*16 + ch_num + 16*level
        word_in_bytes = num_to_bytes(word_in_num % 256, 2)

        print(bytes_to_hexstr(word_in_bytes))
        self.write(word_in_bytes)

    def ad5371_ini(self):
        """To initialize the AD5371 which is a 40-ch low-speed DAC

        :param :
        :type :

        :returns:
        :rtype:
        """
        self.write(b'\x00\x34'+b'\x00'+b'\x02'+b'\x20\x00')  # the b'\x02' can be b'\x03',b'\x04'
        self.write(b'\x00\x34'+b'\x00'+b'\x03'+b'\x20\x00')  # the OFS_g1 is set to be +10V.
        self.write(b'\x00\x34'+b'\x00'+b'\x04'+b'\x20\x00')  # the OFS_g2~4 is set to be +10V.

        self.write(b'\x00\x34'+b'\x00'+b'\x80'+b'\x80\x00')  # C
        self.write(b'\x00\x34'+b'\x00'+b'\x40'+b'\xFF\xFC')  # M
        self.write(b'\x00\x34'+b'\x00'+b'\xC0'+b'\x80\x00')  # X = +10

        stamp_list = [0, 1, 3]
        self.ad5371_wr_stamp_set(stamp_list)  # To set the SPI rate
        # self.ad5371_play_set(ch_num, [106, 59, 111])
        print('AD5371 initial has been finished')

    #################################################################
    # integration-experiment function
    # 以下都是支持多个通道的操作
    #################################################################
    def initial_dds(self):
        """To initialize and synchronize the 16 DDSs

        :param :
        :type :

        :returns:
        :rtype:
        """
        ch_num_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.delay_para_set()
        self.sync_on()
        for index_1 in range(len(ch_num_list)):
            if ch_num_list[index_1] < 4:
                self.initial_AD9915(ch_num_list[index_1])
            else:
                self.initial_ad9910(ch_num_list[index_1])
        self.mannual_sync_2g5()
        self.mannual_sync_1g()
        self.sync_off()
        self.stamp_reset()    # When there are some bugs, this one will be used
        print('channel ', ch_num_list, ' initial has been finished')

    def phase_clear_dds(self, ch_num_list):
        """To clear the phase of DDS in ch_num_list, after that the phase in accumulator will be 0
        What's more, if a dds is play at a freq != 0, we need to stop it and clear the phase for "sequence play".

        :param ch_num_list: List of ch_num(int), ch_num can be [0,1,..15]
        :type ch_num_list: list

        :returns:
        :rtype:
        """
        for index_1 in range(len(ch_num_list)):
            if ch_num_list[index_1] < 4:
                self.phase_clear_2g5(ch_num_list[index_1])
            else:
                self.phase_clear_1g(ch_num_list[index_1])
        # print 'phase of channel ',ch_num_list,' has been cleared'

    def sequence_data_download(self, ch_num_list, raw_data_list_list, check_sign=False):
        """To download the sequence play data for multi channels

        :param ch_num_list: List of ch_num(int), ch_num can be [0,1,..15]
        :type ch_num_list: list
        :param raw_data_list_list: List of raw_data_list(for one channel)
            :*** format of raw_data_list: [  [scan_sign,[A,f(MHz),fai(pi)],[level,time]],  ...]
            :*** eg: [  [scan_sign0,[A0, f0, fai0],[level0, time0]],  [scan_sign1,[A1, f1, fai1],[level1, time1]], ... ]
            : scan_sign: int, [0,1, .. ,4,5,..8]--["no scan", "amp"_0, "freq"_0, "phase"_0, "time"_0]
            : amp: float, range: [0,1]
            : freq: int or float, unit: MHz
            : phase: float, unit: pi, range: [0,2)
            : level: str, 'high'/'low'
            : time: float, unit: us
        :type raw_data_list_list: list
        :param check_sign: If True, the check function will be carried out, which will consume more time.
        :type check_sign: bool

        :returns:
        :rtype:
        """
        if len(ch_num_list) != len(raw_data_list_list):
            print('mismatch of ch_num and data_list')
            exit()
        else:
            play_address_word = b''
            for index_1 in range(len(ch_num_list)):
                raw_data_list_temp = raw_data_list_list[index_1]
                play_address_word_temp = self.single_data_download(ch_num_list[index_1], raw_data_list_temp,
                                                                   check_sign, print_sign=True)
                play_address_word += play_address_word_temp
            print('\ndata-download of channel ', ch_num_list, ' has been finished')
            self.play_sequence_set(ch_num_list, play_address_word, print_sign=True)
            # return play_address_word

    """
    var_type = [0, 1, 2, 3, 4], which is show the scan_para's variable type
               [0, 1, 2, 3, 4] represents ["no scan", "amp", "freq", "phase", "time"]
    scan_sign = [0, 1, 2, 3, 4] + 4*(para_num), which show the scan_para's type and group number
    para_num = 0, 1...; The group number for the scan_para 
    """
    def play(self, var_type, scan_para_list, check_sign=False):
        """To download the scan data and trigger the play
        What's more ,a PMT counter receive function will also be carried

        :param var_type: Int represents the variable type
        :type var_type: int
        :param scan_para_list: List of scan data
            :*** format: [[N_0, para0, para1], [N_1, para0, para1],..]
        :type scan_para_list: list
        :param check_sign: If True, the check function will be carried out, which will consume more time.
        :type check_sign: bool

        :returns:
        :rtype:
        """
        print('')
        scan_para_gen = self.scan_data_gen(var_type, scan_para_list)
        print(bytes_to_hexstr(scan_para_gen[0]))
        self.scan_data_download(scan_para_gen[0], print_sign=True)
        if check_sign:
            if not self.scan_data_check(scan_para_gen[0]):
                self.write(b'\x00\x00')
                print('Scan_data download check failed!')
                exit()
        print('Play ins is ', bytes_to_hexstr(b'\x00\x01' + scan_para_gen[0][0:4]))
        self.write(b'\x00\x01' + scan_para_gen[0][0:4])
        print("total_play ", scan_para_gen[1])
        return self.counter_receive(scan_para_gen[1])

    def counter_receive(self, cnt_number):#PMT
        """To receive PMT counter's result for each single play

        :param cnt_number: Total number of single play in current play
        :type cnt_number: int

        :returns: A list of PMT counter's result
        :rtype: list
        """
        readout_bytes = b''
        cnt_result_list = []
        counter_end_sign = True
        print('')
        # t1 = time.time()

        while counter_end_sign:
            temp = self.read()
            readout_bytes += temp
            while readout_bytes != b'':
                # print('Current time consumed is ', time.time()-t1)
                # print(bytes_to_hexstr(readout_bytes))
                # print('')
                if readout_bytes[0:2] == b'\xFF\xFA':  # start sign
                    readout_bytes = readout_bytes[2:]
                    cnt_addr_start = bytes_to_num(readout_bytes[0:2])
                elif readout_bytes[0:2] == b'\xFF\xF5':  # stop sign(The end sign of this infinite loop)
                    readout_bytes = readout_bytes[2:]
                    cnt_addr_stop = bytes_to_num(readout_bytes[0:2])
                    counter_end_sign = False  # To break from the whole while-loop
                    break
                else:
                    if readout_bytes[0:2] == b'\xFF\xF8':
                        cnt_result_list.append('overflow')
                    else:
                        cnt_result_list.append(bytes_to_num(readout_bytes[0:2]))
                readout_bytes = readout_bytes[2:]

        # print('the start and stop of cnt_addr are %d, %d' % (cnt_addr_start, cnt_addr_stop))
        # print('The length of result is %d' % len(cnt_result_list))
        if cnt_number == (cnt_addr_stop-cnt_addr_start) + 1:
            print('The cnt_number match the input scan number')
        else:
            print('The cnt_number miss match')
        # print('Counter number is ', cnt_number)
        print('The counter results is ', cnt_result_list)
        return cnt_result_list

    def ad5371_play(self, ch_num_list, raw_wave_list, play_sign=True, check_sign=False):#PMT
        """To receive PMT counter's result for each single play

        :param ch_num_list: List of ch_num(int), ch_num can be [0,1,..39]
        :type ch_num_list: list
        :param raw_wave_list: List of raw_wave_data, len(raw_wave_list[0]) = len(ch_num_list)
            :*** format : [[ch0_pt0, ch1_pt0, ...], [ch0_pt1, ch1_pt1, ...], ...]
        :type raw_wave_list: list
        :param play_sign: True/False -- Enable/Disable the play
        :type play_sign: bool
        :param check_sign: If True, the check function will be carried out, which will consume more time.
        :type check_sign: bool

        :returns:
        :rtype:
        """
        addr_start, addr_stop = self.dac_ad5371_data_download(ch_num_list, raw_wave_list, check_sign)
        if play_sign:
            ch_num = len(ch_num_list)
            self.ad5371_play_set(ch_num, [106, 59, 111])  # [106, 59, 111]
            self.write(b'\x00\x31' + addr_start + addr_stop)
            print(bytes_to_hexstr(b'\x00\x31' + addr_start + addr_stop))
            time.sleep((bytes_to_num(addr_stop)-bytes_to_num(addr_start))*1e-6)


class DDSTestClass(FPGA):

    def __init__(self, dev_index=0, test_mode=False):
        FPGA.__init__(self, dev_index=dev_index, test_mode=test_mode)
        self.pulse_width = 5  # default value
        # pulse_width1 = 0.1536
        # pulse_width2 = 3.520
        # pulse_width_ex = 3.1232  # 3.1168

    def initial_device(self):
        self.initial_dds()
        self.phase_clear_dds([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        # self.stamp_reset()

    def sequence_bool2int(self, var_type, raw_data_list_list):
        """To transfer the bool and para_num into scan_sign which can be applied in sequence generation

        :param var_type: Int represents the variable type
        :type var_type: int
        :param raw_data_list_list: List of raw_wave_data
        :type raw_data_list_list: list

        :returns:
        :rtype:
        """
        for ch_index in range(len(raw_data_list_list)):
            raw_data_list_pro = raw_data_list_list[ch_index]
            for seq_index in range(len(raw_data_list_pro)):
                if raw_data_list_pro[seq_index][0][0] and var_type > 0:
                    raw_data_list_pro[seq_index][0] = var_type + 4*raw_data_list_pro[seq_index][0][1]
                else:
                    raw_data_list_pro[seq_index][0] = 0

    def gen_fun_sync(self, raw_data_list_list, ch_num_len, cycles):
        """To generate a test_data in the empty list

        :param raw_data_list_list:
        :type raw_data_list_list: list
        :param ch_num_len: the len of ch_num_list
        :type ch_num_len: int
        :param cycles: the len of ch_num_list
        :type cycles: int

        :returns:
        :rtype:
        """
        for index_ch in range(ch_num_len):
            for index_cycle in range(cycles):
                raw_data_list_list[index_ch].extend([[[True, 0], [1, 0.1, 0], ['high', self.pulse_width]],
                                                     [[False, 0], [0, 0.1, 0], ['low', self.pulse_width]],
                                                     [[True, 1], [1, 0.1, 0], ['high', self.pulse_width]],
                                                     [[False, 1], [0, 0, 0], ['low', self.pulse_width]]])

    def scan_gen_basic(self, var_type):
        """To generate a test_scan_data

        :param var_type:
        :type var_type: int

        :returns:
        :rtype:
        """
        scan_para_list = []
        var_list = [[0, 0],
                    [1, 0.5], [100, .01], [0, 1], [5, 20],
                    [1, 0.5], [100, .01], [0, 1], [15, 20]]
        # var_list = [[0, 0],
        #             [1, 0.5], [100, 10], [0, 1], [5, 20],
        #             [1, 0.5], [100, 10], [0, 1], [15, 20]]
        n_list = [1, 2]
        for loop_index in range(2):
            for index in range(len(n_list)):
                scan_para_list.append([n_list[index], var_list[var_type][index], var_list[var_type+4][index]])
        print('scan_para_list is ', scan_para_list)
        return scan_para_list

    def test_fun_basic(self, play_ch_num_list, var_type, check_sign=False):
        """To carry out the test for DDS with scan

        :type play_ch_num_list: list
        :type var_type: int
        :type check_sign: bool

        :returns:
        :rtype:
        """
        # pulse_width = 4
        ch_num_len = len(play_ch_num_list)
        cycles = 2
        loop_cycles = 1

        # To generate raw_data_list_list
        raw_data_list_list = []
        for ii in range(ch_num_len):  # To generate a list of lists
            raw_data_list_list.append([])
        self.gen_fun_sync(raw_data_list_list, ch_num_len, cycles)
        self.sequence_bool2int(var_type, raw_data_list_list)
        print(raw_data_list_list[0])

        # To generate scan_para
        scan_para_list = self.scan_gen_basic(var_type)

        # To download the sequence data
        t1 = time.time()
        self.sequence_data_download(play_ch_num_list, raw_data_list_list, check_sign)
        print(play_ch_num_list)
        print(raw_data_list_list)
        print(len(play_ch_num_list))
        print(len(raw_data_list_list))


        print('Time consumed in download is', time.time()-t1)

        # To download the scan data and play
        # t1 = time.time()
        #scan_para_list = [[1, 1, 1], [2, 0.5, 1], [1, 1, 1], [2, 0.5, 1]]
        scan_para_list = [[2, 1, 0]]
        #for loop_index in range(1):
        self.play(0, scan_para_list, check_sign)

        print(var_type)
        print(scan_para_list)
        # print('Current time consumed is ', time.time()-t1)
        # print('Time consumed in total is', time.time()-t1)

    def spectrum_test(self):
        """A method to test the spectrum"""
        ch_num = 0
        freq_set = 600
        a, b = self.cw_play(ch_num, 1, freq_set, 0)  # amp = 1, phase = 0
        print(a, '    ', b)


class DacTestClass(FPGA):

    def __init__(self, dev_index=0, test_mode=False):
        FPGA.__init__(self, dev_index=dev_index, test_mode=test_mode)

    # Read!!
    def ch_test_new(self, ch_number, sin_pts=50):
        """To make AD5371 play a 50-point sine waveform

        :param ch_number: To set the number of channels enabled to play
        :type ch_number: int

        :returns:
        :rtype:
        """
        ch_list = []
        raw_wave_list = []
        for index in range(ch_number):
            ch_list.append(index)
        print(ch_list)
        for x in range(sin_pts):
            raw_wave_list.append([])
            data_pts = np.sin((float(x)/sin_pts * 0.8 +0)*2*np.pi) * 10
            for loop_index in range(ch_number):
                raw_wave_list[x].append(data_pts)
        print(raw_wave_list)
        self.ad5371_play(ch_list, raw_wave_list, play_sign=True, check_sign=True)


if __name__ == '__main__':
    """
    var_type = [0, 1, 2, 3, 4]
    scan_sign = [0, 1, 2, 3, 4] + 4*(para_num)
    para_num = 0, 1...
    """

    # # Part1
    # """ DDS and TTL test modules """
    # fpga = DDSTestClass(1)
    # fpga.dll.flushInputBuffer()  # To refresh the USB, just copy
    # fpga.initial_device()
    #
    # var_type = 0
    # play_ch_num_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    # # play_ch_num_list = [0, 1, 2, 3, 4, 5]
    # # play_ch_num_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    # fpga.test_fun_basic(play_ch_num_list, var_type, check_sign=True)

    # Part2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         4
    """ AD5371 test modules """
    ad5371 = DacTestClass(1)
    ad5371.dll.flushInputBuffer()
    ad5371.ad5371_ini()
    ad5371.ch_test_new(10)

    # # Part3
    # """ AD5371 test modules """

    # fpga = DDSTestClass(1)
    # fpga.cw_play(ch_num=5, amp=1, freq=0, phase=0)
    # ch_num=5
    # hp_channel, reg_wr = fpga.ch2identify(ch_num)
    # ch_num_byte = num_to_bytes(2**ch_num, 2)
    # print(fpga.l_read(ch_num_byte, reg_wr, right_rd=b'\x00\x00\x00\x00\x00\x00\x00\x00'))
