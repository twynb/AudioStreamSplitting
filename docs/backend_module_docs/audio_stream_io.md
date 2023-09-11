# Audio Stream IO

## Contents

Public functions:

- [read\_audio\_file\_to\_numpy](#read_audio_file_to_numpy)
- [read\_audio\_file\_to\_stream](#read_audio_file_to_stream)
- [overlapping\_stream](#overlapping_stream)
- [save\_numpy\_as\_audio\_file](#save_numpy_as_audio_file)
- [tag\_audio\_file](#tag_audio_file)

## Public functions

### read_audio_file_to_numpy

Reads a File To Load as a numpy Array

#### read_audio_file_to_numpy:Arguments

- `` audiofile: string|path `` Path to audiofile
- `` mono: bool `` If true, convert to mono.
- `` offset: float `` Start of the segment to read, in seconds.
- `` duration: float `` Duration of the segment to read, in seconds.
- `` sample_rate: int `` Sample rate, defaults to Librosa standard 22050 Hz.

#### read_audio_file_to_numpy:Returns

Returns a ``Tuple[np.ndarray,float]`` of sounddata

### read_audio_file_to_stream

Reads A audofile as a Stream

#### read_audio_file_to_stream:Arguments

- `` audiofile: string `` Path to audiofile
- `` block_len: int `` block length of stream
- `` mono: bool `` loads file as mono audio if true

#### read_audio_file_to_stream:Returns

Returns an `` Audiostream: Generator `` the `` Samplerate: int `` and the `` hop_lenght: int ``

### overlapping_stream

Gets a stream and Returns is with 75% overlapp between each instance.

#### overlapping_stream:Arguments

- `` stream: Generator `` Takes a generator of stereo Audiofiles. $2\times x$ with x as the block size

#### overlapping_stream:Retruns

Returns a `` Generator `` with the size $2\times y$ with y as the block size

### save_numpy_as_audio_file

#### save_numpy_as_audio_file:Augments

- `` song: np.ndarray`` of the song
- `` songname: string `` name of the song
- `` file_path: string|path `` path to file (without filename)
- `` rate: int `` samplerate of the song {Default: 100}
- `` tags: dict `` dict of tags {Default: {}} see [Tags](#tag_audio_file)
- `` extension: string `` string of the extension {Default: ".mp3"}

### tag_audio_file

#### tag_audio_file:Augments

- `` savename: string|path `` path to savefile
- `` songname: string `` name of the song
- `` tags: dict `` A dict of Tags

##### tag_audio_file:Augments:tags

Possible tags are:

- album
- albumartist
- artist
- artwork
- comment
- compilation
- composer
- discnumber
- genre
- lyrics
- totaldiscs
- totaltracks
- tracknumber
- tracktitle
- year
- isrc

Also some alieses like album -> albumname are possible
