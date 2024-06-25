from gpiozero import MCP3208, PWMLED
from time import sleep

adc0 = MCP3208(0)
led = PWMLED(25)

try:
    while True:
        inputVal0 = adc0.value
        led.value = inputVal0
        sleep(0.2)

except KeyboardInterrupt:
    pass

adc0.close()
led.close()
