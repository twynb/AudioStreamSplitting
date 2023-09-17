from itertools import pairwise
from os import path
from typing import Generator, Tuple

import librosa
import music_tag
import numpy as np
import soundfile


def read_audio_file_to_numpy(
    audiofile, mono=False, offset=0, duration=None, sample_rate=22050
) -> Tuple[np.ndarray, float]:
    """
    Reads an audiofile into an numpy array.

    :param audiofile: Path to audiofile
    :param mono: If true, convert to mono.
    :param offset: Start of the segment to read, in seconds.
    :param duration: Duration of the segment to read, in seconds.
    :param sample_rate: Sample rate, defaults to Librosa standard 22050 Hz.
    :returns: Tuple[np.ndarray,float] array of sounddata
    """
    return librosa.load(
        audiofile, mono=mono, offset=offset, duration=duration, sr=sample_rate
    )


def read_audio_file_to_stream(
    audiofile, block_len=4096, mono=False
) -> (Generator[np.ndarray, None, None], float, int):
    """
    Reads an audiofile as blocks in a stream.

    :param audiofile: Path to audiofile
    :param block_len: block length of stream
    :param mono: loads file as mono audio if true
    :returns: Audiostream , samplerate, hop length
    """
    # get rates
    sr = librosa.get_samplerate(audiofile)
    default_sr = 22050

    frame_length = int(1024 * sr) // default_sr
    hop_length = int(1024 * sr) // default_sr

    return (
        librosa.stream(
            audiofile,
            block_length=block_len,
            frame_length=frame_length,
            hop_length=hop_length,
            mono=mono,
        ),
        sr,
        hop_length,
    )


def overlapping_stream(stream):
    """
    Changes a stream of audiodata blocks into a stream of overlapping blocks.
    These have to be in stereo.

    :param stream: Takes a Generator
    :returns: A Generator with 75% Overlap between each instance
    """
    for curr_block, next_block in pairwise(stream):
        for ratio in np.linspace(1, 0, 4, endpoint=False):
            if curr_block.ndim == 1:
                curr_start_index = int((curr_block.shape[0] * (1 - ratio)))
                next_end_index = int((next_block.shape[0] * (1 - ratio)))
                yield np.append(
                    curr_block[curr_start_index:], next_block[:next_end_index], axis=0
                )
            else:
                curr_start_index = int((curr_block.shape[1] * (1 - ratio)))
                next_end_index = int((next_block.shape[1] * (1 - ratio)))
                yield np.append(
                    curr_block[:, curr_start_index:],
                    next_block[:, :next_end_index],
                    axis=1,
                )
        if curr_block.shape != next_block.shape:
            yield next_block


def save_numpy_as_audio_file(
    song: np.ndarray,
    songname: str,
    file_path: str,
    rate=100,
    tags: dict = {},
    extension=".mp3",
):
    """
    Saves a numpy array into an audofile. Also sets tags to the audiofile.

    :param song: np.ndarray of the song
    :param songname: name of the song
    :param file_path: path to file (without filename)
    :param rate: samplerate of the song {Default: 100}
    :param tags: dict of tags see: :func:`tag_audio_file` {Default: {}}
    :param extension: string of the extension {Default: ".mp3"}
    :returns: none
    """
    savename = path.join(file_path, songname + extension)
    soundfile.write(savename, song.T, rate)
    tag_audio_file(savename, tags)


def tag_audio_file(savename: str, tags: dict):
    """
    Tags an audiofile with different tags.

    Possible tags:
            * album
            * albumartist
            * artist
            * artwork
            * comment
            * compilation
            * composer
            * discnumber
            * genre
            * lyrics
            * totaldiscs
            * totaltracks
            * tracknumber
            * tracktitle
            * year
            * isrc

    :param savename: path to savefile
    :param tags: dict of tags
    :returns: none
    """
    audiofile: music_tag.file.AudioFile = music_tag.load_file(savename)  # type: ignore
    if tags:
        for key, value in tags.items():
            audiofile.set(key, value)

    audiofile.save()
