#!/bin/python

########################################################
# uarmController.py
# Written by Mark Millar
# Date created 2015-01-19
# Date modified 2015-01-19
# Version 0.1
# To use this program, excute with the 
# serial port as argument 1
# E.g. ./uarmController /dev/ttyUSB0
# 
########################################################
# Dependencies:
# - Python 3
# - PySerial
# - Pygame
########################################################

import serial
import sys
import subprocess
import pygame
import time

# Check if there are any user arguments to use
# Select serial port for uarm
if len(sys.argv) > 1:
	# Set user selected serial port
    device = sys.argv[1]
    print('using serial ' + device)
else:
	# Use deflaut serial port to save time
    device = '/dev/ttyUSB0'
    print('using deflaut serial /dev/ttyUSB0')

# Check if device is connected to serial port
try:
	# Connect to the uarm over serial connection
	serial = serial.Serial(device,9600, timeout=10)
	# Set serial baud rate and disable hangup on connection (-hup -hupcl)
	subprocess.call("stty -F " + device + " 9600 ignbrk -brkint -icrnl -imaxbel -opost -onlcr -isig -icanon -iexten -echo -echoe -echok -echoctl -echoke noflsh -ixon -crtscts -hup -hupcl", shell=True)
except serial.serialutil.SerialException:
	# if no device at port return error and continue
	print('uarm not connected, no data will be sent')
	serial = None

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

# Map the max and min values
def mapVal(val,minIn,maxIn,minOut,maxOut):
    return (val-minIn)*(maxOut-minOut)/(maxIn-minIn)+minOut


def main():
	# Start pygame to get controller values
	pygame.init()
	 
	# Start joystick
	joystick = pygame.joystick.Joystick(0)
	joystick.init()

	#Loop until the user clicks the close button.
	done = False

	# Controller deadzone values as percentage
	deadzoneX = 25
	deadzoneY = 25

	# uarm starting point
	posX = 0
	posY = 0
	posZ = 0
	posI = 0
	grip = 0

	# -------- Main Program Loop -----------
	while not done:
	    # EVENT PROCESSING STEP
	    for event in pygame.event.get(): # User did something
	    	# If user clicked close
	        if event.type == pygame.QUIT: 
	            done=True # Flag that we are done so we exit this loop
	            print("Received event 'Quit', exiting.")
	            return
	        elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
	        	print ("Escape key pressed, exiting.")
	        	return
	        # Check for button presses
	        elif event.type == pygame.JOYBUTTONDOWN:
	        	if event.button == 0:
	        		grip = 1
	        	if event.button == 1:
	        		grip = 0

	    # Grab values from controller
	    axisX1 = joystick.get_axis(0)
	    axisY1 = joystick.get_axis(1)

	    axisX2 = joystick.get_axis(3)
	    axisY2 = joystick.get_axis(4)

	    # Convert to percentage
	    axisX1 = axisX1 * 100
	    axisY1 = axisY1 * -100

	    axisX2 = axisX2 * 100
	    axisY2 = axisY2 * -100

	    # Add deadzone to reduce controller sensitivity
	    if axisX1 > -deadzoneX and axisX1 < deadzoneX:
	        axisX1 = 0
	    if axisY1 > -deadzoneY and axisY1 < deadzoneY:
	        axisY1 = 0
	    if axisX2 > -deadzoneX and axisX2 < deadzoneX:
	        axisX2 = 0
	    if axisY2 > -deadzoneY and axisY2 < deadzoneY:
	        axisY2 = 0

	    # Map controller inputs to angles
	    axisX1 = mapVal(axisX1,-100,100,-4,4)
	    axisY1 = mapVal(axisY1,-100,100,-4,4)

	    axisX2 = mapVal(axisX2,-100,100,-4,4)
	    axisY2 = mapVal(axisY2,-100,100,-4,4)

	    # Basic mix calculations
	    posX += axisX1
	    posY += axisY1
	    posZ += axisY2
	    posI += axisX2

	    # Set limits for the uarm position
	    if posX > 90: posX = 90
	    if posX < -90: posX = -90
	    if posY > 210: posY = 210
	    if posY < 0: posY = 0
	    if posZ > 150: posZ = 150
	    if posZ < -180: posZ = -180
	    if posI > 90: posI = 90
	    if posI < -90: posI = -90

	    # Slow the transmittion of data
	    time.sleep(.09)
	    # call the writeDate function with user data
	    writeData(posX, posY, posZ, posI, grip)

	    # debug console
	    print(int(posX))
	    print(int(posY))
	    print(int(posZ))
	    print(int(posI))
	    print(grip)

if __name__ == "__main__":
	main()