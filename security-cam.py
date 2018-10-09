# coding:utf-8

import os

# ENV
ACCESS_TOKEN = os.environ.get('ACCESS_TOKEN', '')
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL', '')

import cv2
from datetime import datetime
from picamera import PiCamera
from picamera.array import PiRGBArray
import time
import requests

# Setup Camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 1
camera.rotation = 270
camera.brightness = 65

cap = PiRGBArray(camera, size=(640, 480))

faceClassifier = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

time.sleep(0.1)

print('start capture')

for frame in camera.capture_continuous(cap, format='bgr', use_video_port=True):
    print('capture processing')

    image = frame.array

    # face detection
    print('face detection')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = faceClassifier.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
            )

    print('faces = {}'.format(len(faces)))
    if len(faces) < 1:
        cap.truncate(0)
        continue

    for (x, y, w, h) in faces:
        # Draw rectangle around the faces
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # TODO-2: Face recognition
        # TODO-2: Crop faces

    # Save image
    writeFilename = '/tmp/{}-{}.jpg'.format(datetime.now().strftime('%Y%m%d%H%M%S'), int(round(time.time() * 1000)))
    print('write filename = {}'.format(writeFilename))
    cv2.imwrite(writeFilename, image)

    # Post to slack
    files = {'file': open(writeFilename, 'rb')}
    params = {'filename': writeFilename, 'token': ACCESS_TOKEN, 'channels': [SLACK_CHANNEL]}
    res = requests.post(url="https://slack.com/api/files.upload",params=params, files=files)
    print('post to slack, response = {}'.format(res))

    cap.truncate(0)
