import zmq
import time

ctx = zmq.Context()
sock = ctx.socket(zmq.PUB)
sock.bind("tcp://127.0.0.1:1234")


print("Starting loop...")
i = 1
while True:
    msg = "TIME +Hi for the %d:th time..." % i
    msg2 = "DATE +Hi for the %d:th time..." % i
    sock.send_string(msg)
    time.sleep(1)
    sock.send_string(msg2)
    print("Sent string: %s ..." % msg)
    print("Sent string: %s ..." % msg2)
    i += 1
    time.sleep(1)

sock.close()
ctx.term()
