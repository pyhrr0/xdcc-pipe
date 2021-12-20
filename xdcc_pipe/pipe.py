import json
import urllib.parse
import asyncio
import uvicorn
import uuid

from fastapi import FastAPI
from fastapi.websockets import WebSocket, WebSocketDisconnect
from websockets import connect as ws_connect
from websockets.exceptions import ConnectionClosedOK

from .bot import XDCCBot


class XDCCPipe():
    app = FastAPI()

    @app.websocket("/{client_id}")
    async def forward_pack(websocket: WebSocket, client_id: str) -> None:
        await websocket.accept()
        try:
            pack = await websocket.receive_json()

            bot = XDCCBot()
            await bot.forward(pack, websocket)

            await bot.terminate()
            await websocket.close()
        except WebSocketDisconnect:
            await bot.terminate()
            print(f"Client #{client_id} has disconnected.")

    @staticmethod
    async def request_pack(ws_url, filename, network, channels, bot, packnum):
        client_id = uuid.uuid4()

        async with ws_connect(f'{ws_url}/{client_id}') as websocket:
            try:
                await websocket.send(json.dumps(
                    {'network': network, 'channels': channels, 'bot': bot,
                     'packnum': packnum}))

                with open(filename, 'wb') as fp:
                    while True:
                        chunk = await websocket.recv()
                        fp.write(chunk)

                await websocket.close()
            except ConnectionClosedOK:
                pass
            # TODO handle KeyboardInterrupt


def run_server(**kwargs):
    url = urllib.parse.urlparse(kwargs['ws_url'])
    uvicorn.run(XDCCPipe.app, host=url.hostname, port=url.port)


def run_client(**kwargs):
    asyncio.run(
        XDCCPipe.request_pack(
            kwargs['ws_url'], kwargs['output_file'],
            kwargs['network'], kwargs['channel'],
            kwargs['bot'], kwargs['pack_num']))
