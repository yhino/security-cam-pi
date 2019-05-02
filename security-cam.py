# coding:utf-8

import os

# ENV
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', '')
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL', '')
CAMERA_ROTATE = os.environ.get('CAMERA_ROTATE', '180')
CAMERA_BRIGHTNESS = os.environ.get('CAMERA_BRIGHTNESS', '50')
DEBUG = os.environ.get('DEBUG', 'off')

# LOGGER
import logging
if DEBUG.lower() == 'on':
    level = logging.DEBUG
else:
    level = logging.INFO
logger = logging.getLogger(__name__)
logger.setLevel(level)
handler = logging.StreamHandler()
handler.setLevel(level)
formatter  = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.propagate = False

import cv2
from datetime import datetime
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import requests

# Setup Camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 15
camera.rotation = int(CAMERA_ROTATE)
camera.brightness = int(CAMERA_BRIGHTNESS)

cap = PiRGBArray(camera, size=(640, 480))

model = cv2.dnn.readNetFromTensorflow('models/frozen_inference_graph.pb',
                                      'models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt')

logger.info('wait boot camera')

time.sleep(2.0)

logger.info('start capture')

for frame in camera.capture_continuous(cap, format='bgr', use_video_port=True):
    logger.debug('capture processing')

    image = frame.array
    image_height, image_width, _ = image.shape

    # detection
    logger.debug('detection')

    model.setInput(cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True))
    output = model.forward()

    objects = []
    for detection in output[0, 0, :, :]:
        confidence = detection[2]
        if confidence > .5:
            class_id = detection[1]
            if class_id == 1:
                objects.append([
                    int(detection[3] * image_width),     # x
                    int(detection[4] * image_height),    # y
                    int(detection[5] * image_width),     # width
                    int(detection[6] * image_height),    # height
                    ])


    if len(objects) < 1:
        cap.truncate(0)
        continue

    for (x, y, w, h) in objects:
        # Draw rectangle around the objects
        cv2.rectangle(image, (x, y), (w, h), (0, 255, 0), 2)

    # Save image
    writeFilename = '/tmp/{}-{}.jpg'.format(datetime.now().strftime('%Y%m%d%H%M%S'), int(round(time.time() * 1000)))
    cv2.imwrite(writeFilename, image)

    logger.info('write filename = {}'.format(writeFilename))

    # Post to slack
    files = {'file': open(writeFilename, 'rb')}
    params = {'filename': writeFilename, 'token': ACCESS_TOKEN, 'channels': [SLACK_CHANNEL]}
    res = requests.post(url="https://slack.com/api/files.upload",params=params, files=files)

    logger.info('post to slack, response = {}'.format(res))

    cap.truncate(0)
