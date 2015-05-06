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
import deviceAPIUtils
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
from  System.Collections.Generic import List


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
        self.UserPrevLocation = None 
        

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
			#map user to a house and room
			#the current location should be stored in persistent storage
            CurrentLocation = findMatchingRoom(message['userID'], message['lat'],message['lon'],message['alt'])
            PreviousLocation = self.UserPrevLocation.get(str(message['userID']),None)
            #save new location if user location is not available in   UserPrevLocation
            if ((PreviousLocation is None) and (CurrentLocation is not None)):
                self.UserPrevLocation[str(message['userID'])] = (CurrentLocation[0],CurrentLocation[1])
				#make no decisions, as the previous room data for user was not logged
            if ((PreviousLocation is not None) and (CurrentLocation is not None) and (PreviousLocation != CurrentLocation)):
                #make and log a snapshot of the previous room
				#currently assuminga a dummy device api location
                devInterface = devapi.Interfaces(System.Uri("http://dummy.devapi.not"))
                previousRoomSnapshot = deviceAPIUtils.makeSnapshot(devInterface, PreviousLocation[0], PreviousLocation[1])
                #add call to log the snapshot in persistent storage  
                requestPath = 'PATCH', 'A/' + message['userID'] + '/' + message["time"] + '/' + localUserHouse
                conn.request('PATCH', 'A/' + message['userID'] + '/' + message["time"] + '/' + localUserHouse, previousRoomSnapshot)
				#update the self.UserPrevLocation key value pair with current location
                self.UserPrevLocation[str(message['userID'])] = (CurrentLocation[0],CurrentLocation[1])
				# make a call to the decision algo : Jigar 
                #restoreRoomState(self, userid, roomID, houseID, message)
                restoreRoomState(str(message['userID']), CurrentLocation[1], CurrentLocation[0],message)
				# make a call to the server api : Braedon
                sendUserMessage("Location Changed: Devices Being Set", "information")
            #change the format to the format required by persistent storage     
            #Set up connection to persistent storage
            conn = httplib.HTTPConnection(self.storageAddress[0],self.storageAddress[1])
            #Pass the JSON string to persistent storage
            payload = json.dumps({"action-type":"location-update","action-data":message})
            if (CurrentHouse is None):
                localUserHouse = "NotInAnyHouse"
            else:
                localUserHouse = CurrentHouse
            requestPath = 'PATCH', 'A/' + message['userID'] + '/' + message["time"] + '/' + localUserHouse
            conn.request('PATCH', 'A/' + message['userID'] + '/' + message["time"] + '/' + localUserHouse, payload)
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
            if (str(message["command-string"]) == 'manualDeviceUpdate'):
			    #Set up connection to persistent storage
                conn = httplib.HTTPConnection(self.storageAddress[0], self.storageAddress[1])
                #change the format to the format required by persistent storage
                payload = json.dumps({"action-type":"device state change","action-data":message})
                requestPath = 'PATCH', 'A/' + message['userID'] + '/' + message["time"] + '/' + message["houseID"]+ '/' + message["roomID"] + '/' + message["deviceID"] + '/' + message["deviceType"]
                conn.request('PATCH', 'A/' + message['userID'] + '/' + message["time"] + '/' + message["houseID"]+ '/' + message["roomID"] + '/' + message["deviceID"] + '/' + message["deviceType"], payload)
                response = conn.getresponse()
                print response.status
                print response.read()
                line = "Location Decision " + str(self.locationDecisionCount) + ":\n" + "Data sent to persistent storage: " + str(payload) + "\nRequest Path: " + str(requestPath) + "\nRequest Response: " + str(response.status) + "\n"
                self.locationDecisionCount += 1
                self.logger.debug(line) 
            else:
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
    
    def restoreRoomState(self, userid, roomID, houseID, message):
        conn = httplib.HTTPConnection(self.storageAddress[0], self.storageAddress[1])

        #change time to one week prior to get the snapshot of the state of devices in the room.
        #COMMENTED BLOCK: get the snapshot blob from persistent storage.
        """
        t1 = message["time"]
        temp = t1.split('T', 1)[0]
        temp1 = datetime.datetime.strptime(temp, "\%Y-\%m-\%d")
        sec = t1.split('T', 1)[-1]
        temp2 = temp1 - datetime.timedelta(days=7)
        temp3 = temp2.strftime("%Y %m %d")
        temp4 = temp3.replace(" ","-")
        prev_time = temp4 + 'T' + sec
        
        #GET AL/USERID/TIMEFRAME/HOUSEID*/ROOMID*  Query for each of the actions logged by this user before the provided time.

        reqPath = 'AL/' + str(userid) + message["time"] + message["time"] + '/' + str(houseID) + '/' + str(roomID)
        path_url = self.storageAddress[0] + "/"+self.storageAddress[1]+"/"+reqPath
        resp = urllib2.urlopen(path_url).read()
        if not resp.status == 200:
            raise Exception("Did not receive response")
        else:
            # This creates a list of dictionaries from the JSON
        """
        
        #Instead, use a static string as a proof of concept.
        exampleSnapshotString=\
        """
        [{"Enabled":false,"State":0,"ID":{"HouseID":101,"RoomID":3,"DeviceID":1},"LastUpdate":"2015-05-03T23:22:44.3282415Z","Name":null},
        {"Enabled":true,"Value":1.0,"ID":{"HouseID":101,"RoomID":3,"DeviceID":2},"LastUpdate":"2015-05-03T23:22:44.3482424Z","Name":null},
        {"Enabled":false,"Value":0.0,"ID":{"HouseID":101,"RoomID":3, "DeviceID":3},"LastUpdate":"2015-05-03T23:22:45.2762958Z","Name":null}]
        """
        
        print '\n\n\nExample snapshot:\n' + exampleSnapshotString

        #json_list = json.loads(exampleSnapshotString)
        
        #Commented: Get a list of device instances. Because we're using a static string, to demonstrate I will use a static list of devices.
        #deviceList = devapiInterfaces.getDevices(houseID, roomID)
        
        #Instead, use a static list of devices to demonstrate.
        fan = devapi.CeilingFan(None, None)
        id = devapi.FullID()
        id.HouseID = 101
        id.RoomID = 3
        id.DeviceID = 1
        fan.ID = id
        
        light = devapi.LightSwitch(None, None)
        id = devapi.FullID()
        id.HouseID = 101
        id.RoomID = 3
        id.DeviceID = 2
        light.ID = id
        light.Enabled = True
        
        light2 = devapi.LightSwitch(None, None)
        id = devapi.FullID()
        id.HouseID = 101
        id.RoomID = 3
        id.DeviceID = 3
        light2.ID = id
        
        devlist = List[devapi.Device]()
        devlist.Add(fan)
        devlist.Add(light)
        devlist.Add(light2)
        
        snapshotDict = devapiu.convertSnapshotToDict(exampleSnapshotString)
        
        for device in devlist:
            print '\nExtracted a device snapshot!:'
            deviceSnapshot = devapiu.extractDeviceSnapshot(device, snapshotDict)
            #Interfaces.updateDevice(device, deviceSnapshot, False, False)
            print deviceSnapshot
        
        """
        

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
                
        """

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
					
					
    #Method for sending general information or errors to the user				
    def sendUserMessage(message, msgType):
        #Set up JSON message
        if (msgType == "error"):
            msg = { "Type":"error", "Error": message }	
        elif (msgType == "info"):
            msg = { "Type":  "information", "Information": message}
        elif (msgType == "both"):
            msg = {"Type": "both", "Error": msg[0], "Information": msg[1]} 
        try:	
            serverConn = httplib.HTTPConnection(deviceBase)
            data = json.dumps(msg)
            requestPath = 'POST', 'api/decision/app'
            serverConn.request = ('POST', 'api/decision/app', data)
            serverResponse = serverConn.getresponse()
            print serverResponse.status
            print serverResponse.read()
            line = "Location Decision " + str(self.locationDecisionCount) + ":\n" + "Data sent to persistent storage: " + str(data) + "\nRequest Path: " + str(requestPath) + "\nRequest Response: " + str(serverResponse.status) + "\n"
            self.logger.debug(line)
        except:
            line = 'Error when trying to make a location decision!\nRequest body being handled:\n' + str(message) + '\n'
            self.logger.warning(line)

    #Method for sending the decision about the device to the server api
    def sendDeviceDecision(self, decision, message):
	try: 	
		serverConn = httplib.HTTPConnection(deviceBase)
		data = json.dumps({"deviceID": message['deviceID'], "houseID": message['houseID'], "roomID": message['roomID'], "Decision": decision})
		requestPath = 'POST', 'api/decision/device'
		serverConn.request = ('POST', 'api/decision/device', data)
		serverResponse = serverConn.getresponse()
		print serverResponse.status
		print serverResponse.read()
		line = "Location Decision:\n" + "Data sent to persistent storage: " + str(data) + "\nRequest Path: " + str(requestPath) + "\nRequest Response: " + str(serverResponse.status) + "\n"
		self.logger.debug(line)
	except:
		line = 'Error when trying to make a location decision!\nRequest body being handled:\n' + str(message) + '\n'
		self.logger.warning(line)
			
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


