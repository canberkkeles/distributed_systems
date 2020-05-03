import time
import zmq
import random
import pprint
import threading

def producer():
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)
    socket.bind("tcp://127.0.0.1:5557")
    # Start your result manager and workers before you start your producers
    for num in range(10):
        work_message = {'num' : random.uniform(1,100)}
        socket.send_json(work_message)


def result_collector():
    context = zmq.Context()
    results_receiver = context.socket(zmq.PULL)
    results_receiver.bind("tcp://127.0.0.1:5558")
    
    even_nums = []
    
    for x in range(10):
        result = results_receiver.recv_json()
        even_nums.append(result['num'])
    print(even_nums)

tProducer = threading.Thread(target=producer)
tCollector = threading.Thread(target=result_collector)

tProducer.start()
tCollector.start()
         
            
tProducer.join()
tCollector.join()

