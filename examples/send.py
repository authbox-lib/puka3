#!/usr/bin/env python3

import sys
sys.path.append("..")

import os
import puka3

AMQP_URL = os.environ.get('AMQP_URL', "amqp://localhost/")
client = puka3.Client(AMQP_URL)

promise = client.connect()
client.wait(promise)

promise = client.queue_declare(queue='test')
client.wait(promise)

promise = client.basic_publish(exchange='', routing_key='test',
                              body="Hello world!")
client.wait(promise)

print(" [*] Message sent")

promise = client.queue_declare(queue='test', passive=True)
print(" [*] Queue size:", client.wait(promise)['message_count'])

promise = client.close()
client.wait(promise)

