# -*- mode: python ; coding: utf-8 -*-

import os


project_dir = os.path.abspath(os.getcwd())
ffmpeg_path = os.path.join(project_dir, "ffmpeg.exe")
ffprobe_path = os.path.join(project_dir, "ffprobe.exe")
vlc_dir = r"C:\Program Files\VideoLAN\VLC"

if not os.path.isfile(ffmpeg_path):
    raise SystemExit(f"找不到 FFmpeg：{ffmpeg_path}")
if not os.path.isfile(ffprobe_path):
    raise SystemExit(f"找不到 FFprobe：{ffprobe_path}")
if not os.path.isfile(os.path.join(vlc_dir, "libvlc.dll")):
    raise SystemExit(f"找不到 VLC 运行库：{vlc_dir}")

vlc_datas = []
for root, _dirs, files in os.walk(vlc_dir):
    relative = os.path.relpath(root, vlc_dir)
    destination = "vlc" if relative == "." else os.path.join("vlc", relative)
    for filename in files:
        vlc_datas.append((os.path.join(root, filename), destination))


a = Analysis(
    ["video_trimmer_gui.py"],
    pathex=[project_dir],
    binaries=[
        (ffmpeg_path, "."),
        (ffprobe_path, "."),
    ],
    datas=vlc_datas,
    hiddenimports=["vlc"],
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
    [],
    exclude_binaries=True,
    name="VideoTrimmerTool",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name="VideoTrimmerTool",
)
