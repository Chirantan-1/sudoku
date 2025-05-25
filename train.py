import tensorflow as tf
from tensorflow.keras import layers, models
import numpy as np
import os
import cv2

data_dir = 'C:/Users/chira_mk2ov0g/OneDrive/Documents/python/digits'
img_size = 100

x, y = [], []

for label in os.listdir(data_dir):
    label_dir = os.path.join(data_dir, label)
    if not os.path.isdir(label_dir): continue
    for filename in os.listdir(label_dir):
        path = os.path.join(label_dir, filename)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None: continue
        img = cv2.resize(img, (img_size, img_size))
        img = img / 255.0
        x.append(img)
        y.append(int(label))

x = np.array(x).reshape(-1, img_size, img_size, 1)
y = tf.keras.utils.to_categorical(y, num_classes=10)

model = models.Sequential([
    layers.Conv2D(32, (3, 3), activation='relu', input_shape=(img_size, img_size, 1)),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(64, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Conv2D(128, (3, 3), activation='relu'),
    layers.MaxPooling2D((2, 2)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax'),
])

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x, y, epochs=30, batch_size=32)

model.save("digit_model_100x100.h5")

