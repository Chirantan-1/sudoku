from tensorflow.keras.models import load_model
import cv2
import numpy as np

model = load_model("digit_model_100x100.h5")

def predict_digit(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (100, 100)) / 255.0
    img = img.reshape(1, 100, 100, 1)
    prediction = model.predict(img)
    return np.argmax(prediction)

print(predict_digit("img path"))

