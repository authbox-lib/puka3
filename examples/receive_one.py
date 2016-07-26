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

print("  [*] Waiting for a message. Press CTRL+C to quit.")

consume_promise = client.basic_consume(queue='test')
result = client.wait(consume_promise)
print(" [x] Received message %r" % (result,))

client.basic_ack(result)

promise = client.basic_cancel(consume_promise)
client.wait(promise)

promise = client.close()
client.wait(promise)
