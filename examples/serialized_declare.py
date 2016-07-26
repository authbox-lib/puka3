#!/usr/bin/env python3

import sys
sys.path.append("..")

import logging
FORMAT_CONS = '%(asctime)s %(name)-12s %(levelname)8s\t%(message)s'
logging.basicConfig(level=logging.DEBUG, format=FORMAT_CONS)



import os
import puka3

AMQP_URL = os.environ.get('AMQP_URL', "amqp://localhost/")
client = puka3.Client(AMQP_URL)

promise = client.connect()
client.wait(promise)

for i in range(1000):
    promise = client.queue_declare(queue='a%04i' % i)
    client.wait(promise)

for i in range(1000):
    promise = client.queue_delete(queue='a%04i' % i)
    client.wait(promise)

promise = client.close()
client.wait(promise)
