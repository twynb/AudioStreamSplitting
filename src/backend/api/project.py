import datetime
import os
import subprocess
import uuid

from flask import Blueprint, jsonify, make_response, request
from utils.path import audios_dir, mkdir
from werkzeug.utils import secure_filename

project_bp = Blueprint("project", __name__)


@project_bp.route("/create", methods=["POST"])
def create():
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
        file_name = secure_filename(file.filename)
        name, file_extension = os.path.splitext(file_name)
        file_type = file_extension.strip(".")
        file_path = os.path.join(project_path, file_name)
        file.save(file_path)

        if file_extension.lower() == ".webm":
            output_path = os.path.join(project_path, f"{name}.wav")
            try:
                subprocess.run(
                    [
                        "ffmpeg",
                        "-i",
                        file_path,
                        "-acodec",
                        "pcm_s16le",
                        "-ar",
                        "44100",
                        output_path,
                    ],
                    check=True,
                )
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")
            else:
                os.remove(file_path)
                file_name = f"{name}.wav"
                file_path = output_path
                file_type = "wav"

        project["files"].append(
            {
                "fileName": file_name,
                "filePath": file_path,
                "name": name,
                "fileType": file_type,
            }
        )

    return jsonify(project)


@project_bp.route("/check-ffmpeg")
def check_ffmpeg():
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )
        return "ffmpeg is installed", 400
    except subprocess.CalledProcessError:
        return "ffmpeg is not installed", 404


@project_bp.route("/clear", methods=["GET"])
def clear():
    for root, dirs, files in os.walk(audios_dir, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            os.rmdir(dir_path)
    return make_response({}, 204)
