# Audio Stream Splitting

- [Audio Stream Splitting](#audio-stream-splitting)
  - [Requirements](#requirements)
  - [Installation](#installation)
    - [Manual setup](#manual-setup)
    - [Docker](#docker)
      - [Without extension:](#without-extension)
      - [With extension:](#with-extension)
  - [Usage](#usage)
    - [Availables commands](#availables-commands)

---

## Requirements

- Python 3.10 or later: [Download here](https://www.python.org/downloads/)
- pip: [Download here](https://pip.pypa.io/en/stable/cli/pip_download/)
- pyinstaller: [Download here](https://pypi.org/project/pyinstaller/)
- Node.js 18.17.1 or later: [Download here](https://nodejs.org/en/download)

## Installation

You can choose between manual setup or using Docker for simplicity.

### Manual setup

1. Clone the repository to your local machine.

2. Install the required Python packages using the command `pip install -r requirements.txt`.

3. Install Node.js modules using the command `npm install`.

4. Setup `lint-staged` and `simple-git-hooks` using the command `npx simple-git-hooks`

5. Install the fpcalc tool by including the relevant subdirectory of ``libraries/chromaprint`` in your system PATH or, preferably, copy the fpcalc executable in that subdirectory to a different place on your machine and adding that to your system PATH.

### Docker

If you are using VSCode as your code editor, it is recommended to set up a container with the appropriate extension.

#### Without extension:

1. Build the Docker image using the command:

```bash
docker build -t ass .
```

2. Run the container using the command:

```bash
docker run -v ${pwd}/workspaces/AudioStreamSplitting ass -it bash
```

#### With extension:

1. Download the VSCode Remote - Containers extension from [here](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

2. Press `Ctrl + Shift + P` to open the command palette, then select `Dev Container: Reopen in container`.

## Usage

For normal development, use the following commands in 2 different terminals:

```bash
npm run fe
```

```bash
npm run be:debug
```

### Availables commands

| Command                  | Description                      |
| ------------------------ | -------------------------------- |
| npm run `fe`             | Run frontend server              |
| npm run `be`             | Run backend server               |
| npm run `be:debug`       | Run backend server in debug mode |
| npm run `view:app`       | Run desktop app                  |
| npm run `view:app:debug` | Run desktop app in debug mode    |
| npm run `build:fe`       | Build frontend (html, js, css)   |
| npm run `build:app`      | Build desktop app                |
| npm run `preview`        | Preview built desktop app        |
