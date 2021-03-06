#!/usr/bin/env python3
from gevent import monkey;monkey.patch_all()
from gevent.pywsgi import WSGIServer as WSGI
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler as WSH
from bottle import request, Bottle, abort, static_file
import json, traceback as tb

class PubSubConn(object):
    Connections = []
    def __init__(_):
        _.ws = request.environ.get('wsgi.websocket')
        if not _.ws:  abort(400, 'Expected WebSocket request.')
        _.subs = []
        _.Connections.append( _.ws )
        print(">> NewWS: " + repr(_.ws))
        print(">> Cxns: " + repr(_.Connections))
        pass
    def send(_, x): _.ws.send(json.dumps(x))
    def subscribe(_, channel_names): _.subs.extend( channel_names )
    def message(_, message):
        print(">> Msg: " + repr(type(message)) +  repr(message))
        _.send(["Your message was: %r" % message])
        pass
    def loop(_):
        try:
            _.send([0,":HELLO:",{}])
            msg = _.ws.receive()
            while msg:
                _.message( msg )
                msg = _.ws.receive()
                pass
            print(">> and another one left....")
        except WebSocketError:
            _.Connections.remove( _.ws )
            print(">> and another one down....")
            return tb.print_exc()
        pass
    pass

app = Bottle()

@app.route('/static/')
@app.route('/static/<path>')
def handle_static(path='index.html'): return static_file(path, root='static')

@app.route('/v1/ps')
def handle_pubsub(): return PubSubConn().loop()

def main(): WSGI(("0.0.0.0", 8280), app, handler_class=WSH).serve_forever()

if __name__=='__main__': main()
