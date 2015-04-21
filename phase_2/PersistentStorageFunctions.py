#Functions for Calls to and from the Persistent Storage
#Contributors : Luke Lapham, Sumit Kumar
#Date : 3/30/2015
#Last modified: 4/20/2015

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import requests
import json
import httplib
import urllib

FUNCTION_TYPES = { 'get' : 'GET', 'post' : 'POST'}

class PersistentStorageFunctions():
    def __init__(self, ipAddress='172.31.26.85', extention=8080):
	    #COnnection to the server is established
        self.conn = httplib.HTTPConnection(ipAddress, extention)
		
    def getAllItemsInHouse(self, houseID='testHouseID'):
        self.conn.request(FUNCTION_TYPES['get'],'HD/' + houseID + '/')
        return self.conn.getresponse()

    def getAllItemsInRoom(self, houseID='testHouseID', roomID='testRoomID'):
        self.conn.request(FUNCTION_TYPES['get'],'RD/' + houseID + '/' + roomID + '/')
        return self.conn.getresponse()

    def getHouseDeviceType(self, houseID='testHouseID', deviceTypeID='testDeviceID'):
        self.conn.request(FUNCTION_TYPES['get'],'HT/' + houseID + '/' + deviceTypeID + '/')
        return self.conn.getresponse()
		
    def getHouseRoomDeviceType(self, houseID='testHouseID', roomID='testRoomID', deviceTypeID='testDeviceID'):
        self.conn.request(FUNCTION_TYPES['get'],'RT/' + houseID + '/' + roomID + '/' + deviceTypeID + '/')
        return self.conn.getresponse()

    #Note: since each house can have more than one user it may not make sense to return a signle user ID
	#based upon a house ID.
    def getUserInformationHouse(self, houseID='testHouseID'):
        self.conn.request(FUNCTION_TYPES['get'], 'UI/' + houseID)
        return self.conn.getresponse()

    def getUserInformationUserID(self, userID='testUserID'):
        self.conn.request(FUNCTION_TYPES['get'], 'UI/' + userID)
        return self.conn.getresponse()        

    #The HouseID and roomID are optional fields.
    def getAllLogEntries(self, userID='testUserID', timeframe='testTimeFrame',\
	    houseID= None, roomID= None):
		
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
		
    def getAllLogEntriesDeviceType(self, userID='testUserID', timeframe='testTimeFrame',\
        deviceType='testDeviceType', houseID='testRoomID', roomID='testRoomdID'):
    
        tempKey = 'AT/' + userID + '/' + timeframe + '/' + deviceType + '/' + houseID + '/' + roomID + '/'
        self.conn.request(FUNCTION_TYPES['get'], tempKey)
        return self.conn.getresponse()
		
    def getAllLogEntriesDeviceID(self, userID='testUserID', timeframe='testTimeFrame',\
        deviceID='testDeviceID', houseID='testRoomID', roomID='testRoomdID'):
    
        tempKey = 'AI/' + userID + '/' + timeframe + '/' + deviceID + '/' + houseID + '/' + roomID + '/'
        self.conn.request(FUNCTION_TYPES['get'], tempKey)
        return self.conn.getresponse()
		
    def getAllComputerByLocation(self, userID='testUserID', timeframe='testTimeFrame',\
        houseID='testRoomID', roomID='testRoomdID'):
		
        tempKey = 'CL/' + userID + '/' + timeframe + '/' + houseID + '/' + roomID + '/'
        self.conn.request(FUNCTION_TYPES['get'], tempKey)
        return self.conn.getresponse()
		
    def getAllComputerByType(self, userID='testUserID', timeframe='testTimeFrame',\
	    deviceType='testDeviceType', houseID='testRoomID', roomID='testRoomdID'):

        tempKey = 'CT/' + userID + '/' + timeframe + '/' + deviceType + '/' + houseID + '/' + roomID + '/'
        self.conn.request(FUNCTION_TYPES['get'], tempKey)
        return self.conn.getresponse()
		
    def getComputerbyDeviceID(self, userID='testUserID', timeframe='testTimeFrame',\
        deviceID='testDeviceID', houseID='testRoomID', roomID='testRoomdID'):

        tempKey = 'CI/' + userID + '/' + timeframe + '/' + deviceID + '/' + houseID + '/' + roomID + '/'
        self.conn.request(FUNCTION_TYPES['get'], tempKey)
        return self.conn.getresponse()
		
    def postDevice(self, houseID,roomID, deviceType):
        self.conn.request(FUNCTION_TYPES['post'], 'D/' + houseID +\
            '/' + roomID + '/' + deviceType + '/')
        return self.conn.getresponse()
		
    def postRoom(self, houseID):
        self.conn.request(FUNCTION_TYPES['post'], 'R/' + houseID +"/")
        return self.conn.getresponse()
		
    def postHouse(self):
        self.conn.request(FUNCTION_TYPES['post'], 'H/')
        return self.conn.getresponse()
		
    def postUser(self):
        self.conn.request(FUNCTION_TYPES['post'], 'U/')
        return self.conn.getresponse()