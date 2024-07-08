import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from publisher import *
from features import *
from subscriber import *


st.set_page_config(
    layout="wide",
    page_title="Dashboard",
    initial_sidebar_state="collapsed",
)


st.sidebar.title("Bearing Fault Diagnosis Monitoring - Simulation")

col1, col2, col3 = st.sidebar.columns(3)

with col1:
    input_conexao = st.sidebar.text_input("Broker Address:")
    option_channel= st.sidebar.selectbox(
            "Qual canal gostaria de visualizar?",
            ("Canal 2", "Canal 3", "Canal 4", "Canal 5", "Canal 6", "Canal 7", "Canal 8"), index=6)
with col2:
    botao_input_conexao = st.sidebar.button("Conectar")
with col3:
    botao_input_subscribe = st.sidebar.button("Analisar")
if botao_input_conexao:
    st.session_state['conectado']= True
    st.sidebar.success("Conectado!")

if botao_input_subscribe:
    st.session_state['analisando']= True
    st.sidebar.success("Analisando...")
    st.session_state['subscriber_instance'].subscriber()

if __name__ == "__main__":
    st.title("Dashboard")

    if 'init' not in st.session_state:
        st.session_state['init'] = True
        if 'subscriber_instance' not in st.session_state:
            st.session_state['subscriber_instance'] = Subscriber()
            st.session_state['conectado'] = False
            st.session_state['analisando'] = False

    col1, col2, col3 = st.columns([2,1,7])

    with col1:
        if "option_classifier" not in st.session_state:
            st.session_state["option_classifier"] = "Global"
        option_classifier = st.selectbox(
            "Qual página gostaria de visualizar?",
            ("Global", "MLP", "SVM", "DecisionTree", "RandomForest", "KNN", "NaiveBayes"), index=0)
    with col2:
        st.write(" ")
        st.write(" ")
        aplicar_opcao_classificador = st.button("Selecionar")

    if aplicar_opcao_classificador == True:
        st.session_state["option_classifier"] = option_classifier
    
    st.write("Selecionado:", st.session_state["option_classifier"])

    # Divider
    st.write("------")

    if st.session_state['conectado'] == True and st.session_state['analisando'] ==True:

        col1, col2 = st.columns(2)

        with col1:

            if st.session_state["option_classifier"] == "Global":

                st.write("Gráfico de barras")

                with open("./graphs/model_accuracies.html", 'r', encoding='utf-8') as file:
                    html_data = file.read()
                st.components.v1.html(html_data, height=5000)

            elif st.session_state["option_classifier"] == "MLP":

                with open("./graphs/true_label_vs_mlp_subplot.html", 'r', encoding='utf-8') as file:
                    html_data = file.read()
                st.components.v1.html(html_data, height=5000)

            elif st.session_state["option_classifier"] == "SVM":

                with open("./graphs/true_label_vs_svm_subplot.html", 'r', encoding='utf-8') as file:
                    html_data = file.read()
                st.components.v1.html(html_data, height=5000)

            elif st.session_state["option_classifier"] == "DecisionTree":

                with open("./graphs/true_label_vs_decisiontree_subplot.html", 'r', encoding='utf-8') as file:
                    html_data = file.read()
                st.components.v1.html(html_data, height=5000)

            elif st.session_state["option_classifier"] == "RandomForest":

                with open("./graphs/true_label_vs_randomforest_subplot.html", 'r', encoding='utf-8') as file:
                    html_data = file.read()
                st.components.v1.html(html_data, height=5000)

            elif st.session_state["option_classifier"] == "KNN":

                with open("./graphs/true_label_vs_knn_subplot.html", 'r', encoding='utf-8') as file:
                    html_data = file.read()
                st.components.v1.html(html_data, height=5000)

            elif st.session_state["option_classifier"] == "NaiveBayes":

                with open("./graphs/true_label_vs_naivebayes_subplot.html", 'r', encoding='utf-8') as file:
                    html_data = file.read()
                st.components.v1.html(html_data, height=5000)

        with col2:
    
            if st.session_state["option_classifier"] == "Global":

                st.write("GLobal")

            elif st.session_state["option_classifier"] == "MLP":

                with open("./graphs/MLP_distribution_pie_chart.html", 'r', encoding='utf-8') as file:
                    html_data = file.read()
                st.components.v1.html(html_data, height=5000)

            elif st.session_state["option_classifier"] == "SVM":

                with open("./graphs/SVM_distribution_pie_chart.html", 'r', encoding='utf-8') as file:
                    html_data = file.read()
                st.components.v1.html(html_data, height=5000)

            elif st.session_state["option_classifier"] == "DecisionTree":

                with open("./graphs/DECISIONTREE_distribution_pie_chart.html", 'r', encoding='utf-8') as file:
                    html_data = file.read()
                st.components.v1.html(html_data, height=5000)

            elif st.session_state["option_classifier"] == "RandomForest":

                with open("./graphs/RANDOMFOREST_distribution_pie_chart.html", 'r', encoding='utf-8') as file:
                    html_data = file.read()
                st.components.v1.html(html_data, height=5000)

            elif st.session_state["option_classifier"] == "KNN":

                with open("./graphs/KNN_distribution_pie_chart.html", 'r', encoding='utf-8') as file:
                    html_data = file.read()
                st.components.v1.html(html_data, height=5000)

            elif st.session_state["option_classifier"] == "NaiveBayes":

                with open("./graphs/NAIVEBAYES_distribution_pie_chart.html", 'r', encoding='utf-8') as file:
                    html_data = file.read()
                st.components.v1.html(html_data, height=5000)