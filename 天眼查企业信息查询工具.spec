# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['tianyancha_gui_main.py'],
    pathex=[],
    binaries=[],
    datas=[('tianyancha_treeview.py', '.')],
    hiddenimports=['tkinter', 'tkinter.ttk', 'requests', 'bs4', 'beautifulsoup4'],
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
    name='天眼查企业信息查询工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
