#!/usr/bin/env python
"""
This class handles handles displaying camera data using the
appropriate qtCameraWidget class. It is also responsible for 
displaying the camera record and shutter buttons as well as
choosing the color table, scaling, etc..

Hazen 2/17
"""
import os
from PyQt5 import QtCore, QtGui, QtWidgets

# Debugging
import storm_control.sc_library.parameters as params

# Camera Helper Modules
import storm_control.hal4000.qtWidgets.qtColorGradient as qtColorGradient
import storm_control.hal4000.qtWidgets.qtCameraWidget as qtCameraWidget
import storm_control.hal4000.qtWidgets.qtRangeSlider as qtRangeSlider

# Misc
import storm_control.hal4000.colorTables.colorTables as colorTables

import storm_control.hal4000.qtdesigner.camera_display_ui as cameraDisplayUi

default_widget = None


class BaseFrameDisplay(QtWidgets.QFrame):
    """
    The base frame display class.

    Handles the qtCameraWidget which displays the image as well as other
    GUI elements such as the display range slide, color table chooser, etc..

    This class also keeps track of the display settings for every camera
    and every feed. It is responsible for the 'display' sections of the
    parameters file.

    <displayn>
      <cameran>
        <colortable></colortable>
        <display_max></display_max>
        <display_min></display_min>
        <sync></sync>
      <cameran>
      ..
      <feedn>
        <colortable></colortable>
        <display_max></display_max>
        <display_min></display_min>
        <sync></sync>
      </feedn>
    </displayn>

    I'm not sure whether these shouldn't be feed specific instead of 
    display specific? That would also make it easier to include them
    in the parameters editor.
    """
    guiMessage = QtCore.pyqtSignal(object)

    def __init__(self, display_name = None, feed_name = "camera1", **kwds):
        super().__init__(**kwds)

        # General (alphabetically ordered).
        self.color_gradient = None
        self.color_tables = colorTables.ColorTables(os.path.dirname(__file__) + "/../colorTables/all_tables/")
        self.cycle_length = None
        self.display_name = None
        self.display_timer = QtCore.QTimer(self)
        self.feed_name = feed_name
        self.frame = False
        self.parameters = params.StormXMLObject()
        self.show_grid = False
        self.show_info = True
        self.show_target = False

        # UI setup.
        self.ui = cameraDisplayUi.Ui_Frame()
        self.ui.setupUi(self)

        # Display range slider.
        self.ui.rangeSlider = qtRangeSlider.QVRangeSlider()
        layout = QtWidgets.QGridLayout(self.ui.rangeSliderWidget)
        layout.setContentsMargins(1,1,1,1)
        layout.addWidget(self.ui.rangeSlider)
        self.ui.rangeSliderWidget.setLayout(layout)
        #self.ui.rangeSlider.setRange([0.0, self.max_intensity, 1.0])
        self.ui.rangeSlider.setEmitWhileMoving(True)

        # Color tables combo box.
        for color_name in self.color_tables.getColorTableNames():
            self.ui.colorComboBox.addItem(color_name[:-5])

        self.ui.gridAct = QtWidgets.QAction(self.tr("Show Grid"), self)
        self.ui.infoAct = QtWidgets.QAction(self.tr("Hide Info"), self)
        self.ui.targetAct = QtWidgets.QAction(self.tr("Show Target"), self)

        self.ui.cameraShutterButton.hide()
        self.ui.recordButton.hide()

        self.ui.syncLabel.hide()
        self.ui.syncSpinBox.hide()

        self.camera_widget = qtCameraWidget.QCameraWidget(parent = self.ui.cameraScrollArea)
        self.ui.cameraScrollArea.setWidget(self.camera_widget)
        self.ui.cameraScrollArea.setStyleSheet("QScrollArea { background-color: black } ")

        self.camera_widget.intensityInfo.connect(self.handleIntensityInfo)

        self.ui.autoScaleButton.clicked.connect(self.handleAutoScale)
        self.ui.colorComboBox.currentIndexChanged[str].connect(self.handleColorTableChange)
        self.ui.feedComboBox.currentIndexChanged[str].connect(self.handleFeedChange)
        self.ui.gridAct.triggered.connect(self.handleGrid)
        self.ui.infoAct.triggered.connect(self.handleInfo)        
        self.ui.rangeSlider.doubleClick.connect(self.handleAutoScale)        
        self.ui.rangeSlider.rangeChanged.connect(self.handleRangeChange)
        self.ui.syncSpinBox.valueChanged.connect(self.handleSync)
        self.ui.targetAct.triggered.connect(self.handleTarget)

        # Display timer
        self.display_timer.setInterval(100)
        self.display_timer.timeout.connect(self.handleDisplayTimer)
        self.display_timer.start()
        
    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)
        menu.addAction(self.ui.infoAct)
        menu.addAction(self.ui.targetAct)
        menu.addAction(self.ui.gridAct)
        menu.exec_(event.globalPos())

    def feedConfig(self, data):
        cam_params = data["parameters"]

        # Add a sub-section for this camera / feed if we don't already have one.
        if not self.parameters.has(data["camera"]):

            # Create a sub-section for this camera / feed.
            p = self.parameters.addSubSection(data["camera"])

            # Add display specific parameters.
            p.add("colortable", params.ParameterSetString("Color table",
                                                          "colortable",
                                                          data["colortable"],
                                                          self.color_tables.getColorTableNames()))
                        
            p.add("display_max", params.ParameterInt("Display maximum",
                                                     "display_max",
                                                     cam_params.get("default_max")))

            p.add("display_min", params.ParameterInt("Display minimum",
                                                     "display_min",
                                                     cam_params.get("default_min")))

            p.add("max_intensity", params.ParameterInt("", "max_intensity",
                                                       cam_params.get("max_intensity"),
                                                       is_mutable = False,
                                                       is_saved = False))

            p.add("sync", params.ParameterInt("Frame to display when filming with a shutter sequence",
                                              "sync", 0))

        #
        # Update UI settings if the feed / camera that we got configuration
        # information for is the current feed / camera.
        #
        if (self.feed_name == data["camera"]):

            # Setup the camera display widget
            color_table = self.color_tables.getTableByName(self.getParameter("colortable"))
            self.camera_widget.newColorTable(color_table)
            self.camera_widget.newSize([cam_params.get("x_pixels")/cam_params.get("x_bin"),
                                        cam_params.get("y_pixels")/cam_params.get("y_bin")])
            self.updateRange()

            # Color gradient
            if self.color_gradient is not None:
                self.color_gradient.newColorTable(color_table)
            else:
                self.color_gradient = qtColorGradient.QColorGradient(colortable = color_table,
                                                                     parent = self.ui.colorFrame)
                layout = QtWidgets.QGridLayout(self.ui.colorFrame)
                layout.setContentsMargins(2,2,2,2)
                layout.addWidget(self.color_gradient)
                
            self.ui.colorComboBox.setCurrentIndex(self.ui.colorComboBox.findText(self.getParameter("colortable")[:-5]))

            # General settings
            self.ui.rangeSlider.setRange([0.0, self.getParameter("max_intensity"), 1.0])
            self.ui.rangeSlider.setValues([float(self.getParameter("display_min")),
                                           float(self.getParameter("display_max"))])
            self.ui.syncSpinBox.setValue(self.getParameter("sync"))

    def getParameter(self, pname):
        """
        Wrapper to make it easier to get the appropriate parameter value.
        """
        return self.parameters.get(self.feed_name).get(pname)
    
    def handleAutoScale(self, bool):
        [scalemin, scalemax] = self.camera_widget.getAutoScale()
        if scalemin < 0:
            scalemin = 0
        if scalemax > self.max_intensity:
            scalemax = self.max_intensity
        self.ui.rangeSlider.setValues([float(scalemin), float(scalemax)])

    def handleColorTableChange(self, table_name):
        table_name = str(table_name)
        self.setParameter("colortable", table_name + ".ctbl")
        color_table = self.color_tables.getTableByName(self.getParameter("colortable"))
        self.camera_widget.newColorTable(color_table)
        self.color_gradient.newColorTable(color_table)

    def handleDisplayTimer(self):
        if self.frame:
            self.camera_widget.updateImageWithFrame(self.frame)

    def handleFeedChange(self, feed_name):
        feed_name = str(feed_name)
        self.feedChanged.emit(feed_name)
        
    def handleGrid(self, boolean):
        if self.show_grid:
            self.show_grid = False
            self.ui.gridAct.setText("Show Grid")
        else:
            self.show_grid = True
            self.ui.gridAct.setText("Hide Grid")
        self.camera_widget.setShowGrid(self.show_grid)

    def handleInfo(self, boolean):
        if self.show_info:
            self.show_info = False
            self.ui.infoAct.setText("Show Info")
            self.ui.intensityPosLabel.hide()
            self.ui.intensityIntLabel.hide()
        else:
            self.show_info = True
            self.ui.infoAct.setText("Hide Info")
            self.ui.intensityPosLabel.show()
            self.ui.intensityIntLabel.show()
        self.camera_widget.setShowInfo(self.show_info)

    def handleIntensityInfo(self, x, y, i):
        self.ui.intensityPosLabel.setText("({0:d},{1:d})".format(x, y, i))
        self.ui.intensityIntLabel.setText("{0:d}".format(i))

    def handleRangeChange(self, scale_min, scale_max):
        if (scale_max == scale_min):
            if (scale_max < float(self.getParameter("max_intensity"))):
                scale_max += 1.0
            else:
                scale_min -= 1.0
        self.setParameter("display_max", int(scale_max))
        self.setParameter("display_min", int(scale_min))
        self.updateRange()

    def handleSync(self, sync_value):
        self.sync_value = sync_value
        self.sync_values_by_feedname[self.feed_name] = sync_value

    def handleTarget(self, boolean):
        if self.show_target:
            self.show_target = False
            self.ui.targetAct.setText("Show Target")
        else:
            self.show_target = True
            self.ui.targetAct.setText("Hide Target")
        self.camera_widget.setShowTarget(self.show_target)

#    def newFeed(self, feed_name):
#        self.feed_name = feed_name
#
#        # Setup the camera display widget
#        self.color_table = self.color_tables.getTableByName(self.getParameter("colortable"))
#        self.camera_widget.newColorTable(self.color_table)
#        self.camera_widget.newSize([self.getParameter("x_pixels")/self.getParameter("x_bin"),
#                                    self.getParameter("y_pixels")/self.getParameter("y_bin")])
#        self.updateRange()
#
#        # Color gradient
#        if self.color_gradient:
#            self.color_gradient.newColorTable(self.color_table)
#        else:
#            self.color_gradient = qtColorGradient.QColorGradient(colortable = self.color_table,
#                                                                 parent = self.ui.colorFrame)
#            layout = QtWidgets.QGridLayout(self.ui.colorFrame)
#            layout.setContentsMargins(2,2,2,2)
#            layout.addWidget(self.color_gradient)
#
#        self.ui.colorComboBox.setCurrentIndex(self.ui.colorComboBox.findText(self.getParameter("colortable")[:-5]))
#
#        # General settings
#        self.max_intensity = self.getParameter("max_intensity")
#        self.ui.rangeSlider.setRange([0.0, self.max_intensity, 1.0])
#        self.ui.rangeSlider.setValues([float(self.getParameter("scalemin")), 
#                                       float(self.getParameter("scalemax"))])
#
#        # Find correct sync value, if it exists.
#        if not feed_name in self.sync_values_by_feedname:
#            self.sync_values_by_feedname[feed_name] = self.getParameter("sync")
#        self.ui.syncSpinBox.setValue(self.sync_values_by_feedname[feed_name])

    def newFrame(self, frame):
        if (frame.which_camera == self.feed_name):
            if self.filming and (self.sync_value != 0):
                if((frame.number % self.cycle_length) == (self.sync_value - 1)):
                    self.frame = frame
            else:
                self.frame = frame

#    def newParameters(self, parameters, feed_name):
#        self.feed_controller = feeds.getFeedController(parameters)
#
#        # Pass the parameters that are the same for all of the feeds
#        # associated with a given camera to the camera_widget.
#        self.camera_widget.newParameters(parameters.get(self.feed_controller.getCamera(feed_name)))
#
#        # Find saved sync values for these parameters (if any).
#        if not parameters in self.sync_values_by_params:
#            self.sync_values_by_params[parameters] = {}
#        self.sync_values_by_feedname = self.sync_values_by_params[parameters]
#            
#        # Configure for this feed.
#        self.newFeed(feed_name)
#
#        # Update feed selector combobox.
#        self.ui.feedComboBox.currentIndexChanged[str].disconnect()
#        self.ui.feedComboBox.clear()
#        feed_names = self.feed_controller.getFeedNames()
#        if (len(feed_names) > 1):
#            for name in feed_names:
#                self.ui.feedComboBox.addItem(name)
#            self.ui.feedComboBox.setCurrentIndex(self.ui.feedComboBox.findText(feed_name))                
#            self.ui.feedComboBox.show()
#        else:
#            self.ui.feedComboBox.hide()
#        self.ui.feedComboBox.currentIndexChanged[str].connect(self.handleFeedChange)

    def setParameter(self, pname, pvalue):
        """
        Wrapper to make it easier to set the appropriate parameter value.
        """
        feed_params = self.parameters.get(self.feed_name)
        feed_params.set(pname, pvalue)
        return pvalue
            
#    def setSyncMax(self, sync_max):
#        self.cycle_length = sync_max
#        self.ui.syncSpinBox.setMaximum(sync_max)
        
#    def startFilm(self, run_shutters):
#        self.filming = True
#        if run_shutters:
#            self.ui.syncLabel.show()
#            self.ui.syncSpinBox.show()
            
#    def stopFilm(self):
#        self.filming = False
#        self.ui.syncLabel.hide()
#        self.ui.syncSpinBox.hide()

                
    def updateRange(self):
        self.ui.scaleMax.setText(str(self.getParameter("display_max")))
        self.ui.scaleMin.setText(str(self.getParameter("display_min")))
        self.camera_widget.newRange([self.getParameter("display_min"), self.getParameter("display_max")])


class CameraFrameDisplay(BaseFrameDisplay):
    """
    Add handling of interaction with the feeds, i.e. mouse drags,
    ROI selection, etc..
    """
    def __init__(self, show_record = False, **kwds):
        super().__init__(**kwds)

        self.camera_widget.setDragEnabled(True)
        
        if show_record:
            self.ui.recordButton.show()
                
        # Signals
        self.camera_widget.displayCaptured.connect(self.handleDisplayCaptured)
        self.camera_widget.dragStart.connect(self.handleDragStart)
        self.camera_widget.dragMove.connect(self.handleDragMove)
        self.camera_widget.roiSelection.connect(self.handleROISelection)

        self.ui.cameraShutterButton.clicked.connect(self.handleCameraShutter)

    def handleCameraShutter(self, boolean):
        #self.cameraShutter.emit(self.feed_controller.getCamera(self.feed_name))
        pass

    def handleDisplayCaptured(self, a_pixmap):
        #self.frameCaptured.emit(self.feed_name, a_pixmap)
        pass

    def handleDragStart(self):
        #self.dragStart.emit(self.feed_name)
        pass

    def handleDragMove(self, x_disp, y_disp):
        #self.dragMove.emit(self.feed_name, x_disp, y_disp)
        pass
        
    def handleROISelection(self, select_rect):
        #self.ROISelection.emit(self.feed_name, select_rect)
        pass

    def handleSync(self, sync_value):
        """
        Handles setting the sync parameter. This parameter is used in
        shutter sequences to specify which frame in the sequence should
        be displayed, or just any random frame.
        """
        super.handleSync(self, sync_value)
        #self.setParameter("sync", sync_value)

#    def startFilm(self, run_shutters):
#        CameraFeedDisplay.startFilm(self, run_shutters)
#        self.ui.cameraShutterButton.setEnabled(False)

#    def stopFilm(self):
#        CameraFeedDisplay.stopFilm(self)
#        self.ui.cameraShutterButton.setEnabled(True)

    def updateCameraProperties(self, camera_properties):
        if self.feed_name in camera_properties:
            if "have_shutter" in camera_properties[self.feed_name]:
                self.ui.cameraShutterButton.show()
            else:
                self.ui.cameraShutterButton.hide()
        else:
            self.ui.cameraShutterButton.hide()

    def updatedParams(self):
        if self.getParameter("shutter", False):
            self.ui.cameraShutterButton.setText("Close Shutter")
            self.ui.cameraShutterButton.setStyleSheet("QPushButton { color: green }")
        else:
            self.ui.cameraShutterButton.setText("Open Shutter")
            self.ui.cameraShutterButton.setStyleSheet("QPushButton { color: black }")


#
# The MIT License
#
# Copyright (c) 2017 Zhuang Lab, Harvard University
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