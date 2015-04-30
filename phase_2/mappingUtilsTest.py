import decisionClass as dm
import unittest
import json

class testIsInRoom(unittest.TestCase):
        
    def setUp(self):
        self.BASIC_GOOD_ROOM = {
        'corner1':[37.229874, -80.417754],
        'corner2':[37.229874, -80.417704],
        'corner3':[37.229824, -80.417704],
        'corner4':[37.229824, -80.417754],
        'alt':2080}

    def test_malformedBlob(self):
        malformed = 'this is not JSON'
        self.assertRaises(ValueError, dm.isInRoom, malformed, 0, 0, 0)
    
    def test_missingInformation(self):
        missingKeys = dict(self.BASIC_GOOD_ROOM)
        missingKeys.pop('alt')
        self.assertRaises(KeyError, dm.isInRoom, json.dumps(missingKeys), 0, 0, 0)
    
    def test_inRoom(self):
        self.assertTrue(dm.isInRoom(json.dumps(self.BASIC_GOOD_ROOM), 37.229854, -80.417724, 2085))
    
    def test_completelyOutThere(self):
        self.assertFalse(dm.isInRoom(json.dumps(self.BASIC_GOOD_ROOM), 0, 0, 0))
    
    #Tests if the function detects points too far north but otherwise OK.
    def test_outOfLatHigh(self):
        self.assertFalse(dm.isInRoom(json.dumps(self.BASIC_GOOD_ROOM), 37.229894, -80.417724, 2085))
    
    #Tests if the function detects points too far east but otherwise OK.
    def test_outOfLonHigh(self):
        self.assertFalse(dm.isInRoom(json.dumps(self.BASIC_GOOD_ROOM), 37.229854, -80.417004, 2085))
    
    #Tests if the function detects points too far south but otherwise OK.
    def test_outOfLatLow(self):
        self.assertFalse(dm.isInRoom(json.dumps(self.BASIC_GOOD_ROOM), 37.229804, -80.417724, 2085))
    
    #Tests if the function detects points too far west but otherwise OK.
    def test_outOfLonLow(self):
        self.assertFalse(dm.isInRoom(json.dumps(self.BASIC_GOOD_ROOM), 37.229854, -80.417994, 2085))
    
    def test_aboveRoom(self):
        self.assertFalse(dm.isInRoom(json.dumps(self.BASIC_GOOD_ROOM), 37.229854, -80.417724, 2100))
    
    def test_belowRoom(self):
        self.assertFalse(dm.isInRoom(json.dumps(self.BASIC_GOOD_ROOM), 37.229854, -80.417724, 2000))
        
if __name__ == '__main__':
    unittest.main()