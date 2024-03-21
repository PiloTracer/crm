import hashlib
import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio
import json as myjson

#from sock.src.utils.loadenv import get_env_value
#from sock.src.helper.encoder import hash_string_with_salt

# Configure logging
logging.basicConfig(filename='/crmdir/uploads/sock/log/sock.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S')

app = FastAPI()

clients = set()  # Set to store active WebSocket connections

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>WebSocket Test</title>
    </head>
    <body>
        <h1>WebSocket Client</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:4500/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

def serialize_to_json(data):
    return myjson.dumps(data, sort_keys=True, separators=(',', ':'))

def generate_hash_from_json(data):
    json_string = myjson.dumps(data, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(json_string.encode()).hexdigest()

def hash_string_with_salt(input_string: str) -> str:
    salt = get_env_value("SOCK_secret")
    # Combine the input string with the salt
    salted_input = input_string + salt

    # Create a SHA-1 hash of the salted input
    sha1_hash = hashlib.sha1(salted_input.encode())
    return sha1_hash.hexdigest()

def get_env_value(key: str) -> str:
    load_dotenv()  # Load .env file
    return os.getenv(key)

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    logging.info("WebSocket connection accepted")
    try:
        while True:
            data = await websocket.receive_text()
            logging.info(f"Received data: {data}")

            objdata = myjson.loads(data)
            token = objdata['token']
            objdata['token'] = ""
            logging.info(f"new data: {serialize_to_json(objdata)}")
            token2 = generate_hash_from_json(objdata)
            logging.info(f"Token 2: {token2}")
            
            if token2 == token:
                await broadcast_message(data)
    except Exception as e:
        logging.error(f"Error in websocket_endpoint: {e}")
    finally:
        clients.remove(websocket)
        logging.info("WebSocket connection closed")

async def broadcast_message(message: str):
    disconnected_clients = set()
    for client in clients:
        try:
            await client.send_text(message)
        except Exception as e:
            logging.error(f"Error sending message: {e}")
            disconnected_clients.add(client)

    for client in disconnected_clients:
        clients.remove(client)
        logging.info("Disconnected client removed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4500)


