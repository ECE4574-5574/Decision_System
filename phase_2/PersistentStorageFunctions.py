#Functions for Calls to and from the Persistent Storage
#Contributors : Luke Lapham, Sumit Kumar
#Date : 3/30/2015
#Last modified: 4/20/2015

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import requests
import json
import httplib
import urllib
import logging

FUNCTION_TYPES = { 'get' : 'GET', 'post' : 'POST'}

class PersistentStorageFunctions():
    def __init__(self, storageAddress='172.31.26.85', extention=0):
        #COnnection to the server is established
        self.url = "http://" + str(storageAddress)
        if(extention != 0):
            self.url = self.url + ':' + str(extention) + '/'
        else: 
        self.url = self.url + '/'
        self.logger = logging.getLogger('ServerRequestLogger')
        loggerhandler = logging.FileHandler('ServerRequestLogFile', mode = 'a')
        serverformatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        serverrequestloggerhandler.setFormatter(serverformatter)
        self.serverrequestlogger.addHandler(serverrequestloggerhandler)
        self.serverrequestlogger.setLevel(logging.INFO)
        
    def getDevicesInHouse(self, houseID='testHouseID'):
        try:    
            request = self.url + 'HD/' + str(houseID) + '/'
            print request
            r = requests.get(request)
            print r.status_code
            parsed = json.loads(r.json())
            return parsed
        except:
            print "Error with request"

    def getDevicesInRoom(self, houseID='testHouseID', roomID='testRoomID'):
        try:    
            request = self.url + 'RD/' + str(houseID) + '/' + str(roomID) + '/'
            print request
            r = requests.get(request)
            print r.status_code
            parsed = json.loads(r.json())
            return parsed
        except:
            print "Error with request"

    def getDevice(self, houseID='testHouseID', roomID='testRoomID', deviceTypeID='testDeviceID'):
        try:    
            request = self.url + 'DD/' + str(houseID) + '/' + str(roomID) + '/' + str(deviceTypeID) + '/'
            print request
            r = requests.get(request)
            print r.status_code
            parsed = json.loads(r.json())
            return parsed
        except:
            print "Error with request"
        
    def getDevicesInHouseOfType(self, houseID='testHouseID', deviceType='light'):
        try:    
            request = self.url + 'HT/' + str(houseID) + '/' + str(deviceType) + '/'
            print request
            r = requests.get(request)
            print r.status_code
            parsed = json.loads(r.json())
            return parsed
        except:
            print "Error with request"

    #Note: since each house can have more than one user it may not make sense to return a signle user ID
    #based upon a house ID.
    def getDevicesInRoomOfType(self, houseID = 'testHouseID', roomID = 'testRoomID', deviceType = 'light'):
        try:    
            request = self.url + 'RT/' + str(houseID) + '/' + str(roomID) + '/' + str(deviceType) + '/'
            print request
            r = requests.get(request)
            print r.status_code
            parsed = json.loads(r.json())
            return parsed
        except:
            print "Error with request"
    #TODO: UPDATE COMMENTS
    def getUserInfo(self, userID = 'testUserID'):
        try:    
            request = self.url + 'BU/' + str(userID) + '/'
            print request
            r = requests.get(request)
            print r.status_code
            parsed = json.loads(r.json())
            return parsed
        except:
            print "Error with request"       

    #The HouseID and roomID are optional fields.
    def getRoomInfo(self, houseID = 'testHouseID',roomID = 'testRoomID'):
        try:    
            request = self.url + 'BR/' + str(houseID) + '/' + str(roomID) + '/'
            print request
            r = requests.get(request)
            print r.status_code
            parsed = json.loads(r.json())
            return parsed
        except:
            print "Error with request" 
        
    def getDeviceInfo(self, houseID = 'testHouseID', roomID = 'testRoomID', deviceID = 'testDeviceID'):
        try:    
            request = self.url + 'BD/' + str(houseID) + '/' + str(roomID) + '/' + str(deviceID) + '/'
            print request
            r = requests.get(request)
            print r.status_code
            parsed = json.loads(r.json())
            return parsed
        except:
            print "Error with request"
        
    def getAuthentication(self, userName='testUserName', pw = 'testPW'):
        try:    
            request = self.url + 'IU/' + str(userName) + '/' + str(pw) + '/'
            print request
            r = requests.get(request)
            print r.status_code
            parsed = json.loads(r.json())
            return parsed
        except:
            print "Error with request"
        
    def getUserDeviceToken(self, userID='testUserID'):
        try:    
            request = self.url + 'TU/' + str(userID) + '/'
            print request
            r = requests.get(request)
            print r.status_code
            parsed = json.loads(r.json())
            return parsed
        except:
            print "Error with request"

    def getUserActions(self, userID='testUserID', timeFrame='testTimeFrame', houseID='testHouseID', roomID='testRoomID'):
        try:    
            request = self.url + 'AL/' + str(userID) + '/' + str(timeFrame) + '/'
            if houseID != 'testHouseID':
                request = request + houseID + '/'
            else:
                request = reqest + '0' + '/'
            if roomID != 'testRoomID':
                request = request + roomID + '/'
            else:
                request = reqest + '0' + '/'
            print request
            r = requests.get(request)
            print r.status_code
            parsed = json.loads(r.json())
            return parsed
        except:
            print "Error with request"

    def getUserActionsDeviceType(self, userID='testUserID', timeFrame='testTimeFrame',\
        deviceType='light', houseID='testRoomID', roomID='testRoomdID'):
        try:    
            request = self.url + 'AT/' + str(userID) + '/' + str(timeFrame) + '/' + str(deviceType) + '/' + str(houseID) + '/'
            if roomID != 'testRoomID':
                request = request + roomID + '/'
            else:
                request = reqest + '0' + '/'
            print request
            r = requests.get(request)
            print r.status_code
            parsed = json.loads(r.json())
            return parsed
        except:
            print "Error with request"

    def getUserActionsDeviceID(self, userID='testUserID', timeFrame='testTimeFrame', deviceID='testDeviceID', houseID = 'testHouseID', roomID = 'testRoomID'):
        try:    
            request = self.url + 'AI/' + str(userID) + '/' + str(timeFrame) + '/' + str(deviceID) + '/' + str(houseID) + '/'
            if roomID != 'testRoomID':
                request = request + roomID + '/'
            else:
                request = reqest + '0' + '/'
            print request
            r = requests.get(request)
            print r.status_code
            parsed = json.loads(r.json())
            return parsed
        except:
            print "Error with request"

    def getComputerActions(self, compID='testCompID', timeFrame='testTimeFrame', houseID='testHouseID', roomID='testRoomID'):
        try:    
            request = self.url + 'CL/' + str(compID) + '/' + str(timeFrame) + '/'
            if houseID != 'testHouseID':    
                request = request + houseID + '/'
            else:
                request = reqest + '0' + '/'
            if roomID != 'testRoomID':
                request = request + roomID + '/'
            else:
                request = reqest + '0' + '/'
            print request
            r = requests.get(request)
            print status_code
            parsed = json.loads(r.json())
            return parsed
        except:
            print "Error with request"

    def getCompActionsDeviceType(self, compID='testUserID', timeFrame='testTimeFrame',
        deviceType='light', houseID='testRoomID', roomID='testRoomdID'):
        try:    
            request = self.url + 'CT/' + str(userID) + '/' + str(timeFrame) + '/' + str(deviceType) + '/' + str(houseID) + '/'
            if houseID != 'testHouseID':    
                request = request + houseID + '/'
            else:
                request = reqest + '0' + '/'
            if roomID != 'testRoomID':
                request = request + roomID + '/'
            else:
                request = reqest + '0' + '/'
            print request
            r = requests.get(request)
            print r.status_code
            parsed = json.loads(r.json())
            return parsed
        except:
            print "Error with request"

    def getCompActionsDeviceID(self, compID='testUserID', timeFrame='testTimeFrame',
        deviceID='testDeviceID', houseID='testRoomID', roomID='testRoomdID'):
        try:    
            request = self.url + 'CT/' + str(userID) + '/' + str(timeFrame) + '/' + str(deviceID) + '/' + str(houseID) + '/'
            if roomID != 'testRoomID':
                request = request + roomID + '/'
            else:
                request = reqest + '0' + '/'
            print request
            r = requests.get(request)
            print r.status_code
            parsed = json.loads(r.json())
            return parsed
        except:
            print "Error with request"    

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

thing = PersistentStorageFunctions()