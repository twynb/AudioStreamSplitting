from PyQt6.QtWidgets import QMainWindow, QStatusBar, QMenu
from PyQt6.QtGui import QAction, QActionGroup
from PyQt6.QtCore import QTranslator
from modules.app import app
import os

available_languages = ["English", "German"]

i18n_dir = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "i18n"))

translator = QTranslator()


def setup_status_bar(self: QMainWindow):
    status_bar = QStatusBar()
    self.setStatusBar(status_bar)

    menu_bar = self.menuBar()
    settings_languages = QMenu(self.tr("Languagues"), self)

    language_group = QActionGroup(self)
    language_group.setExclusive(True)

    for lang in available_languages:
        action = QAction(self.tr(lang), self, checkable=True)
        action.triggered.connect(lambda _, l=lang: on_change_language(l))
        settings_languages.addAction(action)
        language_group.addAction(action)

    language_group.actions()[0].setChecked(True)

    settings = menu_bar.addMenu(self.tr("&Settings"))
    settings.addMenu(settings_languages)

    def on_change_language(lang: str):
        """ Not work because it need a function to retranslate UI """
        print(lang)

        # match lang:
        #     case "English":
        #         if translator.load("main_en.qm", os.path.join(
        #                 os.path.dirname(__file__), "..", "i18n")):
        #             app.installTranslator(translator)
        #             return True
        #     case "German":
        #         if translator.load("main_de.qm", os.path.join(
        #                 os.path.dirname(__file__), "..", "i18n")):
        #             app.installTranslator(translator)
        #             return True
        #     case _: return False
