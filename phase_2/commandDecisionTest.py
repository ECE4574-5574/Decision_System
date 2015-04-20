#This automatically tests that the server's handling of POST /CommandsFromApp is correct.

import json
import httplib
import unittest
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
ACTUAL_HOUSE_LAT = 37.23512
ACTUAL_HOUSE_LON = -80.41352
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
class commandDecisionTest(unittest.TestCase):
    
    #We check the behavior of the decision class directly.
    #We do this because when the server is actually running, the decision runs asynchronously,
    #so it is a little bit harder to test.
    def testNoMatchingUser(self):
        testoutfile = open('nomatchinguser.txt', 'w')
        try:
            print 'Testing command decision when user does not exist.'
            dmaking = decisionMaking(testoutfile, ['localhost', 8080], 'http://localhost:8082')
            dmaking.command(good_request_no_user, 0)
            testoutfile.close()
            testoutfile = open('nomatchinguser.txt')
            log = testoutfile.read()
            expected = ['Decision 0:',
                        'req localhost:8080 GET UI/nouser',
                        'response 404']
            self.assertTrue(validateLog(expected, log))
        except:
            if not f.closed:
                f.close()
            raise
    
    def testNoMatchingHouse(self):
        testoutfile = open('nomatchinghouse.txt', 'w')
        try:
            print 'Testing command decision when there will be no matching house'
            dmaking = decisionMaking(testoutfile, ['localhost', 8080], 'http://localhost:8082')
            dmaking.command(good_request_no_house, 0)
            testoutfile.close()
            testoutfile = open('nomatchinghouse.txt')
            log = testoutfile.read().strip('\n')
            expected = ['Decision 0:',
                        'req localhost:8080 GET UI/'+ACTUAL_USER_ID,
                        'response 200',
                        'req localhost:8080 GET HI/1',
                        'response 200',
                        'req localhost:8080 GET HI/101',
                        'response 200',
                        'Could not find a matching house for that user and coordinates.']
            self.assertTrue(validateLog(expected, log))
        except:
            if not testoutfile.closed:
                testoutfile.close()
            raise
    
    def testGoodRequest(self):
        testoutfile = open('goodhouse.txt', 'w')
        try:
            print 'Testing command decision when there will be no matching user'
            dmaking = decisionMaking(testoutfile, ['localhost', 8080], 'http://localhost:8082')
            dmaking.command(good_request_should_work, 0)
            testoutfile.close()
            testoutfile = open('goodhouse.txt')
            log = testoutfile.read().strip('\n')
            expected = ['Decision 0:',
                'req localhost:8080 GET UI/'+ACTUAL_USER_ID,
                'response 200',
                'req localhost:8080 GET HI/1',
                'response 200',
                'req localhost:8080 GET HI/101',
                'response 200',
                'match house 101',
                'requesting devices']
            self.assertTrue(validateLog(expected, log))
        except:
            if not testoutfile.closed:
                testoutfile.close()
            raise

notJson = "this is some garbage that isn't json"

missingKeys = json.dumps({'userID':'some-user-id',
    'lat':0.1111, 'lon':0.1111, 
    'command-string':'brightenNearMe'})
notANumber = json.dumps({'userID':'some-user-id',
    'lat':0.1111, 'lon':'garbage', 'alt':0.111,
    'command-string':'brightenNearMe'})
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
    
    def testGoodRequ(self):
        print 'Checking response to POST with good request with no side effects...'
        self.conn.request('POST', APP_COMMAND_PATH, json.dumps(good_request_no_user))
        self.assertEqual(200, self.conn.getresponse().status)
    
        
if __name__ == "__main__":
    unittest.main()