#!/usr/bin/python

import sys
import time
import datetime
import gspread
from BMP085 import BMP085
import subprocess
import re

# ===========================================================================
# Google Account Details
# ===========================================================================

# Account details for google docs
email = 'you@gmail.com'
password = '$hhh!'
spreadsheet = 'OPV Vacuum'

# ===========================================================================
# Example Code
# ===========================================================================

bmp = BMP085(0x77)


# Login with your Google account
try:
  gc = gspread.login(email, password)
except:
  print "Unable to log in. Check your email address/password"
  sys.exit()

# Open a worksheet from your spreadsheet using the filename
try:
  worksheet = gc.open(spreadsheet).sheet1
  # Alternatively, open a spreadsheet using the spreadsheet's key
  # worksheet = gc.open_by_key('0BmgG6nO_6dprdS1MN3d3MkdPa142WFRrdnRRUWl1UFE')
except:
  print "Unable to open the spreadsheet. Check your filename: %s" % spreadsheet
  sys.exit()



# Continuously append data
while(True):

  # Run the DHT program to get the humidity and temperature readings!

  output_dht = subprocess.check_output(["./DHT", "2302", "4"]);
#  print output_dht
  matches = re.search("Temp =\s+([0-9.]+)", output_dht)
  if (not matches):
    time.sleep(3)
    continue
  temp_dht = float(matches.group(1))
  
  # search for humidity printout
  matches = re.search("Hum =\s+([0-9.]+)", output_dht)
  if (not matches):
    time.sleep(3)
    continue
  humidity = float(matches.group(1))

  print "From DHT22"
  print "\tTemperature: %.1f C" % temp_dht
  print "\tHumidity: %.1f %%" % humidity


  temp_bmp = bmp.readTemperature()
  pressure = bmp.readPressure()
  altitude = bmp.readAltitude()

  print "From BMP085"
  print "\tTemperature: %.2f C" % temp_bmp
  print "\tPressure: %.2f hPa" % (pressure / 100.0)
  print "\tAltitude: %.2f" % altitude

  # Append the data in the spreadsheet, including a timestamp
  try:
    values = [datetime.datetime.now(), temp_dht, humidity, temp_bmp, pressure, altitude]
    worksheet.append_row(values)
  except:
    print "Unable to append data. Check your connection?"
    sys.exit()

  # Wait 5 seconds before continuing
  print "Wrote a row to %s \n" % spreadsheet
  time.sleep(5)
