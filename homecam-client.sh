#/bin/bash

libcamera-vid --nopreview --bitrate 10000000 --codec h264 --framerate 30 --width 1920 --height 1080 --timeout 0000 --inline --listen -o tcp://0.0.0.0:8888

#libcamera-vid --nopreview --bitrate 5000000 --codec h264 --framerate 25 --quality 50 --width 1920 --height 1080 --timeout 0000 --inline -o - | ffmpeg -re -i - -vcodec copy -tune zerolatency -f h264 -rtsp_transport rtsp rtsp://localhost:8554/live
echo "Command exited with code $?"

exit 0
