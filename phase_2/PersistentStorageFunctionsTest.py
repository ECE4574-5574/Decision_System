import unittest
import PersistentStorageFunctions as PSF

STATUS_CODES = { 'OK': 200, 'Bad_Request' : 400, 'Uunauthorized_Access' : 401,\
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
		
if __name__ == '__main__':
    unittest.main()