import music_tag
import soundfile
import librosa
import numpy
from typing import Tuple

def readAudiofileToNumPy(audiofile)-> Tuple[numpy.ndarray, float]:
    return librosa.load(audiofile)

def readAudiofileToStream(audiofile,mode="",block=100):
    sr = librosa.get_samplerate('/path/to/file.wav')

    frame_length = int(2048 * sr) // 22050
    hop_length = int(512 * sr) // 22050

    librosa.stream(audiofile,block_length=128,frame_length=frame_length,hop_length=hop_length)

def saveNumPyAsAudioFile(song:numpy.ndarray, songname:str, rate=100 ,tags:dict={},extention = ".mp3"):
    """Tags -> tagAudiofile()"""
    savename = songname+extention
    soundfile.write(savename,song,rate)
    tagAudiofile(savename,songname,tags)

def tagAudiofile(savename:str,songname:str,tags:dict):
    """
    Tags:
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
    """
    audiofile:music_tag.file.AudioFile = music_tag.load_file(savename)
    audiofile.append_tag("title",songname)
    if tags:
        for key,values in tags.items():
            for value in values:
                audiofile.append_tag(key,value)
    audiofile.save()
