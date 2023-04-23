from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtWidgets import QMainWindow, QWidget, QApplication, QFileDialog, QPushButton, QVBoxLayout, QHBoxLayout, QListView
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Audio Splitting")

        # setup media player
        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(100)
        self.media_player = QMediaPlayer()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_content_list = []

        # create buttons
        self.button_upload = QPushButton('Upload audio files')
        self.button_upload.clicked.connect(self.get_audio_files)

        self.button_play_pause = QPushButton('Play')
        self.button_play_pause.setEnabled(False)
        self.button_play_pause.clicked.connect(self.toggle_play_pause)

        # create list
        self.list_view = QListView()
        self.list_model = QStandardItemModel()
        self.list_view.setModel(self.list_model)
        self.list_view.doubleClicked.connect(self.play_selected_file)

        # setup layouts
        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.button_upload)
        layout_buttons.addWidget(self.button_play_pause)

        layout_main = QVBoxLayout()
        layout_main.addLayout(layout_buttons)
        layout_main.addWidget(self.list_view)

        central_widget = QWidget()
        central_widget.setLayout(layout_main)
        self.setCentralWidget(central_widget)

    def get_audio_files(self):
        # Open file dialog to select multiple audio files
        file_names, _ = QFileDialog.getOpenFileNames(
            self, caption='Select one or more audio files', directory='./', filter='*.wav *.mp3')

        for file_name in file_names:
            item = QStandardItem(file_name)
            self.list_model.appendRow(item)
            media_content = QUrl.fromLocalFile(file_name)
            self.media_content_list.append(media_content)

        self.button_play_pause.setEnabled(True)

    def play_selected_file(self, file):
        self.media_player.stop()
        source = self.media_content_list[file.row()]
        self.media_player.setSource(source)
        self.media_player.play()
        self.button_play_pause.setText("Pause")

    def toggle_play_pause(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
            self.button_play_pause.setText("Play")
        else:
            self.media_player.play()
            self.button_play_pause.setText("Pause")


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
