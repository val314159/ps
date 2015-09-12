# ppsp - pure pub-sub protocol

wire conversation:

- Server: `[0,":HELLO:",{sessionId:"<sessionid>"}]`

    Server says hello, also tells you your client id

- Client: `[0,":SUB:",{channels:["x","y","z"]}]`

    Client subscribes to a bunch of channels (not including "session_id" or "\*")

- Client: `[1,"*","rid",["Hello"]]`

    Client publishes a value over a channel

- Server: `[2,"<sessionid>",[1,"*","rid",["Hello"]]]`

    Server publishes a wrapped message to the "\*" channel

- Client: `[1,"<originalsessionid>","",["ShakeHands"],{replyId:"rid"}]]`

    Other Client decides to say hello back

- Server: `[2,"<remotesessionid>",[1,"<originalsessionid>","",["ShakeHands"],{replyId:"rid"}]]`

    Original client hears the hello back
