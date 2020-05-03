import pika
import threading
import json

def minWorker():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='min1')
    channel.basic_qos(prefetch_count=1)
    def minCallBack(ch, method, properties, body):
        args = json.loads(body)
        m = min(args)
        print(m)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    channel.basic_consume(queue='min1', on_message_callback=minCallBack)
    channel.start_consuming()


def maxWorker():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='max1')
    channel.basic_qos(prefetch_count=1)
    def maxCallBack(ch,method,properties,body):
        args = json.loads(body)
        m = max(args)
        print(m)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    channel.basic_consume(queue='max1', on_message_callback=maxCallBack)
    channel.start_consuming()

"""
def minCallBack(ch, method, properties, body):
    args = json.loads(body)
    m = min(args)
    print(m)
    ch.basic_ack(delivery_tag=method.delivery_tag)
"""
"""
def maxCallBack(ch,method,properties,body):
    args = json.loads(body)
    m = max(args)
    print(m)
    ch.basic_ack(delivery_tag=method.delivery_tag)
"""


maxer = threading.Thread(target=maxWorker).start()
miner = threading.Thread(target = minWorker).start()







