from flask import Flask, render_template, request, redirect, flash
import os
from ultralytics import YOLO

app = Flask(name)
app.secret_key = 'your_secret_key'  # Set a secret key for flash messages

# Load a pretrained YOLOv8n model
model = YOLO('C:/Users/Vedavalli/OneDrive/Desktop/project/tea leaf disease/YOLOv8_Tea lef dise_Model.pt')

# Set the upload folder
UPLOAD_FOLDER = 'C:/Users/Vedavalli/OneDrive/Desktop/project/tea leaf disease/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

 
def create_upload_folder():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
 
 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    create_upload_folder()

    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(request.url)

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        file_path = filename.replace('\\', '/')

        model.predict(file_path, save_txt=True, hide_conf=True)

        txt_files = os.listdir('runs/classify/predict/labels')
        txt_files.sort(key=lambda x: os.path.getmtime(os.path.join('runs/classify/predict/labels', x)), reverse=True)

        if txt_files:
            txt_file_path = os.path.join('runs/classify/predict/labels', txt_files[0])

            # Read the content of the first line excluding the first four characters
            with open(txt_file_path, 'r') as txt_file:
                first_line = txt_file.readline()[4:].strip()

            # Adjust the output b ased on the prediction
            if first_line.lower() == 'healthy':
                result = "The tea leaf is healthy!"
            else:
                result = f'The given leaf belongs to: {first_line} Disease'

            return render_template('result.html', result=result)

    flash('No files found in the "labels" directory.', 'error') 
    return redirect(request.url) 


if name == '_main_': 
    app.run(debug=True)