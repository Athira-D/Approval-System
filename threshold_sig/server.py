from threading import Thread
import socket
addr_client = {}
clients  = {}

def incoming_connection():
   
    count = 0
    while count<2:
        #print("GGGG")
        conn, client_addr = s.accept()
        print(client_addr)
        #print(conn)
        addr_client[conn] = client_addr
        count=count+1
        #print (conn)
        Thread(target = client_connection, args = (conn,)).start()


def client_connection(conn):
    name = conn.recv(100).decode("utf8")
    clients[conn] = name

    while True:
        msg = conn.recv(100).decode("utf8")
        broadcast(msg,name+":")


def broadcast(msg,prefix):
    for sock in clients:
        #print(prefix)
        sock.send(bytes(prefix+msg,"utf8"))


host = 'localhost'
port = 12348
addr = (host,port)
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s.bind(addr)

s.listen(5)
print ("waiting for connection")
Thread (target = incoming_connection).start()
#Thread (target = incoming_connection).join()
