import subprocess
from time import sleep
import datetime
import re

mjpg_env = {'LD_LIBRARY_PATH': '/opt/mjpg-streamer/'}
opt_in = 'input_libcamera.so -camver 1 -fps 15 -r 640x480 -s 640x480'
opt_out = 'output_http.so -p 9000 -w /opt/mjpg-streamer/www'
mjpg_cmd = ['/opt/mjpg-streamer/mjpg_streamer', '-i', opt_in , '-o', opt_out]

launchApp = True

try:
    while True:

        if launchApp :
            p = subprocess.Popen(mjpg_cmd, env=mjpg_env)
            launchApp = False

        check_cmd = ['ps', 'ho', 'command', str(p.pid)]
        check_p = subprocess.Popen(check_cmd, stdout=subprocess.PIPE)
        line = check_p.stdout.readline()
        s = line.decode('utf-8')
        if re.search('defunct', s) != None: 
            p.kill()
            launchApp = True

        sleep(2)

except KeyboardInterrupt:
    pass

p.kill()
