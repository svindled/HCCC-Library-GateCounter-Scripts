# Written By Johnathan Cintron and Devlyn Courtier for the HCCC Library

#!/usr/bin/python

import sys
import MySQLdb
from time import sleep
from datetime import datetime
import RPi.GPIO as GPIO

# Set RPi GPIO Mode
GPIO.setmode(GPIO.BCM)

# Setup GPIO in and out pins
PIR_PIN = 7
GPIO.setup(PIR_PIN, GPIO.IN)

# End GPIO setup

count = 0

try:
	while True:

		if GPIO.input(PIR_PIN):
			count = count + 1

		#print count

		# Open database connection
		db = MySQLdb.connect("HOSTNAME","USERNAME","PASSWORD","DATABASE")

		# prepare a cursor object using cursor() method
		cursor = db.cursor()

		curr_date = datetime.now()

		# Prepare SQL query to INSERT a record into the database.
		sql = "INSERT INTO PIRSTATS (datetime, gatecount) VALUES ('%s', '%d')" % (curr_date.isoformat(' '), count)


		if (curr_date.minute % 10 == 0) and (curr_date.second == 0):
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

		sleep(1)
except KeyboardInterrupt:
	print ("\nCtrl-C pressed cleaning up GPIO")
	GPIO.cleanup()
	sys.exit(0)
