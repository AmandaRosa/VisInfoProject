import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from publisher import *
from features import *
from subscriber import *
import threading


st.sidebar.title("Bearing Fault Diagnosis Monitoring - Simulation")

col1, col2 = st.sidebar.columns(2)

with col1:
    input_conexao = st.sidebar.text_input("Broker Address:")
with col2:
    botao_input_conexao = st.sidebar.button("Conectar")
if botao_input_conexao:
    st.sidebar.success("Conectado!")

if __name__ == "__main__":
    st.title("MQTT with Streamlit")

    if 'init' not in st.session_state:
        st.session_state['init'] = True
        if 'subscriber_instance' not in st.session_state:
            st.session_state['subscriber_instance'] = Subscriber()

    while True:
        st.session_state['subscriber_instance'].subscriber()




