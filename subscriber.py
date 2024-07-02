import json
import paho.mqtt.client as mqtt
from timedomain import *
import pickle
import sklearn
from streamlit_page import *

class Subscriber:

    def __init__(self):

        self.data = {
            'True_Label': [],
            'MLP': [],
            'SVM': [],
            'KNN': [],
            'RANDOMFOREST': [],
            'DECISIONTREE': [],
            'NAIVEBAYES' : []
        }

        # Define the broker address
        self.broker_address = "localhost"  # Replace with the actual broker address

        # Define the topics
        self.topics = ["test/topic1", "test/topic2", "test/topic3"]

    # Define the callback function for when a message is received
    def on_message(self, client, userdata, message):


        mqtt_msg = message.payload.decode()

        data_dict = json.loads(mqtt_msg)

        true_label = list(data_dict.keys())[0]

        data_array = np.array(data_dict[true_label])   

        self.predict(true_label, data_array)

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
    
    def predict(self, true_label, message):

        legend = {
            '0': 'Normal',
            '1': 'Normal',
            '2': 'Unbalanced_30g',
            '3': 'Horizontal_Mis_2mm',
            '4': 'Vertical_Mis_127mm',
            '5': 'Vertical_127_Hor_2_Mis',
            '6': 'Unbalanced_30g_Hor_Mis_2mm',
            '7': 'Unbalanced_30g_Ver_Mis_127mm'
        }

        classifiers = ['MLP', 'SVM', 'KNN', 'RANDOMFOREST', 'DECISIONTREE', 'NAIVEBAYES']

        with open('./Modelos/MLP.pkl', 'rb') as file:
            mlp = pickle.load(file)

        with open('./Modelos/SVM.pkl', 'rb') as file:
            svm = pickle.load(file)

        with open('./Modelos/KNN.pkl', 'rb') as file:
            knn = pickle.load(file)

        with open('./Modelos/RandomForest.pkl', 'rb') as file:
            rf = pickle.load(file)

        with open('./Modelos/DecisionTree.pkl', 'rb') as file:
            dt = pickle.load(file)

        with open('./Modelos/NaiveBayes.pkl', 'rb') as file:
            nb = pickle.load(file)

        models = [mlp, svm, knn, rf, dt, nb]

        self.data['True_Label'].append(true_label)

        for idx, model in enumerate(models):
            y_pred = model.predict(message)
            self.data[classifiers[idx]].append(legend[str(int(y_pred[-1]))])

        self.app.streamlit_page(self.data)




        


