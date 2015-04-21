#============================================================================
#Author - Sumit Kumar (timus@vt.edu)
#Date - 04/19/2015
#Purpose: To populate the database.
#============================================================================

import requests
import httplib
import json

FUNCTION_TYPES = { 'get' : 'GET', 'post' : 'POST'}
STATUS_CODES = { 'OK': 200, 'Bad_Request' : 400, 'Uunauthorized_Access' : 401,\
            'Resource_Not_Found' : 404, 'Internal_Server_Error' : 500, 'Not_Implemented' : 501}

class populateDB():

    userID = ""
    houseID = ""
    roomID = ""
    deviceID = ""

    def __init__(self, ipAddress='172.31.26.85', extention=8080):
        try:
            self.conn = httplib.HTTPConnection(ipAddress, extention)

        except Exception as e:
            print e.message

    def populateDB(self):
        try:
            """Create a user"""

            self.conn.request(FUNCTION_TYPES['post'], 'U/')
            response = self.conn.getresponse()

            if response.status != STATUS_CODES['OK']:
                raise Exception("Failed to create user.")
            else:
                self.userID = response.read()
                print "User created successfully with ID  " + self.userID

            """Create a house"""
            self.conn.request(FUNCTION_TYPES['post'], 'H/')
            response = self.conn.getresponse()
            if response.status != STATUS_CODES['OK']:
                raise Exception("Failed to create house.")
            else:
                self.houseID = response.read()
                print "House created successfully with ID  " + self.houseID

            #Update blob for house
            data = json.dumps({"houseID": self.houseID, "name": "testName"})
            self.conn.request(FUNCTION_TYPES['post'], 'UH/'+self.houseID+"/",data)
            response = self.conn.getresponse()
            if response.status != STATUS_CODES['OK']:
                raise Exception("Failed to update blob for house.")

            #Update blob for user
            data = json.dumps({"userID": self.userID, "Password":"testPassword", "houseIDs": self.houseID })
            self.conn.request(FUNCTION_TYPES['post'], 'UU/'+self.userID+"/",data)
            response = self.conn.getresponse()
            if response.status != STATUS_CODES['OK']:
                raise Exception("Failed to update blob for user.")

            """Create a room"""
            self.conn.request(FUNCTION_TYPES['post'], 'R/'+self.houseID+"/")
            response = self.conn.getresponse()
            if response.status != STATUS_CODES['OK']:
                raise Exception("Failed to create room.")
            else:
                self.roomID = response.read()
                print "Room created successfully with ID  " + self.roomID

            #Update blob for room
            data = json.dumps({"roomID": self.roomID, "type":"Simulated", "name": "Living","x":50, "y":50 })
            self.conn.request(FUNCTION_TYPES['post'], 'UR/'+self.houseID+"/"+self.roomID+"/",data)
            response = self.conn.getresponse()
            if response.status != STATUS_CODES['OK']:
                raise Exception("Failed to update blob for room.")

            """Create a device"""

            self.conn.request(FUNCTION_TYPES['post'], 'D/'+self.houseID+"/"+self.roomID+"/"+"1/")
            response = self.conn.getresponse()
            if response.status != STATUS_CODES['OK']:
                raise Exception("Failed to create device")
            else:
                self.deviceID = response.read()
                print "Device created successfully with ID  " + self.deviceID

            # Update blob for Device
            data = json.dumps({ "houseID":self.houseID, "roomID":self.roomID, "deviceID":self.deviceID, "Name": "testDevice" })
            self.conn.request(FUNCTION_TYPES['post'], 'UD/'+self.houseID+"/"+self.roomID+"/"+self.deviceID+"/",data)
            response = self.conn.getresponse()
            if response.status != STATUS_CODES['OK']:
                raise Exception("Failed to update blob for device")

        except Exception as e:
            print e.message


if __name__ == '__main__':
    populateDB.populateDB()
