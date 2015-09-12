#!/usr/bin/env python
"""
A simple pubsub websocket server
"""
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
import os, sys, traceback as tb, bottle, json, ps

app = bottle.default_app()
app.pubsub = ps.PubSub()

def mk_send(sock):
    """
    returns a send function bound to the socket
    """
    return lambda sid,ch,msg:( sock.send( msg if type(msg)==type('')
                                          else json.dumps( msg ) ) )

@bottle.route('/')
def _(): return bottle.redirect('/static/index.html')

@bottle.route('/static/<path:path>')
def _(path='index.html'): return bottle.static_file(path,'html')

@bottle.route('/ws')
def handle_websocket():
    wsock = bottle.request.environ.get('wsgi.websocket')
    if not wsock:
        raise bottle.abort(400, 'Expected WebSocket request.')
    sid = str( id(wsock) )
    app.pubsub.add( sid, mk_send(wsock) )
    app.pubsub.snd( sid, [0,':HELLO:',{"sessionId":sid}] )
    try:
        while True:
            print sid, "BEFORE RECV"
            message = wsock.receive()
            print sid, "AFTER RECV", repr(message)
            if not message: break
            jmsg = json.loads( message )
            if   jmsg[0] == 0: app.pubsub.sub( sid, jmsg[2]['channels'] )
            elif jmsg[0] == 1: app.pubsub.pub( sid, jmsg[1], [2, sid, jmsg] )
            else:  raise RuntimeError('Bad Command')
    finally:
        app.pubsub.pop( sid )
        pass
    pass

if __name__=='__main__':
    ENV=os.environ.get
    WSGIServer((ENV('HOST','0'), int(ENV('PORT',8001))), app,
               handler_class=WebSocketHandler).serve_forever()
