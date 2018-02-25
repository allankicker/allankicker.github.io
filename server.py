#!/usr/bin/env python
# coding: utf-8 

import socket
import sys
from threading import Thread


client_sockets=[]

class ClientSock(object):

    def __init__(self, socket):
        self.in_use = False
        self.socket = socket


broadcast_lock=False
def broadcast(message):
    global broadcast_lock
    if broadcast_lock:
        print "## broadcast is locked"
        return
    broadcast_lock = True
    for cl_sock in client_sockets:
        if cl_sock.in_use:
            continue
        broadcast_thread = Broadcast(cl_sock, message)
        broadcast_thread.start()
    broadcast_lock = False

class Broadcast(Thread):
    
    def __init__(self, socket, message):
        Thread.__init__(self)
        self.message = message
        self.socket = socket

    def run(self):
        print "runing broadcast"
        try:
            self.socket.in_use = True
            self.socket.socket.send(self.message)
            print "broadcasted " + self.message + " to client"
            self.socket.in_use = False
        except Exception as e:
            print "## exception while broadcasting to client sock : " + str(e)
            client_sockets.remove(self.socket)


class Client(Thread):

    def __init__(self, socket_wrapped):
        Thread.__init__(self)
        self.sock=socket_wrapped.socket
    
    def run(self):
        while True:
            try:
                print "## starting sock.recv"
                message = self.sock.recv(2048)
                print "## recv ended, message : " + message
                if message=="":
                    break
                broadcast(message)
            except Exception as e:
                print "Exception while listening on sock : " + str(e)
                break
            

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.bind(("",11111))

try:
    while True:
        tcpsock.listen(5)
        cl_sock, address = tcpsock.accept()
        print "{} connected".format( address )
        cl_sock_wrapped = ClientSock(cl_sock)
        client_sockets.append(cl_sock_wrapped)
        cl = Client(cl_sock_wrapped)
        cl.start()
except KeyboardInterrupt:
        sys.exit()

