import zmq
import time
import string


HOST = '127.0.0.1'
PORT = '50007'

context = zmq.Context()

php = 'tcp://'+ HOST +':'+ PORT # how and where to connect
s = context.socket(zmq.REQ) # create socket

s.connect(php) # block until connected
for i in range(0, 10):
    block = 'message'.encode()
    s.send(block) # send message
    message = s.recv() # block until response
    print (message) # print result
s.send(b'STOP') # tell server to stop
message = s.recv() # block until response
print (message) # print result
