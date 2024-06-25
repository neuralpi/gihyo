from gpiozero import Button
from time import sleep
import subprocess
from signal import pause

def pressed(button):
    if button.pin.number == 27:
        args = ['sudo', 'poweroff']
        subprocess.Popen(args)

btn = Button(27, pull_up=False, bounce_time=0.05) # for Bookworm (gpiozero 2.0)
#btn = Button(27, pull_up=False, bounce_time=None) # for Bullseye (gpiozero 1.6.2)

btn.when_pressed = pressed

try:
    pause()
except KeyboardInterrupt:
    pass

btn.close()
