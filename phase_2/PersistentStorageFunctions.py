from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import requests
import json
import httplib
import urllib

FUNCTION_TYPES{ 'get' : 'GET'}

class PersistentStorageFunctions():
    def __init__(self):
	    #COnnection to the server is established
        self.conn = httplib.HTTPConnection('localhost', 8080)
		
    def getAllItemsInHouse(self, houseID='testHouseID'):
        
        self.conn.request('GET','HD/HOUSEID/')
        return self.conn.getresponse();

    def getAllItemsInRoom(self, houseID='testHouseID', roomID='testRoomID'):
        pass