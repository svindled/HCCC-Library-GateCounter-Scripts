# Written By Johnathan Cintron and Devlyn Courtier for the HCCC Library

import sys
import MySQLdb
from datetime import datetime
from time import sleep, time
import RPi.GPIO as GPIO

ultraSonicConst = "95"
count = 0

# Set RPi GPIO Mode
GPIO.setmode(GPIO.BCM)

# Set GPIO pins
TRIG = 23
ECHO = 24

# Setup GPIO in and out
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

# End GPIO setup

# Open Database Connection
db = MySQLdb.connect("HOSTNAME","USERNAME","PASSWORD","DATABASE")

# Prepare a cursor object
cursor = db.cursor()

try:
	while True:
		curr_date = datetime.now()

		GPIO.output(TRIG, False)
		sleep(0.5)

		GPIO.output(TRIG, True)
		sleep(0.00001)
		GPIO.output(TRIG, False)

		while GPIO.input(ECHO) == 0:
			pulse_start = time()

		while GPIO.input(ECHO) == 1:
			pulse_end = time()

		pulse_duration = pulse_end - pulse_start

		distance = pulse_duration * 17150

		distance = round(distance, 2)

		if distance < 120:
			count = count + 1

		#print count
		#print distance

		# Open database connection

		# prepare a cursor object using cursor() method

		# Prepare SQL query to INSERT a record into the database.

		if (curr_date.minute % 10 == 0) and (curr_date.second == 0):
			try:
				# Create SQL Query
				sql = "INSERT INTO ULTRASTATS (datetime, gatecount) VALUES ('%s', '%d')" % (curr_date.isoformat(' '), count)
				# Execute the SQL command
				cursor.execute(sql)
				# Commit your changes in the database
				db.commit()
			except:
				# Rollback in case there is any error
				db.rollback()

		sleep(0.5)
except KeyboardInterrupt:
	db.close()
	print("\nCtrl-C pressed cleaning up GPIO")
	GPIO.cleanup()
	sys.exit(0)
