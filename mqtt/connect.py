import logging
import random
import datetime

from paho.mqtt import client as mqtt_client

# log日志配置项
logger = logging.getLogger()
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
# Configure stream handler for the cells
chandler = logging.StreamHandler()
chandler.setLevel(logging.INFO)
chandler.setFormatter(formatter)
logger.addHandler(chandler)
logger.setLevel(logging.INFO)


# 获取系统时间日期
today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# mqtt基本配置项
broker = 'broker.emqx.io'
port = 1883
topic = 'battery-monitor/mqtt'
client_id = f'battery-monitor-client-{random.randint(0, 1000)}'


# 连接函数
def mqtt_connect():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            logging.info('Connected to MQTT Broker!')
        else:
            logging.info('Failed to connect, return code {}\n'.format(rc))

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client
