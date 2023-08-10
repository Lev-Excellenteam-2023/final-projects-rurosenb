import fnmatch
import os
import uuid
import json
import time
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory, abort, render_template

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

UPLOADS_FOLDER = os.getenv('UPLOADS_FOLDER_PATH')

OUTPUTS_FOLDER = os.getenv('OUTPUTS_FOLDER_PATH')

# Set the template folder when creating the Flask app instance
app = Flask(__name__, template_folder='C:\\targilim\\Excellenteam_python_Project\\final-projects-rurosenb\\TEMPLATES')

@app.route('/')
def index():
    return render_template('upload_form.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    uid = str(uuid.uuid4())
    timestamp = int(time.time())
    filename = f"{file.filename}_{timestamp}_{uid}"
    file_path = os.path.join(UPLOADS_FOLDER, filename)
    file.save(file_path)

    return jsonify({'uid': uid})


@app.route('/status/<uid>', methods=['GET'])
def status(uid):
    file_pattern = f"*_{uid}"
    matching_files = [f for f in os.listdir(UPLOADS_FOLDER) if fnmatch.fnmatch(f, file_pattern)]
    print("Matching files in uploads:", matching_files)

    if not matching_files:
        # If not found in uploads, check in outputs
        matching_files = [f for f in os.listdir(OUTPUTS_FOLDER) if fnmatch.fnmatch(f, file_pattern)]
        print("Matching files in uploads:", matching_files)
        if not matching_files:
            return jsonify({'status': 'not found'}), 404

    uploaded_file = matching_files[0]
    print("uploaded_file ", uploaded_file)
    status_data = {'uid': uid}
    print(status_data['uid'])
    #filename, timestamp, _ = uploaded_file.rsplit('_', 2)  # Split the string into parts
    filename, timestamp, _ = uploaded_file.split('_')
    status_data['filename'] = filename
    print(status_data['filename'])
    status_data['timestamp'] = int(timestamp)
    print(status_data['timestamp'])


    output_file = f"{filename}_{timestamp}_{uid}"
    output_path = os.path.join(OUTPUTS_FOLDER, output_file)
    print(output_path)

    if os.path.exists(output_path):
        with open(output_path, 'r') as f:
            output_content = json.load(f)
            status_data['status'] = 'done'
            status_data['explanation'] = output_content[0]
    else:
        status_data['status'] = 'pending'
        status_data['explanation'] = None

    return jsonify(status_data)


if __name__ == "__main__":
    if not os.path.exists(UPLOADS_FOLDER):
        os.makedirs(UPLOADS_FOLDER)

    if not os.path.exists(OUTPUTS_FOLDER):
        os.makedirs(OUTPUTS_FOLDER)

    app.run(debug=True)
