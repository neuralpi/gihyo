import smbus
import sys
from time import sleep

def read_adt7410():
    word_data = bus.read_word_data(address_adt7410, register_adt7410)
    data = (word_data & 0xff00)>>8 | (word_data & 0xff)<<8
    data = data>>3  # 13ビットデータ
    if data & 0x1000 == 0:  # 温度が正または0の場合
        temperature = data*0.0625
    else:  # 温度が負の場合、絶対値を取ってからマイナスをかける
        temperature = ( (~data&0x1fff) + 1)*-0.0625
    return temperature

def setup_st7032():
    trials = 5
    for i in range(trials):
        try:
            c_lower = (contrast & 0xf)
            c_upper = (contrast & 0x30)>>4
            bus.write_i2c_block_data(address_st7032, register_setting, [0x38, 0x39, 0x14, 0x70|c_lower, 0x54|c_upper, 0x6c])
            sleep(0.2)
            bus.write_i2c_block_data(address_st7032, register_setting, [0x38, 0x0d, 0x01])
            sleep(0.001)
            break
        except IOError:
            if i==trials-1:
                sys.exit()

def clear():
    global position
    global line
    position = 0
    line = 0
    bus.write_byte_data(address_st7032, register_setting, 0x01)
    sleep(0.001)

def newline():
    global position
    global line
    if line == display_lines-1:
        clear()
    else:
        line += 1
        position = chars_per_line*line
        bus.write_byte_data(address_st7032, register_setting, 0xc0)
        sleep(0.001)

def write_string(s):
    for c in list(s):
        write_char(ord(c))

def write_char(c):
    global position
    byte_data = check_writable(c)
    if position == display_chars:
        clear()
    elif position == chars_per_line*(line+1):
        newline()
    bus.write_byte_data(address_st7032, register_display, byte_data)
    position += 1

def check_writable(c):
    if c >= 0x06 and c <= 0xff :
        return c
    else:
        return 0x20 # 空白文字

bus = smbus.SMBus(1)
address_adt7410 = 0x48
register_adt7410 = 0x00

address_st7032 = 0x3e
register_setting = 0x00
register_display = 0x40

contrast = 32 # 0から63のコントラスト。30から40程度を推奨
chars_per_line = 8  # LCDの横方向の文字数
display_lines = 2   # LCDの行数

display_chars = chars_per_line*display_lines

position = 0
line = 0

setup_st7032()

try:
    while True:
        inputValue = read_adt7410()
        try:
            clear()
            s = str(inputValue)
            write_string(s)
        except IOError:
            print('接続エラースキップ')
        sleep(1)

except KeyboardInterrupt:
    pass
