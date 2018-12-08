#common register numbers:
#read temperature - 100

import minimalmodbus
import time
import serial

def startup():
 c = 0
 instrument.write_register(c+600,1,0) #0 for thermocouple, 1 for RTD, 2 for process
 instrument.write_register(c+601,0,0) #0 for DIN (European thermocouple standard), 1 for JIS (Japanese standard)
 instrument.write_register(c+606,1,0) #set the position of decimal places in the controller to 1 (0.0)
 instrument.write_register(c+901,1,0) #sets unit to Celsius
 instrument.write_register(c+500,0,0) #switches control method to On/Off
 instrument.write_register(c+1100,2,0) #sets ramping mode to "At start and at set point changes"
 instrument.write_register(c+1102,0,0) #sets ramping scale to minutes (1 would be for hours)
 instrument.write_register(c+507,1,1) #sets hysteresis (maximum deviation) to 1 degree Celsius

def setRampRate(rate): #sets ramp rate in degrees Celsius per minute
 c = 0
 instrument.write_register(c+1101,rate,1)

def setTemp(temp): #sets set point to specified temperature
 c = 0
 instrument.write_register(c+300,temp,1)

def getTemp():
 c = 0
 return instrument.read_register(c+100,1)


instrument = minimalmodbus.Instrument('COM7', 1) # port name, slave address (in decimal)
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity   = serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout  = 0.2
instrument.mode = minimalmodbus.MODE_RTU

print(instrument)
print(getTemp())
print(instrument.read_register(209,0)

startup()
setRampRate(5)
setTemp(25)
for i in range(0,20):
 print(getTemp())
 time.sleep(1)
