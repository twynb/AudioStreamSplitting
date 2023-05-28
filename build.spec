# -*- mode: python ; coding: utf-8 -*-

# PyInstaller options
a = Analysis(
    ['src/backend/main.py'],  # Entry point script(s)
    pathex=['src/backend'],  # Additional module search path
    binaries=[],  # Additional binaries or DLLs (if any)
    datas=[('gui/*', './gui')],  # Additional non-Python files (if any)
    hiddenimports=[],  # Additional imports (if any)
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Create a .exe or executable (modify as needed)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=True,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
