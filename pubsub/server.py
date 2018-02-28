#!/usr/bin/env python3
from gevent import monkey;monkey.patch_all()
from gevent.pywsgi import WSGIServer as WSGI
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler as WSH
from bottle import request, Bottle, abort, static_file
import os, sys, time, json, traceback as tb

class PubSubConn(object):
    Connections = []
    def __init__(_):
        _.ws = request.environ.get('wsgi.websocket')
        if not _.ws:  abort(400, 'Expected WebSocket request.')
        _.subs = []
        _.Connections.append( _ )
        print(">> NewWS: " + repr(_.ws))
        print(">> Cxns: " + repr(_.Connections))
        pass
    def sendj(_, x): _.ws.send(json.dumps(x))
    def subscribe(_, channel_names): _.subs.extend( channel_names )
    def sendfd(_, fd, obj):
        fd = int(fd)
        pkt = [2, _.fd, obj]
        for conn in _.Connections:
            if fd == conn.fd:
                conn.sendj( pkt )
                break
            pass
        pass
    def publish(_, channel_name, obj):
        pkt0 = [-11, _.fd, obj[:3]]
        pkt1 = [-1,  _.fd, obj]
        for conn in _.Connections:
            conn.sendj( pkt0 if _.fd == conn.fd else pkt1 )
            pass
        pass
    @property
    def fd(_): return _.ws.handler.socket.fileno()
    def recvj(_, obj):
        print("[OBJ:%s]"%obj)
        if   obj[0] == 0:
            print("ZERO (sub)", obj[2])
            _.subscribe(obj[2])
        elif obj[0] == 1:
            print("ONE1 (pub)", obj[1:])
            try:
                _.publish(obj[1], obj)
            except:
                print("ERR")
        elif obj[0] == 2:
            print("TWO (req)")
            _.sendfd(obj[1], obj)
        elif obj[0] == 3:
            print("THREE (rep)")
            _.sendfd(obj[1], obj)
        else:
            assert False
    def run_forever(_):
        try:
            _.sendj([-1,":HELLO:",dict(sessionId=_.fd)])
            msg = _.ws.receive()
            while msg:
                _.recvj( json.loads ( msg ) )
                msg = _.ws.receive()
                pass
            print(">> and another one left....")
        except WebSocketError:
            print(">> and another one down....")
            return tb.print_exc()
        finally:
            _.Connections.remove( _ )
            pass
        pass
    pass

app = Bottle()

@app.route('/static/')
@app.route('/static/<path>')
def handle_static(path='index.html'): return static_file(path, root='static')

@app.route('/v1/ps')
def handle_pubsub(): return PubSubConn().run_forever()

def main(): WSGI(("0.0.0.0",int(sys.argv[1])),
                 app, handler_class=WSH).serve_forever()

if __name__=='__main__': main()
