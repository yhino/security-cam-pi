# coding:utf-8

import os

CAMERA_ROTATE = os.environ.get('CAMERA_ROTATE', 180)
CAMERA_BRIGHTNESS = os.environ.get('CAMERA_BRIGHTNESS', 50)

from picamera import PiCamera
import time

camera = PiCamera()
camera.resolution = (640, 480)
camera.rotation = CAMERA_ROTATE
camera.brightness = CAMERA_BRIGHTNESS

camera.start_preview()

time.sleep(10)

camera.stop_preview()
