# Contributing

- [Contributing](#contributing)
  - [Code of Conduct](#code-of-conduct)
  - [Pull Request Workflow](#pull-request-workflow)
    - [Requirements](#requirements)
      - [reST doc example](#rest-doc-example)
  - [Code Structure](#code-structure)
    - [Back-End Structure](#back-end-structure)
    - [Front-End Structure](#front-end-structure)
      - [Folder Structure](#folder-structure)
      - [Frontend Workflow](#frontend-workflow)
    - [Generating documentation](#generating-documentation)
  - [Developing Environment](#developing-environment)
    - [System Requirements](#system-requirements)
    - [Installation](#installation)
      - [Manual setup](#manual-setup)
      - [Docker](#docker)
        - [Without extension](#without-extension)
        - [With extension](#with-extension)
    - [Usage](#usage)
      - [Available commands](#available-commands)
  - [Contributors](#contributors)

This document contains guidelines and advice for people willing to contribute to AudioStreamSplitting development. Most of what is said in here is common sense, but it's best to have it all present and summarized.

## Code of Conduct

Be nice to others :)

Also, please do not submit pull requests or commit messages that contain excessive swearing, we will not accept them. Try to stay professional.

## Pull Request Workflow

When contributing to AudioStreamSplitting, please follow this workflow to ensure things go smoothly.

NOTE: Part of this will only take effect once this repository becomes public. Please remove this note once that is the case.

1. Find an issue describing what you want to implement, or open an issue yourself.
2. Assign the issue to yourself, or ask to have it assigned to you.
3. Fork [this repository](https://github.com/4lex0017/AudioStreamSplitting) to your own account.
4. Implement your contribution and commit it to your forked repository. Be sure to follow the requirements outlined in [Requirements](#requirements). Test your implementation and ensure the program builds on your system.
5. Create a pull request on this repository.
6. The pull request must be approved by at least two of the main maintainers of AudioStreamSplitting (as of current, that's @chubetho, @ChrisItisdud, @4lex0017 and @JosuaE-FHWS). Reviewers must also attempt to build and run the project locally to verify everything works fine.
7. After two approvals, the pull request gets merged.

### Requirements

The following requirements must be met by the system at any time:

1. Every function has documentation comments, formatted in the reST doc format. An example comment is shown below. These documentation comments are used to [generate the back-end documentation](#generating-documentation).
2. All python code must comply to [the black code style](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html).
3. All back-end/python code that can have unit tests (i.e. doesn't rely on files on the file system, external APIs or other outside resources) must have them. When adding a new module, add an according test file in the backend/tests folder. When updating an existing one, add or update tests in the correlating test file. All tests must pass (obviously).
4. All business logic must be in the back-end. The front-end should only contain the user interface.

#### reST doc example

```python
def foo(bar, foobar):
    """My description goes here.
    It can even have multiple lines!

    :param bar: A parameter.
    :param foobar: Another parameter
    :returns: bar again.
    """
    print(foobar)
    return bar
```

## Code Structure

The code is structured into two main parts, the back-end (containing the business logic and written in python) and the front-end (containing the UI and written in TypeScript with Vue.js). It's modular such that you could theoretically stick a new front-end on the current back-end without rewriting business logic.

### Back-End Structure

The back-end is mostly centered around two modules containing the logic for segmentation and song identification. Connection to the front-end is done via Flask. The main relevant files are:

1. ``backend/main.py`` is the entry point that runs the app.
2. ``backend/api/app.py`` is the main entrypoint for Flask. Error handlers and other API modules are registered here.
3. ``backend/api/audio.py`` contains the API routes for song segmentation, recognition and saving.
4. ``backend/modules/segmentation.py`` implements the segmentation logic. Relevant concepts to understand it are [Feature Smoothing](https://www.audiolabs-erlangen.de/resources/MIR/FMP/C4/C4S2_SSM-FeatureSmoothing.html), [Self-similarity-matrices](https://www.audiolabs-erlangen.de/resources/MIR/FMP/C4/C4S2_SSM.html), [Novelty](https://www.audiolabs-erlangen.de/resources/MIR/FMP/C4/C4S4_NoveltySegmentation.html) and [Peak Selection](https://www.audiolabs-erlangen.de/resources/MIR/FMP/C6/C6S1_PeakPicking.html)
5. ``backend/modules/api_service.py`` implements the song recognition. Each song identification API used has either a pre-made python wrapper (such as AcoustID with PyAcoustId) or its own module in ``backend/modules/apis/`` (such as Shazam), which ``api_service`` calls to gather data from that API.

Other modules in the ``backend/modules`` and ``backend/utils`` folders are utility classes used in or for one of the above. The other routes in the ``backend/api`` folder are used for user settings.

Tests are situated in ``backend/tests``. Each module that has unit tests has its own corresponding module in this folder.

### Front-End Structure

#### Folder Structure

- **components**: This directory serves as a home for reusable UI components. All components placed here are automatically imported, simplifying their usage. If you're enhancing or creating user interface elements, this is where you'll focus your efforts.

- **composables**: The "composables" directory contains functions or logic that can be shared across different parts of our application. Functions within this folder are also automatically imported, promoting code reusability.

- **includes**: Files that are included or imported into our project are stored here. This could include configuration files, or utility functions.

- **locales**: For applications with multilingual support, the "locales" directory is the repository for language files and localization-related code, ensuring a smooth internationalization process.

- **models**: In the "models" directory, you'll find data models and classes that define the structure of our application's data. This is the place to work on data-related functionality.

- **modules**: The "modules" directory holds core modules such as pinia, vue-router, and other essential packages that are installed when the application initializes.

- **pages**: Our application's main pages reside in the "pages" directory. Each page typically corresponds to a specific route. When enhancing or creating views, this directory is where you'll make your contributions.

- **public**: Static assets such as images, fonts, or other files that don't require processing by build tools are stored in the public directory.

- **stores**: All pinia stores, responsible for managing application state, are located in the "stores" directory, facilitating structured state management.


#### Frontend Workflow
1.  `main.ts` serves as the entry point for the frontend. It initializes all modules located in the `modules` folder. Eventually, it mounts the `App.vue` component into the DOM. For more details, refer to the [Vue.js documentation](https://vuejs.org/).

2. `App.vue` acts as the wrapper component for the entire application. It defines the layout, including the sidebar, and the content for each page.

3. `pages/project/[id].vue` houses almost all of the application's features. It's the primary focus of your development efforts.

4. Example for adding a new page
     - Create a new component in the `pages` folder (e.g., `statistics.vue`).
     - Add a new `<SideBarRow link="/statistics" />` within the `<SideBar />` component for navigation.
     - At this point your implementation should be inside this `statistics.vue` file.

### Generating documentation

To generate documentation, run ``npm run docs:generate``. You will then find HTML docs for the back-end in docs/_build/html. Also showing the documentation as Github pages is planned for the future, but cannot be done before this repository goes public.

## Developing Environment

### System Requirements

- Python 3.10 or later: [Download here](https://www.python.org/downloads/)
- pip: [Download here](https://pip.pypa.io/en/stable/cli/pip_download/)
- pyinstaller: [Download here](https://pypi.org/project/pyinstaller/)
- Node.js 18.17.1 or later: [Download here](https://nodejs.org/en/download)

### Installation

You can choose between manual setup or using Docker for simplicity.

#### Manual setup

1. Clone the repository to your local machine.
2. Install the required Python packages using the command `pip install -r requirements.txt`.
3. Install Node.js modules using the command `npm install`.
4. Setup `lint-staged` and `simple-git-hooks` using the command `npx simple-git-hooks`
5. Download the latest release of [fpcalc](https://acoustid.org/chromaprint) for your system from [the AcoustID website](https://acoustid.org/chromaprint) if you want to use the AcoustID API. Put it in a location of your choosing and add it to your system PATH. You will probably need to restart your system before first using AudioStreamSplitting.

#### Docker

If you are using VSCode as your code editor, it is recommended to set up a container with the appropriate extension.

##### Without extension

Build the Docker image using the command

```bash
docker build -t ass .
```

Run the container using the command

```bash
docker run -v ${pwd}/workspaces/AudioStreamSplitting ass -it bash
```

##### With extension

1. Download the VSCode Remote - Containers extension from [here](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

2. Press `Ctrl + Shift + P` to open the command palette, then select `Dev Container: Reopen in container`.

### Usage

For normal development, use the following commands in 2 different terminals:

```bash
npm run dev:be
```

```bash
npm run dev:be
```

#### Available commands

| Command                  | Description                      |
| ------------------------ | -------------------------------- |
| npm run `dev:fe`         | Run frontend server              |
| npm run `dev:be`         | Run backend server               |
| npm run `view:app`       | Run desktop app                  |
| npm run `build:fe`       | Build frontend (html, js, css)   |
| npm run `build:app`      | Build desktop app                |
| npm run `docs:generate`  | Generate backend documentation   |

## Contributors

When adding a contribution to this, feel free to add your name to this list, formatted as either just your real name/github username or "Real Name (github username)".

- chubetho
- Christina Reichel (ChrisItisdud)
- 4lex0017
- JosuaE-FHWS
