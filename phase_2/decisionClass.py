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
import logging

class decisionMaking():
    def __init__(self, server,deviceBase):
        self.storageAddress = server
        self.deviceBaseAdd = deviceBase
        self.weatherDecisionCount = 1
        self.deviceStateDecisionCount = 1
        self.locationDecisionCount = 1
        self.timeDecisionCount = 1
        self.commandCount = 1
        logging.basicConfig(filename='output.log', level=logging.DEBUG)
        self.logger = logging.getLogger('MyLogger')

    #message should be a parsed JSON dictionary
    def weatherDecision(self, message):
        line = "Weather Decision " + str(self.weatherDecisionCount) + ":\n"
        self.weatherDecisionCount += 1
        self.logger.debug(line)
        

    def deviceStateDecision(self, message):
        line = "Device State Decision " + str(self.deviceStateDecisionCount) + ":\n"
        self.deviceStateDecisionCount += 1
        self.logger.debug(line)
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

    def locationDecision(self, message):
        #change the format to the format required by persistent storage
        dateTimeObject = datetime.strptime(message["time"], "%Y-%m-%d %H:%M:%S")
        formatted = dateTimeObject.strftime("%Y-%m-%dT%H:%M:%SZ")        
        line = "Location Decision " + str(self.locationDecisionCount) + ":\n"
        self.locationDecisionCount += 1
        self.logger.debug(line)
        #Set up connection to persistent storage
        conn = httplib.HTTPConnection(self.storageAddress[0],self.storageAddress[1])
        #Pass the JSON string to persistent storage
        payload = json.dumps({"action-type":"location-update","action-data":message})
        conn.request('PATCH', 'A/' + message['userId'] + '/' + formatted + '/' + 'WayneManor', payload)
        response = conn.getresponse()
        print response.status
        print response.read()
        #make a random decision

    def timeDecision(self, message):
        line = "Time Decision " + str(self.timeDecisionCount) + ":\n"
        self.timeDecisionCount += 1
        self.logger.debug(line)

    def command(self, message):
        line = "Command " + str(self.commandCount) + ":\n"
        self.commandCount += 1
        self.logger.debug(line)
              
    
        



