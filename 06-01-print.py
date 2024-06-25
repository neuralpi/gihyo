from gpiozero import MCP3208
from time import sleep

adc0 = MCP3208(0)

try:
    while True:
        inputVal0 = adc0.value
        print(inputVal0)
        sleep(0.2)

except KeyboardInterrupt:
    pass

adc0.close()
