import os


def get_ui_file(name: str):
    cwd = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(cwd, f"{name}.ui")
    return path
