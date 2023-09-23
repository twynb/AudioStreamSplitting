import utils.list_helper


def test_flatten_numbers():
    arr = [[1, 4, 7], [99, 2]]
    assert utils.list_helper.flatten(arr) == [1, 4, 7, 99, 2]


def test_flatten_dicts():
    result = utils.list_helper.flatten(
        [
            [{"test": "test2", "test2": "1234"}, {"test": "wah wah", "test2": "wah."}],
            [{"test": "meep", "test2": "boom"}],
            [{"test": "things", "test2": "a lot of them"}],
        ]
    )
    assert result == [
        {"test": "test2", "test2": "1234"},
        {"test": "wah wah", "test2": "wah."},
        {"test": "meep", "test2": "boom"},
        {"test": "things", "test2": "a lot of them"},
    ]


# TODO: test remove_duplicate_dicts
def test_remove_duplicate_dicts_no_duplicates():
    input = [
        {"test": "test2", "test2": "1234"},
        {"test": "wah wah", "test2": "wah."},
        {"test": "meep", "test2": "boom"},
    ]
    result = utils.list_helper.remove_duplicate_dicts(input)
    assert result == input


def test_remove_duplicate_dicts_several_duplicates():
    input = [
        {"test": "test2", "test2": "1234"},
        {"test": "wah wah", "test2": "wah."},
        {"test": "meep", "test2": "boom"},
        {"test": "test2", "test2": "1234"},
        {"test": "wah wah", "test2": "wah."},
    ]
    result = utils.list_helper.remove_duplicate_dicts(input)
    assert result == [
        {"test": "test2", "test2": "1234"},
        {"test": "wah wah", "test2": "wah."},
        {"test": "meep", "test2": "boom"},
    ]


def test_remove_duplicate_dicts_empty():
    assert utils.list_helper.remove_duplicate_dicts([]) == []
