import httplib
import json
import datetime

connection = httplib.HTTPConnection('localhost', 8081)



weather = {"condition":"Sunny", "temperature":70, "time":str(datetime.datetime.now())}
deviceState = {"deviceID":1, "deviceName":"BedroomLight", "deviceType":3, "spaceID": 4, "stateDevice":1, "time":str(datetime.datetime.now())}
locationChange = {"userId":"user1", "lat":70.123456, "long":300.123456, "alt":150.123456, "time":"2015-04-06 18:05:05"}
commandsfromApp = {"commandUserID":4,"commanddeviceID":1, "commanddeviceName":"BedroomLight", "commanddeviceType":3, "commandspaceID": 4, "commandstateDevice":0, "time":str(datetime.datetime.now())}
time = {"localTime":str(datetime.datetime.now())}


connection.request('POST', '/Weather', json.dumps(weather))
res = connection.getresponse()
connection.request('POST', '/DeviceState', json.dumps(deviceState))
res = connection.getresponse()
connection.request('POST', '/LocationChange', json.dumps(locationChange))
res = connection.getresponse()
connection.request('POST', '/CommandsFromApp', json.dumps(commandsfromApp))
res = connection.getresponse()
connection.request('POST', '/LocalTime', json.dumps(time))
res = connection.getresponse()
connection.request('POST', '/CausesError', json.dumps(time))
res = connection.getresponse()
