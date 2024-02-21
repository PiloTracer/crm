#!/usr/bin/python

'''rabbitmq test listener'''
import json
import requests
import pika
import logging

class RabbitMQConsumer:

    def __init__(self):
        self.connection = None
        self.channel = None

    def on_connected(self, connection):
        self.connection = connection
        self.connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        self.channel = channel
        self.channel.queue_declare(queue='newfile', callback=self.on_queue_declared)

    def on_queue_declared(self, method_frame):
        self.channel.basic_consume('newfile', self.handle_delivery)
        print('Waiting for messages. To exit, press Ctrl+C')

    def handle_delivery(self, channel, method, header, body):
        print(f"Receiving...")
        '''handles the reception of RMQ messages'''
        m = body.decode("utf-8")
        print(f"Received message: {m}")
        logFile = 'rmq.log'
        logging.basicConfig( filename = logFile,filemode = 'w+',level = logging.DEBUG,format = '%(asctime)s - %(levelname)s: %(message)s',\
                            datefmt = '%m/%d/%Y %I:%M:%S %p' )
        logging.debug(m)
        message = json.loads(m)
        url = ""
        if message["type"] == "upload" and message["channel"] == "newfile":
            url = f"http://10.5.0.6:8000/pull/loadfile?filename={message["message"]}"
        if url != "":
            response = requests.get(url, timeout=5)
            print(f"Received message: {str(response.status_code)} {url}")
        else:
            print(f"Received message: error... message not understood")
        # end with the acknowledgement of reception
        self.channel.basic_ack(delivery_tag=method.delivery_tag)
            
    def run(self):
        credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
        parameters = pika.ConnectionParameters(
            '10.5.0.20', 5672, '/', credentials)
        self.connection = pika.SelectConnection(parameters, on_open_callback=self.on_connected)

        try:
            # Loop so we can communicate with RabbitMQ
            self.connection.ioloop.start()
        except KeyboardInterrupt:
            # Gracefully close the connection
            self.connection.close()
            # Loop until we're fully closed, will stop on its own
            self.connection.ioloop.start()

if __name__ == '__main__':
    consumer = RabbitMQConsumer()
    consumer.run()
