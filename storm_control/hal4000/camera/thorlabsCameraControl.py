#!/usr/bin/env python
"""
Camera control specialized for a Hamamatsu camera.

Hazen 09/15
"""
from PyQt5 import QtCore

import storm_control.sc_hardware.thorlabs.CS235MU as tcam
import storm_control.sc_library.parameters as params

import storm_control.hal4000.camera.frame as frame
import storm_control.hal4000.camera.cameraControl as cameraControl
import storm_control.hal4000.camera.cameraFunctionality as cameraFunctionality

from thorlabs_tsi_sdk.tl_camera import *
from thorlabs_tsi_sdk.tl_camera_enums import *

class ThorlabsCameraControl(cameraControl.HWCameraControl):
    """
    Interface to a Hamamatsu sCMOS camera.
    """
    def __init__(self, config = None, is_master = False, **kwds):
        kwds["config"] = config
        super().__init__(**kwds)

        # The camera configuration.
        self.camera_functionality = cameraFunctionality.CameraFunctionality(camera_name = self.camera_name,
                                                                            have_gain = True,
                                                                            have_shutter = True,
                                                                            is_master = is_master,
                                                                            parameters = self.parameters)
        self.camera_functionality.setGain = self.setGain

        # Load the library and start the camera.
        tcam.loadThorlabsDLL(config.get("thorlabs_dll"))
<<<<<<< Updated upstream
=======
        print("load successfully?")
>>>>>>> Stashed changes
        self.camera = tcam.cs235mu()

        # Dictionary of the Thorlab camera properties we'll support.

        self.tcam_props = {
                   "binx_range": False,
                   "binx": True,
                   "biny_range": False,
                   "biny": True,
                   "bit_depth": False,
                   "black_level": True,
                   "black_level_range": False,
                   "camera_sensor_type" : False,
                   "communication_interface": False,       # COMMUNICATION_INTERFACE
                   #"data_rate": True,     # Scientific-CCD cameras offer data rates of 20MHz or 40MHz. Compact-scientific cameras offer FPS30 or FPS50, which are frame rates supported by the camera when doing full-frame readout. 
                   #  Neither fps nor readout frequency is supported
                   "exposure_time_range_us": False,
                   "exposure_time_us": True,
                   "firmware_version": False,
                   #"frame_rate_control_value": True,      # Camera does not support frame-rate control
                   "frame_rate_control_value_range": False,
                   "frame_time_us": False,                  # Only scientific CCD cameras support this parameter.
                   "frames_per_trigger_range" : False,
                   "frames_per_trigger_zero_for_unlimited": True,     # 0 for continous, 1+ for fixed number frames
                   "gain_range": False,
                   "gain": True,
                   "hot_pixel_correction_threshold_range": False,
                   "hot_pixel_correction_threshold": True,
                   "image_height_pixels" : False,
                   "image_height_range_pixels" : False,
                   "image_poll_timeout_ms": True,
                   "image_width_pixels" : False,
                   "image_width_range_pixels" : False,
                   "is_armed": False,
                   #"is_frame_rate_control_enabled": True,   #For short exposure times, the maximum frame rate is limited by the readout time of the sensor. For long exposure times, the frame rate is limited by the exposure time.
                   "is_hot_pixel_correction_enabled": True,
                   "model" : False,
                   "name_string_length_range" : False,
                   "name" : False, 
                   "operation_mode": True,          # OPERATION_MODE, guess we only use SOFTWARE_TRIGGERED in our application
                   "roi": True,
                   "roi_range": False,
                   "sensor_height_pixels" : False,
                   "sensor_pixel_height_um" : False,
                   "sensor_pixel_size_bytes" : False,
                   "sensor_pixel_width_um" : False,
                   "sensor_readout_time_ns": False,                   
                   "sensor_width_pixels" : False,
                   "serial_number": False,
                   "usb_port_type" : False,         # USB_PORT_TYPE
                   }


        max_intensity = 2**self.camera.getPropertyValue("bit_depth")
        self.parameters.setv("max_intensity", max_intensity)
        self.parameters.setv("exposure_time", 0.001)

        x_size = self.camera.getPropertyValue("image_width_range_pixels")[1]
        y_size = self.camera.getPropertyValue("image_height_range_pixels")[1]
        self.parameters.setv("x_chip", x_size)
        self.parameters.setv("y_chip", y_size)


        # TODO: Examples of parameters
        # text_values = self.camera.sortedPropertyTextOptions("binning")
        # self.parameters.add(params.ParameterSetString(description = "Camera binning.",
        #                                               name = "binning",
        #                                               value = text_values[0],
        #                                               allowed = text_values))
        

        for prop in self.tcam_props:
            # roi_range:
            # ROIRange(upper_left_x_pixels_min=0, upper_left_y_pixels_min=0, lower_right_x_pixels_min=91, lower_right_y_pixels_min=3, upper_left_x_pixels_max=1828, upper_left_y_pixels_max=1196, lower_right_x_pixels_max=1919, lower_right_y_pixels_max=1199) 
            # "image_poll_timeout_ms"
            # "frames_per_trigger_zero_for_unlimited"  0,4294967280
            # "exposure_time_us":
            # "exposure_time_range_us":
            if self.tcam_props[prop]:
                tmp = self.camera.getPropertyValue(prop)
                if isinstance(tmp, ROI):
                    tmp_range = self.camera.getPropertyValue("roi_range")
                    self.parameters.getp("x_end").setMaximum(tmp_range[6])
                    self.parameters.getp("x_start").setMaximum(tmp_range[4])
                    self.parameters.getp("y_end").setMaximum(tmp_range[7])
                    self.parameters.getp("y_start").setMaximum(tmp_range[5])
                    self.parameters.getp("x_end").setMinimum(tmp_range[2])
                    self.parameters.getp("x_start").setMinimum(tmp_range[0])
                    self.parameters.getp("y_end").setMinimum(tmp_range[3])
                    self.parameters.getp("y_start").setMinimum(tmp_range[1])
                    self.parameters.setv("x_end", x_size)
                    self.parameters.setv("y_end", y_size)
                    self.parameters.setv("x_chip", x_size)
                    self.parameters.setv("y_chip", y_size)
                    continue
                elif prop == "binx" or prop == "biny":
                    prop_t = prop[-1]+"_bin"
                    tmp_range = self.camera.getPropertyValue(prop + "_range")
                    self.parameters.getp(prop_t).setMinimum(tmp_range[0])
                    self.parameters.getp(prop_t).setMaximum(tmp_range[1])
                elif isinstance(tmp, OPERATION_MODE):
                    mode_set = [ x for x in OPERATION_MODE ]
                    self.parameters.add(params.ParameterSetString(description = prop,
                                                       name = prop,
                                                       value = mode_set[0],
                                                       allowed = mode_set))
                    continue
                elif prop == "gain":
                    tmp_range = self.camera.getPropertyValue("gain_range")
                    self.parameters.add(params.ParameterRangeFloat(description = prop,
                                                       name = prop,
<<<<<<< Updated upstream
                                                       value = tmp_range[0]/10,
                                                       min_value = tmp_range[0]/10,
                                                       max_value = tmp_range[1]/10))
=======
                                                       value = tmp_range[0],
                                                       min_value = tmp_range[0],
                                                       max_value = tmp_range[1]))
                    continue
>>>>>>> Stashed changes
                elif prop == "exposure_time_us":
                    tmp_range = self.camera.getPropertyValue("exposure_time_range_us")
                else:
                    tmp_range = self.camera.getPropertyValue(prop + "_range")
                if isinstance(tmp_range, Range):
                    if isinstance(tmp_range[0], int):
                        if tmp_range[1] - tmp_range[0] <= 4:
                            tmp_numbers = list(range(tmp_range[0],tmp_range[1]+1))
                            self.parameters.add(params.ParameterSetInt(description = prop,
                                                       name = prop,
                                                       value = 0,
                                                       allowed = tmp_numbers))
                        else:
                            self.parameters.add(params.ParameterRangeInt(description = prop,
                                                       name = prop,
                                                       value = tmp_range[0],
                                                       min_value = tmp_range[0],
                                                       max_value = tmp_range[1]))
                    elif isinstance(tmp_range[0], float):
                        self.parameters.add(params.ParameterRangeFloat(description = prop,
                                                       name = prop,
                                                       value = tmp_range[0],
                                                       min_value = tmp_range[0],
                                                       max_value = tmp_range[1]))
                    else:
                        print("Unexpected Range type: " + type(tmp) + " with property " + prop + ": ")
                        print(tmp)
                        print("Please add the conditions to ThorlabsCameraControl.py parameters cases.")
                elif isinstance(tmp, bool):
                    self.parameters.add(params.ParameterSetBoolean(description = prop,
                                                       name = prop,
                                                       value = False))
                else:
                    MAX = 1000000
                    self.parameters.add(params.ParameterRangeInt(description = prop,
                                                       name = prop,
                                                       value = 0,
                                                       min_value = 0,
                                                       max_value = MAX))


        ## Disable editing of the HAL versions of these parameters.
        for param in ["x_bin", "x_end", "x_start", "y_end", "y_start", "y_bin"]:
            self.parameters.getp(param).setMutable(False)

        self.newParameters(self.parameters, initialization = True)



    def transROI(x0,y0,x1,y1):
        """
        The camera ROI has a weird transform...
        Although we actually don't need this function since we can just call the getroi to get the value = =
        """
        if x1 < 91:
            x1 = 91
        if y1 < 3:
            y1 = 3
        nx0 = int((x0+1)/4)*4
        ny0 = int((y0+1)/4)*4
        nx1 = int((x1-2*int((x0+1)%4/2))/4)*4+3
        ny1 = int(y1/4)*4+3
        return [nx0, ny0, nx1, ny1]

    # TODO: shouldn't set value when getParameters. move that part here.
    def newParameters(self, parameters, initialization = False):

        # Super class performs some simple checks & update some things.
        super().newParameters(parameters)

        self.camera_working = True

        # Update the parameter values, only the Thorlabs specific 
        # ones and only if they are different.
        to_change = []
        for pname in self.tcam_props:
            if self.tcam_props[pname]:
                if pname == "roi":
                    to_change.append(pname)
                elif (self.parameters.get(pname) != parameters.get(pname)) :
                    to_change.append(pname)

        if (len(to_change) > 0):
            running = self.running
            if running:
                self.stopCamera()

            for pname in to_change:
                if pname == "binx":
                    self.parameters.setv("x_bin", parameters.get(pname))
                elif pname == "biny":
                    self.parameters.setv("y_bin", parameters.get(pname))
                elif pname == "gain":
<<<<<<< Updated upstream
                    gainvalue = int(parameters.get(pname)*10)
                    self.camera.setPropertyValue(pname, gainvalue)
                    self.parameters.setv(pname, parameters.get(pname))
=======
                    gainvalue = int(parameters.get(pname))
                    self.camera.setPropertyValue(pname, gainvalue)
                    self.parameters.setv(pname, parameters.get(pname))
                    continue
>>>>>>> Stashed changes
                elif pname == "roi":
                    # since the camera roi are in pixels of 4, so the first thing is to get the roi value
                    self.camera.setPropertyValue("roi", ROI(parameters.get("x_start"), parameters.get("y_start"), parameters.get("x_end"), parameters.get("y_end")))
                    tmp_roi = self.camera.getPropertyValue("roi")
                    parameters.setv("x_start", tmp_roi[0])
                    parameters.setv("y_start", tmp_roi[1])
                    parameters.setv("x_end", tmp_roi[2])
                    parameters.setv("y_end", tmp_roi[3])
                    size_x = parameters.get("x_end") - parameters.get("x_start") + 1
                    size_y = parameters.get("y_end") - parameters.get("y_start") + 1
                    parameters.setv("x_pixels", size_x)
                    parameters.setv("y_pixels", size_y)
                    # TODO: actually the value should related to the binning value
                    parameters.setv("bytes_per_frame", 2 * size_x * size_y)
                    self.camera.setACQMode("run_till_abort")
                    continue
                self.camera.setPropertyValue(pname, parameters.get(pname))
                self.parameters.setv(pname, parameters.get(pname))

            exposure_time_us = self.camera.getPropertyValue("exposure_time_us")
            readout_time = self.camera.getPropertyValue("sensor_readout_time_ns")
            if (exposure_time_us*1000 < readout_time):
                print(">> Warning! exposure time is shorter than readout time.")
            
            exposure_time = 1.0e-6 * exposure_time_us
            self.parameters.setv("exposure_time", exposure_time)
            self.parameters.setv("fps", 1/exposure_time)


            # Update camera frame size.
            
            self.parameters.setv("bytes_per_frame", 2 * size_x * size_y)
            if running:
                self.startCamera()
                
            self.camera_functionality.parametersChanged.emit()

    def closeShutter(self):
        print("!closeShutter")
        super().closeShutter()
        if self.camera_working:
            running = self.running
            if running:
                self.stopCamera()

            if self.reversed_shutter:
                self.camera.openShutter()
            else:
                self.camera.closeShutter()

            if running:
                self.startCamera()

    def openShutter(self):
        print("!openShutter")
        super().openShutter()
        if self.camera_working:
            running = self.running
            if running:
                self.stopCamera()

            if self.reversed_shutter:
                self.camera.closeShutter()
            else:
                self.camera.openShutter()

            if running:
                self.startCamera()

    def setGain(self, gain):
        super().setGain(gain)
        if self.camera_working:
            running = self.running
            if running:
                self.stopCamera()

            self.camera.setPropertyValue("gain", gain)

            if running:
                self.startCamera()        

    def startCamera(self):
        super().startCamera()
        #self.camera.camera.arm(2)

    def stopCamera(self):
        super().stopCamera()
        #self.camera.camera.disarm()

    def startFilm(self, film_settings, is_time_base):
        super().startFilm(film_settings, is_time_base)
        if self.camera_working:
            if self.film_length is not None:
                print("????????????????????")
                print(self.film_length)
                if (self.film_length > 1000):
                    self.camera.setACQMode("run_till_abort")
                else:
                    self.camera.setACQMode(
                            "fixed_length", 
                            number_frames = self.film_length)
            else:
                self.camera.setACQMode("run_till_abort")

    def stopFilm(self):
        super().stopFilm()
        if self.camera_working:
            self.camera.setACQMode("run_till_abort")

    def run(self):

        #
        # Note: The order is important here, we need to start the camera and
        #       only then set self.running. Otherwise HAL might think the
        #       camera is running when it is not.
        #
        self.camera.startAcquisition()
        self.running = True
        self.thread_started = True
        while(self.running):

            # Get data from camera and create frame objects.
            self.camera_mutex.lock()
            [frames, frame_size] = self.camera.getFrames()
            self.camera_mutex.unlock()

            fps = self.camera.getFPS()

            # Check if we got new frame data.
            if (len(frames) > 0):
                # Create frame objects.
                frame_data = []
                for cam_frame in frames:
                    aframe = frame.Frame(cam_frame,
                                         self.frame_number,
                                         frame_size[0],
                                         frame_size[1],
                                         self.camera_name)
                    frame_data.append(aframe)
                    self.frame_number += 1

                    if self.film_length is not None:                    
                        if (self.frame_number == self.film_length):
                            self.running = False
                            
                # Emit new data signal.
                self.newData.emit(frame_data)
            #self.msleep(5)

        self.camera.stopAcquisition()
 
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