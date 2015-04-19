#This automatically tests that the server's handling of POST /CommandsFromApp is correct.

import json
import httplib
from decisionClass import decisionMaking

def checkStatus(expected, response):
    if expected == response.status:
        return True
    else:
        print 'Expected status ' + str(expected) + ' but got ' + str(response.status)
        return False

if __name__ == "__main__":
    APP_COMMAND_PATH = '/CommandsFromApp'
    OUTPUT_FILE = 'commandtestlog.txt'
    
    ACTUAL_USER_ID = 'bsaget'
    ACTUAL_HOUSE_LAT = 37.23
    ACTUAL_HOUSE_LON = -80.41
    ACTUAL_HOUSE_ALT = 100
    ACTUAL_COMMAND_STRING = 'brightenNearMe'
    
    good_request_no_user = {'userID': 'nouser',
                            'lat': ACTUAL_HOUSE_LAT,
                            'lon': ACTUAL_HOUSE_LON,
                            'alt': ACTUAL_HOUSE_ALT,
                            'command-string':ACTUAL_COMMAND_STRING}
    good_request_no_house = {'userID': ACTUAL_USER_ID,
                             'lat': 0, 'lon': 0, 'alt': 0,
                             'command-string':ACTUAL_COMMAND_STRING}
    good_request_should_work = {'userID': ACTUAL_USER_ID,
                            'lat': ACTUAL_HOUSE_LAT,
                            'lon': ACTUAL_HOUSE_LON,
                            'alt': ACTUAL_HOUSE_ALT,
                            'command-string':ACTUAL_COMMAND_STRING}
    
    #For right now, only good_request_no_user should work, since the data we're looking for won't be in the database.
    
    
    #First, we check the behavior of the decision class directly.
    #We do this because when the server is actually running, the decision runs asynchronously,
    #so it is a little bit harder to test directly.
    dmaking = decisionMaking(OUTPUT_FILE, ['localhost', 8080], 'dummy')
    
    decision_server_port = 8085
    #Then, let's check the server's ability to sort through bad input.
    #We expect a JSON object with the following schema:
    #{
    #    "userID":"some-user-id"
    #    "lat":float
    #    "lon":float
    #    "alt":float
    #    "command-string":"brightenNearMe"
    #}
    #Anything else should be gracefully rejected.

    notJson = "this is some garbage that isn't json"

    missingKeys = json.dumps({'userID':'some-user-id',
        'lat':0.1111, 'long':0.1111, 
        'command-string':'brightenNearMe'})

    notANumber = json.dumps({'userID':'some-user-id',
        'lat':0.1111, 'long':'garbage', 'alt':0.111,
        'command-string':'brightenNearMe'})
        
    conn = httplib.HTTPConnection('localhost', decision_server_port)
    
    all_OK = True    
    print 'Checking response to POST with non-json body...'
    conn.request('POST', APP_COMMAND_PATH, notJson)
    all_OK = all_OK and checkStatus(400, conn.getresponse())
    
    print 'Checking response to POST with missing JSON fields...'
    conn.request('POST', APP_COMMAND_PATH, missingKeys)
    all_OK = all_OK and checkStatus(400, conn.getresponse())
    
    print 'Checking response to POST with bad data in JSON fields...'
    conn.request('POST', APP_COMMAND_PATH, notANumber)
    all_OK = all_OK and checkStatus(400, conn.getresponse())
    
    print 'Checking response to POST with good request with no side effects...'
    conn.request('POST', APP_COMMAND_PATH, json.dumps(good_request_no_user))
    all_OK = all_OK and checkStatus(200, conn.getresponse())
    
    if all_OK:
        print 'Server responses are OK'
    else:
        print 'TEST FAILED.'