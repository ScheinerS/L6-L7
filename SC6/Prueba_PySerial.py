#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prueba de PySerial.

VER:    https://www.youtube.com/watch?v=IKsYlkqzqR0
"""


import serial
import serial.tools.list_ports as port_list


ports = list(port_list.comports())
print('Ports:')
for p in ports: print (p)


#Can be Downloaded from this Link
#https://pypi.python.org/pypi/pyserial

#Global Variables
ser = 0

#Function to Initialize the Serial Port
def init_serial():
    COMNUM = 1          #Enter Your COM Port Number Here.
    global ser          #Must be declared in Each Function
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = COMNUM - 1   #COM Port Name Start from 0
    
    #ser.port = '/dev/ttyUSB0' #If Using Linux

    #Specify the TimeOut in seconds, so that SerialPort
    #Doesn't hangs
    ser.timeout = 10
    ser.open()          #Opens SerialPort

    # print port open or closed
    if ser.isOpen():
        print('Open: ' + ser.portstr)
#Function Ends Here
        

#Call the Serial Initilization Function, Main Program Starts from here
init_serial()

temp = input('Type what you want to send, hit enter:\r\n')
ser.write(temp)         #Writes to the SerialPort

while 1:    
    bytes = ser.readline()  #Read from Serial Port
    print ('You sent: ' + bytes)    # Print What is Read from Port
    
#Ctrl+C to Close Python Window

