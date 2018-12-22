#common register numbers:
#read temperature - 100

#import dummy_serial
import minimalmodbus
import time
import serial

class thermalCycle:


    #minimalmodbus.serial.Serial = dummy_serial.Serial


    def __init__(self,name, cycles, soak,hi_lim,lo_lim):
        self.name = name
        self.cycles = cycles
        self.soak = soak
        self.hi_lim = hi_lim
        self.lo_lim = lo_lim
        self.instrument = minimalmodbus.Instrument('/dev/ttyUSB0', 1) # port name, slave address (in decimal)


    def commSetup(self):
        self.instrument.serial.baudrate = 9600
        self.instrument.serial.bytesize = 8
        self.instrument.serial.parity   = serial.PARITY_NONE
        self.instrument.serial.stopbits = 1
        self.instrument.serial.timeout  = 0.3
        self.instrument.mode = minimalmodbus.MODE_RTU

    def instrumentSetup(self):
        self.instrument.write_register(600,1,0) #0 for thermocouple, 1 for RTD, 2 for process
        self.instrument.write_register(601,0,0) #0 for DIN (European thermocouple standard), 1 for JIS (Japanese standard)
        self.instrument.write_register(606,1,0) #set the position of decimal places in the controller to 1 (0.0)
        self.instrument.write_register(901,1,0) #sets unit to Celsius
        self.instrument.write_register(500,0,0) #switches control method to On/Off
        self.instrument.write_register(1100,2,0) #sets ramping mode to "At start and at set point changes"
        self.instrument.write_register(1102,0,0) #sets ramping scale to minutes (1 would be for hours)
        self.instrument.write_register(507,1,1) #sets hysteresis (maximum deviation) to 1 degree Celsius

    def setRampRate(self, rate): #sets ramp rate in degrees Celsius per minute
        self.instrument.write_register(1101,rate,1)

    def setTemp(self,temp): #sets set point to specified temperature
        self.instrument.write_register(300,temp,1)

    def getTemp(self):
        return self.instrument.read_register(100,1)

    def getSetpoint(self):
        return self.instrument.read_register(300,1)

    def getRampRate(self): #sets ramp rate in degrees Celsius per minute
        return self.instrument.read_register(1101,1)

    def runCycle(self,cycles, soakTime):
        hi_lim = int(self.hi_lim)
        lo_lim = int(self.lo_lim)
        soak = int(soakTime)
        currCycle = 0
        temp = self.getTemp()
        print(name+" cylce started at at "+ time.asctime())
        startTime = time.asctime()
        while currCycle < int(cycles):
            print("Ramping up to {} ".format(hi_lim))
            self.setTemp(hi_lim)
            while temp < hi_lim:
                temp=self.getTemp()
            print("Temperature {} reached at {}".format(hi_lim,time.asctime()))
            time.sleep(soak*60)
            print("Ramping down to {}".format(lo_lim))
            self.setTemp(lo_lim)
            while temp > lo_lim:
                temp=self.getTemp()
            print("Temperature {} reached at {}".format(lo_lim,time.asctime()))
            time.sleep(soak*60)
            currCycle+=1
        self.setTemp(23)
        while self.getTemp >= 23:
            if self.getTemp == 23:
                print("Cycle complete, Room temperature reached")
                print("Total Test time elapsed: {}".format(time.asctime()-startTime))
                print("Perform safety check and turn off thermal chamber before removing test subject")

class checks:

    def __init__(self):
        self.answer = self.setAnswer()

    def dryRun(self):
        while self.answer != "y" and self.answer != "Y":
            self.answer = input("Has a dry run functional test been performed?[y/n]")
        self.answer = self.setAnswer()

    def safety(self):
        while self.answer != "y" and self.answer != "Y":
            self.answer = input("Have safety checks been performed?[y/n]")
            print("Please go through this list")
            print("List of safety checks:")
        self.answer = self.setAnswer()

    def setAnswer(self):
        return "no"

name = input("What is the name of the cycle test?")
cycles = input("How many cycles will the test undergo?")
hi_lim = input("What is the upper limit temp?")
lo_lim = input("What is the lower limit temp?")
soak = input("What is the time of each soak in minutes?")

cyc = thermalCycle(name,cycles,soak,hi_lim,lo_lim)
check = checks()

cyc.commSetup()
#instrument = cyc.instrumentSetup()
#print("instrument:")
#print(instrument)

current_temp = cyc.getTemp()
print("Current Temp: ")
print(current_temp)
current_setpoint = cyc.getSetpoint()
current_ramp = cyc.getRampRate()
print("Current setpoint: ")
print(current_setpoint)

print("Current ramp rate: ")
print(current_ramp)

check.dryRun()
check.safety()

#TODO
#Create logging file of errors, start time, date and starting setpoint. Also log when the setpoints have been reached and how long they have stayed at that setpoint and time of ramping
#Ramp up/down to setpoint, log, start timer, repeat until no. of cycles and time has been reached
#Add hysterisis for the temperature so that it does not have to reach to the exact temperatures before the soak is started

cyc.runCycle(cycles, testTime, soak)
#Send alerts to notify engineer that the cycles are complete
#Ask for safety checks
check.safety()
check.dryRun()
