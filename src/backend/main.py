import argparse
from flaskwebgui import FlaskUI, find_browser
from app import app
import os
import tempfile

parser = argparse.ArgumentParser(description='Script description')

parser.add_argument('--debug', help='Enable debug mode', action='store_true')
parser.add_argument('--alone', help='Run server alone', action='store_true')

args = parser.parse_args()

debug_mode = args.debug
alone_mode = args.alone

port = 55555
browser_path = find_browser()
profile_dir = os.path.join(tempfile.gettempdir(), "audioss")

browser_command=[ browser_path,
                  f'--user-data-dir={profile_dir}',
                  '--new-window',
                  '--disable-extensions',
                  '--disable-background-networking',
                  '--disable-sync',
                  '--disable-translate',
                  '--disable-background-timer-throttling',
                  '--disable-notifications',
                  '--no-first-run',
                  '--window-size=1280,768',
                  f'--app=http://127.0.0.1:{port}'
                  ]

if __name__ == '__main__':
    if alone_mode:
        app.run(debug=debug_mode,port=port)
    else:
        FlaskUI(
            server='flask',
            server_kwargs={
               'app': app,
               'port': port,
               'debug': debug_mode,
            },
            browser_command=browser_command
            ).run()
