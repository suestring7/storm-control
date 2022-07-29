#!/usr/bin/python
#
## @file
#
# Handle LED and turret wheel for Turnkey.
#
# Yuan 06/22
#

import time
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

import storm_control.sc_library.parameters as params

import storm_control.hal4000.halLib.halDialog as halDialog
import storm_control.hal4000.halLib.halMessage as halMessage
import storm_control.hal4000.halLib.halModule as halModule

# UIs.
import storm_control.hal4000.qtdesigner.turnkey_misc_ui as miscControlsUi


# Mirror turret wheel
import storm_control.sc_hardware.olympus.ix73cbm as IXCBM


class TurnkeyMiscControlView(halDialog.HalDialog):
    """
    Manages the Turnkey GUI

    """
    def __init__(self, configuration = None, **kwds):
        super().__init__(**kwds)
        # Add parameters.
        filter_names = configuration.get("filters").split(",")
        self.parameters = params.StormXMLObject()
        self.parameters.add(params.ParameterSetString(description = "Current Filter",
                                                    name = "current_filter",
                                                    value = filter_names[0],
                                                    allowed = filter_names))

        self.parameters.add(params.ParameterRangeInt(description = "Filter position", 
                                                    name = "filter_position",
                                                    value = 1,
                                                    min_value = 1,
                                                    max_value = 8))
        self.filter_wheel = IXCBM.IX73_CBM()
        self.stage_functionality = None
        self.checked = True

        # UI setup
        self.ui = miscControlsUi.Ui_Dialog()
        self.ui.setupUi(self)

        # # connect signals
        # if self.have_parent:
        #     self.ui.okButton.setText("Close")
        #     self.ui.okButton.clicked.connect(self.handleOk)
        # else:
        #     self.ui.okButton.setText("Quit")
        #     self.ui.okButton.clicked.connect(self.handleQuit)

        # setup (turret) filter wheel
        self.filters = [self.ui.filter1Button,
                        self.ui.filter2Button,
                        self.ui.filter3Button,
                        self.ui.filter4Button,
                        self.ui.filter5Button,
                        self.ui.filter6Button,
                        self.ui.filter7Button,
                        self.ui.filter8Button,
                        ]

        # setup filter shutter
        self.shutter = self.ui.shutterButton
        self.shutter.clicked.connect(self.handleShutter)
        for i, afilter in enumerate(self.filters):
            afilter.clicked.connect(self.handleFilter)
            afilter.setText(filter_names[i])
        if self.filter_wheel:
            self.filters[self.filter_wheel.getPosition()-1].click()
            self.handleShutter()        
        # Disable UI until we get a stage functionality.
        # TODO: add cbm as a functionality and do this later...
        #self.setEnabled(False)


    def handleShutter(self):
        if self.checked:
            self.shutter.setText("On")
            self.filter_wheel.openShutter()
            self.checked = False
        else:
            self.shutter.setText("Off")
            self.filter_wheel.closeShutter()
            self.checked = True

    def handleFilter(self):
        # filter autoexclusive, so can be done like this
        for i, filter in enumerate(self.filters):
            if filter.isChecked():
                filter.setStyleSheet("QPushButton { color: red}")
                if self.filter_wheel:
                    self.filter_wheel.setPosition(i+1)
                self.parameters.set("filter_position", i)
            else:
                filter.setStyleSheet("QPushButton { color: black}")


    def handleTCPMessage(self, message):
        #
        # Reserve the spot for future applications // Copied from focus lock
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

    def newParameters(self, parameters):
        self.parameters = parameters
        names = parameters.get("filter_names")
        if (len(names) == 8):
            for i in range(8):
                self.filters[i].setText(names[i])

        self.filters[self.parameters.get("filter_position")].click()

    def show(self):
        super().show()
        self.setFixedSize(self.width(), self.height())



class TurnkeyMiscControl(halModule.HalModule):

    def __init__(self, module_params = None, qt_settings = None, **kwds):
        super().__init__(**kwds)
                                                                   
        self.configuration = module_params.get("configuration")    
        self.view = TurnkeyMiscControlView(module_name = self.module_name,
                                    configuration = self.configuration)
        self.view.halDialogInit(qt_settings,
                                module_params.get("setup_name") + " Misc control")

    
    def cleanUp(self, qt_settings):
        self.view.cleanUp(qt_settings)
        self.view.filter_wheel.disconnect()

    def handleResponse(self, message, response):
        if message.isType("get functionality"):
            self.view.setFunctionality(response.getData()["functionality"])
            
    def processMessage(self, message):
        if message.isType("configure1"):
            self.sendMessage(halMessage.HalMessage(m_type = "add to menu",
                                                   data = {"item name" : "Turnkey",
                                                           "item data" : "TurnkeyMiscControl"}))

            #self.sendMessage(halMessage.HalMessage(m_type = "get functionality",
            #                                       data = {"name" : self.stage_fn_name}))

            self.sendMessage(halMessage.HalMessage(m_type = "initial parameters",
                                                   data = {"parameters" : self.view.getParameters()}))

            self.sendMessage(halMessage.HalMessage(m_type = "configuration",
                                                   data = {"properties" : {"mirror turret functionality name" : self.configuration.get("mirror_turret")}}))
            ## Example for multiple elements
            # self.sendMessage(halMessage.HalMessage(m_type = "configuration",
            #                                        data = {"properties" : {"ir laser functionality name" : self.configuration.get("ir_laser"),
            #                                                                "qpd functionality name" : self.configuration.get("qpd"),
            #                                                                "z stage functionality name" : self.configuration.get("z_stage")}}))

        elif message.isType("new parameters"):
            p = message.getData()["parameters"]
            message.addResponse(halMessage.HalMessageResponse(source = self.module_name,
                                                              data = {"old parameters" : self.view.getParameters().copy()}))
            self.view.newParameters(p.get(self.module_name))
            message.addResponse(halMessage.HalMessageResponse(source = self.module_name,
                                                              data = {"new parameters" : self.view.getParameters()}))
            
        elif message.isType("show"):
            if (message.getData()["show"] == "TurnkeyMiscControl"):
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
