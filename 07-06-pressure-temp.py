# 用途: 気圧・温度センサー
# チップ: LPS25HB
# 型番など: 秋月電子通商(113460)
#
# 接続: I2Cデバイス - Raspberry Pi
# VDD - 3.3V
# SCL - I2C SCL
# SDA - I2C SDA
# 4 - GND
# 5 - 3.3V
# 6 - 接続なし
# 7 - 接続なし
# GND - GND
#
# 気圧[hPa], 温度[degree]
# が表示される
#
import smbus
from time import sleep

address_lps25hb = 0x5c

def read_lps25hb_pressure():
    data = bus.read_i2c_block_data(address_lps25hb, 0x28 | 0x80, 3)
    return (data[2]<<16 | data[1] <<8 | data[0]) / 4096.0

def read_lps25hb_temp():
    data = bus.read_i2c_block_data(address_lps25hb, 0x2B | 0x80, 2)
    temp = data[1] <<8 | data[0]
    if temp>32767:
        temp -= 65536
    return temp/480.0 + 42.5

bus = smbus.SMBus(1)
bus.write_byte_data(address_lps25hb, 0x20, 0x90) # power on
sleep(0.1)

try:
    while True:
        pressure = read_lps25hb_pressure()
        temp = read_lps25hb_temp()
        print('{0:.2f}, {1:.2f}'.format(pressure, temp))
        sleep(0.5)

except KeyboardInterrupt:
    pass
