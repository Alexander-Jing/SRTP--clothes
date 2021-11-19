# SRTP - Smart clothes drying system
SRTP item clothing identification and recognition  
the code running on raspberry PI and Server  
  
including two parts
# the classification of wet and dry clothes  
running on the raspberry PI
the dataset comes from our sensors on clothes in a real environment for drying clothes  
using the traditional deep neutral networks for a classification task in order to classify the clothes  
# the clothes recognition  
using the cascade models, the first is the Yolov3 to detect the clothes, running on the raspberry PI       
the second part is to recognize the clothes, using the inception v4, which is a multi task problem, running Server      
all the codes runs correctly in accord with the other parts of the system 
