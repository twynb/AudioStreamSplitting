import threading
import webview

from werkzeug.serving import make_server
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from server import server, gui_dir


class ViteFileChangeHandler(FileSystemEventHandler):
    # TODO implement HMR here
    def on_any_event(self, event):
        if event.src_path.endswith(('.js', '.css')):
            print("something changed")


if __name__ == '__main__':
    flask_thread = threading.Thread(target=make_server(
        'localhost', 5000, server).serve_forever)
    flask_thread.start()

    event_handler = ViteFileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, gui_dir)
    observer.start()

    webview.create_window('AUDIO', server)
    webview.start(debug=True)

    observer.stop()
    observer.join()

    flask_thread.join()
