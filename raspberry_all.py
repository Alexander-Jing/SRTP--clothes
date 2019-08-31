import time
import serial
from serial import Serial
import string
import tensorflow.keras
from tensorflow.keras.models import load_model
import numpy as np 
import h5py
import pandas as pd
import cv2
import numpy as np
import os
import requests
import matplotlib.pyplot as plt


# 这是树莓派的串口测试程序
# 配置串口 115200波特率 8位字长 没有校验位 1位停止位 （与接下来要用的 stm32 一致）
ser = serial.Serial("com19", baudrate = 115200, bytesize = 8, parity = 'N', stopbits = 1, timeout = 0.5) #"/dev/ttyUSB0"
"""
# 显示一下看看配置
print(ser.bytesize)
print(ser.parity)
print(ser.stopbits)
"""
savepath = "E:\\MachineLearning\\keras\\cloth_model_1.h5" # 导入模型，到时自己改下路径
model_load = load_model(savepath)

face_cascade = cv2.CascadeClassifier("E://MachineLearning//keras//haarcascade_frontalface_default.xml")
#cap = cv2.VideoCapture(0)  # 创建一个 VideoCapture 对象
camera_number = 1
cap = cv2.VideoCapture( camera_number + cv2.CAP_DSHOW)
# this picks the LARGEST image possible
cap.set( cv2.CAP_PROP_FRAME_HEIGHT, 10000 )
cap.set( cv2.CAP_PROP_FRAME_WIDTH, 10000 )
#path = os.getcwd()+'//img'
path = 'E://srtp//photo//python' + '//img'
#url = 'http://127.0.0.1/doFile/doFile.php'
#url = 'http://120.79.141.140'
url = 'http://47.93.246.19/doFile/doFile.php'

cap.set(3, 1280)
cap.set(4, 720)

flag = 1  # 设置一个标志，用来输出视频信息



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
    

#raspberry_usart(1) # 执行函数
def camera(turn,mode):  #我把摄像头读取图像并且处理加发送集成到一个函数里面去了
	if turn == 1:
		while(cap.isOpened()):  # 循环读取每一帧
			ret_flag, Vshow = cap.read()
			print(path)
			if mode == 1:
				Vshow = face_detection(Vshow)
			else :
				Vshow = image_profile(Vshow)
			cv2.imwrite(path+'//person.jpg', Vshow) # 图像被处理之后再发送
			k = cv2.waitKey(30) & 0xFF  # 每帧数据延时 1ms，延时不能为 0，否则读取的结果会是静态帧
			files = {'file123': ('person.jpg', open('E://srtp//photo//python//img//person.jpg', 'rb'))
        	  	}  # 显式的设置文件名
			# post携带的数据
			# data = {'a': '杨', 'b': 'hello'}
			r = requests.post(url, files=files)
			print(r.text)
		cap.release()  # 释放摄像头 
		cv2.destroyAllWindows()  # 删除建立的全部窗口
	else :
		cap.release()
		cv2.destroyAllWindows()

#这个是图像边缘检测的函数
def image_profile(image):
    gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)   #要二值化图像，要先进行灰度化处理
    ret, binary = cv2.threshold(gray,10,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    contours , hierarchy = cv2.findContours(binary , cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #i = max_choose(contours)
    #for i in range(0,len(contours)): 
    #i = max_choose(contours)
    x, y, w, h = cv2.boundingRect(max_choose_1(contours,2))  # max_choose_1(contours)
    cv2.rectangle(image, (x,y), (x+w,y+h), (153,153,0), 5) 
    return image
    '''
    draw_img = cv2.drawContours(binary,contours,-1,(100,200,100),3)
    return draw_img
    '''

#这个是一个提取最大边缘的函数
def max_choose(contours):
    max_contours = 0
    max_contours_index = 0
    for i in range(len(contours)):
        contours_test = len( contours[i] )
        if (contours_test > max_contours):
            max_contours = contours_test
            max_contours_index = i 
        
    return max_contours_index
#这是一个边缘排序并且提取较大边缘的排序
def max_choose_1(contours,rank):
    for i in range(len(contours)):
        for j in range(len(contours) - i -1):
            if(len(contours[j]) > len(contours[j + 1])):
                t = contours[j]
                contours[j] = contours[j + 1]
                contours[j + 1] = t
    return contours[len(contours)-rank]    
#这是一个用来导入官方人脸识别xml文件并且用来人脸识别的函数
def face_detection(image):
    grey = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY) 
    faces = face_cascade.detectMultiScale(grey,scaleFactor = 1.15,minNeighbors = 5,minSize = (5,5))
    for(x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+w),(153,153,0),5)
        #cv2.circle(image,((x+x+w)/2,(y+y+h)/2),w/2,(0,255,0),2)    cv2.cv.CV_HAAR_SCALE_IMAGE
    return image


#raspberry_usart(1)
'''
camera(1,1)
'''
#这是一个同时执行摄像头和串口的函数
def raspberry_usart_1(turn,mode):
    while (turn):
        # 获得接收缓冲区字符
        if(cap.isOpened()):  # 循环读取每一帧 
            ret_flag , Vshow = cap.read()
            #print(path)
            if mode == 1:
                Vshow = face_detection(Vshow)
            else :
                Vshow = image_profile(Vshow)
            
            cv2.imwrite(path+'//person.jpg', Vshow)
            #k = cv2.waitKey(30) & 0xFF
            files = {'file123': ('person.jpg', open('E://srtp//photo//python//img//person.jpg', 'rb'))
        	  	}  # 显式的设置文件名
            r = requests.post(url , files = files)
            print(r.text)
            '''
            #cv2.imshow("Vshow" , Vshow)
            plt.imshow(Vshow)
            plt.show()
            '''
        
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
            if pre < 40:
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

raspberry_usart_1(1,1)
