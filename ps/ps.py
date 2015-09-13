"""
A simple pubsub implementation
"""
class PubSub(object):
    """
    The classic PubSub pattern.

    Everything is indexed by sid, the session id.
    sessions are really callback functions that write the data
    """
    def __init__(_):
        "constructor, sets up internal tables"
        _.sessions, _.channels = {}, {}
        pass
    def add(_,sid,fun):
        "add a session (session id,function pair) to the internal tables"
        _.sessions[sid], _.channels[sid] = fun, ["*",sid]
        pass
    def pop(_,sid):
        "pop off a session from the internal tables"
        return _.sessions.pop( sid ), _.channels.pop( sid )
    def sub(_,sid,chs):
        "subscribe session id (sid) to a new list of channels (chs)"
        print "-PRE-SUB", _.channels[sid]
        _.channels[sid].extend( chs )
        print "POST-SUB", _.channels[sid]
        return
    def pub(_,sid,channel,msg):
        "publish from session id (sid) msg across channel"
        for k,fun in _.sessions.iteritems():
            if k != sid  and  channel in _.channels[k]:
                fun( sid, channel, msg )

    def snd(_,sid,msg):
        _.sessions[sid]( sid, sid, msg )
