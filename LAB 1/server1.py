from socket import *

s = socket(AF_INET, SOCK_STREAM)
s.bind(('localhost', 5000))

s.listen()
print("Server listening...")

isDone = False
(conn, addr) = s.accept() # returns new socket and addr. client
while True: # forever
        data = conn.recv(1024) # receive data from client
        if not data: 
                isDone = True
                 # stop if client stopped
        conn.send(data+b'*') # return sent data plus an "*"
        if isDone:
                conn.close()
                s.listen()
                (conn,addr) = s.accept()
                isDone = False
conn.close() # close the connection
