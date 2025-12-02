# -*- mode: python ; coding: utf-8 -*-
"""
天眼查企业信息查询工具 - PyInstaller打包配置
"""

block_cipher = None

a = Analysis(
    ['tianyancha_gui_main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('tianyancha_treeview.py', '.'),
        ('app_icon.ico', '.'),
    ],
    hiddenimports=[
        'requests',
        'bs4',
        'lxml',
        'pickle',
        'threading',
        'json',
        're',
        'time',
        'os',
        'ctypes',
        'ctypes.wintypes',
        # pywin32相关模块
        'win32clipboard',
        'win32con',
        'win32api',
        'win32gui',
        'pywintypes',
        'pythoncom',
        'win32com',
        'win32com.client',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['PyQt5', 'PyQt6', 'PySide2', 'PySide6', 'IPython', 'sphinx', 'pytest', 'numpy', 'PIL', 'jedi', 'pygments'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='天眼查企业信息查询工具',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico',  # 应用图标
)
