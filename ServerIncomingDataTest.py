import httplib
import json
import datetime

connection = httplib.HTTPConnection('localhost', 8081)



weather = {"condition":"Sunny", "temperature":70, "WeatherTimeStamp":str(datetime.datetime.now())}
deviceState = {"deviceID":1, "deviceName":"BedroomLight", "deviceType":3, "spaceID": 4, "stateDevice":1, "DeviceStateTimeStamp":str(datetime.datetime.now())}
locationChange = {"usersID":3, "latitude":70, "longitude":300, "altitude":150, "locationTimeStamp":str(datetime.datetime.now())}
commandsfromApp = {"commandUserID":4,"commanddeviceID":1, "commanddeviceName":"BedroomLight", "commanddeviceType":3, "commandspaceID": 4, "commandstateDevice":0, "CommandTimeStamp":str(datetime.datetime.now())}
time = {"localTime":str(datetime.datetime.now())}


connection.request('POST', '/Weather1', json.dumps(weather))
res =  connection.getresponse()
connection.request('POST', '/DeviceState', json.dumps(deviceState))
res =  connection.getresponse()
connection.request('POST', '/LocationChange', json.dumps(locationChange))
res =  connection.getresponse()
connection.request('POST', '/CommandsFromApp', json.dumps(commandsfromApp))
res =  connection.getresponse()
connection.request('POST', '/LocalTime', json.dumps(time))
res =  connection.getresponse()
