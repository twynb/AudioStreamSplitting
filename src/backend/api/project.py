import datetime
import os
import uuid

from flask import Blueprint, jsonify, make_response, request
from utils.path import audios_dir, mkdir

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
        file_name = file.filename
        name = file_name.split(".")[0]
        file_type = file_name.split(".")[-1]
        file_path = f"{project_path}/{file_name}"
        file.save(file_path)

        project["files"].append(
            {
                "fileName": file_name,
                "filePath": file_path,
                "name": name,
                "fileType": file_type,
            }
        )

    return jsonify(project)


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
