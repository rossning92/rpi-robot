#!/bin/bash

# sudo nano /etc/rc.local
# /home/pi/rpi-robot/rpi-robot.sh

cd "$(dirname "$0")"

# Stop previous instance
sudo killall --signal SIGINT --wait python3
sudo killall --wait mjpg_streamer

# Start pigpio deamon (to control GPIO)
sudo pigpiod

# Start mjpg-streamer to stream UVC camera.
(
    killall -9 mjpg_streamer
    cd ~/mjpg-streamer-master/mjpg-streamer-experimental
    export LD_LIBRARY_PATH=.
    mjpg_streamer -i "input_uvc.so -d /dev/video0 -r 640x480" -o "output_http.so -w ./www" &
)

# Start rpi-robot web server
python3 main.py
