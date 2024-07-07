import paho.mqtt.client as mqtt
import time
import json
import numpy as np

class Publisher:

    def __init__(self):

        self.broker_address = "localhost"  

        self.topics = ["test/topic1", "test/topic2", "test/topic3"]

        self.client = mqtt.Client(client_id="Publisher")

        self.client.connect(self.broker_address, 1883)


    def publish(self, topic, message):

        mqtt_msg = json.dumps(message)
        
        self.client.publish(topic, mqtt_msg)
        print(f"Published '{mqtt_msg}' to topic '{topic}'")
        time.sleep(5) 
