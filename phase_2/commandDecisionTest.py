#This automatically tests that the server's handling of POST /CommandsFromApp is correct.

#To run these tests: You should start the mock persistent storage server stored at testing_utils/mock_pss/persistent_storage_server.py
#You should also start ServerIncomingData.py on port 8085. You may specify any persistent storage, server address, and output file.
#The behavior of the decision class will be tested directly.

import json
import httplib
import unittest
import logging
from decisionClass import decisionMaking

def checkStatus(expected, response):
    if expected == response.status:
        return True
    else:
        print 'Expected status ' + str(expected) + ' but got ' + str(response.status)
        return False
        
def validateLog(expected, actual):
    splitactual = actual.splitlines()
    if not len(splitactual) == len(expected):
        print 'Length of decision-making log is not what is expected!'
        print 'Log is ' + str(len(splitactual)) + ' long and expected ' + str(len(expected)) + '.'
        return False
    for i in range(0, len(splitactual)):
        if not splitactual[i] == expected[i]:
            print 'Line mismatch at ' + str(i) + '! Found:'
            print splitactual[i]
            print 'But expected:'
            print expected[i]
            return False
    return True

    
OUTPUT_FILE = 'commandtestlog.txt'

ACTUAL_USER_ID = 'bsaget'
ACTUAL_HOUSE_LAT = 37.229854
ACTUAL_HOUSE_LON = -80.417724
ACTUAL_HOUSE_ALT = 2085
ACTUAL_COMMAND_STRING = 'brightenNearMe'
EXAMPLE_TIME_STAMP = '2015-04-19T12:59:23Z'

good_request_no_user = {'userID': 'nouser',
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
class commandDecisionTest(unittest.TestCase):
    
    #We check the behavior of the decision class directly.
    #We do this because when the server is actually running, the decision runs asynchronously,
    #so it is a little bit harder to test.
    def testNoMatchingUser(self):
        try:
            TEST_LOG_FILE = 'testnouser.log'
            testLogger = logging.getLogger('nouser')
            testHandler = logging.FileHandler(TEST_LOG_FILE, mode='w')
            testHandler.setFormatter(logging.Formatter('%(message)'))
            testLogger.addHandler(logging.FileHandler(TEST_LOG_FILE, mode='w'))
            print 'Testing command decision when user does not exist.'
            dmaking = decisionMaking(testLogger, ['localhost', 8080], 'http://localhost:8082')
            dmaking.command(good_request_no_user)
            testoutfile = open(TEST_LOG_FILE)
            log = testoutfile.read().strip('\n')
            expected = ['Command Decision 1:',
                        'nonexistent user']
            self.assertTrue(validateLog(expected, log))
        except:
            raise
    
    def testNoMatchingHouse(self):
        try:
            TEST_LOG_FILE = 'testnohouse.log'
            testLogger = logging.getLogger('nohouse')
            testHandler = logging.FileHandler(TEST_LOG_FILE, mode='w')
            testHandler.setFormatter(logging.Formatter('%(message)'))
            testLogger.addHandler(logging.FileHandler(TEST_LOG_FILE, mode='w'))
            print 'Testing command decision when there will be no matching house'
            dmaking = decisionMaking(testLogger, ['localhost', 8080], 'http://localhost:8082')
            dmaking.command(good_request_no_house)
            testoutfile = open(TEST_LOG_FILE)
            log = testoutfile.read().strip('\n')
            expected = ['Command Decision 1:',
                        'no matching room']
            self.assertTrue(validateLog(expected, log))
        except:
            raise
    
    def testGoodRequest(self):
        try:
            TEST_LOG_FILE = 'testallok.log'
            testLogger = logging.getLogger('allok')
            testHandler = logging.FileHandler(TEST_LOG_FILE, mode='w')
            testHandler.setFormatter(logging.Formatter('%(message)'))
            testLogger.addHandler(logging.FileHandler(TEST_LOG_FILE, mode='w'))
            testLogger.setLevel(logging.INFO)
            print 'Testing command decision when there will be no matching user'
            dmaking = decisionMaking(testLogger, ['localhost', 8080], 'http://localhost:8082')
            dmaking.command(good_request_should_work)
            testoutfile = open(TEST_LOG_FILE)
            log = testoutfile.read().strip('\n')
            expected = ['Command Decision 1:',
                'matched room (101, 3)',
                'requesting devices']
            self.assertTrue(validateLog(expected, log))
        except:
            raise
            
    def testDemoRestoreSnapshot(self):
        print 'Running restore snapshot demo'
        dmaking = decisionMaking(None, ['localhost', 8080], 'http://localhost:8082')
        dmaking.restoreRoomState(None, None, None, None)

notJson = "this is some garbage that isn't json"

missingKeys = json.dumps({'userID':'some-user-id',
    'lat':0.1111, 'lon':0.1111, 
    'command-string':'brightenNearMe'})
notANumber = json.dumps({'userID':'some-user-id',
    'lat':0.1111, 'lon':'garbage', 'alt':0.111,
    'command-string':'brightenNearMe', 'time':'2015-04-19T12:59:23Z'})
garbageTimeStamp = json.dumps({'userID':'some-user-id',
    'lat':0.1111, 'lon':0.1111, 'alt':0.111,
    'command-string':'brightenNearMe', 'time':'2493205901'})
decision_server_port = 8085
APP_COMMAND_PATH = '/CommandsFromApp'
class serverResponseTest(unittest.TestCase):
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
    
    def setUp(self):
        self.conn = httplib.HTTPConnection('localhost', decision_server_port)
    
    def testNonJSON(self):
        print 'Checking response to POST with non-json body...'
        self.conn.request('POST', APP_COMMAND_PATH, notJson)
        self.assertEqual(400, self.conn.getresponse().status)
     
    def testMissingFields(self):
        print 'Checking response to POST with missing JSON fields...'
        self.conn.request('POST', APP_COMMAND_PATH, missingKeys)
        self.assertEqual(400, self.conn.getresponse().status)
    
    def testBadCoords(self):
        print 'Checking response to POST with bad data in JSON fields...'
        self.conn.request('POST', APP_COMMAND_PATH, notANumber)
        self.assertEqual(400, self.conn.getresponse().status)
        
    def testGarbageTimeStamp(self):
        print 'Checking response to POST with a garbage time stamp...'
        self.conn.request('POST', APP_COMMAND_PATH, garbageTimeStamp)
        self.assertEqual(400, self.conn.getresponse().status)
    
    def testGoodRequ(self):
        print 'Checking response to POST with good request with no side effects...'
        self.conn.request('POST', APP_COMMAND_PATH, json.dumps(good_request_no_user))
        self.assertEqual(200, self.conn.getresponse().status)
    
        
if __name__ == "__main__":
    unittest.main()