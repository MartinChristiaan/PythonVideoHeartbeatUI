import cv2
import abc
import os
import time

class FrameCapture():
    def get_frame(self):
        return _,_
    def resample(self,rPPG):
        return rPPG
import numpy as np


class WebcamCapture(FrameCapture):
   
    def __init__(self):
        
        self.fs = 20
        # IMPORTANT set 1 to 0 here if you want default camera
        self.camera = cv2.VideoCapture(1)
        # self.camera.set(3, 1280)
        # self.camera.set(4, 720)
        self.timestamps = []
        self.tprev = None
        

    def get_frame(self):
        _,frame = self.camera.read()
        if not self.tprev == None:
            self.timestamps.append(self.timestamps[-1] + (time.time() - self.tprev))
        else:
            self.timestamps.append(0)
        self.tprev = time.time()

        return frame
    def resample(self,rPPG):
        if len(self.timestamps) == 0:
            self.timestamps.append(self.fs)
        t = np.arange(self.timestamps[0],self.timestamps[-1],1/self.fs)
            
        rPPG_resampled= np.zeros((3,t.shape[0]))
        for col in [0,1,2]:
            rPPG_resampled[col] = np.interp(t,self.timestamps,rPPG[col])
        
        
        return rPPG_resampled
        

