from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from io import BytesIO
import base64
from PIL import Image

# Flask app setup
app = Flask(__name__)

# Load your trained model
model = load_model('mask_detection_best.h5')

# Haarcascade for face detection
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the base64 image data from the request
    data = request.get_json()
    image_data = data['image']

    # Decode the base64 string to get the image
    img_data = base64.b64decode(image_data.split(',')[1])
    image = Image.open(BytesIO(img_data))
    image = np.array(image)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    label = "No Mask"
    # Check if faces are detected and apply the model
    for (x, y, w, h) in faces:
        face = image[y:y+h, x:x+w]
        face = cv2.resize(face, (224, 224))
        face = face / 255.0
        face = np.expand_dims(face, axis=0)

        # Make prediction
        prediction = model.predict(face)
        if prediction[0][0] > 0.5:
            label = "Mask"
        else:
            label = "No Mask"

    # Return prediction as JSON
    return jsonify({'label': label})

if __name__ == "__main__":
    app.run(debug=True)
