#Contributor : Prerana Rane
#Post function will send the device, house, room and user data to the localhost, port 8080 

import BaseHTTPServer
import SocketServer
import json
import sys
import PersistentStorageFunctions as PSF

POST_FUNCTION_RANGE = {'D': '6', 'R': '4', 'H': '2', 'U': '2'}

class PersistentInfoHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            self.PostRequest(self.path)
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
        	resp = PSF.postDevice(self, houseID, version,roomID, deviceID)
        	self.send_response(200)
        elif InputPath[0] == 'R':
            #send Room Data
            resp = PSF.postRoom(self, houseID, version,roomID)
            self.send_response(200)
        elif InputPath[0] == 'H':
            #send House Data
            resp = PSF.postHouse(self, houseID)
            self.send_response(200)
        elif InputPath[0] == 'U':
            #send User Data
            resp = PSF.postUser(self, userID)
            self.send_response(200)
        else:
        	print " Command not supported"
     
    def ResponseInternalErr(self):
        self.send_response(500)
        self.end_headers()


PORT = 8080

Handler = PersistentInfoHandler
SocketServer.ThreadingTCPServer.allow_reuse_address = True
httpd = SocketServer.TCPServer(("localhost", PORT), Handler)
print "Serving at port: ", PORT

httpd.serve_forever()
