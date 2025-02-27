# Zig Zag Rental technical test

## Why
We need a way to verify you are capable of writing code on your own, and FlatBuffers + WebSockets seem like a good option. They might be useful if you end up joining us (FlatBuffers are overkill and probably a performance detriment in python, but they are also very cool), plus they are obscure enough LLMs do not do a great job without a little help.

We heavily encourage you to try this problem without LLM code generation, but we have obviously no way of checking, so there is that.

Flatbuffers offer a more efficient way to serialize data than sending JSON over the network, and provide a file that gives the specification for the interface, from which you can generate code for serialising and deserialising for a bunch of languages, using their compiler `flatc`. Find out more and how to get started on their website.
## What
On the `server` folder you can find a FastAPI WebSocket server that you can run locally. Once your client connects to the `/ws` endpoint it will start to spit data following the interface defined in `interface.fbs`.

You have to write a simple local server that serves the files needed for a client to connect to the FastAPI WebSocket server, and store to local variables the values it gets from the WS. It is the browser client the one that will be connecting to the WS, not the server, therefore the deserialisation will be written in JavaScript/TypeScript, since it must run on a browser.

Some of the fileds will only be sent on some messages, while others will be sent on all of them. You must make sure when a field is not sent it does not overwrite the current value. Remember you have to deserialise the incoming data using FlatBuffers generated code, you do not have to write the code on your own!

If you access the endpoint `ws/json` the server will send you two messages, first one binary containing the data in the FlatBuffers interface and a second one with the values your local variables should have. The JSON message always contains all the fields. You have to check if your local variables, which get the value from the FlatBuffers messages, actually match what the `json` message contains.

On the web interface simply put a button to start the websocket client and a result field, zero for failure of the aforementioned comparison and one if it succeeds.
## How
Fork this [repo](https://github.com/kamplom/zzr-technical-test), and place your code under the `client/` folder.

To get the WS server running, on the server folder execute root:
```
python -m venv .env
```
On linux (google it for windows, or use WSL):
```
  source .env/bin/activate
```
```
python -m ensurepip
```
```
pip install -r requirements.txt
```
All done, to run the server:
```
fastapi run
```

Server code should not be modified, and if you do so (annotations or whatever), please do not commit such changes. Make sure your code works with the original code.
## Random info
Check the `dirty_test.py` file under `server/` to get a rough idea of the logic our app should be following.

I expect this to take about 2 to 3 hours. It may seem intimidating at first but when you grasp the concept of data serialisation and why a non human-readable format is preferred it kinds of fall in place.

May be it is a good idea to start by taking a look at the `JSON` output (human readable!), so you get an intuition of what we are sending.

If you struggle starting up the FastAPI server, which is quite a bad sign, I may be able to spin up a remote instance for you, let me know.

Be aware of optional fields, they tend to make life complicated and cause depression, anxiety and global pandemics.