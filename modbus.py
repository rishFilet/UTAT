#common register numbers:
#read temperature - 100

import dummy_serial
import minimalmodbus
import time
import serial

class thermalCycle:


    minimalmodbus.serial.Serial = dummy_serial.Serial
    # instrument.write_register(600,1,0) #0 for thermocouple, 1 for RTD, 2 for process
    # instrument.write_register(601,0,0) #0 for DIN (European thermocouple standard), 1 for JIS (Japanese standard)
    # instrument.write_register(606,1,0) #set the position of decimal places in the controller to 1 (0.0)
    # instrument.write_register(901,1,0) #sets unit to Celsius
    # instrument.write_register(500,0,0) #switches control method to On/Off
    # instrument.write_register(1100,2,0) #sets ramping mode to "At start and at set point changes"
    # instrument.write_register(1102,0,0) #sets ramping scale to minutes (1 would be for hours)
    # instrument.write_register(507,1,1) #sets hysteresis (maximum deviation) to 1 degree Celsius

    def __init__(self,name, cycles, testTime, soak,hi_lim,lo_lim):
        self.name = name
        self.cycles = cycles
        self.testTime = testTime
        self.soak = soak
        self.hi_lim = hi_lim
        self.lo_lim = lo_lim
        self.instrument = minimalmodbus.Instrument('DUMMYPORTNAME', 1) # port name, slave address (in decimal)

    def commSetup(self):
        self.instrument.serial.baudrate = 9600
        self.instrument.serial.bytesize = 8
        self.instrument.serial.parity   = serial.PARITY_NONE
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout  = 0.2
        self.instrument.mode = minimalmodbus.MODE_RTU

    def setRampRate(self, rate): #sets ramp rate in degrees Celsius per minute
        self.instrument.write_register(1101,rate,1)

    def setTemp(self,temp): #sets set point to specified temperature
        self.instrument.write_register(300,temp,1)

    def getTemp(self):
        return self.instrument.read_register(100,1)

    def getSetpoint(self):
        return self.instrument.read_register(300,temp,1)

    def getRampRate(self): #sets ramp rate in degrees Celsius per minute
        return self.instrument.read_register(1101,rate,1)

    def runCycle(cycles, testTime, soak):
        hi_lim = self.hi_lim
        lo_lim = self.lo_lim
        currCycle = 0
        print(name+" cylce started at at "+ time.asctime())
        while currCycle < cycles:
            print("Ramping up to "+ hi_lim)
            self.setTemp(hi_lim)
            print("Temperature " + hi_lim + " reached at "+ time.asctime())
            time.sleep(soak*60)
            print("Ramping down to "+ loi_lim)
            self.setTemp(lo_lim)
            print("Temperature " + lo_lim + " reached at "+ time.asctime())
            time.sleep(soak*60)
        self.setTemp(23)
        while self.getTemp >= 23:
            if self.getTemp == 23:
                print("Cycle complete, Room temperature reached")
                print("Perform safety check and turn off thermal chamber before removing test subject")

class checks:

    def __init__(self):
        self.answer = self.setAnswer

    def dryRun(self):
        while self.answer != "y" and self.answer != "Y":
            self.answer = raw_input("Has a dry run functional test been performed?")
        self.answer = self.setAnswer

    def safety(self):
        while self.answer != "y" and self.answer != "Y":
            self.answer = raw_input("Have safety checks been performed?")
            print("Please go through this list")
            print("List of safety checks:")
        self.answer = self.setAnswer

    def setAnswer(self):
        return "no"

name = raw_input("What is the name of the cycle test?")
cycles = raw_input("How many cycles will the test undergo?")
hi_lim = raw_input("What is the upper limit temp?")
lo_lim = raw_input("What is the lower limit temp?")
testTime = raw_input("What is the total test time in hours?")
soak = raw_input("What is the time of each soak in minutes?")

cyc = thermalCycle(name,cycles,testTime,soak,hi_lim,lo_lim)
cyc.commSetup()

current_temp = cyc.getTemp()
current_setpoint = cyc.getSetpoint()
current_ramp = cyc.getRampRate()
instrument = cyc.instrument()

print("instrument:")
print(instrument)
print("Current Temp: ")
print(current_temp)
print("Current setpoint: ")
print(current_setpoint)

check = checks()
print(check.answer())
check.dryRun()
check.safety()

#TODO
#Create logging file of errors, start time, date and starting setpoint. Also log when the setpoints have been reached and how long they have stayed at that setpoint and time of ramping
#Ramp up/down to setpoint, log, start timer, repeat until no. of cycles and time has been reached
cyc.runCycle()
#Send alerts to notify engineer that the cycles are complete
#Ask for safety checks
check.safety()
check.dryRun()


# print(instrument.read_register(209,0)
#
# startup()
# setRampRate(5)
# setTemp(25)
# for i in range(0,20):
#  print(getTemp())
#  time.sleep(1)
