import paho.mqtt.client as mqtt

class Subscriber:

    def __init__(self):

        # Define the broker address
        self.broker_address = "localhost"  # Replace with the actual broker address

        # Define the topics
        self.topics = ["test/topic1", "test/topic2", "test/topic3"]

    # Define the callback function for when a message is received
    def on_message(self, client, userdata, message):
        global total_sum
        # Decode the incoming message and convert to an integer
        number = int(message.payload.decode())
        # Add the number to the total sum
        total_sum += number
        print(f"Received number '{number}' on topic '{message.topic}'")
        print(f"Current total sum: {total_sum}")

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
