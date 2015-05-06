import httplib
import json
import datetime
import argparse
from time import sleep

parser = argparse.ArgumentParser(description='Get port number...')
parser.add_argument('-p', '--port', type=int)
args=parser.parse_args()

connection = httplib.HTTPConnection('localhost', args.port)

weather = {"lat":70.123456, "long":300.123456, "alt":150.123456,"condition":"sunny","temperature":72.2,"time":"2015-04-06T18:05:05Z"}
deviceState = {"deviceName":"BedroomLight", "deviceType":3, "enabled":"true", "setpoint":5, "time":"2015-04-06T18:05:05Z"}
locationChange = {"userID":"user1", "lat":70.123456, "lon":300.123456, "alt":150.123456, "time":"2015-04-06T18:05:05Z"}
times = {"localTime":'2015-04-19T12:59:23Z'}
commandsfromApp = {'userID': 'nouser',
                        'lat': 37.23512,
                        'lon': 37.23512,
                        'alt': 100,
                        'command-string':'brightenNearMe',
                        'time': '2015-04-19T12:59:23Z'}
houseUpdate = {"userID":"user1","command-string":"manualChange","time":"2015-04-06T18:05:05Z","device-blob":"THEBLOBBBBB"}
#Test device state change response.
log = open('decisions.log', 'r')
print 'Testing response to device state change'
connection.request('POST', '/DeviceState', json.dumps(deviceState))
res = connection.getresponse()
print 'Device State Change Response' + str(res.status)
sleep(2)
log.readline()
line = log.readline()
data = line.split(':',1)[1]
data = data[1:]
message = json.loads(data)
check = "('PATCH', 'C/user1/2015-04-06T18:05:05Z/WayneManor/aspace/BedroomLight')\n"
line = log.readline()
data = line.split(':',1)[1]
request = data[1:]
line = log.readline()
data = line.split(':',1)[1]
response = data[1:]

if (res.status == 200 and message['action-type'] == 'device state change' and message['action-data'] == deviceState and request == check and int(response) == 200):
    print 'PASS'
else:
    print 'FAIL'

#Test location change response.
print 'Testing response to location change...'
print 'POST/LocationChange ' + json.dumps(locationChange)
connection.request('POST', '/LocationChange', json.dumps(locationChange))
res = connection.getresponse()
print 'Location Change Response' + str(res.status)
sleep(2)
log.readlines(2)
line = log.readline()
data = line.split(':',1)[1]
data = data[1:]
message = json.loads(data)
check = "('PATCH', 'A/user1/2015-04-06T18:05:05Z/WayneManor')\n"
line = log.readline()
data = line.split(':',1)[1]
request = data[1:]
line = log.readline()
data = line.split(':',1)[1]
response = data[1:]
if (res.status == 200 and message['action-type'] == 'location-update' and message['action-data'] == locationChange and request == check and int(response) == 200):
    print 'PASS'
else:
    print 'FAIL'
    
#Test test receiving a user command from the app (ex. brighten lights)
print 'Testing response to app command...'
connection.request('POST', '/CommandsFromApp', json.dumps(commandsfromApp))
res = connection.getresponse()
sleep(2)
log.readlines(2)
line1 = log.readline()
check = "nonexistent user\n"
if (res.status == 200 and line1 == check):
    print 'PASS'
else:
    print 'FAIL'

print "Testing response to houseUpdate"
connection.request('POST', '/CommandsFromApp', json.dumps(houseUpdate))
res = connection.getresponse()
if (res.status == 200):
    print 'PASS'
else:
    print 'FAIL'

#test sending the local time to us
print "Testing response to the time"
connection.request('POST', '/LocalTime', json.dumps(times))
res = connection.getresponse()
sleep(2)
log.readlines(2)
line = log.readline()
data = line.split(':',1)[1]
data = data[1:]
check = str(times) + "\n"
if (res.status == 200 and data == check):
    print 'PASS'
else:
    print 'FAIL'

#Testing sending a weather update
print 'Testing response to weather change...'
print 'POST/Weather ' + json.dumps(weather)
connection.request('POST', '/Weather', json.dumps(weather))
res = connection.getresponse()
print 'Weather Response' + str(res.status)
sleep(2)
log.readlines(2)
line = log.readline()
data = line.split(':',1)[1]
data = data[1:]
check = str(weather) + "\n"
if (res.status == 200 and data == check):
    print 'PASS'
else:
    print 'FAIL'

#Testing an in correct URL
print "Testing an incorrect URL"
connection.request('POST', '/CausesError', json.dumps(times))
res = connection.getresponse()
sleep(1)
if (res.status == 400):
    print 'PASS'
else:
    print 'FAIL'



