#!/usr/bin/env python
"""
A simple pubsub implementation

because the needs of the many outweigh the needs of the few.

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
        _.sessions[sid], _.channels[sid] = fun, [sid]
        pass
    def pop(_,sid):
        "pop off a session from the internal tables"
        return _.sessions.pop( sid ), _.channels.pop( sid )
    def sub(_,sid,chs):
        "subscribe session id (sid) to a new list of channels (chs)"
        return _.channels[sid].append( chs )
    def pub(_,sid,channel,msg,skip_self=True):
        """
        publish from session id (sid) msg across channel
        skip_self can be set to False to reflect your messages back at you
        """
        for k,fun in _.sessions.iteritems():
            if skip_self  and  k==sid: continue
            if channel in _.channels[k]:
                fun( sid, channel, msg )
