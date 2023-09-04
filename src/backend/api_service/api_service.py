import os
from enum import Enum

import acoustid
import numpy as np
import shazam
from utils.env import get_env

from ..modules.audio_stream_io import save_numpy_as_audio_file

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


last_song_data = np.array([[], []])
last_song_metadata_options = [
    {
        "title": "not-set",
        "album": "not-set",
        "artist": "not-set",
        "album-artist": "not-set",
        "year": "not-set",
        "number": 0,
    }
]
current_song_data = np.array([[], []])
current_song_metadata_options = [
    {
        "title": "not-set",
        "album": "not-set",
        "artist": "not-set",
        "album-artist": "not-set",
        "year": "not-set",
        "number": 0,
    }
]


def get_last_song():
    """Get a fully analyzed song with all its metadata options.
    this should be called after a song is finished.
    :returns: tuple (song audio, song metadata options).
    """
    return last_song_data, last_song_metadata_options


def get_song_options(song_data, samplerate):
    """Load the song metadata options for the provided song audio data.
    :param song_data: the audio data to analyze.
    :returns: SongOptionResult.
    """
    # first check using acoustID
    if ACOUSTID_API_KEY is not None:
        duration, fingerprint = _create_fingerprint(song_data, samplerate)
        metadata = _get_api_song_data_acoustid(fingerprint, duration)
        if len(metadata) != 0:
            return _check_song_extended_or_finished(song_data, metadata)

    # if acoustID doesn't find anything, try shazam
    # shazam only works if the sample rate is 44100Hz though!
    if SHAZAM_API_KEY is not None and samplerate == 44100:
        metadata_start = shazam.lookup(song_data, SHAZAM_API_KEY, True)
        metadata_end = shazam.lookup(song_data, SHAZAM_API_KEY, False)
        metadata_start = [metadata_start] if metadata_start is not None else []
        metadata_end = [metadata_end] if metadata_end is not None else []

        shazam_metadata_options = _get_overlapping_metadata_values(
            metadata_start, metadata_end
        )
        if len(shazam_metadata_options) != 0:
            return _check_song_extended_or_finished(song_data, shazam_metadata_options)
        elif len(metadata_start) != 0 and len(metadata_end) != 0:
            return SongOptionResult.SONG_MISMATCH

    # if neither finds anything, song not recognised.
    _store_finished_song(song_data, ())
    return SongOptionResult.SONG_NOT_RECOGNISED


def _check_song_extended_or_finished(song_data, metadata_options):
    """
    Check if the song with the given metadata_options matches the current song.
    Store the finished song if applicable.
    :param song_data: The song data.
    :param metadata_options: The metadata options.
    :returns: SongOptionResult
    """
    global current_song_metadata_options
    global current_song_data
    match_metadata_options = _get_overlapping_metadata_values(
        current_song_metadata_options, metadata_options
    )

    if len(match_metadata_options) == 0:
        _store_finished_song(song_data=song_data, metadata_options=metadata_options)
        return SongOptionResult.SONG_FINISHED
    else:
        current_song_metadata_options = match_metadata_options
        current_song_data = np.concatenate((current_song_data, song_data), axis=1)
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
        overlapping_metadata = {}
        titles2 = map(lambda d: d["title"], metadata2)
        for metadata in metadata1:
            if metadata["title"] in titles2:
                overlapping_metadata.add(metadata)
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
    fingerprint_duration, fingerprint = acoustid.fingerprint_file(filename_with_path)
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
            result.append({"score": score, "title": title, "artist": artist})
        return result
    except acoustid.WebServiceError:
        return []


def _store_finished_song(song_data=np.array([[], []]), metadata_options=()):
    """Store the current (finished) song in last_song_data/last_song_metadata_options
    Store the provided song data as the current song data.
    Reset the current song data if none is provided.
    :param song_data: The new currently read song's data.
    :param metadata_options: The new currently read song's metadata options.
    """
    global current_song_data
    global current_song_metadata_options
    global last_song_data
    global last_song_metadata_options
    last_song_data = current_song_data
    last_song_metadata_options = current_song_metadata_options
    current_song_data = song_data
    current_song_metadata_options = metadata_options
