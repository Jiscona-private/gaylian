import asyncio
import json
import websockets
import functools

rooms = {}

async def handler(websocket, room, username):
    room[str(username)].append(websocket)

    async for message in websocket:
        event = json.loads(message)
        print(event)
        for username in room:
            await room[username][0].send(json.dumps(event["msg"]))

async def join(token, username):
    rooms[str(token)][str(username)] = []

    async with websockets.serve(functools.partial(handler, room=rooms[str(token)], username=username), "", port=7127):
        await asyncio.Future()  # run forever

async def create(token, username):
    rooms[str(token)] = {}
    await join(token=token, username=username)