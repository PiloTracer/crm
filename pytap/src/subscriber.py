'''redis subscriber'''
import json
import redis
import requests
import asyncio

class RedisSubscriber:
    def __init__(self, redis_host, redis_port, channel):
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
        self.channel = channel
        self.setup_subscriber()

    def setup_subscriber(self):
        self.pubsub = self.redis_client.pubsub()
        self.pubsub.subscribe(self.channel)
        print(f"Subscribed to channel '{self.channel}'.")

    def handle_message(self, message_data):
        try:
            data = json.loads(message_data)
            print(f"Received: {data}")

            if data["type"] == "upload":
                if data["header"] == "newfile":
                    self.handle_newfile(data)
                elif data["header"] == "uploadresult":
                    self.handle_uploadresult()
                else:
                    print("Error: Unknown header type.")
            else:
                print("Error: Message type not understood.")
        except json.JSONDecodeError:
            print("Error: Failed to decode JSON message.")
        except KeyError as e:
            print(f"Error: Missing key in message - {e}")

    def handle_newfile(self, data):
        url = f"http://10.5.0.6:8000/pull/loadfile?filename={data['message']}"
        self.make_request(url)

    def handle_uploadresult(self):
        print("Received message: routed to websockets server")
        #broadcast_message(message)
        #asyncio.run(broadcast_message(message))

    def make_request(self, url):
        try:
            response = requests.get(url, timeout=5)
            print(f"Response: {response.status_code} from {url}")
        except requests.RequestException as e:
            print(f"Error making request: {e}")

    def listen(self):
        print("Listening for messages...")
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                self.handle_message(message['data'])


if __name__ == '__main__':
    subscriber = RedisSubscriber('10.5.0.4', 6379, 'newfile')
    subscriber.listen()
