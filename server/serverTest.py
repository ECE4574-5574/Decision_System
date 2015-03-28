from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import requests
import json

url = 'https://25.39.122.197:8080'

parameters = {
'GET': 'HD'
}

response = requests.get(url, params=parameters)

data = response.json()

print data