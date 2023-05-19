import os
from flask import Flask, render_template, send_from_directory, jsonify, request
from flask_cors import CORS
import librosa

cwd = os.path.dirname(os.path.abspath(__file__))
gui_dir = os.path.join(cwd, '..', '..', 'gui')
if not os.path.exists(gui_dir):
    gui_dir = os.path.join(cwd, 'gui')

server = Flask(__name__, static_folder=gui_dir, template_folder=gui_dir)
cors = CORS(server)


@server.route('/')
def index():
    return render_template('index.html')


@server.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(gui_dir, filename)


@server.route('/api/name', methods=['POST'])
def name():
    name = request.get_json()['name']
    return f"Hello {name}."


def allowed_file(filename: str):
    if '.' not in filename:
        return False

    file_parts = filename.rsplit('.', 1)
    file_extension = file_parts[1].lower()

    return file_extension in {'wav', 'mp3'}


@server.route('/api/audio', methods=['POST'])
def audio():
    file = request.files['file']
    if not allowed_file(file.filename):
        return jsonify({
            'message': 'Only accept .wav or .mp3 file!'
        })

    temp_path = 'src/backend/tmp/temp.wav'
    file.save(temp_path)

    audio_data, sample_rate = librosa.load(temp_path)
    duration = librosa.get_duration(y=audio_data, sr=sample_rate)
    num_channels = audio_data.shape[0]
    num_samples = len(audio_data)
    sample_rate = sample_rate
    file_format = temp_path.split('.')[-1]
    file_size = os.path.getsize(temp_path)
    audio_info = {
        'file_path': temp_path,
        'duration': duration,
        'num_channels': num_channels,
        'num_samples': num_samples,
        'sample_rate': sample_rate,
        'file_format': file_format,
        'file_size': file_size
    }

    return jsonify(audio_info)
