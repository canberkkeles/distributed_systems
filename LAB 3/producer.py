import zmq
from threading import Thread
import random

def maks(data):
    makks = data[0]
    for i in range(1, len(data)):
        if data[i] > makks:
            makks = data[i]
    return makks 

def minn(data):
    minn = data[0]
    for i in range(1, len(data)):
        if data[i] < minn:
            minn = data[i]
    return minn

# This function generates a random array of integers of length 'size'
# and sends it to workers in batches 
def producer(size, num, work_type):
    context = zmq.Context()
    push_socket = context.socket(zmq.PUSH)
    push_socket.bind("tcp://127.0.0.1:5153")
    data = []       # random data array
    for i in range(size):
        data.append(random.randint(0, 2**64-1))
        
    for i in range(0, num):
        data_to_send=data[i*(size//num):(i+1)*(size//num)]
        if work_type == 0:
            work_message = ['minimum', data_to_send]
        else:
            work_message = ['maksimum', data_to_send]
        push_socket.send_json(work_message)

# Collects the partial results
# Then calling either minn or maks function compute the overall result 
def res_collector(num):
    context = zmq.Context()
    collector_socket = context.socket(zmq.PULL)
    collector_socket.bind("tcp://127.0.0.1:5159")
    res_maks = []
    res_minn = []
    for i in range(0, num):
        result = collector_socket.recv_json()
        if result[1] == "maksimum":
            res_maks.append(result[2])
            print("worker id: ", result[0], "Partial "+result[1]+":", result[2])
        else:
            res_minn.append(result[2])
            print("worker id: ", result[0], "Partial "+result[1]+":", result[2])

    if len(res_maks) >0:
        print("Overall maksimum: ", maks(res_maks))
    else:
        print("Overall minimum: ",  minn(res_minn))

batch = 10
workload = 200000

work_type = random.randint(0,1)  # random choice of minimum or maksimum
thread_p=Thread(target=producer, args=(workload, batch, work_type))
thread_p.start()

thread_c = Thread(target = res_collector, args=[batch])
thread_c.start()
