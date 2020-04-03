import asyncio
import ssl
import pathlib
import websockets


users = set()


async def userHandler(websocket: websockets.WebSocketClientProtocol, _):  # _ is path.
    print(websocket.remote_address, "has connected.")
    address = websocket.remote_address
    while True:
        try:
            await websocket.send("Test!")
            await asyncio.sleep(1)
        except websockets.exceptions.ConnectionClosedOK:
            print(address, "has disconnected.")
            break


sslContext = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
cert = pathlib.Path(__file__).with_name("cert.pem")
key = pathlib.Path(__file__).with_name("key.pem")
sslContext.load_cert_chain(cert, key)

server = websockets.serve(userHandler, "localhost", 31666, ssl=sslContext)

asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
