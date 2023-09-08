import io
import os.path
import wave

import librosa
from flask import Blueprint, Response, jsonify, request, send_file
from modules.api_service import identify_all_from_generator
from modules.audio_stream_io import read_audio_file_to_numpy, save_numpy_as_audio_file
from modules.segmentation import segment_file

audio_bp = Blueprint("audio", __name__)

# TODO error handling!


@audio_bp.route("/split", methods=["POST"])
def split():
    data = request.json
    file_path = data["filePath"]
    if not os.path.exists(file_path):
        return "File does not exist!", 400
    generator = segment_file(file_path)
    print("==========================================")
    print("alo")
    print("==========================================")
    segments, mismatch_offsets = identify_all_from_generator(generator, file_path)

    result = {
        "segments": segments,
        "mismatchOffsets": mismatch_offsets,
    }

    return jsonify(result)


@audio_bp.route("/get-segment", methods=["POST"])
def get_segment():
    data = request.json
    file_path = data["filePath"]
    if not os.path.exists(file_path):
        return "File does not exist!", 400

    offset = data["offset"]
    duration = data["duration"]

    if offset <= 0 or duration <= 0:
        return "Invalid offset or duration!", 400

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
    if not os.path.exists(file_path):
        return "File does not exist!", 400
    target_directory = data["targetDirectory"]
    if not os.path.exists(target_directory):
        return "Target directory does not exist!", 400

    metadata = data["metadata"]
    offset = data["offset"]
    duration = data["duration"]
    if offset <= 0 or duration <= 0:
        return "Invalid offset or duration!", 400

    audio_data, sample_rate = read_audio_file_to_numpy(
        file_path, mono=False, offset=offset, duration=duration, sample_rate=None
    )
    save_numpy_as_audio_file(
        audio_data, metadata["title"], target_directory, sample_rate, tags=metadata
    )
    return jsonify({"success": True})


# TODO decide whether to remove the routes below this comment


@audio_bp.route("/process", methods=["POST"])
def process():
    data = request.json
    file_path = data["filePath"]
    if not os.path.exists(file_path):
        return "File does not exist!", 400
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
    if not os.path.exists(audio_path):
        return "File does not exist!", 400
    return send_file(audio_path)
