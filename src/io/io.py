import music_tag
import soundfile
import librosa
import numpy as np
from typing import Tuple,Generator

def readAudiofileToNumPy(audiofile, mono=False)-> Tuple[np.ndarray, float]:
    """
    :param audiofile: Path to audiofile
    :returns: Tuple[np.ndarray,float] array of sounddata
    """
    return librosa.load(audiofile, mono=mono)

def readAudiofileToStream(audiofile,rate=128,mono=False) -> Generator[np.ndarray, None, None]:
    """
    :param audiofile: Path to audiofile
    :param rate: block length of stream
    :returns: Audiostream
    """
    #get rates
    sr = librosa.get_samplerate(audiofile)
    default_sr = 22050

    frame_length = int(2048 * sr) // default_sr
    hop_length = int(512 * sr) // default_sr

    return librosa.stream(audiofile,block_length=rate,frame_length=frame_length,hop_length=hop_length,mono=mono)

def saveNumPyAsAudioFile(song:np.ndarray, songname:str,path:str , rate=100 ,tags:dict={},extention = ".mp3"):
    """
    :param song: np.ndarray of the song
    :param songname: name of the song
    :param path: path to file (without filename)
    :param rate: samplerate of the song {Default: 100}
    :param tags: dict of tags {Default: {}}
    :param extention: string of the extention {Default: ".mp3"}
    :returns: none
    """
    savename = path+songname+extention
    soundfile.write(savename,song,rate)
    tagAudiofile(savename,songname,tags)

def tagAudiofile(savename:str,songname:str,tags:dict):
    """
    :param savename: path to savefile 
    :param songname: name of the song
    :param tags:
        album
        albumartist
        artist
        artwork
        comment
        compilation
        composer
        discnumber
        genre
        lyrics
        totaldiscs
        totaltracks
        tracknumber
        tracktitle
        year
        isrc
    :returns: none
    """
    audiofile:music_tag.file.AudioFile = music_tag.load_file(savename) # type: ignore
    audiofile.append_tag("title",songname)
    if tags:
        for key,values in tags.items():
            for value in values:
                audiofile.append_tag(key,value)
    audiofile.save()
