#!/usr/bin/python
#
## @file
#
# SOLA using RS-232.
#
# Yuan 06/20/2022
#


import time
import serial
import storm_control.sc_hardware.serial.RS232 as RS232

## SOLA
#
# This class encapsulates control of a lumencor light engine SOLA via RS-232
#
#

class SOLA(RS232.RS232):
    ## __init__
    #
    # @param port (Optional) The com port, defaults to "COM3".
    # @param baud (Optional) The baud rate, defaults to 9600.
    #
    def __init__(self, port = "COM3", baud = 9600):
        try:
            # open port
            RS232.RS232.__init__(self, port=port, baudrate=baud, end_of_line='', timeout=0.05, wait_time=0.05)

            # Initialization
            init1 = "5702FF50"   # set up GPIO0-3
            init2 = "5703FD50"   # set up GPIO5-7
            self.sendCommand(init1)
            self.sendCommand(init2)
            # TODO: check if it respond on initiation
            assert not(self.commWithResp("53470250") == None)
        except:
            self.live = 0
            print("Failed to connect to the SOLA light engine at port", port)

    def write(self, string):
        self.tty.write(bytes.fromhex(string))

    # return the IIC Temp Sensor
    def getTemperature(self):
        self.sendCommand("53910250")
        tmp = self.tty.readline()
        return int(tmp[2:],16)/256

    # IIC DAC Intensity Control
    def setIntensity(self, intensity):
        intensity = 255-intensity
        cmd = "53180304F" + format(intensity, '02x') + "050"   
        self.sendCommand(cmd)

    # Channel Enable / Disable
    def setOnOff(self, on):
        if on:
            self.sendCommand("4F7D50")
        else:
            self.sendCommand("4F7F50")

    # Set Default intensity
    def setDefault(self, intensity):
        cmd = "52460201" + format(intensity, '02x') + "50"
        self.sendCommand(cmd)



