#/bin/bash

libcamera-vid --timeout 0000 --nopreview --inline --listen -o tcp://0.0.0.0:55000

echo "Command exited with code $?"

exit 0
