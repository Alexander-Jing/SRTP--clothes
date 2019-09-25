import serial
import serial.tools.list_ports


#测试调试输出开关,正式发布需调整为False
mytest = True
#mytest = False

'''
** Descriptions:       获取串口
** Parameters:        void 无
** Returned value:    list - port_serial串口列表
** Created By:        yanerfree
** Created on:        2018年9月25日
** Remarks:
'''
def getPort():
    port_serial=[]#返回串口列表
    port_list = list(serial.tools.list_ports.comports())  

    if len(port_list) <= 0:  
        print("The Serial port can't find!")      
    else:  
        #if(mytest):print("port_list: ",port_list)
        for port in port_list:
            #if(mytest):print("port: ",port)
            port_serial.append(str(port).split(' ')[0])
           # if(mytest):print("port_serial: ",port_serial)
            
    return(port_serial)   

'''
** Descriptions:      发送串口数据
** Parameters:        
** Returned value:    
** Created By:        yanerfree
** Created on:        2018年10月16日
** Remarks:以二进制读取
'''  
def send_data(serial_port="COM6", baudrate=115200, bytesize=8,
              parity=serial.PARITY_NONE,stopbit=1,
              timeout=5, filename="F:\test.txt"):
    serial_port_1 = serial_port
    baudrate_1 = int(baudrate)
    bytesize_1 = int(bytesize)
    parity_1 = parity[:1]
    stopbit_1 = int(stopbit)
    timeout_1 = timeout
    filename_1 = filename
    print(serial_port_1,baudrate_1,bytesize_1,parity_1,stopbit_1,timeout_1,filename_1)
    try:
        print("初始化串口")
#         ser_port = serial.Serial("COM6",115200,timeout=1.5,parity=serial.PARITY_NONE,
#                     stopbits=serial.STOPBITS_ONE,
#                     bytesize=serial.EIGHTBITS)
        ser_port = serial.Serial(serial_port_1, baudrate_1,bytesize_1,parity_1,stopbit_1, timeout_1)
        print("串口是否打开：",ser_port.isOpen())
        if not ser_port.isOpen():
            ser_port.open()
        print("串口是否打开：",ser_port.isOpen())
        
        f = open(filename_1,'rb')#打开或者新建一个文件
        i=0
        while 1:
            i = i + 1
            print("读取文 件第  %d 行"%i)
            #fileData=f.readline().strip('\n').encode(encoding='utf_8')#编码转换成字节发送
            fileData=f.readline().strip(b'\n')
            fileData=fileData.strip(b'\r')
            if fileData==b'':
                break
            #fileData_1=(fileData+'SDSA\r\n'.encode(encoding='utf_8'))
            fileData_1=(fileData+b'SDSA\r\n')
            print("发送数据为:",fileData_1)
            ser_port.write(fileData_1)
            #print("fileData[-11:]",fileData[-11:])
            if fileData[-11:]==b'***[END]***':
            #if fileData[-11:]=='***[END]***':
                print("检测到文件结束符，退出")
                break
            print("等待2s")
            time.sleep(2)
    except Exception:
        print("发送脚本失败")
    finally:
        f.close()
        ser_port.close()      

 
'''
** Descriptions:      获取串口数据
** Parameters:        
** Returned value:    
** Created By:        yanerfree
** Created on:        2018年10月17日
** Remarks:二进制保存
'''      
def receive_data(serial_port="COM6", baudrate=115200, bytesize=8,
                 parity=serial.PARITY_NONE,stopbit=1,
                 timeout=5,filename="F:\test.txt"):
    serial_port_1 = serial_port
    baudrate_1 = int(baudrate)
    bytesize_1 = int(bytesize)
    parity_1 = parity[:1]
    stopbit_1 = int(stopbit)
    timeout_1 = timeout
    filename_1 = filename
    print(serial_port_1,baudrate_1,bytesize_1,parity_1,stopbit_1,timeout_1,filename_1)
    try:
        print("初始化串口")
        #ser_port = serial.Serial(serial_port, baudrate,bytesize,parity,stopbit, timeout)
        ser_port = serial.Serial(serial_port_1, baudrate_1,bytesize_1,parity_1,stopbit_1, timeout_1)
        print("串口是否打开：",ser_port.isOpen())
        if not ser_port.isOpen():
            ser_port.open()
        print("串口是否打开：",ser_port.isOpen())
        
        #f = open(filename_1,'w',encoding='utf-8')#打开或者新建一个文件
        f = open(filename_1,'wb')#以二进制打开或创建一个文件
       
        while True:
            fileData=ser_port.readline()
            if(len(fileData)==0 or fileData[-6:]!=b'SDSA\r\n'):
                continue
            print("接收到的数据:",fileData)
            fileData1=fileData.split(b'SDSA\r\n')[0]
            fileData2=fileData1+b'\n'#'0X0D'
            filedata_str=fileData1.decode(encoding='utf_8')
            content = filedata_str + '\n'
            print("保存的数据为:",fileData2)
            #saveFile(filename_1,fileData1)
            f.write(fileData2)
            if filedata_str[-11:]=='***[END]***':
                break
            sleep(1)
    except Exception:
        print("获取脚本失败")
    finally:
        f.close()
        ser_port.close()
        if mytest: print("串口是否打开：",ser_port.isOpen())