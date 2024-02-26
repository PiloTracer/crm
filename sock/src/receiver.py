#!/usr/bin/python

'''rabbitmq test listener'''
import asyncio
import json
import signal
import time
import requests
import pika
import logging

class RabbitMQConsumer:

    def __init__(self):
        self.connection = None
        self.channel = None
        self.reconnect_delay = 5
        self.is_stopped = False

    def on_connected(self, connection):
        self.connection = connection
        self.connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        self.channel = channel
        self.channel.queue_declare(queue='newfile', callback=self.on_queue_declared)

    def on_queue_declared(self, method_frame):
        self.channel.basic_consume('newfile', self.handle_delivery)
        print('Waiting for messages. To exit, press Ctrl+C')

    def on_connection_closed(self, connection, reply_code, reply_text):
        print(f"Connection closed: ({reply_code}) {reply_text}")
        if not connection.is_closing and not connection.is_closed and not self.is_stopped:
            self.reconnect()


    def handle_delivery(self, channel, method, header, body):
        print(f"Receiving...")
        m = body.decode("utf-8")
        logging.info(m)
        message = json.loads(m)
        url = ""

        if message["type"] == "upload" and message["header"] == "newfile":
            url = f"http://10.5.0.6:8000/pull/loadfile?filename={message["message"]}"
        elif message["type"] == "upload" and message["header"] == "uploadresult":
            print(f"Received message: routed to websockets server")
            #broadcast_message(message)
            #asyncio.run(broadcast_message(message))
        else:
            print(f"Received message: error... message not understood")

        try:
            if url != "":
                response = requests.get(url, timeout=5)
                print(f"Received message: {str(response.status_code)} {url}")
            self.channel.basic_ack(delivery_tag=method.delivery_tag)
        except Exception as e:
            logging.error(f"Error processing message: {e}")
            # Consider requeuing the message
            self.channel.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

    def reconnect(self):
        if not self.is_stopped:
            print("Attempting to reconnect...")
            time.sleep(self.reconnect_delay)
            self.run()

    def run(self):
        credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
        parameters = pika.ConnectionParameters(
            '10.5.0.20', 5672, '/', credentials, heartbeat=60, blocked_connection_timeout=30
        )
        self.connection = pika.SelectConnection(
            parameters, on_open_callback=self.on_connected,
            on_close_callback=self.on_connection_closed
        )

        try:
            self.connection.ioloop.start()
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        self.is_stopped = True
        if self.connection:
            self.connection.close()

def signal_handler(signal, frame):
    global consumer
    consumer.stop()

def start_rabbitmq_consumer():
    global consumer
    consumer = RabbitMQConsumer()
    consumer.run()

def main():
    logging.basicConfig(filename='rmq.log', filemode='w+', level=logging.DEBUG, 
                        format='%(asctime)s - %(levelname)s: %(message)s', 
                        datefmt='%m/%d/%Y %I:%M:%S %p')
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    start_rabbitmq_consumer()

if __name__ == '__main__':
    main()