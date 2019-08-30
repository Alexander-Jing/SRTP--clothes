import tensorflow as tf 
from tensorflow import keras
import numpy as np
import matplotlib 
from matplotlib import pyplot as plt 
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense , Activation
from tensorflow.keras import optimizers
from tensorflow.keras import losses
import pandas as pd

#help(Sequential)
#help(Dense)
times = 35  #设置多次迭代值为100

class data_init(object):
    def __init__(self,data_path):
        self.data_path = data_path
        self.data_obtain()
    def data_obtain(self):
        self.data = pd.read_csv(self.data_path ,usecols = ['cloth_temp','cloth_humi','envir_temp']).as_matrix()
        self.labels = pd.read_csv(self.data_path , usecols = ['rea_time']).as_matrix()

"""设置层数layers，其中第一层Dense要求设置输入变量,最后一层units设置输出单元 """
model = Sequential([    #由于这里的数据并不是满足完全的线性关系，这里我们设置多层神经网络
    Dense(32, input_shape = (3,)),  #输入数据只有3个variables，其实要增多
    Activation("relu"),
    Dense(64),
    Activation("relu"),
    Dense(128),
    Activation("relu"),
    Dense(256),
    Activation("relu"),
    Dense(128),
    Activation("relu"),
    Dense(64),
    Activation("relu"),
    Dense(32),
    Activation("relu"),
    Dense(1),   #这里的1就是输出单元,这里全用ReLu
    Activation("relu")
])
"""设置编译，用来调整优化器，损失函数，metrics是用来评估的，其中accuracy是用来计算准确率的（具体见https://www.cnblogs.com/princecoding/p/6714216.html）"""
adam = keras.optimizers.Adam(lr = 0.001, beta_1 = 0.90,beta_2 = 0.99, epsilon = None, decay = 0.0)
sgd = keras.optimizers.SGD(lr=0.01 ,momentum=0.0, decay=0.0, nesterov=False)  #配置optimizer
# For a mean squared error regression problem
model.compile(optimizer = adam,
              loss = 'mse')  #配置损失函数



"""训练设置，这里要用到fit函数，训练数据用numpy array表示"""
data_train = data_init("E:\\MachineLearning\\keras\\data_train_all_1.csv")
data = data_train.data
labels = data_train.labels  #获取数据集，标签集

for i in range(times):  #按照epoch进行配置训练
    print(i)
    loss = model.fit(data, labels, epochs = 20, batch_size = 80)   #配置训练

'''
pre = model.predict_on_batch(data)
print(pre)
'''
test_cost = model.evaluate(data , labels)  #用原来的数据集进行test
print("costs = " , test_cost)  #打印test误差

print(" save model to 'savepath' ")
savepath = "E:\\MachineLearning\\keras\\cloth_model_1.h5"
model.save(savepath)
