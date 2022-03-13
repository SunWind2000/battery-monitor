import logging
import time
import random

from mqtt.connect import topic, mqtt_connect


# CAN帧数据模拟模块：
# CAN帧数据一共有16个字节，
# 字节（1-2）：帧头，开始标志，一般为0x00 0x00；
# 字节（3）：帧信息，格式为 0x0_，后一位等于有效数据的字节；
# 字节（4-7）：帧ID，又称为仲裁帧，是数据帧类型的判断依据；
# 字节（8-15）：帧数据，8个字节，不够 8个，用0x00填充；
# 字节（16）：SUM，前面15个字节的总和，是校验位。


# 模拟生成CAN常发帧数据，在应用到生产环境时可去掉此函数
def generate_common_data():
    pass


# 消息发布函数
def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"message:{msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            logging.info(f"Send `{msg}` to topic `{topic}`")
        else:
            logging.info(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = mqtt_connect()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()

