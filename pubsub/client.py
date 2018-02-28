#!/usr/bin/env python3
#from gevent import monkey;monkey.patch_all()
import websocket, traceback as tb, json
from websocket import WebSocketApp

try:
    import thread
except ImportError:
    import _thread as thread
import time

class PS(object):
    def __init__(_, host): _.ws = WebSocketApp("ws://"+host+"/v1/ps", (),
                                               _.open, _.mesg)
    def _print_error(_): print(">> Websocket Error"); tb.print_exc()
    def send(_, x): _.ws.send(json.dumps(x))
    def mesg(_, ws, message): print("GOT MESSAGE: %s" % repr(message))
    def open(_, ws):
        def trampoline():
            print(">> Websocket Opened")
            try: _.run()
            except: _._print_error()
            time.sleep(0.2)
            print(">> Websocket Closed")
            return ws.close()
        return thread.start_new_thread(trampoline, ())
    def sub (_, ch_names):      _.send([0,":SUBS:",ch_names])
    def pub (_, ch_name, obj):  _.send([1,ch_name,obj])
    def run(_):
        _.sub(["xx","yz"])
        for i in range(3):
            time.sleep(1)
            _.ws.send("Hello %d" % i)
            pass
        pass
    pass

def main(): PS("localhost:8280").ws.run_forever()

if __name__ == "__main__":  main()
