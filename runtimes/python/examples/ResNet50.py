import json
import mimetypes
import numpy as np
import os
import requests
import shutil
import tempfile

from contextlib import contextmanager
from inaccel.keras.applications.resnet50 import decode_predictions, ResNet50
from inaccel.keras.preprocessing.image import load_img
from werkzeug.exceptions import BadRequest

@contextmanager
def fetch_img(img_url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0'}
    img = requests.get(img_url, headers=headers, stream=True)

    content, _type = img.headers['Content-Type'].split('/')
    if content == 'image':
        ext = mimetypes.guess_extension(img.headers['Content-Type'])
        if not ext:
            ext = _type
    else:
        raise requests.exceptions.InvalidURL("Given URL is not of Content-Type image")

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as img_file:
            shutil.copyfileobj(img.raw, img_file)
        yield img_file.name
    except (FileNotFoundError, FileExistsError, PermissionError, BaseException):
        raise
    else:
        os.remove(img_file.name)

def preprocess_input(img_url):
    with fetch_img(img_url) as img_file:
        return np.expand_dims((load_img(img_file, target_size=(224, 224))), axis=0)

def predict(request):
    try:
        data = request.get_json(force=True)

        if data:
            model = ResNet50(weights='imagenet')

            images = np.vstack(list(map(preprocess_input, data)))

            preds = model.predict(images)

            return str(decode_predictions(preds, top=1))
        else:
            return ""
    except BadRequest:
        return "No valid input JSON data!"
