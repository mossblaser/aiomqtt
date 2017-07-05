import functools
import asyncio

from .version import __version__

import paho.mqtt.client as mqtt


AIO_MQTT_CLIENT_MISC_DELAY = 1.0


class AioMqttClient(object):
    """
    An AsyncIO based wrapper around the paho-mqtt MQTT client class.
    
    Essentially, the differences between this and the paho.mqtt.client.Client
    are:
    
    * The constructor takes an asyncio loop to use
    * Blocking methods (connect, connect_srv, reconnect_delay_set) are now
      coroutines.
    * The MQTT loop is automatically started.
    * Callback functions are inserted into the asyncio event loop rather than
      being run from an unspecified thread.
    """
    
    def __init__(self, loop, *args, **kwargs):
        self._loop = loop
        self._client = mqtt.Client(*args, **kwargs)
        
        self._copy_method("reinitialise")
        self._copy_method("ws_set_options")
        self._copy_method("tls_set_context")
        self._copy_method("tls_set")
        self._copy_method("tls_insecure_set")
        self._copy_method("enable_logger")
        self._copy_method("disable_logger")
        self._wrap_blocking_method("connect")
        self._wrap_blocking_method("connect_srv")
        self._copy_method("connect_async")
        self._copy_method("reconnect_delay_set")
        self._wrap_blocking_method("reconnect")
        self._copy_method("publish")
        self._copy_method("username_pw_set")
        self._copy_method("disconnect")
        self._copy_method("subscribe")
        self._copy_method("unsubscribe")
        self._copy_method("max_inflight_messages_set")
        self._copy_method("max_queued_messages_set")
        self._copy_method("message_retry_set")
        self._copy_method("user_data_set")
        self._copy_method("will_set")
        self._copy_method("will_clear")
        self._copy_method("message_callback_remove")
        
        self._wrap_callback("on_connect")
        self._wrap_callback("on_disconnect")
        self._wrap_callback("on_message")
        self._wrap_callback("on_publish")
        self._wrap_callback("on_subscribe")
        self._wrap_callback("on_unsubscribe")
        self._wrap_callback("on_log")
        
        self._client.loop_start()
    
    def _copy_method(self, name):
        """Copy a method from the client directly."""
        setattr(self, name, getattr(self._client, name))
    
    def _wrap_callback(self, name):
        """Add the named callback to the MQTT client which triggers a call to
        the wrapper's registered callback in the event loop thread.
        
        Also creates an asyncio.Event called _name_event where "name" is the
        name supplied to this function. This event is set whenever the callback
        is called.
        """
        event = asyncio.Event(loop=self._loop)
        
        setattr(self, name, None)
        setattr(self, "_{}_event".format(name), event)
        
        def wrapper(_client, *args):
            self._loop.call_soon_threadsafe(event.set)
            
            f = getattr(self, name)
            if f is not None:
                self._loop.call_soon_threadsafe(f, self, *args)
        
        setattr(self._client, name, wrapper)
    
    def _wrap_blocking_method(self, name):
        """Wrap a blocking function to make it async."""
        f = getattr(self._client, name)
        @functools.wraps(f)
        async def wrapper(*args, **kwargs):
            return await self._loop.run_in_executor(None, functools.partial(f, *args, **kwargs))
        setattr(self, name, wrapper)
    
    @functools.wraps(mqtt.Client.message_callback_add)
    def message_callback_add(self, sub, callback):
        @functools.wraps(callback)
        def wrapper(_client, *args, **kwargs):
            self._loop.call_soon_threadsafe(functools.partial(callback, self, *args, **kwargs))
        self._client.message_callback_add(sub, callback)
