from bls.scheme import *
from bls.utils import *
import socket
from threading import Thread
key=0
params=()
curr=" "

def receive():
    while True:
        data = c.recv(10000).decode("utf8")
        print(data)
        index = data.find(' ')
        init = data[0:index]
        data = data[index + 1:]
        i2=data.find(' ')
        sec=data[0:i2]
        if sec=="Approved":
		global curr
		curr=" "
        if init == 'K':
        	global key
        	key=int(data)
        	#print(key)
        if init=='P':
            data=data.split(',')
            global params
            for i in range(0,len(data)):
                params[i]=int(data[i])
        if init=='R':
            global sigma
            sigma = data
            print(sigma)
            

           

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
    index = data.find(' ')
    init = data[0:index]
    msg = data[index + 1:]
    if init == 'I':
    	c.send(data)
        curr=" "
    if init == 'S':
        if curr== msg:
            print("Already signed this transaction  ")
        else:
	 curr=msg
	 c.send(data+" "+str(key))
           
 

