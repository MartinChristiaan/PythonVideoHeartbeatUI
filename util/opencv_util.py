import cv2
import os
import time
def write_text(img,text,location):
    font                   = cv2.FONT_HERSHEY_SIMPLEX
    fontScale              = 1
    fontColor              = (255,255,255)
    lineType               = 2
    cv2.putText(img,text,location,font,fontScale,fontColor,lineType)


def draw_rect(frame,rect):
    rects = [rect]
    for (x, y, w, h) in rects:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

def crop_frame(frame,rect):
    x = rect[0]
    y = rect[1]
    w = rect[2]
    h = rect[3]
    return frame[y:y+h,x:x+w]

def blackout_rect(frame,rect):
    x = rect[0]
    y = rect[1]
    w = rect[2]
    h = rect[3]
    frame[y:y+h,x:x+w,:] =0


def get_subroi_rect(frame_cropped,roi):
    w,h = frame_cropped.shape[:2]
    min_x = int(roi[0] * w)
    max_x = int(roi[1] * w)
    min_y = int(roi[2] * h)
    max_y = int(roi[3] * h)
    return [min_x,min_y,max_x-min_x,max_y-min_y]