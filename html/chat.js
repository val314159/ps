function Application(cfg){this.cfg=cfg}
Application.prototype.start = function() {
    var cfg = this.cfg;
    var ws = this.ws = new WebSocket('ws://'+cfg.host+'/ws');
    ws.onopen=function(){
	console.log("on open",this);
    }.bind(this);
    ws.onerror=function(){
	console.log("on error");
    }.bind(this);
    ws.onclose=function(){
	console.log("on close");
    }.bind(this);
    ws.onmessage=function(evt){
	console.log("on message",evt);
	this.onjson(JSON.parse(evt.data));
    }.bind(this);
};
Application.prototype.onjson = function(msg){
    console.log("on json msg ", msg);
    var cmd = msg[1];
    if (cmd=="HELLO") this.hello( msg[2] );
};
Application.prototype.pub = function(ch,msg) {
    this.ws.send(JSON.stringify([0,'PUB', ch,this.sid,msg]));
};
Application.prototype.pubp= function(ch,msg) {
    this.ws.send(JSON.stringify([0,'PUB+',ch,this.sid,msg]));
};
Application.prototype.sub = function(channels) {
    this.ws.send(JSON.stringify([0,'SUB',channels]));
};
Application.prototype.hello = function(sid) {
    this.sid = sid;
    console.log("HELLO", sid);
    this.there();
};
Application.prototype.there = function() {
    console.log("THERE");
    this.sub(["*","$chat","SYS"])
    this.pubp("*","WOW")
};
Application.prototype.chat = function(inputCtl) {
    console.log(inputCtl.value);
};
