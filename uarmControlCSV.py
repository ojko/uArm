#!/bin/python

########################################################
# uarmControlCSV.py
# Written by Mark Millar
# Date created 2015-01-11
# Date modified 2015-01-14
# Version 0.2
# To use this program, excute with the CSV location as 
# user argument 1 and uarm serial port as argument 2
# E.g. ./uarmControlCSV position.csv /dev/ttyUSB0
#
########################################################
# Dependencies:
# - Python 3
# - PySerial
########################################################

# stty command to stop hangup after command is sent
#stty -F /dev/ttyUSB0 cs8 9600 ignbrk -brkint -icrnl -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke noflsh -ixon -crtscts -hup -hupcl

import serial
import csv
import time
import sys

# Check if there are any user arguments to use
# CSV file for position
if len(sys.argv) > 1:
	# Get user selected CSV file
    csvFile = sys.argv[1]
else:
	# If no CSV file quit program
    print("No CSV selected")
    sys.exit(0)

# Select serial port for uarm
if len(sys.argv) > 2:
	# Set user selected serial port
    device = sys.argv[2]
    print('using serial ' + device)
else:
	# Use deflaut serial port to save time
    device = '/dev/ttyUSB0'
    print('using deflaut serial /dev/ttyUSB0')

# Check if device is connected to serial port
try:
	# Connect to the uarm over serial connection
	serial = serial.Serial(device,9600, timeout=10)
except serial.serialutil.SerialException:
	# if no device at port return error and continue
	print('uarm not connected')
	serial = None

# Check if data is valid
def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# Print data to the serial port and user console
def writeData(armRotation, armLength, armHeight, wristRotation, gripper):
	# convert user inputs to intigers
	armRotation=int(armRotation)
	armLength=int(armLength)
	armHeight=int(armHeight)
	wristRotation=int(wristRotation)
	gripper=int(gripper)

	# set the gripper condition
	if(gripper == 1): gripper = 0x01
	if(gripper == 0): gripper = 0x02

	# Prepare command string as 8 bit hex
	command = bytes([0xFF]) + bytes([0xAA]) + bytes([(armRotation >> 8) & 0xff]) + bytes([armRotation & 0xff]) + bytes([(armLength >> 8) & 0xff]) + bytes([armLength & 0xff]) + bytes([(armHeight >> 8) & 0xff]) + bytes([armHeight & 0xff]) + bytes([(wristRotation >> 8) & 0xff]) + bytes([wristRotation & 0xff]) + bytes([gripper])

	# Print data as hex to console for debug
	print(command)

	# Send data to serial port if device connected
	if serial is not None:
		serial.write(command)

# Open and read CSV file, then pass data to serial handler
def openCSV():
	# open the user selected csv file
	readCSV = csv.reader(open(csvFile), delimiter=',', quotechar='|')

	# Loop through CSV lines 
	for row in readCSV:
		# Set CSV column names
		[armRotationRaw, armLengthRaw, armHeightRaw, wristRotationRaw, gripperRaw] = row
		
		# Print contents of CSV file
		# print(row) 

		# Check if CSV data is a number
		if isNumber(armRotationRaw)&isNumber(armLengthRaw)&isNumber(armHeightRaw)&isNumber(wristRotationRaw)&isNumber(gripperRaw):
			# call the writeDate function with CSV data
			writeData(armRotationRaw, armLengthRaw, armHeightRaw, wristRotationRaw, gripperRaw)

		# Wait a period for the arm to move	
		time.sleep(1)

# main program used to start application
if __name__ == "__main__":
	openCSV() # Call primary program