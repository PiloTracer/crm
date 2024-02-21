#!/usr/bin/python

'''rabbitmq test listener'''
import pika
import requests

# Connection parameters
credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
connection_params = pika.ConnectionParameters(
    '10.5.0.20', 5672, '/', credentials)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# Declare a queue
channel.queue_declare(queue='newfile')


def callback(ch, method, properties, body):
    '''method docstring'''
    url = f"http://10.5.0.6:8000/pull/loadfile?filename={body.decode("utf-8")}"
    response = requests.get(url, timeout=5)

    print(f"Received message: {str(response.status_code)} {url}")


# Set up the consumer
channel.basic_consume(queue='newfile',
                      on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit, press Ctrl+C')
channel.start_consuming()
