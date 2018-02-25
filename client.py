#!/usr/bin/env python
# coding: utf-8

import os
import sys
import socket
import time
from threading import Thread

hote = "localhost"
port = 11111
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((hote, port))
sock.settimeout(1)

class Receiver(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.must_stop = False

    def run(self):
        while True:
            if self.must_stop:
                break
            try:
                response = sock.recv(2048)
                print response
            except socket.timeout, e:
                err = e.args[0]
                if err == 'timed out':
                    time.sleep(1)
                    
    def stop(self):
        self.must_stop = True

recv = Receiver()
recv.start()
print "/quit to end session"
try:
    while True:
        text = raw_input()
        if text=="/quit":
            print "ending ..."
            recv.stop()
            sys.exit()
        sock.send(text)
except KeyboardInterrupt:
        recv.stop()
        sys.exit()
