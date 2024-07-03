import asyncio
import websockets
import json

connected_users = set()

async def handler(websocket, path):
    # register user
    connected_users.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            # broadcast msg to all connected user
            if data['type'] == 'location_update':
                for user in connected_users:
                    if user != websocket:
                        await user.send(json.dumps(data))
    finally:
        connected_users.remove(websocket)

start_server = websockets.serve(handler, "localhost", 6789)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
