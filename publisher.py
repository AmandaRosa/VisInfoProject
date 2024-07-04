import paho.mqtt.client as mqtt
import time
import json
import numpy as np

class Publisher:

    def __init__(self):

        # Define the broker address
        self.broker_address = "localhost"  # Replace with the actual broker address

        # Define the topics
        self.topics = ["test/topic1", "test/topic2", "test/topic3"]

        # Create a list of numbers from 0 to 10
        self.numbers = list(range(11))

        # Create a new MQTT client instance
        self.client = mqtt.Client(client_id="Publisher")

        # Connect to the broker
        self.client.connect(self.broker_address, 1883)


    def publish(self, topic, message):

        # msg = message.tolist()
        mqtt_msg = json.dumps(message)
        
        self.client.publish(topic, mqtt_msg)
        print(f"Published '{mqtt_msg}' to topic '{topic}'")
        time.sleep(1) 
