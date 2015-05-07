#Functions for Calls to and from the Persistent Storage
#Contributors : Luke Lapham
#Date : 3/30/2015

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import httplib
import urllib
import logging

FUNCTION_TYPES = { 'get' : 'GET', 'post' : 'POST'}

class PersistentStorageFunctions():
    def __init__(self, storageAddress='172.31.26.85', port=0):
        #COnnection to the server is established
        self.conn = httplib.HTTPConnection(storageAddress, port)
        self.logger = logging.getLogger("PersistentStorageFunctionsLogger.log")
        self.logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        fh = logging.FileHandler('getRequests.log', mode='w')
        fh.setLevel(logging.DEBUG) 
        self.logger.addHandler(fh)

    def getRoomsInHouse(self, houseID=123):
        try:
            path = "/HR/" + str(houseID) + "/" 
            self.logger.debug(path)   
            self.conn.request("GET", path)
            response = self.conn.getresponse()
            print response.status
            parsed = json.loads(response.read())
            return parsed
        except:
            print "Error with getRoomsInHouse request"
            raise
        
    def getDevicesInHouse(self, houseID=123):
        try:
            path = "/HD/" + str(houseID) + "/" 
            self.logger.debug(path)   
            self.conn.request("GET", path)
            response = self.conn.getresponse()
            print response.status
            parsed = json.loads(response.read())
            return parsed
        except:
            print "Error with getDevicesInHouse request"
            raise

    def getDevicesInRoom(self, houseID=123, roomID=123):
        try:    
            path = "/RD/" + str(houseID) + "/" + str(roomID) + "/"
            self.logger.debug(path)       
            self.conn.request("GET", path)
            response = self.conn.getresponse()
            print response.status
            parsed = json.loads(response.read())
            return parsed
        except:
            print "Error with getDevicesInRoom request"
            raise

            print "Error with  request"
    def getDevice(self, houseID=123, roomID=132, deviceID=123):
        try:    
            path = "/DD/" + str(houseID) + "/" + str(roomID) + "/" + str(deviceID) + "/"
            self.logger.debug(path)     
            self.conn.request("GET", path)
            response = self.conn.getresponse()
            print response.status
            parsed = json.loads(response.read())
            return parsed
        except:
            print "Error with getDevice request"
            raise
        
    def getDevicesInHouseOfType(self, houseID='testHouseID', deviceType='testDeviceID'):
        try:    
            path = "/HT/" + str(houseID) + "/" + str(deviceType) + "/"
            self.logger.debug(path)      
            self.conn.request("GET", path)
            response = self.conn.getresponse()
            print response.status
            parsed = json.loads(response.read())
            return parsed
        except:
            print "Error with getDevicesInHouseOfType request"
            raise

    #Note: since each house can have more than one user it may not make sense to return a signle user ID
    #based upon a house ID.
    def getDevicesInRoomOfType(self, houseID = 'testHouseID', roomID = 'testRoomID', deviceType = 'light'):
        try:    
            path = "/RT/" + str(houseID) + "/" + str(roomID) + "/" + str(deviceType) + "/"
            self.logger.debug(path)     
            self.conn.request("GET", path)
            response = self.conn.getresponse()
            print response.status
            parsed = json.loads(response.read())
            return parsed
        except:
            print "Error with getDevicesInRoomOfType request"
            raise

    def getUserInfo(self, userID = 'testUserID'):
        try:    
            path = "/BU/" + str(userID) + "/"
            self.logger.debug(path) 
            self.conn.request("GET", path)
            response = self.conn.getresponse()
            print response.status
            parsed = json.loads(response.read())
            return parsed
        except:
            print "Error with getUserInfo request"
            raise       

    def getRoomInfo(self, houseID = 'testHouseID',roomID = 'testRoomID'):
        try:    
            path = "/BR/" + str(houseID) + "/" + str(roomID) + "/"
            self.logger.debug(path)      
            self.conn.request("GET", path)
            response = self.conn.getresponse()
            print response.status
            parsed = json.loads(response.read())
            return parsed
        except:
            print "Error with getRoomInfo request" 
            raise
        
    def getDeviceInfo(self, houseID = 'testHouseID', roomID = 'testRoomID', deviceID = 'testDeviceID'):
        try:    
            path = "/BD/" + str(houseID) + "/" + str(roomID) + "/" + str(deviceID) + "/"
            self.logger.debug(path)     
            self.conn.request("GET", path)
            response = self.conn.getresponse()
            print response.status
            parsed = json.loads(response.read())
            return parsed
        except:
            print "Error with getDeviceInfo request"
            raise
        
    def getAuthentication(self, userName='testUserName', pw = 'testPW'):
        try:    
            path = "/IU/" + str(userName) + "/" + str(pw) + "/"
            self.logger.debug(path)      
            self.conn.request("GET", path)
            response = self.conn.getresponse()
            print response.status
            parsed = json.loads(response.read())
            return parsed
        except:
            print "Error with getAuthentication request"
            raise
        
    def getUserDeviceToken(self, userID='testUserID'):
        try:    
            path = "/TU/" + str(userID) + "/"
            self.logger.debug(path)     
            self.conn.request("GET", path)
            response = self.conn.getresponse()
            print response.status 
            parsed = json.loads(response.read())
            return parsed
        except:
            print "Error with getUserDeviceToken request"
            raise

    def getUserActions(self, userID='testUserID', timeFrame='testTimeFrame', houseID='testHouseID', roomID='testRoomID', deviceID='testDeviceID', deviceType = '0'):
        try:    
            path = "/AL/" + str(userID) + "/" + str(timeFrame) + "/" 
            if houseID != 'testHouseID':
                path = path + str(houseID) + "/"
            else:
                path = path + "0/"
            if roomID != 'testRoomID':
                path = path + str(roomID) + '/'
            else:
                path = path + "0/"
            if deviceID != "testDeviceID":
                path = path + str(deviceID) + '/'
            else:
                path = path + "0/"
            if deviceType != '0':
                path = path + deviceType + '/'
            else:
                path = path + "0/"
            self.logger.debug(path)     
            self.conn.request("GET", path)
            response = self.conn.getresponse()
            print response.status 
            parsed = json.loads(response.read())
            return parsed
        except:
            print "Error with getUserActions request"
            raise


    def getComputerActions(self, compID='testCompID', timeFrame='testTimeFrame', houseID='testHouseID', roomID='testRoomID', deviceID='testDeviceID', deviceType = '0'):
        try:    
            path = "/CL/" + str(compID) + "/" + str(timeFrame) + "/"
            if houseID != 'testHouseID':    
                path = path + str(houseID) + '/'
            else:
                path = path + "0/"
            if roomID != 'testRoomID':
                path = path + str(roomID) + '/'
            else:
                path = path + "0 /"
            if deviceID != "testDeviceID":
                path = path + str(deviceID) + '/'
            else:
                path = path + "0/"
            if deviceType != '0':
                path = path + deviceType + '/'
            else:
                path = path + "0/"
            self.logger.debug(path)
            self.conn.request("GET", path)
            response = self.conn.getresponse()
            print response.status
            parsed = json.loads(response.read())
            return parsed
        except:
            print "Error with getComputerActions request"
            raise

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