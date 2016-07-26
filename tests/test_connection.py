

import os
import puka3
import puka3.connection
import socket

import base

class TestConnection(base.TestCase):
    def test_broken_url(self):
        # Any address that doesn't resolve
        client = puka3.Client('amqp://256.256.256.256/')
        with self.assertRaises(socket.gaierror):
            promise = client.connect()

    def test_connection_refused(self):
        client = puka3.Client('amqp://127.0.0.1:9999/')
        with self.assertRaises(socket.error):
            # Can raise in connect or on wait
            promise = client.connect()
            client.wait(promise)

    # The following tests take 3 seconds each, due to Rabbit.
    def test_wrong_user(self):
        (username, password, vhost, host, port, ssl) = \
            puka3.connection.parse_amqp_url(self.amqp_url)

        client = puka3.Client('amqp://%s:%s@%s:%s%s' % \
                                 (username, 'wrongpass', host, port, vhost))
        promise = client.connect()
        with self.assertRaises(socket.error):
            client.wait(promise)

    # def test_wrong_vhost(self):
    #     client = puka3.Client('amqp:///xxxx')
    #     promise = client.connect()
    #     with self.assertRaises(puka3.ConnectionBroken):
    #         client.wait(promise)


if __name__ == '__main__':
    import tests
    tests.run_unittests(globals())

