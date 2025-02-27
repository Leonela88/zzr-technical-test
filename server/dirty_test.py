import asyncio
import websockets
import json

import pytest

import flatbuffers
import TestInterface.State
import TestInterface.Status
import TestInterface.Vec3

class State:
    pointer = [0, 0, 0]
    offset = None
    hp = None
    message = None
    status = None
    distance = None

def check_is_the_same(a, b):
    if  a.offset == b.offset and a.hp == b.hp and a.message == b.message and a.status == b.status and a.distance == b.distance:
        return True
    else:
        return False
json_msg = State()
fb_msg = State()

async def connect_to_server():
    uri = "ws://localhost:8000/ws/json"  # Update with your server's correct URI
    async with websockets.connect(uri) as websocket:
        try:
            # Keep receiving messages for a specified duration or count
            message_count = 0
            good_messages = 0
            max_messages = 10000  # Adjust as needed
            print("Connected to server. Waiting for messages...")
            
            while message_count < max_messages:
                # Receive message without assuming type
                message = await websocket.recv()
                
                # Check message type
                if isinstance(message, str):
                    # Handle text message (likely JSON)
                    try:
                        #print(f"Received JSON data: {len(message)} bytes")
                        data = json.loads(message)
                        # Extract variables with the same names as server
                        json_msg.pointer = data.get("pointer")
                        json_msg.offset = data.get("offset")
                        json_msg.hp = data.get("hp")
                        json_msg.message = data.get("message")
                        json_msg.status = data.get("status")
                        json_msg.distance = data.get("distance")
                       
                    except json.JSONDecodeError:
                        print(f"Received text (non-JSON): {message}")
                
                elif isinstance(message, bytes):
                    # Handle binary message (likely flatbuffers)
                    #print(f"Received binary data, length: {len(message)} bytes")
                    data = TestInterface.State.State.GetRootAs(message, 0)
                    vector = data.Pointer()
                    fb_msg.pointer[0] = vector.X()
                    fb_msg.pointer[1] = vector.Y()
                    fb_msg.pointer[2] = vector.Z()

                    fb_msg.distance = data.Distance()
                    if data.Hp() is not None:
                        fb_msg.hp = data.Hp()
                    if data.Message() is not None:
                        fb_msg.message = data.Message().decode()
                    if data.Status() is not None:
                        fb_msg.status = data.Status()
                    if data.Offset() is not None:
                        fb_msg.offset = data.Offset()

                else:
                    print(f"Received unknown message type: {type(message)}")
                if check_is_the_same(json_msg, fb_msg) == False and message_count%2 == 1:
                    print("message number: ", message_count/2)
                    print(json_msg.pointer, fb_msg.pointer)
                    print(json_msg.offset, fb_msg.offset)
                    print(json_msg.hp, fb_msg.hp)
                    print(json_msg.message, fb_msg.message)
                    print(json_msg.status, fb_msg.status)
                    print(json_msg.distance, fb_msg.distance)
                else:
                    good_messages += 1
                #print(check_is_the_same(json_msg, fb_msg))
                message_count += 1
            print("total messages: ", message_count/2)
            print("good messages: ", good_messages/2)
                

                
        except websockets.exceptions.ConnectionClosedOK:
            print("Connection closed gracefully.")
        except websockets.exceptions.ConnectionClosedError as e:
            print(f"Connection closed with error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(connect_to_server())