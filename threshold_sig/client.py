from bls.scheme import *
from bls.utils import *
import socket
from threading import Thread
key=0

def receive():
    while True:
        data = c.recv(102).decode("utf8")
        print(data)
        index = data.find(' ')
        init = data[0:index]
        data = data[index + 1:]
        if init == 'K':
        	global key
        	key=int(data)

           

host = 'localhost'
port = 12342
addr = (host,port)
c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
x=c.connect(addr)
print("enter your name")
name = raw_input()
c.send(name)
Thread(target = receive).start()
while True:
    #print(name,end = '')
    data = raw_input()
    index = msg.find(' ')
    init = msg[0:index]
    msg = msg[index + 1:]
    if init == 'S':


    c.send(data)



