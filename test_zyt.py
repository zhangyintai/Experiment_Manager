import device
from device import num_to_bytes, bytes_to_num, bytes_to_hexstr
import dds
import time

fpga = device.FPGA(1, False)
fpga.initial_dds()
# fpga.play(0, [[1, 1, 0]])

# for i in range(0, 16):
#     channel_list.append(i)
#     raw_data_list.append([])
#     raw_data_list[i].append([4, [1, 1, 0], ['high', 10]])
#     #raw_data_list[i].append([1, [1, 1, 0], ['low', 10]])
#
# print(raw_data_list)

channel_list =[4,5] # Change to channel 8 will be fine
raw_data_list = []
raw_data_list.append([])
raw_data_list.append([])
t1 = 10
t2 = 20
t3 = 50
play_list = []

#fpga.ttl_set(4, level)

# for k in range (0,2):
#     for j in range (2,10):
#         raw_data_list[0].clear()
#         raw_data_list[0].append([0, [1, 10**(k-2), 0], ['high', j * 40]])
#         raw_data_list[0].append([0, [0, 1, 0], ['low', t2]])
#         raw_data_list[0].append([0, [1, 10**(k-2), 0], ['high', j * 40]])
#         raw_data_list[0].append([0, [0, 1, 0], ['low', t3]]) #For collecting data
#
#         fpga.sequence_data_download(channel_list, raw_data_list)
#         play_list = [[10, 10**(k-2), 0]]
#         fpga.play(0, play_list)

for k in range(1, 3):

    # config channel who controls the Ramsay
    raw_data_list[0].clear()
    raw_data_list[0].append([0, [1, 0.05 * k, 0], ['high', 10]])
    raw_data_list[0].append([0, [0, 1, 0], ['low', t2]])
    raw_data_list[0].append([0, [1, 0.05 * k, 0], ['high', 10]])
    raw_data_list[0].append([0, [0, 1, 0], ['low', t3]])

    # config the channel that control the detecting by switching on the AOM
    raw_data_list[1].clear()
    raw_data_list[1].append([0, [1, 0.05 * k, 0.5], ['high', 50]])
    raw_data_list[1].append([0, [0, 1, 0], ['low', t2]])
    raw_data_list[1].append([0, [1, 0.05 * k, 0], ['high', 10]])
    raw_data_list[1].append([0, [0, 1, 0], ['low', t3]])

    # t_start = time.time()
    fpga.sequence_data_download(channel_list, raw_data_list)
    # print(k, 'th time consume is', time.time()-t_start)

    play_list = [[2, 10, 10], [2, 20, 20], [1, 100, 100]]

    # The detection time are set to be this way so that I can figure out if the duration is correct
    fpga.play(0, play_list)
    # time.sleep(0.01)
    # 0: no scan; 1: scan both amplitudes; 2: scan both frequencies; 3: scan both initial phases; 4: scan both durations
    # If one of the parameters are not scanned, set bo be constant

    # ch_num=channel_list[0]
    # print('current ch_num is ', ch_num)
    # hp_channel, reg_wr = fpga.ch2identify(ch_num)
    # ch_num_byte = num_to_bytes(2**ch_num, 2)
    # print(fpga.l_read(ch_num_byte, reg_wr, right_rd=b'\x00\x00\x00\x00\x00\x00\x00\x00'))
    #
    # ch_num=channel_list[1]
    # print('current ch_num is ', ch_num)
    # hp_channel, reg_wr = fpga.ch2identify(ch_num)
    # ch_num_byte = num_to_bytes(2**ch_num, 2)
    # print(fpga.l_read(ch_num_byte, reg_wr, right_rd=b'\x00\x00\x00\x00\x00\x00\x00\x00'))

