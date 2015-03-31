"""API Calls to and from the Persistent Storage
Contributors : Prerana Rane
Date : 3/30/2015
Purpose : Receiving HTTP Responses for GET and POST methods sent to the server.
Method of Testing: On running this file, the GET and POST commands issued can be seen on the AWS server. Alternatively, 
change the URL to 'localhost', run the persistent_storage_server.py file (from the Persistent Storage Team) and then 
run this file"""



import requests
import json
import httplib
import decisions
#COnnection to the server is established
#URL provided by Persistent Storage team 
conn = httplib.HTTPConnection('54.152.190.217', 8080)

""" INCOMING DATA FROM PERSISTENT STORAGE """

#Method to get all devices in a specific house
print conn.request('GET','HD/HOUSE47/') #Currently receives dummy data stored in persistent storage
r1 = conn.getresponse();
print r1.status, r1.reason               #Displays status of command                 
d1 = r1.read()
print json.loads(d1)                     #prints data in JSON format
"""Currently this data will not be used for any learning decision. When the learning system is in place, the data received
will have to be sent to the Decision system to generate an action"""
decisions.randomDecision()  

#Method to get all devices in a specific room (for a certain house)
print conn.request('GET','RD/HOUSEID/ROOMID/')  #Currently receives dummy data stored in persistent storage
r1 = conn.getresponse();
print r1.status, r1.reason
d1 = r1.read()
print json.loads(d1)               #prints data in JSON format
"""Currently this data will not be used for any learning decision. When the learning system is in place, the data received
will have to be sent to the Decision system to generate an action"""
decisions.randomDecision()

#Method to get devices of a specific type in a specific house
print conn.request('GET','HT/HOUSEID/TYPE')  #Currently receives dummy data stored in persistent storage
r1 = conn.getresponse();
print r1.status, r1.reason
d1 = r1.read()
print json.loads(d1)                          #prints data in JSON format
"""Currently this data will not be used for any learning decision. When the learning system is in place, the data received 
will have to be sent to the Decision system to generate an action"""
decisions.randomDecision()

#Method to get devices of a specific type in a specific room (for a certain house)
print conn.request('GET','RT/HOUSEID/ROOMID/TYPE/')  #Currently receives dummy data stored in persistent storage
r1 = conn.getresponse();
print r1.status, r1.reason
d1 = r1.read()
print json.loads(d1)        #prints data in JSON format
"""Currently this data will not be used for any learning decision. When the learning system is in place, the data received
will have to be sent to the Decision system to generate an action"""
decisions.randomDecision()

#Methods to user information (accesses information from the users profile)
print conn.request('GET','UI/HOUSEID/')  #Currently receives dummy data stored in persistent storage
r1 = conn.getresponse();
print r1.status, r1.reason
d1 = r1.read()
print json.loads(d1)            #prints data in JSON format
"""Currently this data will not be used for any learning decision. When the learning system is in place, the data received
will have to be sent to the Decision system to generate an action"""
decisions.randomDecision()
print conn.request('GET','UI/USERID/')  #Currently receives dummy data stored in persistent storage
r1 = conn.getresponse();
print r1.status, r1.reason
d1 = r1.read()
print json.loads(d1)     #prints data in JSON format
"""Currently this data will not be used for any learning decision. When the learning system is in place, the data received
will have to be sent to the Decision system to generate an action"""
decisions.randomDecision()

#Method to get all log entries (actions) for a given location
print conn.request('GET','AL/USERID/TIMEFRAME/HOUSEID*/ROOMID*/')  #Currently receives dummy data stored in persistent storage
r1 = conn.getresponse();
print r1.status, r1.reason
d1 = r1.read()
print json.loads(d1)    #prints data in JSON format
"""Currently this data will not be used for any learning decision. When the learning system is in place, the data received 
will have to be sent to the Decision system to generate an action"""
decisions.randomDecision()

#Method to get all log entries (actions) by device type
print conn.request('GET','AT/USERID/TIMEFRAME/DEVICETYPE/HOUSEID/ROOMID/')  #Currently receives dummy data stored in persistent storage
r1 = conn.getresponse();
print r1.status, r1.reason
d1 = r1.read()
print json.loads(d1)   #prints data in JSON format
"""Currently this data will not be used for any learning decision. When the learning system is in place, the data received will have
to be sent to the Decision system to generate an action"""
decisions.randomDecision()

#Method to get all log entries (actions) by device ID
print conn.request('GET','AI/USERID/TIMEFRAME/DEVICEID/HOUSEID/ROOMID/')  #Currently receives dummy data stored in persistent storage
r1 = conn.getresponse();
print r1.status, r1.reason
d1 = r1.read()
print json.loads(d1)    #prints data in JSON format
"""Currently this data will not be used for any learning decision. When the learning system is in place, the data received will have
to be sent to the Decision system to generate an action"""
decisions.randomDecision()

#Method to get all computer (predictive algorithm) log entries by location
print conn.request('GET','CL/USERID/TIMEFRAME/HOUSEID/ROOMID/')  #Currently receives dummy data stored in persistent storage
r1 = conn.getresponse();
print r1.status, r1.reason
d1 = r1.read()
print json.loads(d1)    #prints data in JSON format
"""Currently this data will not be used for any learning decision. When the learning system is in place, the data received will have
to be sent to the Decision system to generate an action"""
decisions.randomDecision()

#Method to get all computer (predictive algorithm) log entries by type
print conn.request('GET','CT/USERID/TIMEFRAME/DEVICETYPE/HOUSEID/ROOMID/')  #Currently receives dummy data stored in persistent storage
r1 = conn.getresponse();
print r1.status, r1.reason
d1 = r1.read()
print json.loads(d1)    #prints data in JSON format
"""Currently this data will not be used for any learning decision. When the learning system is in place, the data received will have
to be sent to the Decision system to generate an action"""
decisions.randomDecision()

#Method to get all computer (predictive algorithm) log entries by device ID
print conn.request('GET','CI/USERID/TIMEFRAME/DEVICEID/HOUSEID/ROOMID/')  #Currently receives dummy data stored in persistent storage
r1 = conn.getresponse();
print r1.status, r1.reason
d1 = r1.read()
print json.loads(d1)    #prints data in JSON format
"""Currently this data will not be used for any learning decision. When the learning system is in place, the data received will have
to be sent to the Decision system to generate an action"""
decisions.randomDecision()

""" OUTGOING CALL TO PERSISTENT STORAGE """

#Method to post information about devices
print conn.request('POST','D/HOUSEID/VER/ROOM/DEVICE/') #Issues a POST command, currently there is no action generated, hence there is no data sent.
r1 = conn.getresponse();
print r1.status, r1.reason                     #Receives a response

#Method to post information about rooms
print conn.request('POST','R/HOUSEID/VER/ROOM/') #Issues a POST command, currently there is no action generated, hence there is no data sent
r1 = conn.getresponse();
print r1.status, r1.reason

#Method to post information about houses
print conn.request('POST','H/HOUSEID/') #Issues a POST command, currently there is no action generated, hence there is no data sent
r1 = conn.getresponse();
print r1.status, r1.reason

#Method to post information about users
print conn.request('POST','U/USERID/') #Issues a POST command, currently there is no action generated, hence there is no data sent
r1 = conn.getresponse();
print r1.status, r1.reason
