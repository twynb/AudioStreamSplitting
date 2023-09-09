import os
import tempfile
from pathlib import Path


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def get_abs_src_dir_in_built_app(lvl=2):
    path = Path(os.path.abspath(__file__))
    for _ in range(lvl):
        path = path.parent
    print(str(path))
    return str(path)


# TODO temp folder is used only in dev
profile_dir = os.path.join(tempfile.gettempdir(), "audiosplitter")

audios_dir = os.path.join(profile_dir, "audios")
