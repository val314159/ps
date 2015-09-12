# ppsp - pure pub-sub protocol

wire conversation:

- Server to new client, client0 <br>
    `[0,":HELLO:",{sessionId:"<sessionid>"}]`

    Server says hello, also tells you your client id

- Client: <br>
    `[0,":SUB:",{channels:["x","y","z"]}]`

    Client subscribes to a bunch of channels (not including "session_id" or "\*")

- Client: <br>
    `[1,"*","rid",["Hello"]]`

    Client publishes a value over a channel

- Server to everyone except client0 <br>
    `[2,"<sessionid>",[1,"*","rid",["Hello"]]]`

    Server publishes a wrapped message to the "\*" channel

- Client: <br>
    `[1,"<originalsessionid>","",["ShakeHands"],{replyId:"rid"}]]`

    Other Client decides to say hello back

- Server to channel remotesessionid (just one client) <br>      
    `[2,"<remotesessionid>",[1,"<originalsessionid>","",["ShakeHands"],{replyId:"rid"}]]`

    Original client hears the hello back
