import paho.mqtt.client as mqtt

class Subscriber:

    def __init__(self):

        # Define the broker address
        self.broker_address = "localhost"  # Replace with the actual broker address

        # Define the topics
        self.topics = ["test/topic1", "test/topic2", "test/topic3"]

    # Define the callback function for when a message is received
    def on_message(self, client, userdata, message):


        mqtt_msg = message.payload.decode()

        print(f"Received number '{mqtt_msg}' on topic '{message.topic}'")

    def subscribe(self):

        # Create a new MQTT client instance
        self.client = mqtt.Client(client_id="Subscriber")

        # Attach the on_message callback function
        self.client.on_message = self.on_message

        # Connect to the broker
        self.client.connect(self.broker_address)

        # Subscribe to the topics
        for topic in self.topics:
            self.client.subscribe(topic)

        # Start the MQTT client loop
        self.client.loop_forever()
