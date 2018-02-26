#!/usr/bin/env python
# coding: utf-8 

import socket
import sys
import time
from threading import Thread, Timer
from contextlib import contextmanager


client_sockets=[]

# --- server stats
max_threads = 0
current_threads = 0
@contextmanager
def log_thread_stats():
    global current_threads
    global max_threads
    current_threads+=1
    max_threads = max(max_threads, current_threads)
    yield
    current_threads-=1

def print_thread_stats():
    print "--- thread stats"
    print "%s active threads" % current_threads
    print "%s max threads" % max_threads
    print "%s sockets opened" % len(client_sockets)
    print "----------------"

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
        with log_thread_stats():
            try:
                self.socket.in_use = True
                self.socket.socket.send(self.message)
                self.socket.in_use = False
            except Exception as e:
                print "## exception while broadcasting to client sock : " + str(e)
                client_sockets.remove(self.socket)


class Client(Thread):

    def __init__(self, socket_wrapped):
        Thread.__init__(self)
        self.sock=socket_wrapped.socket
    
    def run(self):
        with log_thread_stats():
            while True:
                try:
                    message = self.sock.recv(2048)
                    if message=="":
                        break
                    broadcast(message)
                except Exception as e:
                    print "Exception while listening on sock : " + str(e)
                    break
            

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.bind(("",11112))

try:
    while True:
        tcpsock.listen(5)
        cl_sock, address = tcpsock.accept()
        print "{} connected".format( address )
        cl_sock_wrapped = ClientSock(cl_sock)
        client_sockets.append(cl_sock_wrapped)
        cl = Client(cl_sock_wrapped)
        cl.start()
        print_thread_stats()

except KeyboardInterrupt:
        print "exiting ..." 
        sys.exit()

