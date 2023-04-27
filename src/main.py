import sys
from PyQt6.QtCore import QUrl, QModelIndex
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtWidgets import (QMainWindow, QFileDialog,
                             QPushButton, QListView)

from modules.app import app
from modules.status_bar import setup_status_bar
from modules.main_window import setup_main_window


class MainWindow(QMainWindow):
    def __init__(self: QMainWindow):
        super().__init__()

        # setup ui
        setup_status_bar(self)
        setup_main_window(self)

        # setup media player
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(100)
        self.media_player = QMediaPlayer()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_content_list = []

        upload_button: QPushButton = self.findChild(
            QPushButton, "uploadButton")
        upload_button.clicked.connect(self.get_audio_files)

        self.play_button: QPushButton = self.findChild(
            QPushButton, "playButton")
        self.play_button.clicked.connect(self.toggle_play_pause)

        self.list_model = QStandardItemModel()
        audio_list: QListView = self.findChild(QListView, "audioList")
        audio_list.setModel(self.list_model)
        audio_list.doubleClicked.connect(self.play_selected_file)

    def get_audio_files(self):
        file_names, _ = QFileDialog.getOpenFileNames(
            self, caption='Select one or more audio files', directory='./', filter='*.wav *.mp3')

        for file_name in file_names:
            item = QStandardItem(file_name)
            self.list_model.appendRow(item)
            media_content = QUrl.fromLocalFile(file_name)
            self.media_content_list.append(media_content)

        self.play_button.setEnabled(True)

    def play_selected_file(self, file: QModelIndex):
        self.media_player.stop()
        source = self.media_content_list[file.row()]
        self.media_player.setSource(source)
        self.media_player.play()
        self.play_button.setText(self.tr("Pause"))

    def toggle_play_pause(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
            self.play_button.setText(self.tr("Play"))
        else:
            self.media_player.play()
            self.play_button.setText(self.tr("Pause"))


if __name__ == '__main__':
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
