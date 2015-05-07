#Tests the functions for PersistentStorageFunctions
#Contributors : Luke Lapham
#Date : 3/30/2015
#
#Note: This test assumes that you have a persistent storage server running on your desktop.
import unittest
import PersistentStorageFunctions as PSF

STATUS_CODES = { 'OK': 200, 'Bad_Request' : 400, 'Uunauthorized_Access' : 401,\
            'Resource_Not_Found' : 404, 'Internal_Server_Error' : 500, 'Not_Implemented' : 501}

class PersistentStorageFunctionsTest(unittest.TestCase):
    def setUp(self):
        self.API = PSF.PersistentStorageFunctions()
		
    def testGetFunctionsDefaults(self):
        resp = self.API.getAllItemsInHouse('houseID')
        self.assertEqual(resp.status, STATUS_CODES['OK'])
		
        resp = self.API.getAllItemsInRoom('houseID', 'roomID')
        self.assertEqual(resp.status, STATUS_CODES['OK'])
		
        resp = self.API.getHouseDeviceType('houseID', 'deviceTypeID')
        self.assertEqual(resp.status, STATUS_CODES['OK'])
		
        resp = self.API.getHouseRoomDeviceType('houseID', 'roomID', 'deviceTypeID')
        self.assertEqual(resp.status, STATUS_CODES['OK'])
		
        resp = self.API.getUserInformationHouse('houseID')
        self.assertEqual(resp.status, STATUS_CODES['OK'])
		
        resp = self.API.getUserInformationUserID('userID')
        self.assertEqual(resp.status, STATUS_CODES['OK'])
		
        resp = self.API.getAllLogEntries('userID', 'testTimeFriame')
        self.assertEqual(resp.status, STATUS_CODES['OK'])
		
        resp = self.API.getAllLogEntriesDeviceType('testuserID', 'testtimeframe',\
                                                   'testdeviceType', 'testhouseID', 'testroomID')
        self.assertEqual(resp.status, STATUS_CODES['OK'])
		
        resp = self.API.getAllLogEntriesDeviceID('testuserID', 'testtimeframe',\
                                                   'testdeviceID', 'testhouseID', 'testroomID')
        self.assertEqual(resp.status, STATUS_CODES['OK'])
		
        resp = self.API.getAllComputerByLocation('testuserID', 'testtimeframe', 'testhouseID', 'testroomID')
        self.assertEqual(resp.status, STATUS_CODES['OK'])
		
        resp = self.API.getAllComputerByType('testuserID', 'testtimeframe', 'testdeviceType',\
                                            'testhouseID', 'testroomID')
        self.assertEqual(resp.status, STATUS_CODES['OK'])
		
        resp = self.API.getComputerbyDeviceID('testuserID', 'testtimeframe', 'testdeviceID', 'testhouseID',\
                                                'testroomID')
        self.assertEqual(resp.status, STATUS_CODES['OK'])
		
    def testPostFunctionsDefaults(self):
        resp = self.API.postDevice('testHouseID', '1.0', 'roomID', 'deviceID')
        self.assertEqual(resp.status, STATUS_CODES['OK'])
		
        resp = self.API.postRoom('testHouseID', '1.0', 'roomID')
        self.assertEqual(resp.status, STATUS_CODES['OK'])
		
        resp = self.API.postHouse('houseID')
        self.assertEqual(resp.status, STATUS_CODES['OK'])
		
        resp = self.API.postUser('userID')
        self.assertEqual(resp.status, STATUS_CODES['OK'])
		
if __name__ == '__main__':
    unittest.main()
