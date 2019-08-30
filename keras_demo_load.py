import tensorflow.keras
from tensorflow.keras.models import load_model
import numpy as np 
import h5py
import pandas as pd

savepath = "E:\\MachineLearning\\keras\\cloth_model.h5"
data_path = "E:\\MachineLearning\\keras\\data_train_all.csv"

print("load trained models to use...")
model_load = load_model(savepath)

data = pd.read_csv(data_path ,usecols = ['cloth_temp','cloth_humi','envir_temp']).as_matrix()
labels = pd.read_csv(data_path , usecols = ['time']).as_matrix()

pre = model_load.predict(data)
print(pre)
cost = model_load.evaluate(data , labels)
print("loss : " , cost)

