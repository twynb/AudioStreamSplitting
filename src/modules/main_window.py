from ui.utils import get_ui_file
from PyQt6.QtWidgets import QMainWindow
from PyQt6 import uic


def setup_main_window(self: QMainWindow):
    path = get_ui_file("main_window")
    uic.loadUi(path, self)
