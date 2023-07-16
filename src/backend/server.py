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


@server.route('/api/info', methods=['POST'])
def audio():
    name = request.form.get('name')
    description = request.form.get('description')
    files = request.files.getlist('file')

    project = {
        'name': name,
        'description': description,
        'files': []
    }

    for file in files:
      audio_data, sample_rate = librosa.load(file, sr=None)
      duration = librosa.get_duration(y=audio_data, sr=sample_rate)
      num_channels = audio_data.shape[0]
      num_samples = len(audio_data)
      file_format = file.filename.split('.')[-1]
      file.seek(0)
      file_size = len(file.read())
      info = {
          'name': file.filename,
          'duration': duration,
          'numChannels': num_channels,
          'numSamples': num_samples,
          'sampleRate': sample_rate,
          'format': file_format,
          'size': file_size
      }
      project['files'].append(info)

    return jsonify(project)

