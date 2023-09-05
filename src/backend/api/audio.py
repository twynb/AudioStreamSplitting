import io
import wave

import librosa
from flask import Blueprint, Response, jsonify, request, send_file

from ..modules.api_service import identify_all_from_generator
from ..modules.audio_stream_io import read_audio_file_to_numpy, save_numpy_as_audio_file
from ..modules.segmentation import segment_file

audio_bp = Blueprint("audio", __name__)

# TODO error handling!


@audio_bp.route("/split", methods=["POST"])
def split():
    data = request.json
    file_path = data["filePath"]
    generator = segment_file(file_path)
    segments = identify_all_from_generator(generator, file_path)

    result = {
        "segments": segments if segments is not None else [],
        "success": segments is not None,
    }

    return jsonify(result)


@audio_bp.route("/get-segment", methods=["POST"])
def get_segment():
    data = request.json
    file_path = data["filePath"]
    offset = data["offset"]
    duration = data["duration"]

    audio_data, sample_rate = read_audio_file_to_numpy(
        file_path, mono=False, offset=offset, duration=duration, sample_rate=None
    )
    audio_data = (audio_data * (2**15 - 1)).astype("<i2")

    audio_stream = io.BytesIO()

    with wave.open(audio_stream, "w") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(audio_data.tobytes())

    headers = {
        "Content-Type": "audio/wav",
        "Content-Disposition": "inline; filename=audio.wav",
    }

    audio_stream.seek(0)

    content_length = len(audio_stream.getvalue())

    return Response(
        audio_stream,
        headers=headers,
        content_length=content_length,
        content_type="audio/wav",
    )


@audio_bp.route("/store", methods=["POST"])
def store():
    data = request.json
    file_path = data["filePath"]
    target_file_path = data["targetFilePath"]
    metadata = data["metadata"]
    offset = data["offset"]
    duration = data["duration"]
    audio_data, sample_rate = read_audio_file_to_numpy(
        file_path, mono=False, offset=offset, duration=duration, sample_rate=None
    )
    save_numpy_as_audio_file(
        audio_data, metadata["title"], target_file_path, sample_rate, tags=metadata
    )
    return jsonify({"success": True})


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
