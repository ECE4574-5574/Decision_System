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
    def weatherDecision(self, message, decisionCount):
        line = "Decision " + str(decisionCount) + ":\n"
        self.outputfile.write(line)

    def deviceStateDecision(self, message, decisionCount):
        line = "Decision " + str(decisionCount) + ":\n"
        self.outputfile.write(line)
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

    def locationDecision(self, message, decisionCount):
        #change the format to the format required by persistent storage
        dateTimeObject = datetime.strptime(message["time"], "%Y-%m-%d %H:%M:%S")
        formatted = dateTimeObject.strftime("%Y-%m-%dT%H:%M:%SZ")
        handler = threading.Thread(None, self.decisionThread, 'Handler for POST/LocationChange', args = (message,formatted,self.storageAddress, self.deviceBaseAdd, self.outputfile, decisionCount))
        handler.start()        
        return True

    def timeDecision(self, message, decisionCount):
        line = "Decision " + str(decisionCount) + ":\n"
        self.outputfile.write(line)

    def command(self, message, decisionCount):
        try:
            conn = httplib.HTTPConnection(self.storageAddress[0], self.storageAddress[1])
            reqMethod = 'GET'
            reqPath = 'UI/' + message['userID']
            
            #First, try to get the request.
            self.outputfile.write('req ' + self.storageAddress[0] + ':' + str(self.storageAddress[1]) + ' ' + reqMethod + ' ' + reqPath + '\n')
            conn.request(reqMethod, reqPath)
            resp = conn.getresponse()
            self.outputfile.write('response ' + str(resp.status) + '\n')
            body = resp.read()
            if (not resp.status == 200):
                return
            body = json.loads(body)
            print 'Debug: '
            print body
            matchingHouse = None
            for houseID in body['houseIDs']:
                reqMethod = 'GET'
                reqPath = 'HI/' + str(houseID)
                self.outputfile.write('req ' + self.storageAddress[0] + ':' + str(self.storageAddress[1]) + ' ' + reqMethod + ' ' + reqPath + '\n')
                conn.request(reqMethod, reqPath)
                resp = conn.getresponse()
                self.outputfile.write('response ' + str(resp.status) + '\n')
                body = resp.read()
                body = json.loads(body)
                print 'Debug house body: '
                print body
                try:
                    blob = json.loads(body['blob'])
                    if abs(blob['lat']-message['lat']) <= 0.01 and \
                       abs(blob['lon']-message['lon']) <= 0.01 and \
                       abs(blob['alt']-message['alt']) <= 1:
                        matchingHouse = houseID
                        break
                except ValueError:
                    self.outputfile.write('ValueError reading blob for house ' + str(houseID) + '. Blob is likely corrupt.\n')
                except TypeError:
                    self.outputfile.write('TypeError reading coordinates for house ' + str(houseID) + '. Blob is likely corrupt.\n')
                except KeyError as ke:
                    self.outputfile.write('KeyError reading coordinates for house ' + str(houseID) + 
                    ' . Blob is missing field: ' + ke.args[0] + '\n')
            else:
                self.outputfile.write('Could not find a matching house for that user and coordinates.\n')
                return
            assert(not matchingHouse is None)
            self.outputfile.write('match house ' + str(matchingHouse) + '\n')
        except:
            self.outputfile.write('Error when trying to make a command decision!\n')
            self.outputfile.write('Request body being handled:\n')
            self.outputfile.write(str(message))
            traceback.print_exc(None, self.outputfile)
              
    def decisionThread(self, message, cleanTime,storageAdd, deviceBaseAdd, outputfile, decisionCount):
        line = "Decision " + str(decisionCount) + ":\n"
        self.outputfile.write(line)
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



