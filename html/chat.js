function Application() {
    var Host='localhost:8001';
    var ws = this.ws = new WebSocket('ws://'+Host+'/ws');
    ws.onopen=function(evt){
	console.log("on open");
	this.sub(["*","$chat","SYS"])
    };
    ws.onerror=function(evt){
	console.log("on error");
    };
    ws.onclose=function(evt){
	console.log("on close");
    };
    ws.onmessage=function(evt){
	ws.onjsonmessage(JSON.parse(evt.data));
    };
    ws.onjsonmessage=function(msg){
	console.log("on json msg ", msg);
    };
}
Application.prototype.pub = function(ch,sid,msg) {
    this.ws.send(JSON.stringify([0,'PUB', ch,sid,msg]));
};
Application.prototype.pubp= function(ch,sid,msg) {
    this.ws.send(JSON.stringify([0,'PUB+',ch,sid,msg]));
};
Application.prototype.sub = function(channels) {
    this.ws.send(JSON.stringify([0,'SUB',channels]));
};
function startApp() {
    alert("1");
    App=new Application();
    alert("2");
}
