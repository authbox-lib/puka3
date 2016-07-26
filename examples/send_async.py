#!/usr/bin/env python3

import sys
sys.path.append("..")

import os
import puka3

def on_connection(promise, result):
    client.queue_declare(queue='test', callback=on_queue_declare)

def on_queue_declare(promise, result):
    client.basic_publish(exchange='', routing_key='test',
                         body="Hello world!",
                         callback=on_basic_publish)

def on_basic_publish(promise, result):
    print(" [*] Message sent")
    client.loop_break()

AMQP_URL = os.environ.get('AMQP_URL', "amqp://localhost/")
client = puka3.Client(AMQP_URL)
client.connect(callback=on_connection)
client.loop()

promise = client.close()
client.wait(promise)
