import time
import zmq
import random
import pprint
import threading
import math


def consumer():
    consumer_id = threading.current_thread().ident

    print("Consumer: ", consumer_id)

    context = zmq.Context()

    # Reciever Socket
    recieveSocket = context.socket(zmq.PULL)
    recieveSocket.connect("tcp://127.0.0.1:5153")


    # Sender Socket
    sendSocket = context.socket(zmq.PUSH)
    sendSocket.connect("tcp://127.0.0.1:5159")

    while True:
        work = recieveSocket.recv_json()
        # print(type(work[1:]))

        if(work[0] == "minimum"):
            toSend = min(work[1])
            result = [consumer_id,"minimum",toSend]
        else:
            toSend = max(work[1])
            result = [consumer_id,"maksimum",toSend]
        sendSocket.send_json(result)
        


for i in range(10):
    # consumer_id = random.randrange(1,10005)
    pConsumer = threading.Thread(target=consumer).start()

