import os

from api.audio import audio_bp
from api.env import env_bp
from api.project import project_bp
from flask import (
    Flask,
    render_template,
    send_from_directory,
)
from flask_cors import CORS
from utils.path import get_abs_src_dir_in_built_app

gui_dir = os.path.join(os.getcwd(), "gui")
if not os.path.exists(gui_dir):
    gui_dir = os.path.join(get_abs_src_dir_in_built_app(), "gui")

app = Flask(__name__, static_folder=gui_dir, template_folder=gui_dir)
app.register_blueprint(audio_bp, url_prefix="/api/audio")
app.register_blueprint(project_bp, url_prefix="/api/project")
app.register_blueprint(env_bp, url_prefix="/api/env")
CORS(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(gui_dir, filename)
