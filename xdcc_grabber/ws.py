from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


@app.websocket("/ws/")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await websocket.accept()
    try:
        while True:
            await websocket.send_bytes(b'\x41\x42\x43\x44')
    except WebSocketDisconnect as e:
        print(f'client disconnected: {client_id}')
