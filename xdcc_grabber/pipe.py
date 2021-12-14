import asyncio
import signal
from fastapi import FastAPI
from fastapi.websockets import WebSocket, WebSocketDisconnect
from websockets import connect as ws_connect

from bot import XDCCBot


class XDCCPipe():
    app = FastAPI()

    @app.websocket("/")
    async def websocket_endpoint(websocket: WebSocket, client_id: int) -> None:
        await websocket.accept()
        try:
            pack = await websocket.receive_json()
            await XDCCBot().forward(pack, websocket)
            await websocket.close()
        except WebSocketDisconnect:
            print(f"Client #{client_id} has disconnected.")

    @staticmethod
    async def receive_pack(ws_url, filename, network, channel, bot, packnum):
        async with ws_connect(ws_url) as websocket:
            loop = asyncio.get_running_loop()
            loop.add_signal_handler(
                signal.SIGTERM, loop.create_task, websocket.close())

            await websocket.send_json(
                {'network': network, 'channel': channel, 'bot': bot,
                 'packnum': packnum})

            with open(filename, 'a+') as fp:
                for chunk in websocket.recv():
                    fp.write(chunk)

            await websocket.close()
