# Written By Johnathan Cintron and Devlyn Courtier for the HCCC Library

#!/usr/bin/python

import sys
import time, MySQLdb
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

		curr_date = time.strftime("%Y-%m-%d")
		curr_time = time.strftime("%H:%M:%S")


		# Prepare SQL query to INSERT a record into the database.
		sql = "INSERT INTO PIRSTATS (date, time, gatecount) VALUES ('%s', '%s', '%d')" % (curr_date, curr_time, count)


		if any( [time.strftime("%M") == "00", int(time.strftime("%M")) == 10, int(time.strftime("%M")) == 20, int(time.strftime("%M")) == 30, int(time.strftime("%M")) == 40, int(time.strftime("%M")) == 50]) and (time.strftime("%S") == "00"):
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

		time.sleep(1)
except KeyboardInterrupt:
	print ("\nCtrl-C pressed cleaning up GPIO")
	GPIO.cleanup()
	sys.exit(0)
