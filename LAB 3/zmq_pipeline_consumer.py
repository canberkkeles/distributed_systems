import time
import zmq
import random
import pprint
import threading
import math

def consumer():
    consumer_id = threading.current_thread().ident
    print("I am consumer " ,consumer_id)  #get thread id
    context = zmq.Context()
    # recieve work
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect("tcp://127.0.0.1:5557")
    # send work
    consumer_sender = context.socket(zmq.PUSH)
    consumer_sender.connect("tcp://127.0.0.1:5558")
    
    while True:
        work = consumer_receiver.recv_json()
        print(consumer_id, ' received work', work)
        data = work['num']
        result = { 'consumer' : consumer_id, 'num' : math.ceil(data)}
        print('sending result to collector', result['num'])
        consumer_sender.send_json(result)


for i in range(10):
    consumer_id = random.randrange(1,10005)
    pConsumer = threading.Thread(target=consumer).start()

