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
sighs = []
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
    global k
    clients[conn] = [name,sk[k]]
    conn.send("K "+str(sk[k]))
    #print(str(sk[k]))
    k=k+1
    #conn.send("P "+str(params_str))
    print ("in client_connection"+str(len(clients)))
    global counter
    counter = 0
    while True:
        msg = conn.recv(100).decode('utf8')
        index = msg.find(' ')
        init = msg[0:index]
        msg = msg[index + 1:]
        if init == 'I':
            broadcast(msg, name + ':')    
        if init == 'S':
            if counter < t:
               index2 = msg.find(' ')
               data = [int(msg[0:index2])]
            #print(data)
               key = msg[index2 + 1:]
               for ski in sk:
                    if str(ski) == key:
                        v = ski
            #print(key)
               sighs.append(sign(params, v, data))
               counter= counter +1
            else:
            	conn.send("Already Signed")
            	counter = counter +1
           #sigs = [sign(params, ski, data) for ski in sk]
            #print(sighs)
            if counter == t:
            	#sighs[2] = None
                sigma = aggregate_sigma(params, sighs)
	        print(sigma)
	        if verify(params, aggr_vk, sigma, data):
	            conn.send("Verified-PASSED")
	        else: 
	            conn.send("ERROR")
	    #conn.send("R "+str(sigma))




def broadcast(msg, prefix):
    for sock in clients:

        # print(prefix)

        sock.send(prefix + msg)


host = 'localhost'
port = 12354
addr = (host, port)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
params = setup()
print(params)
for t in params:
	params_str=params_str+','+str(t)
#print(len(params_str))	
(t, n) = (2, 3)	
(sk, vk) = ttp_keygen(params, t, n)
aggr_vk = aggregate_vk(params, vk)
s.bind(addr)

s.listen(5)
print 'waiting for connection'
Thread(target=incoming_connection).start()

# Thread (target = incoming_connection).join()
