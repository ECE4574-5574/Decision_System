import unittest
import deviceAPIUtils
import clr
import json
clr.AddReferenceToFileAndPath("DeviceDLL/DeviceDLL/bin/Debug/DeviceDLL.dll")
clr.AddReferenceToFile("Newtonsoft.Json.dll")
clr.AddReference("System")
import api as devapi
import System
from  System.Collections.Generic import List

class deviceAPIUtilsTest(unittest.TestCase):
    
    def testCanBrightenNotCLR(self):
        self.assertFalse(deviceAPIUtils.canBrighten(10))
        self.assertFalse(deviceAPIUtils.canBrighten('a string'))
        somePythonTypeObject = ['this is', 'a list of python strings', 'not a .NET class']
        self.assertFalse(deviceAPIUtils.canBrighten(somePythonTypeObject))
        
    def testCanBrightenIsEnableable(self):
        someIEnableable = devapi.CeilingFan(None, None)
        self.assertFalse(deviceAPIUtils.canBrighten(someIEnableable))
        
    def testCanBrightenWrongIReadable(self):
        wrongGenericIReadable = devapi.Thermostat(None, None)
        self.assertFalse(deviceAPIUtils.canBrighten(wrongGenericIReadable))
    
    def testCanBrightenIsLight(self):
        lightswitch = devapi.LightSwitch(None, None)
        lightswitch.Enabled = True
        self.assertTrue(deviceAPIUtils.canBrighten(lightswitch))
        
    def testDemoCreateSnapshotString(self):
        #This is also meant to demonstrate what the snapshot format will look like.
        
        #Setting up...
        fan = devapi.CeilingFan(None, None)
        light = devapi.LightSwitch(None, None)
        devlist = List[devapi.Device]()
        devlist.Add(fan)
        devlist.Add(light)
        
        #Once you have a list of devices (for example, from a call to interfaces.)
        #Just call this function to generate the snapshot.
        #We'll print it here to show what the format looks like.
        print 'Demo: Show snapshot string format'
        print deviceAPIUtils.createSnapshotString(devlist)
        
    def testDemoMakeSnapshot(self):
        #This test/code snippet shows how to get a snapshot string given a house and room ID.
        
        #You will need to have constructed an instance of the Device API "Interfaces" class - 
        #This tells the device API how it can talk to the devices, and it is the class that provides
        #most of the querying capabilities for the Device API.
        #For this demo we use a dummy address (we assume the device API is not using it)
        devInterface = devapi.Interfaces(System.Uri("http://dummy.devapi.not"))
        
        SOME_HOUSE_ID = 101
        SOME_ROOM_ID = 3
        
        #Now, take this interfaces class and pass it to makeSnapshot
        print 'Demo: Make snapshot from device api'
        print deviceAPIUtils.makeSnapshot(devInterface, 101, 3)
        
    def testDemoExtractFromSnapshot(self):
    
        print '\n\nDemo: Extract from Snapshot'
        #This helps demonstrate how to retrieve a particular device's snapshot from a snapshot string.
        
        #You can ignore this part - you can assume you already have the snapshot string - I am just setting up something
        #to mimic it.
        fan = devapi.CeilingFan(None, None)
        id = devapi.FullID()
        id.HouseID = 101
        id.RoomID = 3
        id.DeviceID = 1
        fan.ID = id
        
        light = devapi.LightSwitch(None, None)
        id = devapi.FullID()
        id.HouseID = 101
        id.RoomID = 3
        id.DeviceID = 2
        light.ID = id
        light.Enabled = True
        
        light2 = devapi.LightSwitch(None, None)
        id = devapi.FullID()
        id.HouseID = 101
        id.RoomID = 3
        id.DeviceID = 3
        light2.ID = id
        
        devlist = List[devapi.Device]()
        devlist.Add(fan)
        devlist.Add(light)
        devlist.Add(light2)
        print 'Extracting from snapshot string:'
        snapshotString = deviceAPIUtils.createSnapshotString(devlist)
        print snapshotString
        
        #Once you have your snapshot string (retrieved from persistent storage)
        snapshotJson = json.loads(snapshotString)
        
        #The snapshot is just a list of individual device snapshots.
        #To make searching for a device easier, we build a dictionary
        deviceSnapshotDict = {}
        for oneDeviceSnapshot in snapshotJson:
            oneDeviceFullID = oneDeviceSnapshot["ID"]
            oneFullIDTuple = (int(oneDeviceFullID["HouseID"]), int(oneDeviceFullID["RoomID"]), int(oneDeviceFullID["DeviceID"]))
            deviceSnapshotDict[oneFullIDTuple] = oneDeviceSnapshot
        
        #Now, we look for a particular device ID in the dictionary. Let's say we have the device light...
        
        deviceFullIDTuple = (int(light.ID.HouseID), int(light.ID.RoomID), int(light.ID.DeviceID))
        print "\n\nTrying to extract device with ID: " + str(deviceFullIDTuple)
        
        if deviceFullIDTuple in deviceSnapshotDict:
            print "Found it:"
            print deviceSnapshotDict[deviceFullIDTuple]
        else:
            print "Uh-oh..."
    
    def testMakeAndExtractSnapshotNoMatch(self):
        #Tests the entire snapshot-making process with no match at the end.
        #Build a list of dummy device objects.
        #This test
        fan = devapi.CeilingFan(None, None)
        id = devapi.FullID()
        id.HouseID = 101
        id.RoomID = 3
        id.DeviceID = 1
        fan.ID = id
        
        light = devapi.LightSwitch(None, None)
        id = devapi.FullID()
        id.HouseID = 101
        id.RoomID = 3
        id.DeviceID = 2
        light.ID = id
        light.Enabled = True
        
        light2 = devapi.LightSwitch(None, None)
        id = devapi.FullID()
        id.HouseID = 101
        id.RoomID = 3
        id.DeviceID = 3
        light2.ID = id
        
        devlist = List[devapi.Device]()
        devlist.Add(fan)
        devlist.Add(light)
        devlist.Add(light2)
        
        #Create a snapshot string (in actual use this would be stored in and retrieved from persistent storage)
        snapshotString = deviceAPIUtils.createSnapshotString(devlist)
        
        #Use convertSnapshotToDict to produce the snapshot
        snapshotDict = deviceAPIUtils.convertSnapshotToDict(devlist)
        self.AssertIsNotNone(snapshotDict)
        self.AssertTrue(len(snapshotDict) > 0)
        
        #Create a device with an ID not in the list.
        missingDevice = devapi.LightSwitch(None, None)
        id = devapi.FullID()
        id.HouseID = 101
        id.RoomID = 3
        id.DeviceID = 400
        missingDevice.ID = id
        
        #Try to extract its device from the room snapshot string. Should return none.
        self.AssertIsNone(deviceAPIUtils.extractDeviceSnapshot(missingDevice, snapshotDict))
    
    def testMakeAndExtractSnapshotNoMatch(self):
        #Tests the entire snapshot-making process with no match at the end.
        #Build a list of dummy device objects
        fan = devapi.CeilingFan(None, None)
        id = devapi.FullID()
        id.HouseID = 101
        id.RoomID = 3
        id.DeviceID = 1
        fan.ID = id
        
        light = devapi.LightSwitch(None, None)
        id = devapi.FullID()
        id.HouseID = 101
        id.RoomID = 3
        id.DeviceID = 2
        light.ID = id
        light.Enabled = True
        
        light2 = devapi.LightSwitch(None, None)
        id = devapi.FullID()
        id.HouseID = 101
        id.RoomID = 3
        id.DeviceID = 3
        light2.ID = id
        
        devlist = List[devapi.Device]()
        devlist.Add(fan)
        devlist.Add(light)
        devlist.Add(light2)
        
        #Create a snapshot string (in actual use this would be stored in and retrieved from persistent storage)
        snapshotString = deviceAPIUtils.createSnapshotString(devlist)
        
        #Use convertSnapshotToDict to produce the snapshot
        snapshotDict = deviceAPIUtils.convertSnapshotToDict(snapshotString)
        self.assertIsNotNone(snapshotDict)
        self.assertTrue(len(snapshotDict) > 0)
        
        #Create a device with an ID not in the list.
        missingDevice = devapi.LightSwitch(None, None)
        id = devapi.FullID()
        id.HouseID = 101
        id.RoomID = 3
        id.DeviceID = 400
        missingDevice.ID = id
        
        #Try to extract its device from the room snapshot string. Should not return none.
        devsnapshot = deviceAPIUtils.extractDeviceSnapshot(light, snapshotDict)
        self.assertIsNotNone(devsnapshot)
        devsnapshotTestDict = json.loads(devsnapshot)
        
        self.assertEquals(devsnapshotTestDict['ID']['HouseID'], 101)
        self.assertEquals(devsnapshotTestDict['ID']['RoomID'], 3)
        self.assertEquals(devsnapshotTestDict['ID']['DeviceID'], 2)
        
if __name__ == '__main__':
    unittest.main()