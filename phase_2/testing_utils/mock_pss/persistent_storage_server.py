from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import logging
import threading
import time
import sys
import json
import mock_responses as mresp

GET_FUNCTION_TOKEN_RANGES = {\
            'HD': '2', 'RD': '3', 'HT': '3', 'RT': '4',\
            'BU': '2,3', 'BH': '2,3', 'BR':'3',\
            'AL': '3-5', 'AT': '6', 'AI': '6',\
            'CL': '3-5', 'CT': '6', 'CI': '6', 'HR': '2'}
POST_FUNCTION_TOKEN_RANGES = {'D': '6', 'R': '4', 'H': '2', 'U': '2'}
PATCH_FUNCTION_TOKEN_RANGES = {'A': '4-7', 'C': '4-7'}
DELETE_FUNCTION_TOKEN_RANGES = {'A': '2', 'D': '5', 'R': '4', 'H': '2', 'U': '2'}

class HATSPersistentStorageRequestHandler(BaseHTTPRequestHandler):

    #When responsding to a request, the server instantiates a DeviceHubRequestHandler
    #and calls one of these functions on it.
    
    def do_GET(self):
        try:
            if self.validateGetRequest(self.path):
                if self.path.strip('/').split('/')[0] == 'BU' and not self.path.strip('/').split('/')[1] == 'bsaget':
                    self.send_response(404)
                    self.end_headers()
                self.send_response(200)
                self.send_header('Content-Type', 'applcation/json')
                self.end_headers()
                tokens = self.path.strip('/').split('/')
                if len(tokens) == 2:
                    self.wfile.write(mresp.getMockResponse(tokens[0], tokens[1]))
                elif len(tokens) == 3:
                    self.wfile.write(mresp.getMockResponse(tokens[0], [tokens[1], tokens[2]]))
                else:
                    self.wfile.write(mresp.getMockResponse(tokens[0]), 0)
            else:
                self.stubResponseBadReq()
        except:
            #For any other uncaught internal error, respond HTTP 500:
            e = sys.exc_info()
            print e
            self.stubResponseInternalErr()
    
    def validateGetRequest(self, path): 
        tokenizedPath = path.strip('/').split('/')
        if not tokenizedPath[0] in GET_FUNCTION_TOKEN_RANGES:
            return False
        return (isInRange(len(tokenizedPath), GET_FUNCTION_TOKEN_RANGES[tokenizedPath[0]]))

    def do_POST(self):
        try:
            if self.validatePostRequest(self.path):
                self.stubResponseOK()
            else:
                self.stubResponseBadReq()
        except:
            e = sys.exc_info()
            print e
            self.stubResponseInternalErr()

    def validatePostRequest(self, path):
        tokenizedPath = path.strip('/').split('/')
        if not tokenizedPath[0] in POST_FUNCTION_TOKEN_RANGES:
            return False
        return (isInRange(len(tokenizedPath), POST_FUNCTION_TOKEN_RANGES[tokenizedPath[0]]))
    
    def do_PATCH(self):
        try:
            if self.validatePatchRequest(self.path):
                self.stubResponseOK()
            else:
                self.stubResponseBadReq()
        except:
            e = sys.exc_info()
            print e
            self.stubResponseInternalErr()

    def validatePatchRequest(self, path):
        tokenizedPath = path.strip('/').split('/')
        if not tokenizedPath[0] in PATCH_FUNCTION_TOKEN_RANGES:
            return False
        return (isInRange(len(tokenizedPath), PATCH_FUNCTION_TOKEN_RANGES[tokenizedPath[0]]))
    
    def do_DELETE(self):
        try:
            if self.validateDeleteRequest(self.path):
                self.stubResponseOK()
            else:
                self.stubResponseBadReq()
        except:
            e = sys.exc_info()
            print e
            self.stubResponseInternalErr()

    def validateDeleteRequest(self, path):
        tokenizedPath = path.strip('/').split('/')
        if not tokenizedPath[0] in DELETE_FUNCTION_TOKEN_RANGES:
            return False
        return (isInRange(len(tokenizedPath), DELETE_FUNCTION_TOKEN_RANGES[tokenizedPath[0]]))

    def stubResponseOK(self):
        self.send_response(200)
        self.end_headers()

    def stubResponseBadReq(self):
        self.send_response(400)
        self.end_headers()

    def stubResponseInternalErr(self):
        self.send_response(500)
        self.end_headers()

class HATSPersistentStorageServer(HTTPServer):

    def __init__(self, server_address, RequestHandlerClass):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.shouldStop = False
        self.timeout = 1

    def serve_forever (self):
        while not self.shouldStop:
            self.handle_request()

def isInRange(i, strRange):
    if '+' in strRange:
        min = int(strRange.split('+')[0])
        return i >= min

    allowable = []
    for onePart in strRange.split(','):
        if '-' in onePart:
            lo, hi = onePart.split('-')
            lo, hi = int(lo), int(hi)
            allowable.extend(range(lo, hi+1))
        else:
            allowable.append(int(onePart))
    
    return i in allowable

def runServer(server):
    server.serve_forever()

## Starts a server on a background thread.
#  @param server the server object to run.
#  @return the thread the server is running on.
#          Retain this reference because you should attempt to .join() it before exiting.
def serveInBackground(server):
    thread = threading.Thread(target=runServer, args =(server,))
    thread.start()
    return thread


if __name__ == "__main__":
    LISTEN_PORT = 8080
    server = HATSPersistentStorageServer(('',LISTEN_PORT), HATSPersistentStorageRequestHandler)
    serverThread = serveInBackground(server)
    try:
        while serverThread.isAlive():
            print 'Serving...'
            time.sleep(10)
            print 'Still serving...'
            time.sleep(10)
    except KeyboardInterrupt:
        print 'Attempting to stop server (timeout in 30s)...'
        server.shouldStop = True
        serverThread.join(30)
        if serverThread.isAlive():
            print 'WARNING: Failed to gracefully halt server.'

