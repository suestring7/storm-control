#!/usr/bin/python
#
## @file
#
# Handle LED and turret wheel for SOLA.
#
# Yuan 06/22
#

import time
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIntValidator, QDoubleValidator, QRegExpValidator

import storm_control.sc_library.parameters as params

import storm_control.hal4000.halLib.halDialog as halDialog
import storm_control.hal4000.halLib.halMessage as halMessage
import storm_control.hal4000.halLib.halModule as halModule

# UIs.
import storm_control.hal4000.qtdesigner.sola_ui as SOLAControlsUi


# Mirror turret wheel
import storm_control.sc_hardware.lumencor.sola as SOLA


class SOLAControlView(halDialog.HalDialog):
    """
    Manages the SOLA GUI

    """
    def __init__(self, configuration = None, **kwds):
        super().__init__(**kwds)
        # Add parameters.
        self.parameters = params.StormXMLObject()
        self.sola = SOLA.SOLA()
        self.checked = True

        # UI setup
        self.ui = SOLAControlsUi.Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.okButton.setDefault(False)
        self.ui.okButton.setAutoDefault(False)

        self.onOff = self.ui.onOffButton
        self.onOff.clicked.connect(self.handleOnOffChange)

        self.onOff.setDefault(False)
        self.onOff.setAutoDefault(False)

        self.power = self.ui.powerSlider
        maximum = 255
        minimum = 0        
        page_step = 0.1 * (maximum - minimum)
        if (page_step > 1.0):
            self.power.setPageStep(page_step)
        self.power.setSingleStep(1)
        self.power.setMaximum(maximum)
        self.power.setMinimum(minimum)
        self.power.valueChanged.connect(self.handlePowerChangeBySlider)

        self.powervalue = self.ui.inputPower
        int_validator = QIntValidator(0, 255, self)
        self.powervalue.setValidator(int_validator) 
        self.powervalue.returnPressed.connect(self.handlePowerChangeByEditor)
        self.parameters.add(params.ParameterRangeInt(description = "SOLA light intensity",
                                                       name = "Intensity",
                                                       value = 0,
                                                       min_value = 0,
                                                       max_value = 255))
        self.parameters.add(params.ParameterSetBoolean(description = "Power",
                                                       name = "OnOff",
                                                       value = False))
        self.newParameters(self.parameters, initialization = True)

    def handleOnOffChange(self):
        if self.checked:
            self.onOff.setText("On")
            self.sola.setOnOff(True)
            self.checked = False
            self.parameters.setv("OnOff", True)
        else:
            self.onOff.setText("Off")
            self.sola.setOnOff(False)
            self.checked = True
            self.parameters.setv("OnOff", False)

    def handlePowerChangeBySlider(self):
        intensity = self.power.value()
        self.powervalue.setText(str(intensity))
        self.sola.setIntensity(intensity)
        self.parameters.setv("Intensity", intensity)

    def handlePowerChangeByEditor(self):
        intensity = int(self.powervalue.text())
        self.power.setValue(intensity)
        self.sola.setIntensity(intensity)
        self.parameters.setv("Intensity", intensity)

    def handleTCPMessage(self, message):
        #
        # TODO: Reserve the spot for future applications // Copied from focus lock
        #
        tcp_message = message.getData()["tcp message"]
        if tcp_message.isType("Set Focus Lock Mode"):
            if tcp_message.isTest():
                return True

            mode_name = tcp_message.getData("mode_name")
            locked = tcp_message.getData("locked")

            for i in range(self.ui.modeComboBox.count()):
                if (mode_name == self.ui.modeComboBox.itemText(i)):
                    self.ui.modeComboBox.setCurrentIndex(i)
                    if locked and not self.amLocked() and self.ui.lockButton.isEnabled():
                        self.ui.lockButton.click()
                    return True

            tcp_message.setError(True, "Requested mode '" + mode_name + "' not found.")
            return True
        
        else:
            return False

    def getParameters(self):
        return self.parameters

    def newParameters(self, parameters, initialization = False):
        for pname in ["Intensity", "OnOff"]:
            pnow = parameters.get(pname)
            if self.parameters.get(pname) != pnow:
                getattr(self.sola, "set"+pname)(pnow)
                self.parameters.setv(pname, pnow)
                if pname == "Intensity":
                    self.power.setValue(pnow)
                elif pname == "OnOff":
                    self.onOff.click()

    def show(self):
        super().show()
        # TODO: why 391, 105?
        print(self.width())
        print(self.height())
        self.setFixedSize(200, 400)
        print(self.width())
        print(self.height())



class SOLAControl(halModule.HalModule):

    def __init__(self, module_params = None, qt_settings = None, **kwds):
        super().__init__(**kwds)
                                                                   
        self.configuration = module_params.get("configuration")    
        self.view = SOLAControlView(module_name = self.module_name,
                                    configuration = self.configuration)
        self.view.halDialogInit(qt_settings,
                                module_params.get("setup_name") + " SOLA control")

    
    def cleanUp(self, qt_settings):
        self.view.cleanUp(qt_settings)
        self.view.sola.setOnOff(False)

    def handleResponse(self, message, response):
        if message.isType("get functionality"):
            self.view.setFunctionality(response.getData()["functionality"])
            
    def processMessage(self, message):
        if message.isType("configure1"):
            self.sendMessage(halMessage.HalMessage(m_type = "add to menu",
                                                   data = {"item name" : "SOLA",
                                                           "item data" : "SOLAControl"}))

            #self.sendMessage(halMessage.HalMessage(m_type = "get functionality",
            #                                       data = {"name" : self.stage_fn_name}))

            self.sendMessage(halMessage.HalMessage(m_type = "initial parameters",
                                                   data = {"parameters" : self.view.getParameters()}))

            #self.sendMessage(halMessage.HalMessage(m_type = "configuration",
            #                                       data = {"properties" : {"mirror turret functionality name" : self.configuration.get("mirror_turret")}}))

        elif message.isType("new parameters"):
            p = message.getData()["parameters"]
            message.addResponse(halMessage.HalMessageResponse(source = self.module_name,
                                                              data = {"old parameters" : self.view.getParameters().copy()}))
            self.view.newParameters(p.get(self.module_name))
            message.addResponse(halMessage.HalMessageResponse(source = self.module_name,
                                                              data = {"new parameters" : self.view.getParameters()}))
            
        elif message.isType("show"):
            if (message.getData()["show"] == "SOLAControl"):
                self.view.show()

        elif message.isType("start"):
            #self.view.start()
            #self.control.start()
            if message.getData()["show_gui"]:
                self.view.showIfVisible()

# should had nothing to do with start/stop movie for now?
        elif message.isType("tcp message"):
            # See control handles this message.
            handled = self.control.handleTCPMessage(message)

            # If not, check view.
            if not handled:
                handled = self.view.handleTCPMessage(message)

            # Mark if we handled the message.
            if handled:
                message.addResponse(halMessage.HalMessageResponse(source = self.module_name,
                                                                  data = {"handled" : True}))


        
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