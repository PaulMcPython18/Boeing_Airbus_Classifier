'''
Airbus/Boeing Machine Learning Model powered through ResNet50

By: Paul McBurney

Last Edited: 01/12/2019

Do Not Take Without Permission
'''

from keras.applications.resnet50 import ResNet50
from keras.applications import VGG19
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
from sklearn.utils import shuffle
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras import models
from keras import layers
import matplotlib as plt
import cv2
import os
boeing_dir = 'Boeing-Image-Dir' # Insert URL of Files
airbus_dir = 'Airbus-Image-Dir'

conv_base = ResNet50(weights='imagenet', input_shape=(224, 224, 3))





model = models.Sequential()
model.add(conv_base)

model.add(layers.Dropout(0.15))
model.add(layers.GaussianNoise(0.15))
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(16, activation='relu'))
model.add(layers.Dense(2, activation='softmax'))
model.save('resnet-BA-classifier.h5')

boeing_data = []
boeing_label = []
airbus_data = []
airbus_label = []
'''iterate through each file, resize, append to variable accordingly'''
for filename in os.listdir(boeing_dir):
    if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
        path_b = os.path.join(boeing_dir, filename)
        im = cv2.imread(path_b)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB) # Convert with cv2 module to RGB format
        im = cv2.resize(im, (224, 224)) # Resizing
        boeing_data.append(im)
        boeing_label.append(0)

for filename in os.listdir(airbus_dir):
    if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
        path_b = os.path.join(airbus_dir, filename)
        im = cv2.imread(path_b)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
        im = cv2.resize(im, (224, 224))
        airbus_data.append(im)
        airbus_label.append(1)




training_data = boeing_data + airbus_data #Concadenate Boeing and Airbus data
training_label = boeing_label + airbus_label

training_data = np.array(training_data)
training_label = np.asarray(training_label) # Turn Data into numpy arrays
training_data, training_label = shuffle(training_data, training_label) # Shuffle

print(training_data.shape)
print(training_label)
model.compile(loss='sparse_categorical_crossentropy', optimizer='sgd', metrics=['accuracy']) # Compile (Use sparse_categorical_crossentropy when you have two classes, otherwise use categorical_crossentropy)
print(model.summary())
model.fit(training_data, training_label, epochs=10, batch_size=20, validation_split=0.1, verbose=1) # Train
print('finished training')
