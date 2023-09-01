import requests
import numpy as np
import base64
import librosa

SHAZAM_URL_DETECT_V2 = "https://shazam.p.rapidapi.com/songs/v2/detect"
# duration of segments taken from the song data to be sent to the API, in seconds
LOOKUP_SEGMENTS_DURATION = 4
# amount of time to skip to the next segment if segment isn't recognized, in seconds
LOOKUP_OFFSET_INCREMENT = 10


# TODO-CR figure out what happens when API limit is reached
def lookup(songData: np.ndarray, apikey: str, fromStart: bool = True):
    """
    Look up a song using the Shazam API.
    :param songData: The song data. Must be at a sample rate of 44.100 Hz.
    :param apikey: The Shazam API key.
    :param fromStart: Whether to take a sample from the start or end of the song.
    :returns: the retrieved metadata, or None if no matches are found.
    """
    offset = 0 if fromStart else -(LOOKUP_SEGMENTS_DURATION * 44100)

    songData = format_song_data(songData)
    length = len(songData)
    matches, track = lookup_segment_with_offset(songData, apikey, offset)
    while len(matches) == 0:
        offset += (LOOKUP_OFFSET_INCREMENT * 44100) * (1 if fromStart else -1)
        if (fromStart and offset > length) or (not fromStart and offset < -length):
            break
        matches, track = lookup_segment_with_offset(songData, apikey, offset)
    if len(matches) != 0:
        album = extract_value_from_metadata(track, "Album")
        year = extract_value_from_metadata(track, "Released")
        return {
            "title": track["title"],
            "artist": track["subtitle"],
            "album": album,
            "year": year,
        }
    return None


def lookup_segment_with_offset(songData: np.ndarray, apikey: str, offset: int):
    """
    Look up a song segment at the given offset.
    :param songData: The song data. Must be at a sample rate of 44.100 Hz.
    :param apikey: The Shazam API key.
    :param offset: The offset to look up from.
    :returns: the retrieved metadata.
    """
    songDataSegment = get_song_data_segment(songData, offset)
    payload = create_payload_from_song_data(songDataSegment)
    response = send_lookup_request(payload, apikey).json()
    return (response["matches"], response["track"])


def format_song_data(songData):
    """
    Format the song data as a mono int16 array.
    :param songData: The song data.
    :returns: The formatted song data.
    """
    return (librosa.to_mono(songData) * 32767).astype("<i2")


def get_song_data_segment(songData: np.ndarray, offset: int):
    """
    Get a segment of the song data, either from the start or end of the data.
    :param songData: The song data. Must be at a sample rate of 44.100 Hz.
    :param offset: The offset to take the data from.
    :returns: The song data segment.
    """
    endIndex = offset + (44100 * LOOKUP_SEGMENTS_DURATION)
    if endIndex == 0:
        return songData[offset:]
    return songData[offset:endIndex]


def create_payload_from_song_data(songData: np.ndarray):
    """
    Create the payload in the API's data format (base64-encoded byte array).
    :param songData: The song data.
    :returns: The payload.
    """
    return base64.b64encode(songData.tobytes())


def send_lookup_request(payload: str, apikey: str):
    """
    Send the actual lookup request to the shazam API.
    :param payload: The payload (generate with create_payload_from_song_data)
    :param apikey: The Shazam API key.
    :returns: The request response.
    """
    headers = {
        "content-type": "text/plain",
        "X-RapidAPI-Key": apikey,
        "X-RapidAPI-Host": "shazam.p.rapidapi.com",
    }
    return requests.post(SHAZAM_URL_DETECT_V2, data=payload, headers=headers)


def extract_value_from_metadata(track, key: str):
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
