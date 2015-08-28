function Application(cfg){this.cfg=cfg}
Application.prototype.start = function() {
    var cfg = this.cfg;
    var ws = this.ws = new WebSocket('ws://'+cfg.host+'/ws');
    ws.onopen=function(){
	console.log("on open",this);
	this.sub(["*","$chat","SYS"])
	console.log("on open",this);
	this.pubp("*","?","WOW")
	console.log("on open",this);
    }.bind(this);
    ws.onerror=function(){
	console.log("on error");
    }.bind(this);
    ws.onclose=function(){
	console.log("on close");
    }.bind(this);
    ws.onmessage=function(evt){
	ws.onjsonmessage(JSON.parse(evt.data));
    }.bind(this);
    ws.onjsonmessage=function(msg){
	console.log("on json msg ", msg);
    }.bind(this);
};
Application.prototype.pub = function(ch,sid,msg) {
    this.ws.send(JSON.stringify([0,'PUB', ch,sid,msg]));
};
Application.prototype.pubp= function(ch,sid,msg) {
    this.ws.send(JSON.stringify([0,'PUB+',ch,sid,msg]));
};
Application.prototype.sub = function(channels) {
    this.ws.send(JSON.stringify([0,'SUB',channels]));
};
Application.prototype.chat = function(inputCtl) {
    console.log(inputCtl.value);
};
