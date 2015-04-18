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
        return True

    def deviceStateDecision(self,message):
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
        return True


    def locationDecision(self, message):
        #change the format to the format required by persistent storage
        dateTimeObject = datetime.strptime(message["time"], "%Y-%m-%d %H:%M:%S")
        formatted = dateTimeObject.strftime("%Y-%m-%dT%H:%M:%SZ")
        handler = threading.Thread(None, self.decisionThread, 'Handler for POST/LocationChange', args = (message,formatted,self.storageAddress, self.deviceBaseAdd, self.outputfile))
        handler.start()        
        return True

    def timeDecision(self, message):
        return True


    def command(self, message):
        return True        

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



