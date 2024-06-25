from gpiozero import MCP3208
from time import sleep
import subprocess

adc0 = MCP3208(0)

vol_old = -1

try:
    while True:
        inputVal0 = adc0.value
        vol = "{0}%".format(int(inputVal0*100))
        if vol != vol_old:
            print(vol)
            args = ['amixer','-q','cset','numid=3',vol]
            subprocess.Popen(args)
            vol_old = vol
        sleep(0.2)

except KeyboardInterrupt:
    pass

adc0.close()
