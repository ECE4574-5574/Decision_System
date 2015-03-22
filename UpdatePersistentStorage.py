/*Prerana Rane*/
/*Learned behaviours will be stored in the Persistent Storage in the form of Device States*/

import sqlite3

conn = sqlite3.connect('device.sqlite3')
cur = conn.cursor()

cur.execute('INSERT INTO Devices (DeviceID,State, timestamp) VALUES ( ?, ?, ?)', 
    ( 'Light', 'ON', sysdate ) )
cur.execute('UPDATE Devices (DeviceID,State, timestamp)  VALUES ( ?, ? )', 
    ( 'Light', 'OFF', sysdate ) )
conn.commit()

print 'Tracks:'
cur.execute('SELECT DeviceID,State, timestamp FROM Devices')
for row in cur :
   print row

conn.commit()

cur.close()
