import os
from enum import Enum
from typing import Generator

import acoustid
from acoustid import FingerprintGenerationError, NoBackendError, WebServiceError
from utils.env import get_env
from utils.logger import log_error

from .apis.shazam import lookup as shazam_lookup
from .audio_stream_io import read_audio_file_to_numpy, save_numpy_as_audio_file


class SongOptionResult(Enum):
    """`SongOptionResult` contains information about the state of the API service.
    This is returned after analyzing a new song segment.

    The following four states can occur:

    - `SONG_EXTENDED`: The previous and current song segments are the same song.
        This happens if the segmentation algorithm split a song in the middle.
        The previous segment has been extended to include the current one.
    - `SONG_FINISHED`: The previous and current song segments are different songs.
        The previous segment has been stored in the last_song_* variables
        and can be retrieved using `ApiService.get_last_song()`.
    - `SONG_MISMATCH`: The current song segment is a different song in the beginning and end.
        This happens if the segmentation algorithm didn't detect a change of songs.
        To solve this, the front-end should prompt the user to manually place the missing split.
        The previous segment has been stored in the last_song_* variables
        and can be retrieved using `ApiService.get_last_song()`.
    - `SONG_NOT_RECOGNISED`: The current song segment couldn't be recognised.
        This happens if none of the song recognition APIs the user provided API keys for
        know the given song.
        The previous segment has been stored in the last_song_* variables
        and can be retrieved using `ApiService.get_last_song()`.
    """

    SONG_EXTENDED = 0  # previous song extended by current song
    SONG_FINISHED = 1  # previous song finished, new song started
    SONG_MISMATCH = 2  # start and end of song are different songs
    SONG_NOT_RECOGNISED = 3  # analysed song has no results from the API.


"""
Constant defining empty metadata options.
"""
EMPTY_METADATA_OPTIONS = [
    {
        "title": "not-set",
        "album": "not-set",
        "artist": "not-set",
        "year": "not-set",
    }
]

"""
Constant defining the standard sample rate of 44100Hz.
Songs must be loaded at this sample rate for the Shazam API to work.
"""
SAMPLE_RATE_STANDARD = 44100


class ApiService:
    """The `ApiService` class contains the business logic for retrieving song metadata
    via various song identification APIs.

    The currently analyzed song is stored in the current_song_* attributes,
    formatted as an offset and a duration to indicate its position in the analyzed file
    and the metadata options for the song, as gathered from the song recognition APIs.
    Once a new segment's metadata doesn't match the currently analyzed song,
    the current song is stored in the last_song_* attributes
    and can be retrieved using `get_last_song`.

    The workflow of using the API service, as implemented in `identify_all_from_generator`
    should look as follows:
    ``
    import modules.api_service

    segments = [(0, 160), (160, 90), (250, 110.4)] # the segment data
    filename = "my_file.mp3" # the target file
    service = ApiService()
    result_segments = []
    first_segment = True
    for offset, duration in segments:
      result = service.get_song_options(offset, duration, filename)
      if (
        (
            result is SongOptionResult.SONG_FINISHED or SongOptionResult.SONG_NOT_RECOGNISED
            and first_segment = False
        )
        or result is SongOptionResult.SONG_MISMATCH
        ):
        result_segments.append(service.get_last_song())
      if (result is not SongOptionResult.SONG_EXTENDED)
        first_segment = False
    result_segments.append(service.get_final_song())
    print(result_segments)
    ``

    The condition involving first_segment is required as the service is initialised with placeholder
    values, which are written to the last_song_* attributes the first time a segment is passed in.
    """

    """Offset of the last finished segment.
    This is always >= 0 and smaller than the analyzed file's duration.
    """
    last_song_offset = 0
    """Duration of the last finished segment.
    This is always > 0 and smaller than the analyzed file's duration minus `last_song_offset`.
    """
    last_song_duration = 0
    """Metadata options for the last finished segment.
    This can contain attributes for the song's title, artist, album and year.
    "title" and "artist" must always be set.
    "album" and "year" will not be set if the service didn't offer them.

    Format example:
    ``
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
    ``
    """
    last_song_metadata_options = EMPTY_METADATA_OPTIONS
    """Offset of the currently analyzed segment.
    This is always >= 0 and smaller than the analyzed file's duration.
    If segments are properly provided in sequence,
    `current_song_offset` == `last_song_offset` + `last_song_duration` will always be true.
    """
    current_song_offset = 0
    """Duration of the currently analyzed segment.
    This is always > 0 and smaller than the analyzed file's duration minus `current_song_offset`.
    """
    current_song_duration = 0
    """Metadata options for the currently analyzed segment.
    This can contain attributes for the song's title, artist, album and year.
    "title" and "artist" must always be set.
    "album" and "year" will not be set if the service didn't offer them.

    Format example:
    ``
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
    ``
    """
    current_song_metadata_options = EMPTY_METADATA_OPTIONS

    def identify_all_from_generator(
        self, generator: Generator[tuple, float, float], file_path: (str, str)
    ):
        """Identify all song segments provided by a generator,
        which should be created by `modules.segmentation`.
        This function will iterate over every segment the generator provides
        and call `get_song_options` with its parameters.
        Whenever a song is not extended, the result is written to the segments list.
        If `get_song_options` returns `SongOptionResult`.`SONG_MISMATCH`,
        the segment's offset is additionally written to the mismatch_offsets list.
        :param generator: A generator (returned by `modules.segmentation`) that provides tuples of
            song data as (offset: float, duration: float).
        :param file_path: The path to the analyzed file.
        :returns: (segments, mismatches)
            - segments: A list containing all the identified segments,
                formatted as a dict with the keys "offset" for the segment start,
                "duration" for the segment duration and "metadataOptions" for the metadata options.
            - mismatch_offsets: A list containing all "offset" values from "segments"
                where `SongOptionResult`.`SONG_MISMATCH` occurred.
        :raise `requests.exceptions.RequestException`: if a Shazam request fails
            due to too many redirections or other problems.
            ConnectionErrors are caught within the function, but other errors are not.
            A detailed list of Exceptions `requests` can raise can be found at https://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions
        """
        is_first_segment = True
        segments = []
        mismatch_offsets = []
        for start, duration in generator:
            result = self.get_song_options(start, duration, file_path)
            if (
                result
                in [
                    SongOptionResult.SONG_FINISHED,
                    SongOptionResult.SONG_NOT_RECOGNISED,
                ]
            ) and not is_first_segment:
                segments.append(self.get_last_song())
            elif result == SongOptionResult.SONG_MISMATCH:
                segments.append(self.get_last_song())
                mismatch_offsets.append(start)
            if result != SongOptionResult.SONG_EXTENDED:
                is_first_segment = False
        segments.append(self.get_final_song())
        return (segments, mismatch_offsets)

    def get_last_song(self):
        """Get a fully analyzed song with all its metadata options.
        This should be called after a song is finished, except for the first time
        (as it will then contain empty metadata).
        :returns: A dict with the keys "offset" for the segment start,
            "duration" for the segment duration and "metadataOptions" for the metadata options.
        Example:
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
        """
        return self._song_export(
            self.last_song_offset,
            self.last_song_duration,
            self.last_song_metadata_options,
        )

    def get_final_song(self):
        """Retrieve the final song.
        This should be called after calling `get_song_options` for the last time for a file.
        This should be the very last call to an ApiService instance.
        :returns: A dict with the keys "offset" for the segment start,
            "duration" for the segment duration and "metadataOptions" for the metadata options.
        Example:
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
        """
        result = self._song_export(
            self.current_song_offset,
            self.current_song_duration,
            self.current_song_metadata_options,
        )
        return result

    def _song_export(self, offset, duration, metadata_options):
        """Format the given offset, duration and metadata as a dict for the API.
        This is used for formatting for `get_last_song` and `get_final_song`.
        :param offset: The offset at which the segment begins, in seconds.
        :param duration: The duration of the segment, in seconds.
        :param metadata_options: A list of the metadata options, formatted as dicts.
        :returns: A dict with the keys "offset" for the segment start,
            "duration" for the segment duration and "metadataOptions" for the metadata options.
        Example:
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
        """
        return {
            "offset": offset,
            "duration": duration,
            "metadataOptions": metadata_options,
        }

    def get_song_options(self, offset: float, duration: float, file_path: str):
        """Call the song recognition APIs the user has provided an API key for
        and attempt to identify the given segment of the given file.
        If keys for multiple song recognition APIs are provided,
        AcoustID is queried first as it is fully free. Thus, if AcoustID can identify a song,
        costly requests to other services can be saved for songs AcoustID cannot identify.
        The order of other API calls, if more song recognition APIs besides AcoustID and Shazam are
        added, is irrelevant, although it would be best practice to order them by cost per request
        so as to limit fees for users.
        :param offset: The offset at which the segment begins, in seconds.
        :param duration: The duration of the segment, in seconds.
        :param file_path: The path to the analyzed file.
        :returns: `SongOptionResult` indicating the new state of the service.
        :raise `requests.exceptions.RequestException`: if a Shazam request fails
            due to too many redirections or other problems.
            ConnectionErrors are caught within the function, but other errors are not.
            A detailed list of Exceptions requests can raise can be found at https://docs.python-requests.org/en/latest/user/quickstart/#errors-and-exceptions
        """
        sample_rate = SAMPLE_RATE_STANDARD
        song_data, sample_rate = read_audio_file_to_numpy(
            file_path,
            mono=False,
            offset=offset,
            duration=duration,
            sample_rate=sample_rate,
        )

        ACOUSTID_API_KEY = get_env("SERVICE_ACOUSTID_API_KEY")
        SHAZAM_API_KEY = get_env("SERVICE_SHAZAM_API_KEY")

        # first check using acoustID
        if ACOUSTID_API_KEY is not None:
            try:
                duration, fingerprint = self._create_fingerprint(song_data, sample_rate)
                metadata = self._get_api_song_data_acoustid(fingerprint, duration)
                if len(metadata) != 0:
                    return self._check_song_extended_or_finished(
                        offset, duration, metadata
                    )
            except NoBackendError as ex:
                log_error(ex, "No fpcalc/chromaprint found")
            except FingerprintGenerationError as ex:
                log_error(ex, "AcoustID fingerprinting")
            except WebServiceError as ex:
                log_error(ex, "AcoustID request")

        # if acoustID doesn't find anything, try shazam
        # If sample_rate inexplicably becomes something other than 44100Hz, shazam won't work
        if SHAZAM_API_KEY is not None and sample_rate == SAMPLE_RATE_STANDARD:
            try:
                metadata_start = shazam_lookup(song_data, SHAZAM_API_KEY, True)
                metadata_end = shazam_lookup(song_data, SHAZAM_API_KEY, False)
                metadata_start = [metadata_start] if metadata_start is not None else []
                metadata_end = [metadata_end] if metadata_end is not None else []

                shazam_metadata_options = self._get_overlapping_metadata_values(
                    metadata_start, metadata_end
                )
                if len(shazam_metadata_options) != 0:
                    return self._check_song_extended_or_finished(
                        offset, duration, shazam_metadata_options
                    )
                elif len(metadata_start) != 0 and len(metadata_end) != 0:
                    self._store_finished_song(offset, duration, ())
                    return SongOptionResult.SONG_MISMATCH
            except ConnectionError as ex:
                log_error(ex, "Shazam connection error")

            # if neither finds anything, song not recognised.
            self._store_finished_song(offset, duration, ())
        return SongOptionResult.SONG_NOT_RECOGNISED

    def _check_song_extended_or_finished(
        self, offset: float, duration: float, metadata_options
    ):
        """Check if metadata options of the analyzed segment match those of the previous segment.
        Store the finished song if applicable.
        :param offset: The offset at which the segment begins, in seconds.
        :param duration: The duration of the segment, in seconds.
        :param metadata_options: A list of the metadata options for the analyzed segment as dicts.
        :returns: `SongOptionResult` indicating if the previous segment was extended or finished.
        """
        match_metadata_options = self._get_overlapping_metadata_values(
            self.current_song_metadata_options, metadata_options
        )

        if len(match_metadata_options) == 0:
            self._store_finished_song(
                offset=offset, duration=duration, metadata_options=metadata_options
            )
            return SongOptionResult.SONG_FINISHED
        else:
            self.current_song_metadata_options = match_metadata_options
            self.current_song_duration += duration
            return SongOptionResult.SONG_EXTENDED

    def _get_overlapping_metadata_values(self, metadata1, metadata2):
        """From two lists of metadata, get all that have the same artist and title.
        If either of the lists is empty, return the other list.
        If metadata other than artist and title mismatch, the metadata from metadata1 are used,
        even if that means discarding data that is empty in metadata1 and set in metadata2.
        :param metadata1: first list of metadata to compare.
        :param metadata2: second list of metadata to compare.
        :returns: a list of the matching metadata options.
        Example:
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
        """
        if len(metadata1) == 0:
            return metadata2
        elif len(metadata2) == 0:
            return metadata1
        else:
            overlapping_metadata = []
            titles2 = [d["title"] for d in metadata2]
            artists2 = [d["artist"] for d in metadata2]
            for metadata in metadata1:
                if metadata["title"] in titles2 and metadata["artist"] in artists2:
                    overlapping_metadata.append(metadata)
            return overlapping_metadata

    def _create_fingerprint(self, song_data, samplerate):
        """Create a chromaprint/AcoustID fingerprint for the given audio data
        in order to identify it using AcoustID.
        As of current, this works by writing the data to a temporary file
        and using the fpcalc command line tool to generate the fingerprint.
        The temporary file is deleted immediately afterwards.
        TODO: If it becomes feasible to build and distribute DLL versions of chromaprint
        for all target platforms, this should be refactored to use that instead.
        :param song_data: the audio data to generate a fingerprint from.
        :param samplerate: the audio data's sample rate.
        :returns: (song_duration, fingerprint).
            - song_duration is measured in seconds and used for the API call to AcoustID.
            - fingerprint is generated by fpcalc.
        :raise `acoustid.NoBackendError`: if fpcalc is not installed.
        :raise `acoustid.FingerprintGenerationError`: if fingerprint generation fails.
        """
        filename = "TEMP_FILE_FOR_FINGERPRINTING"
        save_numpy_as_audio_file(
            song_data, os.path.abspath(filename), "", rate=samplerate
        )

        filename_with_path = os.path.abspath(filename + ".mp3")
        fingerprint_duration, fingerprint = acoustid.fingerprint_file(
            filename_with_path, force_fpcalc=True
        )
        os.remove(filename_with_path)
        return (fingerprint_duration, fingerprint)

    def _get_api_song_data_acoustid(self, fingerprint, fingerprint_duration):
        """Get data about the provided fingerprint from the AcoustID API.
        This uses the `pyacoustid` library as a wrapper, which will only return the song's title
        and artist, as well as a match score and the MusicBrainz ID,
        although those are discarded as they have no further use.
        TODO: This should be enhanced to include a second call to the AcoustID API
        that gathers more metadata for the song using the MusicBrainz ID.
        :param fingerprint: the fingerprint generated using `_create_fingerprint`.
        :param fingerprint_duration: duration of the fingerprinted data, in seconds.
        :returns: A list of dicts containing the results.
        :raise `acoustid.WebServiceError`: if the request fails.
            The dicts have the keys "artist" for the artist name and "title" for the song title.
        Example:
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
        """
        ACOUSTID_API_KEY = get_env("SERVICE_ACOUSTID_API_KEY")

        try:
            result = []
            for score, recording_id, title, artist in acoustid.parse_lookup_result(
                acoustid.lookup(ACOUSTID_API_KEY, fingerprint, fingerprint_duration)
            ):
                if (
                    title is not None
                    and artist is not None
                    and {"title": title, "artist": artist} not in result
                ):
                    result.append({"title": title, "artist": artist})
            return result
        except acoustid.WebServiceError:
            return []

    def _store_finished_song(self, offset: float, duration: float, metadata_options):
        """Store the current (finished) data in the last_song_* variables.
        Store the provided data in the current_song_* variables.
        This is used to correctly change the service's state in `get_song_options`.
        :param offset: The new currently read song's offset, in seconds.
        :param duration: The new currently read song's duration, in seconds.
        :param metadata_options: The new currently read song's metadata options.
        """

        self.last_song_offset = self.current_song_offset
        self.last_song_duration = self.current_song_duration
        self.last_song_metadata_options = self.current_song_metadata_options
        self.current_song_offset = offset
        self.current_song_duration = duration
        self.current_song_metadata_options = metadata_options
