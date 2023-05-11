import ffmpegio
import music_tag

def readAudiofileToNumPy(audiofile):
    return ffmpegio.audio.read(audiofile)

def readAudiofileToStream(audiofile,mode="",block=100):
    """ 
    ====  ===================================================
    Mode  Description
    ====  ===================================================
    'r'   read from url (default)
    'w'   write to url
    'f'   filter data defined by fg
    'v'   operate on video stream, 'vv' if multi-video reader
    'a'   operate on audio stream, 'aa' if multi-audio reader
    ====  ===================================================
    """
    with ffmpegio.open(audiofile,mode,blocksize=block) as fin:
        return fin

def saveNumPyAsAudioFile(song, songname:str, tags:dict={}, rate=100,extention = ".mp3"):
    savename = songname+extention
    ffmpegio.audio.write(savename,rate,song)
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
