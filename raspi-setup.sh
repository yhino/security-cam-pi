#!/bin/bash

mkdir -p models && \
    wget https://github.com/rdeepc/ExploreOpencvDnn/raw/master/models/frozen_inference_graph.pb && \
    wget https://raw.githubusercontent.com/rdeepc/ExploreOpencvDnn/master/models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt

sudo apt install python3 python3-pip python3-picamera python3-requests && \
    wget https://github.com/mt08xx/files/raw/master/opencv-rpi/libopencv3_3.4.4%2Brpi01-20181119.2_armhf.deb && \
    sudo apt install -y ./libopencv3_3.4.4+rpi01-20181119.2_armhf.deb && \
    sudo ldconfig


