import cv2
import json
import numpy as np

from inaccel.keras.applications.resnet50 import decode_predictions, ResNet50
from skimage import io

def preprocess_input(data):
    return np.expand_dims(cv2.resize(io.imread(data)[..., ::-1], (224, 224)), axis=0)

def predict(event, context):
    model = ResNet50(weights='imagenet')

    images = np.vstack(list(map(preprocess_input, json.loads(event['data']))))

    preds = model.predict(images)

    return str(decode_predictions(preds, top=1))
