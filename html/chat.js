function Application(cfg){this.cfg=cfg}
Application.prototype.start = function() {
    this.ws = new WebSocket('ws://'+this.cfg.host+'/ws');
    this.ws.onopen=function(){
	    console.log("on open",this);
    }.bind(this);
    this.ws.onerror=function(){
	    console.log("on error");
    }.bind(this);
    this.ws.onclose=function(){
	    console.log("on close");
    }.bind(this);
    this.ws.onmessage=function(evt){
	    console.log("on message",evt.data);
      var msg = JSON.parse(evt.data);
      var typ = msg[0];
      if (typ===0) {
        this.sid = msg[2].sessionId;
        this.onhello();
      } else if (typ===2) {
        this.onpub( msg[1], msg[2]);
      } else {
        console.log("ERR", msg);
      }
    }.bind(this);
};
Application.prototype.appendJSON = function(msg) {
  var elt = document.createTextNode( JSON.stringify( msg ) );
  document.getElementsByTagName( 'body' )[0].appendChild( elt );
}
Application.prototype.pub = function(ch,msg,rid) {
    this.ws.send(JSON.stringify([1, ch, rid||"", msg]));
};
Application.prototype.sub = function(channels) {
    this.ws.send(JSON.stringify([0,':SUB:',{"channels":channels}]));
};
Application.prototype.onpub = function(src, msg) {
    this.appendJSON([src,msg]);
};
Application.prototype.onhello = function() {
    this.appendJSON([":HELLO:",this.sid]);
};
