from server import create_server
from UIInstructions import *
import video_capture
import time
import cv2
import numpy as np
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

from skinclassifier import SkinClassifier
from facetracker import FaceTracker
from rppgsensor import SimplePPGSensor
from signalprocessor import extract_pulse_chrominance,extract_pulse_PBV
from evaluator import Evaluator
from framecapture import WebcamCapture
import os


class Main:
    def __init__(self):
        self.frameCapture = WebcamCapture() #Stationary(1)
        self.SkinClassifier = SkinClassifier()
        self.faceTracker = FaceTracker()
        self.sensor = SimplePPGSensor(self.frameCapture)
        
        self.evaluator = Evaluator(self.frameCapture.fs)
        self.fps =  0
        self.tprev = 0
        self.display = 1
        self.detectionMethod = 0

    def resetMeasurement(self):
        print("Reseting measurements")
        self.faceTracker.resetTracker()
        self.sensor.reset(self.frameCapture)
        self.frameCapture.timestamps = []
    # this function will be called repeatedly
    def main(self):
        frame = self.frameCapture.get_frame()
        fs = self.frameCapture.fs
        face = []
        face = self.faceTracker.crop_to_face(frame)

        skin,pixels = self.SkinClassifier.apply_skin_classifier(face)
        self.sensor.sense_ppg(skin,pixels)
        
        if self.detectionMethod == 0:
            normalized_amplitude = extract_pulse_chrominance(self.frameCapture.fs,self.sensor.rppg)
        else:
            normalized_amplitude = extract_pulse_PBV(self.frameCapture.fs,self.sensor.rppg)
                
        self.evaluator.evaluate(fs,normalized_amplitude)
        
        self.fps = 1/(time.time() - self.tprev + 1e-10)
        self.tprev = time.time()

        if self.display == 2:
           return skin
        elif self.display == 1:
            return face
        else:
            return frame
        
main = Main()

video_capture.main = main
# Here the available ui elements are defined
uiInstructions = [
            Slider("maxh","SkinClassifier","Max Hue",0,255,main.SkinClassifier,None),
            Slider("minh","SkinClassifier","Min Hue",0,255,main.SkinClassifier,None),
            Slider("mins","SkinClassifier","Min Saturation",0,255,main.SkinClassifier,None),
            Slider("maxs","SkinClassifier","Max Saturation",0,255,main.SkinClassifier,None),
            Slider("minv","SkinClassifier","Min Value",0,255,main.SkinClassifier,None),
            Slider("maxv","SkinClassifier","Max Value",0,255,main.SkinClassifier,None),         
            Slider("elipse_size","SkinClassifier","Elipse Size",0,20,main.SkinClassifier,None),
            Slider("blursize","SkinClassifier","Blur Size",0,50,main.SkinClassifier,None), 
            Switch("enabled","SkinClassifier","Enabled",main.SkinClassifier,None), 
            
            AddingFigure(main,"t",["fps"],"t",["fps"]),
            AddingFigure(main.evaluator,"t",["curbpm"],"t",["curbpm"]), 
            AddingFigure(main.evaluator,"t",["cursnr"],"t",["cursnr"]),
            ReplacingFigure(main.evaluator,"f",["normalized_amplitude"],"frequency",["Normalized Amplitude"]),
            Button("Face Tracker","Reset Tracker",main.faceTracker,"resetTracker"),
            Switch("enabled","Face Tracker","Enabled",main.faceTracker,None), 
            
            
            #Dropdown("frameCapture","VideoSettings","Video Input",main,[Stationary(1),MixedMotion(1),WebcamCapture()],["Stationary","Mixed Motion","Webcam"],"resetMeasurement"),
           
            Dropdown("display","VideoSettings","Video Output",main,[0,1,2],["Source","Face","Face Skin Only"],None),
                      
            Button("VideoSettings","Reset Measurements",main,"resetMeasurement"),
            Dropdown("detectionMethod","Pulse Detection","DetectionMethod",main,[0,1],["Chrominance","PBV"],None)
            # Dropdown("selectedCamera","VideoSettings","Selected Camera",main,[1,0],["1","0"],"setCameraUpdate")    
            
                            
            
            
            ]


if __name__ == '__main__':
    print("test")
    os.system('start public/index.html')
    app = create_server(uiInstructions,lambda : video_capture.Camera())
    app.run(threaded = True)

