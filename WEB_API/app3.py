import fnmatch
import os
import uuid
import json
import time
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask, request, jsonify, send_from_directory, abort, render_template
from DB.database import User, Upload  # Import the User and Upload classes from your database module

load_dotenv()

UPLOADS_FOLDER = os.getenv('UPLOADS_FOLDER_PATH')
OUTPUTS_FOLDER = os.getenv('OUTPUTS_FOLDER_PATH')

DB_PATH = os.path.join(os.getenv('DB_FOLDER_PATH'), "gpt_explainer.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=True)
Session = sessionmaker(bind=engine)

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

    email = request.form.get('email')
    session = Session()

    user = None
    if email:
        user = session.query(User).filter_by(email=email).first()
        if not user:
            user = User(email=email)
            session.add(user)

    upload = Upload(uid=uid, filename=filename, upload_time=datetime.now(), status="pending", user=user)
    session.add(upload)
    session.commit()
    session.close()

    return jsonify({'uid': uid})
@app.route('/status/<uid>', methods=['GET'])
def status(uid):
    session = Session()
    upload = session.query(Upload).filter_by(uid=uid).first()

    if not upload:
        return jsonify({'status': 'not found'}), 404

    status_data = {
        'uid': uid,
        'filename': upload.filename,
        'timestamp': upload.upload_time.timestamp(),
    }

    output_file = f"{upload.filename}_{upload.upload_time.timestamp()}_{uid}"
    output_path = os.path.join(OUTPUTS_FOLDER, output_file)

    if os.path.exists(output_path):
        with open(output_path, 'r') as f:
            output_content = json.load(f)
            status_data['status'] = 'done'
            status_data['explanation'] = output_content[0]
    else:
        status_data['status'] = 'pending'
        status_data['explanation'] = None

    session.close()
    return jsonify(status_data)

if __name__ == "__main__":
    if not os.path.exists(UPLOADS_FOLDER):
        os.makedirs(UPLOADS_FOLDER)

    if not os.path.exists(OUTPUTS_FOLDER):
        os.makedirs(OUTPUTS_FOLDER)

    app.run(debug=True)