import io
import picamera
import logging   # for tracking events
import socketserver
from threading import Condition
from http import server

camera = None
class StreamingOutput(object):  # generate streaming output
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()  # in-memory binary stream
        self.condition = Condition() # condition variable object

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'): # start of image in JPEG
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate() # resize to the current position
            with self.condition: 
                self.frame = self.buffer.getvalue() # get entire buffer
                self.condition.notify_all() # wake up all threads waiting
            self.buffer.seek(0) # change stream position to the start
        return self.buffer.write(buf) # buffer write

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')  # for Cors
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                cnt = 0
                while True:
                    if (cnt == 24):
                        camera.capture('/home/pi/Desktop/Programs/Final/success.jpg')
                        cnt = 0
                    with output.condition:
                        output.condition.wait() # block
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n') # write the response body
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame) 
                    self.wfile.write(b'\r\n')
                    cnt +=1
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

with picamera.PiCamera(resolution='640x480', framerate=24) as camera:
    output = StreamingOutput()  # output configuration
    camera.start_recording(output, format='mjpeg')  # recording
    camera.capture('/home/pi/Desktop/Programs/Final/success.jpg')
    try:
        address = ('', 8000)
        server = StreamingServer(address, StreamingHandler)  # start server
        server.serve_forever() # handle requests until shutdown
    finally:
        camera.stop_recording() 
