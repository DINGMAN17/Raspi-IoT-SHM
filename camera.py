import time
from picamera import PiCamera
import subprocess

camera = PiCamera()

camera.start_preview()
time.sleep(60)
camera.stop_preview()