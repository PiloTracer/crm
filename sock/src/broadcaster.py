#!/usr/bin/env python3

import asyncio
import websockets
import logging

class WebSocketServer:
    def __init__(self, host='0.0.0.0', port=6789, auth_token="somethingextrahere2024$$!!!!I6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ"):
        self.connected_clients = set()
        self.host = host
        self.port = port
        self.auth_token = auth_token

    async def authenticate_client(self, websocket):
        try:
            token = await asyncio.wait_for(websocket.recv(), timeout=10)
            return token == self.auth_token
        except asyncio.TimeoutError:
            return False

    async def register_client(self, websocket):
        self.connected_clients.add(websocket)

    async def unregister_client(self, websocket):
        self.connected_clients.remove(websocket)

    async def websocket_handler(self, websocket, path):
        if not await self.authenticate_client(websocket):
            await websocket.close(code=1008, reason="Authentication failed")
            return
        await self.register_client(websocket)
        try:
            await websocket.wait_closed()
        finally:
            await self.unregister_client(websocket)

    async def broadcast_message(self, message):
        if self.connected_clients:
            await asyncio.gather(*(client.send(message) for client in self.connected_clients))

    def run(self):
        start_server = websockets.serve(self.websocket_handler, self.host, self.port)
        asyncio.get_event_loop().run_until_complete(start_server)
        logging.info(f"WebSocket server started on ws://{self.host}:{self.port}")
        asyncio.get_event_loop().run_forever()


def main():
    logging.basicConfig(level=logging.INFO)

    server = WebSocketServer()
    server.run()

if __name__ == '__main__':
    main()
