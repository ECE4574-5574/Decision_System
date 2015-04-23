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
    def __init__(self, ipAddress='localhost', extention=8080):
	    #COnnection to the server is established
        self.conn = httplib.HTTPConnection(ipAddress, extention)
		
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

	#Note: since each house can have more than one user it may not make sense to return a signle user ID
	#based upon a house ID.
    def getUserInformationHouse(self, houseID):
        self.conn.request(FUNCTION_TYPES['get'], 'UI/' + houseID)
        return self.conn.getresponse()

    def getUserInformationUserID(self, userID):
        self.conn.request(FUNCTION_TYPES['get'], 'UI/' + userID)
        return self.conn.getresponse()        

    #The HouseID and roomID are optional fields.
    def getAllLogEntries(self, userID, timeframe,houseID= None, roomID= None):
		
        if houseID is None:
            tempKey = 'AL/' + userID + '/' + timeframe + '/'
            self.conn.request(FUNCTION_TYPES['get'], tempKey)		
        elif roomID is None:
            tempKey = 'AL/' + userID + '/' + timeframe + '/' + houseID + '/'
            self.conn.request(FUNCTION_TYPES['get'], tempKey)		
        else:
            tempKey = 'AL/' + userID + '/' + timeframe + '/' + houseID + '/' + roomID
            self.conn.request(FUNCTION_TYPES['get'], tempKey)
        return self.conn.getresponse()
		
    def getAllLogEntriesDeviceType(self, userID, timeframe, deviceType, houseID, roomID):
    
        tempKey = 'AT/' + userID + '/' + timeframe + '/' + deviceType + '/' + houseID + '/' + roomID + '/'
        self.conn.request(FUNCTION_TYPES['get'], tempKey)
        return self.conn.getresponse()
		
    def getAllLogEntriesDeviceID(self, userID, timeframe, deviceID, houseID, roomID):
    
        tempKey = 'AI/' + userID + '/' + timeframe + '/' + deviceID + '/' + houseID + '/' + roomID + '/'
        self.conn.request(FUNCTION_TYPES['get'], tempKey)
        return self.conn.getresponse()
		
    def getAllComputerByLocation(self, userID, timeframe, houseID, roomID):
		
        tempKey = 'CL/' + userID + '/' + timeframe + '/' + houseID + '/' + roomID + '/'
        self.conn.request(FUNCTION_TYPES['get'], tempKey)
        return self.conn.getresponse()
		
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