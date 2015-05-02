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

#This monkey-patch is NECESSARY to make sympy work.
#It's a dangerous hack, but we're only using some limited parts of sympy...
def my_unicode_escape_decode(x):
    return x
codecs.unicode_escape_decode = my_unicode_escape_decode
from sympy import Point, Polygon
import decisions
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
	def sendUserMessage(message, type):
		#Set up JSON message
		if (type == "error"):
			msg = { 
					"Type":	 "error",
					"Error": message 
				  }
	
			elif (type == "info"):
				msg = {
						"Type":        "information",
						"Information": message
					  }
			elif (type == "both"):
				msg = {
						"Type":        "both",
						"Error":   	   msg[0],
						"Information": msg[1]
					  } 
			serverConn = httplib.HTTPConnection(deviceBase)
			data = json.dumps(msg)
			requestPath = 'POST', 'api/decision/app'
			serverConn.request = ('POST', 'api/decision/app', data)
			serverResponse = serverConn.getresponse()
			print serverResponse.status
			print serverResponse.read()
			line = "Location Decision " + str(self.locationDecisionCount) + ":\n" + "Data sent to persistent storage: " + str(data) + "\nRequest Path: " + str(requestPath) + "\nRequest Response: " + str(serverResponse.status) + "\n"
			self.logger.debug(line)

	#Method for sending the decision about the device to the server api
	def sendDeviceDecision(self, decision, message):
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


