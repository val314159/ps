"""
A simple pubsub websocket server

because the needs of the many outweigh the needs of the few

"""
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler
import os, sys, traceback as tb, bottle, json, ps

app = bottle.default_app()
app.pubsub = ps.PubSub()

def mk_send(sock):
    """
    whee
    """
    return lambda msg:( sock.send( msg if type(msg)==type('')
                                   else json.dumps( msg ) ) )

@bottle.route('/')
@bottle.route('/static/<path:path>')
def _(path='index.html'): return bottle.static_file(path)

@bottle.route('/ws')
def handle_websocket():
    wsock = bottle.request.environ.get('wsgi.websocket')
    if not wsock:
        raise bottle.abort(400, 'Expected WebSocket request.')
    sid = str( id(wsock) )
    app.pubsub.add( sid, mk_send(wsock) )
    try:
        while True:
            message = wsock.receive()
            jmsg = json.loads( message )
            cmd = jmsg[1]
            if   cmd=='PUB' :  app.pubsub.pub ( sid, jmsg[2], message )
            elif cmd=='PUB+':  app.pubsub.pubp( sid, jmsg[2], message, 0 )
            elif cmd=='SUB' :  app.pubsub.sub ( sid, jmsg[2] )
            else:              raise RuntimeError('Bad Command')
    finally:
        app.pubsub.pop( sid )
        pass
    pass
if __name__=='__main__':
    ENV=os.environ.get
    WSGIServer((ENV('HOST','0'), int(ENV('PORT',8080))), app,
               handler_class=WebSocketHandler).serve_forever()
