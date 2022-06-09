import aiohttp
from collections import deque, defaultdict
from functools import partial
from os import getenv
if getenv("IS_DOCKERIZED"):

    WS_CONN = "ws://wsserver/sample"
else:
    WS_CONN = "ws://localhost:8501/sample"


from fastapi import FastAPI, WebSocket
from random import choice, randint
import asyncio


app = FastAPI()

CHANNELS = ["A", "B", "C"]

@app.websocket("/sample")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        await websocket.send_json({
            "channel": choice(CHANNELS),
            "data": randint(1, 10)
            }
        )
        await asyncio.sleep(0.5)

async def consumer(graphs, selected_channels, window_size, status):
    windows = defaultdict(partial(deque, [0]*window_size, maxlen=window_size))

    async with aiohttp.ClientSession(trust_env = True) as session:
        status.subheader(f"Connecting to {WS_CONN}")
        async with session.ws_connect(WS_CONN) as websocket:
            status.subheader(f"Connected to: {WS_CONN}")
            async for message in websocket:
                data = message.json()

                windows[data["channel"]].append(data["data"])

                for channel, graph in graphs.items():
                    channel_data = {channel: windows[channel]}
                    if channel == "A":
                        graph.line_chart(channel_data)
                    elif channel == "B":
                        graph.area_chart(channel_data)
                    elif channel == "C":
                        graph.bar_chart(channel_data)
