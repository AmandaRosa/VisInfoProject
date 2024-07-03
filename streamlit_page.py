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

if "option_classifier" not in st.session_state:
    st.session_state["option_classifier"] = "MLP"

col1, col2, col3 = st.sidebar.columns(3)

with col1:
    input_conexao = st.sidebar.text_input("Broker Address:")
with col2:
    botao_input_conexao = st.sidebar.button("Conectar")
with col3:
    botao_input_subscribe = st.sidebar.button("Analisar")
if botao_input_conexao:
    st.sidebar.success("Conectado!")

if __name__ == "__main__":
    st.title("Dashboard")

    if 'init' not in st.session_state:
        st.session_state['init'] = True
        if 'subscriber_instance' not in st.session_state:
            st.session_state['subscriber_instance'] = Subscriber()

    col1, col2, col3 = st.columns([2,1,7])

    with col1:
        option_classifier = st.selectbox(
            "Qual classificador gostaria de visualizar?",
            ("MLP", "SVM", "DecisionTree", "RandomForest", "KNN", "NaiveBayes"), index=0)
    with col2:
        st.write(" ")
        st.write(" ")
        aplicar_opcao_classificador = st.button("Selecionar")

    if aplicar_opcao_classificador == True:
        st.session_state["option_classifier"] = option_classifier
    st.write("Selecionado:", st.session_state["option_classifier"])

    st.write("------")

    col1, col2 = st.columns([3,2])

    with col1:

        st.write("Grafico de curvas")

        # fig, ax = plt.subplots()
        # ax.plot(time, fault1, label='Fault Type 1')
        # ax.plot(time, fault2, label='Fault Type 2')
        # ax.plot(time, fault3, label='Fault Type 3')
        # ax.set_xlabel("Time")
        # ax.set_ylabel("True/False")
        # ax.legend()
        # st.pyplot(fig)

    with col2:

        st.write("Gráfico de pizza")
        # labels = 'Fault Type 1', 'Fault Type 2', 'Fault Type 3'
        # sizes = [fault1.sum(), fault2.sum(), fault3.sum()]
        # fig1, ax1 = plt.subplots()
        # ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        # ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        # st.pyplot(fig1)

    st.write("gráfico de barras")
    # st.subheader("Fault Counts")
    # fig2, ax2 = plt.subplots()
    # bar_width = 0.35
    # index = np.arange(len(labels))
    # ax2.bar(index, sizes, bar_width, label='Fault Counts')
    # ax2.set_xlabel('Fault Type')
    # ax2.set_ylabel('Counts')
    # ax2.set_title('Counts by Fault Type')
    # ax2.set_xticks(index)
    # ax2.set_xticklabels(labels)
    # ax2.legend()
    # st.pyplot(fig2)
    
    while True:
        pass
        # st.session_state['subscriber_instance'].subscriber()
