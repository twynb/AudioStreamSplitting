import os
from flask import Flask, render_template, send_from_directory, jsonify

gui_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'gui')

server = Flask(__name__, static_folder=gui_dir, template_folder=gui_dir)


@server.route('/')
def index():
    return render_template('index.html')


@server.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(gui_dir, filename)


@server.route('/foo', methods=['GET'])
def foo():
    return jsonify({
        'status': 'ok',
    })
