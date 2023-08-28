import librosa
from flask import Blueprint, jsonify, request, send_file

audio_bp = Blueprint("audio", __name__)


@audio_bp.route("/process", methods=["POST"])
def process():
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


@audio_bp.route("/get", methods=["POST"])
def get():
    data = request.json
    audio_path = data["audioPath"]
    return send_file(audio_path)
