import requests
import time
url = 'http://127.0.0.1/doFile/doFile.php'
#url = 'http://www.test.com/doPost.php'
#files = {'file': open('D:/tmp/1.jpg', 'rb')}

while (1):
	# 要上传的文件
	files = {'file123': ('person.jpg', open('/home/sun/Work/Python/photo/img/person.jpg', 'rb'))
		}  # 显式的设置文件名
	# post携带的数据
	data = {'a': '杨', 'b': 'hello'}
	r = requests.post(url, files=files, data=data)
	print(r.text)
	time.sleep(0.05)
