import clr
clr.AddReferenceToFileAndPath("DeviceDLL/DeviceDLL/bin/Debug/DeviceDLL.dll")
clr.AddReferenceToFile("Newtonsoft.Json.dll")
clr.AddReference("System")
import api as devapi
import json
import System
import Newtonsoft.Json as nsoft

#Returns true if device can be brightened.
def canBrighten(device):
    #There may be a slightly cleaner way of doing this, but currently the necessary interfaces are private.
    #Establish that this is in fact a Device from the C# device library...
    if not isinstance(device, devapi.Device):
        return False

    #This is basically the best kludge I've ever come up with: Because the IEnableable and IReadable interfaces
    #are not declared public in the Device API (for now) we can't actually get their Type from here...
    #So make a list of the methods on the device and check for the ones we need.
    methods = {}
    for method in clr.GetClrType(type(device)).GetMethods():
        methods[method.Name] = method.ReturnType.Name
    
    return ('set_Enabled' in methods) and 'get_Value' in methods and methods['get_Value'] == 'Light'
    
    """
    #We can uncomment this block if they actually make those interfaces public...
    #Establish that it is IEnableable
    if not clr.GetClrType(type(device)).IsAssignableFrom(clr.GetClrType(devapi.IEnableable)):
        return False
        
    if not clr.GetClrType(type(device)).IsAssignableFrom(clr.GetClrType(devapi.IReadable[Light])):
        return False
    
    return True
    """

    
#Functions to make a snapshot from the device API.
#Takes an instance of the device API Interfaces class, and
#returns a string to be stored in persistent storage as the room snapshot.
def makeSnapshot(devapiInterfaces, houseID, roomID):
    return createSnapshotString(devapiInterfaces.getDevices(houseID, roomID))

def createSnapshotString(deviceList):
    return nsoft.JsonConvert.SerializeObject(deviceList)
    
#Takes the string from persistent storage and returns a dictionary containing the device snapshot.
#To avoid having to recreate this dictionary for every extractDeviceSnapshot, make sure to run
#this function once and store the dictionary.
#This function does not catch any errors, so you will need to insulate the rest of your code from that.
def convertSnapshotToDict(snapshotString):
    snapshotJson = json.loads(snapshotString)
    #The snapshot is just a list of individual device snapshots.
    #To make searching for a device easier, we build a dictionary
    deviceSnapshotDict = {}
    for oneDeviceSnapshot in snapshotJson:
        oneDeviceFullID = oneDeviceSnapshot["ID"]
        oneFullIDTuple = (int(oneDeviceFullID["HouseID"]), int(oneDeviceFullID["RoomID"]), int(oneDeviceFullID["DeviceID"]))
        deviceSnapshotDict[oneFullIDTuple] = oneDeviceSnapshot
    return deviceSnapshotDict

#Uses a device snapshot dictionary as above to extract a particular device
#snapshot as a JSON string.
#Takes an instance of device and you should pass a dictionary.
#from convertSnapshotToDict above into the second parameter.
#Returns None if no matching device could be found.
def extractDeviceSnapshot(device, snapshotDict):
    deviceFullIDTuple = (int(device.ID.HouseID), int(device.ID.RoomID), int(device.ID.DeviceID))
    if deviceFullIDTuple in snapshotDict:
        return json.dumps(snapshotDict[deviceFullIDTuple])
    else:
        return None