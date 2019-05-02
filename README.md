# Security-Cam-Pi

Security Camera Script running on Raspberry Pi


## Requirement

```
sudo apt-get install \
    python3 \
    python3-picamera \
    python3-requests

# opencv-3.x
wget https://github.com/mt08xx/files/raw/master/opencv-rpi/libopencv3_3.4.4%2Brpi01-20181119.2_armhf.deb && \
    sudo apt install -y ./libopencv3_3.4.4+rpi01-20181119.2_armhf.deb && \
    sudo ldconfig

# pretrained model

```


## Install

1. Clone
    ```
    git clone https://github.com/yhinoz/security-cam-pi.git
    ```
2. Create `run.sh`, It's easy to copy `run.sh.sample`
    ```
    cp run.sh.sample run.sh
    ```
3. Change the "YOUR-SLACK-TOKEN" and "YOUR-SLACK-CHANNEL" in `run.sh`

4. Install pretrained model
    ```
    mkdir -p models && \
        wget https://github.com/rdeepc/ExploreOpencvDnn/raw/master/models/frozen_inference_graph.pb && \
        wget https://raw.githubusercontent.com/rdeepc/ExploreOpencvDnn/master/models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt
    ```


## Usage

Run simple.

    /your-install-dir/run.sh

When want to run debug mode,

    DEBUG=on /your-install-dir/run.sh

