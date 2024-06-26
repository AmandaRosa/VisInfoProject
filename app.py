from publisher import *
from features import *


sessao = Features()
publisher = Publisher()

while True:
    chave, valor = sessao.disparar()
    topic = "test/topic1"
    message = {f'{chave}': valor.tolist()}
    publisher.publish(topic, message)
