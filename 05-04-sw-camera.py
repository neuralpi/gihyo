from gpiozero import Button
from time import sleep
import datetime
import threading
import sys
import cv2
from picamera2 import Picamera2

(w, h)=(640, 480)

picam2 = Picamera2()
try:
    # camver=1 or camver=2
    camver = 1
    preview_config = picam2.create_preview_configuration({'format': 'XRGB8888', 'size': (w, h)}, raw=picam2.sensor_modes[3])
except IndexError:
    try:
        camver=3
        preview_config = picam2.create_preview_configuration({'format': 'XRGB8888', 'size': (w, h)}, raw=picam2.sensor_modes[2])
    except IndexError:
        camver=0
        preview_config = picam2.create_preview_configuration({'format': 'XRGB8888', 'size': (w, h)})
picam2.configure(preview_config)
picam2.start()

capturing = False
def takingPicture():
    global capturing
    d = datetime.datetime.today()
    filename = "{0}{1:02d}{2:02d}-{3:02d}{4:02d}{5:02d}.jpg".format(d.year, d.month, d.day, d.hour, d.minute, d.second)
    capturing = True
    cv2.imwrite(filename, frame)
    capturing = False

def pressed(button):
    if button.pin.number == 27:
        t = threading.Thread(target=takingPicture)
        t.start()

btn = Button(27, pull_up=False, bounce_time=0.05) # for Bookworm (gpiozero 2.0)
#btn = Button(27, pull_up=False, bounce_time=None) # for Bullseye (gpiozero 1.6.2)

btn.when_pressed = pressed

frame = picam2.capture_array()
try:
    while True:
        if not capturing:
            frame = picam2.capture_array()

        # frameをウインドウに表示
        cv2.imshow('frame', frame)

        # "q"を入力でアプリケーション終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass

btn.close()
cv2.destroyAllWindows()
