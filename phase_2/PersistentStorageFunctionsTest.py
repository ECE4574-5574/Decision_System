#Tests the functions for PersistentStorageFunctions
#Contributors : Luke Lapham, Sumit Kumar
#Date : 3/30/2015
#Last modified: 4/20/2015
#Note: This test assumes that you have a persistent storage server running on your desktop.
import unittest
import PersistentStorageFunctions as PSF
import argparse

'''STATUS_CODES = { 'OK': 200, 'Bad_Request' : 400, 'Unauthorized_Access' : 401,\
            'Resource_Not_Found' : 404, 'Internal_Server_Error' : 500, 'Not_Implemented' : 501}

class PersistentStorageFunctionsTest(unittest.TestCase):
    def setUp(self):
        self.API = PSF.PersistentStorageFunctions()
        
    def testGetFunctionsDefaults(self):
        resp = self.API.getAllItemsInHouse()
        self.assertEqual(resp.status, STATUS_CODES['OK'])
        
        resp = self.API.getAllItemsInRoom()
        self.assertEqual(resp.status, STATUS_CODES['OK'])
        
        resp = self.API.getHouseDeviceType()
        self.assertEqual(resp.status, STATUS_CODES['OK'])
        
        resp = self.API.getHouseRoomDeviceType()
        self.assertEqual(resp.status, STATUS_CODES['OK'])
        
        resp = self.API.getUserInformationHouse()
        self.assertEqual(resp.status, STATUS_CODES['OK'])
        
        resp = self.API.getUserInformationUserID()
        self.assertEqual(resp.status, STATUS_CODES['OK'])
        
        resp = self.API.getAllLogEntries()
        self.assertEqual(resp.status, STATUS_CODES['OK'])
        
        resp = self.API.getAllLogEntriesDeviceType()
        self.assertEqual(resp.status, STATUS_CODES['OK'])
        
        resp = self.API.getAllLogEntriesDeviceID()
        self.assertEqual(resp.status, STATUS_CODES['OK'])
        
        resp = self.API.getAllComputerByLocation()
        self.assertEqual(resp.status, STATUS_CODES['OK'])
        
        resp = self.API.getAllComputerByType()
        self.assertEqual(resp.status, STATUS_CODES['OK'])
        
        resp = self.API.getComputerbyDeviceID()
        self.assertEqual(resp.status, STATUS_CODES['OK'])
        
    def testPostFunctionsDefaults(self):
        resp = self.API.postDevice("testHouseID","testRoomID","1")
        self.assertEqual(resp.status, STATUS_CODES['OK'])
        
        resp = self.API.postRoom("testHouseID")
        self.assertEqual(resp.status, STATUS_CODES['OK'])
        
        resp = self.API.postHouse()
        self.assertEqual(resp.status, STATUS_CODES['OK'])
        
        resp = self.API.postUser()
        self.assertEqual(resp.status, STATUS_CODES['OK'])
        
if __name__ == '__main__':
    unittest.main()'''

argparser = argparse.ArgumentParser()
argparser.add_argument('-t', '--storage', type=str)

args = argparser.parse_args()

DUT = PSF.PersistentStorageFunctions(args.storage, 0)
print "getDevicesInHouse()"
print DUT.getDevicesInHouse()
print '\n'
print "getDevicesInRoom()"
print DUT.getDevicesInRoom()
print '\n'
print "getDevice()"
print DUT.getDevice()
print '\n'
print "getDevicesInHouseOfType()"
print DUT.getDevicesInHouseOfType()
print '\n'
print "getDevicesInRoomOfType()"
print DUT.getDevicesInRoomOfType()
print '\n'
print "getUserInfo()"
print DUT.getUserInfo()
print '\n'
print "getRoomInfo()"
print DUT.getRoomInfo()
print '\n'
print "getDeviceInfo()"
print DUT.getDeviceInfo()
print '\n'
print "getAuthentication()"
print DUT.getAuthentication()
print '\n'
print "getUserDeviceToken()"
print DUT.getUserDeviceToken()
print '\n'
print "getUserActions()"
print DUT.getUserActions()
print '\n'
print "getUserActionsDeviceType()"
print DUT.getUserActionsDeviceType()
print '\n'