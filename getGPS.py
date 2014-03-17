#! /usr/bin/python
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
 
#os.system('clear') #clear the terminal (optional)
 
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
         SELECT * FROM
         (
         SELECT
         prefecture,city,area,rtrim(jiban) as banchi,X(geom) as lng,Y(geom) as lat,
         distance_spheroid(
         geom,
         GeometryFromText('POINT(%s %s)',4326),
         'SPHEROID["GRS_1980",6378137,298.257222101]'
         ) AS KYORI FROM geos
         where
         distance_spheroid(geom,GeometryFromText('POINT(%s %s)',4326),'SPHEROID["GRS_1980",6378137,298.257222101]') < 100
         ) AS GISX
         ORDER BY
         GISX.KYORI;
     """) % (val1,val2,val1,val2)
     ret = cur.fetchone()
     cur.close()
 
if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while True:
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
 
      if gpsd.fix.latitude and gpsd.fix.longitude:
          sql = DBExecute()
          #sql.run(gpsd.fix.latitude,gpsd.fix.longitude)
          print "%s %s" %(gpsd.fix.longitude,gpsd.fix.latitude)
          sys.exit(0)       
      time.sleep(5) #set to whatever
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    #print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  #print "Done.\nExiting."
