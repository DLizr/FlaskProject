import asyncio
import websockets


users = set()


async def userHandler(websocket: websockets.WebSocketClientProtocol, _):  # _ is path.
    print(websocket.remote_address, "has connected.")
    while True:
        try:
            await websocket.send("Test!")
        except websockets.exceptions.ConnectionClosedOK:
            print(websocket.remote_address, "has disconnected.")
            break
        await asyncio.sleep(1)


server = websockets.serve(userHandler, "localhost", 31666)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
