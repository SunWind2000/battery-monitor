import logging

from mqtt.connect import topic, mqtt_connect


def subscribe(client):
    def on_message(client, userdata, msg):
        logging.info(f"Received '{msg.payload.decode()}' from '{msg.topic}' topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = mqtt_connect()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
