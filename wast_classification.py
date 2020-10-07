# -*- coding: utf-8 -*-
"""Wast Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yo1voKeas9_2irHNQGAGIpvd78EZ4DBs
"""

from google.colab import files

# importing Json File From Local Computer
files.upload()

# Create Directory Name Kaggle 
! mkdir ~/.kaggle

# Make Directory
! mkdir ~/.kaggle

# Copy Contents Of json into Directory
! cp kaggle.json ~/.kaggle/

# Asking Permission For Read And Write
! chmod 600 ~/.kaggle/kaggle.json

# Dataset Url
! kaggle datasets download -d techsash/waste-classification-data

"""Now Make Directory Name Data and Unzip Images in it"""

! mkdir Data

# After Successfully Downloading Dataset Now Extracting Dataset
! unzip /content/waste-classification-data.zip -d Data

# Commented out IPython magic to ensure Python compatibility.
# Now Importing Main Libraries here
import cv2
import matplotlib.pyplot as plt
# %matplotlib inline
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D,Dense,Activation,Dropout,MaxPooling2D,Flatten
from tensorflow.keras.preprocessing import image
import numpy as np

# Let see What Organi
Organin_img=cv2.imread("/content/Data/DATASET/TRAIN/O/O_10000.jpg")

plt.imshow(Organin_img)

Organin_img.shape

# Converting in RBG Format
Organin_img=cv2.cvtColor(Organin_img,cv2.COLOR_BGR2RGB)

plt.imshow(Organin_img)

Recycle_img=cv2.imread("/content/Data/DATASET/TRAIN/R/R_1007.jpg")

plt.imshow(Recycle_img)

Recycle_img=cv2.cvtColor(Recycle_img,cv2.COLOR_BGR2RGB)

Recycle_img.shape

# Data Augmentation
from keras.preprocessing.image import ImageDataGenerator
image_gen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')

# Showing Image wheather data augmented not
plt.imshow(image_gen.random_transform(Recycle_img))
print('Done')

# Give Data to image generator for augmentation
image_gen.flow_from_directory("/content/Data/DATASET/TRAIN")
image_gen.flow_from_directory("/content/Data/DATASET/TEST")

input_shape=(150,150,3)

model=Sequential()
# conv Block 1
model.add(Conv2D(filters=32,kernel_size=(3,3),input_shape=input_shape,activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

# conv Block 2
model.add(Conv2D(filters=64,kernel_size=(3,3),input_shape=input_shape,activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

# conv Block 3
model.add(Conv2D(filters=128,kernel_size=(3,3),input_shape=input_shape,activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))

# Flatten Layer
model.add(Flatten())

# Dense for Connection
model.add(Dense(256))
model.add(Activation('relu'))

# DropOut Layer for avoiding overfitting

model.add(Dropout(0.5))
# Dense Layer for output
model.add(Dense(1))
# Activation for Output
model.add(Activation('sigmoid'))

model.compile(optimizer='adam',loss='binary_crossentropy',metrics=['accuracy'])

# Seeing Model Summary
model.summary()

input_shape[:2]

batch_size=32

# Now analyzing Data and Augmented with image data generator
train_gen=image_gen.flow_from_directory('/content/Data/DATASET/TRAIN',
                                        target_size=input_shape[:2],
                                        batch_size=batch_size,
                                        class_mode='binary')
test_gen=image_gen.flow_from_directory('/content/Data/DATASET/TEST',
                                        target_size=input_shape[:2],
                                        batch_size=batch_size,
                                        class_mode='binary')

train_gen.class_indices

# Now Fit Model
results=model.fit_generator(train_gen,epochs=5,steps_per_epoch=100,validation_data=test_gen,validation_steps=12)

type(results)

print(results.history['accuracy'])

print(results.history['loss'])

plt.plot(results.history['accuracy'])
plt.plot(results.history['loss'])
plt.title('Model Performance')
plt.ylabel('Accuracy')
plt.xlabel('Loss')
plt.legend(['Accuracy','Loss'],loc=('upper left'))
plt.show()

plt.plot(results.history['accuracy'])
plt.plot(results.history['val_accuracy'])
plt.title('Model Performance')
plt.ylabel('Accuracy')
plt.xlabel('Loss')
plt.legend(['Accuracy','val_accuracy'],loc=('upper left'))
plt.show()

# Pick Random Image From Train/O Folder 
Organic=image.load_img('/content/Data/DATASET/TRAIN/R/R_1761.jpg',target_size=(150,150,3))
Organic=image.img_to_array(Organic)
print(Organic.shape)
Organic=np.expand_dims(Organic,axis=0)
print(Organic.shape)
Organic=Organic/255

Pred_O=model.predict(Organic)

# Pick Random Image From Train/R Folder 
Recycle=image.load_img('/content/Data/DATASET/TRAIN/R/R_1524.jpg',target_size=(150,150,3))
Recycle=image.img_to_array(Recycle)
print(Recycle.shape)
Recycle=np.expand_dims(Recycle,axis=0)
print(Recycle.shape)
Recycle=Recycle/255

Pred_R=model.predict(Recycle)

print(f'chances of Organic Image according to model is:{Pred_O}')
print(f'chances of Recyclable Image according to model is:{Pred_R}')

result=model.predict_classes(Organic)
print(result)
if result[0][0]==1:
  prediction='Recyclabe Image'
else:
  prediction='Organic Image'

print(prediction)

result=model.predict_classes(Recycle)
print(result)
if result[0][0]==1:
  prediction='Recyclabe Image'
else:
  prediction='Organic Image'

print(prediction)

model.save_weights('Waste_Classification.h5')

