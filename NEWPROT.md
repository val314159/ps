## PROT

```
- ping
    - write [">>PIN>>",fd,109,{blah}]
- pong
    - read  ["<<PON<<",fd,109,{blah}]
- sub
    - write [">>SUB>>",fd,109,["x","y"]]
- uns
    - write ["<<UNS<<",fd,109,["x","y"]]
- pub
    - write ["channel",fd,109,{data}]
- error
    - read  ["channel",fd,109,{err stuff}]
- req
    - write [">25>32>",fd,109,{data}]
- rep
    - read  ["<25<32<",fd,109,{data}]
```
