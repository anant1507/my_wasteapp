import os
import logging
from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
from waste_classifier import classify_waste

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_key")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    # Read image file
    img_array = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    if img is None:
        return jsonify({'error': 'Invalid image'}), 400

    # Classify the waste
    classification, confidence = classify_waste(img)
    
    # Return classification result
    return jsonify({
        'classification': classification,
        'confidence': confidence,
        'bin_color': {
            'biodegradable': '#2ECC71',
            'non-biodegradable': '#3498DB',
            'chemical': '#2C3E50'
        }.get(classification, '#333333')
    })
