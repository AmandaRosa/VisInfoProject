import json
import paho.mqtt.client as mqtt

class Subscriber:

    def __init__(self):

        self.data = []

        # Define the broker address
        self.broker_address = "localhost"  # Replace with the actual broker address

        # Define the topics
        self.topics = ["test/topic1", "test/topic2", "test/topic3"]

    # Define the callback function for when a message is received
    def on_message(self, client, userdata, message):


        mqtt_msg = message.payload.decode()

        true_label = list(json.loads(mqtt_msg).keys())[0]

        print(f"Received number '{true_label}' on topic '{message.topic}'")

        self.data.append(true_label)

        ## chamar função que transforma para Dataframe cujas linhas são tempo e colunas são os labels e os valores são 0s e 1s 

        ## chamar aqui o modelo de predicao e resultados comparados aos gabaritos

        return mqtt_msg

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

        return self.client.on_message
