#/bin/bash

libcamera-vid --nopreview --bitrate 10000000 --codec h264 --framerate 30 --width 1920 --height 1080 --timeout 0000 --inline --listen -o tcp://0.0.0.0:8888

echo "Command exited with code $?"

exit 0
