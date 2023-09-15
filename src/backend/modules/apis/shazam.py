import base64

import librosa
import numpy as np
import requests

"""
This class provides functionality to access the Shazam API (https://rapidapi.com/apidojo/api/shazam)
to identify a segment of song data.

Requests are performed using the `requests` library, so functions sending requests to the
Shazam API may raise all exceptions `requests` can raise.
"""

"""The URL to send requests to."""
SHAZAM_URL_DETECT_V2 = "https://shazam.p.rapidapi.com/songs/v2/detect"
"""duration of segments taken from the song data to be sent to the API, in seconds."""
LOOKUP_SEGMENTS_DURATION = 4
"""amount of time to skip to the next segment if segment isn't recognized, in seconds."""
LOOKUP_OFFSET_INCREMENT = 10


def lookup(song_data: np.ndarray, apikey: str, from_start: bool = True):
    """Attempt to identify the given song using the Shazam API.
        If the song can't be recognised from the first segment, step through it until the song ends
        or a result is found.
        The step size is defined by LOOKUP_OFFSET_INCREMENT and set to 10 seconds by default.
        The segment size is defined by LOOKUP_SEGMENTS_DURATION and set to 4 seconds by default,
        as the Shazam API expects segments between 3 and 5 seconds.
        :param song_data: The song data. The data must be at a sample rate of 44100Hz as the Shazam
            API will not work with other sample rates.
        :param apikey: The Shazam API key.
        :param from_start: Whether to take a sample from the start or end of the song.
        :returns: the retrieved metadata as a dict, or None if no matches are found.
            Example:
            ``
            {
              "title": "Thunderstruck",
              "artist": "AC/DC",
              "album": "The Razor's Edge",
              "year": "1990"
            }
            ``
        :raise `requests.exceptions.RequestException`: if the request fails due to network problems,
            too many redirections or other problems. A detailed list of Exceptions `requests`can
            raise can be found in the `requests` documentation at
            (https://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions)
        Usage example:
    Load a song and load metadata for it using `lookup`.
    ``
    import librosa
    import modules.apis.shazam

    song, sr = librosa.load("my_cool_file", sr=44100)
    result = lookup(song, "MY-SHAZAM-API-KEY")

    print(result)
    ``
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
    """Look up a segment of the given song at the given offset.
    This function integrates functionality to create the payload required for a request,
    send the request to the Shazam API and process the response.
    :param song_data: The song data. Must be at a sample rate of 44.100 Hz.
    :param apikey: The Shazam API key.
    :param offset: The offset the segment should start at, in seconds.
    :returns: Tuple (matches, track) of the retrieved metadata, matching the sections of the API
        response with the same name.
        The format for the API response can be found using the test functionality on the Shazam API
        website (https://rapidapi.com/apidojo/api/shazam).
    :raise `requests.exceptions.RequestException`: If the request fails due to network problems,
        too many redirections or other problems.
        A detailed list of Exceptions `requests`can raise can be found at (https://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions)
    """
    song_data_segment = _get_song_data_segment(song_data, offset)
    payload = _create_payload_from_song_data(song_data_segment)
    response = _send_lookup_request(payload, apikey).json()
    if "track" in response and "matches" in response:
        return (response["matches"], response["track"])
    return ([], [])


def _format_song_data(song_data):
    """Format the song data as a mono 16-bit integer array,
    as the Shazam API will not work with other formats.
    :param song_data: The song data. This is expected to be formatted as floats between -1 and 1.
    :returns: `numpy.ndarray` containing the formatted song data.
    """
    return (librosa.to_mono(song_data) * 32767).astype("<i2")


def _get_song_data_segment(song_data: np.ndarray, offset: int):
    """Extract a segment of the song data at the given offset.
    The duration of the segment is determined by the LOOKUP_SEGMENTS_DURATION constant.
    :param song_data: The song data.
    :param offset: The offset the snippet should start at, in seconds.
    :returns: `numpy.ndarray` containing the extracted segment.
    """
    end_index = offset + (44100 * LOOKUP_SEGMENTS_DURATION)
    if end_index == 0:
        return song_data[offset:]
    return song_data[offset:end_index]


def _create_payload_from_song_data(song_data: np.ndarray):
    """Create the payload to include with the request in the Shazam API's data format
    (A base64-encoded byte array). This expects that the song data has been formatted using
    `format_song_data` and that the song data is between 3-5 seconds long.
    :param song_data: The song data, formatted as a mono 16-bit integer array..
    :returns: `str` containing the payload.
    """
    return base64.b64encode(song_data.tobytes())


def _send_lookup_request(payload: str, apikey: str):
    """Send the actual lookup request to the Shazam API. This uses the `requests` module to send
    the request and can thus raise all errors a failed `requests.post` can.
    :param payload: The payload as generated by `_create_payload_from_song_data`
    :param apikey: The Shazam API key.
    :returns: `requests.Response` containing the request response. The format for the API response
        can be found using the test functionality at the Shazam API website at
        https://rapidapi.com/apidojo/api/shazam.
    :raise `requests.exceptions.RequestException`: If the request fails due to network problems,
        too many redirections or other problems.
        A detailed list of Exceptions `requests`can raise can be found at (https://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions)
    """
    headers = {
        "content-type": "text/plain",
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "shazam.p.rapidapi.com",
    }
    return requests.post(SHAZAM_URL_DETECT_V2, data=payload, headers=headers)


def _extract_value_from_metadata(track, key: str):
    """Extract a value from the response's "Metadata" section.
    If an error occurs that leads to the "Metadata" section containing two sets of data with the
    same label, the first set of data is returned. This should not be able to happen.
    :param track: The "track" segment of the API response.
    :param key: The key to search for in the metadata.
    :returns: `str` containing the value, or an empty `str` if it doesn't exist.
    """
    for item in [
        x["text"] for x in track["sections"][0]["metadata"] if x["title"] == key
    ]:
        return item
    return ""
