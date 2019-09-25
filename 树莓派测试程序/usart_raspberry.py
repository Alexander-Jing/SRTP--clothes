import time
import serial
from serial import Serial
import string

# 这是树莓派的串口测试程序
# 配置串口 115200波特率 8位字长 没有校验位 1位停止位 （与接下来要用的 stm32 一致）
ser = serial.Serial("com17", baudrate = 115200, bytesize = 8, parity = 'N', stopbits = 1, timeout = 0.5) #"/dev/ttyUSB0"
"""
# 显示一下看看配置
print(ser.bytesize)
print(ser.parity)
print(ser.stopbits)
"""

def raspberry_usart(turn):
    while (turn):
        # 获得接收缓冲区字符
        count = ser.inWaiting()  # inwaiting 是获取缓冲区中字符个数的函数
        if count !=0 :
            # 读取内容并回显
            recv = ser.read(count)  # 读取缓冲区里面数据
            #print(recv)
            recv = recv.split()
            a = float(recv[0])
            b = float(recv[1])
            c = float(recv[2])
            recv = [a , b , c]
            print(recv)
            #ser.write(recv)
        # 清空接收缓冲区
        ser.flushInput()
        # 必要的软件延时
        time.sleep(0.1)
    ser.close()

raspberry_usart(1)
