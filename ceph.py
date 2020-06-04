# -*- coding: utf-8 -*-
"""orjinalresim_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-v6TTjJYyTdEw4aVVGBHTqd44IA1cMrm
"""

from google.colab import drive 
drive.mount('/content/gdrive',force_remount=True)

!ls "/content/gdrive/My Drive/ceph/"

!pip install -U -q PyDrive
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials
# Authenticate and create the PyDrive client.
auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

link='' #link of the csv file
fluff, id = link.split('=')
print (id)

import keras
from keras.models import Sequential
from keras.layers import Input,Dense, Dropout, Flatten,Activation,GlobalMaxPooling2D
from keras.layers import Conv2D, MaxPooling2D,ZeroPadding2D,BatchNormalization,Convolution2D
from keras.utils import to_categorical
from keras.preprocessing import image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tqdm import tqdm
from keras.preprocessing.image import ImageDataGenerator
from keras_preprocessing.image import ImageDataGenerator,load_img,img_to_array

from keras.optimizers import SGD,Adam
import numpy as np
from keras import layers
from keras.layers import Input, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D
from keras.layers import AveragePooling2D, MaxPooling2D, Dropout, GlobalMaxPooling2D, GlobalAveragePooling2D
from keras.models import Model
from keras.preprocessing import image
from keras.utils import layer_utils
from keras.utils.data_utils import get_file
from keras.applications.imagenet_utils import preprocess_input
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot
from keras.utils import plot_model
from keras.layers.convolutional import Conv2D,MaxPooling2D
import keras.backend as K
K.set_image_data_format('channels_last')
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow

downloaded = drive.CreateFile({'id':id}) 
downloaded.GetContentFile('Filename.csv')

# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline


train = pd.read_csv('Filename.csv')
train.head(25) 
print(train.columns) 
print(train.dtypes) 
print(train.shape) 

train_image = []
for i in tqdm(range(train.shape[0])):
    img = image.load_img('' + train['Id'][i]+'.bmp',target_size=(400,400)) # file path of dataset
    img = image.img_to_array(img)
    img = img/255
    train_image.append(img)
X = np.array(train_image)

print(X.shape)
plt.imshow(X[330])
train['Class'][330]

y=np.array(train.drop(['Id','Class'],axis=1)) 
y.shape

#validation set oluşturma
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.10,shuffle=True)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

from skimage.transform import rotate
from skimage.util import random_noise
from skimage.filters import gaussian
from scipy import ndimage

# data augmentation
final_train_data = []
final_target_train = []
for i in tqdm(range(X_train.shape[0])):
    final_train_data.append(X_train[i])
    final_train_data.append(rotate(X_train[i], angle=15, mode = 'wrap'))
    final_train_data.append(rotate(X_train[i], angle=7, mode = 'wrap'))
    final_train_data.append(rotate(X_train[i], angle=-7, mode = 'wrap'))
    final_train_data.append(rotate(X_train[i], angle=-15, mode = 'wrap'))
    

    
    for j in range(5):
        final_target_train.append(y_train[i])

len(final_target_train), len(final_train_data)
final_train = np.array(final_train_data)
final_target_train = np.array(final_target_train)

fig,ax = plt.subplots(nrows=1,ncols=5,figsize=(20,20))
for i in range(5):
    ax[i].imshow(final_train[i+30])
    ax[i].axis('off')

print(final_train.shape)
print(final_target_train.shape)

plt.imshow(final_train[140])
print(final_target_train[140])

#validation set oluşturma
X_train,X_test,y_train,y_test=train_test_split(final_train,final_target_train,test_size=0.10,shuffle=True)
#X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

#from keras.constraints import maxnorm
#from keras.wrappers.scikit_learn import KerasClassifier
#from keras.constraints import maxnorm
#from keras.optimizers import SGD
#from sklearn.model_selection import cross_val_score
#from sklearn.preprocessing import LabelEncoder
#from sklearn.model_selection import StratifiedKFold
#from sklearn.preprocessing import StandardScaler
#from sklearn.pipeline import Pipeline

model = Sequential()
model.add(Conv2D(filters=16, kernel_size=(3, 3), activation="relu", input_shape=(400,400,3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(filters=32, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation="relu"))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32,activation='relu'))
model.add(Dense(16,activation='relu'))
model.add(Dense(3, activation='softmax'))

plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=True)

model.compile(Adam(lr=0.001),loss='binary_crossentropy', metrics=['accuracy'])

model.fit(final_train, final_target_train, epochs=20, validation_data=(X_test, y_test), batch_size=60)

test_img=image.load_img('/content/gdrive/My Drive/ceph/test1/367.bmp',target_size=(400,400,1)) # file path of test set 
test_img=image.img_to_array(test_img)
test_img=test_img/255
print(train.columns[2:])

classes = np.array(train.columns[2:])
proba = model.predict(test_img.reshape(1,400,400,3))
top_3 = np.argsort(proba[0])[:-4:-1]
print(proba[0][:-4:-1])
for i in range(3):
    print("{}".format(classes[top_3[i]])+" ({:.3})".format(proba[0][top_3[i]]))
plt.imshow(test_img)

