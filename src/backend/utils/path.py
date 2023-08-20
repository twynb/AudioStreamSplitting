import os
import tempfile


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


# TODO temp folder is used only in dev
profile_dir = os.path.join(tempfile.gettempdir(), "audiosplitter")

audios_dir = profile_dir + "/audios"
