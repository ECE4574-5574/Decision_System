""" Purpose : The decision system accepts incoming data from the server API. The incoming data includes user location,
commands from the App, local time, weather and state of the devices. The data will be continuously received from the server API
and  posted to the local server. The data will then be stored in temporary data structures (temporaryHolding.py). """

import BaseHTTPServer
import SocketServer
import json
import decisions
import httplib
from temporaryHolding import TemporaryHolding
from datetime import datetime

#Class that gets called whenever there is an HTTP request
class ServerInfoHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_POST(self):
    length = int(self.headers.getheader('content-length', 0))
    data = self.rfile.read(length)
    #Dictionary of the json string received
    message = json.loads(data)
    #If a weather update is received then that information is printed and a 200 response is sent
    if self.path == "/Weather":
        print "The weather condition is " + str(message["condition"])
        print "The temperature is " + str(message["temperature"])
        print "Timestamp of WeatherUpdate " + str(message["time"])
        self.send_response(200)
    #If a device state update is received then that inofrmation is printed and a 200 response is sent
    elif self.path == "/DeviceState":
        print "The Device ID is " + str(message["deviceID"])
        print "The Device Name is " + str(message["deviceName"])
        print "The Device Type is " + str(message["deviceType"])
        print "The SpaceID is " + str(message["spaceID"])
        print "The state is " + str(message["stateDevice"])
        print "Timestamp of DeviceState Action " + str(message["time"])
        self.send_response(200)
    #If a location change update is received the information is printed and sent to persistent storage. A decision is also made based on the change of location
    #and a 200 response is sent
    elif self.path == "/LocationChange":
        temp = TemporaryHolding()
        print "The user ID is: " + str(message["userId"])
        print "The Latitude is " + str(message["lat"])
        print "The Longitude is  " + str(message["long"])
        print "The Altitude is " + str(message["alt"])
        print "Timestamp of LocationChange " + str(message["time"])
        #Set up connection to persistent storage
        conn = httplib.HTTPConnection("54.152.190.217", 8081)
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
        decisions.randomDecision(float(message["lat"]), float(message["long"]), float(message["alt"]), str(message["userId"]), formatted)        
        self.send_response(200)
    #If there is a command from the app print the command
    elif self.path == "/CommandsFromApp":
        print "For User " + str(message["commandUserID"])
        print "Turn off Device ID " + str(message["commanddeviceID"])
        print "The Device Name is " + str(message["commanddeviceName"])
        print "The Device Type is " + str(message["commanddeviceType"])
        print "The SpaceID is " + str(message["commandspaceID"])
        print "The state is " + str(message["commandstateDevice"])
        print "Timestamp of Command " + str(message["time"])
        self.send_response(200)
        
    elif self.path == "/LocalTime":
        print "You may choose to perform a action based on time/date, so the time/date is now" + str(message["localTime"])
        self.send_response(200)
    else:
        self.send_response(400)
    

PORT = 8081

Handler = ServerInfoHandler
SocketServer.ThreadingTCPServer.allow_reuse_address = True
httpd = SocketServer.TCPServer(("localhost", PORT), Handler)
print "serving at port: ", PORT

httpd.serve_forever()
