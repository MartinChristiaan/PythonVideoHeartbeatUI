import math
import numpy as np
from framecapture import FrameCapture
from util.opencv_util import *
class LandMarkRoiFinder():
    def get_roi(self,frame,landmarktracker):
        peyer = landmarktracker.peyer
        peyel = landmarktracker.peyel
        pmouth = landmarktracker.pmouth
    
        x0 = peyel[0]
        x1 = peyer[0]
        y0 = pmouth[1]
        y1 = max(peyer[1],peyel[1])
        h = y1 - y0
        w = x1 - x0
        rect = int(x0-w*1.3),int(y0+2.2*h),int(w*3.5),int(-2.5*h)
        draw_rect(frame,rect)
        return crop_frame(frame,rect)

        # Che
class PPGSensor():
    def __init__(self,framecapture:FrameCapture):
        self.rppgl = []
        self.rppg = np.array([])
        self.cap = framecapture     
    def sense_ppg(self,frame,numpixels):
        pass   
    def reset(self,framecapture:FrameCapture):
        self.rppgl = []
        self.rppg = np.array([])
        self.cap = framecapture
        

class SimplePPGSensor(PPGSensor):
    def sense_ppg(self,frame,num_pixels):
        r_avg = np.sum(frame[:,:,0])/num_pixels
        g_avg = np.sum(frame[:,:,1])/num_pixels
        b_avg = np.sum(frame[:,:,2])/num_pixels
        ppg = [r_avg,g_avg,b_avg]
        for i,col in enumerate(ppg):
            if math.isnan(col):
                ppg[i] = 0
        self.rppgl.append(ppg)
        # if len(self.rppgl)>300:
        #     del self.rppgl[0]
        rppg = np.transpose(np.array(self.rppgl))
        self.rppg = self.cap.resample(rppg)
        



class SimpleForeheadSensor(PPGSensor):
    def sense_ppg(self,frame,bp):

        sub_roi_rect = get_subroi_rect(frame,[.35,.70,.08,.23])
        draw_rect(frame,sub_roi_rect)
        forehead = crop_frame(frame,sub_roi_rect)
        num_pixels = forehead.shape[0] * forehead.shape[1]
        r_avg = np.sum(forehead[:,:,0])/num_pixels
        g_avg = np.sum(forehead[:,:,1])/num_pixels
        b_avg = np.sum(forehead[:,:,2])/num_pixels
        ppg = [r_avg,g_avg,b_avg]
        for i,col in enumerate(ppg):
            if math.isnan(col):
                ppg[i] = 0
        self.rppgl.append(ppg)
        # if len(self.rppgl)>300:
        #     del self.rppgl[0]
        rppg = np.transpose(np.array(self.rppgl[-300:]))
        self.rppg = self.cap.resample(rppg)
        


def blackout_regions(frame):
    regions = [[.20,.45,.30,.54],[.35,.70,.77,.93],[.55,.85,.30,.54]]
    #num_pixels = frame.shape[0] * frame.shape[1]
    rects = []
    for region in regions:
        #print(region)
        region_rect = get_subroi_rect(frame,region)
        #region = crop_frame(frame,region)
        blackout_rect(frame,region_rect) 
        rects.append(region_rect)
    #    num_pixels-=region_rect[2] * region_rect[3] 
    #return num_pixels
       

class RegionSensor(PPGSensor):
    def sense_ppg(self,frame,bp):
        regions = [[.15,.40,.45,.75],[.6,.85,.45,.75],[.35,.70,.08,.23]]

        num_pixels = 0
        r = []
        g = []
        b = []
        for region in regions:
            #print(region)
            region = get_subroi_rect(frame,region)
            draw_rect(frame,region)
            region = crop_frame(frame,region)
            r.append(np.sum(region[:,:,0]))
            g.append(np.sum(region[:,:,1]))
            b.append(np.sum(region[:,:,2]))
            num_pixels+=region.shape[0] * region.shape[1] 

        r_avg = sum(r)/num_pixels
        g_avg = sum(g)/num_pixels
        b_avg = sum(b)/num_pixels

        ppg = [r_avg,g_avg,b_avg]
        for i,col in enumerate(ppg):
            if math.isnan(col):
                ppg[i] = 0
        self.rppgl.append(ppg)
        # if len(self.rppgl)>300:
        #     del self.rppgl[0]
        rppg = np.transpose(np.array(self.rppgl[-300:]))
        self.rppg = self.cap.resample(rppg)
        




# import matlab.engine
# eng = matlab.engine.start_matlab()
# tf = eng.isprime(37)
# print(tf)