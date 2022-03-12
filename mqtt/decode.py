"""
CAN帧数据解析模块

Author: 孙昊阳
Created on: 2022/03/12

Description: 解析CAN帧数据编码
# 解码基本规则如下：
* 一个通常的CAN常发帧数据通常有十六个字节，格式为：
  00 00 08 00 00 01 c7 86 82 33 44 77 77 66 66 d8
- 数据帧标志头为前2位，一般为“00 00”，即十六进制数0x00，0x00
- 第3个字节位置为蓄电池模块信息“08”，一般为0x0_，空格处即为模块ID
- 帧ID为第4-7字节部分“00 00 01 c7”，即ID[0] = 0x01，ID[1]=0xc7，为十六进制整数，
  是数据帧类型的判断依据，又称为仲裁帧
- 数据部分为8~15字节的位置：
  最高电压为“86 82”，即data[0] = 0x86，data[1] = 0x82，
  最低电压为“33 44”，即data[2] = 0x33，data[3] = 0x44，
  最高温度为“77 77”，即data[4] = 0x77，data[5] = 0x77，
  最低温度为“66 66”，即data[6] = 0x66，data[7] = 0x66
- 第16个字节为校验位，为前面十五个字节的和
* 一个通常的CAN请求帧数据通常有16个字节，唯一表示：
  00 00 0x 00 00 01 00 00 00 20 00 00 00 00 00 24
* 一个通常的CAN反馈帧数据通常包括16个字节，格式与位置和常发帧相同，
  反馈帧的帧ID有：
  0x1x4，0x1x5，0x1x6，0x1x7，0x1x8，0x1x9，0x1xa，0x1xb，0x1xc
- 当帧ID为0x1x4时，帧数据包含1-4号单体电池的电压值；
- 当帧ID为0x1x5时，帧数据包含5-8号单体电池的电压值；
- 当帧ID为0x1x6时，帧数据包含9-12号单体电池的电压值；
- 当帧ID为0x1x7时，帧数据包含1-4号单体电池的温度值；
- 当帧ID为0x1x8时，帧数据包含5-8号单体电池的温度值；
- 当帧ID为0x1x9时，此帧不做处理；
- 当帧ID为0x1xa时，帧数据包含13-16号单体电池的电压值；
- 当帧ID为0x1xb时，帧数据包含17-20号单体电池的电压值；
- 当帧ID为0x1xc时，帧数据包含21-24号单体电池的电压值；
"""


# K9120的CAN帧解码
class K9120CanDecode:
    # CAN帧数据，以数组形式存储
    frame = []

    def __init__(self, frame):
        """
        :param frame: CAN帧数据，以数组形式存储
        """
        self.frame = frame

    def get_module_id(self):
        """
        获取模块ID
        :return: 传入数据帧所在模块的ID
        """
        # 获取数据帧的模块ID部分
        ID = int(self.frame[2], base=16)
        # 解析模块ID为16进制数
        _ID = hex(ID & int(0xff))
        return _ID

    def get_frame_id(self):
        """
        获取单帧ID
        :return: 传入数据帧的帧ID
        """
        # 获取数据帧的5、6位位帧ID位
        ID = [
            int(self.frame[5], base=16),
            int(self.frame[6], base=16),
        ]
        # 解析帧ID位为十六进制数
        _ID = hex((ID[0] & 0xff) * 256 + (ID[1] & 0xff))
        return _ID

    def get_frame_data(self):
        """
        获取单帧的数据部分
        :return: 数据帧包含的8个字节数据部分
        """
        data = []
        for i in range(7, 16):
            data.append(hex(int(self.frame[i], base=16)))
        return data

    def get_frame_type(self):
        """
        获取帧类型：常发帧/请求帧/反馈帧
        :return: 代表帧类型的十六进制数
        """
        # 蓄电池协议规定，获取get_frame_id()处理后的结果，并取该结果的后四位形成新的type_id，
        # 来判断下一步的动作
        code = self.get_frame_id()
        code = hex(int(code, base=16) & 0x00f)
        # _code代表数据帧类型
        _code = ''
        # 扩展code有效数字位数
        if len(code) == 3:
            _code = code[0] + code[1] + '00' + code[2]
        elif len(code) == 4:
            _code = code[0] + code[1] + '0' + code[2]
        else:
            _code = code
        return _code

    def cell_vol_temp_info(self):
        """
        获得单体电池的最高最低电压、最高最低温度
        :return: res: [cellMaxVoltage, cellMinVoltage, cellMaxTemperature, cellMinTemperature]
        """
        frame_data = self.get_frame_data()
        res = []
        if int(frame_data[1], base=16) >> 7:
            res.append(0.0)
        else:
            res.append(float(
                (int(frame_data[0], base=16) & 0xff) + (int(frame_data[1], base=16) & 0x7f) * 0xff) / 1000
            )
        if int(frame_data[3], base=16) >> 7:
            res.append(0.0)
        else:
            res.append(float(
                (int(frame_data[2], base=16) & 0xff) + (int(frame_data[3], base=16) & 0x7f) * 0xff) / 1000
            )
        if int(frame_data[5], base=16) >> 7:
            res.append(0.0)
        else:
            res.append(float(
                (int(frame_data[4], base=16) & 0xff) + (int(frame_data[5], base=16) & 0x07) * 0xff) / 10 - 40
            )
        if int(frame_data[7], base=16) >> 7:
            res.append(0.0)
        else:
            res.append(float(
                (int(frame_data[6], base=16) & 0xff) + (int(frame_data[7], base=16) & 0x07) * 0xff) / 10 - 40
            )
        return res

    def get_cell_info(self, Type):
        """
        获取单体电池cell数据
        :param: type: 当type=1时返回电压数据，当type=2时返回温度数据
        :return: res: [cell_vol, cell_vol, cell_vol, cell_vol]
        """
        res = []
        _res = []
        frame_data = self.get_frame_data()
        # 将十六进制的frame帧数据转换成十进制数据
        for i in range(len(frame_data)):
            _res.append(int(frame_data[i], base=16))
        # 当Type = 1时代表此帧的数据部分为cell电压数据
        if Type == 1:
            for i in range(4):
                # 位溢出处理
                if _res[2 * i + 1] >> 7:
                    res.append(0.0)
                else:
                    res.append(float(
                        (_res[2 * i] & 0xff) + (_res[2 * i + 1] & 0x7f) * 0xff) / 1000
                    )
        # 当Type = 2时代表此帧的数据部分为cell温度数据
        if Type == 2:
            for i in range(4):
                # 位溢出处理
                if _res[2 * i + 1] >> 7:
                    res.append(0.0)
                else:
                    res.append((float(
                        (_res[2 * i] & 0xff) + (_res[2 * i + 1] & 0x07) * 0xff) - 400) / 10
                    )
        return res

    def sys_vol_temp_info(self, Type):
        """
        获得系统的最高最低电压， 最高最低温度信息
        :param: Type == 1 或 Type == 2
        :return: res: [sysMaxVoltage, sysMinVoltage, sysMaxTemperature, sysMinTemperature]
        """
        frame_data = self.get_frame_data()
        res = []
        _res = []
        # 将十六进制的frame帧数据转换成十进制数据
        for i in range(len(frame_data)):
            _res.append(int(frame_data[i], base=16))
        # 当Type == 1时代表此时帧中为系统的最高电压、最低电压、平均电压
        if Type == 1:
            res.append(float(
                ((_res[0] & 0xff) * 16 + ((_res[1] & 0xf0) >> 4))) / 1000
            )
            res.append(float(
                ((_res[1] & 0x0f) * 256 + (_res[2] & 0xff))) / 1000
            )
            res.append(float(
                ((_res[3] & 0xff) * 16 + ((_res[4] & 0xf0) >> 4))) / 1000
            )
        # 当Type == 2时代表此时帧中为系统的最高温度、最低温度、平均温度
        if Type == 2:
            res.append(float(
                ((_res[0] & 0xff) * 16 + ((_res[1] & 0xf0) >> 4))) / 10 - 40
            )
            res.append(float(
                ((_res[1] & 0x0f) * 256 + (_res[2] & 0xff))) / 10 - 40
            )
            res.append(float(
                ((_res[3] & 0xff) * 16 + ((_res[4] & 0xf0) >> 4))) / 10 - 40
            )
        return res

    def sys_res_load_info(self):
        """
        获取电池的电流、绝缘阻抗、电池端电压、负载端电压、剩余容量
        :return: res: [current, impedance, battery_terminal_voltage, load_terminal_voltage, SOC]
        """
        frame_data = self.get_frame_data()
        res = []
        _res = []
        # 将十六进制的frame帧数据转换成十进制数据
        for i in range(len(frame_data)):
            _res.append(int(frame_data[i], base=16))
        # 系统电流
        res.append(float(
            ((_res[0] & 0xff) * 256 + (_res[1] & 0xff))) / 40 - 1000
        )
        # 绝缘阻抗
        res.append(float(
            ((_res[2] & 0xff) * 256 + (_res[3] & 0xff))) / 4
        )
        # 电池端电压
        res.append(float(
            ((_res[4] & 0xff) * 16 + ((_res[5] & 0xf0) >> 4))) / 4
        )
        # 负载端电压
        res.append(float(
            ((_res[5] & 0x0f) * 256 + (_res[6] & 0xff))) / 4
        )
        # 电池剩余容量（SOC）
        res.append(float(
            (_res[7] & 0xff)) / 2
        )
        return res

    def get_relay_data(self):
        """
        获取系统继电器信息
        :return: res [relay1, relay2]
        """
        frame_data = self.get_frame_data()
        res = []
        _res = []
        # 将十六进制的frame帧数据转换成十进制数据
        for i in range(len(frame_data)):
            _res.append(int(frame_data[i], base=16))
        res.append(_res[0] & 0x30 >> 4)
        res.append(_res[0] & 0x0c >> 2)
        return res

    def get_max_voltage_position(self):
        """
        获取最大电压模块的位置信息
        :return: res: [] (length == 8)
        """
        frame_data = self.get_frame_data()
        res = []
        _res = []
        # 将十六进制的frame帧数据转换成十进制数据
        for i in range(len(frame_data)):
            _res.append(int(frame_data[i], base=16))
        res.append(_res[0] >> 4 & 0x0f)
        res.append(_res[0] & 0x0f)
        res.append(_res[1] >> 4 & 0x0f)
        res.append(_res[1] & 0x0f)
        res.append(_res[2] >> 4 & 0x0f)
        res.append(_res[2] & 0x0f)
        res.append(_res[3] >> 4 & 0x0f)
        res.append(_res[3] & 0x0f)
        return res

    def handle_frame_data(self):
        """
        将帧数据转换成十进制浮点数形式
        :return: 返回处理后的帧数据
        """
        res = None
        frame_data = self.get_frame_data()
        frame_id = self.get_frame_id()
        if hex(0x100) < frame_id < hex(0x400):
            # 此时帧数据为反馈帧数据
            code = self.get_frame_type()
            if code == '0x000':
                # 此帧ID表示单个电池的最高最低温度和最高最低电压
                res = self.cell_vol_temp_info()
            elif code == '0x002':
                # 报警信息
                pass
            elif code == '0x004':
                # 1-4号单体电池电压信息
                res = self.get_cell_info(1)
            elif code == '0x005':
                # 5-8号单体电池电压信息
                res = self.get_cell_info(1)
            elif code == '0x006':
                # 9-12号单体电池电压信息
                res = self.get_cell_info(1)
            elif code == '0x00a':
                # 13-16号单体电池电压信息
                res = self.get_cell_info(1)
            elif code == '0x00b':
                # 17-20号单体电池电压信息
                res = self.get_cell_info(1)
            elif code == '0x00c':
                # 21-24号单体电池电压信息
                res = self.get_cell_info(1)
            elif code == '0x007':
                # 1-4号单体电池温度信息
                res = self.get_cell_info(2)
            elif code == '0x008':
                # 5-8号单体电池温度信息
                res = self.get_cell_info(2)
            else:
                pass
        else:
            # 此时帧数据为常发帧数据
            if frame_id == hex(0x51):
                pass
            elif frame_id == hex(0x52):
                pass
            elif frame_id == hex(0x53):
                pass
            elif frame_id == hex(0x54):
                # 此帧包含电池系统的最大电压、最小电压和平均电压
                res = self.sys_vol_temp_info(1)
            elif frame_id == hex(0x55):
                # 此帧包含电池系统的最大温度、最小温度和平均温度
                res = self.sys_vol_temp_info(2)
            elif frame_id == hex(0x411):
                # 此帧包含电池系统的电流、绝缘阻抗、负载端电压、剩余容量
                res = self.sys_res_load_info()
            elif frame_id == hex(0x413):
                # 此帧包含继电器状态
                res = self.get_relay_data()
            elif frame_id == hex(0x415):
                pass
            elif frame_id == hex(0x416):
                # 处理相关电压最值模块单体位置信息
                res = self.get_max_voltage_position()
            elif frame_id == hex(0x417):
                pass
            else:
                pass
        return res


if __name__ == "__main__":
    Frame = ['00', '00', '08', '00', '00', '00', '55', '44', '33', '22', '11', '44', '33', '22', '11', 'd8']
    Can = K9120CanDecode(Frame)
    print('模块ID：' + Can.get_module_id())
    print('帧ID：' + Can.get_frame_id())
    data1 = Can.get_frame_data()
    str_data1 = ''
    for i in range(8):
        str_data1 += data1[i] + ' '
    print('帧数据：' + str_data1)
    print('帧类型：' + Can.get_frame_type())
    data2 = Can.handle_frame_data()
    str_data2 = ''
    for i in range(len(data2)):
        str_data2 += str(data2[i]) + ' '
    print('温度电压信息：' + str_data2)

    Frame1 = ['00', '00', '08', '00', '00', '04', '11', 'aa', '38', '22', '11', '44', '33', '22', '11', 'd8']
    Can1 = K9120CanDecode(Frame1)
    data3 = Can1.sys_res_load_info()
    str_data3 = ''
    for i in range(len(data3)):
        str_data3 += str(data3[i]) + ' '
    print('电流、阻抗、电压、容量信息：' + str_data3)

