# coding=UTF-8

"""
--------------------------------------------------------
Copyright (c) ****-2018 ESR, Inc.  All rights reserved.
--------------------------------------------------------
Author: Mingdong Zhu
Date:  2018/10/29
Design Name: The user interface of the DDS software
Purpose: Design an interface software for customers to
         set the dds hardware using Python 3.6.3
--------------------------------------------------------
"""

import ctypes
import time
# import csv
# import threading
import numpy as np
import os


def num_to_bytes(num, bytenum, high_head=True):
    if high_head:
        return np.array([num], dtype='>u8').tobytes()[-bytenum:]  # big-endian
    else:
        return np.array([num], dtype='<u8').tobytes()[:bytenum]  # little-endian


def bytes_to_num(bytes_, signed_=True, big_=True):
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


def bytes_to_hexstr(s, space=True):
    # ss = s_str.encode('hex') # original solution in Python2
    ss = s.hex() # original solution in Python2
    if space:
        sl = [ss[i:i + 2] for i in range(0, len(ss), 2)]
        return ' '.join(sl)
    else:
        return ss


# def dec2bin_mal(mal, dig):
#     mal_1 = mal - int(mal)
#     bins = ''
#     while mal_1 >= 0:
#         mal_1 *= 2
#         if mal_1 >= 1 and len(bins) < dig:
#             bins = bins + '1'
#             mal_1 = mal_1 - int(mal_1)
#         elif mal_1 < 1 and len(bins) < dig:
#             bins = bins + '0'
#             mal_1 = mal_1 - int(mal_1)
#         else:
#             break
#     return bins


# def DEC_to_BIN(num_, byte_num, dem_dig):
#     num = float(num_)
#     integer = num // 1
#     decimal = num - integer
#     integer_BIN = str(bin(int(integer)))
#     decimal_BIN = dec2bin_mal(decimal, dem_dig)
#     out_put = integer_BIN + decimal_BIN
#     out_put1 = int(out_put, 2)
#     output = num_to_bytes(out_put1, byte_num)
#     return output


# class ReadCSV(object):
#     def __init__(self, PATH):
#         self.path = PATH
#         self.csvHand = open(self.path, "r")
#         self.readcsv = csv.reader(self.csvHand)
#         self.buffer = [row for row in self.readcsv]
#         self.csvHand.close()
#         # print self.buffer
#
#     def demarcate(self):
#         # print self.buffer
#         fine_data1 = [row for row in self.buffer]
#         return fine_data1


class GenWave(object):
    # SCAN_BYTES_LIST = [b'\x00\x00', b'\x00\x80', b'\x00\xA0', b'\x00\xC0', b'\x00\xE0']
    # scan_bytes_list = [b'\x00\x00', b'\x00\x80', b'\x00\xA0', b'\x00\xC0', b'\x00\xE0']
    """A class used for the Waveform Generation, including DDS and TTL waveform

    :param hp_channel: A flag used to distinguish the channel.
        True/False means 2G5-DDS/1G-DDS
    :type hp_channel: bool
    """
    # SCAN_BYTES_LIST = [b'\x00\x00', b'\x00\x80', b'\x00\xA0', b'\x00\xC0', b'\x00\xE0']

    def __init__(self):
        # scan list : ["no scan", "amp", "freq", "phase", "time"]
        self.SCAN_BYTES_LIST = [b'\x00\x00',
                                b'\x00\x40', b'\x00\x50', b'\x00\x60', b'\x00\x70',
                                # b'\x00\x00',
                                b'\x00\x80', b'\x00\x90', b'\x00\xA0', b'\x00\xB0']
        pass

    # Level1--DDS波形的基本转换操作
    # 包含 amplitude_hex, frequency_hex, phase_hex 三项
    def amplitude_hex(self, amp, hp_channel):
        # """
        # :param amp: float, range: [0,1]
        # :param hp_channel: bool, True/False means 2G5-DDS/1G-DDS
        # :return: bytes, length = 2 (12/14bit valid)
        # """
        """To get the bytes format of amplitude

        :param amp: Amplitude of DDS
        :type amp: float
        :param hp_channel: A flag used to distinguish the channel. True/False means 2G5-DDS/1G-DDS
        :type hp_channel: bool
        :returns: Bytes representing the amplitude
        :rtype: bytes, length = 2 (12/14bit valid)
        """
        if hp_channel:
            full_scale = 2**12-1
        else:
            full_scale = 2**14-1
        amp_dec = int(amp*full_scale)
        amp_byte = num_to_bytes(amp_dec, 2)  # transfer the decimal int into hex str
        return amp_byte

    def frequency_hex(self, freq, hp_channel):
        # """
        # :param freq: int or float, unit: MHz
        # :param hp_channel: bool, True/False means 2G5-DDS/1G-DDS
        # :return: [bytes, float, float]; [length, unit, unit] = [4 (32bit valid), MHz, Hz]
        # """
        """To get the bytes format of frequency

        :param freq: Frequency of DDS
        :type freq: float
        :param hp_channel: A flag used to distinguish the channel. True/False means 2G5-DDS/1G-DDS
        :type hp_channel: bool
        :returns: A list of the results after digitizing
        :rtype: [bytes, float, float]; [length, unit, unit] = [4 (32bit valid), MHz, Hz]
        """
        byte_full_scale = 2**32
        if hp_channel:
            sam_rate = 2500.0
        else:
            sam_rate = 1000.0
        freq_dec = int(round(freq*byte_full_scale/sam_rate))
        # int()   int will only be less than real
        freq_byte = num_to_bytes(freq_dec, 4)  # the freq unit is MHz
        real_freq = freq_dec*sam_rate/byte_full_scale
        diff_freq = (real_freq - freq)*10**6  # the diff_freq unit is Hz
        """
        return specification:
        1--bytes for the freq
        2--the real digital freq
        3--the difference of freq (real - set)
        """
        return [freq_byte, real_freq, diff_freq]

    def phase_hex(self, phase, hp_channel):
        # """
        # :param phase: float, unit: pi, range: [0,2)
        # :param hp_channel: bool, True/False means 2G5-DDS/1G-DDS
        # :return: bytes, length = 2 (16bit valid)
        # """
        """To get the bytes format of phase

        :param phase: Frequency of DDS
        :type phase: float
        :param hp_channel: A flag used to distinguish the channel. True/False means 2G5-DDS/1G-DDS
        :type hp_channel: bool
        :returns: Bytes representing the phase
        :rtype: bytes, length = 2 (16bit valid)
        """
        if hp_channel:
            phase_dec = int(((phase-1) % 2)*2**15)
            # add a pi offset to the phase
        else:
            phase_dec = int((phase % 2)*2**15)
        phase_byte = num_to_bytes(phase_dec, 2)
        return phase_byte

    def address_gen(self, data_number):
        """地址生成：用于写入以及播放
        :param data_number: int
        :return: [bytes, bytes]; length = 2 (for each one)
        """
        dds_start = num_to_bytes(0, 2)
        dds_stop = num_to_bytes(data_number - 1, 2)
        return [dds_start, dds_stop]

    # Level2--DDS与TTL波形生成, 以及地址生成
    # 包含 dds_data_form, ttl_data_form以及 pulse_data_encode, sequence_address_gen 四项
    def dds_data_form(self, hp_channel, amp, freq, phase):
        """DDS波形的生成操作——调用上面的3个，生成DDS波形

        :param hp_channel: bool, True/False means 2G5-DDS/1G-DDS
        :param amp: float, range: [0,1]
        :param freq: int or float, unit: MHz
        :param phase: float, unit: pi, range: [0,2)
        :return: [bytes, float, float]; [length, unit, unit] = [8, MHz, Hz]
        """
        amp_word = self.amplitude_hex(amp, hp_channel)
        freq_list = self.frequency_hex(freq, hp_channel)
        phase_word = self.phase_hex(phase, hp_channel)
        if hp_channel:
            dds_word = freq_list[0] + amp_word + phase_word
        else:
            dds_word = amp_word + phase_word + freq_list[0]
        """
        return specification:
        1--bytes for one single waveform of DDS play sequence
        2--the real digital freq
        3--the difference of freq (real - set)
        """
        return [dds_word, freq_list[1], freq_list[2]]

    def ttl_data_form(self, hp_channel, level, time):
        """TTL波形的基本转换操作，只转换单个TTL的高/低电平（并且返回实际的时间值、以及实际的与设置值的偏差）

        :param hp_channel: bool, True/False means 2G5-DDS/1G-DDS
        :param level: str, 'high'/'low'
        :param time: float, unit: us
        :return: [bytes, float, float]; [length, unit, unit] = [4, us, us]
        """
        ttl_sign_bit = 2**26
        if hp_channel:
            real_time = int(round(time*156.25))-1
        else:
            real_time = int(round(time*125.0))-1
        diff_time = real_time - time
        if level == 'high':
            single_ttl = num_to_bytes(real_time + ttl_sign_bit, 4)
        else:
            single_ttl = num_to_bytes(real_time, 4)
        """
        return specification:
        1--bytes for one single waveform of TTL play sequence
        2--the real digital time
        3--the difference of time (real - set)
        """
        return [single_ttl, real_time, diff_time]

    def pulse_data_encode(self, hp_channel, raw_data_list):
        """波形的转换操作;  调用DDS与TTL的转换（兼容一个DDS对应多个TTL波形的模式）

        :param hp_channel: bool, True/False means 2G5-DDS/1G-DDS
        :param raw_data_list: [scan_sign, [A, f(MHz), fai(pi)], [level, time],..]
            : scan_sign: int, [0,1, .. ,4]--["no scan", "amp", "freq", "phase", "time"]
            : amp: float, range: [0,1]
            : freq: int or float, unit: MHz
            : phase: float, unit: pi, range: [0,2)
            : level: str, 'high'/'low'
            : time: float, unit: us
        :return: [bytes, bytes, int, int]; [length_para1, length_para2] = [10*para_3, 4*para_4]
        """
        dds_data = b''
        ttl_data = b''
        # index = 0
        sequence_number = len(raw_data_list)
        # ttl_number = 0
        for index_1 in range(sequence_number):
            # temp_ttl_num = len(raw_data_list[index_1])-1  # the first one must be dds_list
            # ttl_number += temp_ttl_num
            scan_sign = raw_data_list[index_1][0]
            dds_temp_list = raw_data_list[index_1][1]
            # print(dds_temp_list)
            dds_data_list = self.dds_data_form(hp_channel, dds_temp_list[0], dds_temp_list[1], dds_temp_list[2])

            dds_data += self.SCAN_BYTES_LIST[scan_sign] + dds_data_list[0]

            ttl_temp_list = raw_data_list[index_1][2]
            ttl_data_list = self.ttl_data_form(hp_channel, ttl_temp_list[0], ttl_temp_list[1])
            ttl_data += ttl_data_list[0]
            # print bytes_to_hexstr(dds_data)
            # print bytes_to_hexstr(ttl_data)
            # print ' '
        """
        return specification:
            dds_number is len(dds_data)/10
            ttl_number is len(ttl_data)/4
        """
        return [dds_data, ttl_data, sequence_number]

    # Level3--序列生成
    # 仅 pulse_data_gen 一项
    def pulse_data_gen(self, hp_channel, raw_data_list):
        """序列生成：调用如上两个，生成DDS与ttl的波形，并且也生成地址

        :param hp_channel: bool, True/False means 2G5-DDS/1G-DDS
        :param raw_data_list: [[A,f(MHz),fai(pi)],[level,time],..]
            : amp: float, range: [0,1]
            : freq: int or float, unit: MHz
            : phase: float, unit: pi, range: [0,2)
            : level: str, 'high'/'low'
            : time: float, unit: us
        :return: [bytes, bytes, bytes, bytes]; length_3rd = 6
        """
        encode_data_list = self.pulse_data_encode(hp_channel, raw_data_list)
        sequence_number = len(raw_data_list)
        # ttl_number = encode_data_list[3]
        address_list = self.address_gen(sequence_number)
        dds_download_data = address_list[0] + address_list[1] + encode_data_list[0]
        ttl_download_data = address_list[0] + address_list[1] + encode_data_list[1]
        play_address = address_list[0] + address_list[1]
        """
        return specification:
            dds_number is len(dds_data[4:])/10
            ttl_number is len(ttl_data[4:])/4
        """
        return [dds_download_data, ttl_download_data, play_address]

    # ex--原始数据预处理
    # 目的：给实验波形加上头尾波形的数据处理————为了使得不做实验时，没有多余的输出。
    # Level1--基本指令(分为：头尾操作)
    def raw_data_list_head(self, raw_data_list):
        """ this function adds a 'head' to the wave_data_list"""
        raw_data_list.insert([0, [0, 0, 0], ['low', 5]])
        # return(raw_data_list)

    def raw_data_list_tail(self, raw_data_list):
        """ this function adds a 'tail' to the wave_data_list to end the play"""
        raw_data_list.extend([[0, [0, 0, 0], ['low', 5]]])  # no scan and no waveform for 5us
        # raw_data_list.append([[0,0,0],['low',5]])
        # a = self.raw_data_list_tail(a)  is equal to      self.raw_data_list_tail(a)

    def raw_data_list_head_a(self, raw_data_list):
        del raw_data_list[0]

    def raw_data_list_tail_a(self, raw_data_list):
        raw_data_list.pop()

    # Level2--高阶指令(仅分为：预处理、后处理)
    def raw_data_list_pro(self, raw_data_list):
        # self.raw_data_list_head(raw_data_list)
        self.raw_data_list_tail(raw_data_list)

    def raw_data_list_after_pro(self, raw_data_list):
        # self.raw_data_list_head_a(raw_data_list)
        self.raw_data_list_tail_a(raw_data_list)

    #################################################################
    # Scan data generation [basic functions]
    #
    # 5 functions
    #################################################################
    def scan_gen_0(self, scan_para_list):
        """To get the scan download data for "no scan"

        :param scan_para_list: list of [N_i, 0, 0...]
        :type scan_para_list: list
        :returns: Bytes representing the data byte stream
        :rtype: bytes, length = 6 * len(scan_para_list)
        """
        scan_data_bytes = b''
        cnt_number = 0
        para_len = len(scan_para_list[0]) - 1
        for index in range(len(scan_para_list)):
            cnt_number += scan_para_list[index][0]  # eg: Assumed N_i = 2, it will loop 2 times. The bytes is \x01
            scan_number_bytes = num_to_bytes((scan_para_list[index][0]-1) % (2**16), 2)
            scan_data_bytes += scan_number_bytes
            for para_index in range(para_len):
                scan_para_bytes = num_to_bytes(0, 4)
                scan_data_bytes += scan_para_bytes + scan_para_bytes
        return [scan_data_bytes, cnt_number]

    def scan_gen_1(self, scan_para_list):
        """To get the scan download data for "amp"

        :param scan_para_list: list of [N_i, amp1, amp2 ...]
        :type scan_para_list: list
        :returns: Bytes representing the data byte stream
        :rtype: bytes, length = 10 * len(scan_para_list)
        """
        scan_data_bytes = b''
        cnt_number = 0
        para_len = len(scan_para_list[0]) - 1
        for index in range(len(scan_para_list)):
            cnt_number += scan_para_list[index][0]  # eg: Assumed N_i = 2, it will loop 2 times. The bytes is \x01
            scan_number_bytes = num_to_bytes((scan_para_list[index][0]-1) % (2**16), 2)
            scan_data_bytes += scan_number_bytes
            for para_index in range(para_len):
                scan_para_bytes_2g5 = num_to_bytes(0, 2) + self.amplitude_hex(scan_para_list[index][para_index+1], True)
                scan_para_bytes_1g = num_to_bytes(0, 2) + self.amplitude_hex(scan_para_list[index][para_index+1], False)
                scan_data_bytes += scan_para_bytes_2g5 + scan_para_bytes_1g
        return [scan_data_bytes, cnt_number]

    def scan_gen_2(self, scan_para_list):
        """To get the scan download data for "freq"

        :param scan_para_list: list of [N_i, freq1, freq2...]
        :type scan_para_list: list
        :returns: Bytes representing the data byte stream
        :rtype: bytes, length = 10 * len(scan_para_list)
        """
        scan_data_bytes = b''
        cnt_number = 0
        para_len = len(scan_para_list[0]) - 1
        for index in range(len(scan_para_list)):
            cnt_number += scan_para_list[index][0]  # eg: Assumed N_i = 2, it will loop 2 times. The bytes is \x01
            scan_number_bytes = num_to_bytes((scan_para_list[index][0]-1) % (2**16), 2)
            scan_data_bytes += scan_number_bytes
            for para_index in range(para_len):
                scan_para_bytes_2g5 = self.frequency_hex(scan_para_list[index][para_index+1], True)[0]
                scan_para_bytes_1g = self.frequency_hex(scan_para_list[index][para_index+1], False)[0]
                scan_data_bytes += scan_para_bytes_2g5 + scan_para_bytes_1g
        return [scan_data_bytes, cnt_number]

    def scan_gen_3(self, scan_para_list):
        """To get the scan download data for "phase"

        :param scan_para_list: list of [N_i, phase1, phase2...]
        :type scan_para_list: list
        :returns: Bytes representing the data byte stream
        :rtype: bytes, length = 10 * len(scan_para_list)
        """
        scan_data_bytes = b''
        cnt_number = 0
        para_len = len(scan_para_list[0]) - 1
        for index in range(len(scan_para_list)):
            cnt_number += scan_para_list[index][0]  # eg: Assumed N_i = 2, it will loop 2 times. The bytes is \x01
            scan_number_bytes = num_to_bytes((scan_para_list[index][0]-1) % (2**16), 2)
            scan_data_bytes += scan_number_bytes
            for para_index in range(para_len):
                scan_para_bytes_2g5 = num_to_bytes(0, 2) + self.phase_hex(scan_para_list[index][para_index+1], True)
                scan_para_bytes_1g = num_to_bytes(0, 2) + self.phase_hex(scan_para_list[index][para_index+1], False)
                scan_data_bytes += scan_para_bytes_2g5 + scan_para_bytes_1g
        return [scan_data_bytes, cnt_number]

    def scan_gen_4(self, scan_para_list):
        """To get the scan download data for "time"

        :param scan_para_list: list of [N_i, time1, time2...]
        :type scan_para_list: list
        :returns: Bytes representing the data byte stream
        :rtype: bytes, length = 10 * len(scan_para_list)
        """
        scan_data_bytes = b''
        cnt_number = 0
        para_len = len(scan_para_list[0]) - 1
        for index in range(len(scan_para_list)):
            cnt_number += scan_para_list[index][0]  # eg: Assumed N_i = 2, it will loop 2 times. The bytes is \x01
            scan_number_bytes = num_to_bytes((scan_para_list[index][0]-1) % (2**16), 2)
            scan_data_bytes += scan_number_bytes
            for para_index in range(para_len):
                scan_para_bytes_2g5 = self.ttl_data_form(True, 'low', scan_para_list[index][para_index+1])[0]
                scan_para_bytes_1g = self.ttl_data_form(False, 'low', scan_para_list[index][para_index+1])[0]
                scan_data_bytes += scan_para_bytes_2g5 + scan_para_bytes_1g
        return [scan_data_bytes, cnt_number]

    #################################################################
    # Scan data generation [higher-order functions]
    #
    # Only 1 function
    #################################################################
    def scan_data_gen(self, var_type1, scan_para_list):
        """
        :param var_type1: [0,1,2,3,4] represents ["no scan", "amp", "freq", "phase", "time"]
        :type var_type1: int
        :param scan_para_list: list (of [data, N_i])
        :type scan_para_list: list
        :returns: list of [download data, cnt_number], length = 4 + 18*len(scan_para_list)
        :rtype: list
        """
        if var_type1 == 0:
            scan_para_gen = self.scan_gen_0(scan_para_list)
        elif var_type1 == 1:
            scan_para_gen = self.scan_gen_1(scan_para_list)
        elif var_type1 == 2:
            scan_para_gen = self.scan_gen_2(scan_para_list)
        elif var_type1 == 3:
            scan_para_gen = self.scan_gen_3(scan_para_list)
        elif var_type1 == 4:
            scan_para_gen = self.scan_gen_4(scan_para_list)
        else:
            print('incorrect input for var_type')
            exit()

        address_list = self.address_gen(len(scan_para_list))
        scan_download_data = address_list[0] + address_list[1] + scan_para_gen[0]
        return [scan_download_data, scan_para_gen[1]]

    #################################################################
    # AD5371 data generation [basic functions]
    #
    # 4 functions
    #################################################################
    def ad5371_addr_gen(self, ch_num_list, raw_wave_list):
        addr_start = num_to_bytes(0, 3)
        addr_stop_num = len(ch_num_list)*len(raw_wave_list) - 1
        addr_stop = num_to_bytes(addr_stop_num, 3)
        addr_word = addr_start + addr_stop
        return addr_word

    def ad5371_ch2bytes(self, ch_num_list):
        # g0_ch_list = [b'\x00\xC8', b'\x00\xC9', b'\x00\xCA', b'\x00\xCB',
        #               b'\x00\xCC', b'\x00\xCD', b'\x00\xCE', b'\x00\xCF']
        # g1_ch_list = [b'\x00\xD0', b'\x00\xD1', b'\x00\xD2', b'\x00\xD3',
        #               b'\x00\xD4', b'\x00\xD5', b'\x00\xD6', b'\x00\xD7']
        # g2_ch_list = [b'\x00\xD8', b'\x00\xD9', b'\x00\xDA', b'\x00\xDB',
        #               b'\x00\xDC', b'\x00\xDD', b'\x00\xDE', b'\x00\xDF']
        # g3_ch_list = [b'\x00\xE0', b'\x00\xE1', b'\x00\xE2', b'\x00\xE3',
        #               b'\x00\xE4', b'\x00\xE5', b'\x00\xE6', b'\x00\xE7']
        # g4_ch_list = [b'\x00\xE8', b'\x00\xE9', b'\x00\xEA', b'\x00\xEB',
        #               b'\x00\xEC', b'\x00\xED', b'\x00\xEE', b'\x00\xEF']
        reg_ch_list = [b'\x00\xC8', b'\x00\xC9', b'\x00\xCA', b'\x00\xCB',  # group0
                       b'\x00\xCC', b'\x00\xCD', b'\x00\xCE', b'\x00\xCF',
                       b'\x00\xD0', b'\x00\xD1', b'\x00\xD2', b'\x00\xD3',  # group1
                       b'\x00\xD4', b'\x00\xD5', b'\x00\xD6', b'\x00\xD7',
                       b'\x00\xD8', b'\x00\xD9', b'\x00\xDA', b'\x00\xDB',  # group2
                       b'\x00\xDC', b'\x00\xDD', b'\x00\xDE', b'\x00\xDF',
                       b'\x00\xE0', b'\x00\xE1', b'\x00\xE2', b'\x00\xE3',  # group3
                       b'\x00\xE4', b'\x00\xE5', b'\x00\xE6', b'\x00\xE7',
                       b'\x00\xE8', b'\x00\xE9', b'\x00\xEA', b'\x00\xEB',  # group4
                       b'\x00\xEC', b'\x00\xED', b'\x00\xEE', b'\x00\xEF']
        ch_bytes_list = []
        for index in range(len(ch_num_list)):
            ch_bytes_list.append(reg_ch_list[ch_num_list[index]])
        return ch_bytes_list

    def ad5371_pts2bytes(self, pts_data):
        """
        :param pts_data: -10 ~ +10, unit: V
        :type pts_data: float
        :param scan_para_list: list (of [data, N_i])
        :type scan_para_list: list
        :returns: list of [download data, cnt_number], length = 4 + 10*len(scan_para_list)
        :rtype: bytes
        """
        fsc = 2**13 - 1
        offset = 2**13
        data_in_num = (pts_data/10)*fsc + offset
        # y = np.sin((float(x)/sin_pts+0)*2*np.pi) * (2**13-1) + 2**13
        data_in_bytes = num_to_bytes(int(data_in_num)*4, 2)
        return data_in_bytes

    def ad5371_data_gen(self, ch_num_list, raw_wave_list):
        ch_bytes_list = self.ad5371_ch2bytes(ch_num_list)
        addr_word = self.ad5371_addr_gen(ch_num_list, raw_wave_list)
        dac_download_data = addr_word
        for index_pts in range(len(raw_wave_list)):
            for index_ch in range(len(ch_bytes_list)):
                temp_data = self.ad5371_pts2bytes(raw_wave_list[index_pts][index_ch])
                dac_download_data += ch_bytes_list[index_ch] + temp_data
        return dac_download_data

class HardWare(GenWave):
    """A class used for the basic Hardware controlling, including the instructions

    """

    #################################################################
    # __init__ and WR/RD for the USB_CY68013
    #################################################################
    def __init__(self, dev_index=0, test_mode=False):
        GenWave.__init__(self)

        """ init function just keep the same"""
        if test_mode:
            import random

            def read():
                return random.choice(
                    [b'\xff\x00\x00\x00', b'\xff\x00\x00\x01', b'\x00' * 4, b'\x11' * 4, b'\x22' * 4, b'\x11' * 6,
                     b'\xff' * 4])

            def write(msg):
                return len(msg)

            class dll:
                def flushInputBuffer(self, *args):
                    pass
            self.dev_index = 0
            self.read = read
            self.write = write
            self.dll = dll()
            self.stop()
            return
        import platform
        bits = platform.architecture()[0]
        dll_load = False
        # try:
        #     self.dll = ctypes.cdll.LoadLibrary('driver/xyj.dll')
        #     dll_load = True
        # except:
        #     print 'Load xyj_dll file fail!'
        bit32_driver_possible_list = ['driver/xyj_x86.dll', 'xyj_x86.dll', 'driver/xyj.dll', 'xyj.dll']
        bit64_driver_possible_list = ['driver/xyj_x64.dll', 'xyj_x64.dll', 'driver/xyj.dll', 'xyj.dll']
        if '32bit' in bits:
            driver_possible_list = bit32_driver_possible_list
        else:
            driver_possible_list = bit64_driver_possible_list
        d_index = 0
        for ii in range(len(driver_possible_list)):
            if os.path.exists(driver_possible_list[ii]):
                d_index = ii
                break
        try:
            if not dll_load:
                self.dll = ctypes.cdll.LoadLibrary(driver_possible_list[d_index])
        except:
            import traceback
            traceback.print_exc()
            # print('\nLoad FPGA USB fail!\n')
            print('load FPGA USB fail')
            return
        self.dll.read.restype = ctypes.c_bool
        self.dll.open.restype = ctypes.c_bool
        self.dll.read_until.restype = ctypes.c_bool
        self.dll.GetPara.restype = ctypes.c_ulong
        self.dev_index = ctypes.c_ubyte(0)
        self.open(dev_index)
        self.stop()

    def open(self, index=0):
        print('index=', index)
        self.dll.open.restype = ctypes.c_bool
        return self.dll.open(ctypes.c_byte(index))
        
    # def stop_old(self):
    #     """
    #     stop the device.
    #     :return:
    #     """
    #     # use for stop counter
    #     self.run_flag = False
    #     time.sleep(0.01)
    #     self.write(b'\x00' * 2)
    #     time.sleep(0.01)
    #     # clear buffer
    #     self.dll.flushInputBuffer()
    #     global CountDataBuf
    #     CountDataBuf = [0, []]

    def stop(self):
        """
        stop the device.
        :return:
        """
        # global stop_flag
        # stop_flag = True
        time.sleep(0.01)
        self.write(b'\x00' * 2)
        time.sleep(0.01)

        # clear buffer
        self.dll.flushInputBuffer()

    def read(self, num=4096):
        """ A new read function for Python3"""
        # print 'enter read'
        bufp = (ctypes.c_ubyte * 4100)()
        # bufp = ctypes.c_char_p(b'\x00' * num)
        cnum = ctypes.c_long(num)
        cnum_p = ctypes.pointer(cnum)

        if not self.dll.read(bufp, cnum_p):
            # fh.write('F%d\n' % cnum_p.contents.value)
            self.dll.ResetInputEnpt()
            return b''
        # fh.write('S%d\n' % cnum_p.contents.value)
        # fh.flush()
        # print num, 'rx num', cnum_p.contents.value
        # return str(bytearray(bufp))[:cnum_p.contents.value]
        return bytearray(bufp)[:cnum_p.contents.value]  # for Python3, we can return the bytes format rather than str

    def write(self, msg):
        """ A new write function for Python3"""
        # bufp = ctypes.c_char_p(bytes(msg, 'utf-8'))
        bufp = ctypes.c_char_p(msg)
        self.dll.write(bufp, ctypes.c_long(len(msg)))
        return len(msg)

    #################################################################
    # Some basic data pro
    #
    # Include 3 functions
    #################################################################
    # register transform
    def reg_wr2rd(self, reg_wr):    # eg:b'\x00'-->b'\x80'
        reg_rd = num_to_bytes(bytes_to_num(reg_wr) + 128, 1)
        return reg_rd

    def reg_rd2wr(self, reg_rd):
        reg_wr = num_to_bytes(bytes_to_num(reg_rd) % 128, 1)
        return reg_wr

    def ch2identify(self, ch_num):
        """ 判断是否是高采样率的DDS, HP：high performance"""
        if ch_num < 4:
            hp_channel = True
            reg_wr = b'\x0B'
        elif ch_num < 16:
            hp_channel = False
            reg_wr = b'\x0E'
        else:
            print('the ch_num is over range!')
            exit()
        return hp_channel, reg_wr

    #################################################################
    # To Enable/Disable some HW functions
    #
    # Include 4 functions
    #################################################################
    def sync_on(self):
        """ To enable the SYNC signal output"""
        self.write(b'\x00\x21')
        time.sleep(0.001)

    def sync_off(self):
        """ To disable the SYNC signal output"""
        self.write(b'\x00\x22')
        time.sleep(0.001)

    def auto_clear_on(self):
        """ To enable the auto clear (after each play)"""
        self.write(b'\x00\x23')
        time.sleep(0.001)

    def auto_clear_off(self):
        """ To disable the auto clear (after each play)"""
        self.write(b'\x00\x24')
        time.sleep(0.001)

    #################################################################
    # To configure and read register
    #
    # Include 4 functions
    #################################################################
    def s_configure(self, ch_num_byte, reg_wr, wr_data):
        """short/long configure (register) for DDS

        :param ch_num_byte: bytes, length = 2
        :param reg_wr: bytes, length = 1
        :param wr_data: bytes, length = 4
        :return:
        """
        if len(wr_data) == 4:
            self.write(b'\x00\x06' + ch_num_byte + b'\x00' + reg_wr + wr_data)
            time.sleep(0.001)

    def l_configure(self, ch_num_byte, reg_wr, wr_data):
        if len(wr_data) == 8:
            self.write(b'\x00\x07' + ch_num_byte + b'\x00' + reg_wr + wr_data)
            time.sleep(0.001)

    def s_read(self, ch_num_byte, reg_wr, right_rd=b'null'):
        """short/long read (register) for DDS

        :param ch_num_byte: bytes, length = 2
        :param reg_wr: bytes, length = 1; the reg_wr will be transfer into reg_rd
        :param right_rd: bytes, length = 4; the input is the right result for the readout
        :return: 1. result (type:string); 2. result, True/False
        """
        self.write(b'\x00\x08'+ch_num_byte + self.reg_wr2rd(reg_wr) + b'\x00')
        time.sleep(0.001)
        result = self.read()
        if right_rd == b'null':
            return bytes_to_hexstr(result)
        elif len(right_rd) == 4:
            if result == b'\x08'+reg_wr + right_rd:
                return bytes_to_hexstr(result), True
            else:
                return bytes_to_hexstr(result), False

    def l_read(self, ch_num_byte, reg_wr, right_rd=b'null'):
        self.write(b'\x00\x09'+ch_num_byte + self.reg_wr2rd(reg_wr) + b'\x00')
        time.sleep(0.001)
        result = self.read()
        if right_rd == b'null':
            return bytes_to_hexstr(result)
        elif len(right_rd) == 8:
            if result == b'\x09'+reg_wr + right_rd:
                return bytes_to_hexstr(result), True
            else:
                return bytes_to_hexstr(result), False

    #################################################################
    # To set the parameter
    # Part1: delay set
    # Part2: wr/rd stamp set for SPI/BPI, and Play set for AD5371
    #################################################################
    # Part1: delay set
    def ttl_coarse_delay_set(self, ch_num, coarse_delay):
        # delay_step: 8 ns(1G-DDS) / 6.4 ns(2G5-DDS)
        """
        :param ch_num: int; range(0, 16, 1)
        :param coarse_delay: int; range(0, 16, 1), default: 7
        :return:
        """
        ch_num_byte = num_to_bytes(2**ch_num, 2)
        coarse_delay_byte = num_to_bytes(coarse_delay, 2)
        # print bytes_to_hexstr(b'\x00\x0A' + ch_num_byte + coarse_delay_byte)
        self.write(b'\x00\x0A' + ch_num_byte + coarse_delay_byte)
        # time.sleep(0.001)

    def ttl_serdese_delay_set(self, ch_num, serdese_delay):
        # delay_step: 1.6 ns
        """
        :param ch_num: int; range(0, 16, 1)
        :param serdese_delay: int; for 1G-DDS --- range(0, 5, 1), default: 4; for 2G5-DDS --- range(0, 4, 1), default: 0;
        :return:
        """
        ch_num_byte = num_to_bytes(2**ch_num, 2)
        serdese_delay_byte = num_to_bytes(serdese_delay, 2)
        # print bytes_to_hexstr(b'\x00\x0B' + ch_num_byte + serdese_delay_byte)
        self.write(b'\x00\x0B' + ch_num_byte + serdese_delay_byte)
        # time.sleep(0.001)

    def ttl_odelaye_delay_set(self, ch_num, delay_tap):
        # delay_step: ~52 ps
        """
        :param ch_num: int; range(0, 16, 1)
        :param delay_tap: int; range(0, 32, 1), 1G-DDS_default: 0, 2G5-DDS_default: 0;
        :return:
        """
        ch_num_byte = num_to_bytes(2**ch_num, 2)
        delay_tap_byte = num_to_bytes(delay_tap, 2)
        # print bytes_to_hexstr(b'\x00\x0C' + ch_num_byte + delay_tap_byte)
        self.write(b'\x00\x0C' + ch_num_byte + delay_tap_byte)
        # time.sleep(0.001)

    # def dds_coarse_delay_set(self, ch_num, coarse_delay):
    #     ch_num_byte = num_to_bytes(2**ch_num,2)
    #     coarse_delay_byte = num_to_bytes(coarse_delay,2)
    #     # print bytes_to_hexstr(b'\x00\x0A' + ch_num_byte + coarse_delay_byte)
    #     self.write(b'\x00\x0D' + ch_num_byte + coarse_delay_byte)
    #     # time.sleep(0.001)

    def dds_serdese_delay_set(self, ch_num, serdese_delay):
        # delay_step: 1.6 ns
        """
        :param ch_num: int; range(4, 16, 1)
        :param serdese_delay: int; for 1G-DDS --- range(0, 5, 1), default: 0; for 2G5-DDS --- range(0, 4, 1), default: 0;
        :return:
        """
        # if ch_num > 3:
        ch_num_byte = num_to_bytes(2**ch_num, 2)
        serdese_delay_byte = num_to_bytes(serdese_delay, 2)
        # print('dds_serdese_delay_set ', bytes_to_hexstr(b'\x00\x0E' + ch_num_byte + serdese_delay_byte))
        self.write(b'\x00\x0E' + ch_num_byte + serdese_delay_byte)
        # time.sleep(0.001)

    # def dds_odelaye_delay_set(self, ch_num, delay_tap):
    #     ch_num_byte = num_to_bytes(2**ch_num,2)
    #     delay_tap_byte = num_to_bytes(delay_tap,2)
    #     # print bytes_to_hexstr(b'\x00\x0C' + ch_num_byte + delay_tap_byte)
    #     self.write(b'\x00\x0F' + ch_num_byte + delay_tap_byte)
    #     # time.sleep(0.001)

    def sync_delay_set(self, ch_num, delay_tap):
        # delay_step: ~52 ps
        """
        :param ch_num: int; range(0, 16, 1)
        :param delay_tap: int; range(0, 32, 1), 1G-DDS_default: 15, 2G5-DDS_default: 12;
        :return:
        """
        ch_num_byte = num_to_bytes(2**ch_num, 2)
        delay_tap_byte = num_to_bytes(delay_tap, 2)
        # print bytes_to_hexstr(b'\x00\x0D' + ch_num_byte + delay_tap_byte)
        self.write(b'\x00\x18' + ch_num_byte + delay_tap_byte)  # the former one is b'\x0D'
        # time.sleep(0.001)

    # Part2: wr/rd stamp set for SPI/BPI, and Play set for AD5371
    def wr_stamp_set(self, ch_num, stamp_list):
        """
        :param ch_num: int; range(0, 16, 1)
        :param stamp_list: list (of int), length = 3; default is shown below
                ch_num_list = [2,3,4]
                stamp_list_wr = [[0,1,3],[0,2,5],[0,2,5]]
        :return:
        """
        ch_num_byte = num_to_bytes(2**ch_num, 2)
        stamp = b''
        for index_1 in range(3):
            stamp += num_to_bytes(stamp_list[index_1] % 128, 1)
        print(bytes_to_hexstr(b'\x00\x10'+ch_num_byte+b'\x00'+stamp))
        self.write(b'\x00\x10'+ch_num_byte+b'\x00'+stamp)
        time.sleep(0.001)

    def rd_stamp_set(self, ch_num, stamp_list):
        """
        :param ch_num: int; range(0, 16, 1)
        :param stamp_list: list (of int), length = 3; default is shown below
                ch_num_list = [2,3,4]
                stamp_list_rd = [[2,7,9],[4,6,9],[3,5,12]]
        :return:
        """
        ch_num_byte = num_to_bytes(2**ch_num, 2)
        stamp = b''
        for index_1 in range(3):
            stamp += num_to_bytes(stamp_list[index_1] % 128, 1)
        print(bytes_to_hexstr(b'\x00\x11'+ch_num_byte+b'\x00'+stamp))
        self.write(b'\x00\x11'+ch_num_byte+b'\x00'+stamp)
        time.sleep(0.001)

    def ad5371_wr_stamp_set(self, stamp_list):
        """
        :param stamp_list: list (of int), length = 3; default: [0,1,3]
        :return:
        """
        stamp = b''
        for index_1 in range(3):
            stamp += (num_to_bytes(stamp_list[index_1] % 128, 1))
        print(bytes_to_hexstr(b'\x00\x35\x00'+stamp))
        self.write(b'\x00\x35\x00'+stamp)
        time.sleep(0.001)

    def ad5371_play_set(self, num_of_ch, time_list):
        """
        :param num_of_ch: int; range(1, 41, 1)
        :param time_list: list (of int), length = 3; default(also minmum): [106,59,111]
        :return:
        """
        play_para = num_to_bytes(num_of_ch % 64, 1)
        for index_1 in range(3):
            play_para += num_to_bytes(time_list[index_1] % 4096, 2)
        print(bytes_to_hexstr(b'\x00\x36\x00'+play_para))
        self.write(b'\x00\x36\x00'+play_para)
        time.sleep(0.001)


    #################################################################
    # To download or check DDS/TTL data
    #
    # Include 4 functions
    #################################################################
    def dds_data_download(self, ch_num_byte, dds_download_data, print_sign=False):
        """
        :param ch_num_byte: bytes, length = 2;
        :param dds_download_data: bytes, length = 4 + 10*N (1+8 is valid)
        :param print_sign: bool
        :return:
        """
        # print 'into dds_download'
        if print_sign:
            print('Into dds_download ', bytes_to_hexstr(b'\x00\x02' + ch_num_byte + dds_download_data[0:4]))
            print(bytes_to_hexstr(dds_download_data[4:]))
        # print(len(b'\x00\x02' + ch_num_byte + dds_download_data))
        data = b'\x00\x02' + ch_num_byte + dds_download_data
        self.write(data)
        time.sleep(0.001)

    def dds_data_check(self, ch_num, dds_download_data):
        # for downloading, the dds_data share the same interface, not for checking
        """
        :param ch_num: int; range(0, 16, 1)
        :param dds_download_data: bytes, length = 4 + 10*N (1+8 is valid)
        :return: True/False
        """
        ch_num_byte = num_to_bytes(2**ch_num, 2)
        if ch_num < 4:
            print(bytes_to_hexstr(b'\x00\x03' + ch_num_byte + dds_download_data[0:4]))
            self.write(b'\x00\x03' + ch_num_byte + dds_download_data[0:4])
        else:
            # print bytes_to_hexstr(b'\x00\x13' + ch_num_byte + dds_download_data[0:4])
            self.write(b'\x00\x13' + ch_num_byte + dds_download_data[0:4])
        time.sleep(0.001)
        check_data = b''
        zero_len_cnt = 0  # to count the times of readout's length is 0
        while len(check_data) < len(dds_download_data[4:]):
            check_data_temp = self.read()
            if zero_len_cnt == 3:
                print('check data is ', bytes_to_hexstr(check_data))
                print('right data is ', bytes_to_hexstr(dds_download_data[4:]))
                break
            if len(check_data_temp) == 0:
                zero_len_cnt += 1
                time.sleep(0.001)
                continue
            # print bytes_to_hexstr(check_data_temp)
            check_data += check_data_temp
            # print bytes_to_hexstr(check_data)
        if check_data == dds_download_data[4:]:
            return True
        else:
            print('error')
            if len(check_data) == len(dds_download_data[4:]):
                print('len is okay')
            # print bytes_to_hexstr(check_data)
            return False

    def ttl_data_download(self, ch_num_byte, ttl_download_data, print_sign=False):
        """
        :param ch_num_byte: bytes, length = 2;
        :param ttl_download_data: bytes, length = 4 + 4*N (27bits are valid)
        :param print_sign: bool
        :return:
        """
        if print_sign:
            print('ttl_data_download ', bytes_to_hexstr(b'\x00\x04' + ch_num_byte + ttl_download_data[0:4]))
            print(bytes_to_hexstr(ttl_download_data[4:]))
        data = b'\x00\x04' + ch_num_byte + ttl_download_data
        self.write(data)
        time.sleep(0.001)

    def ttl_data_check(self, ch_num, ttl_download_data):
        # for downloading, the ttl_data share the same interface, not for checking
        """
        :param ch_num: int; range(0, 16, 1)
        :param ttl_download_data: bytes, length = 4 + 4*N (27bits are valid)
        :return: True/False
        """
        ch_num_byte = num_to_bytes(2**ch_num, 2)
        if ch_num < 4:
            # print bytes_to_hexstr(b'\x00\x05' + ch_num_byte + ttl_download_data[0:4])
            self.write(b'\x00\x05' + ch_num_byte + ttl_download_data[0:4])
        else:
            # print bytes_to_hexstr(b'\x00\x15' + ch_num_byte + ttl_download_data[0:4])
            self.write(b'\x00\x15' + ch_num_byte + ttl_download_data[0:4])
        time.sleep(0.001)
        check_data = b''
        zero_len_cnt = 0
        while len(check_data) < len(ttl_download_data[4:]):
            check_data_temp = self.read()
            if zero_len_cnt == 3:
                print('check data is ', bytes_to_hexstr(check_data))
                print('right data is ', bytes_to_hexstr(ttl_download_data[4:]))
                break
            if len(check_data_temp) == 0:
                zero_len_cnt += 1
                time.sleep(0.001)
                continue
            check_data += check_data_temp
        if check_data == ttl_download_data[4:]:
            return True
        else:
            print('error')
            if len(check_data) == len(ttl_download_data[4:]):
                print('len is okay')
            # print bytes_to_hexstr(check_data)
            return False

    def scan_data_download(self, scan_download_data, print_sign=False):
        """
        :param scan_download_data: bytes, length = 4 + 18*N (144bits in total)
        :param print_sign: bool
        :return:
        """
        if print_sign:
            print('scan_data_download ', bytes_to_hexstr(b'\x00\x40' + scan_download_data[0:4]))
            print(bytes_to_hexstr(scan_download_data[4:]))
        data = b'\x00\x40' + scan_download_data
        self.write(data)
        time.sleep(0.001)
    #
    # def scan_data_download(self, var_type, scan_para_list):
    #     """
    #     :param var_type: int, value: [0,1,2,3,4] represents ["no scan","amp","freq","phase","time"]
    #     :param scan_para_list: list (of [data, N_i])
    #     :return:
    #     """
    #     scan_para_byte = b''
    #     if var_type == 0:
    #         scan_para_byte = self.scan_gen_0(scan_para_list)
    #     elif var_type == 1:
    #         scan_para_byte = self.scan_gen_1(scan_para_list)
    #     elif var_type == 2:
    #         scan_para_byte = self.scan_gen_2(scan_para_list)
    #     elif var_type == 3:
    #         scan_para_byte = self.scan_gen_3(scan_para_list)
    #     elif var_type == 4:
    #         scan_para_byte = self.scan_gen_4(scan_para_list)
    #     else:
    #         print('incorrect input for var_type')
    #         exit()
    #
    #     scan_addr_start = num_to_bytes(0, 2)
    #     scan_addr_stop = num_to_bytes(int(len(scan_para_byte)/10) - 1, 2)
    #     self.write(b'\x00\x01' + scan_addr_start + scan_addr_stop + scan_para_byte)

    def scan_data_check(self, scan_download_data):
        """
        :param scan_download_data: bytes, length = 4 + 18*N (144bits in total)
        :return: True/False
        """
        print(bytes_to_hexstr(b'\x00\x41' + scan_download_data[0:4]))
        self.write(b'\x00\x41' + scan_download_data[0:4])
        time.sleep(0.001)

        check_data = b''
        zero_len_cnt = 0  # to count the times of readout's length is 0
        while len(check_data) < len(scan_download_data[4:]):
            check_data_temp = self.read()
            if zero_len_cnt == 3:
                print('check data is ', bytes_to_hexstr(check_data))
                print('right data is ', bytes_to_hexstr(scan_download_data[4:]))
                break
            if len(check_data_temp) == 0:
                zero_len_cnt += 1
                time.sleep(0.001)
                continue
            # print bytes_to_hexstr(check_data_temp)
            check_data += check_data_temp
            # print bytes_to_hexstr(check_data)

        if check_data == scan_download_data[4:]:
            return True
        else:
            print('error')
            if len(check_data) == len(scan_download_data[4:]):
                print('len is okay')
            # print bytes_to_hexstr(check_data)
            return False

    def ad5371_data_download(self, dac_download_data, print_sign=False):
        """
        :param dac_download_data: bytes, length = 6 + 4*N (32bits in total)
        :param print_sign: bool
        :return:
        """
        if print_sign:
            print('ad5371_data_download ', bytes_to_hexstr(b'\x00\x32' + dac_download_data[0:6]))
            print(bytes_to_hexstr(dac_download_data[6:]))
        data = b'\x00\x32' + dac_download_data
        self.write(data)
        time.sleep(0.001)

    def ad5371_data_check(self, dac_download_data):
        """
        :param dac_download_data: bytes, length = 4*N (3 is valid)
        :return: True/False
        """
        print(bytes_to_hexstr(b'\x00\x33' + dac_download_data[0:6]))
        self.write(b'\x00\x33' + dac_download_data[0:6])
        time.sleep(0.001)

        check_data = b''
        zero_len_cnt = 0  # to count the times of readout's length is 0
        while len(check_data) < len(dac_download_data[6:]):
            check_data_temp = self.read()
            if zero_len_cnt == 3:
                print('check data is ', bytes_to_hexstr(check_data))
                print('right data is ', bytes_to_hexstr(dac_download_data[6:]))
                break
            if len(check_data_temp) == 0:
                zero_len_cnt += 1
                time.sleep(0.001)
                continue
            # print bytes_to_hexstr(check_data_temp)
            check_data += check_data_temp
            # print bytes_to_hexstr(check_data)

        if check_data == dac_download_data[6:]:
            return True
        else:
            print('error')
            if len(check_data) == len(dac_download_data[6:]):
                print('len is okay')
            # print bytes_to_hexstr(check_data)
            return False

    def dac_ad5371_data_download(self, ch_num_list, raw_wave_list, check_sign=False):
        """ AD5371 low sample rate DAC的数据下载"""
        if len(ch_num_list) != len(raw_wave_list[0]):
            print('mismatch of ch_num and data_list')
            exit()
        else:
            dac_download_data = self.ad5371_data_gen(ch_num_list, raw_wave_list)
            self.ad5371_data_download(dac_download_data, print_sign=True)
            if check_sign:
                if not self.ad5371_data_check(dac_download_data):
                    self.write(b'\x00\x00')
                    print('AD5371 data download check fail')
                    exit()
                else:
                    print('AD5371 data download has been finished with check')

            addr_start = dac_download_data[0:3]
            addr_stop = dac_download_data[3:6]
            return addr_start, addr_stop

    #################################################################
    # 多（单）通道的播放指令
    #
    # Only 2 functions
    #################################################################
    def play_sequence_set(self, ch_num_list, play_address_word, print_sign=False):
        """
        :param ch_num_list: list (of int), length: range(1, 17, 1)
        :param play_address_word: bytes, length = 6*len(ch_num_list)
        :param print_sign: bool
        :return:
        """
        ch_num_sum = 0
        for index_1 in range(len(ch_num_list)):
            ch_num_sum += 2**ch_num_list[index_1]
        ch_num_sum_byte = num_to_bytes(ch_num_sum, 2)
        self.write(b'\x00\x1A' + ch_num_sum_byte + play_address_word)
        if print_sign:
            print('\nThe play_sequence_set bytes are ',
                  bytes_to_hexstr(b'\x00\x1A' + ch_num_sum_byte + play_address_word))

    # def play(self, scan_para_list):
    #     """
    #     :param scan_para_list: list (of [scan_para, N_i])
    #     :return:
    #     """
    #     scan_addr_start = num_to_bytes(0, 2)
    #     scan_addr_stop = num_to_bytes(int(len(scan_para_list)) - 1, 2)
    #     self.write(b'\x00\x01' + scan_addr_start + scan_addr_stop)

    #################################################################
    # To set the Para
    #
    # Include 2 functions
    #################################################################
    def stamp_reset(self):
        """ 重置读写的速率（平时不使用，只有出错时，快速返回默认值用的）"""
        ch_num_list = [2, 3, 4]
        stamp_list_wr = [[0, 1, 3], [0, 2, 5], [0, 2, 5]]
        stamp_list_rd = [[2, 7, 9], [4, 6, 9], [3, 5, 12]]
        for index_1 in range(3):
            self.wr_stamp_set(ch_num_list[index_1], stamp_list_wr[index_1])
            self.rd_stamp_set(ch_num_list[index_1], stamp_list_rd[index_1])

    # def delay_para_set(self):     #para set backup
    #     self.sync_delay_set(4,15)
    #     self.sync_delay_set(2,12)    # from 9 to 14 (8, 15 is not okay)
    #     for ii in range(4):
    #         self.ttl_coarse_delay_set(ii,7)
    #         self.ttl_serdese_delay_set(ii,0)
    #         self.ttl_odelaye_delay_set(ii,0)
    #     for ii in range(12):
    #         self.ttl_coarse_delay_set(ii+4,7)
    #         self.ttl_serdese_delay_set(ii+4,4)
    #         self.ttl_odelaye_delay_set(ii+4,0)
    #
    #         self.dds_serdese_delay_set(ii+4,0)

    def delay_para_set(self):
        """ 设置延时（确定后不用调整）"""
        self.sync_delay_set(4, 15)
        self.sync_delay_set(2, 12)    # from 9 to 14 (8, 15 is not okay)
        for index_1 in range(4):
            self.ttl_coarse_delay_set(index_1, 7)
            self.ttl_serdese_delay_set(index_1, 0)
            self.ttl_odelaye_delay_set(index_1, 0)
        for index_1 in range(12):
            self.ttl_coarse_delay_set(index_1+4, 7)
            self.ttl_serdese_delay_set(index_1+4, 4)
            self.ttl_odelaye_delay_set(index_1+4, 0)
            self.dds_serdese_delay_set(index_1+4, 0)

    #################################################################
    # 2.5GSPS / 1GSPS 的DDS的初始化配置、相位清零、手动同步
    #
    # Include 6 functions
    #################################################################
    def initial_AD9915(self, ch_num):
        """ 2.5GSPS dds的初始化配置"""
        # print ('channel-%d initial' %ch_num)
        ch_num_byte = num_to_bytes(2**ch_num, 2)
        self.s_configure(ch_num_byte, b'\x00', b'\x00\x01\x01\x0A')  # con-phase  and amp en
        self.s_configure(ch_num_byte, b'\x01', b'\x00\x80\x80\x00')
        self.s_configure(ch_num_byte, b'\x03', b'\x01\x05\x21\x20')  # DAC_CAL en
        self.s_configure(ch_num_byte, b'\x03', b'\x00\x05\x21\x20')  # DAC_CAL disable
        # print 'initial finished!'
        # print(self.s_read(ch_num_byte, b'\x01', b'\x00\x80\x80\x00'))
        # print(self.l_read(ch_num_byte, b'\x0B', b'\x00\x00\x00\x00\x00\x00\x00\x00'))

    def phase_clear_2g5(self, ch_num):
        """ 2.5GSPS dds的相位清零"""
        ch_num_byte = num_to_bytes(2**ch_num, 2)
        self.s_configure(ch_num_byte, b'\x00', b'\x00\x01\x09\x0A')  # asynchronous phase clear set
        self.s_configure(ch_num_byte, b'\x00', b'\x00\x01\x01\x0A')  # the bit clear
        # print 'phase accumulator has been cleared!!'

    def mannual_sync_2g5(self):
        """ 2.5GSPS dds的手动同步"""
        ch_num_byte_list = [b'\x00\x02', b'\x00\x01', b'\x00\x04', b'\x00\x08']
        # self.sync_on()
        # time.sleep(0.003)
        # self.s_configure(ch_num_byte_list[0], b'\x01', b'\x00\x80\x83\x00')#enable SYNC_OUT
        for index_1 in range(4):
            self.s_configure(ch_num_byte_list[index_1], b'\x1B', b'\x00\x00\x08\x40')
            self.s_configure(ch_num_byte_list[index_1], b'\x03', b'\x01\x05\x21\x20')  # DAC_CAL en
            self.s_configure(ch_num_byte_list[index_1], b'\x03', b'\x00\x05\x21\x20')  # DAC_CAL disable
        # self.sync_off()
        # self.s_configure(ch_num_byte_list[3], b'\x01', b'\x00\x80\x80\x00')#disable SYNC_OUT
        # print 'SYNC process has been finished!!'

    def initial_ad9910(self, ch_num):
        """ 1GSPS dds的初始化配置"""
        # sine waveform
        # print ('channel-%d initial' %ch_num)
        ch_num_byte = num_to_bytes(2**ch_num, 2)
        self.s_configure(ch_num_byte, b'\x00', b'\x00\x01\x00\x02')
        self.s_configure(ch_num_byte, b'\x01', b'\x01\x40\x00\xA0')
        self.s_configure(ch_num_byte, b'\x02', b'\x1F\x3F\xC0\x00')
        self.s_configure(ch_num_byte, b'\x03', b'\x00\x00\x00\xFF')  # from 7F to FF
        # print 'initial finished!'
        # print(self.s_read(ch_num_byte, b'\x01', b'\x01\x40\x00\xA0'))
        # print(self.l_read(ch_num_byte, b'\x0E', b'\x08\xB5\x00\x00\x00\x00\x00\x00'))

    def phase_clear_1g(self, ch_num):
        """ 1GSPS dds的相位清零"""
        ch_num_byte = num_to_bytes(2**ch_num, 2)
        self.s_configure(ch_num_byte, b'\x00', b'\x00\x01\x08\x02')
        self.s_configure(ch_num_byte, b'\x00', b'\x00\x01\x00\x02')
        # print 'phase accumulator has been cleared!!'

    def mannual_sync_1g(self):
        """ 1GSPS dds的手动同步"""
        # self.sync_on()
        # time.sleep(0.001)
        # self.s_configure(b'\x00\x10', b'\x0A', b'\x0C\x00\x00\x00')
        for index_1 in range(12):
            # print index_1+5
            ch_num_byte = num_to_bytes(2**(index_1+4), 2)
            self.s_configure(ch_num_byte, b'\x0A', b'\x08\x00\x00\xf8')
            #  [7:0] set 0x00 to 0x58  ([2:0] is not used)-----6~17

            #  [7:0] set 0x30 to 0x88  ([2:0] is not used)-----6~17
            self.s_configure(ch_num_byte, b'\x0A', b'\x00\x00\x00\x00')
        # self.s_configure(b'\x00\x10', b'\x0A', b'\x00\x00\x00\x00')
        # self.sync_off()
        # print 'SYNC process has been finished!!'

    #################################################################
    # 单通道的数据下载
    #
    # Only 1 function
    #################################################################
    def single_data_download(self, ch_num, raw_data_list, check_sign, print_sign=False):
        """
        :param ch_num: number of channel
        :type ch_num: int
        :param raw_data_list: [[A,f(MHz),fai(pi)],[level,time],..]
                : amp: float, range: [0,1]
                : freq: int or float, unit: MHz
                : phase: float, unit: pi, range: [0,2)
                : level: str, 'high'/'low'
                : time: float, unit: us
        :param check_sign: True/False means Enable/Disable check_process
        :type check_sign: bool
        :param print_sign: True/False means Enable/Disable Print the download bytes
        :type print_sign: bool
        :returns: List of Bytes
        :rtype: [bytes, bytes, bytes, bytes]; length_3rd = 6
        """
        ch_num_byte = num_to_bytes(2**ch_num, 2)
        hp_channel, reg_wr = self.ch2identify(ch_num)  # in this part reg_wr is useless
        self.raw_data_list_pro(raw_data_list)
        # self.raw_data_list_pro(raw_data_list)
        if print_sign:
            print('\nChannel %d data download start' % ch_num)
            print(raw_data_list)
        pulse_list = self.pulse_data_gen(hp_channel, raw_data_list)
        # self.raw_data_list_after_pro(raw_data_list)
        self.raw_data_list_after_pro(raw_data_list)
        self.dds_data_download(ch_num_byte, pulse_list[0], print_sign)
        if check_sign:
            if not self.dds_data_check(ch_num, pulse_list[0]):
                self.write(b'\x00\x00')
                print('channel-%d dds_data download check fail' % ch_num)
                # if not self.dds_data_check(ch_num, pulse_list[0]):
                #     print 'channel-%d dds_data download fails' %ch_num
                exit()
            else:
                print('channel-%d dds_data download has been finished with check' % ch_num)
        self.ttl_data_download(ch_num_byte, pulse_list[1], print_sign)
        if check_sign:
            if not self.ttl_data_check(ch_num, pulse_list[1]):
                self.write(b'\x00\x00')
                print('channel-%d ttl_data download check fail' % ch_num)
                # if not self.ttl_data_check(ch_num, pulse_list[1]):
                #     print 'channel-%d ttl_data download fails' %ch_num
                exit()
            else:
                print('channel-%d ttl_data download has been finished with check' % ch_num)
            # time.sleep(0.001)
        return pulse_list[2]  # retrun the address for play


    #################################################################
    # test function only for the hardware debug, useless for application
    #
    # Included 6 functions
    #################################################################
    '''
    ####### mode set for IO_A0 and IO_A1
    def IO_mode_set(self, mode_num):    # this one is a function for my test
        mode_num_byte = num_to_bytes(mode_num, 2)
        print(bytes_to_hexstr(b'\x00\x20' + mode_num_byte))
        self.write(b'\x00\x20' + mode_num_byte)
        time.sleep(0.001)

    #######################################protocol test function
    #######这一部分主要是为了测试DDS的读/写的速率
    def SPI_TEST(self, ch_num, wr_en):
        if ch_num>=3:
            ini_stamp = [25,50,100,[1,2,4]]
        else:
            if wr_en == '1':
                ini_stamp = [1,10,20,[0,1,2]]
            else:
                ini_stamp = [10,20,30,[1,2,3]]

        stamp_list=[25,50,100]
        while True:
            for ii in range(3):
                stamp_list[ii] = ini_stamp[ii]-1
            if wr_en == '1':
                self.wr_stamp_set(ch_num, stamp_list)
            else:
                self.rd_stamp_set(ch_num, stamp_list)
            check_reuslt = self.data_check(ch_num, 4)
            print (check_reuslt)
            if not check_reuslt or (ini_stamp[0] == 1 and wr_en == '1'):
                print("when stamp0, stamp1, stamp2 is %d, %d, %d, the error begins" 
                        %(ini_stamp[0],ini_stamp[1],ini_stamp[2]))
                break
            else:
                for ii in range(3):
                    ini_stamp[ii] -= ini_stamp[3][ii]


    def data_check(self, ch_num, check_times):# ch,
        ch_num_byte = num_to_bytes(2**ch_num, 2)
        error_times = 0
        check_data_list = [b'\x00\x00\x00\x00', b'\x19\x99\x99\x99', b'\x0F\xFF\xFF\xFF',
                        b'\x19\x99\x99\x99', b'\x0F\xFF\xFF\xFF']
        if ch_num < 4:
            reg_wr = b'\x0B'
        else:
            reg_wr = b'\x0E'
        for ii in range(check_times):
            self.l_configure(ch_num_byte, reg_wr, b'\x00\x00\x00\x00'+check_data_list[ii+1])
            rd_result, compare_result = self.l_read(ch_num_byte, reg_wr, b'\x00\x00\x00\x00'+check_data_list[ii+1])

            if compare_result == True:
                continue
            else:
                error_times += 1
                print ("the error time is %d" %ii)
                print (rd_result+'    '+bytes_to_hexstr(check_data_list[ii+1]))
            break
        if error_times == 0:
            return(True)
        else:
            print ('the error_times in %d is %d' %(check_times,error_times))
            return(False)


    def AD5371_SPI_TEST(self):
        dec_step_stamp = [1,2,4]
        ini_stamp=[6,12,24]
        # ini_stamp=[25,50,100]
        stamp_list=[25,50,100]
        while True:
            for ii in range(3):
                stamp_list[ii] = ini_stamp[ii]-1
            self.AD5371_wr_stamp_set(stamp_list)
            # check_reuslt = self.data_check(ch_num, 4)
            # print check_reuslt
            # if not check_reuslt or (ini_stamp[0] == 1 and wr_en == '1'):
            print("when stamp0, stamp1, stamp2 is %d, %d, %d" %(ini_stamp[0],ini_stamp[1],ini_stamp[2]))

            fpga.write(b'\x00\x31'+b'\x00'+b'\xC9'+b'\xFF\xFC')  # X_0 = +10
            time.sleep(1)
            fpga.write(b'\x00\x31'+b'\x00'+b'\xC9'+b'\x80\x00')  # X_0 = 0
            time.sleep(1)
            fpga.write(b'\x00\x31'+b'\x00'+b'\xC9'+b'\x00\x00')  # X_0 = -10

            time.sleep(10)
            for ii in range(3):
                ini_stamp[ii] -= dec_step_stamp[ii]
            if ini_stamp[0] == 0:
                break
    
    ####### 单通道的“测试”数据下载
    def single_test_download(self, ch_num):
        # ch_num_byte = num_to_bytes(2**ch_num, 2)
        raw_data_list = [   [[1,200,0],['high',5]],   [[0,200,0],['low',5]],    [[1,200,0],['high',5],['low',5]]    ]
        return(self.single_data_download(ch_num, raw_data_list))
    def test_download(self, ch_num_list):
        play_address_word = b''
        for ii in range(len(ch_num_list)):
            play_address_word_temp = self.single_test_download(ch_num_list[ii])
            play_address_word += play_address_word_temp
        print ('test data-download of channel ',ch_num_list,' has been finished')
        return (play_address_word)
    
    '''

    """To get the bytes format of phase

    :param phase: Frequency of DDS
    :type phase: float
    :param hp_channel: A flag used to distinguish the channel. True/False means 2G5-DDS/1G-DDS
    :type hp_channel: bool
    :returns: Bytes representing the phase
    :rtype: bytes, length = 2 (16bit valid)
    """

    """ To enable the SYNC signal output"""


# class FPGA(HardWare):  # GenWave,
#     """ A class used for integration
#
#     """
#
#     def __init__(self, dev_index=0, test_mode=False):
#         """ To launch the Instantiation of classes"""
#         # GenWave.__init__(self)
#         HardWare.__init__(self, dev_index=dev_index, test_mode=test_mode)
#
#     def cw_play(self, ch_num, amp, freq, phase):
#         """ 单通道DDS的播放特定波形（连续播放————测试频谱时使用）"""
#         hp_channel, reg_wr = self.ch2identify(ch_num)
#         ch_num_byte = num_to_bytes(2**ch_num, 2)
#
#         dds_data_list = self.dds_data_form(hp_channel, amp, freq, phase)
#         print(bytes_to_hexstr(dds_data_list[0]))
#         self.l_configure(ch_num_byte, reg_wr, dds_data_list[0])
#         return dds_data_list[1], dds_data_list[2]
#
#     def ad5371_ini(self):
#         fpga.write(b'\x00\x31'+b'\x00'+b'\x02'+b'\x20\x00')  # the b'\x02' can be b'\x03',b'\x04'
#         fpga.write(b'\x00\x31'+b'\x00'+b'\x03'+b'\x20\x00')  # the OFS_g1 is set to be +10V.
#         fpga.write(b'\x00\x31'+b'\x00'+b'\x04'+b'\x20\x00')  # the OFS_g2~4 is set to be +10V.
#
#         fpga.write(b'\x00\x31'+b'\x00'+b'\x80'+b'\x80\x00')  # C
#         fpga.write(b'\x00\x31'+b'\x00'+b'\x40'+b'\xFF\xFC')  # M
#         fpga.write(b'\x00\x31'+b'\x00'+b'\xC0'+b'\x80\x00')  # X = +10
#
#         """
#         ini_stamp=[1,2,4]
#         stamp_list=[25,50,100]
#         for index_1 in range(3):
#             stamp_list[index_1] = ini_stamp[index_1]-1
#         """
#         stamp_list = [0, 1, 3]
#         self.AD5371_wr_stamp_set(stamp_list)
#         print('AD5371 initial has been finished')
#
#     #################################################################
#     # integration-experiment function
#     # 以下都是支持多个通道的操作
#     #################################################################
#     def initial_dds(self, ch_num_list):
#         """ 多通道DDS的初始化配置以及同步"""
#         self.delay_para_set()
#         self.sync_on()
#         for index_1 in range(len(ch_num_list)):
#             if ch_num_list[index_1] < 4:
#                 self.initial_AD9915(ch_num_list[index_1])
#             else:
#                 self.initial_ad9910(ch_num_list[index_1])
#         self.mannual_sync_2g5()
#         self.mannual_sync_1g()
#         self.sync_off()
#         # self.stamp_reset()    #when there are some bugs, this one will be used
#         print('channel ', ch_num_list, ' initial has been finished')
#
#     def phase_clear_dds(self, ch_num_list):
#         """ 多通道DDS的相位清空"""
#         for index_1 in range(len(ch_num_list)):
#             if ch_num_list[index_1] < 4:
#                 self.phase_clear_2g5(ch_num_list[index_1])
#             else:
#                 self.phase_clear_1g(ch_num_list[index_1])
#         # print 'phase of channel ',ch_num_list,' has been cleared'
#
#     def sequence_data_download(self, ch_num_list, raw_data_list_list, check_sign=False):
#         """ 多通道的数据下载"""
#         if len(ch_num_list) != len(raw_data_list_list):
#             print('mismatch of ch_num and data_list')
#             exit()
#         else:
#             play_address_word = b''
#             for index_1 in range(len(ch_num_list)):
#                 raw_data_list_temp = raw_data_list_list[index_1]
#                 play_address_word_temp = self.single_data_download(ch_num_list[index_1], raw_data_list_temp, check_sign)
#                 play_address_word += play_address_word_temp
#             print('data-download of channel ', ch_num_list, ' has been finished')
#             self.play_sequence_set(ch_num_list, play_address_word)
#             # return play_address_word
#
#     def play(self, var_type, scan_para_list, check_sign=False):
#         scan_para_gen = self.scan_data_gen(var_type, scan_para_list)
#         self.scan_data_download(scan_para_gen[0])
#         if check_sign:
#             if not self.scan_data_check(scan_para_gen[0]):
#                 self.write(b'\x00\x00')
#                 print('Scan_data download check failed!')
#                 exit()
#         self.write(b'\x00\x01' + scan_para_gen[0][0:4])
#         self.counter_receive(scan_para_gen[1])
#
#     def counter_receive(self, cnt_number):
#         readout_bytes = b''
#         cnt_result_list = []
#         while True:
#             temp = self.read()
#             readout_bytes += temp
#             if readout_bytes[0:2] == b'\xFF\xFA':  # start sign
#                 readout_bytes = readout_bytes[2:]
#                 cnt_addr_start = bytes_to_num(readout_bytes[0:2])
#             elif readout_bytes[0:2] == b'\xFF\xF5':  # start sign
#                 readout_bytes = readout_bytes[2:]
#                 cnt_addr_stop = bytes_to_num(readout_bytes[0:2])
#                 break
#             else:
#                 if readout_bytes[0:2] == b'\xFF\xF8':
#                     cnt_result_list.append('overflow')
#                 else:
#                     cnt_result_list.append(bytes_to_num(readout_bytes[0:2]))
#             readout_bytes = readout_bytes[2:]
#
#         print('the start and stop of cnt_addr are %d, %d' % (cnt_addr_start, cnt_addr_stop))
#         print('The length of result is %d' % len(cnt_result_list))
#         if cnt_number == (cnt_addr_stop-cnt_addr_start) + 1:
#             print('The cnt_number match the input scan number')
#         else:
#             print('The cnt_number miss match')


if __name__ == '__main__':
    fpga = HardWare(1)

    # fpga.write(b'\x00\x00')


    # # fpga=FPGA(0)
    # # global fpga
    # fpga.dll.flushInputBuffer()

    # # fpga.datasave()
    #
    # t1=time.time()
    # print 'time consumpted', time.time()-t1

    # fpga.IO_mode_set(5)
    # fpga.s_configure(b'\x00\x04',b'\x01', b'\x00\x80\x88\x00')#SYNC_CLK output enable
    # fpga.s_configure(b'\x00\x02',b'\x01', b'\x00\x80\x83\x00')#SYNC_OUT enable
    # fpga.sync_off()

    # [[A,f(Hz),fai(pi)], [on,rise moment(us)], [off,fall moment(us)]]
    # [[A,f(Hz),fai(pi)],[time, t]]

    # ###main function of experiment(end)

    # fpga.initial_dds([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    # z1 = [b'\x00\x00\x00\x00',b'\x00\x00\x00\x01']
    #
    # for ii in range(4):
    #     index = ii%2
    #     print index
    #     fpga.s_configure(b'\x00\x06',b'\x0E',z1[index])
    #     a = fpga.s_read(b'\x00\x02',b'\x0E',z1[index])
    #     b = fpga.s_read(b'\x00\x08',b'\x0E',z1[index])
    #     print a,b

    # z2 = [b'\x00\x00\x00\x00\x00\x00\x00\x00',b'\x00\x00\x00\x00\x00\x00\x00\x01']
    #
    # for ii in range(4):
    #     index = ii%2
    #     print ii
    #     fpga.l_configure(b'\xFF\xF0',b'\x0E',z2[index])
    #     a1 = fpga.l_read(b'\x00\x10',b'\x0E',z2[index])
    #     b1 = fpga.l_read(b'\x00\x20',b'\x0E',z2[index])
    #     a2 = fpga.l_read(b'\x00\x40',b'\x0E',z2[index])
    #     b2 = fpga.l_read(b'\x00\x80',b'\x0E',z2[index])
    #     c1 = fpga.l_read(b'\x01\x00',b'\x0E',z2[index])
    #     d1 = fpga.l_read(b'\x02\x00',b'\x0E',z2[index])
    #     c2 = fpga.l_read(b'\x04\x00',b'\x0E',z2[index])
    #     d2 = fpga.l_read(b'\x08\x00',b'\x0E',z2[index])
    #     x1 = fpga.l_read(b'\x10\x00',b'\x0E',z2[index])
    #     y1 = fpga.l_read(b'\x20\x00',b'\x0E',z2[index])
    #     x2 = fpga.l_read(b'\x40\x00',b'\x0E',z2[index])
    #     y2 = fpga.l_read(b'\x80\x00',b'\x0E',z2[index])
    #     print a1,b1,a2,b2   #a,b,a,b
    #     print c1,d1,c2,d2
    #     print x1,y1,x2,y2






    # fpga.auto_clear_on()


    # pulse_width1 = 0.1536
    # pulse_width2 = 3.520
    # pulse_width_ex = 3.1232#3.1168



    # # #sync test
    #
    # pulse_width = 4
    # raw_data_list_list = []
    # for ii in range(16):
    #     raw_data_list_list.append([])
    #
    # cycles = 10
    #
    # for ii in range(16):
    #     for jj in range(cycles):
    #         raw_data_list_list[ii].extend([[[1, 200, 0], ['high', pulse_width]], [[0, 200, 0], ['low', pulse_width]]])
    # print(raw_data_list_list[2])
    #
    # t1 = time.time()
    # #
    # for ii in range(1):   # 100    ~ 95 s        32400~8.5h
    #
    #     fpga.initial_dds([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    #     fpga.phase_clear_dds([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
    #     print('time consumpted', time.time()-t1)
    #
    #     play_ch_num_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    #
    #     fpga.phase_clear_dds(play_ch_num_list)
    #     play_address_word = fpga.data_download(play_ch_num_list, raw_data_list_list)
    #     # play_address_word = fpga.test_download(play_ch_num_list)
    #     # print bytes_to_hexstr(play_address_word)
    #     print('time consumpted', time.time()-t1)
    #
    #     t2=time.time()
    #     for jj in range(1):
    #         fpga.play(play_ch_num_list, play_address_word)
    #         # t2=time.time()
    #         # time.sleep(0.001)
    #         while True:
    #             a = fpga.read()
    #             if a == b'\x80\x80':
    #                 print(bytes_to_hexstr(a))
    #                 break
    #             else:
    #                 if len(a) != 0:
    #                     print(bytes_to_hexstr(a))
    #         print('time consumpted', time.time()-t2)
    #         # fpga.phase_clear_dds([0,2])#change the list
    #         #
    #         # a = fpga.read()
    #         # print bytes_to_hexstr(a)
    #         # fpga.phase_clear_dds([0])
    #
    #         # time.sleep(0.001)
    #     print('')
    #     print('time consumpted', time.time()-t1)










    # ##############  python3 test
    # ch_num_byte = b'\x00\x01'
    # # fpga.initial_AD9915(1)
    # print(b'\x00\x06' + ch_num_byte + b'\x00' + b'\x00\x00\x01\x01\x0A')
    # print(len(b'\x00\x06' + ch_num_byte + b'\x00' + b'\x00\x00\x01\x01\x0A'))
    # print(bytes_to_hexstr(b'\x00\x06' + ch_num_byte + b'\x00' + b'\x00\x00\x01\x01\x0A'))
    # fpga.write(b'\x00\x06' + ch_num_byte + b'\x00' + b'\x00\x00\x01\x01\x0A')
    #
    # fpga.s_configure(ch_num_byte, b'\x00', b'\x00\x01\x01\x0A')#con-phase  and amp en
    # fpga.s_configure(ch_num_byte, b'\x01', b'\x00\x80\x80\x00')
    # fpga.s_configure(ch_num_byte, b'\x03', b'\x01\x05\x21\x20')#DAC_CAL en
    # fpga.s_configure(ch_num_byte, b'\x03', b'\x00\x05\x21\x20')#DAC_CAL disable
    # print('initial finished!')
    # print(fpga.s_read(ch_num_byte, b'\x01', b'\x00\x80\x80\x00'))
    # print(fpga.l_read(ch_num_byte, b'\x0B', b'\x00\x00\x00\x00\x00\x00\x00\x00'))


    # # ##test spectrum
    # #
    # t1=time.time()
    # #
    # for ii in range(1):   #100    ~ 95 s        32400~8.5h
    #     fpga.initial_dds([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    #     fpga.phase_clear_dds([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
    #     print ('time consumpted', time.time()-t1)
    # frequency = 600
    # test_time = 1
    # t1=time.time()
    # a, b = fpga.cw_play(0,1,frequency,0)
    # print (a ,'    ',b)
    #
    # for ii in range(test_time):
    #     print (ii,'  ')
    #     time.sleep(1)
    # print ('time consumpted', time.time()-t1)
    # # fpga.cw_play(4,0,0,0)
    # # fpga.cw_play(ii,1,frequency,0)





    # fpga.write(b'\x00\x31'+b'\x00'+b'\x02'+b'\x20\x00')  # the b'\x02' can be b'\x03',b'\x04'
    #
    # fpga.write(b'\x00\x31'+b'\x00'+b'\x80'+b'\x80\x00')  # C
    # fpga.write(b'\x00\x31'+b'\x00'+b'\x40'+b'\xFF\xFC')  # M
    #
    # time.sleep(1)
    # fpga.write(b'\x00\x31'+b'\x00'+b'\xC0'+b'\xFF\xFC')  # X = +10
    # time.sleep(1)
    # fpga.write(b'\x00\x31'+b'\x00'+b'\xC0'+b'\x80\x00')  # X = 0
    # time.sleep(1)
    # fpga.write(b'\x00\x31'+b'\x00'+b'\xC0'+b'\x00\x00')  # X = -10

    # fpga.AD5371_SPI_TEST()


    # fpga.write(b'\x00\x31'+b'\x00'+b'\xC1'+b'\x80\x00')  # X_G0_0 = 0



    # ini_stamp=[1,2,4]
    # stamp_list=[25,50,100]
    # for ii in range(3):
    #     stamp_list[ii] = ini_stamp[ii]-1
    # fpga.AD5371_wr_stamp_set(stamp_list)
    # print("when stamp0, stamp1, stamp2 is %d, %d, %d" %(ini_stamp[0],ini_stamp[1],ini_stamp[2]))
    # for ii in range(10):
    #     fpga.write(b'\x00\x31'+b'\x00'+b'\xC9'+b'\x80\x00')  # X_G0_1 = +10
    #     time.sleep(2)
    #     # fpga.write(b'\x00\x31'+b'\x00'+b'\xC9'+b'\x80\x00')  # X_G0_1 = 0
    #     # time.sleep(5)
    #     fpga.write(b'\x00\x31'+b'\x00'+b'\xC9'+b'\x7F\xFC')  # X_G0_1 = -10
    #
    #     time.sleep(2)


    # # a = np.dtype('<i4')
    # for ii in range(258):
    #     a = num_to_bytes(ii, 2)
    #     c = a.hex()
    #     print('when ii is ', ii, ', a is ', a,', the ord() is ', c)
    #     b = bytes_to_num(a)
    #     print(b)
    #     # b = int.from_bytes(a, byteorder='big')
    #     # print(b)
    #     # b = int.from_bytes(a, byteorder='little')
    #     # print(b)

    # fpga.write(b'\x00\x00')
    # fpga.ad5371_ini()

    # g0_ch_list = [b'\x00\xC8',b'\x00\xC9',b'\x00\xCA',b'\x00\xCB',b'\x00\xCC',b'\x00\xCD',b'\x00\xCE',b'\x00\xCF']
    # g1_ch_list = [b'\x00\xD0',b'\x00\xD1',b'\x00\xD2',b'\x00\xD3',b'\x00\xD4',b'\x00\xD5',b'\x00\xD6',b'\x00\xD7']
    # g2_ch_list = [b'\x00\xD8',b'\x00\xD9',b'\x00\xDA',b'\x00\xDB',b'\x00\xDC',b'\x00\xDD',b'\x00\xDE',b'\x00\xDF']
    # g3_ch_list = [b'\x00\xE0',b'\x00\xE1',b'\x00\xE2',b'\x00\xE3',b'\x00\xE4',b'\x00\xE5',b'\x00\xE6',b'\x00\xE7']
    # g4_ch_list = [b'\x00\xE8',b'\x00\xE9',b'\x00\xEA',b'\x00\xEB',b'\x00\xEC',b'\x00\xED',b'\x00\xEE',b'\x00\xEF']
    # y_str = b''
    # sin_pts = 50
    # ch_num = 3
    # for x in range(sin_pts):
    #     y = np.sin((float(x)/sin_pts+0)*2*np.pi) * (2**13-1) + 2**13
    #     y_int = num_to_bytes(int(y)*4, 2)
    #     y_str += g0_ch_list[0]+ y_int + g0_ch_list[1]+ y_int #CC
    #     # print len(y_str)
    #     print ('the y and y_int are ', y, ',', bytes_to_hexstr(y_int))
    #
    # # y_str += g0_ch_list[0]+ b'\x80\x00' + g0_ch_list[4]+ b'\x80\x00' + g0_ch_list[1]+ b'\x80\x00' #CC
    # # y_str += g0_ch_list[0]+ b'\xB0\x08' + g0_ch_list[4]+ b'\x90\x08' + g0_ch_list[1]+ b'\x90\x08' #CC
    # # y_str += g0_ch_list[0]+ b'\xB0\x08' + g0_ch_list[4]+ b'\x90\x08' + g0_ch_list[1]+ b'\x90\x08' #CC
    # # y_str += g0_ch_list[0]+ b'\x80\x00' + g0_ch_list[4]+ b'\x80\x00' + g0_ch_list[1]+ b'\x80\x00' #CC
    # data_DAC = b''
    # cycles = 2
    # for ii in range(cycles):
    #     data_DAC += y_str
    #
    # # data_DAC += b'\x00'+b'\xC8'+ b'\x80\x00' + b'\x00'+b'\xCC'+ b'\x80\x00' #CC
    #
    # addr_start = b'\x00\x00\x00'
    # addr_stop = num_to_bytes(int(len(data_DAC)/4) -1, 3)
    # print (bytes_to_hexstr(b'\x00\x33' + addr_start + addr_stop))
    # fpga.write(b'\x00\x33' + addr_start + addr_stop + data_DAC)
    # time.sleep(0.01)
    #
    # # fpga.write(b'\x00\x36\x01\x19')  # 2 us for 00F9
    # # time.sleep(0.01)
    # fpga.ad5371_play_set(ch_num, [106,59,111])
    # # fpga.ad5371_play_set(ch_num, [200,250,200])
    # # addr_start = b'\x00\x00\x00'
    # # addr_stop = num_to_bytes(int(len(data_DAC)/4) -1, 3)
    # fpga.write(b'\x00\x01' + addr_start + addr_stop)
    # time.sleep(0.002)
    # fpga.write(b'\x00\x01' + addr_start + addr_stop)


# ############  10 ch test      fpga.ad5371_play_set(ch_num = 10, [106,59,111])
#
#     g0_ch_list = [b'\x00\xC8',b'\x00\xC9',b'\x00\xCA',b'\x00\xCB',b'\x00\xCC',b'\x00\xCD',b'\x00\xCE',b'\x00\xCF']
#     g1_ch_list = [b'\x00\xD0',b'\x00\xD1',b'\x00\xD2',b'\x00\xD3',b'\x00\xD4',b'\x00\xD5',b'\x00\xD6',b'\x00\xD7']
#     g2_ch_list = [b'\x00\xD8',b'\x00\xD9',b'\x00\xDA',b'\x00\xDB',b'\x00\xDC',b'\x00\xDD',b'\x00\xDE',b'\x00\xDF']
#     g3_ch_list = [b'\x00\xE0',b'\x00\xE1',b'\x00\xE2',b'\x00\xE3',b'\x00\xE4',b'\x00\xE5',b'\x00\xE6',b'\x00\xE7']
#     g4_ch_list = [b'\x00\xE8',b'\x00\xE9',b'\x00\xEA',b'\x00\xEB',b'\x00\xEC',b'\x00\xED',b'\x00\xEE',b'\x00\xEF']
#
#     y_str = b''
#     sin_pts = 50
#     ch_num = 10
#     for x in range(sin_pts):
#         y = np.sin((float(x)/sin_pts+0)*2*np.pi) * (2**13-1) + 2**13
#         y_int = num_to_bytes(int(y)*4, 2)
#         for ii in range(8):
#             y_str += g0_ch_list[ii] + y_int
#         y_str += g1_ch_list[0] + y_int
#         y_str += g1_ch_list[1] + y_int
#         # print len(y_str)
#         print('the y and y_int are ', y, ',', bytes_to_hexstr(y_int))
#
#
#
#     data_DAC = b''
#     cycles = 2
#     for ii in range(cycles):
#         data_DAC += y_str
#
# # for ii in range(8):
# #             y_str += g0_ch_list[ii] + y_int
# #
# #     data_DAC += b'\x00'+b'\xC8'+ b'\x80\x00' + b'\x00'+b'\xCC'+ b'\x80\x00' #CC
#
#     addr_start = b'\x00\x00\x00'
#     addr_stop = num_to_bytes(int(len(data_DAC)/4) -1, 3) #+ch_num
#     print(bytes_to_hexstr(b'\x00\x33' + addr_start + addr_stop))
#     fpga.write(b'\x00\x33' + addr_start + addr_stop + data_DAC)
#     time.sleep(0.01)
#
#     # fpga.write(b'\x00\x36\x01\x19')  # 2 us for 00F9
#     # time.sleep(0.01)
#     # fpga.ad5371_play_set(10, [124,74,10])
#     # fpga.ad5371_play_set(ch_num, [106,99,10])
#     fpga.ad5371_play_set(ch_num, [106,59,111])
#     # addr_start = b'\x00\x00\x00'
#     # addr_stop = num_to_bytes(int(30 * 10) -1, 3)
#     fpga.write(b'\x00\x01' + addr_start + addr_stop)
#     # time.sleep(2)
#     # fpga.write(b'\x00\x01' + addr_start + addr_stop)


# ############  40 ch test
#     g0_ch_list = [b'\x00\xC8',b'\x00\xC9',b'\x00\xCA',b'\x00\xCB',b'\x00\xCC',b'\x00\xCD',b'\x00\xCE',b'\x00\xCF']
#     g1_ch_list = [b'\x00\xD0',b'\x00\xD1',b'\x00\xD2',b'\x00\xD3',b'\x00\xD4',b'\x00\xD5',b'\x00\xD6',b'\x00\xD7']
#     g2_ch_list = [b'\x00\xD8',b'\x00\xD9',b'\x00\xDA',b'\x00\xDB',b'\x00\xDC',b'\x00\xDD',b'\x00\xDE',b'\x00\xDF']
#     g3_ch_list = [b'\x00\xE0',b'\x00\xE1',b'\x00\xE2',b'\x00\xE3',b'\x00\xE4',b'\x00\xE5',b'\x00\xE6',b'\x00\xE7']
#     g4_ch_list = [b'\x00\xE8',b'\x00\xE9',b'\x00\xEA',b'\x00\xEB',b'\x00\xEC',b'\x00\xED',b'\x00\xEE',b'\x00\xEF']
#
#     y_str = b''
#     sin_pts = 50
#     ch_num = 40
#     for x in range(sin_pts):
#         y = np.sin((float(x)/sin_pts+0)*2*np.pi) * (2**13-1) + 2**13
#         y_int = num_to_bytes(int(y)*4, 2)
#         for ii in range(8):
#             y_str += g0_ch_list[ii] + y_int
#             y_str += g1_ch_list[ii] + y_int
#             y_str += g2_ch_list[ii] + y_int
#             y_str += g3_ch_list[ii] + y_int
#             y_str += g4_ch_list[ii] + y_int
#         # y_str += g1_ch_list[0] + y_int
#         # y_str += g1_ch_list[1] + y_int
#         print(len(y_str))
#         print('the y and y_int are ', y, ',', bytes_to_hexstr(y_int))
#
#
#
#     data_DAC = b''
#     cycles = 2
#     for ii in range(cycles):
#         data_DAC += y_str
#
# # for ii in range(8):
# #             y_str += g0_ch_list[ii] + y_int
# #
# #     data_DAC += b'\x00'+b'\xC8'+ b'\x80\x00' + b'\x00'+b'\xCC'+ b'\x80\x00' #CC
#
#     addr_start = b'\x00\x00\x00'
#     addr_stop = num_to_bytes(int(len(data_DAC)/4) -1, 3) #+ch_num
#     print(bytes_to_hexstr(b'\x00\x33' + addr_start + addr_stop))
#     fpga.write(b'\x00\x33' + addr_start + addr_stop + data_DAC)
#     time.sleep(0.01)
#
#     # fpga.write(b'\x00\x36\x01\x19')  # 2 us for 00F9
#     # time.sleep(0.01)
#     # fpga.ad5371_play_set(40, [124,74,10])
#     # fpga.ad5371_play_set(ch_num, [106,59,111])
#     fpga.ad5371_play_set(ch_num, [106,59,111])
#     addr_start = b'\x00\x00\x00'
#     # addr_stop = num_to_bytes(int(30 * 10) -1, 3)
#     fpga.write(b'\x00\x01' + addr_start + addr_stop)
#     time.sleep(0.002)
#     # fpga.write(b'\x00\x01' + addr_start + addr_stop)

    # fpga.ad5371_ini()
    #
    #
    # y_str = b''
    # sin_pts = 100
    # for x in range(sin_pts):
    #     y = np.sin((float(x)/sin_pts+0.25)*2*np.pi) * (2**13-1) + 2**13
    #     y_int = num_to_bytes(int(y)*4, 2)
    #     y_str += b'\x00'+b'\xC8'+y_int
    #     # print len(y_str)
    #     print 'the y and y_int are ', y, ',', bytes_to_hexstr(y_int)
    #
    # data_DAC = b''
    # cycles = 10
    # for ii in range(cycles):
    #     data_DAC += y_str
    #
    # addr_start = b'\x00\x00\x00'
    # addr_stop = num_to_bytes(int(sin_pts * cycles) - 1, 3)
    # print bytes_to_hexstr(b'\x00\x33' + addr_start + addr_stop)
    # fpga.write(b'\x00\x33' + addr_start + addr_stop + data_DAC)
    # time.sleep(0.01)
    #
    # fpga.write(b'\x00\x36\x01\x19')  # 2/3 us for 00F9/0176
    # time.sleep(0.01)
    # addr_start = b'\x00\x00\x00'
    # addr_stop = num_to_bytes(int(100 * 10) -1, 3)
    # fpga.write(b'\x00\x01' + addr_start + addr_stop)



    ###data check function
    # while True:
    #     check_data_temp = fpga.read()
    #     if len(check_data_temp) == 0:
    #         break
    #     else:
    #         print bytes_to_hexstr(check_data_temp)

    # raw_data_list_1 = [   [[1,200,0],['high',5]],   [[0,200,0],['low',4]],    [[1,200,0],['high',5]]    ]
    # raw_data_list_2 = [   [[0.5,100,0.5],['high',10]],   [[0.1,100,0.5],['low',8]],    [[0.9,100,0.5],['high',10]]    ]
    # t1=time.time()
    # for kk in range(1):
    #     for jj in range(16):
    #         for ii in range(200):
    #             fpga.single_data_download(jj, raw_data_list_1)
    #             fpga.single_data_download(jj, raw_data_list_2)
    # print 'time consumpted', time.time()-t1





    ###test function
    # a, b = fpga.cw_play(1,1,200,0)
    # print a ,'    ',b
    # for ii in range(16):
    #     fpga.cw_play(ii,1,200,0)



    ####### this one is a simple one for test the frequency difference
    # a=fpga.dds_data_form(True,0.5,200,0.25)
    # print 'hp-dds result'
    # print bytes_to_hexstr(a[0])
    # print a[1], a[2]
    # b=fpga.dds_data_form(False,0.5,200,0.25)
    # print 'non-hp-dds result'
    # print bytes_to_hexstr(b[0])
    # print b[1], b[2]








    ######      protocol speed rate check
    # fpga.initial_AD9915(1)
    # fpga.initial_ad9910(4)
    # fpga.SPI_TEST(1,'0')
    # fpga.SPI_TEST(4,'1')

    # a, b=fpga.l_read(b'\x00\x10',b'\x0E',b'\x08\xb5\x00\x00\x00\x00\x00\x00')
    # print a, b

    # fpga.wr_stamp_set(5,[0,1,2])
    # fpga.rd_stamp_set(5,[4,9,13])#the error will occur
    # for ii in range(10):
    #     print "the %d time result:" %ii
    #     a=fpga.data_check(5, 4)
    #     print a
    #     if a:
    #        continue
    #     break
    ######      protocol speed rate check   (end)




















    ################former used, but has been integrated
    # fpga.initial_AD9915(3)    ####initial
    # fpga.initial_AD9915(2)
    # fpga.initial_AD9915(1)
    # fpga.initial_ad9910(4)
    # fpga.initial_ad9910(5)

    # fpga.phase_clear_2g5(3)   ####clear phase
    # fpga.phase_clear_2g5(2)
    # fpga.phase_clear_2g5(1)
    # fpga.phase_clear_1g(4)
    # fpga.phase_clear_1g(5)

    # fpga.mannual_sync_2g5()   ###mannual synchronization
    # fpga.mannual_sync_1g()

    ###     data_list_processing
    # a = fpga.raw_data_list_head([[[1,200,0],['high',10]],   [[0,200,0],['low',10]],    [[1,200,0],['high',10],['low',10]]])
    # print a
    # b=fpga.raw_data_list_tail(a)
    # print b
    # fpga.single_data_download(4, [[[1,200,0],['high',10]],   [[0,200,0],['low',10]],    [[1,200,0],['high',10],['low',10]]])

    # fpga.single_test_download(1)   ###test_data download
    # fpga.single_test_download(2)
    # fpga.single_test_download(3)

    ################former used, but has been integrated(end)









    ################ test call function
    ################ this part is really useless
    # a = fpga.pulse_data_gen(True,[[[1,200,0],['high',10]],   [[0,200,0],['low',10]],    [[1,200,0],['high',10],['low',10]]])
    # # print bytes_to_hexstr(a[0])
    # # print bytes_to_hexstr(a[1])
    # print bytes_to_hexstr(a[1][0:4])
    # print len(a[1][4:])     #this length is 4*ttl_num
    # print bytes_to_hexstr(a[2])


    # a = [[[1,200,0],['high',10]],   [[0,200,0],['low',10]],    [[1,200,0],['high',10],['low',10]]]
    # print a
    # fpga.raw_data_list_pro(a)
    # print a
    ################test call function(end)













    # # 最终使用的
    # fpga.start()

    # fpga.socket_server_new()



    # fpga.counter(cnt_time)

