import os
from enum import Enum
from typing import Generator

import acoustid
import modules.apis.shazam as shazam
from utils.env import get_env

from .audio_stream_io import read_audio_file_to_numpy, save_numpy_as_audio_file

"""
TODO: Decide how to behave if SONG_NOT_RECOGNISED happens! Options:
a. Make it a separate song and ask for details in the frontend
b. Just append it to the current song and hope it fits
c. Start a new song and append the next segment to it.
Current implementation is c.
All of the above would lead to errors if previous and next segment are the same song.
"""

ACOUSTID_API_KEY = get_env("SERVICE_ACOUSTID_API_KEY")
SHAZAM_API_KEY = get_env("SERVICE_SHAZAM_API_KEY")


class SongOptionResult(Enum):
    """SongOptionResult contains information about the state of the API service."""

    SONG_EXTENDED = 0  # previous song extended by current song
    SONG_FINISHED = 1  # previous song finished, new song started
    SONG_MISMATCH = 2  # start and end of song are different songs
    SONG_NOT_RECOGNISED = 3  # analysed song has no results from the API.


EMPTY_METADATA_OPTIONS = [
    {
        "title": "not-set",
        "album": "not-set",
        "artist": "not-set",
        "year": "not-set",
    }
]

SAMPLE_RATE_STANDARD = 44100

last_song_offset = 0
last_song_duration = 0
last_song_metadata_options = EMPTY_METADATA_OPTIONS
current_song_offset = 0
current_song_duration = 0
current_song_metadata_options = EMPTY_METADATA_OPTIONS


def identify_all_from_generator(
    generator: Generator[tuple, float, float], file_path: (str, str)
):
    """Identify all segments from the segment generator in the given file.
    :param generator: A generator, usually from segment_file in segmentation.py.
    :param file_path: The file path.
    :returns: (segments, mismatches)
    """
    reset_service_state()
    is_first_segment = True
    segments = []
    mismatch_offsets = []
    for (segment, samplerate), start, duration in generator:
        result = get_song_options(start, duration, file_path)
        if (
            result
            in [SongOptionResult.SONG_FINISHED, SongOptionResult.SONG_NOT_RECOGNISED]
        ) and not is_first_segment:
            segments.append(get_last_song())
        elif result == SongOptionResult.SONG_MISMATCH:
            segments.append(get_last_song())
            mismatch_offsets.append(start)
        if result != SongOptionResult.SONG_EXTENDED:
            is_first_segment = False
    segments.append(get_final_song())
    return (segments, mismatch_offsets)


def reset_service_state():
    """Reset the service state."""
    global last_song_offset
    last_song_offset = 0
    global last_song_duration
    last_song_duration = 0
    global last_song_metadata_options
    last_song_metadata_options = EMPTY_METADATA_OPTIONS
    global current_song_offset
    current_song_offset = 0
    global current_song_duration
    current_song_duration = 0
    global current_song_metadata_options
    current_song_metadata_options = EMPTY_METADATA_OPTIONS


def get_last_song():
    """Get a fully analyzed song with all its metadata options.
    This should be called after a song is finished.
    :returns: dict
    """
    return _song_export(
        last_song_offset, last_song_duration, last_song_metadata_options
    )


def get_final_song():
    """Get the final fully analyzed song with all its metadata options.
    Reset the stored data after.
    This should be called once the last segment was iterated over.
    :returns: dict
    """
    result = _song_export(
        current_song_offset, current_song_duration, current_song_metadata_options
    )
    reset_service_state()
    return result


def _song_export(offset, duration, metadata_options):
    """Get the export as returned by get_last_song.
    :param offset: Start of the segment, in seconds.
    :param duration: Duration of the segment, in seconds.
    :param metadata_options: Metadata options as a dict.
    :returns: dict
    """
    return {"offset": offset, "duration": duration, "metadataOptions": metadata_options}


def get_song_options(offset: float, duration: float, file_path: str):
    """Load the song metadata options for the provided song audio data.
    :param offset: Start of the segment to analyze, in seconds.
    :param duration: Duration of the segment to analyze, in seconds.
    :param file_path: Path of the file to analyze.
    :returns: SongOptionResult.
    """
    sample_rate = SAMPLE_RATE_STANDARD
    song_data, sample_rate = read_audio_file_to_numpy(
        file_path, mono=False, offset=offset, duration=duration, sample_rate=sample_rate
    )
    # first check using acoustID
    if ACOUSTID_API_KEY is not None:
        duration, fingerprint = _create_fingerprint(song_data, sample_rate)
        metadata = _get_api_song_data_acoustid(fingerprint, duration)
        if len(metadata) != 0:
            return _check_song_extended_or_finished(offset, duration, metadata)

    # if acoustID doesn't find anything, try shazam
    # If sample_rate inexplicably becomes something other than 44100Hz, shazam won't work
    if SHAZAM_API_KEY is not None and sample_rate == SAMPLE_RATE_STANDARD:
        metadata_start = shazam.lookup(song_data, SHAZAM_API_KEY, True)
        metadata_end = shazam.lookup(song_data, SHAZAM_API_KEY, False)
        metadata_start = [metadata_start] if metadata_start is not None else []
        metadata_end = [metadata_end] if metadata_end is not None else []

        shazam_metadata_options = _get_overlapping_metadata_values(
            metadata_start, metadata_end
        )
        if len(shazam_metadata_options) != 0:
            return _check_song_extended_or_finished(
                offset, duration, shazam_metadata_options
            )
        elif len(metadata_start) != 0 and len(metadata_end) != 0:
            _store_finished_song(offset, duration, ())
            return SongOptionResult.SONG_MISMATCH

    # if neither finds anything, song not recognised.
    _store_finished_song(offset, duration, ())
    return SongOptionResult.SONG_NOT_RECOGNISED


def _check_song_extended_or_finished(offset: float, duration: float, metadata_options):
    """
    Check if the song with the given metadata_options matches the current song.
    Store the finished song if applicable.
    :param offset:  Start of the segment, in seconds.
    :param duration: Duration of the segment, in seconds.
    :param metadata_options: The metadata options.
    :returns: SongOptionResult
    """
    global current_song_offset
    global current_song_duration
    global current_song_metadata_options
    match_metadata_options = _get_overlapping_metadata_values(
        current_song_metadata_options, metadata_options
    )

    if len(match_metadata_options) == 0:
        _store_finished_song(
            offset=offset, duration=duration, metadata_options=metadata_options
        )
        return SongOptionResult.SONG_FINISHED
    else:
        current_song_metadata_options = match_metadata_options
        current_song_duration += duration
        return SongOptionResult.SONG_EXTENDED


def _get_overlapping_metadata_values(metadata1, metadata2):
    """Get all values from metadata1 and metadata2 that are the same.
    :param metadata1: first set of metadata to compare.
    :param metadata2: second set of metadata to compare.
    :returns: a set of metadata containing all matches.
    """
    if len(metadata1) == 0:
        return metadata2
    elif len(metadata2) == 0:
        return metadata1
    else:
        overlapping_metadata = []
        titles2 = map(lambda d: d["title"], metadata2)
        artists2 = map(lambda d: d["artist"], metadata2)
        for metadata in metadata1:
            if metadata["title"] in titles2 and metadata["artist"] in artists2:
                overlapping_metadata.append(metadata)
        return overlapping_metadata


def _create_fingerprint(song_data, samplerate):
    """Create a fingerprint for the audio data.
    :param song_data: the audio data to generate a fingerprint from.
    :param samplerate: the audio data's sample rate.
    :returns: (song duration, fingerprint).
    """
    filename = "TEMP_FILE_FOR_FINGERPRINTING"
    save_numpy_as_audio_file(song_data, os.path.abspath(filename), "", rate=samplerate)

    filename_with_path = os.path.abspath(filename + ".mp3")
    fingerprint_duration, fingerprint = acoustid.fingerprint_file(
        filename_with_path, force_fpcalc=True
    )
    os.remove(filename_with_path)
    return (fingerprint_duration, fingerprint)


def _get_api_song_data_acoustid(fingerprint, fingerprint_duration):
    """Get data about the provided fingerprint from the AcoustID API.
    :param fingerprint: the fingerprint.
    :param fingerprint_duration: duration of the fingerprint in seconds.
    :returns: [{"score": match score, "title": title, "artist": artist}]
    """
    try:
        result = []
        for score, recording_id, title, artist in acoustid.parse_lookup_result(
            acoustid.lookup(ACOUSTID_API_KEY, fingerprint, fingerprint_duration)
        ):
            result.append({"title": title, "artist": artist})
        return result
    except acoustid.WebServiceError:
        return []


def _store_finished_song(offset: float, duration: float, metadata_options):
    """Store the current (finished) data in the last_song_* variables.
    Store the provided data in the current_song_* variables.
    :param offset: The new currently read song's offset, in seconds.
    :param duration: The new currently read song's duration, in seconds.
    :param metadata_options: The new currently read song's metadata options.
    """
    global current_song_offset
    global current_song_duration
    global current_song_metadata_options
    global last_song_offset
    global last_song_duration
    global last_song_metadata_options
    last_song_offset = current_song_offset
    last_song_duration = current_song_duration
    last_song_metadata_options = current_song_metadata_options
    current_song_offset = offset
    current_song_duration = duration
    current_song_metadata_options = metadata_options
