import BaseHTTPServer
import SocketServer
import json

class ServerInfoHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_POST(self):
    length = int(self.headers.getheader('content-length', 0))
    data = self.rfile.read(length)
    message = json.loads(data)
    if self.path == "/Weather":
      print "The weather condition is " + str(message["condition"])
      print "The temperature is " + str(message["temperature"])
      print "Timestamp of WeatherUpdate " + str(message["WeatherTimeStamp"])

  
    if self.path == "/DeviceState":
        print "The Device ID is " + str(message["deviceID"])
        print "The Device Name is " + str(message["deviceName"])
        print "The Device Type is " + str(message["deviceType"])
        print "The SpaceID is " + str(message["spaceID"])
        print "The state is " + str(message["stateDevice"])
        print "Timestamp of DeviceState Action " + str(message["DeviceStateTimeStamp"])


    if self.path == "/LocationChange":
        print "The UserID that changed location is " + str(message["usersID"])
        print "The Latitude is " + str(message["latitude"])
        print "The Longitude is  " + str(message["longitude"])
        print "The Altitude is " + str(message["altitude"])
        print "Timestamp of LocationChange " + str(message["locationTimeStamp"])


    if self.path == "/CommandsFromApp":
        print "For User " + str(message["commandUserID"])
        print "Turn off Device ID " + str(message["commanddeviceID"])
        print "The Device Name is " + str(message["commanddeviceName"])
        print "The Device Type is " + str(message["commanddeviceType"])
        print "The SpaceID is " + str(message["commandspaceID"])
        print "The state is " + str(message["commandstateDevice"])
        print "Timestamp of Command " + str(message["CommandTimeStamp"])


    if self.path == "/LocalTime":
        print "You may choose to perform a action based on time/date, so the time/date is now" + str(message["localTime"]) 

    self.send_response(200)

PORT = 8081

Handler = ServerInfoHandler
SocketServer.ThreadingTCPServer.allow_reuse_address = True
httpd = SocketServer.TCPServer(("localhost", PORT), Handler)
print "serving at port: ", PORT

httpd.serve_forever()
