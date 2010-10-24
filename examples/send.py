#!/usr/bin/env python

import os
import sys
sys.path.append(os.path.join("..", "puka"))


import puka


client = puka.Puka("amqp://localhost/")
ticket = client.connect()
client.wait(ticket)

ticket = client.queue_declare(queue='test')
client.wait(ticket)

ticket = client.basic_publish(exchange='', routing_key='test',
                              body="Hello world!")
client.wait(ticket)

print " [*] Message sent"
