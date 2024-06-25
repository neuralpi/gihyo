from gpiozero import LED, Button
from time import sleep

led = LED(25)
btn = Button(27, pull_up=None, active_state=True)

try:
    while True:
        if btn.value == 1:  # if btn.is_pressed: とも書ける
            led.on()
        else:
            led.off()
        sleep(0.01)

except KeyboardInterrupt:
    pass

led.close()
btn.close()
