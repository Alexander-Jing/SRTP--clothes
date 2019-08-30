import time
import serial
from serial import Serial
import string
import tensorflow.keras
from tensorflow.keras.models import load_model
import numpy as np 
import h5py
import pandas as pd

# 这是树莓派的串口测试程序
# 配置串口 115200波特率 8位字长 没有校验位 1位停止位 （与接下来要用的 stm32 一致）
ser = serial.Serial("com5", baudrate = 115200, bytesize = 8, parity = 'N', stopbits = 1, timeout = 0.5) #"/dev/ttyUSB0"
"""
# 显示一下看看配置
print(ser.bytesize)
print(ser.parity)
print(ser.stopbits)
"""
savepath = "E:\\MachineLearning\\keras\\cloth_model_1.h5" # 导入模型，到时自己改下路径
model_load = load_model(savepath)


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
            recv = np.array([[a , b , c]]) # 读取数据并且转化为模型输入
            print(recv)
            data = recv 
            pre = 4*int(model_load.predict(data)[0][0]) # 输出转化
            print(pre)
            if pre < 20:
                pre4 = 1
            else :
                pre4 = 0
            pre1 = (int(pre/100))
            pre2 = (int(pre%100/10))
            pre3 = (int(pre%10)) # 输出发送
            '''
            print(pre1)
            print(pre2)
            print(pre3) # 中断打印输出
            '''
            ser.write(trans_asc(pre1)) # 发送数据给串口 3个
            ser.write(trans_asc(pre2))
            ser.write(trans_asc(pre3))
            ser.write(trans_asc(pre4))
            print('send to stm32')
            # 清空接收缓冲区
            ser.flushInput()
            
        # 必要的软件延时
        time.sleep(0.5)
    ser.close()

def trans_asc(data): # 数据的ascii 转码函数
    if(int(data) == 0):
        return b'0'
    if(int(data) == 1):
        return b'1'
    if(int(data) == 2):
        return b'2'
    if(int(data) == 3):
        return b'3'
    if(int(data) == 4):
        return b'4'
    if(int(data) == 5):
        return b'5'
    if(int(data) == 6):
        return b'6'
    if(int(data) == 7):
        return b'7'  
    if(int(data) == 8):
        return b'8'
    if(int(data) == 9):
        return b'9'
    

raspberry_usart(1) # 执行函数
