import os
import tempfile


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_abs_src_dir_in_built_app(lvl=2):
    absolute_path = os.path.abspath(__file__)
    splitted_absolute_path = absolute_path.split("/")
    for _ in range(lvl):
        len(splitted_absolute_path) != 0 and splitted_absolute_path.pop()
    return os.path.join("/".join(splitted_absolute_path))


# TODO temp folder is used only in dev
profile_dir = os.path.join(tempfile.gettempdir(), "audiosplitter")

audios_dir = profile_dir + "/audios"
