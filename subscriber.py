import json
import paho.mqtt.client as mqtt
from timedomain import *
import pickle
import sklearn
import streamlit as st
from graphs import *
from collections import Counter
from scipy.stats import mode

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

        self.acc = {}
        self.data_counter = {
            'True_Label': [],
            'MLP': [],
            'SVM': [],
            'KNN': [],
            'RANDOMFOREST': [],
            'DECISIONTREE': [],
            'NAIVEBAYES' : []
        }

        self.data_normal_fault = {
            'True_Label': [],
            'MLP': [],
            'SVM': [],
            'KNN': [],
            'RANDOMFOREST': [],
            'DECISIONTREE': [],
            'NAIVEBAYES' : []
        }
        self.broker_address = "localhost"  
        self.topics = ["test/topic1", "test/topic2", "test/topic3"]

    def calculate_accuracy(self, data):
        for idx, key in enumerate(self.data.keys()):
            correct = np.sum(np.array(self.data['True_Label']) == np.array(self.data[key]))
            # print(self.data)
            self.acc[key] = f"{correct / len(self.data['True_Label']) * 100:.2f}"

        for key, value in data.items():
            label_counts = Counter(value)
            label_counts_list = [[label, count] for label, count in label_counts.items()]
            self.data_counter[key] = label_counts_list
            normal_count = label_counts['Normal']
            fault_count = sum(count for label, count in label_counts.items() if label != 'Normal')

            self.data_normal_fault[key] = {
                "Normal": normal_count,
                "Fault": fault_count
            }

        return self.acc, self.data_counter, self.data_normal_fault

    def on_message(self, client, userdata, message):


        mqtt_msg = message.payload.decode()

        data_dict = json.loads(mqtt_msg)

        true_label = list(data_dict.keys())[0]

        data_array = np.array(data_dict[true_label])

        accuracies, occurrences, data, normal_fault = self.predict(true_label, data_array)

        print_accuracies(accuracies)

        print_occurrences(occurrences)

        print_data_bruta(data)

        print_normal_fault(normal_fault)

        return st.session_state

    def calling_subscriber(self):

        self.client = mqtt.Client(client_id="Subscriber")
        self.client.on_message = self.on_message
        self.client.connect(self.broker_address)

        for topic in self.topics:
            self.client.subscribe(topic)

        self.client.loop_forever()
    
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
            unique_nparray = np.concatenate(message)
            y_pred = model.predict(unique_nparray.reshape(-1,1))
            mode_value, _ = mode(y_pred)
            self.data[classifiers[idx]].append(legend[str(int(mode_value))])

        acuracies, occurrences, normal_fault = self.calculate_accuracy(self.data)

        return acuracies, occurrences, self.data, normal_fault






        


