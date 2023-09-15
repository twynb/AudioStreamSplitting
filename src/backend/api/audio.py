import io
import os.path
import wave

from flask import Blueprint, Response, jsonify, request, send_file
from modules.api_service import ApiService
from modules.audio_stream_io import read_audio_file_to_numpy, save_numpy_as_audio_file
from modules.segmentation import segment_file
from pathvalidate import sanitize_filename
from utils.env import get_env
from utils.file_name_formatter import format_file_name

audio_bp = Blueprint("audio", __name__)


@audio_bp.route("/split", methods=["POST"])
def split():
    """Split and identify the segments of the provided file.
    This uses the logic from `modules.api_service` and `modules.segmentation`.
    :returns: The result as a JSON, if the file path is valid. A 400 error otherwise.
    """
    data = request.json
    file_path = data["filePath"]
    if not os.path.exists(file_path):
        return "File does not exist!", 400
    generator = segment_file(file_path)
    segments, mismatch_offsets = ApiService().identify_all_from_generator(
        generator, file_path
    )

    result = {
        "segments": segments,
        "mismatchOffsets": mismatch_offsets,
    }

    return jsonify(result)


@audio_bp.route("/get-segment", methods=["POST"])
def get_segment():
    """Get the given segment of the provided file's audio.
    Formats the segment as a wav file and sends that file.
    :returns: the audio as a .wav file.
    """
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

    return Response(
        audio_stream,
        headers=headers,
        content_type="audio/wav",
    )


@audio_bp.route("/store", methods=["POST"])
def store():
    """Store the given segment of the provided file as a new file.
    Add the given metadata to this file.
    If the provided file or the target directory does not exist, a 400 error is returned.
    :returns: "{success: true}" if storing the file worked. A 400 error otherwise.
    """
    data = request.json
    file_path = data["filePath"]
    if not os.path.exists(file_path):
        return "File does not exist!", 400
    target_directory = data["targetDirectory"]
    if not os.path.exists(target_directory):
        return "Target directory does not exist!", 400

    metadata = data["metadata"]

    file_type = "." + (data["fileType"] if "fileType" in data else "mp3")
    file_name_template = (
        data["nameTemplate"]
        if "nameTemplate" in data
        else get_env("OUTPUT_FILE_NAME_TEMPLATE")
    )
    target_file_name = sanitize_filename(
        format_file_name(
            file_name_template,
            metadata["title"] if "title" in metadata else "",
            metadata["artist"] if "artist" in metadata else "",
            metadata["album"] if "album" in metadata else "",
            str(metadata["year"]) if "year" in metadata else "",
        )
    )

    offset = data["offset"]
    duration = data["duration"]
    if offset <= 0 or duration <= 0:
        return "Invalid offset or duration!", 400

    audio_data, sample_rate = read_audio_file_to_numpy(
        file_path, mono=False, offset=offset, duration=duration, sample_rate=None
    )
    save_numpy_as_audio_file(
        audio_data,
        target_file_name,
        target_directory,
        sample_rate,
        tags=metadata,
        extension=file_type,
    )
    return jsonify({"success": True})


@audio_bp.route("/get", methods=["POST"])
def get():
    """Load an audio file into the frontend.
    :returns: The audio path. A 400 error if it does not exist.
    """
    data = request.json
    audio_path = data["audioPath"]
    if not os.path.exists(audio_path):
        return "File does not exist!", 400
    return send_file(audio_path)
