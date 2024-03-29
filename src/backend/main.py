import argparse

from api import app
from flaskwebgui import FlaskUI, find_browser
from utils import path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script description")

    parser.add_argument("--debug", help="Enable debug mode", action="store_true")
    parser.add_argument("--alone", help="Run server alone", action="store_true")

    args = parser.parse_args()

    debug_mode = args.debug
    alone_mode = args.alone

    port = 55555
    browser_path = find_browser()

    browser_command = [
        browser_path,
        f"--user-data-dir={path.profile_dir}",
        "--new-window",
        "--disable-extensions",
        "--disable-background-networking",
        "--disable-sync",
        "--disable-translate",
        "--disable-background-timer-throttling",
        "--disable-notifications",
        "--disable-pinch",
        "--disable-geolocation",
        "--disable-default-apps",
        "--disable-infobars",
        "--no-first-run",
        "--no-default-browser-check",
        "--window-size=1280,800",
        f"--app=http://127.0.0.1:{port}",
    ]

    if alone_mode:
        app.app.run(debug=debug_mode, port=port)
    else:
        FlaskUI(
            server="flask",
            server_kwargs={
                "app": app.app,
                "port": port,
                "debug": debug_mode,
            },
            browser_command=browser_command,
        ).run()
