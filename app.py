from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
import time
import random
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed video extensions
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Simulate animal detection
def simulate_detection():
    animals = ['cattle', 'sheep', 'goats', 'pigs', 'chickens']
    detections = []
    
    # Random number of animals detected (1-5)
    num_animals = random.randint(1, 5)
    
    for _ in range(num_animals):
        animal = random.choice(animals)
        detection = {
            'type': 'animal',
            'species': animal,
            'confidence': round(random.uniform(0.7, 0.95), 2),
            'x': random.randint(10, 90),
            'y': random.randint(20, 80),
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
        detections.append(detection)
    
    # Random human detection (30% chance)
    if random.random() < 0.3:
        human_detection = {
            'type': 'human',
            'species': 'human',
            'confidence': round(random.uniform(0.8, 0.98), 2),
            'x': random.randint(10, 90),
            'y': random.randint(20, 80),
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
        detections.append(human_detection)
    
    return detections

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    
    file = request.files['video']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Simulate processing time
        time.sleep(2)
        
        return jsonify({
            'success': True,
            'filename': filename,
            'message': 'Video uploaded and ready for analysis'
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/analyze')
def analyze():
    detections = simulate_detection()
    
    # Count animals by species
    animal_counts = {
        'cattle': 0,
        'sheep': 0,
        'goats': 0,
        'pigs': 0,
        'chickens': 0
    }
    
    human_detected = False
    
    for detection in detections:
        if detection['type'] == 'animal':
            animal_counts[detection['species']] += 1
        elif detection['type'] == 'human':
            human_detected = True
    
    total_animals = sum(animal_counts.values())
    
    return jsonify({
        'detections': detections,
        'animal_counts': animal_counts,
        'total_animals': total_animals,
        'human_detected': human_detected
    })

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)