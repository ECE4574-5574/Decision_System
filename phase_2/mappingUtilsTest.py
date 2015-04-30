import decisionClass as dc
from decisionClass import decisionMaking
import unittest
import logging
import json

class testIsInRoom(unittest.TestCase):
        
    def setUp(self):
        self.BASIC_GOOD_ROOM = {
        'corner1':[37.229874, -80.417754],
        'corner2':[37.229874, -80.417724],
        'corner3':[37.229824, -80.417704],
        'corner4':[37.229824, -80.417754],
        'alt':2080}

    def test_malformedBlob(self):
        malformed = 'this is not JSON'
        self.assertRaises(ValueError, dc.isInRoom, malformed, 0, 0, 0)
    
    def test_missingInformation(self):
        missingKeys = dict(self.BASIC_GOOD_ROOM)
        missingKeys.pop('alt')
        self.assertRaises(KeyError, dc.isInRoom, json.dumps(missingKeys), 0, 0, 0)
    
    def test_inRoom(self):
        self.assertTrue(dc.isInRoom(json.dumps(self.BASIC_GOOD_ROOM), 37.229854, -80.417724, 2085))
    
    def test_clippedCorner(self):
        self.assertFalse(dc.isInRoom(json.dumps(self.BASIC_GOOD_ROOM), 37.229874, -80.417704, 2085))
    
    def test_completelyOutThere(self):
        self.assertFalse(dc.isInRoom(json.dumps(self.BASIC_GOOD_ROOM), 0, 0, 0))
    
    #Tests if the function detects points too far north but otherwise OK.
    def test_outOfLatHigh(self):
        self.assertFalse(dc.isInRoom(json.dumps(self.BASIC_GOOD_ROOM), 37.229894, -80.417724, 2085))
    
    #Tests if the function detects points too far east but otherwise OK.
    def test_outOfLonHigh(self):
        self.assertFalse(dc.isInRoom(json.dumps(self.BASIC_GOOD_ROOM), 37.229854, -80.417004, 2085))
    
    #Tests if the function detects points too far south but otherwise OK.
    def test_outOfLatLow(self):
        self.assertFalse(dc.isInRoom(json.dumps(self.BASIC_GOOD_ROOM), 37.229804, -80.417724, 2085))
    
    #Tests if the function detects points too far west but otherwise OK.
    def test_outOfLonLow(self):
        self.assertFalse(dc.isInRoom(json.dumps(self.BASIC_GOOD_ROOM), 37.229854, -80.417994, 2085))
    
    def test_aboveRoom(self):
        self.assertFalse(dc.isInRoom(json.dumps(self.BASIC_GOOD_ROOM), 37.229854, -80.417724, 2100))
    
    def test_belowRoom(self):
        self.assertFalse(dc.isInRoom(json.dumps(self.BASIC_GOOD_ROOM), 37.229854, -80.417724, 2000))
        
#Tests the decision-making class's ability to find a matching room.        
class testFindMatchingRoom(unittest.TestCase):
    #We check the behavior of the decision class directly.
    #We do this because when the server is actually running, the decision runs asynchronously,
    #so it is a little bit harder to test.
    def testMatchRoom(self):
        TEST_LOG_FILE = 'room_testnohouses.log'
        testLogger = logging.getLogger('nohouses')
        testHandler = logging.FileHandler(TEST_LOG_FILE, mode='w')
        testHandler.setFormatter(logging.Formatter('%(message)'))
        testLogger.addHandler(logging.FileHandler(TEST_LOG_FILE, mode='w'))
        dmaking = decisionMaking(testLogger, ['localhost', 8080], 'http://localhost:8082')
        self.assertEquals(dmaking.findMatchingRoom('bsaget', 37.229854, -80.417724, 2085), (101, 3))
        
    def testNoMatchingUser(self):
        TEST_LOG_FILE = 'room_testnouser.log'
        testLogger = logging.getLogger('nouser')
        testHandler = logging.FileHandler(TEST_LOG_FILE, mode='w')
        testHandler.setFormatter(logging.Formatter('%(message)'))
        testLogger.addHandler(logging.FileHandler(TEST_LOG_FILE, mode='w'))
        dmaking = decisionMaking(testLogger, ['localhost', 8080], 'http://localhost:8082')
        self.assertRaises(KeyError, dmaking.findMatchingRoom, 'nouser', 37.229854, -80.417724, 2085)
        
if __name__ == '__main__':
    unittest.main()