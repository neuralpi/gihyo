from gpiozero import LED, Button
from time import sleep
import subprocess
from signal import pause

def pressed(button):
    if button.pin.number == 27:
        global isPlaying
        global process
        if isPlaying == False:
            isPlaying = True
            led.on()
            args = ['mplayer', '05-07-test.mp3']
            process = subprocess.Popen(args)
        else:
            isPlaying = False
            led.off()
            args = ['kill', str(process.pid)]
            subprocess.Popen(args)

led = LED(25)
btn = Button(27, pull_up=False, bounce_time=0.05) # for Bookworm (gpiozero 2.0)
#btn = Button(27, pull_up=False, bounce_time=None) # for Bullseye (gpiozero 1.6.2)

isPlaying = False
process = None

btn.when_pressed = pressed

try:
    pause()
except KeyboardInterrupt:
    pass

led.close()
btn.close()
