from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import requests
import json
import httplib


"""
#url = 'https://25.39.122.197:8080'
url = 'https://172.31.215.239:8080' #Luke's IP

parameters = {
    'path': 'HD/house47/'
}
"""

conn = httplib.HTTPConnection('172.31.215.239', 8080)
conn.request('GET', 'HD/HOUSEID/')
resp = conn.getresponse();	
conn.request('GET', 'RD/HOUSEID/ROOMID/')
resp = conn.getresponse();	
conn.request('GET', 'HT/HOUSEID/TYPE')
resp = conn.getresponse();	
conn.request('GET', 'RT/HOUSEID/ROOMID/TYPE')
resp = conn.getresponse();	
data = resp.read()
conn.request('POST', 'R/house2022/15/atrium/')
resp1 = conn.getresponse()

#data = resp.json()

print resp
print resp1
print data
#resp = requests.get(url, params=parameters)


#data = resp.json()

#print data
