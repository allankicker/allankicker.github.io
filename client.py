#!/usr/bin/env python
# coding: utf-8

import os
import sys
import socket
import time
from threading import Thread


def get_sock():
    hote = "localhost"
    port = 11112
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hote, port))
    #sock.settimeout(1)
    return sock

class Receiver(Thread):

    def __init__(self, sock):
        Thread.__init__(self)
        self.must_stop = False
        self.sock = sock

    def run(self):
        while True:
            if self.must_stop:
                break
            try:
                response = self.sock.recv(2048)
                if response == "":
                    break
                print response
            except socket.timeout, e:
                err = e.args[0]
                if err == 'timed out':
                    time.sleep(1)
                    
    def stop(self):
        self.must_stop = True

class Transmitter(Thread):
    
    def __init__(self, sock, nb_messages=10, client_name="default name"):
        Thread.__init__(self)
        self.must_stop = False
        self.socket = sock
        self.nb_msgs = nb_messages
        self.cl_name = client_name

    def run(self):
        for i in range(self.nb_msgs):
            if self.must_stop:
                break
            self.socket.send("client %s msg nb #%s" % (self.cl_name, i))
            time.sleep(0.5)

    def stop(self):
        self.must_stop=True

def usage():
    print " To launch 10 clients sending 100 messages (1 each 0.5s) : python client.py 10 100" 


if len(sys.argv)<2:
    usage()
    sys.exit()

try:
    nb_clients = int(sys.argv[-2])
    nb_msgs = int(sys.argv[-1])
except:
    usage()
    sys.exit()


trans_threads=[]
recv_threads=[]

for i in range(nb_clients):
    sock = get_sock()
    
    recv = Receiver(sock)
    recv.start()
    recv_threads.append(recv)
    trans = Transmitter(sock, nb_msgs, "client %s" %i)
    trans.start()
    trans_threads.append(trans)

for th in trans_threads:
    th.join()

for th in recv_threads:
    th.stop()





