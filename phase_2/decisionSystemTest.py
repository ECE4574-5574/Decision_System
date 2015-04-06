# Contributor : Sumit Kumar

import unittest
import BaseHTTPServer
import httplib
from ServerIncomingData import ServerInfoHandler as sih
from decisions import randomDecision
from PersistentStorageFunctions import PersistentStorageFunctions as psf
from outgoingAPI import runOutgoingAPI
from PersistentStoragePost import PersistentInfoHandler as PIH

class DecisionSystemTest(unittest.TestCase):

    def testIncomingData(self):
        HOST_NAME = 'example.net' # Change this to host_name.
        PORT_NUMBER = 80 # Change this to the port_number.
        server_class = BaseHTTPServer.HTTPServer
        httpd = server_class((HOST_NAME, PORT_NUMBER), sih)

        self.assert_( httpd.serve_forever(), "Incoming data API failed." )

    def testRandomDecisions(self):
        self.assert_( randomDecision(), "Random decision failed." )

    def testPersistentStorage_house(self):
        self.assert_(psf.getAllItemsInHouse())

    def testPersistentStorage_room(self):
        self.assert_(psf.getAllItemsInRoom())

    def testOutgoingApi(self):
        self.assert_(runOutgoingAPI(), "Outgoing API failed test.")

    def testPersistentStoragePost(self):
        # Please change the following parameters.
        path = ""
        houseID = ""
        version = ""
        roomID = ""
        deviceID = ""
        userID = ""
        self.assert_(PIH.PostRequest(path, houseID, version, roomID, deviceID, userID), "Outgoing API failed test.")

if __name__ == '__main__':
    unittest.main()