import cv2
import numpy as np

class SkinClassifier:
    def __init__(self):
        self.minh = 0
        self.mins = 40
        self.minv = 80
        self.maxh = 20
        self.maxs = 255
        self.maxv = 255
        self.elipse_size = 12
        self.blursize = 5

        self.num_skin_pixels = 0
        self.myy = 100
        self.enabled = True
   

    def apply_skin_classifier(self,frame):
        if self.enabled:
            try:
                lower = np.array([self.minh, self.mins, self.minv], dtype = "uint8")
                upper = np.array([self.maxh, self.maxs, self.maxv], dtype = "uint8")
                elipse_size = int(self.elipse_size)
                blursize = int(self.blursize)
                converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                skinMask = cv2.inRange(converted, lower, upper)
                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (elipse_size, elipse_size))
                skinMask = cv2.erode(skinMask, kernel, iterations = 2)
                skinMask = cv2.dilate(skinMask, kernel, iterations = 2)
                skinMask = cv2.GaussianBlur(skinMask, (blursize, blursize), 0)
            
                self.num_skin_pixels = skinMask.clip(0,1).sum()
                skin = cv2.bitwise_and(frame, frame, mask = skinMask)
                return skin,self.num_skin_pixels
            except:
                return frame,frame.shape[0] * frame.shape[1]
        else:
            return frame,frame.shape[0] * frame.shape[1]
