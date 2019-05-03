import numpy as np
import cv2
import scipy.io as sio
import math
from util.opencv_util import draw_rect
cascPath = "haarcascade_frontalface_default.xml"
eyePath = "haarcascade_eye.xml"
face_cascade = cv2.CascadeClassifier(cascPath)
eye_cascade = cv2.CascadeClassifier(eyePath)
def crop_frame(frame,rect):
    x = rect[0]
    y = rect[1]
    w = rect[2]
    h = rect[3]
    return frame[y:y+h,x:x+w]


def track_eyes(frame):
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray_frame, 1.35, 10)
    for eye in eyes:
        draw_rect(frame,eye)
    if len(eyes) >= 2:
        for i,eye1 in enumerate (eyes):
            for j,eye2 in enumerate(eyes):
                if not i == j:
                    d = abs(eye1[1] + eye1[3]/2 - (eye2[1]+ eye2[3]/2))
                    print(d)
                    if d < 20:
                        return True

    return False
      
       


class FaceTracker():
    def __init__(self):
        self.tracker =cv2.TrackerMOSSE_create()###cv2.TrackerKCF_create()#
        self.found_face = False
        self.enabled = True
    def resetTracker(self):
        self.found_face = False
        self.tracker =cv2.TrackerMOSSE_create()
    def crop_to_face(self,frame):
        if self.enabled:
            gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            success=False
            if not self.found_face:
                print("Face not yet found")
                faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)
                if len(faces)>0:
                    face=faces[0]
                    face=(face[0],face[1],face[2],face[3])
                    self.tracker.init(frame,face)
                    self.found_face= True
                    success = True
            else:
                (success, face) = self.tracker.update(frame) 
            if success:       
                x,y,dx,dy = face
                face = [int(x),max(int(y),0),int(dx),int(dy)]
                frame_cropped = crop_frame(frame,face)
                return frame_cropped
        return frame
        
         

