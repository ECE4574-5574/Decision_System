import httplib
import json
import datetime
import argparse

parser = argparse.ArgumentParser(description='Get port number...')
parser.add_argument('-p', '--port', type=int)
args=parser.parse_args()

connection = httplib.HTTPConnection('localhost', args.port)


deviceState = {"deviceName":"BedroomLight", "deviceType":3, "enabled":"true", "setpoint:":5, "time":"2015-04-06 18:05:05"}
locationChange = {"userId":"user1", "lat":70.123456, "long":300.123456, "alt":150.123456, "time":"2015-04-06 18:05:05"}
time = {"localTime":str(datetime.datetime.now())}

#Test device state change response.
print 'Testing response to device state change':
connection.request('POST', '/DeviceState', json.dumps(deviceState))
res = connection.getresponse()
print 'Device State Change Response' + str(res.status)
if (res.status == 200):
    print 'PASS'
else
    print 'FAIL'

#Test location change response.
print 'Testing response to location change...'
print 'POST/LocationChange ' + json.dumps(locationChange)
connection.request('POST', '/LocationChange', json.dumps(locationChange))
res = connection.getresponse()
print 'Location Change Response' + str(res.status)
if (res.status == 200):
    print 'PASS'
else
    print 'FAIL'
    
#Test 
print 'Testing response to app command...'
connection.request('POST', '/CommandsFromApp', json.dumps(commandsfromApp))
res = connection.getresponse()

connection.request('POST', '/LocalTime', json.dumps(time))
res = connection.getresponse()

connection.request('POST', '/CausesError', json.dumps(time))
res = connection.getresponse()
