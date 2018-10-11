# Security-Cam-Pi

Security Camera Script running on Raspberry Pi

## Requirement

```
sudo apt-get install \
    python-picamera \
    python-opencv \
    python-requests
```

## Install

1. Clone

    git clone https://github.com/yhinoz/security-cam-pi.git

2. Create `run.sh`, It's easy to copy `run.sh.sample`

    cp run.sh.sample run.sh

3. change "YOUR-SLACK-TOKEN" and "YOUR-SLACK-CHANNEL"
    vim run.sh


## Usage

Run simple.

    /your-install-dir/run.sh

When want to run debug mode,

    DEBUG=on /your-install-dir/run.sh
