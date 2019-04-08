import device

fpga = device.FPGA(1, False)

# initial DDS
fpga.initial_dds()
fpga.cw_play(4, 1, 1, 0)
print("help")
fpga.initial_dds()
# define channel
channel_list = [4, 5, 6, 8]
raw_data_list = []
raw_data_list.append([])
raw_data_list.append([])
raw_data_list.append([])
raw_data_list.append([])


for i in range(1, 9):

    raw_data_list[0].clear()
    raw_data_list[0].append([0, [0, 0.1, 0], ['low', 10]])
    raw_data_list[0].append([0, [1, 0.1, 0], ['high', 60]])

    raw_data_list[1].clear()
    raw_data_list[1].append([0, [0, 0, 0], ['low', 10]])
    raw_data_list[1].append([2, [1, 1, 0.5], ['high', i * 10]])
    raw_data_list[1].append([0, [0, 0.15, 0], ['low', 10]])
    raw_data_list[1].append([2, [1, 0.1, 0], ['high', i * 10]])
    raw_data_list[1].append([0, [0, 0.15, 0], ['low', 10]])

    raw_data_list[2].clear()
    raw_data_list[2].append([0, [0, 100, 0], ['low', 140 + i * 100]])
    raw_data_list[2].append([0, [1, 100, 0], ['high', 20]])

    raw_data_list[3].clear()
    raw_data_list[3].append([0, [0, 0, 0], ['low', 160]])
    raw_data_list[3].append([0, [0, 0, 0], ['high', i * 100]])

    fpga.sequence_data_download(channel_list, raw_data_list)

    play_list = [[2, 30, 0], [2, 0.1, 0], [2, 0.1, 0], [2, 200, 0], [2, 200, 0]]

    fpga.play(2, play_list)

