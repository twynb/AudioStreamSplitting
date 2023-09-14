from backend.utils.file_name_formatter import format_file_name, replace_all


def test_replace_all_multiple():
    testString = "{DEMO} is {TEST} andEMPTY it's {SOMETHING}"
    testDict = {
        "{DEMO}": "This",
        "{TEST}": "working",
        "{SOMETHING}": "cool!",
        "EMPTY": "",
    }
    assert replace_all(testString, testDict) == "This is working and it's cool!"


def test_replace_all_no_occurences():
    testString = "This has nothing to replace!"
    testDict = {"n0thing": "bgnfldd", "working": "work work"}
    assert replace_all(testString, testDict) == "This has nothing to replace!"


def test_replace_all_order():
    testString = "house om"
    testDict = {"house": "home", "om": "em"}
    assert replace_all(testString, testDict) == "heme em"


def test_format_file_name_full():
    format = "{{ARTIST}}_{{TITLE}}_{{ALBUM}}_{{YEAR}}"
    assert (
        format_file_name(format, "MySong", "Arty", "ablum", "2003")
        == "Arty_MySong_ablum_2003"
    )
