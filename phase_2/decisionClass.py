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
from datetime import datetime
import decisions
import logging
import StringIO

import clr
import deviceAPIUtils
clr.AddReferenceToFileAndPath("DeviceDLL/DeviceDLL/bin/Debug/DeviceDLL.dll")
clr.AddReference('System')
import api as devapi
import deviceAPIUtils as devapiu
import System


class decisionMaking():
    def __init__(self, logger, server, deviceBase):
        self.storageAddress = server
        self.deviceBaseAdd = deviceBase
        self.weatherDecisionCount = 1
        self.deviceStateDecisionCount = 1
        self.locationDecisionCount = 1
        self.timeDecisionCount = 1
        self.commandCount = 1
        self.logger = logger

    #message should be a parsed JSON dictionary
    def weatherDecision(self, message):
        try:    
            line = "Weather Decision " + str(self.weatherDecisionCount) + ":\nData to be sent to persistent storage: " + str(message) + "\n"
            self.weatherDecisionCount += 1
            self.logger.debug(line)
        except:
            line = 'Error when trying to make a weather decision!\nRequest body being handled:\n' + str(message) + '\n'
            self.logger.warning(line)

    def deviceStateDecision(self, message):
        try:
            
            
            #Logging the device state changes in the persistent storage 
            #Set up connection to persistent storage
            conn = httplib.HTTPConnection(self.storageAddress[0], self.storageAddress[1])
            #change the format to the format required by persistent storage
            payload = json.dumps({"action-type":"device state change","action-data":message})
            requestPath = 'PATCH', 'C/' + "user1" + '/' + message["time"] + '/' + 'WayneManor' + '/' + "aspace" + '/' + message['deviceName']   
            conn.request('PATCH', 'C/' + "user1" + '/' + message["time"] + '/' + 'WayneManor' + '/' + "aspace" + '/' + message['deviceName'], payload)
            response = conn.getresponse()
            print response.status
            print response.read()
            line = "Device State Decision " + str(self.deviceStateDecisionCount) + ":\nData sent to persistent storage: " + str(payload) + "\nRequest Path: " + str(requestPath) + "\nRequest response: " + str(response.status) + "\n"
            self.deviceStateDecisionCount += 1
            self.logger.debug(line)                         
        except:
            line = 'Error when trying to make a device state decision!\nRequest body being handled:\n' + str(message) + '\n'
            self.logger.warning(line)

    def locationDecision(self, message):
        try:    
            #change the format to the format required by persistent storage     
            #Set up connection to persistent storage
            conn = httplib.HTTPConnection(self.storageAddress[0],self.storageAddress[1])
            #Pass the JSON string to persistent storage
            payload = json.dumps({"action-type":"location-update","action-data":message})
            requestPath = 'PATCH', 'A/' + message['userId'] + '/' + message["time"] + '/' + 'WayneManor'
            conn.request('PATCH', 'A/' + message['userId'] + '/' + message["time"] + '/' + 'WayneManor', payload)
            response = conn.getresponse()
            print response.status
            print response.read()
            line = "Location Decision " + str(self.locationDecisionCount) + ":\n" + "Data sent to persistent storage: " + str(payload) + "\nRequest Path: " + str(requestPath) + "\nRequest Response: " + str(response.status) + "\n"
            self.locationDecisionCount += 1
            self.logger.debug(line) 
        except:
            line = 'Error when trying to make a location decision!\nRequest body being handled:\n' + str(message) + '\n'
            self.logger.warning(line)

    def timeDecision(self, message):
        try:
            line = "Time Decision: " + str(self.timeDecisionCount) + "\nData to be sent to persistent storage: " + str(message) + "\n" 
            self.timeDecisionCount += 1
            self.logger.debug(line)
        except:
            line = 'Error when trying to make a time decision!\nRequest body being handled:\n' + str(message) + '\n'
            self.logger.warning(line)

    def command(self, message):
        output = StringIO.StringIO()
        output.write('Command Decision ' + str(self.commandCount) + ':\n')
        self.commandCount += 1
        try:
            conn = httplib.HTTPConnection(self.storageAddress[0], self.storageAddress[1])
            reqMethod = 'GET'
            reqPath = 'BU/' + message['userID']
            
            #First, try to get the user information.
            output.write('req ' + self.storageAddress[0] + ':' + str(self.storageAddress[1]) + ' ' + reqMethod + ' ' + reqPath + '\n')
            conn.request(reqMethod, reqPath)
            resp = conn.getresponse()
            output.write('response ' + str(resp.status) + '\n')
            body = resp.read()
            if (not resp.status == 200):
                self.logger.warning(output.getvalue())
                return
            body = json.loads(body)
            
            print 'Debug: '
            print body
            
            #Next, try to find a matching house.
            matchingHouse = None
            for houseID in body['houseIDs']:
                reqMethod = 'GET'
                reqPath = 'BH/' + str(houseID)
                output.write('req ' + self.storageAddress[0] + ':' + str(self.storageAddress[1]) + ' ' + reqMethod + ' ' + reqPath + '\n')
                conn.request(reqMethod, reqPath)
                resp = conn.getresponse()
                output.write('response ' + str(resp.status) + '\n')
                try:
                    blob = resp.read()
                    blob = json.loads(blob)
                    if abs(blob['lat']-message['lat']) <= 0.01 and \
                       abs(blob['lon']-message['lon']) <= 0.01 and \
                       abs(blob['alt']-message['alt']) <= 1:
                        matchingHouse = houseID
                        break
                except ValueError:
                    output.write('ValueError reading blob for house ' + str(houseID) + '. Blob is likely corrupt.\n')
                except TypeError:
                    output.write('TypeError reading coordinates for house ' + str(houseID) + '. Blob is likely corrupt.\n')
                except KeyError as ke:
                    output.write('KeyError reading coordinates for house ' + str(houseID) + 
                    ' . Blob is missing field: ' + ke.args[0] + '\n')
            else:
                output.write('Could not find a matching house for that user and coordinates.\n')
                self.logger.warning(output.getvalue())
                return
            assert(not matchingHouse is None)
            output.write('match house ' + str(matchingHouse) + '\n')
            
            #Now, request all devices in that house.
            output.write('requesting devices\n')
            devinterface = devapi.Interfaces(System.Uri(self.deviceBaseAdd))
            devices = devinterface.getDevices(matchingHouse)
            
            print 'Debug:'
            print devices
            
            for oneDevice in devices:
                if devapiu.canBrighten(oneDevice):
                    print 'found a brightenable'
                    oneDevice.set_Enabled(True)
            print output.getvalue()
            self.logger.info(output.getvalue())
            
        except:
            output.write('Error when trying to make a command decision!\n')
            output.write('Request body being handled:\n')
            output.write(str(message) + '\n')
            traceback.print_exc(None, output)
            self.logger.error(output.getvalue())
              
    
        



