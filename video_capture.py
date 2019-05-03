import cv2
from base_camera import BaseCamera
import time

# required class for video streaming

main = ""
class Camera(BaseCamera):
    @staticmethod
    def frames():
        while True:
            # Runs the main loop
            result = main.main()     
            yield cv2.imencode('.jpg', result)[1].tobytes()
