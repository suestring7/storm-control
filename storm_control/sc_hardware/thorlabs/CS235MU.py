#!/usr/bin/env python
"""
Thorlabs CS235MU control.

Yuan 06/22
"""
import traceback
import os
import sys
import storm_control.sc_library.halExceptions as halExceptions


from thorlabs_tsi_sdk.tl_camera import *
from thorlabs_tsi_sdk.tl_camera_enums import *
from thorlabs_tsi_sdk.tl_mono_to_color_processor import MonoToColorProcessorSDK

import tkinter as tk
from PIL import Image, ImageTk
import typing
import threading
import queue


def loadThorlabsDLL(thorlabs_dlls):
    #thorlabs_dlls = r"C:\Users\yxt5273\Downloads\Scientific_Camera_Interfaces_Windows-2.1\Scientific Camera Interfaces\SDK\Python Toolkit\dlls\64_lib"
    os.environ['PATH'] = thorlabs_dlls + os.pathsep + os.environ['PATH']
    try:
        # Python 3.8 introduces a new method to specify dll directory
        os.add_dll_directory(thorlabs_dlls)
    except AttributeError:
        print("unable to load thorlabs_dlls at path "+thorlabs_dlls)
        pass

# TODO: Use camera ID instead
class cs235mu(object):
    """
    Camera Interface class
    """
    def __init__(self):
        self.sdk = TLCameraSDK()
        camera_list = self.sdk.discover_available_cameras()
        self.camera = self.sdk.open_camera(camera_list[0])
        self.acquisition_mode = "run_till_abort"
        super().__init__()
        # Read-Only properties False, others True
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
                   "data_rate": True,     # Scientific-CCD cameras offer data rates of 20MHz or 40MHz. Compact-scientific cameras offer FPS30 or FPS50, which are frame rates supported by the camera when doing full-frame readout. 
                   "exposure_time_range_us": False,
                   "exposure_time_us": True,
                   "firmware_version": False,
                   "frame_rate_control_value": True,
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
                   "is_frame_rate_control_enabled": True,   #For short exposure times, the maximum frame rate is limited by the readout time of the sensor. For long exposure times, the frame rate is limited by the exposure time.
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
        self.setPropertyValue("operation_mode", OPERATION_MODE.SOFTWARE_TRIGGERED)
        self.vshutter = False
        self.printFullInfo()

    def printFullInfo(self):
        """
        Return the model and other information of the camera
        """
        for name in self.tcam_props:
            if not self.tcam_props[name]:
                print(name+": "+ str(self.getPropertyValue(name)))


    def getFPS(self):
        return self.camera.get_measured_frame_rate_fps()

    def getFrames(self):
        # TODO: why the camera always only return one frame at a time???
        if self.vshutter:
            return [[], self.frame_size]
        else:
            frames = []
            t_frame = self.camera.get_pending_frame_or_null()
            if t_frame is None:
                return [[], self.frame_size]
            else:
                return [[t_frame.image_buffer], self.frame_size]

    def getPropertyValue(self, name):
        if name in self.tcam_props:
            return getattr(self.camera, name)
        else:
            print(">> Unknown parameter '" + name + "'")
            return -1

    def setPropertyValue(self, name, value):
        if name in self.tcam_props and self.tcam_props[name]:
            setattr(self.camera, name, value)
        else:
            print(">> Unknown parameter '" + name + "', or the parameter is Read-Only" )

    def setACQMode(self, mode, number_frames = 10):
        '''
        Set the acquisition mode to either run until aborted or to 
        stop after acquiring a set number of frames.

        mode should be either "fixed_length" or "run_till_abort"

        if mode is "fixed_length", then number_frames indicates the number
        of frames to acquire.
        '''

        #print("cam set ACQ"+ mode)
        self.stopAcquisition()

        if mode == "fixed_length":
            self.acquisition_mode = mode
            self.number_frames = number_frames
            self.setPropertyValue("frames_per_trigger_zero_for_unlimited", number_frames)
        elif mode == "run_till_abort":
            self.acquisition_mode = mode
            self.number_frames = number_frames
            self.setPropertyValue("frames_per_trigger_zero_for_unlimited", 0)
        else:
            raise TCAMException("Unrecognized acqusition mode: " + mode)


    def startAcquisition(self):
        """
        Start data acquisition.
        """
        # Start acquisition.
        # TODO: does the arm number really make any difference? 
        self.camera.arm(2)
        self.frame_size = [self.getPropertyValue("image_width_pixels"), self.getPropertyValue("image_height_pixels")]

        if self.vshutter:
            pass
        else:      
            self.camera.issue_software_trigger()
            #
            # Allocate  image buffers.
            # We allocate enough to buffer 2 seconds of data or the specified 
            # number of frames for a fixed length acquisition
            # TODO: how to use this information?
            if self.acquisition_mode == "run_till_abort":
                n_buffers = int(2.0*self.getFPS())
            elif self.acquisition_mode == "fixed_length":
                n_buffers = self.number_frames

            self.number_image_buffers = n_buffers

    ## closeShutter
    #
    # Close the camera shutter. This will abort the current acquisition.
    def closeShutter(self):
        self.vshutter = True

    ## openShutter
    #
    # Open the camera shutter. This will abort the current acquisition.
    #
    def openShutter(self):
        self.vshutter = False

    def stopAcquisition(self):
        """
        Stop data acquisition.
        """
        if self.vshutter:
            pass
        else:
            # Stop acquisition.
            self.camera.disarm()

            #print("max camera backlog was", self.max_backlog, "of", self.number_image_buffers)
            #self.max_backlog = 0

            # Free image buffers.
            # TODO:
            self.number_image_buffers = 0
 
    def shutdown(self):
        self.closeShutter()
        self.camera.disarm()
        #self.camera.dispose()


    def run(self):
        self.startAcquisition()
        self.running = True
        counter = 0
        while(self.running):
            [frames, frame_size] = self.camera.getFrames()
            # Yuan: the frame_size is set by Width x Height
            #self.msleep(5)
            counter = counter+1
        print(counter)
        self.camera.stopAcquisition()

    def __del__(self):
        self.camera.dispose()
        self.sdk.dispose()


# TODO: if I would like to add something here
class TCAMException(halExceptions.HardwareException):
    pass


#
# Testing.
#
if (__name__ == "__main__"):

    import time
    import random

    tcam = cs235mu()
    tcam.printFullInfo()
    if False:

        # List support properties.
        if False:
            print("Supported properties:")
            props = hcam.getProperties()
            for i, id_name in enumerate(sorted(props.keys())):
                [p_value, p_type] = hcam.getPropertyValue(id_name)
                p_rw = hcam.getPropertyRW(id_name)
                read_write = ""
                if (p_rw[0]):
                    read_write += "read"
                if (p_rw[1]):
                    read_write += ", write"
                print("  ", i, ")", id_name, " = ", p_value, " type is:", p_type, ",", read_write)
                text_values = hcam.getPropertyText(id_name)
                if (len(text_values) > 0):
                    print("          option / value")
                    for key in sorted(text_values, key = text_values.get):
                        print("         ", key, "/", text_values[key])

        # Test setting & getting some parameters.
        if False:
            print(hcam.setPropertyValue("exposure_time", 0.001))

            #print(hcam.setPropertyValue("subarray_hsize", 2048))
            #print(hcam.setPropertyValue("subarray_vsize", 2048))
            print(hcam.setPropertyValue("subarray_hpos", 512))
            print(hcam.setPropertyValue("subarray_vpos", 512))
            print(hcam.setPropertyValue("subarray_hsize", 1024))
            print(hcam.setPropertyValue("subarray_vsize", 1024))

            print(hcam.setPropertyValue("binning", "1x1"))
            print(hcam.setPropertyValue("readout_speed", 2))
    
            hcam.setSubArrayMode()
            #hcam.startAcquisition()
            #hcam.stopAcquisition()

            params = ["internal_frame_rate",
                      "timing_readout_time",
                      "exposure_time"]

            #                      "image_height",
            #                      "image_width",
            #                      "image_framebytes",
            #                      "buffer_framebytes",
            #                      "buffer_rowbytes",
            #                      "buffer_top_offset_bytes",
            #                      "subarray_hsize",
            #                      "subarray_vsize",
            #                      "binning"]
            for param in params:
                print(param, hcam.getPropertyValue(param)[0])

        # Test 'run_till_abort' acquisition.
        if False:
            print("Testing run till abort acquisition")
            hcam.startAcquisition()
            cnt = 0
            for i in range(300):
                [frames, dims] = hcam.getFrames()
                for aframe in frames:
                    print(cnt, aframe[0:5])
                    cnt += 1

            print("Frames acquired: " + str(cnt))    
            hcam.stopAcquisition()

        # Test 'fixed_length' acquisition.
        if True:
            for j in range (10000):
                print("Testing fixed length acquisition")
                hcam.setACQMode("fixed_length", number_frames = 10)
                hcam.startAcquisition()
                cnt = 0
                iterations = 0
                while cnt < 11 and iterations < 20:
                    [frames, dims] = hcam.getFrames()
                    waitTime = random.random()*0.03
                    time.sleep(waitTime)
                    iterations += 1
                    print('Frames loaded: ' + str(len(frames)))
                    print('Wait time: ' + str(waitTime))
                    for aframe in frames:
                        print(cnt, aframe[0:5])
                        cnt += 1
                if cnt < 10:
                    print('##############Error: Not all frames found#########')
                    input("Press enter to continue")
                print("Frames acquired: " + str(cnt))        
                hcam.stopAcquisition()

                hcam.setACQMode("run_till_abort")
                hcam.startAcquisition()
                time.sleep(random.random())
                contFrames = hcam.getFrames()
                hcam.stopAcquisition()





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