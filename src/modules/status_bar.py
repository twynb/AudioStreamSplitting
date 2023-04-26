from PyQt6.QtWidgets import QMainWindow, QStatusBar, QMenu
from PyQt6.QtGui import QAction, QIcon, QKeySequence

available_languages = ["English", "German"]


def setup_status_bar(self: QMainWindow):
    status_bar = QStatusBar()
    self.setStatusBar(status_bar)

    menu_bar = self.menuBar()

    settings_languages = QMenu(self.tr("Languagues"), self)
    for lang in available_languages:
        action = QAction(self.tr(lang), self)
        action.setCheckable(True)
        action.triggered.connect(
            lambda _, l=lang: on_change_language(l))
        settings_languages.addAction(action)

    settings = menu_bar.addMenu(self.tr("&Settings"))
    settings.addMenu(settings_languages)

    def on_change_language(lang: str):
        print("Selected language:", lang)
