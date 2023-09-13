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

Reads a file To load as a numpy array.

#### read_audio_file_to_numpy:Arguments

- `` audiofile: string|path `` Path to audiofile
- `` mono: bool `` If true, convert to mono.
- `` offset: float `` Start of the segment to read, in seconds.
- `` duration: float `` Duration of the segment to read, in seconds.
- `` sample_rate: int `` Sample rate, defaults to Librosa standard 22050 Hz.

#### read_audio_file_to_numpy:Returns

Returns a ``Tuple[np.ndarray,float]`` of sound data.

### read_audio_file_to_stream

Reads an audiofile as a stream.

#### read_audio_file_to_stream:Arguments

- `` audiofile: string `` Path to audio file
- `` block_len: int `` Block length of stream
- `` mono: bool `` Loads file as mono audio if true

#### read_audio_file_to_stream:Returns

Returns an `` audiostream: Generator `` the `` samplerate: int `` and the `` hop_lenght: int ``.

### overlapping_stream

Gets a stream and returns is with 75% overlap between each instance.

#### overlapping_stream:Arguments

- `` stream: Generator `` Takes a generator of stereo audio file data. Stereo data with the size $2\times x$ (2 channels) with $x$ as the block size.

#### overlapping_stream:Retruns

Returns a `` Generator `` with the size $2\times y$ (2 channels) with $y$ as the block size.

### save_numpy_as_audio_file

#### save_numpy_as_audio_file:Augments

- `` song: np.ndarray`` Numpy array of the song
- `` songname: string `` Name of the song
- `` file_path: string|path `` Path to file (without file name)
- `` rate: int `` Samplerate of the song {Default: 100}
- `` tags: dict `` Dict of tags {Default: {}} see [Tags](#tag_audio_file)
- `` extension: string `` String of the extension {Default: ".mp3"}

### tag_audio_file

#### tag_audio_file:Augments

- `` savename: string|path `` Path to savefile
- `` songname: string `` Name of the song
- `` tags: dict `` A dict of tags

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

Also some aliases like album -> albumname are possible
