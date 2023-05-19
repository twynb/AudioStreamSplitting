import os
from flask import Flask, render_template, send_from_directory, jsonify
from flask_cors import CORS

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


@server.route('/api/foo', methods=['GET'])
def foo():
    obj = {}
    for i in range(10):
        obj[f"key {i}"] = f"value {i}"
    return jsonify({
        'status': 'ok',
        'message': obj
    })
