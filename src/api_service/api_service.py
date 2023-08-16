import numpy as np
from enum import Enum
import acoustid
from ..io.io import saveNumPyAsAudioFile
import os

"""
API-Service Workflow:
1. call get_song_options() with your audio data segment and its sample rate
2a. if SongOptionResult.SONG_EXTENDED is returned, repeat 1. with your next segment.
2b. if SongOptionResult.SONG_FINISHED is returned, get the finalised song using get_last_song(), then repeat 1. with your next segment.
2c. if SongOptionResult.FINGERPRINT_MISMATCH is returned, split up your segment further and repeat 1.
2d. if SongOptionResult.SONG_NOT_RECOGNISED is returned, get the finalised song using get_last_song(), then repeat 1. with your next segment.
TODO: Decide how to behave if SONG_NOT_RECOGNISED happens!
"""

# constant defining how much of the song_data is used for creating a fingerprint, by taking the first/last 1/FINGERPRINT_SEGMENT of data.
FINGERPRINT_SEGMENT = 3
# constant for the API key. TODO: allow user to provide API key.
API_KEY = "b'kDPSCEb4"

class SongOptionResult(Enum):
    """
    SongOptionResult contains information about the state of the API service.
    """
    SONG_EXTENDED = 0 # analysed song has results matching with the previous song, so the previous song is extended. Happens if a song was split in the middle.
    SONG_FINISHED = 1 # analysed song has no results matching with the previous song, so the previous song can be retrieved using get_last_song().
    FINGERPRINT_MISMATCH = 2 # fingerprints from the start and end of the analysed song have no matching results. Happens if two songs are still together after splitting.
    SONG_NOT_RECOGNISED = 3 # analysed song has no results from the API. Happens when the song isn't yet in the AcoustID database.

lastSongData = np.array([[], []])
lastSongMetadataOptions = ({"id": "", "title": "not-set", "album": "not-set", "artist": "not-set", "album-artist": "not-set", "year": "not-set", "number": 0})
currentSongData = np.array([[], []])
currentSongMetadataOptions = ()

def get_last_song():
    """
    get a fully analyzed song with all its metadata options.
    this should be called to provide a user with options after get_song_options returns SongOptionResult.SONG_FINISHED.
    :returns: a tuple that contains the song's audio data and the song's metadata options.
    """
    return lastSongData, lastSongMetadataOptions

def get_song_options(songData, samplerate):
    """
    load the song metadata options for the provided song audio data.
    :param songData: the audio data to analyze.
    :returns: SongOptionResult
    """
    global currentSongMetadataOptions
    global currentSongData
    fingerprintStart = create_fingerprint(songData, samplerate, True)
    fingerprintEnd = create_fingerprint(songData, samplerate, False)
    fingerprintLength = samplerate * len(songData[0]) / FINGERPRINT_SEGMENT
    metadataStart = get_api_song_data(fingerprintStart, fingerprintLength)
    metadataEnd = get_api_song_data(fingerprintEnd, fingerprintLength)
    if(len(metadataStart) == 0 and len(metadataEnd) == 0):
        store_finished_song()
        return SongOptionResult.SONG_NOT_RECOGNISED

    overlappingMetadata = get_overlapping_metadata_values(metadataStart, metadataEnd)
    if len(overlappingMetadata) == 0:
        return SongOptionResult.FINGERPRINT_MISMATCH

    matchMetadataOptions = get_overlapping_metadata_values(currentSongMetadataOptions, overlappingMetadata)
    if len(matchMetadataOptions) == 0:
        store_finished_song(songData=songData, metadataOptions=overlappingMetadata)
        return SongOptionResult.SONG_FINISHED
    else:
        currentSongMetadataOptions = matchMetadataOptions
        currentSongData = np.concatenate((currentSongData, songData), axis=1)
        return SongOptionResult.SONG_EXTENDED

def get_overlapping_metadata_values(metadata1, metadata2):
    """
    get all values from metadata1 and metadata2 that are the same.
    :param metadata1: first set of metadata to compare.
    :param metadata2: second set of metadata to compare.
    :returns: a set of metadata containing all matches.
    """
    if len(metadata1) == 0:
        return metadata2
    elif len(metadata2)  ==  0:
        return metadata1
    else:
        overlappingMetadata = {}
        idsEnd = map(lambda d: d["id"], metadata2)
        for metadata in metadata1:
            if metadata["id"] in idsEnd:
                overlappingMetadata.add(metadata)
        return overlappingMetadata

def create_fingerprint(songData, samplerate, fromBeginning = True):
    """
    create a fingerprint for either the first or last 1/FINGERPRINT_SEGMENT-th part of the audio data.
    :param songData: the audio data to generate a fingerprint from.
    :param samplerate: the audio data's sample rate.
    :param fromBeginning: whether to generate the fingerprint from the beginning or end of the audio data.
    :returns: the acoustID fingerprint.
    """
    newData = get_sample_segment_for_fingerprint(songData, fromBeginning)
    filename = "TEMP_FILE_FOR_FINGERPRINTING"

    saveNumPyAsAudioFile(newData, filename, os.path.abspath('') + '\\', rate=samplerate)
    filenameWithPath = os.path.abspath(filename + '.mp3')
    fingerprint = acoustid.fingerprint_file(filenameWithPath)
    os.remove(filenameWithPath)
    return fingerprint

def get_sample_segment_for_fingerprint(songData, fromBeginning):
    """
    get a segment of the audio data to sample for a fingerprint, formatted for acoustid.fingerprint().
    :param songData: the audio data to generate a fingerprint from.
    :param fromBeginning: whether to generate the sample segment from the beginning or end of the data.
    :returns: numpy.ndarray the sample segment.
    """
    newData = np.array([[],[]])
    sampleSize = round(len(songData[0]) / FINGERPRINT_SEGMENT)
    if(fromBeginning):
        newData = np.array([songData[0][0:sampleSize], songData[1][0:sampleSize]])
    else:
        endIndex = len(songData[0])-1
        startIndex = endIndex-sampleSize
        newData = np.array([songData[0][startIndex:endIndex], songData[1][startIndex:endIndex]])
    return ((newData - 0.5) * 2 * np.iinfo(np.int16).max).astype(np.int16)

def get_api_song_data(fingerprint, fingerprintLength):
    """
    get data about the provided fingerprint from the AcoustID API.
    :param fingerprint: the fingerprint.
    :param fingerprintLength: duration of the fingerprint in seconds.
    :returns: list({"id": the id, "score": how well the result matches the fingerprint, "title": song title, "artist": song artist})
    """
    try:
        lookupResult = acoustid.parse_lookup_result(acoustid.lookup(API_KEY, fingerprint, fingerprintLength))
        result = ()
        for lookupRes in lookupResult:
            result.append({"score": lookupRes[0], "id": lookupRes[1], "title": lookupRes[2], "artist": lookupRes[3]})
        return result
    except acoustid.WebServiceError:
        return ()
    return ()

def store_finished_song(songData = np.array([[],[]]), metadataOptions = ()):
    """
    Store the current (finished) song in lastSongData/lastSongMetadataOptions to be retrieved using get_last_song(), store the provided song data as the current song data or reset it.
    :param songData: The new currently read song's data. Resets to empty array if not specified.
    :param metadataOptions: The new currently read song's metadata options. Resets to empty list if not specified.
    """
    global currentSongData
    global currentSongMetadataOptions
    global lastSongData
    global lastSongMetadataOptions
    lastSongData = currentSongData
    lastSongMetadataOptions = currentSongMetadataOptions
    currentSongData = songData
    currentSongMetadataOptions = metadataOptions
