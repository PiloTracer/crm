'''redis subscriber'''
import json
import redis
import requests
import asyncio
import websockets
import logging
from datetime import datetime

class RedisSubscriber:
    def __init__(self, redis_host, redis_port, channel, websocket_url):
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
        self.channel = channel
        self.websocket_url = websocket_url
        self.websocket = None
        self.setup_subscriber()
        logging.info("Pytap initialized")

    async def connect_websocket(self):
        logging.info(f"connect_websocket: entered")
        self.websocket = await websockets.connect(self.websocket_url)
        logging.info("connect_websocket; complete")

    async def close_websocket(self):
        logging.info(f"close_websocket: entered")
        if self.websocket:
            await self.websocket.close()
            logging.info("close_websocket: closed")
        else:
            logging.info("close_websocket: else")

    async def broadcast_message(self, data):
        logging.info(f"broadcast_message: entered")
        try:
            if not self.websocket or self.websocket.closed:
                logging.info(f"broadcast_message: reconnecting")
                await self.connect_websocket()
            message = json.dumps(data)
            await self.websocket.send(message)
            logging.info(f"broadcast_message: {message}")
        except Exception as e:
            logging.info(f"broadcast_message error: {e}")
        finally:
            await self.close_websocket()

    def setup_subscriber(self):
        self.pubsub = self.redis_client.pubsub()
        self.pubsub.subscribe(self.channel)
        logging.info(f"Subscribed to channel '{self.channel}'.")

    async def handle_message(self, message_data):
        try:
            data = json.loads(message_data)
            logging.info(f"Received: {data}")

            if data["type"] == "upload":
                if data["header"] == "newfile":
                    self.handle_newfile(data)
                elif data["header"] == "uploadresult":
                    await self.handle_uploadresult(data)
                else:
                    logging.info("Error: Unknown header type.")
            else:
                logging.info("Error: Message type not understood.")
        except json.JSONDecodeError:
            logging.info("Error: Failed to decode JSON message.")
        except KeyError as e:
            logging.info(f"Error: Missing key in message - {e}")

    def handle_newfile(self, data):
        url = f"http://10.5.0.6:8000/pull/loadfile?filename={data['message']}"
        self.make_request(url)

    async def handle_uploadresult(self, data):
        logging.info("Received message: routed to websockets server")
        await self.broadcast_message(data)

    def make_request(self, url):
        try:
            response = requests.get(url, timeout=5)
            logging.info(f"Response: {response.status_code} from {url}")
        except requests.RequestException as e:
            logging.info(f"Error making request: {e}")

    async def listen_async(self):
        logging.info("Listening for messages...")
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                await self.handle_message(message['data'])  # Assuming handle_message is also async
        await self.close_websocket()

    def listen(self):
        asyncio.run(self.listen_async())
              

if __name__ == '__main__':
    now = datetime.now()
    date_string = now.strftime("%Y%m%d%H")
    logging.basicConfig(filename=f'/crmdir/uploads/pytap/log/pytap.log', level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s', 
                        datefmt='%Y-%m-%d %H:%M:%S')
    subscriber = RedisSubscriber(
        '10.5.0.4', 
        6379, 
        'newfile', 
        'ws://10.5.0.7:4500/ws')
    asyncio.run(subscriber.listen_async())
