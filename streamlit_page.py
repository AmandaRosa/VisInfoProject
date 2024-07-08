import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import subprocess
import time

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
            ("Canal 2", "Canal 3", "Canal 4", "Canal 5", "Canal 6", "Canal 7", "Canal 8"), index=6, key='selection_box')
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

st.title("Dashboard")

col1, col2, col3 = st.columns([2,1,7])

with col1:
    if "option_classifier" not in st.session_state:
        st.session_state["option_classifier"] = "Global"
    option_classifier = st.selectbox(
        "Qual página gostaria de visualizar?",
        ("Global", "MLP", "SVM", "DecisionTree", "RandomForest", "KNN", "NaiveBayes"), index=0, key="selection_classifier")
with col2:
    st.write(" ")
    st.write(" ")
    aplicar_opcao_classificador = st.button("Selecionar")

if aplicar_opcao_classificador == True:
    st.session_state["option_classifier"] = option_classifier

st.write("Selecionado:", st.session_state["option_classifier"])


def execution():

    if st.session_state["option_classifier"] == "Global":

        path = "./graphs/model_accuracies.html"
        path2 = "./graphs/True_Label_distribution_pie_chart.html"
        path3 = None

    elif st.session_state["option_classifier"] == "MLP":

        path = "./graphs/true_label_vs_mlp_subplot.html"
        path2 = "./graphs/MLP_distribution_pie_chart.html"
        path3 = "./graphs/MLP_fp_fn_results.html"

    elif st.session_state["option_classifier"] == "SVM":

        path = "./graphs/true_label_vs_svm_subplot.html"
        path2 = "./graphs/SVM_distribution_pie_chart.html"
        path3 = "./graphs/SVM_fp_fn_results.html"

    elif st.session_state["option_classifier"] == "DecisionTree":

        path = "./graphs/true_label_vs_decisiontree_subplot.html"
        path2 = "./graphs/DECISIONTREE_distribution_pie_chart.html"
        path3 = "./graphs/DECISIONTREE_fp_fn_results.html"

    elif st.session_state["option_classifier"] == "RandomForest":

        path = "./graphs/true_label_vs_randomforest_subplot.html"
        path2 = "./graphs/RANDOMFOREST_distribution_pie_chart.html"
        path3 = "./graphs/RANDOMFOREST_fp_fn_results.html"

    elif st.session_state["option_classifier"] == "KNN":

        path = "./graphs/true_label_vs_knn_subplot.html"
        path2 = "./graphs/KNN_distribution_pie_chart.html"
        path3 = "./graphs/KNN_fp_fn_results.html"

    elif st.session_state["option_classifier"] == "NaiveBayes":

        path = "./graphs/true_label_vs_naivebayes_subplot.html"
        path2 = "./graphs/NAIVEBAYES_distribution_pie_chart.html"
        path3 = "./graphs/NAIVEBAYES_fp_fn_results.html"

    # Divider
    st.write("------")


    with st.container():
        try:

            with open(path, 'r', encoding='utf-8') as file:
                html_data = file.read()
            st.components.v1.html(html_data, height=700, width=1750)

        except:
            pass

    with st.container():
        try:

            with open(path2, 'r', encoding='utf-8') as file:
                html_data = file.read()
            st.components.v1.html(html_data, height=500)

        except:
            pass

    with st.container():
        try:
            with open(path3, 'r', encoding='utf-8') as file:
                html_data = file.read()
            st.components.v1.html(html_data, height=500)
        except:
            pass


if __name__ == "__main__":

    if 'init' not in st.session_state:
        print('iniciou')
        st.session_state['init'] = True
        st.session_state['conectado'] = False
        st.session_state['analisando'] = False

    while True:
        execution()
        time.sleep(10)


