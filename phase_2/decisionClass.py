#import requests
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
import codecs
import urllib2

#This monkey-patch is NECESSARY to make sympy work.
#It's a dangerous hack, but we're only using some limited parts of sympy...
def my_unicode_escape_decode(x):
    return x
codecs.unicode_escape_decode = my_unicode_escape_decode
from sympy import Point, Polygon
#import decisions
import logging
import StringIO

import clr
import deviceAPIUtils
clr.AddReferenceToFileAndPath("DeviceDLL/DeviceDLL/bin/Debug/DeviceDLL.dll")
clr.AddReference('System')
clr.AddReference('System.Drawing')
clr.AddReference('System.Windows.Forms')
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
            requestPath = 'PATCH', 'A/' + message['userID'] + '/' + message["time"] + '/' + 'WayneManor'
            conn.request('PATCH', 'A/' + message['userID'] + '/' + message["time"] + '/' + 'WayneManor', payload)
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
                    oneDevice.Enabled = True
            print output.getvalue()
            self.logger.info(output.getvalue())
        
        except:
            output.write('Error when trying to make a command decision!\n')
            output.write('Request body being handled:\n')
            output.write(str(message) + '\n')
            traceback.print_exc(None, output)
            self.logger.error(output.getvalue())
              
    def houseUpdate(self, message):
        #PUT THE THING IN PERSISTENT STORAGE HERE
        #DO WHATEVER JIGAR WANTS TO DO WITH IT
        print "Do the decision stuff"
	
    def restoreRoomState(self, userid, roomID, houseID):
        conn = httplib.HTTPConnection(self.storageAddress[0], self.storageAddress[1])

        #change time to one week prior to get the snapshot of the state of devices in the room.
        t1 = self.message["time"]
        temp = t1.split('T', 1)[0]
        temp1 = datetime.datetime.strptime(temp, "\%Y-\%m-\%d")
        sec = t1.split('T', 1)[-1]
        temp2 = temp1 - datetime.timedelta(days=7)
        temp3 = temp2.strftime("%Y %m %d")
        temp4 = temp3.replace(" ","-")
        prev_time = temp4 + 'T' + sec
    
	    #GET AL/USERID/TIMEFRAME/HOUSEID*/ROOMID*  Query for each of the actions logged by this user before the provided time.

        reqPath = 'AL/' + str(userid) + self.message["time"] + self.message["time"] + '/' + str(houseID) + '/' + str(roomID)
        path_url = self.storageAddress[0] + "/"+self.storageAddress[1]+"/"+reqPath
        resp = urllib2.urlopen(path_url).read()
        if not resp.status == 200:
            raise Exception("Did not receive response")
        else:
            # This creates a list of dictionaries from the JSON

            """
            Demo: Extract from Snapshot
                    Extracting from snapshot string:
                    [{"Enabled":false,"State":0,"ID":{"HouseID":101,"RoomID":3,"DeviceID":1},"LastUp
                    date":"2015-05-03T23:22:44.3282415Z","Name":null},{"Enabled":true,"Value":1.0,"I
                    D":{"HouseID":101,"RoomID":3,"DeviceID":2},"LastUpdate":"2015-05-03T23:22:44.343
                    2424Z","Name":null},{"Enabled":false,"Value":0.0,"ID":{"HouseID":101,"RoomID":3,
                    "DeviceID":3},"LastUpdate":"2015-05-03T23:22:45.2762958Z","Name":null}]
            """

            json_list = json.loads(resp)

            for x in json_list:
                boolValue = x["Enabled"]
                if boolValue == "false":
                    boolValue = False
                elif boolValue == "true":
                    boolValue = True

                # x is a dictionary
                ID = x["ID"]
                # ID is a dictionary
                device = ID["DeviceID"]
                #device contains the Device ID
                devapiu.updateDeviceState(device,boolValue)

    def findMatchingRoom(self, userid, lat, lon, alt):
        conn = httplib.HTTPConnection(self.storageAddress[0], self.storageAddress[1])
        reqMethod = 'GET'
        reqPath = 'BU/' + str(userid)
        
        #First, try to get the user information.
        conn.request(reqMethod, reqPath)
        resp = conn.getresponse()
        body = resp.read()
        if (not resp.status == 200):
            raise KeyError('That userID does not exist.')
            return
        body = json.loads(body)
        
        print 'Debug: '
        print body
        
        matchingRoom = None
        for houseID in body['houseIDs']:
            print 'Debug: house ' + str(houseID)
            reqMethod = 'GET'
            reqPath = 'HR/' + str(houseID)
            conn.request(reqMethod, reqPath)
            resp = conn.getresponse()
            if not resp.status == 200:
                continue
            try:
                oneHouseBody = json.loads(resp.read())
            except (ValueError, KeyError):
                continue
            #Looping for all rooms...
            for roomID in oneHouseBody['roomIDs']:
                print 'Debug: room ' + str(roomID)
                #Trying to get room info. Should be replaced once that library is ready.
                reqMethod = 'GET'
                reqPath = 'BR/'+str(houseID)+'/'+str(roomID)
                conn.request(reqMethod, reqPath)
                resp = conn.getresponse()
                if not resp.status == 200:
                    continue
                
                respMSG = resp.read()
                print respMSG
                #Check if room matches or not.
                try:
                    if isInRoom(respMSG, lat, lon, alt):
                        matchingRoom = (houseID, roomID)
                        return matchingRoom
                        break
                except (ValueError, KeyError):
                    continue

#Utility function: takes a room blob from persistent storage, and checks if the coordinates
#are within it.
def isInRoom(roomBlob, lat, lon, alt):
    roomJson = json.loads(roomBlob)
    if (alt - roomJson['alt'] > 10 or alt < roomJson['alt']):
        return False
    p1 = Point(roomJson['corner1'][1], roomJson['corner1'][0])
    p2 = Point(roomJson['corner2'][1], roomJson['corner2'][0])
    p3 = Point(roomJson['corner3'][1], roomJson['corner3'][0])
    p4 = Point(roomJson['corner4'][1], roomJson['corner4'][0])
    pn = Point(lon, lat)
    poly = Polygon(p1, p2, p3, p4)
    return poly.encloses_point(pn)


