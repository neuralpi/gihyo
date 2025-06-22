import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from gpiozero import PWMOutputDevice
import os
import sys
from time import sleep

def pwm_check():
    global chipid, pwmchip, isOldPi5, isPi5, pwmid0, pwmid1
    if not os.access(pwmchip, os.F_OK):
        chipid = 0 # Pi 1-4, or Pi 5 with kernel 6.12+
        pwmid0 = 2 # Pi 5 with kernel 6.12+, GPIO18
        pwmid1 = 3 # Pi 5 with kernel 6.12+, GPIO19
        pwmchip = '/sys/class/pwm/pwmchip{}'.format(chipid)
        isOldPi5 = False
        isPi5 = True
        if not os.access(pwmchip, os.F_OK):
            print('{},2 do not exist. \'dtoverlay=pwm-2chan\' in /boot/firmware/config.txt is required.'.format(pwmchip))
            sys.exit()

def pi5_check():
    global pwmid0, pwmid1, pwmchip, isPi5
    pwmdir = '{}/pwm{}'.format(pwmchip, pwmid0)
    pwmexp = '{}/export'.format(pwmchip)
    if not os.path.isdir(pwmdir):
        try:
            with open(pwmexp, 'w') as f:
                f.write('{}\n'.format(pwmid0))
            sleep(0.3)
        except OSError:
            pwmid0 = 0 # Pi1-4, GPIO18
            pwmid1 = 1 # Pi1-4, GPIO19
            pwmchip = '/sys/class/pwm/pwmchip{}'.format(chipid)
            isPi5 = False

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

isOldPi5 = True # Pi 5 with kernel 6.6
isPi5 = False   # Pi 5 with kernel 6.12+
chipid = 2 # Pi5 with kernel 6.6
pwmid0 = 2 # Pi5 with kernel 6.6, GPIO18
pwmid1 = 3 # Pi5 with kernel 6.6, GPIO19
pwmchip = '/sys/class/pwm/pwmchip{}'.format(chipid)

pwm_check()
pi5_check()

pwm_open(pwmid0)
pwm_freq(pwmid0, 50) #Hz
pwm_duty(pwmid0, 1.35) #ms
pwm_enable(pwmid0)

app = FastAPI()
app.mount(path="/10-3/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

out1 = PWMOutputDevice(25)
out2 = PWMOutputDevice(24)
out3 = PWMOutputDevice(23)
out4 = PWMOutputDevice(22)
out1.value = 0
out2.value = 0
out3.value = 0
out4.value = 0

@app.get('/10-3/get/{rate1}/{rate2}/{rate3}/{rate4}')
async def get(rate1: str, rate2: str, rate3: str, rate4:str):
    rate1_f = float(rate1)
    rate2_f = float(rate2)
    rate3_f = float(rate3)
    rate4_f = float(rate4)

    out1.value = rate1_f
    out2.value = rate2_f
    out3.value = rate3_f
    out4.value = rate4_f

    return rate1_f

@app.get('/10-3/get_servo/{rate}')
async def get_servo(rate: str):
    rate_f = float(rate)
    pwm_duty(pwmid0, servo_duty_hwpwm(rate_f))
    return rate_f

@app.get('/10-3', response_class=HTMLResponse)
async def index(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)

try:
    uvicorn.run(app, host='0.0.0.0', port=8000)
except KeyboardInterrupt:
    pass

pwm_disable(pwmid0)
out1.close()
out2.close()
out3.close()
out4.close()
