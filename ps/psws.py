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
    app.pubsub.snd( sid, sid, [0,'HELLO',sid] )
    try:
        while True:
            message = wsock.receive()
            if not message: break
            jmsg = json.loads( message )
            cmd  = jmsg[1]
            if   cmd=='PUB' :  app.pubsub.pub ( sid, jmsg[2], message )
            elif cmd=='PUB+':  app.pubsub.pub ( sid, jmsg[2], message, 0 )
            elif cmd=='SUB' :  app.pubsub.sub ( sid, jmsg[2] )
            else:              raise RuntimeError('Bad Command')
    finally:
        app.pubsub.pop( sid )
        pass
    pass

if __name__=='__main__':
    ENV=os.environ.get
    WSGIServer((ENV('HOST','0'), int(ENV('PORT',8001))), app,
               handler_class=WebSocketHandler).serve_forever()
