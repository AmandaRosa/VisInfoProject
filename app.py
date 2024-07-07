from publisher import *
from features import *


publisher = Publisher()
sessao = Features()

while True:
    chave, valor = sessao.disparar()
    topic = "test/topic1"
    message = {f'{chave}': valor.tolist()}
    publisher.publish(topic, message)
