#! /usr/bin/python
# coding:utf-8
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0
import sys 
import os
from gps import *
from time import *
import time
import threading
import commands
import psycopg2
 
gpsd = None #seting the global variable
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

class DBExecute:
  def run(self,val1,val2):
     conn = psycopg2.connect("dbname=pgis host=localhost user=postgres password=postgres")
     cur = conn.cursor()
     cur.execute("""
SELECT '現在の住所は'||pref_name||city_name||street_name||address||'番地付近です' 
FROM address 
WHERE ST_DWithin(geom2,ST_GeomFromText('POINT(139.802933333 35.788736667)',4326),1000) 
ORDER BY ST_Distance(geom2,ST_GeomFromText('POINT(139.802933333 35.788736667)',4326)) limit 1;
     """)
     ret = cur.fetchone()
     cur.close()

     return ret
 
if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
 
      if gpsd.fix.latitude and gpsd.fix.longitude:
          sql = DBExecute()
          print "%s %s" %(gpsd.fix.longitude,gpsd.fix.latitude)
          ret = sql.run(gpsd.fix.latitude,gpsd.fix.longitude)
          sys.exit(0)
      time.sleep(5) #set to whatever
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing

  str = ret[0].encode('utf-8')
  print str
  cmd = "./jsay " + str
  os.system(cmd)
