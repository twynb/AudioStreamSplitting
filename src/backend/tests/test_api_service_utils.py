from unittest.mock import patch

from modules.api_service import (
    SongOptionResult,
    _check_song_extended_or_finished,
    _get_overlapping_metadata_values,
    _song_export,
    _store_finished_song,
    get_final_song,
    get_last_song,
    reset_service_state,
)

# main API functions can't be tested because they depend on external APIs. test utils though.

TEST_EMPTY_METADATA_OPTIONS = [
    {
        "title": "not-set",
        "album": "not-set",
        "artist": "not-set",
        "year": "not-set",
    }
]

LAST_METADATA_OPTIONS_ONE_OVERLAP = [
    {
        "title": "The very matching track",
        "artist": "Matcha Artist",
        "album": "The album doesn't matter",
        "year": 1999,
    },
    {
        "title": "Well it isn't this",
        "artist": "Not the right one",
        "album": "It really doesn't",
        "year": 2040,
    },
]
CURRENT_METADATA_OPTIONS_ONE_OVERLAP = [
    {
        "title": "The very matching track",
        "artist": "Matcha Artist",
        "album": "It really doesn't",
        "year": 2040,
    },
    {
        "title": "Title *and* artist have to match!",
        "artist": "Not the right one",
        "album": "The album doesn't matter",
        "year": 1999,
    },
]

LAST_METADATA_OPTIONS_TWO_OVERLAPS = [
    {
        "title": "The very matching track",
        "artist": "Matcha Artist",
        "album": "The album doesn't matter",
        "year": 1999,
    },
    {
        "title": "Well it isn't this",
        "artist": "Not the right one",
        "album": "It really doesn't",
        "year": 2040,
    },
    {"title": "This one matches too", "artist": "Another one"},
]
CURRENT_METADATA_OPTIONS_TWO_OVERLAPS = [
    {"title": "This one matches too", "artist": "Another one"},
    {
        "title": "The very matching track",
        "artist": "Matcha Artist",
        "album": "It really doesn't",
        "year": 2040,
    },
    {
        "title": "Title *and* artist have to match!",
        "artist": "Not the right one",
        "album": "The album doesn't matter",
        "year": 1999,
    },
]


LAST_OFFSET = 54.2
LAST_DURATION = 189.6
LAST_METADATA_OPTIONS_NO_OVERLAP = [
    {"title": "The very last song", "artist": "The last singer", "year": 1999},
    {
        "title": "The even laster song",
        "artist": "I think, haven't checked",
        "year": 2000,
    },
]
CURRENT_OFFSET = 99.12
CURRENT_DURATION = 999
CURRENT_METADATA_OPTIONS_NO_OVERLAP = [
    {"title": "long long song", "artist": "long long john", "year": 2000}
]

@patch("modules.api_service.last_song_offset", LAST_OFFSET)
@patch("modules.api_service.current_song_offset", CURRENT_OFFSET)
@patch("modules.api_service.last_song_duration", LAST_DURATION)
@patch("modules.api_service.current_song_duration", CURRENT_DURATION)
@patch(
    "modules.api_service.last_song_metadata_options", LAST_METADATA_OPTIONS_NO_OVERLAP
)
@patch(
    "modules.api_service.current_song_metadata_options",
    CURRENT_METADATA_OPTIONS_NO_OVERLAP,
)
def test_get_last_and_final_song():
    assert get_last_song() == {
        "offset": LAST_OFFSET,
        "duration": LAST_DURATION,
        "metadataOptions": LAST_METADATA_OPTIONS_NO_OVERLAP,
    }
    assert get_final_song() == {
        "offset": CURRENT_OFFSET,
        "duration": CURRENT_DURATION,
        "metadataOptions": CURRENT_METADATA_OPTIONS_NO_OVERLAP,
    }


def test_song_export_no_metadata():
    assert _song_export(100, 439.2, []) == {
        "offset": 100,
        "duration": 439.2,
        "metadataOptions": [],
    }


def test_song_export_one_metadata():
    assert _song_export(
        100, 439.2, [{"title": "My Metadata Title", "artist": "Artsy Art Artist"}]
    ) == {
        "offset": 100,
        "duration": 439.2,
        "metadataOptions": [
            {"title": "My Metadata Title", "artist": "Artsy Art Artist"}
        ],
    }


def test_song_export_several_metadata():
    assert _song_export(
        100,
        439.2,
        [
            {"title": "Metaing some Data", "artist": "Data of the meta"},
            {"title": "tfw ur metaing data", "artist": "Met a data once"},
        ],
    ) == {
        "offset": 100,
        "duration": 439.2,
        "metadataOptions": [
            {"title": "Metaing some Data", "artist": "Data of the meta"},
            {"title": "tfw ur metaing data", "artist": "Met a data once"},
        ],
    }


@patch("modules.api_service.current_song_offset", LAST_OFFSET)
@patch("modules.api_service.current_song_duration", LAST_DURATION)
@patch(
    "modules.api_service.current_song_metadata_options",
    LAST_METADATA_OPTIONS_NO_OVERLAP,
)
def test_check_song_extended_or_finished_no_overlaps():
    assert (
        _check_song_extended_or_finished(
            CURRENT_OFFSET, CURRENT_DURATION, CURRENT_METADATA_OPTIONS_NO_OVERLAP
        )
        == SongOptionResult.SONG_FINISHED
    )
    assert get_last_song()["duration"] == LAST_DURATION
    assert get_final_song()["duration"] == CURRENT_DURATION


@patch("modules.api_service.current_song_offset", LAST_OFFSET)
@patch("modules.api_service.current_song_duration", LAST_DURATION)
@patch(
    "modules.api_service.current_song_metadata_options",
    LAST_METADATA_OPTIONS_ONE_OVERLAP,
)
def test_check_song_extended_or_finished_one_overlap():
    assert (
        _check_song_extended_or_finished(
            CURRENT_OFFSET, CURRENT_DURATION, CURRENT_METADATA_OPTIONS_ONE_OVERLAP
        )
        == SongOptionResult.SONG_EXTENDED
    )
    assert get_final_song() == {
        "offset": LAST_OFFSET,
        "duration": CURRENT_DURATION + LAST_DURATION,
        "metadataOptions": [
            {
                "title": "The very matching track",
                "artist": "Matcha Artist",
                "album": "The album doesn't matter",
                "year": 1999,
            }
        ],
    }


@patch("modules.api_service.current_song_offset", LAST_OFFSET)
@patch("modules.api_service.current_song_duration", LAST_DURATION)
@patch(
    "modules.api_service.current_song_metadata_options",
    LAST_METADATA_OPTIONS_TWO_OVERLAPS,
)
def test_check_song_extended_or_finished_two_overlaps():
    assert (
        _check_song_extended_or_finished(
            CURRENT_OFFSET, CURRENT_DURATION, CURRENT_METADATA_OPTIONS_TWO_OVERLAPS
        )
        == SongOptionResult.SONG_EXTENDED
    )
    assert get_final_song() == {
        "offset": LAST_OFFSET,
        "duration": CURRENT_DURATION + LAST_DURATION,
        "metadataOptions": [
            {
                "title": "The very matching track",
                "artist": "Matcha Artist",
                "album": "The album doesn't matter",
                "year": 1999,
            },
            {"title": "This one matches too", "artist": "Another one"},
        ],
    }


@patch("modules.api_service.current_song_offset", LAST_OFFSET)
@patch("modules.api_service.current_song_duration", LAST_DURATION)
@patch("modules.api_service.current_song_metadata_options", [])
def test_check_song_extended_or_finished_previous_is_empty():
    assert (
        _check_song_extended_or_finished(
            CURRENT_OFFSET, CURRENT_DURATION, CURRENT_METADATA_OPTIONS_TWO_OVERLAPS
        )
        == SongOptionResult.SONG_EXTENDED
    )
    assert get_final_song() == {
        "offset": LAST_OFFSET,
        "duration": CURRENT_DURATION + LAST_DURATION,
        "metadataOptions": CURRENT_METADATA_OPTIONS_TWO_OVERLAPS,
    }


# this should not be able to happen with the system as it is
# if current is empty, _check_song_extended_or_finished isn't entered
@patch("modules.api_service.current_song_offset", LAST_OFFSET)
@patch("modules.api_service.current_song_duration", LAST_DURATION)
@patch(
    "modules.api_service.current_song_metadata_options",
    CURRENT_METADATA_OPTIONS_ONE_OVERLAP,
)
def test_check_song_extended_or_finished_current_is_empty():
    assert (
        _check_song_extended_or_finished(CURRENT_OFFSET, CURRENT_DURATION, [])
        == SongOptionResult.SONG_EXTENDED
    )
    assert get_final_song() == {
        "offset": LAST_OFFSET,
        "duration": CURRENT_DURATION + LAST_DURATION,
        "metadataOptions": CURRENT_METADATA_OPTIONS_ONE_OVERLAP,
    }


def test_get_overlapping_metadata_values_no_overlap():
    assert (
        _get_overlapping_metadata_values(
            CURRENT_METADATA_OPTIONS_NO_OVERLAP, LAST_METADATA_OPTIONS_NO_OVERLAP
        )
        == []
    )


def test_get_overlapping_metadata_values_one_overlap():
    assert _get_overlapping_metadata_values(
        CURRENT_METADATA_OPTIONS_ONE_OVERLAP, LAST_METADATA_OPTIONS_ONE_OVERLAP
    ) == [
        {
            "title": "The very matching track",
            "artist": "Matcha Artist",
            "album": "It really doesn't",
            "year": 2040,
        }
    ]


def test_get_overlapping_metadata_values_two_overlaps():
    assert _get_overlapping_metadata_values(
        CURRENT_METADATA_OPTIONS_TWO_OVERLAPS, LAST_METADATA_OPTIONS_TWO_OVERLAPS
    ) == [
        {"title": "This one matches too", "artist": "Another one"},
        {
            "title": "The very matching track",
            "artist": "Matcha Artist",
            "album": "It really doesn't",
            "year": 2040,
        },
    ]


def test_get_overlapping_metadata_values_one_empty():
    assert (
        _get_overlapping_metadata_values([], CURRENT_METADATA_OPTIONS_NO_OVERLAP)
        == CURRENT_METADATA_OPTIONS_NO_OVERLAP
    )
    assert (
        _get_overlapping_metadata_values(LAST_METADATA_OPTIONS_TWO_OVERLAPS, [])
        == LAST_METADATA_OPTIONS_TWO_OVERLAPS
    )


def test_get_overlapping_metadata_values_both_empty():
    assert _get_overlapping_metadata_values([], []) == []


# TODO: test _store_finished_song()
@patch("modules.api_service.last_song_offset", LAST_OFFSET)
@patch("modules.api_service.current_song_offset", CURRENT_OFFSET)
@patch("modules.api_service.last_song_duration", LAST_DURATION)
@patch("modules.api_service.current_song_duration", CURRENT_DURATION)
@patch(
    "modules.api_service.last_song_metadata_options", LAST_METADATA_OPTIONS_NO_OVERLAP
)
@patch(
    "modules.api_service.current_song_metadata_options",
    CURRENT_METADATA_OPTIONS_NO_OVERLAP,
)
def test_store_finished_song():
    assert get_last_song() == {
        "offset": LAST_OFFSET,
        "duration": LAST_DURATION,
        "metadataOptions": LAST_METADATA_OPTIONS_NO_OVERLAP,
    }
    _store_finished_song(140.0, 503.0, [{"title": "mytest", "artist": "notyourtest"}])
    assert get_last_song() == {
        "offset": CURRENT_OFFSET,
        "duration": CURRENT_DURATION,
        "metadataOptions": CURRENT_METADATA_OPTIONS_NO_OVERLAP,
    }
    assert get_final_song() == {
        "offset": 140.0,
        "duration": 503.0,
        "metadataOptions": [{"title": "mytest", "artist": "notyourtest"}],
    }
