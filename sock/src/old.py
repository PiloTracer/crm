#!/usr/bin/env python3

import asyncio
import json
import websockets
import logging
from datetime import datetime

class WebSocketServer:
    def __init__(self, host='0.0.0.0', port=6789, auth_token="somethingextrahereI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ"):
        self.connected_clients = set()
        self.host = host
        self.port = port
        self.auth_token = auth_token
        logging.info("WebSocketServer initialized")

    async def authenticate_client(self, websocket):
        try:
            msg = await asyncio.wait_for(websocket.recv(), timeout=10)
            obj = json.loads(msg)
            token = obj['wstoken']
            logging.info(f"Authentication attempt with token: {token}")
            return token == self.auth_token
        except (asyncio.TimeoutError, json.JSONDecodeError) as e:
            logging.error(f"Authentication error: {e}")
            return False

    async def register_client(self, websocket):
        self.connected_clients.add(websocket)
        logging.info(f"Client registered: {websocket.remote_address}")

    async def unregister_client(self, websocket):
        self.connected_clients.remove(websocket)
        logging.info(f"Client unregistered: {websocket.remote_address}")

    async def websocket_handler(self, websocket, path):
        logging.info("websocket_handler: entered")
        if not await self.authenticate_client(websocket):
            await websocket.close(code=1008, reason="Authentication failed")
            return
        await self.register_client(websocket)
        try:
            # Just keep the connection open and listen for messages
            async for message in websocket:
                logging.info(f"Received message: {message}")
                omsg = json.loads(message)
                if omsg["header"] == "uploadresult":
                    await self.broadcast_message(message)
                # Here you can add logic to process incoming messages
                # and potentially call broadcast_message
        except Exception as e:
            logging.error(f"Error in websocket connection: {e}")
        finally:
            await self.unregister_client(websocket)

    async def broadcast_message(self, message):
        logging.info("broadcast_message: entered")
        message['wstoken'] = ""
        json_message = json.dumps(message)
        for client in self.connected_clients:
            try:
                await client.send(json_message)
            except Exception as e:
                logging.error(f"Error sending message: {e}")
                continue
        logging.info("Broadcast message completed")

    def run(self):
        start_server = websockets.serve(
            self.websocket_handler, 
            self.host, 
            self.port,
            ping_interval=60,  # Send a ping every 60 seconds
            ping_timeout=30    # Wait 30 seconds for a pong before closing
        )
        asyncio.get_event_loop().run_until_complete(start_server)
        logging.info(f"WebSocket server started on ws://{self.host}:{self.port}")
        asyncio.get_event_loop().run_forever()

def main():
    now = datetime.now()
    date_string = now.strftime("%Y%m%d%H")
    logging.basicConfig(filename='/crmdir/uploads/sock/log/sock.log', level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s', 
                        datefmt='%Y-%m-%d %H:%M:%S')
    server = WebSocketServer()
    server.run()

if __name__ == '__main__':
    main()
