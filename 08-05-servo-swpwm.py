from gpiozero import MCP3208, Servo
from gpiozero.pins.native import NativeFactory
from time import sleep

adc0 = MCP3208(0)
servo = Servo(25)

try:
    while True:
        inputVal0 = adc0.value
        servo.value = 2*(0.5 - inputVal0)
        #servo.value = 2*(inputVal0 - 0.5)
        sleep(0.2)

except KeyboardInterrupt:
    pass

adc0.close()
servo.close()
