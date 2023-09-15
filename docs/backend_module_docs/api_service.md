# Module API Service

This class provides utilities for identifying songs using various song recognition APIs. Currently, the [Shazam API](https://rapidapi.com/apidojo/api/shazam) and [AcoustID](https://acoustid.org/) are supported. Support for other APIs might be added in the future (see issue #53).

To aid in finding segmentation errors, the service is stateful. The currently identified song as well as the last one are stored to allow concatenating segments in case the splitting was too eager. Songs are stored as their duration, their starting offset in a given file as well as their metadata options as gathered from song recognition APIs.

An example for the general workflow of the API service can be found in ``identify_all_from_generator``.

## Contents

Classes:

- [``SongOptionResult``](#songoptionresult)
- [``ApiService``](#apiservice)

## Classes

### SongOptionResult

Enum containing all possible results of ``get_song_options``:

- ``SONG_EXTENDED: 0``: The previous and current song segments are the same song. This happens if the segmentation algorithm split a song in the middle. The previous segment has been extended to include the current one.
- ``SONG_FINISHED: 1``: The previous and current song segments are different songs. The previous segment has been stored in the ``last_song_*`` variables and can be retrieved using [``get_last_song``](#get_last_song).
- ``SONG_MISMATCH: 2``: The current song segment is recognised as a different song in the beginning and end. This happens if the segmentation algorithm didn't detect a change of songs. To solve this, the front-end should prompt the user to manually place the missing split. The previous segment has been stored in the ``last_song_*`` variables and can be retrieved using [``get_last_song``](#get_last_song).
- ``SONG_NOT_RECOGNISED: 3``: The current song segment couldn't be recognised. This happens if none of the song recognition APIs the user provided API keys for know the given song. The previous segment has been stored in the ``last_song_*`` variables and can be retrieved using [``get_last_song``](#get_last_song).

### ApiService

The ApiService class contains the business logic for retrieving song metadata via various song identification APIs.

The currently analyzed song is stored in the ``current_song_*`` attributes, formatted as an offset and a duration to indicate its position in the analyzed file and the metadata options for the song, as gathered from the song recognition APIs. Once a new segment's metadata doesn't match the currently analyzed song, the current song is stored in the ``last_song_*`` attributes and can be retrieved using [``get_last_song``](#get_last_song).

The workflow of using the API service, as implemented in [``identify_all_from_generator``](#identify_all_from_generator), should look as follows:

```python
import modules.api_service

segments = [(0, 160), (160, 90), (250, 110.4)] # the segment data - this will usually come from segmentation.py
filename = "my_file.mp3" # the target file
service = ApiService()
result_segments = []
first_segment = True
for offset, duration in segments:
  result = service.get_song_options(offset, duration, filename)
  if (result is SongOptionResult.SONG_FINISHED or SongOptionResult.SONG_NOT_RECOGNISED and first_segment = False) or result is SongOptionResult.SONG_MISMATCH:
    result_segments.append(service.get_last_song())
  if (result is not SongOptionResult.SONG_EXTENDED)
    first_segment = False
result_segments.append(service.get_final_song())
print(result_segments)
```

The condition involving ``first_segment`` is required as the service is initialised with placeholder values, which are written to the ``last_song_*`` attributes the first time a segment is passed in.

#### ApiService:Contents

Attributes:

- [``last_song_offset``](#apiservicelast_song_offset)
- [``last_song_duration``](#apiservicelast_song_duration)
- [``last_song_metadata_options``](#apiservicelast_song_metadata_options)
- [``current_song_offset``](#apiservicecurrent_song_offset)
- [``current_song_duration``](#apiservicecurrent_song_duration)
- [``current_song_metadata_options``](#apiservicecurrent_song_metadata_options)

Public functions:

- [``identify_all_from_generator``](#identify_all_from_generator)
- [``get_last_song``](#get_last_song)
- [``get_final_song``](#get_final_song)
- [``get_song_options``](#get_song_options)

Private functions:

- [``_song_export``](#_song_export)
- [``_check_song_extended_or_finished``](#_check_song_extended_or_finished)
- [``_get_overlapping_metadata_values``](#_get_overlapping_metadata_values)
- [``_create_fingerprint``](#_create_fingerprint)
- [``_get_api_song_data_acoustid``](#_get_api_song_data_acoustid)
- [``_store_finished_song``](#_store_finished_song)

#### ApiService:Attributes

##### ApiService.last_song_offset

``float`` Offset of the last finished segment. This is always >= 0 and smaller than the analyzed file's duration.

##### ApiService.last_song_duration

``float`` Duration of the last finished segment. This is always > 0 and smaller than the analyzed file's duration minus ``last_song_offset``.

##### ApiService.last_song_metadata_options

``dict`` Metadata options for the last finished segment. This can contain attributes for the song's title, artist, album and year.

``title`` and ``artist`` must always be set. ``album`` and ``year`` will not be set if the service didn't offer them.

Example:

```python
{
  "title": "Thunderstruck",
  "artist": "AC/DC",
  "album": "The Razor's Edge",
  "year": "1990"
}
```

##### ApiService.current_song_offset

Offset of the currently analyzed segment. This is always >= 0 and smaller than the analyzed file's duration. If segments are properly provided in sequence, ``current_song_offset == last_song_offset + last_song_duration`` will always be true.

##### ApiService.current_song_duration

Duration of the currently analyzed segment. This is always > 0 and smaller than the analyzed file's duration minus ``current_song_offset``.

##### ApiService.current_song_metadata_options

``dict`` Metadata options for the currently analyzed segment. This can contain attributes for the song's title, artist, album and year.

``title`` and ``artist`` must always be set. ``album`` and ``year`` will not be set if the service didn't offer them.

Example:

```python
{
  "title": "Thunderstruck",
  "artist": "AC/DC",
  "album": "The Razor's Edge",
  "year": "1990"
}
```

#### ApiService:Public functions

##### identify_all_from_generator

Identify all song segments provided by a generator, which should be created by ``modules/segmentation.py``.

This function will iterate over every segment the generator provides and call ``get_song_options`` with its parameters. Whenever a song is not extended, the result is written to the ``segments`` list. If ``get_song_options`` returns [``SongOptionResult.SONG_MISMATCH``](#songoptionresult), the segment's offset is additionally written to the ``mismatch_offsets`` list.

###### identify_all_from_generator:Arguments

- ``generator: Generator``: A generator (generated by ``modules/segmentation.py``) that provides tuples of song data as ``(offset: float, duration: float)``. The first provided tuple is only left for historic reasons and should be refactored out eventually.
- ``file_path: str``: The path to the analysed file. This needs to be properly formatted for the operating system this program is running in, so using ``\`` for Windows and ``/`` for \*nix systems.

###### identify_all_from_generator:Returns

Tuple ``(segments, mismatch_offsets)``.

- ``segments``: A list containing all the identified segments, formatted as a ``dict`` with the keys ``offset`` for the segment start, ``duration`` for the segment duration and ``metadataOptions`` for the metadata options.
- ``mismatch_offsets`` contains all ``offset`` values from ``segments`` where [``SongOptionResult.SONG_MISMATCH``](#songoptionresult) occurred.

###### identify_all_from_generator:Example

Example: Simply segment a file and identify all segments.

```python
import modules.segmentation
import modules.api_service

api_service = ApiService()
generator = segment_file("my_file.mp3")
segments, mismatches = api_service.identify_all_from_generator(generator, "my_file.mp3")
print("Segments:")
print(segments)
print("Mismatches:")
print(mismatches)
```

##### get_last_song

Retrieve a finished song. This should be called whenever [``get_song_options``](#get_song_options) returns [``SongOptionResult.SONG_FINISHED``](#songoptionresult), except for the first time (as it will then contain empty metadata).

###### get_last_song:Arguments

###### get_last_song:Returns

A ``dict`` with the keys ``offset`` for the segment start, ``duration`` for the segment duration and ``metadataOptions`` for the metadata options.

Example:

```python
{
  "offset": 195.2
  "duration": 170
  "metadataOptions": [
    {
      "title": "Thunderstruck",
      "artist": "AC/DC",
      "album": "The Razor's Edge",
      "year": "1990"
    },
    {
      "title": "Thunderstruck",
      "artist": "2Cellos"
    }
  ]
}
```

##### get_final_song

Retrieve the final song. This should be called after calling [``get_song_options``](#get_song_options) for the last time for a file. This should be the very last call to an ``ApiService`` instance.

###### get_final_song:Arguments

###### get_final_song:Returns

A ``dict`` with the keys ``offset`` for the segment start, ``duration`` for the segment duration and ``metadataOptions`` for the metadata options.

Example:

```python
{
  "offset": 195.2
  "duration": 170
  "metadataOptions": [
    {
      "title": "Thunderstruck",
      "artist": "AC/DC",
      "album": "The Razor's Edge",
      "year": "1990"
    },
    {
      "title": "Thunderstruck",
      "artist": "2Cellos"
    }
  ]
}
```

##### get_song_options

Call the song recognition APIs the user has provided an API key for and attempt to identify the given segment of the given file.

If keys for multiple song recognition APIs are provided, AcoustID is queried first as it is fully free. Thus, if AcoustID can identify a song, limited or costly requests to other services can be saved for songs AcoustID cannot identify. The order of other API calls, if more song recognition APIs besides AcoustID and Shazam are added, is irrelevant, although it would be best practice to order them by cost per request so as to limit fees for users.

The check for whether the given segment matches the currently analyzed song, as implemented in [``_get_overlapping_metadata_values``](#_get_overlapping_metadata_values) only accounts for song title and artist. If other metadata differ, the currently analyzed song's metadata are used.

###### get_song_options:Arguments

- ``offset: float``: The offset at which the segment begins, in seconds.
- ``duration: float``: The duration of the segment, in seconds.
- ``file_path: str``: The path to the analyzed file. This needs to be properly formatted for the operating system this program is running in, so using ``\`` for Windows and ``/`` for \*nix systems.

###### get_song_options:Returns

[``SongOptionResult``](#songoptionresult) indicating the new state of the service.

#### ApiService:Private functions

While these functions aren't "private" in the sense that they cannot be accessed from the outside, they should not be called from outside this file.

##### _song_export

Format the given offset, duration and metadata as a dict for the API. This is used for formatting for [``get_last_song``](#get_last_song) and [``get_final_song``](#get_final_song).

###### _song_export:Arguments

- ``offset: float``: The offset at which the segment begins, in seconds.
- ``duration: float``: The duration of the segment, in seconds.
- ``metadata_options: list``: A list of the metadata options, formatted as dicts.

###### _song_export:Returns

A ``dict`` with the keys ``offset`` for the segment start, ``duration`` for the segment duration and ``metadataOptions`` for the metadata options.

Example:

```python
{
  "offset": 195.2
  "duration": 170
  "metadataOptions": [
    {
      "title": "Thunderstruck",
      "artist": "AC/DC",
      "album": "The Razor's Edge",
      "year": "1990"
    },
    {
      "title": "Thunderstruck",
      "artist": "2Cellos"
    }
  ]
}
```

##### _check_song_extended_or_finished

Check if the metadata options of the analyzed segment match those of the previous segment. Store the finished song if applicable.

The check for whether the given segment matches the currently analyzed song, as implemented in [``_get_overlapping_metadata_values``](#_get_overlapping_metadata_values) only accounts for song title and artist. If other metadata differ, the currently analyzed song's metadata are used.

###### _check_song_extended_or_finished:Arguments

- ``offset: float``: The offset at which the analyzed segment begins, in seconds.
- ``duration: float``: The duration of the analyzed segment, in seconds.
- ``metadata_options: list``: A list of the metadata options for the analyzed segment, formatted as dicts.

###### _check_song_extended_or_finished:Returns

[``SongOptionResult``](#songoptionresult) indicating whether the previous segment was extended or finished.

##### _get_overlapping_metadata_values

From two sets of metadata, get all that have the same artist and title. If either of the sets is empty, return the other set.

If metadata other than artist and title mismatch, the metadata from ``metadata1`` are used, even if that means discarding data that is empty in ``metadata1`` and set in ``metadata2``.

###### _get_overlapping_metadata_values:Arguments

- ``metadata1: list``: First list of metadata to compare.
- ``metadata2: list``: Second list of metadata to compare.

###### _get_overlapping_metadata_values:Returns

A ``list`` of the matching metadata options.

Example:

```python
[
  {
      "title": "Thunderstruck",
      "artist": "AC/DC",
      "album": "The Razor's Edge",
      "year": "1990"
    },
    {
      "title": "Thunderstruck",
      "artist": "2Cellos"
    }
]
```

##### _create_fingerprint

Create a [chromaprint/AcoustID](https://github.com/acoustid/chromaprint) fingerprint for the given audio data in order to identify it using [AcoustID](https://acoustid.org).

As of current, this works by writing the data to a temporary file and using the ``fpcalc`` command line tool to generate the fingerprint. The temporary file is deleted immediately afterwards. If it becomes feasible to build and distribute DLL versions of ``chromaprint`` for all target platforms, this should be refactored to use that instead.

###### _create_fingerprint:Arguments

- ``song_data: numpy.ndarray`` The song data to generate a fingerprint from.
- ``samplerate: int`` The sample rate of the song data.

###### _create_fingerprint:Returns

Tuple ``(song_duration, fingerprint)``. The ``song_duration`` is measured in seconds and used for the API call to AcoustID. The ``fingerprint`` is generated by ``fpcalc``.

##### _get_api_song_data_acoustid

Get data about the provided fingerprint from the [AcoustID](https://acoustid.org) API.

This uses the ``pyacoustid`` library as a wrapper, which will only return the song's title and artist, as well as a match score and the MusicBrainz ID, although those are discarded as they have no further use. This should be enhanced to include a second call to the AcoustID API that gathers more metadata for the song using the MusizcBrainz ID.

###### _get_api_song_data_acoustid:Arguments

- ``fingerprint: str`` The fingerprint generated using [``create_fingerprint``](#_create_fingerprint) or other usage of [chromaprint](https://github.com/acoustid/chromaprint).
- ``fingerprint_duration: float`` The duration of the fingerprinted data, in seconds.

###### _get_api_song_data_acoustid:Returns

A ``list`` of ``dict``s containing the results. The ``dict``s have the keys ``"artist"`` for the artist name and ``"title"`` for the song title.

Example:

```python
[
  {
      "title": "Thunderstruck",
      "artist": "AC/DC",
    },
    {
      "title": "Thunderstruck",
      "artist": "2Cellos"
    }
]
```

##### _store_finished_song

Store the data from the ``current_song_*`` variables in the ``last_song_*`` variables and replace the ``current_song_*`` variables with the provided data. This is used to correctly change the service's state in [``get_song_options``](#get_song_options) and functions called by it.

###### _store_finished_song:Arguments

- ``offset: float``: The new currently read song's offset, in seconds.
- ``duration: float``: The new currently read song's duration, in seconds.
- ``metadata_options: dict``: The new currently read song's metadata options.

###### _store_finished_song:Returns
