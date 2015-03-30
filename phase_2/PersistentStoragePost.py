#Contributor : Prerana Rane
#Post function will send the device, house, room and user data 
import BaseHTTPServer
import SocketServer
import json
import sys
import decisions

POST_FUNCTION_RANGE = {'D': '6', 'R': '4', 'H': '2', 'U': '2'}

class PersistentInfoHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            if self.PostRequest(self.path):
                self.ResponseOK()
            else:
                self.ResponseBadReq()
        except:
            error = sys.exc_info()
            print error
            self.ResponseInternalErr()

    def PostRequest(self, path):
        InputPath = path.strip('/').split('/')
        print InputPath
        if not InputPath[0] in POST_FUNCTION_RANGE:
            return False 
        elif InputPath[0] == 'D':
        	#send Device Data
        elif InputPath[0] == 'R':
            #send Room Data
        elif InputPath[0] == 'H':
            #send House Data
        elif InputPath[0] == 'U':
            #send User Data
            
    def ResponseOK(self):
        self.send_response(200)
        self.end_headers()

    def ResponseBadReq(self):
        self.send_response(400)
        self.end_headers()

    def ResponseInternalErr(self):
        self.send_response(500)
        self.end_headers()


PORT = 8080

Handler = PersistentInfoHandler
SocketServer.ThreadingTCPServer.allow_reuse_address = True
httpd = SocketServer.TCPServer(("localhost", PORT), Handler)
print "Serving at port: ", PORT

httpd.serve_forever()
