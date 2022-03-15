"""
生成电池系统模拟数据帧

Author: 孙昊阳
Created on: 2022/03/14
API:
  - generate_module_id(_id=None)
  - generate_common_frame_id(num)
  - generate_feedback_frame_id(num)
  - generate_data(Type)
  - generate_verification(module_id, frame_id, data)
  - generate_frame(module_id, frame_id, data, veri)
"""


import random
from mqtt.decode import K9120CanDecode


def generate_module_id(_id=None):
    """
    生成随机模块ID
    :param _id: 指定的模块ID
    :return: 两位十六进制数，如‘08’，‘0c’等
    """
    if _id is None:
        _id = random.randint(1, 15)
    module_id = hex(_id)
    # 将module_id规范化为两位十六进制数
    if len(module_id) < 4:
        module_id = '0' + module_id[2]
    else:
        module_id = module_id[2:]
    return module_id


def generate_common_frame_id(num):
    """
    生成随机常发帧ID
    :param num 常发帧类型
    :return: 帧ID序列，如['00', '00', '01', '27']
    """
    frame_id_pool = (
        ['00', '00', '00', '54'],  # 包含系统最高电压最低电压和平均电压
        ['00', '00', '00', '55'],  # 包含系统最高温度最低温度和平均温度
        ['00', '00', '04', '11'],  # 包含系统电流、绝缘阻抗、负载端电压、剩余容量
        ['00', '00', '04', '13'],  # 包含继电器状态
        ['00', '00', '04', '16']   # 包含最高电压所在单体电池的位置
    )
    return frame_id_pool[num]


def generate_feedback_frame_id(num):
    """
    生成随机反馈帧ID
    :param num: 反馈帧类型
    :return: 帧ID序列，如['00', '00', '01', '27']
    """
    frame_id_pool = (
        ['00', '00', '01', '10'],  # 包含蓄电池系统的最高最低温度和最高最低电压
        ['00', '00', '01', '12'],  # 报警信息
        ['00', '00', '01', '14'],  # 1-4号单体电池电压信息
        ['00', '00', '01', '15'],  # 5-8号单体电池电压信息
        ['00', '00', '01', '16'],  # 9-12号单体电池电压信息
        ['00', '00', '01', '1a'],  # 13-16号单体电池电压信息
        ['00', '00', '01', '1b'],  # 17-20号单体电池电压信息
        ['00', '00', '01', '1c'],  # 21-24号单体电池电压信息
        ['00', '00', '01', '17'],  # 1-4号单体电池温度信息
        ['00', '00', '01', '18']   # 5-8号单体电池温度信息
    )
    return frame_id_pool[num]


def generate_data(Type):
    """
    随机生成CAN帧中所包含的数据
    :param Type: 需要生成数据的类型
    :return: 生成的随机数据序列，长度为8，如['88', '77', '55', '44', '22', '11', '33'', '44']
    """
    data = []
    if Type == 1:
        # 生成反馈帧单体电池Cell1-24电压信息
        standard_vol = 35
        offset = random.randint(0, 15)
        max_vol = standard_vol + offset
        min_vol = standard_vol - offset // 2
        data.append('44')
        data.append(str(max_vol))
        data.append('44')
        data.append(str(min_vol))
        offset = random.randint(0, 15)
        max_vol = standard_vol + offset
        min_vol = standard_vol - offset // 2
        data.append('44')
        data.append(str(max_vol))
        data.append('44')
        data.append(str(min_vol))
    elif Type == 2:
        # 生成反馈帧单体电池Cell1-8温度信息
        stanard_temp = 45
        offest = random.randint(0, 20)
        max_temp = stanard_temp + offest
        min_temp = stanard_temp - offest - 5
        data.append(str(max_temp))
        data.append('6c')
        data.append(str(min_temp))
        data.append('6c')
        offest = random.randint(0, 20)
        max_temp = stanard_temp + offest
        min_temp = stanard_temp - offest - 5
        data.append(str(max_temp))
        data.append('6c')
        data.append(str(min_temp))
        data.append('6c')
    elif Type == 3:
        # 生成反馈帧单体电池最高最低电压温度信息
        standard_vol = 35
        standard_temp = 45
        vol_offset = random.randint(0, 15)
        temp_offset = random.randint(0, 20)
        max_temp = standard_temp + temp_offset
        min_temp = standard_temp - temp_offset - 5
        max_vol = standard_vol + vol_offset
        min_vol = standard_vol - vol_offset // 2
        data.append('44')
        data.append(str(max_vol))
        data.append('44')
        data.append((str(min_vol)))
        data.append(str(max_temp))
        data.append('5c')
        data.append(str(min_temp))
        data.append('5c')
    elif Type == 4:
        # 生成常发帧系统电压信息
        standard_vol = 55
        offset = random.randint(0, 10)
        max_vol = standard_vol * offset * 10
        min_vol = standard_vol - offset - 5
        data.append('c5')
        data.append(str(max_vol))
        data.append('f2')
        data.append(str(min_vol))
        data.append('ed')
        for i in range(3):
            data.append(str(standard_vol + 5 * i))
    elif Type == 5:
        pass
    else:
        pass
    return data


def generate_verification(module_id, frame_id, data):
    """
    生成CAN帧数据的校验位
    :param module_id: 模块ID
    :param frame_id: 帧ID
    :param data: 帧数据部分
    :return: 校验位字符串
    """
    id1 = int(module_id, base=16)
    id2 = 0
    for i in range(len(frame_id)):
        id2 += int(frame_id[i], base=16)
    data_sum = 0
    for i in range(len(data)):
        data_sum += int(data[i], base=16)
    verification = id1 + id2 + data_sum
    return hex(verification)[3:]


def generate_frame(module_id, frame_id, data, veri):
    """
    生成一个CAN帧数据
    :param module_id: 模块ID
    :param frame_id: 帧ID
    :param data: 帧数据
    :param veri: 校验位
    :return: 一个完整的CAN数据帧
    """
    # 模拟CAN数据帧，共16位字节（len(frame)=16）
    frame = ['00', '00', module_id]
    for i in range(len(frame_id)):
        frame.append(frame_id[i])
    for i in range(len(data)):
        frame.append(data[i])
    frame.append(veri)
    return frame


if __name__ == "__main__":
    module_id = generate_module_id(45)
    frame_id = generate_feedback_frame_id(0)
    data = generate_data(3)
    veri = generate_verification(module_id, frame_id, data)
    frame = generate_frame(module_id, frame_id, data, veri)

    frame_str = ''
    for i in range(len(frame)):
        frame_str += frame[i]
    Can = K9120CanDecode(frame)
    data2 = Can.handle_frame_data()
    str_data2 = ''
    for i in range(len(data2)):
        str_data2 += str(data2[i]) + ' '

    print('CAN反馈帧：' + frame_str)
    print('模块ID：' + Can.get_module_id())
    print('帧ID：' + Can.get_frame_id())
    print('Masked ID：' + Can.get_frame_type())
    print('温度电压信息：' + str_data2)

    module_id = generate_module_id(32)
    frame_id = generate_common_frame_id(0)
    data_ = generate_data(4)
    veri = generate_verification(module_id, frame_id, data_)
    frame = generate_frame(module_id, frame_id, data_, veri)

    frame_str = ''
    for i in range(len(frame)):
        frame_str += frame[i]
    Can = K9120CanDecode(frame)
    data2 = Can.handle_frame_data()
    str_data2 = ''
    for i in range(len(data2)):
        str_data2 += str(data2[i]) + ' '

    print('CAN反馈帧：' + frame_str)
    print('模块ID：' + Can.get_module_id())
    print('帧ID：' + Can.get_frame_id())
    print('Masked ID：' + Can.get_frame_type())
    print('温度电压信息：' + str_data2)
