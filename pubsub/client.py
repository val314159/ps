#!/usr/bin/env python3
#from gevent import monkey;monkey.patch_all()
import os, sys, time, json, traceback as tb
from websocket import WebSocketApp

try:
    import thread
except ImportError:
    import _thread as thread

class PubSubClient(object):
    def __init__(_, host):
        _.ws = WebSocketApp("ws://"+host+"/v1/ps", (),
                            lambda ws: thread.start_new_thread(_._tramp, ()),
                            lambda ws, message: _.recvj(json.loads(message)))
    def _print_error(_): print(">> Websocket Error"); tb.print_exc()
    def _tramp(_):
        print(">> Websocket Opened")
        try: _.run()
        except: _._print_error()
        time.sleep(0.2)
        print(">> Websocket Closed")
        return _.ws.close()
    def sendj(_, x): _.ws.send(json.dumps(x))
    def subscribe(_, ch_names):   _.sendj([0,":SUBS:",ch_names])
    def publish(_, ch_name, obj): _.sendj([1,ch_name,obj])
    def run_forever(_): _.ws.run_forever()

    def recvj(_, obj):
        print("[OBJ:%s]"%obj)
    def run(_):
        _.subscribe(["xx","yz"])
        for i in range(3):
            time.sleep(1)
            _.sendj("Hello %d" % i)
            pass
        pass
    pass

def main(): PubSubClient(':'.join(sys.argv[1:3])).run_forever()

if __name__ == "__main__":  main()
