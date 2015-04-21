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
locationChange = {"userId":"user1", "lat":70.123456, "long":300.123456, "alt":150.123456, "time":"2015-04-06T18:05:05Z"}
times = {"localTime":'2015-04-19T12:59:23Z'}
commandsfromApp = {'userID': 'nouser',
                        'lat': 37.23512,
                        'lon': 37.23512,
                        'alt': 100,
                        'command-string':'brightenNearMe',
                        'time': '2015-04-19T12:59:23Z'}
#Test device state change response.
print 'Testing response to device state change'
connection.request('POST', '/DeviceState', json.dumps(deviceState))
res = connection.getresponse()
print 'Device State Change Response' + str(res.status)
sleep(1)

if (res.status == 200):
    print 'PASS'
else:
    print 'FAIL'

#Test location change response.
print 'Testing response to location change...'
print 'POST/LocationChange ' + json.dumps(locationChange)
connection.request('POST', '/LocationChange', json.dumps(locationChange))
res = connection.getresponse()
print 'Location Change Response' + str(res.status)
sleep(1)
if (res.status == 200):
    print 'PASS'
else:
    print 'FAIL'
    
#Test test receiving a user command from the app (ex. brighten lights)
print 'Testing response to app command...'
connection.request('POST', '/CommandsFromApp', json.dumps(commandsfromApp))
res = connection.getresponse()
sleep(1)
if (res.status == 200):
    print 'PASS'
else:
    print 'FAIL'

#test sending the local time to us
print "Testing response to the time"
connection.request('POST', '/LocalTime', json.dumps(times))
res = connection.getresponse()
sleep(1)
if (res.status == 200):
    print 'PASS'
else:
    print 'FAIL'

#Testing sending a weather update
print 'Testing response to weather change...'
print 'POST/Weather ' + json.dumps(weather)
connection.request('POST', '/Weather', json.dumps(weather))
res = connection.getresponse()
print 'Weather Response' + str(res.status)
sleep(1)
if (res.status == 200):
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

log = open('decisions.log', 'r')
print log.read()
