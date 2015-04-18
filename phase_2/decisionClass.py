import requests
import json
import os
import httplib
import traceback
import threading
import BaseHTTPServer
import SocketServer
import traceback
import threading
import time
import httplib
import argparse
import sys
from temporaryHolding import TemporaryHolding
from datetime import datetime
import decisions

class decisionMaking():
    def __init__(self,outputfile,server, deviceBase):
        self.outputfile = outputfile
        self.storageAddress = server
        self.deviceBaseAdd = deviceBase
    #message should be a parsed JSON dictionary
    def weatherDecision(self, message):
        try: 
            print "The weather condition is " + str(message["condition"])
            print "The temperature is " + str(message["temperature"])
            print "Timestamp of WeatherUpdate " + str(message["WeatherTimeStamp"])
        except KeyError as ke:
            self.handleMissingKey(ke)
            return false
        return True

    def deviceStateDecision(self,message):
        try:
            print "The Device Name is " + str(message["deviceName"])
            print "The Device Type is " + str(message["deviceType"])
            print "The Device is enabled " + str(message["enabled"])
            print "The setpoint is " + str(message["setpoint"])
            print "Timestamp of DeviceState Action " + str(message["time"])
            # Begin - Prerana Rane 4/15/2015
            #Logging the device state changes in the persistent storage 
            #Set up connection to persistent storage
            conn = httplib.HTTPConnection(self.storageAddress[0], self.storageAddress[1])
            #change the format to the format required by persistent storage
            dateTimeObject = datetime.strptime(message["time"], "%Y-%m-%d %H:%M:%S")
            formatted = dateTimeObject.strftime("%Y-%m-%dT%H:%M:%SZ")
            payload = json.dumps({"action-type":"device state change","action-data":message})
            conn.request('PATCH', 'C/' + "user1" + '/' + formatted + '/' + 'WayneManor' + '/' + "aspace" + '/' + message['deviceName'], payload)
            response = conn.getresponse()
            print response.status
            print response.read()               
            #End - Prerana Rane 4/15/2015
        except KeyError as ke:
            self.handleMissingKey(ke)
            return
        return True

    def locationDecision(self, message):
        try:
            print "The user ID is: " + str(message["userId"])
            print "The Latitude is " + str(message["lat"])
            print "The Longitude is  " + str(message["long"])
            print "The Altitude is " + str(message["alt"])
            print "Timestamp of LocationChange " + str(message["time"])
            #change the format to the format required by persistent storage
            dateTimeObject = datetime.strptime(message["time"], "%Y-%m-%d %H:%M:%S")
            formatted = dateTimeObject.strftime("%Y-%m-%dT%H:%M:%SZ")
            handler = threading.Thread(None, self.decisionThread, 'Handler for POST/LocationChange', args = (message,formatted,self.storageAddress, self.deviceBaseAdd, self.outputfile))
            handler.start()        
        except KeyError as ke:
            self.handleMissingKey(ke)
            return
        return True

    def timeDecision(self, message):
        try:
            print "You may choose to perform a action based on time/date, so the time/date is now" + str(message["localTime"])
        except KeyError as ke:
            self.handleMissingKey(ke)
            return
        return True


    def command(self, message):
        try:
            print "For User " + str(message["commandUserID"])
            print "Latitude " + str(message["lat"])
            print "Longitude " + str(message["long"])
            print "Altitude " + str(message["alt"])
            print "Turn off Device ID " + str(message["commanddeviceID"])
            print "The Device Name is " + str(message["commanddeviceName"])
            print "The Device Type is " + str(message["commanddeviceType"])
            print "The SpaceID is " + str(message["commandspaceID"])
            print "The state is " + str(message["commandstateDevice"])
            print "Timestamp of Command " + str(message["time"])
        except KeyError as ke:
            self.handleMissingKey(ke)
            return
        return True        

    def handleMissingKey(self, keyError):
        self.send_response(400)
        self.end_headers()
        self.wfile.write('\nYour request body is missing a JSON key which is necessary to handle your request.\n')
        self.wfile.write('Request path: ' + self.path + '\n')
        if not keyError is None:
            self.wfile.write('Missing key: ' + keyError.args[0])

    def decisionThread(self, message, cleanTime,storageAdd, deviceBaseAdd, outputfile):
        #Set up connection to persistent storage
        conn = httplib.HTTPConnection(storageAdd[0],storageAdd[1])
        #Pass the JSON file to persistent storage
        payload = json.dumps({"action-type":"location-update","action-data":message})
        conn.request('PATCH', 'A/' + message['userId'] + '/' + cleanTime + '/' + 'WayneManor', payload)
        response = conn.getresponse()
        print response.status
        print response.read()
        #make a random decision
        decisions.randomDecision(float(message["lat"]), float(message["long"]), float(message["alt"]), str(message["userId"]), cleanTime, storageAdd, deviceBaseAdd, outputfile)



