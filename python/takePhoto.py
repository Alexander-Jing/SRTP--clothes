#coding:utf-8
import cv2
import numpy as np
import os
import requests
import time

cap = cv2.VideoCapture(0)  # 创建一个 VideoCapture 对象
path = os.getcwd()+'/img'
url = 'http://127.0.0.1/doFile/doFile.php'

cap.set(3, 1280)
cap.set(4, 720)

flag = 1  # 设置一个标志，用来输出视频信息

while(cap.isOpened()):  # 循环读取每一帧
	ret_flag, Vshow = cap.read()
	print(path)
	cv2.imwrite(path+'/person.jpg', Vshow)
	k = cv2.waitKey(30) & 0xFF  # 每帧数据延时 1ms，延时不能为 0，否则读取的结果会是静态帧
	files = {'file123': ('person.jpg', open('/home/sun/Work/Python/photo/img/person.jpg', 'rb'))
          }  # 显式的设置文件名
	# post携带的数据
	# data = {'a': '杨', 'b': 'hello'}
	r = requests.post(url, files=files)
	print(r.text)
cap.release()  # 释放摄像头
cv2.destroyAllWindows()  # 删除建立的全部窗口
