Deprecated
==========

**This library has been deprecated and the 'aiomqtt' name handed over to the
project formally known as
[`asyncio-mqtt`](https://github.com/sbtinstruments/aiomqtt).**

This legacy aiomqtt library will continue to exist via PyPI with versions <
1.0.0 with only essential maintaince on a "best effort" basis and no further
development.

New projects are encouraged to try the [new
qiomqtt](https://github.com/sbtinstruments/aiomqtt) project instead which
features a much more idiomatic Python API.


`aiomqtt` (v0.x): An asyncio Wrapper for paho-mqtt
==================================================

This library implements a minimal Python 3
[asyncio](https://docs.python.org/3/library/asyncio.html) wrapper around the
MQTT client in [paho-mqtt](https://github.com/eclipse/paho.mqtt.python).

Installation:

    pip install aiomqtt

You might prefer [`asyncio-mqtt`](https://github.com/sbtinstruments/asyncio-mqtt)
---------------------------------------------------------------------------------

Whilst you're welcome to use this library, you're probably better off using
[`asyncio-mqtt`](https://github.com/sbtinstruments/asyncio-mqtt) intead.
`asyncio-mqtt` is a a really slick and idiomatic asyncio MQTT library (also
built on paho-mqtt). As well as being much easier to use, it is also much more
actively maintained.

By contrast this library is just 61
[SLOC](https://en.wikipedia.org/wiki/Source_lines_of_code) of Python and is
intended to be as thin a wrapper around paho-mqtt as possible. It is also
maintained on a very limited basis.


API
---

This library is as thin as possible, exposing the exact same API as the
original paho-mqtt `Client` object with blocking calls replaced with coroutines
and all callbacks being scheduled into the asyncio main event loop. It does not
attempt to introduce a more idiomatic asyncio API.

When using aiomqtt, refer to the [paho-mqtt
documentation](https://pypi.python.org/pypi/paho-mqtt/1.1) which applies
verbatim with the exception of the above rules. An example use of the library
is shown below:

```python
import asyncio
import aiomqtt

loop = asyncio.get_event_loop()

async def demo():
    c = aiomqtt.Client(loop)
    c.loop_start()  # See "About that loop..." below.

    connected = asyncio.Event()
    def on_connect(client, userdata, flags, rc):
        connected.set()
    c.on_connect = on_connect

    await c.connect("localhost")
    await connected.wait()
    print("Connected!")

    subscribed = asyncio.Event()
    def on_subscribe(client, userdata, mid, granted_qos):
        subscribed.set()
    c.on_subscribe = on_subscribe

    c.subscribe("my/test/path")
    await subscribed.wait()
    print("Subscribed to my/test/path")

    def on_message(client, userdata, message):
        print("Got message:", message.topic, message.payload)
    c.on_message = on_message

    message_info = c.publish("my/test/path", "Hello, world")
    await message_info.wait_for_publish()
    print("Message published!")

    await asyncio.sleep(1)
    print("Disconnecting...")

    disconnected = asyncio.Event()
    def on_disconnect(client, userdata, rc):
        disconnected.set()
    c.on_disconnect = on_disconnect

    c.disconnect()
    await disconnected.wait()
    print("Disconnected")

    await c.loop_stop()
    print("MQTT loop stopped!")

loop.run_until_complete(demo())
```

About that loop...
------------------

Unfortunately the author was unable to work out how to integrate paho-mqtt's
event loop into asyncio, despite the best efforts of the paho-mqtt authors to
make this possible. (Patches are welcome.)

Instead, `loop_start()` and `loop_stop()` may be used as normal (and aiomqtt
will ensure callbacks arrive in the correct thread) or `loop_forever()` may be
used which in aiomqtt is a coroutine.
