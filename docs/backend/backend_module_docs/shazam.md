# Shazam

This class provides functionality to access the [Shazam API](https://rapidapi.com/apidojo/api/shazam) to identify a segment of song data.

Requests are performed using the Python ``requests`` library, so functions sending requests to the Shazam API may throw all exceptions the ``requests`` library can throw.

## Contents

Public functions:

- [``lookup``](#lookup)

Private functions:

- [``_lookup_segment_with_offset``](#_lookup_segment_with_offset)
- [``_format_song_data``](#_format_song_data)
- [``_get_song_data_segment``](#_get_song_data_segment)
- [``_create_payload_from_song_data``](#_create_payload_from_song_data)
- [``_send_lookup_request``](#_send_lookup_request)
- [``_extract_value_from_metadata``](#_extract_value_from_metadata)

## Public functions

### lookup

Attempt to identify the given song using the [Shazam API](https://rapidapi.com/apidojo/api/shazam). If the song can't be recognised from the first segment, step through it until the segment ends or a result is found.

The step size is defined by the ``LOOKUP_OFFSET_INCREMENT`` constant and set to 10 seconds by default. The segment size is defined by the ``LOOKUP_SEGMENTS_DURATION`` constant and set to 4 seconds by default, as the [Shazam API](https://rapidapi.com/apidojo/api/shazam) expects segments between 3 and 5 seconds.

#### lookup:Arguments

- ``song_data: numpy.ndarray``: The song data. The data must be at a sample rate of 44100Hz as the [Shazam API](https://rapidapi.com/apidojo/api/shazam) will not work with other sample rates.
- ``apikey: str``: The Shazam API key.
- ``from_start: bool = True``: Whether to start attempting to identify segments of the given song from the beginning or the ending.

#### lookup:Returns

- If matches are found: The retrieved metadata as a ``dict``, with the keys ``"title"``, ``"artist"``, ``"album"`` and ``"year"`` for the respective metadata.
- ``None`` otherwise.

Example:

```python
{
  "title": "Thunderstruck",
  "artist": "AC/DC",
  "album": "The Razor's Edge",
  "year": "1990"
}
```

#### lookup:Raises

- ``requests.exceptions.RequestException`` if the request fails due to network problems, too many redirections or other problems. A detailed list of Exceptions ``requests``can raise can be found in [the ``requests`` documentation](https://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions)

#### lookup:Example

Load a song and load metadata for it using ``lookup``.

```python
import librosa
import modules.apis.shazam

song, sr = librosa.load("my_cool_file", sr=44100)
result = lookup(song, "MY-SHAZAM-API-KEY")

print(result)
```

## Private functions

While these functions aren't "private" in the sense that they cannot be accessed from the outside, they should not be called from outside this file.

### _lookup_segment_with_offset

Look up a snippet of the given song at the given offset. This function integrates functionality to create the payload required for a request, send the request to the [Shazam API](https://rapidapi.com/apidojo/api/shazam) and process the response.

#### _lookup_segment_with_offset:Arguments

- ``song_data: numpy.ndarray``: The song data. Must be at a sample rate of 44100Hz.
- ``apikey: str``: The API key.
- ``offset: int``: The offset the snippet should start at, in seconds.

#### _lookup_segment_with_offset:Returns

Tuple ``(matches, track)`` of the retrieved metadata, matching the sections of the API response with the same name. The format for the API response can be found using the test functionality on the [Shazam API](https://rapidapi.com/apidojo/api/shazam) website.

#### _lookup_segment_with_offset:Raises

- ``requests.exceptions.RequestException`` if the request fails due to network problems, too many redirections or other problems. A detailed list of Exceptions ``requests``can raise can be found in [the ``requests`` documentation](https://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions)

### _format_song_data

Format the song data as a mono 16-bit integer array, as the [Shazam API](https://rapidapi.com/apidojo/api/shazam) will not work with other formats.

#### _format_song_data:Arguments

- ``song_data: numpy.ndarray``: The song data. This is expected to be formatted as ``float``s between -1 and 1.

#### _format_song_data:Returns

``numpy.ndarray`` containing the formatted data.

### _get_song_data_segment

Extract a segment of the song data at the given offset.

#### _get_song_data_segment:Arguments

- ``song_data: numpy.ndarray``: The song data.
- ``offset: int``: The offset the snippet should start at, in seconds.

#### _get_song_data_segment:Returns

``numpy.ndarray`` containing the extracted segment.

### _create_payload_from_song_data

Create the payload to include with the request in the [Shazam API](https://rapidapi.com/apidojo/api/shazam)'s data format (A base64-encoded byte array). This expects that the song data has been formatted using [``format_song_data``](#_format_song_data) and that the song data is between 3-5 seconds.

#### _create_payload_from_song_data:Arguments

- ``song_data: numpy.ndarray``: The song data, formatted as a mono 16-bit integer array.

#### _create_payload_from_song_data:Returns

``str`` containing the payload.

### _send_lookup_request

Send the actual lookup request to the [Shazam API](https://rapidapi.com/apidojo/api/shazam). This uses the ``requests`` module to send the request and can thus throw all errors a failed ``requests.post()`` can.

#### _send_lookup_request:Arguments

- ``payload: str``: The payload as generated by [``_create_payload_from_song_data``](#_create_payload_from_song_data).
- ``apikey``: The Shazam API key.

#### _send_lookup_request:Returns

``requests.Response`` containing the request response. The format for the API response can be found using the test functionality at the [Shazam API](https://rapidapi.com/apidojo/api/shazam) website.

#### _send_lookup_request:Raises

- ``requests.exceptions.RequestException`` if the request fails due to network problems, too many redirections or other problems. A detailed list of Exceptions ``requests``can raise can be found in [the ``requests`` documentation](https://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions)

### _extract_value_from_metadata

Extract a value from the response's "Metadata" section.

If an error occurs that leads to the "Metadata" section containing two sets of data with the same label, the first set of data is returned.

#### _extract_value_from_metadata:Arguments

- ``track: list``: The "track" segment of the API response.
- ``key: str``: The key to search for in the metadata.

#### _extract_value_from_metadata:Returns

- ``str`` containing the value if it exists.
- Empty ``str`` otherwise.