import httplib
import json

ACTUAL_USER_ID = 'bsaget'
ACTUAL_HOUSE_LAT = 37.229854
ACTUAL_HOUSE_LON = -80.417724
ACTUAL_HOUSE_ALT = 2085
ACTUAL_COMMAND_STRING = 'brightenNearMe'
EXAMPLE_TIME_STAMP = '2015-04-19T12:59:23Z'

good_request_no_user = {'userID': '2000',
                        'lat': ACTUAL_HOUSE_LAT,
                        'lon': ACTUAL_HOUSE_LON,
                        'alt': ACTUAL_HOUSE_ALT,
                        'command-string':ACTUAL_COMMAND_STRING,
                        'time': EXAMPLE_TIME_STAMP}

good_request_no_house = {'userID': ACTUAL_USER_ID,
                         'lat': 0, 'lon': 0, 'alt': 0,
                         'command-string':ACTUAL_COMMAND_STRING,
                         'time': EXAMPLE_TIME_STAMP}

good_request_should_work = {'userID': ACTUAL_USER_ID,
                        'lat': ACTUAL_HOUSE_LAT,
                        'lon': ACTUAL_HOUSE_LON,
                        'alt': ACTUAL_HOUSE_ALT,
                        'command-string':ACTUAL_COMMAND_STRING,
                        'time': EXAMPLE_TIME_STAMP}
						
good_location_message = {'userID': ACTUAL_USER_ID,
                        'lat': ACTUAL_HOUSE_LAT,
                        'lon': ACTUAL_HOUSE_LON,
                        'alt': ACTUAL_HOUSE_ALT,
                        'command-string':ACTUAL_COMMAND_STRING,
                        'time': EXAMPLE_TIME_STAMP}
change_location_message = {'userID': ACTUAL_USER_ID,
                        'lat': 37.229854,
                        'lon': -80.417666,
                        'alt': ACTUAL_HOUSE_ALT,
                        'command-string':ACTUAL_COMMAND_STRING,
                        'time': EXAMPLE_TIME_STAMP}

conn = httplib.HTTPConnection('localhost', 8085)
print 'Demo: User ID does not exist.'                        
conn.request('POST', '/CommandsFromApp', json.dumps(good_request_no_user))
print 'Response:' + str(conn.getresponse().status)
print 'PAUSE'
raw_input()
print ''

print 'Demo: User location does not match any house.'
conn.request('POST', '/CommandsFromApp', json.dumps(good_request_no_house))
print 'Response:' + str(conn.getresponse().status)
print 'PAUSE'
raw_input()
print ''

print 'Demo: Make it brighter near me command executes the whole way through.'
conn.request('POST', '/CommandsFromApp', json.dumps(good_request_should_work))
print 'Response:' + str(conn.getresponse().status)
print 'PAUSE'
raw_input()
print ''

print 'Demo: Location change, stage one.'
conn.request('POST', '/LocationChange', json.dumps(good_location_message))
print 'Response:' + str(conn.getresponse().status)
print 'PAUSE'
raw_input()
print ''

print 'Demo: Location change, stage two.'
conn.request('POST', '/LocationChange', json.dumps(change_location_message))
print 'Response:' + str(conn.getresponse().status)
print 'PAUSE'
raw_input()
print ''
