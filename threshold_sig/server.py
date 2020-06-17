#!/usr/bin/python
# -*- coding: utf-8 -*-

from bls.scheme import *
from bls.utils import *

from threading import Thread
import socket
addr_client = {}
clients = {}
k=0
params_str=""

def incoming_connection():

    count = 0
    while count < 3:

        # print("GGGG")

        (conn, client_addr) = s.accept()
        print client_addr

        # print(conn)

        addr_client[conn] = client_addr
        count = count + 1


        # print (conn)

        Thread(target=client_connection, args=(conn, )).start()

    

def send_key(sk,clients):
	i=0
	print (len(clients))
	for sock in clients:
		print sk[i]
		print ("hiiiiiiiiii")
		sock.send("hello")
		i=i+1




def client_connection(conn):
    name = conn.recv(100).decode('utf8')
    global clients
    clients[conn] = name
    global k
    conn.send("K "+str(sk[k]))
    k=k+1
    print ("in client_connection"+str(len(clients)))

    while True:
        msg = conn.recv(100).decode('utf8')
        index = msg.find(' ')
        init = msg[0:index]
        msg = msg[index + 1:]
        if init == 'I':
            broadcast(msg, name + ':')






def broadcast(msg, prefix):
    for sock in clients:

        # print(prefix)

        sock.send(prefix + msg)


host = 'localhost'
port = 12342
addr = (host, port)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
(t, n) = (2, 3)
params = setup()
#print(params)
for t in params:
	params_str=params_str+','+str(t)
(sk, vk) = ttp_keygen(params, t, n)
s.bind(addr)

s.listen(5)
print 'waiting for connection'
Thread(target=incoming_connection).start()

# Thread (target = incoming_connection).join()
