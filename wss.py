import websockets
import asyncio
import json
import base64


PORT = 8080

print("Server listening on Port " + str(PORT))

async def echo(websocket, path):
    print("A client just connected")
    try:
        async for message in websocket:
            hh=message
            # # print(hh)
            # data=hh.find('payload 
            # if data:
            #     try :
            #         find2=hh.find('=',138)
            #         coded_string=hh[139:find2+1]
            #         print(coded_string)
            #         print(base64.b64decode(coded_string))
            #     except :
            #         pass
            
            # else :
            #     print("Received message from client: " + json.dumps(message))
            print("Received message from client: " + json.dumps(message))
            
            await websocket.send(json.dumps("SGVsbG8gSGFyc2ggS3VtYXI="))
    except websockets.exceptions.ConnectionClosed as e:
        print("A client just disconnected")

start_server = websockets.serve(echo, "localhost", PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()