#!/usr/bin/python


# Written By Johnathan Cintron and Devlyn Courtier
# Copyright (c) 2016

#import time, MySQLdb

import sys
import MySQLdb
from datetime import datetime
from time import sleep

# Import Adafruit Libraries
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Set LDR constant
#lrdConst = "25"

# Set current date and time
# count = int(sys.argv[1])

count = 0

# Hardware SPI config
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

try:
	while True:
		curr_date = datetime.now().strftime("%Y-%m-%d")
		curr_time = datetime.now().strftime("%H:%M:%S")

		# Read current LDR value from ADC
		#curr_ldr = mcp.read_adc(0)
		#print mcp.read_adc(0)
		# Check if current ldr value is less than or greater than ldrConst
		if mcp.read_adc(0) > 150:
			count = count + 1

		# Open database connection
		db = MySQLdb.connect("HOSTNAME","USERNAME","PASSWORD","DATABASE")

		# prepare a cursor object using cursor() method
		cursor = db.cursor()

		# Prepare SQL query to INSERT a record into the database.
		sql = "INSERT INTO LDRSTATS (date, time, gatecount) VALUES ('%s', '%s', '%d')" % (curr_date, curr_time, count)

		if any( [datetime.now().strftime("%M") == "00", int(datetime.now().strftime("%M")) == 10, int(datetime.now().strftime("%M")) == 20, int(datetime.now().strftime("%M")) == 30, int(datetime.now().strftime("%M")) == 40, int(datetime.now().strftime("%M")) == 50] ) and (datetime.now().strftime("%S") == "00"):
			try:
				# Execute the SQL command
				cursor.execute(sql)
				# Commit your changes in the database
				db.commit()
			except:
				# Rollback in case there is any error
				db.rollback()

		# Disconnect from database server
		db.close()

		# Pause for three tenths of a second (will adjust later to find good timing)
		sleep(0.33)
except KeyboardInterrupt:
	print("\nCtr-C pressed cleaning up GPIO")
	sys.exit(0)
