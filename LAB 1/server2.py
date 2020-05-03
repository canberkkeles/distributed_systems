from socket import *

p = 82774018375762036230659850750851711854039699313175216914470363560945323457727
a0 = 26748908084769669758664722731140522800875206292361297608046702271758631669759
a1 = 59489944712712493230446426050522902095714591665803937192613571374709152682872
a2 = 71257019652372732006624209284281187993740077445682918560838974809666187201576
a3 = 55315635592811832356973556884353215645720087042315880077665613542569819620485
a4 = 20411929856341763513465955098957309007252776763418101366798367886225234827183
isDone = False

s = socket(AF_INET, SOCK_STREAM)
s.bind(('localhost', 5000))

s.listen()
print("Server listening...")

(conn, addr) = s.accept() # returns new socket and addr. client
while True: # forever
        data = conn.recv(1024) # receive data from client
        value = int(data.decode())
        if not data: 
                isDone = True # stop if client stopped
        if isDone:
                conn.close()
                s.listen()
                (conn,addr) = s.accept()
                isDone = False
        conn.send((str((a0 + (a1 * value) + (a2 * value ** 2) + (a3 * value ** 3) + (a4 * value ** 4)) % p).encode())) # return the polynomial
conn.close() # close the connection
