from fastapi import FastAPI, WebSocket
from enum import Enum
import random
import string

import flatbuffers
import TestInterface.State
import TestInterface.Status
import TestInterface.Vec3
import json
app = FastAPI()

class Status(Enum):
    ALERT = 0
    HOMING = 1
    IDLE = 2
    JOGGING = 3

vector = [0, 0, 0]
offset = None
hp = None
message = None
distance = None

def generate_distance():
    return distance
def random_str(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.get("/")
def read_root():
    return {"msg": "not this rotue"}


@app.websocket_route("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    i = 0
    # Construct a Builder with 1024 byte backing array.
    while i < 5000:
        builder = flatbuffers.Builder(1024)
        ## generate some random data and serialize it

        # need to serialize before starting the builder
        if i % 600 == 0:
            message = random_str()
            # serialization
            serialized_message = builder.CreateString(message)

        TestInterface.State.StateStart(builder)
        vector[0]=random.random()*100
        vector[1]=random.random()*100
        vector[2]=random.random()*100
        # serialization
        vector_buff = TestInterface.Vec3.CreateVec3(builder, vector[0], vector[1], vector[2])
        TestInterface.State.StateAddPointer(builder, vector_buff)

        # offset: each 250 cycles
        if i % 250 == 0:
            offset = random.randrange(0, 5000) 
            # serialization
            TestInterface.State.StateAddOffset(builder, offset)

        # hp: each 270 cycles
        if i % 270 == 0:
            hp = random.randrange(0, 3300) 
            # serialization
            TestInterface.State.StateAddHp(builder, hp)

        # message: each 600 cycles
        if i % 600 == 0:
            TestInterface.State.StateAddMessage(builder, serialized_message)

        # status: each 130 cycles
        if i % 130 == 0:
            status = random.randrange(0, 3)
            # serialization
            TestInterface.State.StateAddStatus(builder, status)
        
        # Distance: each cycle
        distance = random.randrange(0, 7777)
        TestInterface.State.StateAddDistance(builder, distance)
        serilaized_data = TestInterface.State.End(builder)
        builder.Finish(serilaized_data)

        ## send through websocket
        await websocket.send_bytes(builder.Output())
        i = i + 1
    await websocket.close()

@app.websocket_route("/ws/json")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    i = 0
    # Construct a Builder with 1024 byte backing array.
    while i < 5000:
        builder = flatbuffers.Builder(1024)
        ## generate some random data and serialize it
        # pointer each 300 cycles
        if i % 600 == 0:
            message = random_str()
            # serialization
            serialized_message = builder.CreateString(message)

        TestInterface.State.StateStart(builder)
        vector[0]=random.random()*100
        vector[1]=random.random()*100
        vector[2]=random.random()*100
        # serialization
        vector_buff = TestInterface.Vec3.CreateVec3(builder, vector[0], vector[1], vector[2])
        TestInterface.State.StateAddPointer(builder, vector_buff)

        # offset: each 250 cycles
        if i % 250 == 0:
            offset = random.randrange(0, 5000) 
            # serialization
            TestInterface.State.StateAddOffset(builder, offset)

        # hp: each 270 cycles
        if i % 270 == 0:
            hp = random.randrange(0, 3300) 
            # serialization
            TestInterface.State.StateAddHp(builder, hp)

        # message: each 600 cycles
        if i % 600 == 0:
            TestInterface.State.StateAddMessage(builder, serialized_message)

        # status: each 130 cycles
        if i % 130 == 0:
            status = random.randrange(0, 3)
            # serialization
            TestInterface.State.StateAddStatus(builder, status)
        
        # Distance: each cycle
        distance = random.randrange(0, 7777)
        TestInterface.State.StateAddDistance(builder, distance)
        serilaized_data = TestInterface.State.End(builder)
        builder.Finish(serilaized_data)

        ## send through websocket
        await websocket.send_bytes(builder.Output())

        ## send raw data as json, testing purpose
        json_data = { "pointer": (vector[0], vector[1], vector[2]), "offset": offset, "hp": hp, "message": message, "status": status, "distance": distance }
        await websocket.send_json(json_data)
        i = i + 1
    await websocket.close()