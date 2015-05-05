#Functions for Calls to and from the Persistent Storage
#Contributors : Luke Lapham
#Date : 3/30/2015

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import requests
import json
import httplib
import urllib

FUNCTION_TYPES = { 'get' : 'GET', 'post' : 'POST'}

class PersistentStorageFunctions():
    def __init__(self, ipAddress = 'localhost', extention = 8080):
	    #COnnection to the server is established
        self.conn = httplib.HTTPConnection(ipAddress, extention)
		
	###### 2.0 Requests for devices #####
    def getRoomIDs(self, houseID):
        self.conn.request(FUNCTION_TYPES['get'],'HR/' + houseID + '/')
        return self.conn.getresponse()
	
    def getAllItemsInHouse(self, houseID):
        self.conn.request(FUNCTION_TYPES['get'],'HD/' + houseID + '/')
        return self.conn.getresponse()

    def getAllItemsInRoom(self, houseID, roomID):
        self.conn.request(FUNCTION_TYPES['get'],'RD/' + houseID + '/' + roomID + '/')
        return self.conn.getresponse()

    def getHouseDeviceType(self, houseID, deviceTypeID):
        self.conn.request(FUNCTION_TYPES['get'],'HT/' + houseID + '/' + deviceTypeID + '/')
        return self.conn.getresponse()
		
    def getHouseRoomDeviceType(self, houseID, roomID, deviceTypeID):
        self.conn.request(FUNCTION_TYPES['get'],'RT/' + houseID + '/' + roomID + '/' + deviceTypeID + '/')
        return self.conn.getresponse()
		
    def getDiviceInSpecficRoom(self, houseID, roomID, deviceID):
        self.conn.request(FUNCTION_TYPES['get'],'DD/' + houseID + '/' + roomID + '/' + deviceID + '/')
        return self.conn.getresponse()
	###### End Requests for devices. ######
	
	###### 3.0 Requests for Blobs ######
	
	###### End Requests for Blobs ######
	
	###### 4.0 Requests for Accessing Log Files ######
    #The HouseID and roomID are optional fields.
    def getAllLogEntriesUser(self, userID, timeframe,houseID = None, roomID = None, deviceID = None, deviceType = None):
		
        if houseID is None:
            tempKey = 'AL/' + userID + '/' + timeframe + '/'
            self.conn.request(FUNCTION_TYPES['get'], tempKey)		
        elif roomID is None:
            tempKey = 'AL/' + userID + '/' + timeframe + '/' + houseID + '/'
            self.conn.request(FUNCTION_TYPES['get'], tempKey)		
        elif deviceID is None:
            tempKey = 'AL/' + userID + '/' + timeframe + '/' + houseID + '/' + roomID
            self.conn.request(FUNCTION_TYPES['get'], tempKey)
        elif deviceType is None:
            tempKey = 'AL/' + userID + '/' + timeframe + '/' + houseID + '/' + roomID + '/' + deviceID
            self.conn.request(FUNCTION_TYPES['get'], tempKey)
        else:
            tempKey = 'AL/' + userID + '/' + timeframe + '/' + houseID + '/' + roomID + '/' + deviceID + deviceType
            self.conn.request(FUNCTION_TYPES['get'], tempKey)
        return self.conn.getresponse()
		
    def getAllLogEntriesAI(self, compID, timeframe,houseID = None, roomID = None, deviceID = None, deviceType = None):
        if houseID is None:
            tempKey = 'CL/' + compID + '/' + timeframe + '/'
            self.conn.request(FUNCTION_TYPES['get'], tempKey)		
        elif roomID is None:
            tempKey = 'CL/' + compID + '/' + timeframe + '/' + houseID + '/'
            self.conn.request(FUNCTION_TYPES['get'], tempKey)		
        elif deviceID is None:
            tempKey = 'CL/' + compID + '/' + timeframe + '/' + houseID + '/' + roomID
            self.conn.request(FUNCTION_TYPES['get'], tempKey)
        elif deviceType is None:
            tempKey = 'CL/' + compID + '/' + timeframe + '/' + houseID + '/' + roomID + '/' + deviceID
            self.conn.request(FUNCTION_TYPES['get'], tempKey)
        else:
            tempKey = 'CL/' + compID + '/' + timeframe + '/' + houseID + '/' + roomID + '/' + deviceID + deviceType
            self.conn.request(FUNCTION_TYPES['get'], tempKey)
        return self.conn.getresponse()     
	###### End Requests for accessing Log Files	######
	
    def getAllLogEntriesDeviceType(self, userID, timeframe, deviceType, houseID, roomID):
    
        tempKey = 'AT/' + userID + '/' + timeframe + '/' + deviceType + '/' + houseID + '/' + roomID + '/'
        self.conn.request(FUNCTION_TYPES['get'], tempKey)
        return self.conn.getresponse()
		
    def getAllLogEntriesDeviceID(self, userID, timeframe, deviceID, houseID, roomID):
    
        tempKey = 'AI/' + userID + '/' + timeframe + '/' + deviceID + '/' + houseID + '/' + roomID + '/'
        self.conn.request(FUNCTION_TYPES['get'], tempKey)
        return self.conn.getresponse()
		
    #def getAllComputerByLocation(self, userID, timeframe, houseID, roomID):
	#	
    #    tempKey = 'CL/' + userID + '/' + timeframe + '/' + houseID + '/' + roomID + '/'
    #    self.conn.request(FUNCTION_TYPES['get'], tempKey)
    #    return self.conn.getresponse()
		
    def getAllComputerByType(self, userID, timeframe, deviceType, houseID, roomID):

        tempKey = 'CT/' + userID + '/' + timeframe + '/' + deviceType + '/' + houseID + '/' + roomID + '/'
        self.conn.request(FUNCTION_TYPES['get'], tempKey)
        return self.conn.getresponse()
		
    def getComputerbyDeviceID(self, userID, timeframe, deviceID, houseID, roomID):

        tempKey = 'CI/' + userID + '/' + timeframe + '/' + deviceID + '/' + houseID + '/' + roomID + '/'
        self.conn.request(FUNCTION_TYPES['get'], tempKey)
        return self.conn.getresponse()
		
    def postDevice(self, houseID, version, roomID, deviceID):
        self.conn.request(FUNCTION_TYPES['post'], 'D/' + houseID +\
            '/' + version + '/' + roomID + '/' + deviceID + '/')
        return self.conn.getresponse()
		
    def postRoom(self, houseID, version, roomID):
        self.conn.request(FUNCTION_TYPES['post'], 'R/' + houseID + '/' + version + '/' + roomID + '/')
        return self.conn.getresponse()
		
    def postHouse(self, houseID):
        self.conn.request(FUNCTION_TYPES['post'], 'H/' + houseID + '/')
        return self.conn.getresponse()
		
    def postUser(self, userID):
        self.conn.request(FUNCTION_TYPES['post'], 'U/' + userID + '/')
        return self.conn.getresponse()