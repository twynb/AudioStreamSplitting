import acoustid
from modules.apis.acoustid import _extract_recordings, _parse_lookup_result

# TODO: Tests for multiple recording and no album

EXAMPLE_ACOUSTID_RESPONSE = {
    "results": [
        {
            "id": "9ff43b6a-4f16-427c-93c2-92307ca505e0",
            "recordings": [
                {
                    "artists": [
                        {"id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd", "name": "M83"}
                    ],
                    "duration": 638,
                    "id": "cd2e7c47-16f5-46c6-a37c-a1eb7bf599ff",
                    "releasegroups": [
                        {
                            "artists": [
                                {
                                    "id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd",
                                    "name": "M83",
                                }
                            ],
                            "id": "ddaa2d4d-314e-3e7c-b1d0-f6d207f5aa2f",
                            "title": "Before the Dawn Heals Us",
                            "type": "Album",
                        },
                        {
                            "artists": [
                                {
                                    "id": "89ad4ac3-39f7-470e-963a-56509c546377",
                                    "name": "Various Artists",
                                }
                            ],
                            "id": "425771a3-31a4-4dc2-9dee-f2993611b44b",
                            "secondarytypes": ["Compilation"],
                            "title": "Caf\u00e9 del Mar, Volumen Veinte",
                            "type": "Album",
                        },
                        {
                            "artists": [
                                {
                                    "id": "89ad4ac3-39f7-470e-963a-56509c546377",
                                    "name": "Various Artists",
                                }
                            ],
                            "id": "9e585041-f2c1-3f0d-be40-40c845a3323f",
                            "secondarytypes": ["Soundtrack"],
                            "title": "Donkey Punch",
                            "type": "Album",
                        },
                    ],
                    "title": "Lower Your Eyelids to Die With the Sun",
                }
            ],
            "score": 1.0,
        },
        {
            "id": "be6fa248-97d1-4a18-845b-7c6a070b764c",
            "recordings": [
                {
                    "artists": [
                        {"id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd", "name": "M83"}
                    ],
                    "duration": 638,
                    "id": "cd2e7c47-16f5-46c6-a37c-a1eb7bf599ff",
                    "releasegroups": [
                        {
                            "artists": [
                                {
                                    "id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd",
                                    "name": "M83",
                                }
                            ],
                            "id": "ddaa2d4d-314e-3e7c-b1d0-f6d207f5aa2f",
                            "title": "Before the Dawn Heals Us",
                            "type": "Album",
                        },
                        {
                            "artists": [
                                {
                                    "id": "89ad4ac3-39f7-470e-963a-56509c546377",
                                    "name": "Various Artists",
                                }
                            ],
                            "id": "425771a3-31a4-4dc2-9dee-f2993611b44b",
                            "secondarytypes": ["Compilation"],
                            "title": "Caf\u00e9 del Mar, Volumen Veinte",
                            "type": "Album",
                        },
                        {
                            "artists": [
                                {
                                    "id": "89ad4ac3-39f7-470e-963a-56509c546377",
                                    "name": "Various Artists",
                                }
                            ],
                            "id": "9e585041-f2c1-3f0d-be40-40c845a3323f",
                            "secondarytypes": ["Soundtrack"],
                            "title": "Donkey Punch",
                            "type": "Album",
                        },
                    ],
                    "title": "Lower Your Eyelids to Die With the Sun",
                }
            ],
            "score": 1.0,
        },
    ],
    "status": "ok",
}
"""Example response returned by the AcoustID API example request.
The metadata requested was changed to reflect the metadata the actual requests in the
acoustid module.
"""

EXAMPLE_ACOUSTID_RESPONSE_ONE_EMPTY = {
    "results": [
        {
            "id": "9ff43b6a-4f16-427c-93c2-92307ca505e0",
            "recordings": [
                {
                    "artists": [
                        {"id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd", "name": "M83"}
                    ],
                    "duration": 638,
                    "id": "cd2e7c47-16f5-46c6-a37c-a1eb7bf599ff",
                    "releasegroups": [
                        {
                            "artists": [
                                {
                                    "id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd",
                                    "name": "M83",
                                }
                            ],
                            "id": "ddaa2d4d-314e-3e7c-b1d0-f6d207f5aa2f",
                            "title": "Before the Dawn Heals Us",
                            "type": "Album",
                        },
                        {
                            "artists": [
                                {
                                    "id": "89ad4ac3-39f7-470e-963a-56509c546377",
                                    "name": "Various Artists",
                                }
                            ],
                            "id": "425771a3-31a4-4dc2-9dee-f2993611b44b",
                            "secondarytypes": ["Compilation"],
                            "title": "Caf\u00e9 del Mar, Volumen Veinte",
                            "type": "Album",
                        },
                        {
                            "artists": [
                                {
                                    "id": "89ad4ac3-39f7-470e-963a-56509c546377",
                                    "name": "Various Artists",
                                }
                            ],
                            "id": "9e585041-f2c1-3f0d-be40-40c845a3323f",
                            "secondarytypes": ["Soundtrack"],
                            "title": "Donkey Punch",
                            "type": "Album",
                        },
                    ],
                    "title": "Lower Your Eyelids to Die With the Sun",
                }
            ],
            "score": 1.0,
        },
        {
            "id": "be6fa248-97d1-4a18-845b-7c6a070b764c",
            "score": 1.0,
        },
    ],
    "status": "ok",
}
"""Example response returned by the AcoustID API example request.
The metadata requested was changed to reflect the metadata the actual requests in the
acoustid module.
"""


EXAMPLE_ACOUSTID_RESPONSE_MULTIPLE_SONGS = {
    "results": [
        {
            "id": "9ff43b6a-4f16-427c-93c2-92307ca505e0",
            "recordings": [
                {
                    "artists": [
                        {"id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd", "name": "M83"}
                    ],
                    "duration": 638,
                    "id": "cd2e7c47-16f5-46c6-a37c-a1eb7bf599ff",
                    "releasegroups": [
                        {
                            "artists": [
                                {
                                    "id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd",
                                    "name": "M83",
                                }
                            ],
                            "id": "ddaa2d4d-314e-3e7c-b1d0-f6d207f5aa2f",
                            "title": "Before the Dawn Heals Us",
                            "type": "Album",
                        },
                        {
                            "artists": [
                                {
                                    "id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd",
                                    "name": "M83",
                                }
                            ],
                            "secondarytypes": ["Soundtrack"],
                            "id": "425771a3-31a4-4dc2-9dee-f2993611b44b",
                            "title": "A Fake Album",
                            "type": "Album",
                        },
                        {
                            "artists": [
                                {
                                    "id": "89ad4ac3-39f7-470e-963a-56509c546377",
                                    "name": "Various Artists",
                                }
                            ],
                            "id": "9e585041-f2c1-3f0d-be40-40c845a3323f",
                            "secondarytypes": ["Soundtrack"],
                            "title": "Donkey Punch",
                            "type": "Album",
                        },
                    ],
                    "title": "Lower Your Eyelids to Die With the Sun",
                }
            ],
            "score": 1.0,
        },
        {
            "id": "3dfbb248-97d1-4a18-845b-7c6a070b764c",
            "recordings": [
                {
                    "artists": [
                        {
                            "id": "087b7cd4-254b-4c25-83f6-dd20f98ceacd",
                            "name": "My Test Artist",
                        }
                    ],
                    "duration": 638,
                    "id": "dfbddc47-16f5-46c6-a37c-a1eb7bf599ff",
                    "releasegroups": [
                        {
                            "artists": [
                                {
                                    "id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd",
                                    "name": "M83",
                                }
                            ],
                            "id": "ddaa2d4d-314e-3e7c-b1d0-f6d207f5aa2f",
                            "title": "Before the Dawn Heals Us",
                            "type": "Album",
                        },
                        {
                            "artists": [
                                {
                                    "id": "89ad4ac3-39f7-470e-963a-56509c546377",
                                    "name": "Various Artists",
                                }
                            ],
                            "id": "425771a3-31a4-4dc2-9dee-f2993611b44b",
                            "secondarytypes": ["Compilation"],
                            "title": "Caf\u00e9 del Mar, Volumen Veinte",
                            "type": "Album",
                        },
                        {
                            "artists": [
                                {
                                    "id": "89ad4ac3-39f7-470e-963a-56509c546377",
                                    "name": "Various Artists",
                                }
                            ],
                            "id": "9e585041-f2c1-3f0d-be40-40c845a3323f",
                            "secondarytypes": ["Soundtrack"],
                            "title": "Donkey Punch",
                            "type": "Album",
                        },
                    ],
                    "title": "Lower Your Eyelids to Die With the Sun",
                }
            ],
            "score": 1.0,
        },
    ],
    "status": "ok",
}
"""Example response returned by the AcoustID API example request.
The metadata requested was changed to reflect the metadata the actual requests in the
acoustid module.
"""


EXAMPLE_ACOUSTID_RESPONSE_MULTIPLE_ALBUMS = {
    "results": [
        {
            "id": "9ff43b6a-4f16-427c-93c2-92307ca505e0",
            "recordings": [
                {
                    "artists": [
                        {"id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd", "name": "M83"}
                    ],
                    "duration": 638,
                    "id": "cd2e7c47-16f5-46c6-a37c-a1eb7bf599ff",
                    "releasegroups": [
                        {
                            "artists": [
                                {
                                    "id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd",
                                    "name": "M83",
                                }
                            ],
                            "id": "ddaa2d4d-314e-3e7c-b1d0-f6d207f5aa2f",
                            "title": "Before the Dawn Heals Us",
                            "type": "Album",
                        },
                        {
                            "artists": [
                                {
                                    "id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd",
                                    "name": "M83",
                                }
                            ],
                            "id": "425771a3-31a4-4dc2-9dee-f2993611b44b",
                            "title": "A Fake Album",
                            "type": "Album",
                        },
                        {
                            "artists": [
                                {
                                    "id": "89ad4ac3-39f7-470e-963a-56509c546377",
                                    "name": "Various Artists",
                                }
                            ],
                            "id": "9e585041-f2c1-3f0d-be40-40c845a3323f",
                            "secondarytypes": ["Soundtrack"],
                            "title": "Donkey Punch",
                            "type": "Album",
                        },
                    ],
                    "title": "Lower Your Eyelids to Die With the Sun",
                }
            ],
            "score": 1.0,
        },
        {
            "id": "be6fa248-97d1-4a18-845b-7c6a070b764c",
            "recordings": [
                {
                    "artists": [
                        {"id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd", "name": "M83"}
                    ],
                    "duration": 638,
                    "id": "cd2e7c47-16f5-46c6-a37c-a1eb7bf599ff",
                    "releasegroups": [
                        {
                            "artists": [
                                {
                                    "id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd",
                                    "name": "M83",
                                }
                            ],
                            "id": "ddaa2d4d-314e-3e7c-b1d0-f6d207f5aa2f",
                            "title": "Before the Dawn Heals Us",
                            "type": "Album",
                        },
                        {
                            "artists": [
                                {
                                    "id": "89ad4ac3-39f7-470e-963a-56509c546377",
                                    "name": "Various Artists",
                                }
                            ],
                            "id": "425771a3-31a4-4dc2-9dee-f2993611b44b",
                            "secondarytypes": ["Compilation"],
                            "title": "Caf\u00e9 del Mar, Volumen Veinte",
                            "type": "Album",
                        },
                        {
                            "artists": [
                                {
                                    "id": "89ad4ac3-39f7-470e-963a-56509c546377",
                                    "name": "Various Artists",
                                }
                            ],
                            "id": "9e585041-f2c1-3f0d-be40-40c845a3323f",
                            "secondarytypes": ["Soundtrack"],
                            "title": "Donkey Punch",
                            "type": "Album",
                        },
                    ],
                    "title": "Lower Your Eyelids to Die With the Sun",
                }
            ],
            "score": 1.0,
        },
    ],
    "status": "ok",
}
"""Example response returned by the AcoustID API example request.
The metadata requested was changed to reflect the metadata the actual requests in the
acoustid module.
"""


EXAMPLE_ACOUSTID_ERROR_RESPONSE = {
    "error": {"code": 3, "message": "invalid fingerprint"},
    "status": "error",
}
"""An example for a response for a failed request."""

EXAMPLE_ACOUSTID_EMPTY_RESPONSE = {"status": "ok"}
"""An example for an empty response."""


def test_parse_lookup_result_success():
    result = _parse_lookup_result(EXAMPLE_ACOUSTID_RESPONSE)
    assert result == [
        {
            "artist": "M83",
            "title": "Lower Your Eyelids to Die With the Sun",
            "album": "Before the Dawn Heals Us",
            "albumartist": "M83",
        },
    ]


def test_parse_lookup_result_one_empty():
    result = _parse_lookup_result(EXAMPLE_ACOUSTID_RESPONSE_ONE_EMPTY)
    assert result == [
        {
            "artist": "M83",
            "title": "Lower Your Eyelids to Die With the Sun",
            "album": "Before the Dawn Heals Us",
            "albumartist": "M83",
        },
    ]


def test_parse_lookup_result_multiple_albums():
    result = _parse_lookup_result(EXAMPLE_ACOUSTID_RESPONSE_MULTIPLE_ALBUMS)
    assert result == [
        {
            "artist": "M83",
            "title": "Lower Your Eyelids to Die With the Sun",
            "album": "Before the Dawn Heals Us",
            "albumartist": "M83",
        },
        {
            "artist": "M83",
            "title": "Lower Your Eyelids to Die With the Sun",
            "album": "A Fake Album",
            "albumartist": "M83",
        },
    ]


def test_parse_lookup_result_multiple_songs():
    result = _parse_lookup_result(EXAMPLE_ACOUSTID_RESPONSE_MULTIPLE_SONGS)
    assert result == [
        {
            "artist": "M83",
            "title": "Lower Your Eyelids to Die With the Sun",
            "album": "Before the Dawn Heals Us",
            "albumartist": "M83",
        },
        {
            "artist": "My Test Artist",
            "title": "Lower Your Eyelids to Die With the Sun",
            "album": "Before the Dawn Heals Us",
            "albumartist": "M83",
        },
    ]


def test_parse_lookup_result_error():
    try:
        _parse_lookup_result(EXAMPLE_ACOUSTID_ERROR_RESPONSE)
        assert 0 == 1
    except acoustid.WebServiceError:
        # this error should be thrown.
        assert 1 == 1


def test_parse_lookup_result_empty():
    try:
        _parse_lookup_result(EXAMPLE_ACOUSTID_EMPTY_RESPONSE)
        assert 0 == 1
    except acoustid.WebServiceError:
        # this error should be thrown.
        assert 1 == 1


# TODO: Test _extract_recordings
def test_extract_recordings():
    result = _extract_recordings(EXAMPLE_ACOUSTID_RESPONSE["results"])
    assert result == [
        {
            "title": "Lower Your Eyelids to Die With the Sun",
            "artists": [{"id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd", "name": "M83"}],
            "releasegroups": [
                {
                    "artists": [
                        {
                            "id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd",
                            "name": "M83",
                        }
                    ],
                    "id": "ddaa2d4d-314e-3e7c-b1d0-f6d207f5aa2f",
                    "title": "Before the Dawn Heals Us",
                    "type": "Album",
                },
            ],
        }
    ]


def test_extract_recordings_empty():
    result = _extract_recordings(EXAMPLE_ACOUSTID_RESPONSE_ONE_EMPTY["results"])
    assert result == [
        {
            "title": "Lower Your Eyelids to Die With the Sun",
            "artists": [{"id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd", "name": "M83"}],
            "releasegroups": [
                {
                    "artists": [
                        {
                            "id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd",
                            "name": "M83",
                        }
                    ],
                    "id": "ddaa2d4d-314e-3e7c-b1d0-f6d207f5aa2f",
                    "title": "Before the Dawn Heals Us",
                    "type": "Album",
                },
            ],
        }
    ]


def test_extract_recordings_multiple_albums():
    result = _extract_recordings(EXAMPLE_ACOUSTID_RESPONSE_MULTIPLE_ALBUMS["results"])
    assert result == [
        {
            "title": "Lower Your Eyelids to Die With the Sun",
            "artists": [{"id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd", "name": "M83"}],
            "releasegroups": [
                {
                    "artists": [
                        {
                            "id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd",
                            "name": "M83",
                        }
                    ],
                    "id": "ddaa2d4d-314e-3e7c-b1d0-f6d207f5aa2f",
                    "title": "Before the Dawn Heals Us",
                    "type": "Album",
                },
                {
                    "artists": [
                        {
                            "id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd",
                            "name": "M83",
                        }
                    ],
                    "id": "425771a3-31a4-4dc2-9dee-f2993611b44b",
                    "title": "A Fake Album",
                    "type": "Album",
                },
            ],
        }
    ]


def test_extract_recordings_multiple_songs():
    result = _extract_recordings(EXAMPLE_ACOUSTID_RESPONSE_MULTIPLE_SONGS["results"])
    assert result == [
        {
            "title": "Lower Your Eyelids to Die With the Sun",
            "artists": [{"id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd", "name": "M83"}],
            "releasegroups": [
                {
                    "artists": [
                        {
                            "id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd",
                            "name": "M83",
                        }
                    ],
                    "id": "ddaa2d4d-314e-3e7c-b1d0-f6d207f5aa2f",
                    "title": "Before the Dawn Heals Us",
                    "type": "Album",
                },
            ],
        },
        {
            "title": "Lower Your Eyelids to Die With the Sun",
            "artists": [
                {
                    "id": "087b7cd4-254b-4c25-83f6-dd20f98ceacd",
                    "name": "My Test Artist",
                }
            ],
            "releasegroups": [
                {
                    "artists": [
                        {
                            "id": "6d7b7cd4-254b-4c25-83f6-dd20f98ceacd",
                            "name": "M83",
                        }
                    ],
                    "id": "ddaa2d4d-314e-3e7c-b1d0-f6d207f5aa2f",
                    "title": "Before the Dawn Heals Us",
                    "type": "Album",
                },
            ],
        },
    ]


# TODO: test _merge_matching_recordings

# TODO: test _filter_out_compilations_from_releasegroups

# TODO: test _get_results_for_recordings

# TODO: test _get_results_for_releasegroup

# TODO: test _join_artist_names
