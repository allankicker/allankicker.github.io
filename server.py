#!/usr/bin/env python
# coding: utf-8 

import socket
import sys
from threading import Thread


client_sockets={}

def broadcast(message):
    broadcast_thread = Broadcast(message)
    broadcast_thread.start()
    broadcast_thread.join()
    
class Broadcast(Thread):
    
    def __init__(self, message):
        Thread.__init__(self)
        self.message = message

    def run(self):
        client_to_pop=[]
        print "runing broadcast"
        for key, sock in client_sockets.iteritems():
            try:
                sock.send(self.message)
                print "broadcasted " + self.message + " to " + str(key)
            except Exception as e:
                print "exception while broadcasting" + str(e)
                client_to_pop.append(key)
        for key in client_to_pop:
            print "pop client " + str(key)
            client_sockets.pop(key)

class Client(Thread):

    def __init__(self, socket):
        Thread.__init__(self)
        self.sock=socket
        
    def run(self):
        while True:
            try:
                time.sleep(1)
                message = self.sock.recv(2048)
                broadcast(message)
            except Exception as e:
                print "Exception while listening on sock : " + str(e)
                break
            

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.bind(("",11110))

try:
    while True:
        tcpsock.listen(5)
        cl_sock, address = tcpsock.accept()
        print "{} connected".format( address )
        client_sockets[address]=cl_sock
        cl = Client(cl_sock)
        cl.start()
except KeyboardInterrupt:
        sys.exit()

