# 用途: 加速度x3、ジャイロx3、磁気コンパスx3
# チップ: BMX055
# 型番など: 秋月電子通商(113010)
#
# JP7に半田を盛ってショートさせる
#
# 接続: I2Cデバイス - Raspberry Pi
# GND - GND
# SDA - I2C SDA
# SCL - I2C SCL
# 3V3 - 3.3V
# VCCIO - 接続なし
# VCC - 3.3V
# ピン配置は商品ページでダウンロードできるPDFを参照すること
#
# acc[m/s^2]: x方向加速度、y方向加速度、z方向加速度
# gyro[deg/s]: x方向ジャイロ、y方向ジャイロ、z方向ジャイロ
# mag[μT]: x方向磁気、y方向磁気、z方向磁気
# が表示される
#
import smbus
import time
from time import sleep

bus = smbus.SMBus(1)

address_bmx055_acc = 0x19
address_bmx055_gyro = 0x69
address_bmx055_mag = 0x13

register_bmx055 = 0x02
register_bmx055_mag = 0x42

def read_bmx055_acc():
    ax_l = bus.read_byte_data(address_bmx055_acc, register_bmx055)
    ax_h = bus.read_byte_data(address_bmx055_acc, register_bmx055+1)
    ay_l = bus.read_byte_data(address_bmx055_acc, register_bmx055+2)
    ay_h = bus.read_byte_data(address_bmx055_acc, register_bmx055+3)
    az_l = bus.read_byte_data(address_bmx055_acc, register_bmx055+4)
    az_h = bus.read_byte_data(address_bmx055_acc, register_bmx055+5)

    ax = ax_h<<4 | ax_l>>4
    if ax > 2047:
        ax -= 4096
    ay =  ay_h<<4 | ay_l>>4
    if ay > 2047:
        ay -= 4096
    az =  az_h<<4 | az_l>>4
    if az > 2047:
        az -= 4096

    # range: +-2g (0.00958 = 2g/2048)
    ax = ax * 0.00958
    ay = ay * 0.00958
    az = az * 0.00958

    print ('acc : {0:2.2f}, {1:2.2f}, {2:2.2f}'.format(ax, ay, az))

def read_bmx055_gyro():
    ox_l = bus.read_byte_data(address_bmx055_gyro, register_bmx055)
    ox_h = bus.read_byte_data(address_bmx055_gyro, register_bmx055+1)
    oy_l = bus.read_byte_data(address_bmx055_gyro, register_bmx055+2)
    oy_h = bus.read_byte_data(address_bmx055_gyro, register_bmx055+3)
    oz_l = bus.read_byte_data(address_bmx055_gyro, register_bmx055+4)
    oz_h = bus.read_byte_data(address_bmx055_gyro, register_bmx055+5)

    ox = ox_h<<8 | ox_l
    if ox > 32767:
        ox -= 65536
    oy = oy_h<<8 | oy_l
    if oy > 32767:
        oy -= 65536
    oz = oz_h<<8 | oz_l
    if oz > 32767:
        oz -= 65536

    # range: +-125 deg/s (0.0038 = 125/32768)
    ox = ox * 0.0038
    oy = oy * 0.0038
    oz = oz * 0.0038

    print ('gyro: {0:2.2f}, {1:2.2f}, {2:2.2f}'.format(ox, oy, oz))

def read_bmx055_mag():
    mx_l = bus.read_byte_data(address_bmx055_mag, register_bmx055_mag)
    mx_h = bus.read_byte_data(address_bmx055_mag, register_bmx055_mag+1)
    my_l = bus.read_byte_data(address_bmx055_mag, register_bmx055_mag+2)
    my_h = bus.read_byte_data(address_bmx055_mag, register_bmx055_mag+3)
    mz_l = bus.read_byte_data(address_bmx055_mag, register_bmx055_mag+4)
    mz_h = bus.read_byte_data(address_bmx055_mag, register_bmx055_mag+5)

    mx = mx_h<<5 | mx_l>>3
    if mx > 4095:
        mx -= 8192
    my = my_h<<5 | my_l>>3
    if my > 4095:
        my -= 8192
    mz = mz_h<<7 | mz_l>>1
    if mz > 16383:
        mz -= 32768
    # range: +-1300μT (0.317 = 1300/4096)
    mx = mx * 0.317
    my = my * 0.317
    # range: +-2500μT (0.153 = 2500/16384)
    mz = mz * 0.153

    print ('mag : {0:.2f}, {1:.2f}, {2:.2f}'.format(mx, my, mz))

# setup for accelerometer
bus.write_byte_data(address_bmx055_acc, 0x0F, 0x03) # Range=+-2g
sleep(0.1)
bus.write_byte_data(address_bmx055_acc, 0x10, 0x08) # Bandwidth=7.81Hz
sleep(0.1)
bus.write_byte_data(address_bmx055_acc, 0x11, 0x00) # Sleep duration=0.5ms
sleep(0.1)

# setup for gyroscope
bus.write_byte_data(address_bmx055_gyro, 0x0F, 0x04) # Range=+-125 deg/s
sleep(0.1)
bus.write_byte_data(address_bmx055_gyro, 0x10, 0x07) # ODR=100Hz
sleep(0.1)
bus.write_byte_data(address_bmx055_gyro, 0x11, 0x00) # Sleep duration=2ms
sleep(0.1)

# setup for magnetmeter
bus.write_byte_data(address_bmx055_mag, 0x4B, 0x01) # Power on
sleep(0.1)
bus.write_byte_data(address_bmx055_mag, 0x4C, 0x00) # ODR=10Hz
sleep(0.1)
bus.write_byte_data(address_bmx055_mag, 0x4E, 0x84) # X,Y,Z-axis enabled
sleep(0.1)
bus.write_byte_data(address_bmx055_mag, 0x51, 0x04) # No of Repetitions XY=9
sleep(0.1)
bus.write_byte_data(address_bmx055_mag, 0x52, 0x16) # No of Repetitions Z=15
sleep(0.1)

try:
    while True:
        read_bmx055_acc()
        read_bmx055_gyro()
        read_bmx055_mag()
        sleep(0.2)

except KeyboardInterrupt:
    pass
