from time import time
from PIL import ImageGrab
import numpy as np
import cv2 as cv2

class Input:
    def __init__(self, show_fps=False):
        self.show_fps = show_fps
        self.loop_time = time()

    def Start(self):
        pass

    def CaptureFrame(self, rect=None):
        pass

    def GetFrame(self):
        return self.frame

    def ShowFPS(self):
        if (self.show_fps):
            fps = 1 / min(time() - self.loop_time, 1)
            self.frame = cv2.putText(self.frame, f'FPS {int(fps)}', (16, 32), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255,0,0), 1, 0)
            self.loop_time = time()

    def Stop(self):
        pass

class Webcam(Input):
    def Start(self, index=0):
        self.cap = cv2.VideoCapture(index)

        if not self.cap.isOpened():
            print("Cannot open camera")
            exit()

    def CaptureFrame(self, rect=None):
        # Capture frame-by-frame
        rect, self.frame = self.cap.read()
        
        # if frame is read correctly ret is True
        if not rect:
            print("Can't receive frame (stream end?). Exiting ...")
            exit()
        return self.frame

    def Stop(self):
        self.cap.release()

class Screencast(Input):
    def CaptureFrame(self, rect=None): # x, y, w, h
        screenshot = ImageGrab.grab(bbox=rect)
        self.frame = np.array(screenshot)
        self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
        return self.frame

    def GetFrame(self):
        return cv2.resize(self.frame.copy(), (800, 450))
