import time
from datetime import datetime
import logging
import json

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

logging.basicConfig(level=logging.INFO)


class MQTTWebSocketsClient:

    def __init__(self, client_id, host, topics, root_ca_path):
        self.client = AWSIoTMQTTClient(client_id, useWebsocket=True)
        self.client.configureEndpoint(host, 443)
        self.client.configureCredentials(root_ca_path)

        self.client.connect()
        # Subscribes to all of the given topics
        # topics = [(<topic>, <QoS>),]
        for t in topics:
            self.client.subscribe(t[0], t[1], self.on_message)

        self.messages = []

    def on_message(self, client, user_data, message):
        logging.info(f"Message was received on topic '{message.topic}':")
        logging.info(datetime.utcfromtimestamp(message.timestamp)
                     .strftime('%m-%d -> %H:%M:%S'))
        logging.info(message.payload)

        self.messages.append(message)

    @staticmethod
    def run():
        while True:
            time.sleep(1)


if __name__ == "__main__":
    client = MQTTWebSocketsClient("C1", "a2l18ps0rkgzno-ats.iot.us-east-1.amazonaws.com",
                                  [("cars/test_calls", 1)], "./certificates/rootCA.crt")
    client.run()
