import cv2
import matplotlib.pyplot as plt
import numpy as np
face_cascade = cv2.CascadeClassifier("E://MachineLearning//keras//haarcascade_frontalface_default.xml")

#初期化USB摄像头
def camera_use(turn,mode):
    cap = cv2.VideoCapture(1)
    if turn == 1:   
        while( cap.isOpened() ):
	        #USB摄像头工作时,读取一帧图像
            ret, frame = cap.read()
            #显示图像窗口在树莓派的屏幕上
       
            if mode == 1:
                frame1 = face_detection(frame)
            else :
                frame1 = image_profile(frame)
                #frame1 = hough_detection(frame)
            cv2.imshow('Capture',frame1)
            #plt.imshow(frame)
            #plt.show()
            #按下q键退出
        
            key = cv2.waitKey(1)
            #print( '%08X' % (key&0xFFFFFFFF) )
            if key & 0x00FF  == ord('q'):
                break
        
        #释放资源和关闭窗口
        cap.release()
        cv2.destroyAllWindows()
    else :
        #释放资源和关闭窗口
        cap.release()
        cv2.destroyAllWindows()

def image_profile(image):
    gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)   #要二值化图像，要先进行灰度化处理
    ret, binary = cv2.threshold(gray,100,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    contours , hierarchy = cv2.findContours(binary , cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #i = max_choose(contours)
    #for i in range(0,len(contours)): 
    #i = max_choose(contours)
    x, y, w, h = cv2.boundingRect(max_choose_1(contours))  # max_choose_1(contours)
    cv2.rectangle(image, (x,y), (x+w,y+h), (153,153,0), 5) 
    return image
    '''
    draw_img = cv2.drawContours(binary,contours,-1,(100,200,100),3)
    return draw_img
    '''

def max_choose(contours):
    max_contours = 0
    max_contours_index = 0
    for i in range(len(contours)):
        contours_test = len( contours[i] )
        if (contours_test > max_contours):
            max_contours = contours_test
            max_contours_index = i 
        
    return max_contours_index

def max_choose_1(contours):
    for i in range(len(contours)):
        for j in range(len(contours) - i -1):
            if(len(contours[j]) > len(contours[j + 1])):
                t = contours[j]
                contours[j] = contours[j + 1]
                contours[j + 1] = t
    return contours[len(contours)-2]    

def face_detection(image):
    grey = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY) 
    faces = face_cascade.detectMultiScale(grey,scaleFactor = 1.15,minNeighbors = 5,minSize = (5,5))
    for(x,y,w,h) in faces:
        cv2.rectangle(image,(x,y),(x+w,y+w),(153,153,0),5)
        #cv2.circle(image,((x+x+w)/2,(y+y+h)/2),w/2,(0,255,0),2)    cv2.cv.CV_HAAR_SCALE_IMAGE
    return image

def hough_detection(image):
    minLineLength = 15
    maxLineGap = 200
    image1 = cv2.GaussianBlur(image,(3,3),0)
    edges = cv2.Canny(image1, 50, 150, apertureSize = 3)
    stran_lines = cv2.HoughLinesP(edges,1,np.pi/90,80,minLineLength,maxLineGap)#minLineLength,maxLineGap
    print(stran_lines)
    for x1,y1,x2,y2 in stran_lines[0]:
        cv2.line(image,(x1,y1),(x2,y2),(0,255,0),2)
    return image



camera_use(1,1)
