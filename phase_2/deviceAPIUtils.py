import clr
clr.AddReferenceToFileAndPath("DeviceDLL/DeviceDLL/bin/Debug/DeviceDLL.dll")
clr.AddReferenceToFile("Newtonsoft.Json.dll")
clr.AddReference("System")
import api as devapi
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
    
def makeSnapshot(devapiInterfaces, houseID, roomID):
    return createSnapshotString(devapiInterfaces.getDevices(houseID, roomID))

def createSnapshotString(deviceList):
    return nsoft.JsonConvert.SerializeObject(deviceList)