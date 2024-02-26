#!/usr/bin/python

'''rabbitmq test listener'''
import asyncio
import json
import requests
import pika
import logging
import threading
import websockets

# Global set to keep track of connected WebSocket clients
connected_clients = set()

async def authenticate_client(websocket):
    # Wait for a message from the client and validate it
    token = await websocket.recv()
    if token == "somethingextrahere2024$$!!!!I6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ":  # Replace with your validation logic
        return True
    return False

# Function to register a new WebSocket client
async def register_client(websocket):
    connected_clients.add(websocket)

# Function to unregister a disconnected WebSocket client
async def unregister_client(websocket):
    connected_clients.remove(websocket)

# WebSocket server handler
async def websocket_server_handler(websocket, path):
    if not await authenticate_client(websocket):
        await websocket.close(code=1008, reason="Authentication failed")
        return
    await register_client(websocket)
    try:
        await websocket.wait_closed()
    finally:
        await unregister_client(websocket)

# Function to broadcast messages to all connected WebSocket clients
async def broadcast_message(message):
    if connected_clients:  # Check if there are any connected clients
        #await asyncio.wait([client.send(message) for client in connected_clients])
        await asyncio.gather(*(client.send(message) for client in connected_clients))

# Start the WebSocket server
def start_websocket_server():
    start_server = websockets.serve(websocket_server_handler, "0.0.0.0", 6789)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

def run_websocket_server():
    # Create a new event loop for the thread
    asyncio.set_event_loop(asyncio.new_event_loop())
    start_websocket_server()


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

def start_rabbitmq_consumer():
    consumer = RabbitMQConsumer()
    consumer.run()

def main():
    # Start the WebSocket server in a separate thread
    ws_thread = threading.Thread(target=run_websocket_server)
    ws_thread.start()

    # Start the RabbitMQ consumer
    start_rabbitmq_consumer()

    # Wait for the WebSocket thread to finish (if needed)
    ws_thread.join()

if __name__ == '__main__':
    main()