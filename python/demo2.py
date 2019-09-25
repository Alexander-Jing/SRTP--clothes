import cv2
import sys
import os
import time

# 定义图片保存位置
# path = os.getcwd() 

path = os.getcwd()
cap = cv2.VideoCapture(0)

def getPicture():

	ret, frame = cap.read()
	cv2.imwrite(path+'/person.jpg', frame)
	# 关闭摄像头
	# cap.release()

while (1):
	getPicture()

