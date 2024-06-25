import paho.mqtt.client as mqtt
import time
import random

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
        self.client.connect(self.broker_address)


    def publish(self):
        # Select a random number and a random topic
        message = str(random.choice(self.numbers))
        topic = random.choice(self.topics)
        self.client.publish(topic, message)
        print(f"Published '{message}' to topic '{topic}'")
        time.sleep(5)  # Wait for 5 seconds before publishing again
