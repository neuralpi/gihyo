# チップ: TMP102
# 型番など: 千石電商など(SEN-13314)
#
# 接続: I2Cデバイス - Raspberry Pi
# GND - GND
# VCC - 3.3V
# SDA - I2C SDA
# SCL - I2C SCL
# ALT - 接続なし
# ADD0 - 接続なし
#
import smbus
from time import sleep

def read_tmp102():
    word_data =  bus.read_word_data(address_tmp102, register_tmp102)
    data = (word_data & 0xff00)>>8 | (word_data & 0xff)<<8
    data = data>>4  # 12ビットデータ
    if data & 0x800 == 0:  # 温度が正または0の場合
        temperature = data*0.0625
    else:  # 温度が負の場合、絶対値を取ってからマイナスをかける
        temperature = ( (~data&0xfff) + 1)*-0.0625
    return temperature

bus = smbus.SMBus(1)
address_tmp102 = 0x48
register_tmp102 = 0x00

try:
    while True:
        inputValue = read_tmp102()
        print(inputValue)
        sleep(0.5)

except KeyboardInterrupt:
    pass
