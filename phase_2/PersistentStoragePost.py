"""API Calls to and from the Persistent Storage
Contributors : Prerana Rane and Sumit Kumar
Created : 3/30/2015
Last modified : 4/6/2015
Purpose : Post function will send the device, house, room and user data to the localhost, port 8080 
Method of Testing: Run this file and then send a POST command."""

import BaseHTTPServer
import SocketServer
import json
import sys
import PersistentStorageFunctions as PSF

POST_FUNCTION_RANGE = {'D': '6', 'R': '4', 'H': '2', 'U': '2'}
InputPath = []

class PersistentInfoHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            self.PostRequest(self.path)
        except:
            error = sys.exc_info()  #catches exceptions
            print error
            self.ResponseInternalErr()

    def PostRequest(self, path, houseID, version, roomID, deviceID, userID):
        try:
            global InputPath
            InputPath = path.strip('/').split('/')
            print InputPath
            if not InputPath[0] in POST_FUNCTION_RANGE:
                return False

            elif InputPath[0] == 'D':
                resp = PSF.postDevice(self, houseID, version, roomID, deviceID)
                if resp:
                    self.send_response(200)
                else:
                    raise Exception("Failed to Post.")

            elif InputPath[0] == 'R':
                #send Room Data
                resp = PSF.postRoom(self, houseID, version, roomID)
                if resp:
                    self.send_response(200)
                else:
                    raise Exception("Failed to Post.")

            elif InputPath[0] == 'H':
                #send House Data
                resp = PSF.postHouse(self, houseID)
                if resp:
                    self.send_response(200)
                else:
                    raise Exception("Failed to Post.")
            elif InputPath[0] == 'U':
                #send User Data
                resp = PSF.postUser(self, userID)
                if resp:
                    self.send_response(200)
                else:
                    raise Exception("Failed to Post.")
            else:
                print " Command not supported"

        except Exception as e:
            print e.message
     
    def ResponseInternalErr(self):
        self.send_response(500)
        self.end_headers()


if __name__ == '__main__':
    PORT = 8080

    Handler = PersistentInfoHandler
    SocketServer.ThreadingTCPServer.allow_reuse_address = True
    httpd = SocketServer.TCPServer(("localhost", PORT), Handler)
    print "Serving at port: ", PORT

    httpd.serve_forever()

