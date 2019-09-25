#coding:utf-8
import cv2
import numpy as np
import os
import requests
import time

camera_number = 1
face_cascade = cv2.CascadeClassifier("E://MachineLearning//keras//haarcascade_frontalface_default.xml")
#cap = cv2.VideoCapture(1)  # 创建一个 VideoCapture 对象
cap = cv2.VideoCapture( camera_number + cv2.CAP_DSHOW)
# this picks the LARGEST image possible
cap.set( cv2.CAP_PROP_FRAME_HEIGHT, 10000 )
cap.set( cv2.CAP_PROP_FRAME_WIDTH, 10000 )

#path = os.getcwd()+'//img'
path = 'E://srtp//photo//python' + '//img'
#url = 'http://127.0.0.1/doFile/doFile.php'
#url = 'http://120.79.141.140'
url = 'http://47.93.246.19/doFile/doFile.php'


#cap.set(3, 1280)
#cap.set(4, 720)
cap.set(3,320)
cap.set(4,180)

flag = 1  # 设置一个标志，用来输出视频信息
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
            k = cv2.waitKey(10) & 0xFF  # 每帧数据延时 1ms，延时不能为 0，否则读取的结果会是静态帧
            
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

camera(1,1)  #用来摄像头读取图像并且进行简单处理的函数