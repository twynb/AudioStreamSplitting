import argparse
import threading
import webview

from werkzeug.serving import make_server
from server import server

parser = argparse.ArgumentParser(description='Script description')

parser.add_argument('--debug', help='Enable debug mode', action='store_true')
parser.add_argument('--alone', help='Run server alone', action='store_true')

args = parser.parse_args()

debug_mode = args.debug
alone_mode = args.alone

if __name__ == '__main__':
    if alone_mode:
        server.run(debug=True if debug_mode else False)
    else:
        flask_thread = threading.Thread(target=make_server(
            'localhost', 5000, server).serve_forever)
        flask_thread.start()

        # TODO implement HMR for backend

        webview.create_window('AUDIO', server)
        webview.start(debug=True if debug_mode else False)

        flask_thread.join()
