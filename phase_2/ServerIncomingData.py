""" Purpose : The decision system accepts incoming data from the server API. The incoming data includes user location,
commands from the App, local time, weather and state of the devices. The data will be continuously received from the server API
and  posted to the local server. The data will then be stored in temporary data structures (temporaryHolding.py). """

#Andrew Gardner: Added functionality to the location change post request so that the location data would be written to persistent storage and the 
#decision class would be called to make a random decision to send to the server and persistent storage. Also editted the JSON string received to 
#meet requirements from other teams

#Mark Koninckx: Added error-handling code that allows for discerning between unhandled internal errors and malformed requests, and accurately
#reporting these errors to the code making the call over HTTP.

import BaseHTTPServer
import SocketServer
import json
import decisions
import traceback
import threading
import time
import httplib
import argparse
import sys
from temporaryHolding import TemporaryHolding
from datetime import datetime

#Class that gets called whenever there is an HTTP request
class ServerInfoHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_POST(self):
    try:
        length = int(self.headers.getheader('content-length', 0))
        data = self.rfile.read(length)
        message = ""
        #Dictionary of the json string received
        try:
            message = json.loads(data)
        except ValueError:
            self.send_response(400)
            self.end_headers
            self.wfile.write("\nThe request body could not be parsed as JSON. The received request body:\n" + data)
            return
        #If a weather update is received then that information is printed and a 200 response is sent
        if self.path == "/Weather":
            try: 
                print "The weather condition is " + str(message["condition"])
                print "The temperature is " + str(message["temperature"])
                print "Timestamp of WeatherUpdate " + str(message["WeatherTimeStamp"])
            except KeyError as ke:
                self.handleMissingKey(ke)
                return
            self.send_response(200)
        #If a device state update is received then that inofrmation is printed and a 200 response is sent
        elif self.path == "/DeviceState":
            try:
                print "The Device ID is " + str(message["deviceID"])
                print "The Device Name is " + str(message["deviceName"])
                print "The Device Type is " + str(message["deviceType"])
                print "The SpaceID is " + str(message["spaceID"])
                print "The state is " + str(message["stateDevice"])
                print "Timestamp of DeviceState Action " + str(message["DeviceStateTimeStamp"])
            except KeyError as ke:
                self.handleMissingKey(ke)
                return
            self.send_response(200)
        #If a location change update is received the information is printed and sent to persistent storage. A decision is also made based on the change of location
        #and a 200 response is sent
        elif self.path == "/LocationChange":
            try:
                temp = TemporaryHolding()
                print "The user ID is: " + str(message["userId"])
                print "The Latitude is " + str(message["lat"])
                print "The Longitude is  " + str(message["long"])
                print "The Altitude is " + str(message["alt"])
                print "Timestamp of LocationChange " + str(message["time"])
                #Set up connection to persistent storage
                conn = httplib.HTTPConnection(self.server.storageAddress[0], self.server.storageAddress[1])
                #change the format to the format required by persistent storage
                dateTimeObject = datetime.strptime(message["time"], "%Y-%m-%d %H:%M:%S")
                formatted = dateTimeObject.strftime("%Y-%m-%dT%H:%M:%SZ")
                #Pass the JSON file to persistent storage
                payload = json.dumps({"action-type":"location-update","action-data":message})
                conn.request('PATCH', 'A/' + message['userId'] + '/' + formatted + '/' + 'WayneManor', payload)
                response = conn.getresponse()
                print response.status
                print response.read()
                #make a random decision
                decisions.randomDecision(float(message["lat"]), float(message["long"]), float(message["alt"]), str(message["userId"]), formatted, self.server.storageAddress, self.server.deviceBase)        
                self.send_response(200)
            except KeyError as ke:
                self.handleMissingKey(ke)
                return
        #If there is a command from the app print the command
        elif self.path == "/CommandsFromApp":
            try:
                print "For User " + str(message["commandUserID"])
                print "Turn off Device ID " + str(message["commanddeviceID"])
                print "The Device Name is " + str(message["commanddeviceName"])
                print "The Device Type is " + str(message["commanddeviceType"])
                print "The SpaceID is " + str(message["commandspaceID"])
                print "The state is " + str(message["commandstateDevice"])
                print "Timestamp of Command " + str(message["CommandTimeStamp"])
            except KeyError as ke:
                self.handleMissingKey(ke)
                return
            decisions.randomDecision()
            self.send_response(200)
        elif self.path == "/TimeConfig":
            self.server.timeconfig = message
            self.send_response(200)
            self.end_headers()
        elif self.path == "/LocalTime":
            try:
                print "You may choose to perform a action based on time/date, so the time/date is now" + str(message["localTime"])
            except KeyError as ke:
                self.handleMissingKey(ke)
                return
            self.send_response(200)
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write("\nThe request path: " + self.path + " does not match anything on the decision-making API.")
    except:
        #We want to catch all otherwise-unhandled errors, and return a 500 error code.
        self.send_response(500)
        self.end_headers()
        self.wfile.write("\nAn internal error occured. Please report this to the Decision-Making API team.\n")
        self.wfile.write("Request path: " + self.path + "\n")
        traceback.print_exc(None, self.wfile)
  
  def handleMissingKey(self, keyError):
    self.send_response(400)
    self.end_headers()
    self.wfile.write('\nYour request body is missing a JSON key which is necessary to handle your request.\n')
    self.wfile.write('Request path: ' + self.path + '\n')
    if not keyError is None:
        self.wfile.write('Missing key: ' + keyError.args[0])

class HaltableHTTPServer(BaseHTTPServer.HTTPServer):

    def __init__(self, server_address, persistentStorageAddress, deviceBase, RequestHandlerClass):
        BaseHTTPServer.HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.shouldStop = False
        self.timeout = 1
        self.storageAddress = persistentStorageAddress
        self.timeconfig = {}
	self.deviceBase = deviceBase

    def serve_forever (self):
        while not self.shouldStop:
            self.handle_request()

def runServer(server):
    server.serve_forever()

def serveInBackground(server):
    thread = threading.Thread(target=runServer, args =(server,))
    thread.start()
    return thread

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-q', '--quiet', action='store_true')
    argparser.add_argument('-p', '--port', type=int)
    argparser.add_argument('-t', '--storage', type=str)
    argparser.add_argument('-d', '--devicebase', type=str, default='http://localhost:8082/api/devicemgr/state/')
    args = argparser.parse_args()
    #Validate arguments. Port number:
    if args.port < 0:
        print "You must enter a port number greater than 0."
        argparser.print_help()
        sys.exit(1)
    #Persistent storage address:
    persistentStorageAddress=[]
    try:
        persistentStorageAddress.append(args.storage.split(':')[0])
        persistentStorageAddress.append(args.storage.split(':')[1])
        if persistentStorageAddress[1] <= 0:
            raise ValueError
    except (ValueError, IndexError):
        print "You must enter a valid persistent storage address and port number (e.g. 127.0.0.1:8080)"
        argparser.print_help()
        sys.exit(1) 
    server = HaltableHTTPServer(('',args.port), persistentStorageAddress, args.devicebase, ServerInfoHandler)
    #Print the server port. We actually get this from the server object, since
    #the user can enter a port number of 0 to have the OS assign some open port.
    print "Serving on port " + str(server.socket.getsockname()[1]) + "..."
    print "Using persistent storage at " + persistentStorageAddress[0] + ":" + str(persistentStorageAddress[1]) + "..."
    serverThread = serveInBackground(server)
    try:
        while serverThread.isAlive():
            if not args.quiet:
                print 'Serving...'
            time.sleep(10)
            if not args.quiet:
                print 'Still serving...'
            time.sleep(10)
    except KeyboardInterrupt:
        print 'Attempting to stop server (timeout in 30s)...'
        server.shouldStop = True
        serverThread.join(30)
        if serverThread.isAlive():
            print 'WARNING: Failed to gracefully halt server.'
