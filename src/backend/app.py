import datetime
import os
import uuid

import librosa

from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    send_from_directory,
    make_response,
    send_file,
)
from flask_cors import CORS
from utils import audios_dir, mkdir

cwd = os.path.dirname(os.path.abspath(__file__))
gui_dir = os.path.join(cwd, "..", "..", "gui")
if not os.path.exists(gui_dir):
    gui_dir = os.path.join(cwd, "gui")

app = Flask(__name__, static_folder=gui_dir, template_folder=gui_dir)
cors = CORS(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(gui_dir, filename)


@app.route("/api/create_project", methods=["POST"])
def create_project():
    name = request.form.get("name")
    description = request.form.get("description")
    files = request.files.getlist("file")
    project_id = uuid.uuid4()
    project_path = f"{audios_dir}/{project_id}"
    mkdir(project_path)

    project = {
        "id": project_id,
        "name": name,
        "description": description,
        "path": project_path,
        "files": [],
        "createAt": datetime.datetime.now().isoformat(),
    }

    for file in files:
        file_name = file.filename
        file_path = f"{project_path}/{file_name}"
        file.save(file_path)

        project["files"].append({"fileName": file_name, "filePath": file_path})

    return jsonify(project)


@app.route("/api/process_audio", methods=["POST"])
def process_audio():
    data = request.json
    file_path = data["filePath"]
    audio_data, sample_rate = librosa.load(file_path, sr=None)
    duration = librosa.get_duration(y=audio_data, sr=sample_rate)
    num_channels = audio_data.shape[0]
    num_samples = len(audio_data)
    info = {
        "duration": duration,
        "numChannels": num_channels,
        "numSamples": num_samples,
        "sampleRate": sample_rate,
    }
    file = {"filePath": file_path, "info": info}

    return jsonify(file)


@app.route("/api/get_audio", methods=["POST"])
def get_audio():
    data = request.json
    audio_path = data["audioPath"]
    return send_file(audio_path)


@app.route("/api/clear_all", methods=["GET"])
def clear_all():
    for root, dirs, files in os.walk(audios_dir, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            os.rmdir(dir_path)
    return make_response({}, 204)
