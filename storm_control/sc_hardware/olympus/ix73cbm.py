#!/usr/bin/python
#
## @file
#
# This controls the IX73 microscope through CBM
#
# Yuan 06/20/22
#

import time
import serial
import storm_control.sc_hardware.serial.RS232 as RS232

## IX73_CBM
#
# This class encapsulates control of an Olympus filter wheel that
# is run by an IX3CBM controller. Communication is done via RS-232
#
#

class IX73_CBM(RS232.RS232):
    ## __init__
    #
    # @param port (Optional) The com port, defaults to "COM4".
    # @param baud (Optional) The baud rate, defaults to 19200.
    #
    def __init__(self, port = "COM4", baud = 19200):
        try:
            # open port
            RS232.RS232.__init__(self, port=port, baudrate=baud, end_of_line='\r\n', timeout=0.05, wait_time=0.05, bytesize=serial.EIGHTBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_TWO)
            # verify that we can talk to the filter wheel
            #
            self.sendCommand("1INIT")
            assert not(self.commWithResp("1INIT?") == None)
        except:
            self.live = 0
            print("Failed to connect to the IX3-CBM controller at port", port)
        # to make sure that the initialization has been done
        self.waitResponse(max_attempts = 200)   
        try:
            assert self.commWithResp("1L 1")[3] == '+'
        except:
            self.live = 0
            print("Failed to switch IX-CBM to remote control mode")


    ## getPosition
    #
    # @return The current position of the filter wheel.
    #
    def getPosition(self):
        resp = self.commWithResp("1MU1?")
        if resp:
            position = resp[5]
            temp = resp[4]
            if temp == "!":
                print("IX3-CBM error code: "+resp[6:])
                return 1
            else:
                try:
                    self.position = int(position)
                    return self.position
                except:
                    print("IX3-CBM: Could not parse:"+ str(position))
                    return 1
        else:
            print("IX3-CBM: Failed to get filter wheel position")
            return 1


    ## setPosition
    #
    # @param position The desired filter wheel position (1-8).
    #
    def setPosition(self, position):
        if (position != self.position):
            if (position < 1):
                position = 1
            if (position > 8):
                position = 8
            print("notcomm")
            self.commWithResp("1MU1 " + str(position))
            #self.waitResponse() #YT: commented 7/10/2023 to avoid stuck when change between setting profiles
            print("commend")
            self.position = position

    def openShutter(self):
        resp = self.commWithResp("1ESH1 0")
        if resp:
            temp = resp[6]
            if temp != "+":
                print("IX3-CBM: Failed to open the filter shutter ")

    def closeShutter(self):
        resp = self.commWithResp("1ESH1 1")
        if resp:
            temp = resp[6]
            if temp != "+":
                print("IX3-CBM: Failed to close the filter shutter ")

    def disconnect(self):
        resp = self.commWithResp("1L 0")
        if resp:
            temp = resp[6]
            if temp != "+":
                print("IX3-CBM: Failed to switch the filter shutter from remote mode")


#
# Testing
#

if __name__ == "__main__":
    ix3 = IX73_CBM()

    print(ix3.getPosition())
    ix3.setPosition(1)
    print(ix3.getPosition())

    ix3.setPosition(3)
    print(ix3.getPosition())

    ix3.setPosition(5)

#
# The MIT License
#
# Copyright (c) 2022 Zhou Lab, Pennsylvania State University
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#