from gpiozero import MCP3208, PWMOutputDevice
from time import sleep

adc0 = MCP3208(0)
out0 = PWMOutputDevice(25)
out1 = PWMOutputDevice(24)

try:
    while True:
        inputVal0 = adc0.value
        if inputVal0 > 0.025 and inputVal0 < 0.5:
            out1.value = 0
            out0.value = (0.5 - inputVal0) * 0.7 / 0.5
        elif inputVal0 >= 0.5 and inputVal0 < 0.975:
            out0.value = 0
            out1.value = (inputVal0 - 0.5) * 0.7 / 0.5
        sleep(0.2)

except KeyboardInterrupt:
    pass

adc0.close()
out0.close()
out1.close()
