from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
import os
from PIL import Image
import torch
from transformers import OwlViTProcessor, OwlViTForObjectDetection
import cv2
import numpy as np
import requests
from io import BytesIO

# Initialize the Flask application
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the model and processor
processor = OwlViTProcessor.from_pretrained("google/owlvit-base-patch16")
model = OwlViTForObjectDetection.from_pretrained("google/owlvit-base-patch16")

def detect_objects(image_path, keywords, confidence_threshold):
    # Open the image file
    image = Image.open(image_path)
    texts = [keywords]
    
    # Process the image and keywords
    inputs = processor(text=texts, images=image, return_tensors="pt")
    outputs = model(**inputs)

    # Post-process the outputs
    target_sizes = torch.Tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs=outputs, threshold=confidence_threshold, target_sizes=target_sizes)

    detections = []
    i = 0
    text = texts[i]
    boxes, scores, labels = results[i]["boxes"], results[i]["scores"], results[i]["labels"]

    # Collect detection results
    for box, score, label in zip(boxes, scores, labels):
        box = [round(i, 2) for i in box.tolist()]
        detection = {
            "label": text[label],
            "confidence": round(score.item(), 3),
            "box": box
        }
        detections.append(detection)
        print(f"Detected {text[label]} with confidence {round(score.item(), 3)} at location {box}")

    # Draw bounding boxes on the image
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    for box in boxes:
        start_point = (int(box[0]), int(box[1]))
        end_point = (int(box[2]), int(box[3]))
        color = (255, 0, 0)
        thickness = 2
        img = cv2.rectangle(img, start_point, end_point, color, thickness)

    # Save the result image
    result_image_path = os.path.join(UPLOAD_FOLDER, 'result.png')
    cv2.imwrite(result_image_path, cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return 'result.png', detections

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    image_url = None
    detections = []
    if request.method == 'POST':
        keywords = request.form.get('keywords', '').split(',')
        confidence_threshold = float(request.form.get('confidence_threshold', 0.05))
        
        # Handle file upload
        if 'file' in request.files and request.files['file'].filename != '':
            file = request.files['file']
            if file:
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
                file.save(filepath)
                result_image, detections = detect_objects(filepath, keywords, confidence_threshold)
                return render_template('index.html', image_url=url_for('uploaded_file', filename=result_image), detections=detections)
        
        # Handle image URL input
        elif 'imageUrl' in request.form and request.form['imageUrl'] != '':
            image_url = request.form['imageUrl']
            try:
                response = requests.get(image_url)
                if response.status_code == 200:
                    filename = secure_filename(image_url.split('/')[-1])
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    with open(filepath, 'wb') as f:
                        f.write(response.content)
                    result_image, detections = detect_objects(filepath, keywords, confidence_threshold)
                    return render_template('index.html', image_url=url_for('uploaded_file', filename=result_image), detections=detections)
            except requests.RequestException as e:
                print(f"Error fetching image: {e}")
                return redirect(request.url)

    return render_template('index.html', detections=detections)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
