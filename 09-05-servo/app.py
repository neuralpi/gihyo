import os
import sys
from time import sleep
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

def pwm_check():
    global chipid, pwmchip, isPi5, pwmid0, pwmid1
    if not os.access(pwmchip, os.F_OK):
        chipid = 0 # Pi 1-4
        pwmid0 = 0 # Pi 1-4, GPIO18
        pwmid1 = 1 # Pi 1-4, GPIO19
        pwmchip = '/sys/class/pwm/pwmchip{}'.format(chipid)
        isPi5 = False
        if not os.access(pwmchip, os.F_OK):
            print('{},4 do not exist. \'dtoverlay=pwm-2chan\' in /boot/config.txt is required. '.format(pwmchip))
            sys.exit()

def pwm_open(pwmid):
    pwmdir = '{}/pwm{}'.format(pwmchip, pwmid)
    pwmexp = '{}/export'.format(pwmchip)
    if not os.path.isdir(pwmdir):
        with open(pwmexp, 'w') as f:
            f.write('{}\n'.format(pwmid))
    sleep(0.3)

def pwm_freq(pwmid, freq): # Hz
    pwmdir = '{}/pwm{}'.format(pwmchip, pwmid)
    pwmperiod = '{}/period'.format(pwmdir)
    period = int(1000000000/freq)
    with open(pwmperiod, 'w') as f:
        f.write('{}\n'.format(period))

def pwm_duty(pwmid, duty): # ms
    pwmdir = '{}/pwm{}'.format(pwmchip, pwmid)
    pwmduty = '{}/duty_cycle'.format(pwmdir)
    dutyns = int(1000000*duty)
    with open(pwmduty, 'w') as f:
        f.write('{}\n'.format(dutyns))

def pwm_enable(pwmid):
    pwmdir = '{}/pwm{}'.format(pwmchip, pwmid)
    pwmenable = '{}/enable'.format(pwmdir)
    with open(pwmenable, 'w') as f:
        f.write('1\n')

def pwm_disable(pwmid):
    pwmdir = '{}/pwm{}'.format(pwmchip, pwmid)
    pwmenable = '{}/enable'.format(pwmdir)
    with open(pwmenable, 'w') as f:
        f.write('0\n')

def servo_duty_hwpwm(val):
    val_min = 0
    val_max = 1
    servo_min = 0.7 # ms
    servo_max = 2.0 # ms
    duty = (servo_min-servo_max)*(val-val_min)/(val_max-val_min) + servo_max
    # サーボモーターを逆向きに回転させたい場合はこちらを有効に
    #duty = (servo_max-servo_min)*(val-val_min)/(val_max-val_min) + servo_min
    return duty

isPi5 = True
chipid = 2 # Pi5
pwmid0 = 2 # Pi5, GPIO18
pwmid1 = 3 # Pi5, GPIO19
pwmchip = '/sys/class/pwm/pwmchip{}'.format(chipid)

pwm_check()

pwm_open(pwmid0)
pwm_freq(pwmid0, 50) #Hz
pwm_duty(pwmid0, 1.35) #ms
pwm_enable(pwmid0)

pwm_open(pwmid1)
pwm_freq(pwmid1, 50) #Hz
pwm_duty(pwmid1, 1.35) #ms
pwm_enable(pwmid1)

app = FastAPI()
app.mount(path="/9-5/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get('/9-5/get/{servoID}/{rate}')
async def get(servoID: int, rate: str):
    rate_f = float(rate)
    if servoID == 0:
        pwm_duty(pwmid0, servo_duty_hwpwm(rate_f))
    elif servoID == 1:
        pwm_duty(pwmid1, servo_duty_hwpwm(rate_f))
    return rate_f

@app.get('/9-5', response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)

try:
    uvicorn.run(app, host='0.0.0.0', port=8000)
except KeyboardInterrupt:
    pass

pwm_disable(pwmid0)
pwm_disable(pwmid1)
