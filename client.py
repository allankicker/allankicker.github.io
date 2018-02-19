#!/usr/bin/env python
import pika
import time
import sys
import uuid
from threading import Thread

client_uid = str(uuid.uuid4())
offset=len(client_uid)

class consumer(Thread):
    def run(self):
	credentials = pika.PlainCredentials('guest', 'guest')
	self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', '5672', '/', credentials))
	channel = self.connection.channel()
	channel.exchange_declare(exchange='logs',
		                 exchange_type='fanout')

	result = channel.queue_declare(exclusive=True)
	queue_name = result.method.queue
	channel.queue_bind(exchange='logs',
		           queue=queue_name)

	def callback(ch, method, properties, body):
	    if client_uid not in body:
	        print("%s" % body[offset:])

	channel.basic_consume(callback,
		              queue=queue_name,
		              no_ack=True)
	channel.start_consuming()

    def close(self):
	self.connection.close()

class sender(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')
    def send(self, message):
        self.channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)
    

con = consumer()
con.start()
message=""
sen = sender()
print "starting session, type /quit to end"
while True:
    message = raw_input()
    if message == "/quit":
        break
    sen.send(client_uid+message)

print "ending session ..."
con.close()

