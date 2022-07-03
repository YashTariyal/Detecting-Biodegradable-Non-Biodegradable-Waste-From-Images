from flask import Flask, request, jsonify, render_template
import base64, json
from io import BytesIO
from model import MyModel
import numpy as np
import os
from math import floor
import json

# declare constants
HOST = 'localhost'

# initialize flask application
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Read model to keep it ready all the time

model =  MyModel('cnn2.pth', 'cpu')
#model =  MyModel('app/cnn2.pth', 'cpu')
CLASS_MAPPING = ['metal', 'plastic', 'cardboard', 'paper', 'trash', 'glass']


# Make the prediction human-readable
img_class_map = None
with open('index_to_name.json') as f:
            img_class_map = json.load(f)


def render_prediction(index):
    stridx = str(index)
    class_name = 'Unknown'
    if img_class_map is not None:
        if stridx in img_class_map is not None:
            class_name = img_class_map[stridx]

    return class_name


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/infer', methods=['GET','POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        saveLocation = f.filename
        f.save(saveLocation)
        inference, confidence = model.infer(saveLocation)
        class_name = render_prediction(inference)
        # make a percentage with 2 decimal points
        confidence = floor(confidence * 10000) / 100
        # delete file after making an inference
        os.remove(saveLocation)

        return render_template('inference.html', name=class_name, confidence=confidence)

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 8080))
    app.run(host='localhost', port=port, debug=True)