#if this doesnt work, add 40001 to every modbus register

import minimalmodbus
import time

def startup():
 instrument.write_register(600,1,0) #0 for thermocouple, 1 for RTD, 2 for process
 instrument.write_register(601,0,0) #0 for DIN (European thermocouple standard), 1 for JIS (Japanese standard)
 instrument.write_register(606,1,0) #set the position of decimal places in the controller to 1 (0.0)
 instrument.write_register(901,1,0) #sets unit to Celsius
 instrument.write_register(500,0,0) #switches control method to On/Off
 instrument.write_register(1100,2,0) #sets ramping mode to "At start and at set point changes"
 instrument.write_register(1102,0,0) #sets ramping scale to minutes (1 would be for hours)
 instrument.write_register(507,1,1) #sets hysteresis (maximum deviation) to 1 degree Celsius

def setRampRate(rate): #sets ramp rate in degrees Celsius per minute
 instrument.write_register(1101,rate,1)

def setTemp(temp): #sets set point to specified temperature
 instrument.write_register(300,temp,1)
 
def getTemp():
 return instrument.read_register(1500,1)


instrument = minimalmodbus.Instrument('/dev/ttyUSB1', 1) # port name, slave address (in decimal)
startup()
while True:
 print(getTemp)
 time.sleep(3)