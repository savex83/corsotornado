# https://websockets.readthedocs.io/en/stable/intro.html
from websocket import create_connection
import random
import time

print('Apro connessione')
ws = create_connection("ws://127.0.0.1:8888/websocket/counters/")
print('Connessione aperta')
try:
    while True:
        if random.random() >= 0.9:
            ws.send('fallato')
        else:
            ws.send('ok')
        # result =  ws.recv()
        # print(result)
        time.sleep(1)
except KeyboardInterrupt:
    ws.close()
    print('Connessione chiusa')