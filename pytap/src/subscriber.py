'''redis subscriber'''
import json
import redis
import requests

class RedisSubscriber:
    def __init__(self, redis_host, redis_port, channel):
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
        self.pubsub = self.redis_client.pubsub()
        self.pubsub.subscribe(channel)

    def listen(self):
        print(f"Receiving...")
        for message in self.pubsub.listen():
            if message['type'] == 'message':
                data = json.loads(message['data'])
                print(f"Received: {data}")

                if data["type"] == "upload" and data["header"] == "newfile":
                    url = f"http://10.5.0.6:8000/pull/loadfile?filename={data["message"]}"
                elif data["type"] == "upload" and data["header"] == "uploadresult":
                    print(f"Received message: routed to websockets server")
                    #broadcast_message(message)
                    #asyncio.run(broadcast_message(message))
                else:
                    print(f"Received message: error... message not understood")

                if url != "":
                    response = requests.get(url, timeout=5)
                    print(f"Received message: {str(response.status_code)} {url}")


if __name__ == '__main__':
    subscriber = RedisSubscriber('10.5.0.4', 6379, 'newfile')
    subscriber.listen()
