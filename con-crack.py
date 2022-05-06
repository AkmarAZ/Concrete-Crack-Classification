# -*- coding: utf-8 -*-
"""
Created on Fri May  6 22:18:56 2022

@author: User
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image

negative_images = os.listdir('/concrete_data/train/negative')
positive_images = os.listdir('/concrete_data/train/positive')

import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense
from keras.applications import ResNet50
from keras.applications.resnet50 import preprocess_input
num_classes = 2
image_resize = 224
batch_size_training = 100
batch_size_validation = 100
data_generator = ImageDataGenerator(
    preprocessing_function=preprocess_input,
)
train_generator = data_generator.flow_from_directory(
    'concrete_data/train',
    target_size=(image_resize, image_resize),
    batch_size=batch_size_training,
    class_mode='categorical')
    
validation_generator = data_generator.flow_from_directory(
    'concrete_data/valid',
    target_size=(image_resize, image_resize),
    batch_size=batch_size_validation,
    class_mode='categorical')

model = Sequential()
model.add(ResNet50(
    include_top=False,
    pooling='avg',
    weights='imagenet',
    ))
    
model.add(Dense(num_classes, activation='softmax'))
model.layers[0].trainable = False
model.summary()

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

steps_per_epoch_training = len(train_generator)
steps_per_epoch_validation = len(validation_generator)
num_epochs = 2

fit_history = model.fit_generator(
    train_generator,
    steps_per_epoch=steps_per_epoch_training,
    epochs=num_epochs,
    validation_data=validation_generator,
    validation_steps=steps_per_epoch_validation,
    verbose=1,
)

