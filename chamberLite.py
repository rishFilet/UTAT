import minimalmodbus
import serial


gas = minimalmodbus.Instrument('COM7', 1)
gas.serial.baudrate = 9600  
gas.serial.bytesize = 8
gas.serial.parity   = serial.PARITY_NONE
gas.serial.stopbits = 1
gas.serial.timeout  = 0.2    #This is an important factor in getting readings from the chamber
gas.mode = minimalmodbus.MODE_RTU  


temp = gas.read_register(100, 1)
print (float(temp))
