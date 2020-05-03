import pika
import json
from threading import Thread
import random

def producer(workload, task_type):
    data = []       # random data array
    for i in range(workload):
        data.append(random.randint(0, 2**64-1))

    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue = task_type)

    channel.basic_publish(exchange='',
                      routing_key = task_type,
                      body = json.dumps(data))
    print("Sent for ", task_type)

    connection.close()

workload = 2000

for i in range(10):
    if random.randint(0,1)==0:
        thread_p=Thread(target=producer, args=(workload, 'max1'))
        thread_p.start()
        thread_p.join()
    else:
        thread_p=Thread(target=producer, args=(workload, 'min1'))
        thread_p.start()
        thread_p.join()
