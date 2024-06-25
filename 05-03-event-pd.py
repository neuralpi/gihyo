from gpiozero import LED, Button
from time import sleep
from signal import pause

def pressed(button):
    if button.pin.number == 27:
        global ledState 
        ledState = not ledState
        if ledState == 1:
            led.on()
        else:
            led.off()

led = LED(25)
btn = Button(27, pull_up=False, bounce_time=0.05) # Bookworm (gpiozero 2.0) 用
#btn = Button(27, pull_up=False, bounce_time=None) # Bullseye (gpiozero 1.6.2) 用

btn.when_pressed = pressed
ledState = led.value

try:
    pause()
except KeyboardInterrupt:
    pass

led.close()
btn.close()
