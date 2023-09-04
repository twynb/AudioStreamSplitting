import base64

import librosa
import numpy as np
import requests

SHAZAM_URL_DETECT_V2 = "https://shazam.p.rapidapi.com/songs/v2/detect"
# duration of segments taken from the song data to be sent to the API, in seconds
LOOKUP_SEGMENTS_DURATION = 4
# amount of time to skip to the next segment if segment isn't recognized, in seconds
LOOKUP_OFFSET_INCREMENT = 10


# TODO-CR figure out what happens when API limit is reached
def lookup(song_data: np.ndarray, apikey: str, from_start: bool = True):
    """
    Look up a song using the Shazam API.
    :param song_data: The song data. Must be at a sample rate of 44.100 Hz.
    :param apikey: The Shazam API key.
    :param from_start: Whether to take a sample from the start or end of the song.
    :returns: the retrieved metadata, or None if no matches are found.
    """
    offset = 0 if from_start else -(LOOKUP_SEGMENTS_DURATION * 44100)

    song_data = _format_song_data(song_data)
    length = len(song_data)
    matches, track = _lookup_segment_with_offset(song_data, apikey, offset)
    while len(matches) == 0:
        offset += (LOOKUP_OFFSET_INCREMENT * 44100) * (1 if from_start else -1)
        if (from_start and offset > length) or (not from_start and offset < -length):
            break
        matches, track = _lookup_segment_with_offset(song_data, apikey, offset)
    if len(matches) != 0:
        album = _extract_value_from_metadata(track, "Album")
        year = _extract_value_from_metadata(track, "Released")
        return {
            "title": track["title"],
            "artist": track["subtitle"],
            "album": album,
            "year": year,
        }
    return None


def _lookup_segment_with_offset(song_data: np.ndarray, apikey: str, offset: int):
    """
    Look up a song segment at the given offset.
    :param song_data: The song data. Must be at a sample rate of 44.100 Hz.
    :param apikey: The Shazam API key.
    :param offset: The offset to look up from.
    :returns: the retrieved metadata.
    """
    song_data_segment = _get_song_data_segment(song_data, offset)
    payload = _create_payload_from_song_data(song_data_segment)
    response = _send_lookup_request(payload, apikey).json()
    if "track" in response and "matches" in response:
        return (response["matches"], response["track"])
    return ([], [])


def _format_song_data(song_data):
    """
    Format the song data as a mono int16 array.
    :param song_data: The song data.
    :returns: The formatted song data.
    """
    return (librosa.to_mono(song_data) * 32767).astype("<i2")


def _get_song_data_segment(song_data: np.ndarray, offset: int):
    """
    Get a segment of the song data, either from the start or end of the data.
    :param song_data: The song data. Must be at a sample rate of 44.100 Hz.
    :param offset: The offset to take the data from.
    :returns: The song data segment.
    """
    end_index = offset + (44100 * LOOKUP_SEGMENTS_DURATION)
    if end_index == 0:
        return song_data[offset:]
    return song_data[offset:end_index]


def _create_payload_from_song_data(song_data: np.ndarray):
    """
    Create the payload in the API's data format (base64-encoded byte array).
    :param song_data: The song data.
    :returns: The payload.
    """
    return base64.b64encode(song_data.tobytes())


def _send_lookup_request(payload: str, apikey: str):
    """
    Send the actual lookup request to the shazam API.
    :param payload: The payload (generate with _create_payload_from_song_data)
    :param apikey: The Shazam API key.
    :returns: The request response.
    """
    headers = {
        "content-type": "text/plain",
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "shazam.p.rapidapi.com",
    }
    return requests.post(SHAZAM_URL_DETECT_V2, data=payload, headers=headers)


def _extract_value_from_metadata(track, key: str):
    """
    Extract a value from the response's "Metadata" section.
    :param track: The response's "track" element
    :param key: The metadata type to search
    :returns: The value.
    """
    for item in [
        x["text"] for x in track["sections"][0]["metadata"] if x["title"] == key
    ]:
        return item
