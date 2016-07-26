#!/usr/bin/env python3
import sys
sys.path.append("..")

import os
import puka3

AMQP_URL = os.environ.get('AMQP_URL', "amqp://localhost/")
client = puka3.Client(AMQP_URL)
promise = client.connect()
client.wait(promise)


promise = client.exchange_declare(exchange='headers_logs', type='headers')
client.wait(promise)

promise = client.queue_declare(exclusive=True)
queue_name = client.wait(promise)['queue']

argv = sys.argv[1:]
if not argv:
    print("Usage: %s [header:value]..." % (sys.argv[0],), file=sys.stderr)
    sys.exit(1)

headers = dict(arg.split(':', 2) for arg in argv)
headers['x-match'] = 'any'
promise = client.queue_bind(exchange='headers_logs', queue=queue_name,
                            routing_key='', arguments=headers)
client.wait(promise)

print(' [*] Waiting for logs %r. To exit press CTRL+C' % (headers,))

consume_promise = client.basic_consume(queue=queue_name, no_ack=True)
while True:
    msg_result = client.wait(consume_promise)
    print(" [x] %r:%r" % (msg_result['headers'], msg_result['body']))
