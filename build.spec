# -*- mode: python ; coding: utf-8 -*-
import platform

current_os = platform.system()

if current_os == "Linux":
    app_name = "audio_splitter_linux"
elif current_os == "Darwin":
    app_name = "audio_splitter_macos"
elif current_os == "Windows":
    app_name = "audio_splitter_window.exe"
else:
    raise Exception(f"Unsupported operating system: {current_os}")

a = Analysis(  # noqa F821
    ["src/backend/main.py"],
    pathex=["src/backend"],
    binaries=[],
    datas=[("gui/*", "./gui"), (".env", ".")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "altgraph",
        "black",
        "iniconfig",
        "Jinja2",
        "MarkupSafe",
        "pooch",
        "pytest",
        "ruff",
        "tomli",
        "watchdog",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)  # noqa F821

exe = EXE(  # noqa F821
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name=app_name,
    icon="src/frontend/public/logo.ico",
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
