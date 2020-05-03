from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.connect(('localhost', 5000)) # connect to server (block until accepted)

toSend = input("Please enter an integer:").strip()

s.send(toSend.encode()) # send some data

data = s.recv(1024) # receive the response
print('Received', data) # print the result

s.close() # close the connection

