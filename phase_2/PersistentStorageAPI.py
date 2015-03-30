#API Calls to and from the Persistent Storage
#Contributors : Prerana Rane, Luke Lapham
#Date : 3/29/2015

# Receiving HTTP Responses for GET and POST methods sent to the server.
# Unable to convert to JSON format since there is no data present. Receiving the error "No JSON object to decode"

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import requests
import json
import httplib
import urllib

#COnnection to the server is established
conn = httplib.HTTPConnection('localhost', 8080)

""" INCOMING DATA FROM PERSISTENT STORAGE """

#Method to get all devices in a specific house
print conn.request('GET','HD/HOUSEID/')
conn.getresponse();

#Method to get all devices in a specific room (for a certain house)
print conn.request('GET','RD/HOUSEID/ROOMID/')
conn.getresponse();

#Method to get devices of a specific type in a specific house
print conn.request('GET','HT/HOUSEID/TYPE')
conn.getresponse();

#Method to get devices of a specific type in a specific room (for a certain house)
print conn.request('GET','RT/HOUSEID/ROOMID/TYPE/')
conn.getresponse();

#Methods to user information (accesses information from the user’s profile)
print conn.request('GET','UI/HOUSEID')
conn.getresponse();
print conn.request('GET','UI/USERID')
conn.getresponse();

#Method to get all log entries (actions) for a given location
print conn.request('GET','AL/USERID/TIMEFRAME/HOUSEID*/ROOMID*/')
conn.getresponse();

#Method to get all log entries (actions) by device type
print conn.request('GET','AT/USERID/TIMEFRAME/DEVICETYPE/HOUSEID/ROOMID/')
conn.getresponse();

#Method to get all log entries (actions) by device ID
print conn.request('GET','AI/USERID/TIMEFRAME/DEVICEID/HOUSEID/ROOMID/')
conn.getresponse();

#Method to get all computer (predictive algorithm) log entries by location
print conn.request('GET','CL/USERID/TIMEFRAME/HOUSEID/ROOMID/')
conn.getresponse();

#Method to get all computer (predictive algorithm) log entries by type
print conn.request('GET','CT/USERID/TIMEFRAME/DEVICETYPE/HOUSEID/ROOMID/')
conn.getresponse();

#Method to get all computer (predictive algorithm) log entries by device ID
print conn.request('GET','CI/USERID/TIMEFRAME/DEVICEID/HOUSEID/ROOMID/')
conn.getresponse();


""" PROCESSING OF DATA """



""" OUTGOING CALL TO PERSISTENT STORAGE """

#Method to post information about devices
print conn.request('POST','D/HOUSEID/VER/ROOM/DEVICE/')
conn.getresponse();

#Method to post information about rooms
print conn.request('POST','R/HOUSEID/VER/ROOM/')
conn.getresponse();

#Method to post information about houses
print conn.request('POST','H/HOUSEID/')
conn.getresponse();

#Method to post information about users
print conn.request('POST','U/USERID/')
conn.getresponse();



"""
resp = conn.request('GET', 'HD/HOUSEID/')
data = resp.read()
print resp
print data

data1 = json.loads(data)
print data1


#import httplib
conn = httplib.HTTPConnection("www.python.org")
conn.request("GET", "/index.html")
r1 = conn.getresponse()
print r1.status, r1.reason
data1 = r1.read()

print data1
#conn.close()
"""
