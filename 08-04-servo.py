from gpiozero import MCP3208
from time import sleep
import os
import sys

def pwm_check():
    global chipid, pwmchip, isPi5, pwmid0, pwmid1
    if not os.access(pwmchip, os.F_OK):
        print('If you are using Pi 5, please add \'dtoverlay=pwm-2chan\' in /boot/firmware/config.txt.')
        chipid = 0 # Pi 1-4
        pwmid0 = 0 # Pi 1-4, GPIO18
        pwmid1 = 1 # Pi 1-4, GPIO19
        pwmchip = '/sys/class/pwm/pwmchip{}'.format(chipid)
        isPi5 = False
        if not os.access(pwmchip, os.F_OK):
            print('{},2 do not exist. \'dtoverlay=pwm-2chan\' in /boot/firmware/config.txt is required.'.format(pwmchip))
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

adc0 = MCP3208(0)

try:
    while True:
        inputVal0 = adc0.value
        pwm_duty(pwmid0, servo_duty_hwpwm(inputVal0))
        sleep(0.2)

except KeyboardInterrupt:
    pass

pwm_disable(pwmid0)
adc0.close()
