import io
import picamera
import logging
import socketserver
from threading import Condition
from http import server
import sys

f = open('data.txt','r')

PAGE="""\
<html>
<head>
    <title>canvas</title>
    <script src="https://ajax.aspnetcdn.com/ajax/jquery/jquery-3.5.1.min.js"></script>
	<script type="text/javascript" src="//cdnjs.cloudflare.com/ajax/libs/socket.io/1.4.8/socket.io.min.js"></script>
    <style>
        html, body {
          
          width: 100%;
          height: 100%;
          padding: 0;
          margin: 0;
          overflow: hidden;
          font-family: Abel;
        }
        canvas {
          position: relative;
          background-color: #333;
          -webkit-transform: scaleY(-1);
                  transform: scaleY(-1);
        }
        .info {
          
          position: absolute;
          left: 50px;
          bottom: 50px;
        }
        h1 {
          
          color: white;
          letter-spacing: 3px;
          margin: 0;
        }
        .message {
          margin: 0;
          color: #08fe02;
        }
		.dark {
          margin: 0;
          color: #08fe02;
        }
        img {
            background-color: grey;
            margin: 0 auto;
            position: absolute;
            top: 250px;
            left: 100px;
        }
    </style>
</head>
<body>
    <canvas id="myCanvas"></canvas>
    <img src="stream.mjpg" width="640" height="480" />
	<div class="info">
	  <h1>Intelligent Surveillance Camera</h1>
	  <p class="message">temp</p>
	  <p class="dark">temp</p>
	</div>
</body>
<script>
	var radius = 100;
  	var resData= {r: 1, deg:1, night: "day"};
	var enemies = [{}]
	var c = $("#myCanvas")[0];
	var ctx = c.getContext("2d");
	var color_gold="8,254,2";
	var ww,wh;
	var center={
      x: 0,y: 0};

	function getWindowSize(){
      
	  ww=$(window).outerWidth();
	  wh=$(window).outerHeight();
	  c.width=ww;
	  c.height=wh;
	  center={
      x: ww/2+400,y: wh/2};
	  
	  ctx.restore();
	  ctx.translate(center.x,center.y);
	}
	getWindowSize();
	$(window).resize(getWindowSize);
	

	setInterval(()=>{draw(resData.deg)},200);
    setInterval(()=>{fetch("/info").then((response) => response.json()).then((data) => {resData = data;});},200);

	setInterval(()=>{
		enemies=Array(1).fill({
        }).map(
      function(obj){
        return {
          r: resData.r*4,
          deg: resData.deg,
          opacity: 0
        } 
      }
    );

	}, 100)
  	

	var deg_to_pi=Math.PI/180;

	function Point(r,deg){
      
	  return {
      
	    x: r*Math.cos(deg_to_pi*deg),
	    y: r*Math.sin(deg_to_pi*deg),
	  };
	}
	function Color(op){
      
	  return "rgba("+color_gold+","+op+")";
	}

	function draw(line_deg) {
		$(".dark").text(resData.night);
	  ctx.fillStyle = "#111";
	  ctx.beginPath();
	  ctx.rect(-2000,-2000,4000,4000);
	  ctx.fill();
	  
	  ctx.strokeStyle="rgba(255,255,255,0.1)";
	  ctx.moveTo(-ww/2+400,0);
	  ctx.lineTo(ww/2+400,0);
	  ctx.moveTo(0,-wh/2+110);
	  ctx.lineTo(0,wh/2-110 );
	  ctx.stroke();
	  
	  ctx.strokeStyle=Color(1);
	  var r=200;
	  var newpoint=Point(r,deg);
	  // console.log(line_deg);
	  

        var deg1 = (line_deg-1) ;
        var deg2 = (line_deg) ;

        var point1=Point(r,deg1);
        var point2=Point(r,deg2);

        ctx.beginPath();
        // ctx.fillStyle="white";
        ctx.fillStyle=Color(1);
        ctx.moveTo(0,0);
        ctx.lineTo(point1.x,point1.y);
        ctx.lineTo(point2.x,point2.y);
        // ctx.stroke();
        ctx.fill();

	  
	  enemies.forEach(function(obj){
	    ctx.fillStyle=Color(obj.opacity);
		obj.deg =resData.deg
		if (obj.r > 200) {
			obj.r = 200
		}
	    var obj_point=Point(obj.r,obj.deg);
	    
	    ctx.beginPath();
	    ctx.arc(
	      obj_point.x,obj_point.y,
	      4,0,2*Math.PI
	    );
	    ctx.fill();
	    
	    ctx.strokeStyle= Color(obj.opacity);
	    var x_size=6;
	    ctx.lineWidth=4;
	    ctx.beginPath();
	    ctx.moveTo(obj_point.x-x_size,obj_point.y+x_size);
	    ctx.lineTo(obj_point.x+x_size,obj_point.y-x_size);
	    ctx.moveTo(obj_point.x+x_size,obj_point.y+x_size);
	    ctx.lineTo(obj_point.x-x_size,obj_point.y-x_size);
	    ctx.stroke();
	    
	    if (Math.abs(obj.deg - line_deg)<=1){
        if (obj.r<200) {
           obj.opacity=1;
	        $(".message").text("Detected: "+ ((obj.r)/4).toFixed(3) + " at " +obj.deg.toFixed(3));

        } else {
	        $(".message").text("Not Detected");

        }
	     
	    }
	    obj.opacity*=0.99;	    
	    ctx.strokeStyle= Color(obj.opacity);
	    ctx.lineWidth=1;
	    ctx.beginPath();
	    ctx.arc(
	      obj_point.x,obj_point.y,
	      10*(1/(obj.opacity+0.0001)),0,2*Math.PI
	    );
	    ctx.stroke();
	  });
	  
	  ctx.strokeStyle=Color(1);
	  var split =120;
	  var feature =15;
	  var start_r=230;
	  var len = 5;
	  
	  for(var i=0;i<split;i++){
      
	    ctx.beginPath();
	    var deg = (i/120) * 180;
	    
	    if (i%feature==0){
      
	      len=10;
	      ctx.lineWidth=3;
	    }else{
      
	      len=5; 
	      ctx.lineWidth=1;
	    }
	    var point1 =Point(start_r,deg);
	    var point2 =Point(start_r+len,deg);
	    
	    ctx.moveTo(point1.x,point1.y);
	    ctx.lineTo(point2.x,point2.y);
	    ctx.stroke();
	  }
	}
</script>
</html>
"""

class StreamingOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/index.html':
            print "page load"
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/info':
            data = f.readlines()[-1].split(' ')
            f.seek(0)
            inf = '{"r": '+ data[1] +', "deg": '+data[0]+ ', "night": "'+ data[2].strip('\n') +'"}'
            content = inf.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

with picamera.PiCamera(resolution='640x480', framerate=20) as camera:
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    try:

        address = ('', 8888)
        server = StreamingServer(address, StreamingHandler)
        server.serve_forever()
    finally:
        camera.stop_recording()