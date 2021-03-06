#Tests the functions for PersistentStorageFunctions
#Contributors : Luke Lapham, Sumit Kumar
#Date : 3/30/2015
#Last modified: 4/20/2015
#Note: This test assumes that you have a persistent storage server running on your desktop.
import unittest
import PersistentStorageFunctions as PSF
import argparse
from time import sleep

open('getRequests.log', 'w').close()

argparser = argparse.ArgumentParser()
argparser.add_argument('-t', '--storage', type=str)
argparser.add_argument('-p', '--port', type=int)

args = argparser.parse_args()

try: 
    DUT = PSF.PersistentStorageFunctions(args.storage, args.port)
except:
   print "\n"
try: 
    DUT.getRoomsInHouse(54321)
except:
    print "\n"
try: 
    DUT.getDevicesInHouse(54321)
except:
    print "\n"
try:
    DUT.getDevicesInRoom(54321, 12345)
except:
    print "\n"
try:
    DUT.getDevice(54321, 12345, 67890)
except:
    print "\n"
try:
    DUT.getDevicesInHouseOfType(12345, "light")
except:
    print "\n"
try:
    DUT.getDevicesInRoomOfType(12345, 54321, "light")
except:
    print "\n"
try:
    DUT.getUserInfo(12)
except:
    print "\n"
try:
    DUT.getRoomInfo(12345, 54321)
except:
    print "\n"
try:
    DUT.getDeviceInfo(12345, 54321, 67890)
except:
    print "\n"
try:
    DUT.getAuthentication("bob", "thePW")
except:
    print "\n"
try:
    DUT.getUserDeviceToken(12)
except:
    print "\n"
try:
    DUT.getUserActions(12, "2015-04-06T18:05:05Z/2015-04-06T18:05:05Z", 12345, 54321)
except:
    print "\n"
try:
    DUT.getComputerActions(21, "2015-04-06T18:05:05Z/2015-04-06T18:05:05Z", 12345, 54321)
except:
    print "\n"

log = open('getRequests.log', 'r')
print "getRoomsInHouse()"
line = log.readline()
if line == "/HD/54321/\n":
    print "PASS\n"
else:
    print "FAIL"
print "getDevicesInHouse()"
line = log.readline()
if line == "/HD/54321/\n":
    print "PASS\n"
else:
    print "FAIL"
print "getDevicesInRoom()"
line = log.readline()
if line == "/RD/54321/12345/\n":
    print "PASS\n"
else:
    print "FAIL"
print "getDevice()"
line = log.readline()
if line == "/DD/54321/12345/67890/\n":
    print "PASS\n"
else:
    print "FAIL"
print "getDevicesInHouseOfType()"
line = log.readline()
if line == "/HT/12345/light/\n":
    print "PASS\n"
else:
    print "FAIL"
print "getDevicesInRoomOfType()"    
line = log.readline()
if line == "/RT/12345/54321/light/\n":
    print "PASS\n"
else:
    print "FAIL"
print "getUserInfo()"
line = log.readline()
if line == "/BU/12/\n":
    print "PASS\n"
else:
    print "FAIL"
print "getRoomInfo()"
line = log.readline()
if line == "/BR/12345/54321/\n":
    print "PASS\n"
else:
    print "FAIL"
print "getDeviceInfo()"
line = log.readline()
if line == "/BD/12345/54321/67890/\n":
    print "PASS\n"
else:
    print "FAIL"
print "getAuthentication()"
line = log.readline()
if line == "/IU/bob/thePW/\n":
    print "PASS\n"
else:
    print "FAIL"
print "getUserDeviceToken()"
line = log.readline()
if line == "/TU/12/\n":
    print "PASS\n"
else:
    print "FAIL"
print "getUserActions()"
line = log.readline()
if line == "/AL/12/2015-04-06T18:05:05Z/2015-04-06T18:05:05Z/12345/54321/0/0/\n":
    print "PASS\n"
else:
    print "FAIL"
print "getComputerActions()"
line = log.readline()
if line == "/CL/21/2015-04-06T18:05:05Z/2015-04-06T18:05:05Z/12345/54321/0/0/\n":
    print "PASS\n"
else:
    print "FAIL"



