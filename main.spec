import os

a = Analysis(
    ["main.py"],
    pathex=[os.path.abspath(".")],  # Add project root to path
    binaries=[],
    datas=[
        ("assets", "assets"),
        ("version.py", "."),
        ("logs", "logs"),
        ("user_config", "user_config"),
    ],
    # Bundle the full assets folder
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="PDF-Toolkit",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False = --windowed
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="assets/PDF_file.ico",
)
