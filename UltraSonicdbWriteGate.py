#!/usr/bin/python

# Written By Johnathan Cintron and Devlyn Courtier
# Copyright (c) 2016

import sys
import time, MySQLdb
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
		curr_date = time.strftime("%Y-%m-%d")
		curr_time = time.strftime("%H:%M:%S")

		GPIO.output(TRIG, False)
		time.sleep(0.5)

		GPIO.output(TRIG, True)
		time.sleep(0.00001)
		GPIO.output(TRIG, False)

		while GPIO.input(ECHO) == 0:
			pulse_start = time.time()

		while GPIO.input(ECHO) == 1:
			pulse_end = time.time()

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

		#if any( [int(time.strftime("%H")) == 8, int(time.strftime("%H")) == 15, int(time.strftime("%H")) == 22] ) and (int(time.strftime("%M")) == 0):
		if any( [time.strftime("%M") == "00", int(time.strftime("%M")) == 10, int(time.strftime("%M")) == 20, int(time.strftime("%M")) == 30, int(time.strftime("%M")) == 40, int(time.strftime("%M")) == 50]) and (time.strftime("%S") == "00"):
			try:
				# Create SQL Query
				sql = "INSERT INTO ULTRASTATS (date, time, gatecount) VALUES ('%s', '%s', '%d')" % (curr_date, curr_time, count)
				# Execute the SQL command
				cursor.execute(sql)
				# Commit your changes in the database
				db.commit()
			except:
				# Rollback in case there is any error
				db.rollback()

		time.sleep(0.5)
except KeyboardInterrupt:
	db.close()
	print("\nCtrl-C pressed cleaning up GPIO")
	GPIO.cleanup()
	sys.exit(0)
