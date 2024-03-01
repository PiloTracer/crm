import json
import logging
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import asyncio
from sock.src.helper.encoder import hash_string_with_salt

from sock.src.utils.loadenv import get_env_value

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

@app.get("/")
async def get():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            #key = "SOCK_secret"
            #logging.info(f"Message: {data}")
            #objdata = json.loads(data)
            #token = objdata["token"]
            #logging.info(f"Message token: {token}")
            #objdata["token"] = ""
            #token2 = hash_string_with_salt(json.dumps(objdata))
            #logging.info(f"Token 2: {token2}")
            #data = json.dumps(objdata)
            #logging.info(f"Message New: {data}")
            #if token == token2:
            await broadcast_message(data)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        clients.remove(websocket)

async def broadcast_message(message: str):
    disconnected_clients = set()
    for client in clients:
        try:
            await client.send_text(message)
        except Exception:
            # The client is likely disconnected
            disconnected_clients.add(client)

    for client in disconnected_clients:
        clients.remove(client)

if __name__ == "__main__":
    import uvicorn
    #logging.basicConfig(filename='/crmdir/uploads/sock/log/sock.log', level=logging.INFO, 
    #                    format='%(asctime)s - %(levelname)s - %(message)s', 
    #                    datefmt='%Y-%m-%d %H:%M:%S')
    #logging.info(f"Initiating websockets session")
    uvicorn.run(app, host="0.0.0.0", port=4500)
