from gpiozero import Button
from time import sleep
import subprocess

state = 0 

btn = Button(27, pull_up=False)

try:
    while True:
        if btn.value == 1:
            if state == 2:
                state = 0
                args = ['sudo', 'poweroff']
                subprocess.Popen(args)
            else:
                state += 1
        else:
            state = 0

        sleep(0.5)

except KeyboardInterrupt:
    pass
