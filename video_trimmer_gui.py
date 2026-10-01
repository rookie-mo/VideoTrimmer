import sys
import os
import time
import subprocess
import json
import ctypes
from datetime import timedelta

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox,
    QProgressBar, QSpinBox, QDoubleSpinBox, QCheckBox, QGroupBox,
    QFormLayout, QStatusBar, QSlider, QComboBox, QListWidget,
    QListWidgetItem, QAbstractItemView, QFrame, QScrollArea, QSplitter
)
from PyQt6.QtCore import (
    Qt,
    QEvent,
    QThread,
    pyqtSignal,
    QUrl,
    QRectF,
    QSettings,
    QTimer,
)
from PyQt6.QtGui import (
    QDesktopServices,
    QPainter,
    QColor,
    QPen,
)


DARK_STYLE = """
QWidget {
    background-color: #1e1f22;
    color: #e8e8e8;
    font-size: 13px;
}
QMainWindow, QDialog {
    background-color: #1e1f22;
}
QGroupBox {
    border: 1px solid #3b3f46;
    border-radius: 6px;
    margin-top: 10px;
    padding-top: 8px;
    font-weight: 600;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 4px;
    color: #d7d9de;
}
QPushButton {
    background-color: #2b2e33;
    border: 1px solid #464b53;
    border-radius: 6px;
    padding: 6px 11px;
    min-height: 18px;
}
QPushButton:hover {
    background-color: #363a41;
    border-color: #5b626c;
}
QPushButton:pressed {
    background-color: #202227;
}
QPushButton:disabled {
    background-color: #25272b;
    color: #74787f;
    border-color: #35383d;
}
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {
    background-color: #25272b;
    border: 1px solid #464b53;
    border-radius: 6px;
    padding: 5px 7px;
    selection-background-color: #0e639c;
    selection-color: #ffffff;
}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
    border-color: #3794ff;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox QAbstractItemView {
    background-color: #25272b;
    color: #e8e8e8;
    border: 1px solid #4b5058;
    selection-background-color: #0e639c;
    selection-color: #ffffff;
}
QListWidget {
    background-color: #25272b;
    border: 1px solid #464b53;
    border-radius: 6px;
    outline: none;
}
QListWidget::item {
    padding: 4px 6px;
}
QListWidget::item:selected {
    background-color: #0e639c;
    color: #ffffff;
}
QCheckBox {
    spacing: 7px;
}
QCheckBox::indicator {
    width: 14px;
    height: 14px;
    border: 1px solid #5b626c;
    border-radius: 3px;
    background-color: #25272b;
}
QCheckBox::indicator:checked {
    background-color: #0e639c;
    border-color: #3794ff;
}
QSlider::groove:horizontal {
    height: 6px;
    background-color: #3a3d42;
    border-radius: 3px;
}
QSlider::sub-page:horizontal {
    background-color: #0e639c;
    border-radius: 3px;
}
QSlider::handle:horizontal {
    background-color: #d8dbe0;
    border: 1px solid #ffffff;
    width: 14px;
    margin: -5px 0;
    border-radius: 7px;
}
QProgressBar {
    background-color: #25272b;
    border: 1px solid #464b53;
    border-radius: 6px;
    text-align: center;
    color: #ffffff;
}
QProgressBar::chunk {
    background-color: #0e639c;
    border-radius: 5px;
}
QStatusBar {
    background-color: #18191c;
    color: #b9bdc4;
}
QSplitter::handle {
    background-color: #34383e;
    width: 6px;
}
QSplitter::handle:hover {
    background-color: #3794ff;
}
QToolTip {
    background-color: #2b2e33;
    color: #f1f1f1;
    border: 1px solid #5b626c;
}
"""

LIGHT_STYLE = ""

GITHUB_USER = "rookie-mo"
GITHUB_URL = "https://github.com/rookie-mo"
APP_NAME = "VideoTrimmerTool"

CURRENT_LANGUAGE = "zh"

TRANSLATIONS = {
    "en": {
        "多视频拼接裁剪与压缩工具": "Multi-Video Trimmer & Joiner",
        "就绪": "Ready",
        "没有有效的片段可截取。": "No valid segments to process.",
        "正在准备 {count} 个片段...": "Preparing {count} segment(s)...",
        "FFmpeg 正在输出视频...": "FFmpeg is exporting the video...",
        "FFmpeg 正在输出视频... {percent}%": "FFmpeg exporting... {percent}%",
        "FFmpeg 返回错误码 {code}\n{details}": (
            "FFmpeg exited with code {code}\n{details}"
        ),
        "处理完成！": "Processing complete.",
        "视频已保存至：\n{path}": "Video saved to:\n{path}",
        "处理出错：{error}\n若使用 GPU 编码失败，请确认 NVIDIA 驱动正常，或切换到 CPU 软件编码。": (
            "Processing failed: {error}\n"
            "If GPU encoding failed, check the NVIDIA driver "
            "or switch to CPU encoding."
        ),
        "错误": "Error",
        "提示": "Notice",
        "请先加载视频。": "Load a video first.",
        "起始时间必须小于结束时间。": "Start time must be earlier than end time.",
        "结束时间不能超过总时长 {duration:.1f}s。": (
            "End time cannot exceed the total duration of {duration:.1f}s."
        ),
        "片段 {index}: {start:.2f}s → {end:.2f}s (时长 {duration:.2f}s)": (
            "Segment {index}: {start:.2f}s -> {end:.2f}s "
            "(duration {duration:.2f}s)"
        ),
        "预览模式：仅播放选中的区间": "Preview mode: selected ranges only",
        "预览模式：正常播放全部视频": "Preview mode: play the full video",
        "文件": "File",
        "视频队列": "Video queue",
        "添加视频...": "Add videos...",
        "移除选中": "Remove selected",
        "上移": "Move up",
        "下移": "Move down",
        "清空队列": "Clear queue",
        "队列顺序即输出顺序；没有片段的视频会输出完整内容。": (
            "Queue order is the output order. Videos without segments "
            "are exported in full."
        ),
        "输出文件": "Output file",
        "当前视频:": "Current video:",
        "当前选中的视频": "Selected video",
        "{count} 个片段": "{count} segment(s)",
        "完整视频": "Full video",
        "{index}. {name} | {duration} | {segments}": (
            "{index}. {name} | {duration} | {segments}"
        ),
        "静音导出": "Mute output",
        "以下视频无法读取：\n{errors}": (
            "The following videos could not be read:\n{errors}"
        ),
        "请先添加至少一个视频。": "Add at least one video first.",
        "没有可输出的视频。": "There are no videos to export.",
        "请选择输入视频": "Select an input video",
        "浏览输入...": "Browse input...",
        "选择输出路径...": "Choose output path...",
        "输入:": "Input:",
        "当前区间设置（用于添加）": "Current range settings",
        " 秒": " sec",
        "起始:": "Start:",
        "结束:": "End:",
        "区间列表": "Segment list",
        "➕ 添加区间": "➕ Add segment",
        "➖ 删除选中": "➖ Delete selected",
        "🗑️ 清空所有": "🗑️ Clear all",
        "🎯 仅播放选区 (预览拼接效果)": (
            "🎯 Play selected ranges only (preview result)"
        ),
        "未加载视频": "No video loaded",
        "输出分辨率": "Output resolution",
        "调整分辨率": "Resize output",
        "原始": "Original",
        "保持宽高比": "Keep aspect ratio",
        "预设:": "Preset:",
        "宽度:": "Width:",
        "高度:": "Height:",
        "输出编码器": "Output encoder",
        "编码器:": "Encoder:",
        "GPU 加速 (NVENC H.264)": "GPU (NVENC H.264)",
        "GPU 加速 (NVENC H.265)": "GPU (NVENC H.265)",
        "CPU 软件编码 (H.264)": "CPU H.264",
        "NVENC 画质:": "NVENC quality:",
        "高 (cq 23)": "High (cq 23)",
        "中 (cq 28)": "Medium (cq 28)",
        "低 (cq 32)": "Low (cq 32)",
        "H.264 兼容性更好；H.265 压缩率更高。GPU 编码使用 NVIDIA NVENC。": (
            "H.264 has wider compatibility; H.265 offers better compression. "
            "GPU encoding uses NVIDIA NVENC."
        ),
        "开始处理 (拼接所有区间)": "Start processing",
        "打开输出文件夹": "Open output folder",
        "输出路径：未设置": "Output path: not set",
        "输出路径：{path}": "Output path: {path}",
        "选择视频文件": "Select video file",
        "视频文件 (*.mp4 *.avi *.mkv *.mov *.flv *.wmv);;所有文件 (*.*)": (
            "Video files (*.mp4 *.avi *.mkv *.mov *.flv *.wmv);;All files (*.*)"
        ),
        "保存拼接视频": "Save joined video",
        "MP4 文件 (*.mp4);;所有文件 (*.*)": (
            "MP4 files (*.mp4);;All files (*.*)"
        ),
        "读取失败": "Read failed",
        "无法加载视频信息：{error}": "Unable to load video information: {error}",
        "FFprobe 读取失败": "FFprobe failed",
        "无法从文件中读取视频时长": "Unable to read video duration",
        "无法从文件中读取视频分辨率": "Unable to read video resolution",
        "视频已加载（VLC 内核）。点击播放开始预览。": (
            "Video loaded with VLC. Click Play to preview."
        ),
        "▶ 播放": "▶ Play",
        "⏸ 暂停": "⏸ Pause",
        "■ 停止": "■ Stop",
        "已停止": "Stopped",
        "播放结束": "Playback finished",
        "所有选区已播放完毕": "All selected ranges have finished",
        "已标记起点：{time}": "Start marked: {time}",
        "已标记终点：{time}": "End marked: {time}",
        "已清除起点/终点标记": "Start/end markers cleared",
        "时间线缩小": "Zoom out timeline",
        "时间线放大": "Zoom in timeline",
        "复位": "Reset",
        "显示完整时间线": "Show the full timeline",
        "点击帧线附近可定位时间；\n空白区域按住左右拖动可平移时间线": (
            "Click near the playhead to seek;\n"
            "drag the empty area left/right to pan the timeline"
        ),
        " 帧": " frames",
        "左右方向键每次前进/后退的帧数": (
            "Number of frames moved by the left/right arrow keys"
        ),
        "步长:": "Step:",
        "📍 标记起点": "📍 Mark start",
        "📍 标记终点": "📍 Mark end",
        "清除标记": "Clear markers",
        "界面主题:": "Theme:",
        "深色主题": "Dark theme",
        "浅色主题": "Light theme",
        "语言:": "Language:",
        "语言将在重启程序后生效。": (
            "The language change will take effect after restarting."
        ),
        "步进 {steps} 帧 {sign} | 第 {frame} 帧 @ {ms}ms": (
            "Step {steps} frame(s) {sign} | Frame {frame} @ {ms}ms"
        ),
        "时长 {duration} | 原始分辨率 {resolution} | 当前区间 {start:.1f}s ~ {end:.1f}s (时长 {range:.1f}s)": (
            "Duration {duration} | Source {resolution} | "
            "Range {start:.1f}s - {end:.1f}s ({range:.1f}s)"
        ),
        "请先选择有效的输入视频。": "Select a valid input video first.",
        "请设置输出路径。": "Set an output path first.",
        "请先添加至少一个截取区间。": "Add at least one segment first.",
        "正在使用 CPU 软件编码（libx264）...": "Using CPU H.264 (libx264)...",
        "正在使用 {encoder} · 画质 {quality} ...": (
            "Using {encoder} - {quality} ..."
        ),
        "正在输出视频... {percent}%": "Exporting video... {percent}%",
        "编码器：{encoder}\n用时：{elapsed:.2f} 秒": (
            "Encoder: {encoder}\nElapsed: {elapsed:.2f} s"
        ),
        "处理完成，用时 {elapsed:.2f} 秒 ({encoder})": (
            "Completed in {elapsed:.2f} s ({encoder})"
        ),
        "完成": "Complete",
        "处理失败": "Processing failed",
        "正在打开 GitHub：{url}": "Opening GitHub: {url}",
        "VLC 无法解码此视频": "VLC cannot decode this video",
        "预览失败": "Preview failed",
        "VLC 无法解码此视频。\n文件可能已损坏，或不是有效的 FLV/FLASH 视频。\n您仍可使用时间输入框手动设置截取区间。": (
            "VLC cannot decode this video.\n"
            "The file may be damaged or is not a valid FLV/Flash video.\n"
            "You can still set segment times manually."
        ),
    },
    "ja": {
        "多视频拼接裁剪与压缩工具": "複数動画 トリミング＆結合ツール",
        "就绪": "準備完了",
        "没有有效的片段可截取。": "処理できる区間がありません。",
        "正在准备 {count} 个片段...": "{count} 個の区間を準備しています...",
        "FFmpeg 正在输出视频...": "FFmpeg が動画を出力しています...",
        "FFmpeg 正在输出视频... {percent}%": "FFmpeg 出力中... {percent}%",
        "FFmpeg 返回错误码 {code}\n{details}": (
            "FFmpeg エラーコード {code}\n{details}"
        ),
        "处理完成！": "処理が完了しました。",
        "视频已保存至：\n{path}": "動画を保存しました：\n{path}",
        "处理出错：{error}\n若使用 GPU 编码失败，请确认 NVIDIA 驱动正常，或切换到 CPU 软件编码。": (
            "処理に失敗しました：{error}\n"
            "GPU エンコードに失敗した場合は NVIDIA ドライバーを確認するか、"
            "CPU エンコードに切り替えてください。"
        ),
        "错误": "エラー",
        "提示": "お知らせ",
        "请先加载视频。": "先に動画を読み込んでください。",
        "起始时间必须小于结束时间。": "開始時間は終了時間より前にしてください。",
        "结束时间不能超过总时长 {duration:.1f}s。": (
            "終了時間は動画の長さ {duration:.1f} 秒を超えられません。"
        ),
        "片段 {index}: {start:.2f}s → {end:.2f}s (时长 {duration:.2f}s)": (
            "区間 {index}: {start:.2f}s → {end:.2f}s（長さ {duration:.2f}s）"
        ),
        "预览模式：仅播放选中的区间": "プレビュー：選択区間のみ再生",
        "预览模式：正常播放全部视频": "プレビュー：全体を再生",
        "文件": "ファイル",
        "视频队列": "動画キュー",
        "添加视频...": "動画を追加...",
        "移除选中": "選択を削除",
        "上移": "上へ移動",
        "下移": "下へ移動",
        "清空队列": "キューを空にする",
        "队列顺序即输出顺序；没有片段的视频会输出完整内容。": (
            "キューの順番が出力順です。区間のない動画は全体を出力します。"
        ),
        "输出文件": "出力ファイル",
        "当前视频:": "現在の動画:",
        "当前选中的视频": "選択中の動画",
        "{count} 个片段": "{count} 区間",
        "完整视频": "動画全体",
        "{index}. {name} | {duration} | {segments}": (
            "{index}. {name} | {duration} | {segments}"
        ),
        "静音导出": "音声なしで出力",
        "以下视频无法读取：\n{errors}": (
            "次の動画を読み込めません：\n{errors}"
        ),
        "请先添加至少一个视频。": "先に動画を1つ以上追加してください。",
        "没有可输出的视频。": "出力できる動画がありません。",
        "请选择输入视频": "入力動画を選択",
        "浏览输入...": "入力動画を選択...",
        "选择输出路径...": "出力先を選択...",
        "输入:": "入力:",
        "当前区间设置（用于添加）": "現在の区間設定",
        " 秒": " 秒",
        "起始:": "開始:",
        "结束:": "終了:",
        "区间列表": "区間リスト",
        "➕ 添加区间": "➕ 区間を追加",
        "➖ 删除选中": "➖ 選択を削除",
        "🗑️ 清空所有": "🗑️ すべて削除",
        "🎯 仅播放选区 (预览拼接效果)": "🎯 選択区間のみ再生",
        "未加载视频": "動画が読み込まれていません",
        "输出分辨率": "出力解像度",
        "调整分辨率": "解像度を変更",
        "原始": "元のサイズ",
        "保持宽高比": "アスペクト比を維持",
        "预设:": "プリセット:",
        "宽度:": "幅:",
        "高度:": "高さ:",
        "输出编码器": "出力エンコーダー",
        "编码器:": "エンコーダー:",
        "GPU 加速 (NVENC H.264)": "GPU (NVENC H.264)",
        "GPU 加速 (NVENC H.265)": "GPU (NVENC H.265)",
        "CPU 软件编码 (H.264)": "CPU H.264",
        "NVENC 画质:": "NVENC 画質:",
        "高 (cq 23)": "高 (cq 23)",
        "中 (cq 28)": "中 (cq 28)",
        "低 (cq 32)": "低 (cq 32)",
        "H.264 兼容性更好；H.265 压缩率更高。GPU 编码使用 NVIDIA NVENC。": (
            "H.264 は互換性が高く、H.265 は圧縮率が高いです。"
            "GPU エンコードには NVIDIA NVENC を使用します。"
        ),
        "开始处理 (拼接所有区间)": "処理を開始",
        "打开输出文件夹": "出力フォルダーを開く",
        "输出路径：未设置": "出力先: 未設定",
        "输出路径：{path}": "出力先: {path}",
        "选择视频文件": "動画ファイルを選択",
        "视频文件 (*.mp4 *.avi *.mkv *.mov *.flv *.wmv);;所有文件 (*.*)": (
            "動画ファイル (*.mp4 *.avi *.mkv *.mov *.flv *.wmv);;すべてのファイル (*.*)"
        ),
        "保存拼接视频": "結合動画を保存",
        "MP4 文件 (*.mp4);;所有文件 (*.*)": (
            "MP4 ファイル (*.mp4);;すべてのファイル (*.*)"
        ),
        "读取失败": "読み込み失敗",
        "无法加载视频信息：{error}": "動画情報を読み込めません：{error}",
        "FFprobe 读取失败": "FFprobe の読み込みに失敗しました",
        "无法从文件中读取视频时长": "動画の長さを取得できません",
        "无法从文件中读取视频分辨率": "動画の解像度を取得できません",
        "视频已加载（VLC 内核）。点击播放开始预览。": (
            "VLC で動画を読み込みました。再生をクリックしてください。"
        ),
        "▶ 播放": "▶ 再生",
        "⏸ 暂停": "⏸ 一時停止",
        "■ 停止": "■ 停止",
        "已停止": "停止しました",
        "播放结束": "再生が終了しました",
        "所有选区已播放完毕": "選択区間をすべて再生しました",
        "已标记起点：{time}": "開始位置を設定：{time}",
        "已标记终点：{time}": "終了位置を設定：{time}",
        "已清除起点/终点标记": "開始/終了マーカーを消去しました",
        "时间线缩小": "タイムラインを縮小",
        "时间线放大": "タイムラインを拡大",
        "复位": "リセット",
        "显示完整时间线": "タイムライン全体を表示",
        "点击帧线附近可定位时间；\n空白区域按住左右拖动可平移时间线": (
            "再生位置付近をクリックして移動；\n"
            "空白部分を左右にドラッグしてタイムラインを移動"
        ),
        " 帧": " フレーム",
        "左右方向键每次前进/后退的帧数": "左右キーで移動するフレーム数",
        "步长:": "ステップ:",
        "📍 标记起点": "📍 開始をマーク",
        "📍 标记终点": "📍 終了をマーク",
        "清除标记": "マーカーを消去",
        "界面主题:": "テーマ:",
        "深色主题": "ダークテーマ",
        "浅色主题": "ライトテーマ",
        "语言:": "言語:",
        "语言将在重启程序后生效。": "言語の変更は再起動後に反映されます。",
        "步进 {steps} 帧 {sign} | 第 {frame} 帧 @ {ms}ms": (
            "{steps} フレーム {sign} | {frame} フレーム目 @ {ms}ms"
        ),
        "时长 {duration} | 原始分辨率 {resolution} | 当前区间 {start:.1f}s ~ {end:.1f}s (时长 {range:.1f}s)": (
            "長さ {duration} | 元の解像度 {resolution} | "
            "区間 {start:.1f}s - {end:.1f}s（{range:.1f}s）"
        ),
        "请先选择有效的输入视频。": "有効な入力動画を選択してください。",
        "请设置输出路径。": "出力先を設定してください。",
        "请先添加至少一个截取区间。": "少なくとも1つの区間を追加してください。",
        "正在使用 CPU 软件编码（libx264）...": "CPU H.264（libx264）を使用中...",
        "正在使用 {encoder} · 画质 {quality} ...": (
            "{encoder} - {quality} を使用中..."
        ),
        "正在输出视频... {percent}%": "動画を出力中... {percent}%",
        "编码器：{encoder}\n用时：{elapsed:.2f} 秒": (
            "エンコーダー: {encoder}\n所要時間: {elapsed:.2f} 秒"
        ),
        "处理完成，用时 {elapsed:.2f} 秒 ({encoder})": (
            "完了：{elapsed:.2f} 秒（{encoder}）"
        ),
        "完成": "完了",
        "处理失败": "処理失敗",
        "正在打开 GitHub：{url}": "GitHub を開いています：{url}",
        "VLC 无法解码此视频": "VLC でこの動画をデコードできません",
        "预览失败": "プレビュー失敗",
        "VLC 无法解码此视频。\n文件可能已损坏，或不是有效的 FLV/FLASH 视频。\n您仍可使用时间输入框手动设置截取区间。": (
            "VLC でこの動画をデコードできません。\n"
            "ファイルが破損しているか、有効な FLV/Flash 動画ではありません。\n"
            "時間入力欄から区間を手動設定できます。"
        ),
    },
}


def set_language(language_code):
    global CURRENT_LANGUAGE
    CURRENT_LANGUAGE = (
        language_code if language_code in ("zh", "en", "ja") else "zh"
    )


def tr(text):
    if CURRENT_LANGUAGE == "zh":
        return text
    return TRANSLATIONS.get(CURRENT_LANGUAGE, {}).get(text, text)


def _runtime_roots():
    roots = []
    if getattr(sys, "frozen", False):
        bundle_root = getattr(sys, "_MEIPASS", "")
        if bundle_root:
            roots.append(bundle_root)
        roots.append(os.path.dirname(os.path.abspath(sys.executable)))
    else:
        roots.append(os.path.dirname(os.path.abspath(__file__)))
    return roots


def _find_runtime_file(filename):
    for root in _runtime_roots():
        candidate = os.path.join(root, filename)
        if os.path.isfile(candidate):
            return candidate
    return None


# 优先使用随程序打包的 FFmpeg，它包含 h264_nvenc / hevc_nvenc
_FFMPEG_PATH = _find_runtime_file("ffmpeg.exe") or "ffmpeg"
_FFPROBE_PATH = _find_runtime_file("ffprobe.exe") or "ffprobe"

def _find_vlc_directory():
    candidates = []
    for root in _runtime_roots():
        candidates.append(os.path.join(root, "vlc"))
    if os.name != "nt":
        return None
    candidates.extend([
        r"C:\Program Files\VideoLAN\VLC",
        r"C:\Program Files (x86)\VideoLAN\VLC",
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\VideoLAN\VLC"),
    ])
    for directory in candidates:
        if os.path.isfile(os.path.join(directory, "libvlc.dll")):
            return directory
    return None


_VLC_DIR = _find_vlc_directory()
if _VLC_DIR:
    os.environ["PYTHON_VLC_LIB_PATH"] = os.path.join(_VLC_DIR, "libvlc.dll")
    plugin_path = os.path.join(_VLC_DIR, "plugins")
    if os.path.isdir(plugin_path):
        os.environ["PYTHON_VLC_MODULE_PATH"] = plugin_path

import vlc


# ==================== FFmpeg 直接处理线程（真实进度 + 硬件编码） ====================
class ProcessThread(QThread):
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    finished = pyqtSignal(bool, str)

    def __init__(
        self,
        items,
        output_path,
        target_size,
        codec="libx264",
        preset="medium",
        ffmpeg_params=None,
        mute_audio=False,
        keep_ratio=True,
    ):
        super().__init__()
        self.items = items
        self.output_path = output_path
        self.target_size = target_size
        self.codec = codec
        self.preset = preset
        self.ffmpeg_params = ffmpeg_params
        self.mute_audio = mute_audio
        self.keep_ratio = keep_ratio

    @staticmethod
    def _parse_fraction_rate(value):
        if not value:
            return None
        try:
            if "/" in value:
                numerator, denominator = value.split("/", 1)
                numerator = float(numerator)
                denominator = float(denominator)
                if denominator:
                    return numerator / denominator
            return float(value)
        except ValueError:
            return None

    @staticmethod
    def _probe_media_info(input_path):
        fps = 25.0
        has_audio = False
        flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        try:
            result = subprocess.run(
                [
                    _FFPROBE_PATH,
                    "-v", "error",
                    "-print_format", "json",
                    "-show_streams",
                    input_path,
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=15,
                creationflags=flags,
            )
            data = json.loads(result.stdout or "{}")
            for stream in data.get("streams", []):
                codec_type = stream.get("codec_type")
                if codec_type == "video":
                    for key in ("avg_frame_rate", "r_frame_rate"):
                        parsed = ProcessThread._parse_fraction_rate(
                            stream.get(key)
                        )
                        if parsed:
                            fps = parsed
                            break
                elif codec_type == "audio":
                    has_audio = True
        except Exception:
            pass
        return fps, has_audio

    def run(self):
        try:
            valid_items = []
            for item in self.items:
                duration = float(item.get("duration") or 0)
                segments = [
                    (float(start), float(end))
                    for start, end in item.get("segments", [])
                    if end > start
                ]
                if not segments and duration > 0:
                    segments = [(0.0, duration)]
                if not segments:
                    continue
                normalized = dict(item)
                normalized["segments"] = segments
                valid_items.append(normalized)

            if not valid_items:
                raise ValueError(tr("没有有效的片段可截取。"))

            first_item = valid_items[0]
            if self.target_size:
                target_w, target_h = self.target_size
            else:
                target_w, target_h = first_item.get(
                    "resolution", (1280, 720)
                )
            target_w = int(target_w or 1280)
            target_h = int(target_h or 720)
            if target_w % 2 == 1:
                target_w += 1
            if target_h % 2 == 1:
                target_h += 1

            output_fps = float(first_item.get("fps") or 30.0)
            output_has_audio = (
                not self.mute_audio
                and any(item.get("has_audio") for item in valid_items)
            )
            segment_count = sum(
                len(item["segments"]) for item in valid_items
            )

            self.status_updated.emit(
                tr("正在准备 {count} 个片段...").format(
                    count=segment_count
                )
            )
            filter_parts = []
            concat_inputs = []
            output_index = 0
            for input_index, item in enumerate(valid_items):
                for start, end in item["segments"]:
                    video_chain = (
                        f"[{input_index}:v:0]"
                        f"trim=start={start:.6f}:end={end:.6f},"
                        "setpts=PTS-STARTPTS"
                    )
                    if self.keep_ratio:
                        video_chain += (
                            f",scale={target_w}:{target_h}:"
                            "force_original_aspect_ratio=decrease:"
                            "flags=lanczos"
                            f",pad={target_w}:{target_h}:"
                            "(ow-iw)/2:(oh-ih)/2:color=black"
                        )
                    else:
                        video_chain += (
                            f",scale={target_w}:{target_h}:flags=lanczos"
                        )
                    video_chain += (
                        f",setsar=1,fps={output_fps:.6f},"
                        f"format=yuv420p[v{output_index}]"
                    )
                    filter_parts.append(video_chain)
                    concat_inputs.append(f"[v{output_index}]")

                    if output_has_audio:
                        if item.get("has_audio"):
                            audio_chain = (
                                f"[{input_index}:a:0]"
                                f"atrim=start={start:.6f}:end={end:.6f},"
                                "asetpts=PTS-STARTPTS,"
                                "aresample=48000,"
                                "aformat=sample_fmts=fltp:"
                                "channel_layouts=stereo"
                            )
                        else:
                            audio_chain = (
                                "anullsrc=channel_layout=stereo:"
                                "sample_rate=48000,"
                                f"atrim=duration={max(0.001, end - start):.6f},"
                                "asetpts=PTS-STARTPTS"
                            )
                        audio_chain += f"[a{output_index}]"
                        filter_parts.append(audio_chain)
                        concat_inputs.append(f"[a{output_index}]")

                    output_index += 1

            if output_has_audio:
                concat_part = (
                    "".join(concat_inputs)
                    + f"concat=n={segment_count}:v=1:a=1[vout][aout]"
                )
            else:
                concat_part = (
                    "".join(concat_inputs)
                    + f"concat=n={segment_count}:v=1:a=0[vout]"
                )
            filter_graph = ";".join(filter_parts) + ";" + concat_part

            command = [
                _FFMPEG_PATH,
                "-hide_banner",
                "-y",
                "-nostdin",
                "-nostats",
                "-progress", "pipe:1",
            ]
            for item in valid_items:
                command.extend(["-i", item["path"]])
            command.extend([
                "-filter_complex", filter_graph,
                "-map", "[vout]",
            ])
            if output_has_audio:
                command.extend([
                    "-map", "[aout]",
                    "-c:a", "aac",
                    "-b:a", "192k",
                ])
            else:
                command.append("-an")
            command.extend(["-c:v", self.codec])
            if self.preset:
                command.extend(["-preset", self.preset])
            if self.ffmpeg_params:
                command.extend(self.ffmpeg_params)
            command.extend([
                "-pix_fmt", "yuv420p",
                "-r", f"{output_fps:.6f}",
                "-movflags", "+faststart",
                self.output_path,
            ])

            self.status_updated.emit(tr("FFmpeg 正在输出视频..."))
            flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1,
                creationflags=flags,
            )

            total_duration = max(
                0.000001,
                sum(
                    end - start
                    for item in valid_items
                    for start, end in item["segments"]
                ),
            )
            last_percent = -1
            while True:
                line = process.stdout.readline()
                if not line:
                    break
                line = line.strip()
                if line.startswith("out_time_us="):
                    try:
                        elapsed_us = int(line.split("=", 1)[1])
                        percent = max(
                            0,
                            min(
                                99,
                                int(elapsed_us / 1_000_000 / total_duration * 100),
                            ),
                        )
                    except ValueError:
                        percent = 0
                    if percent != last_percent:
                        last_percent = percent
                        self.progress_updated.emit(percent)
                        self.status_updated.emit(
                            tr("FFmpeg 正在输出视频... {percent}%").format(
                                percent=percent
                            )
                        )

            error_text = ""
            if process.stderr:
                error_text = process.stderr.read()
            return_code = process.wait()
            if return_code != 0:
                raise RuntimeError(
                    tr(
                        "FFmpeg 返回错误码 {code}\n{details}"
                    ).format(
                        code=return_code,
                        details=error_text[-3000:],
                    )
                )

            self.progress_updated.emit(100)
            self.status_updated.emit(tr("处理完成！"))
            self.finished.emit(
                True,
                tr("视频已保存至：\n{path}").format(
                    path=self.output_path
                ),
            )

        except Exception as exc:
            error_message = tr(
                "处理出错：{error}\n"
                "若使用 GPU 编码失败，请确认 NVIDIA 驱动正常，"
                "或切换到 CPU 软件编码。"
            ).format(
                error=exc
            )
            self.finished.emit(False, error_message)


# ==================== 多区间显示控件 ====================
class MultiRangeBar(QWidget):
    positionClicked = pyqtSignal(float)
    viewPanned = pyqtSignal(float, float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(20)
        self.segments = []
        self.duration = 0.0
        self.position_ratio = 0.0
        self.position_sec = 0.0
        self.marker_start = None
        self.marker_end = None
        self.view_start = 0.0
        self.view_end = 0.0
        self._drag_mode = None
        self._drag_start_x = 0.0
        self._drag_start_view = (0.0, 0.0)
        self._drag_moved = False
        self.colors = [
            QColor(0, 200, 0, 120),
            QColor(0, 150, 255, 120),
            QColor(255, 200, 0, 120),
            QColor(255, 80, 80, 120),
            QColor(200, 50, 200, 120)
        ]
        self.setMinimumWidth(100)

    def set_segments(self, segments, duration):
        self.segments = sorted(segments, key=lambda x: x[0])
        self.duration = duration
        self.update()

    def set_view(self, start_sec, end_sec):
        self.view_start = max(0.0, start_sec)
        self.view_end = max(self.view_start, end_sec)
        self.update()

    def set_markers(self, start_sec, end_sec):
        self.marker_start = start_sec
        self.marker_end = end_sec
        self.update()

    def clear_markers(self):
        self.marker_start = None
        self.marker_end = None
        self.update()

    def set_position(self, pos_sec):
        self.position_sec = max(0.0, pos_sec)
        if self.duration > 0:
            self.position_ratio = max(
                0.0, min(1.0, pos_sec / self.duration)
            )
        else:
            self.position_ratio = 0.0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        painter.fillRect(rect, QColor(40, 40, 40))

        view_start = self.view_start
        view_end = self.view_end
        if view_end <= view_start:
            view_start = 0.0
            view_end = self.duration or 1.0
        view_duration = view_end - view_start

        for idx, (start, end) in enumerate(self.segments):
            if view_duration <= 0:
                continue
            draw_start = max(start, view_start)
            draw_end = min(end, view_end)
            if draw_end <= draw_start:
                continue
            left = int(
                rect.left()
                + (draw_start - view_start) / view_duration * rect.width()
            )
            right = int(
                rect.left()
                + (draw_end - view_start) / view_duration * rect.width()
            )
            if left < right:
                color = self.colors[idx % len(self.colors)]
                range_rect = QRectF(left, rect.top(), right - left, rect.height())
                painter.fillRect(range_rect, color)

        if (
            self.marker_start is not None
            and self.marker_end is not None
            and self.marker_end > self.marker_start
        ):
            draw_start = max(self.marker_start, view_start)
            draw_end = min(self.marker_end, view_end)
            if draw_end > draw_start:
                left = int(
                    rect.left()
                    + (draw_start - view_start)
                    / view_duration
                    * rect.width()
                )
                right = int(
                    rect.left()
                    + (draw_end - view_start)
                    / view_duration
                    * rect.width()
                )
                painter.fillRect(
                    QRectF(left, rect.top(), right - left, rect.height()),
                    QColor(0, 220, 255, 85),
                )

        for marker, color in (
            (self.marker_start, QColor(255, 220, 0)),
            (self.marker_end, QColor(255, 80, 80)),
        ):
            if marker is None or not (view_start <= marker <= view_end):
                continue
            marker_x = int(
                rect.left()
                + (marker - view_start) / view_duration * rect.width()
            )
            painter.setPen(QPen(color, 3))
            painter.drawLine(marker_x, rect.top(), marker_x, rect.bottom())
            painter.fillRect(
                QRectF(marker_x - 2, rect.top(), 5, 5), color
            )

        if view_start <= self.position_sec <= view_end:
            position_in_view = (
                self.position_sec - view_start
            ) / view_duration
            pos_x = int(rect.left() + position_in_view * rect.width())
            painter.setPen(QPen(QColor(255, 255, 255), 2))
            painter.drawLine(pos_x, rect.top(), pos_x, rect.bottom())

        painter.setPen(QPen(QColor(80, 80, 80), 1))
        painter.drawRect(rect)

    def _position_from_event(self, event):
        view_start = self.view_start
        view_end = self.view_end
        if view_end <= view_start:
            view_start = 0.0
            view_end = self.duration or 1.0
        view_duration = view_end - view_start
        if view_duration <= 0 or self.width() <= 0:
            return
        ratio = event.position().x() / self.width()
        ratio = max(0.0, min(1.0, ratio))
        position_sec = view_start + ratio * view_duration
        self.set_position(position_sec)
        self.positionClicked.emit(position_sec)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start_x = event.position().x()
            self._drag_start_view = (self.view_start, self.view_end)
            self._drag_moved = False

            view_start = self.view_start
            view_end = self.view_end
            if view_end <= view_start:
                view_start = 0.0
                view_end = self.duration or 1.0
            view_duration = view_end - view_start
            playhead_x = None
            if (
                view_duration > 0
                and view_start <= self.position_sec <= view_end
            ):
                playhead_x = self.width() * (
                    self.position_sec - view_start
                ) / view_duration

            if (
                playhead_x is not None
                and abs(self._drag_start_x - playhead_x) <= 6
            ):
                self._drag_mode = "seek"
                self._position_from_event(event)
            else:
                self._drag_mode = "pan"
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            dx = event.position().x() - self._drag_start_x
            if abs(dx) > 3:
                self._drag_moved = True

            if self._drag_mode == "seek":
                self._position_from_event(event)
            elif self._drag_mode == "pan" and self._drag_moved:
                view_start, view_end = self._drag_start_view
                view_duration = view_end - view_start
                if view_duration > 0 and self.width() > 0:
                    delta = dx / self.width() * view_duration
                    new_start = view_start - delta
                    duration = self.duration or view_duration
                    new_start = max(
                        0.0, min(duration - view_duration, new_start)
                    )
                    new_end = new_start + view_duration
                    self.set_view(new_start, new_end)
                    self.viewPanned.emit(new_start, new_end)
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self._drag_mode == "pan" and not self._drag_moved:
                self._position_from_event(event)
            self._drag_mode = None
            self._drag_moved = False
            event.accept()
        else:
            super().mouseReleaseEvent(event)


# ==================== 主窗口 ====================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(
            tr("多视频拼接裁剪与压缩工具")
        )
        self.setMinimumSize(1100, 750)

        self.input_path = ""
        self.output_path = ""
        self._output_path_manual = False
        self.clips = []
        self.current_clip_index = -1
        self._clip_sequence = 0
        self.video_duration = 0.0
        self.video_resolution = (0, 0)
        self.video_fps = 25.0
        self.has_audio = False
        self.original_ratio = 1.0
        self._updating_spins = False
        self.segments = []
        self.marker_start_sec = None
        self.marker_end_sec = None
        self.preview_mode = False
        self.timeline_view = (0.0, 0.0)
        self.zoom_factor = 1.0

        self._setup_ui()
        self._connect_signals()
        self._restore_splitter_sizes()
        self._application = QApplication.instance()
        if self._application is not None:
            self._application.installEventFilter(self)

        self.video_widget = QFrame()
        self.video_widget.setObjectName("previewVideo")
        self.video_widget.setAttribute(Qt.WidgetAttribute.WA_NativeWindow, True)
        self.video_widget.setMinimumSize(480, 280)
        self.video_widget.setStyleSheet(
            "#previewVideo { background-color: #000000; border: 1px solid #666666; }"
        )
        self.preview_layout.insertWidget(0, self.video_widget)

        self.vlc_instance = vlc.Instance(
            ["--quiet", "--no-video-title-show", "--no-video-on-top"]
        )
        self.vlc_player = self.vlc_instance.media_player_new()
        self.current_vlc_media = None
        self._vlc_output_bound = False
        self._vlc_error_shown = False
        self._vlc_end_notified = False
        self._pending_frame_position_ms = None
        self._frame_step_generation = 0
        QTimer.singleShot(0, self._bind_vlc_output)

        self.vlc_refresh_timer = QTimer(self)
        self.vlc_refresh_timer.setInterval(120)
        self.vlc_refresh_timer.timeout.connect(self._on_vlc_timer)
        self.vlc_refresh_timer.start()

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage(tr("就绪"))
        self.apply_theme(self.theme_combo.currentIndex())

    def apply_theme(self, theme_index):
        self.setStyleSheet(
            DARK_STYLE if theme_index == 0 else LIGHT_STYLE
        )
        self._apply_window_frame_theme()

    def _restore_splitter_sizes(self):
        settings = QSettings(GITHUB_USER, APP_NAME)
        saved = settings.value("layout/splitter_sizes", "760,400")
        try:
            left, right = [int(value) for value in str(saved).split(",", 1)]
        except (TypeError, ValueError):
            return
        if left > 300 and right > 300:
            self.main_splitter.setSizes([left, right])

    def _apply_window_frame_theme(self):
        if os.name != "nt":
            return
        try:
            hwnd = int(self.winId())
            enabled = ctypes.c_int(
                1 if self.theme_combo.currentIndex() == 0 else 0
            )
            for attribute in (20, 19):
                result = ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    attribute,
                    ctypes.byref(enabled),
                    ctypes.sizeof(enabled),
                )
                if result == 0:
                    break
        except Exception:
            pass

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(0, self._apply_window_frame_theme)

    def change_language(self, language_index):
        language_code = ("zh", "en", "ja")[language_index]
        settings = QSettings(GITHUB_USER, APP_NAME)
        settings.setValue("language", language_code)
        QMessageBox.information(
            self,
            tr("提示"),
            tr("语言将在重启程序后生效。"),
        )

    def _bind_vlc_output(self):
        if self._vlc_output_bound:
            return
        hwnd = int(self.video_widget.winId())
        if hwnd:
            self.vlc_player.set_hwnd(hwnd)
            self._vlc_output_bound = True

    def _vlc_position_ms(self):
        return max(0, self.vlc_player.get_time())

    def _vlc_duration_ms(self):
        return max(0, self.vlc_player.get_length())

    def _safe_stop_vlc(self):
        state = self.vlc_player.get_state()
        if state in (
            vlc.State.Playing,
            vlc.State.Opening,
            vlc.State.Buffering,
        ):
            self.vlc_player.set_pause(1)
        self.vlc_player.stop()

    def _clear_preview_media(self):
        self.vlc_refresh_timer.stop()
        self._safe_stop_vlc()
        try:
            self.vlc_player.set_media(None)
        except Exception:
            pass
        if self.current_vlc_media is not None:
            try:
                self.current_vlc_media.release()
            except Exception:
                pass
            self.current_vlc_media = None
        self._vlc_error_shown = False
        self._vlc_end_notified = False
        self._pending_frame_position_ms = None
        self._frame_step_generation += 1

    def _on_vlc_timer(self):
        if not hasattr(self, "vlc_player"):
            return
        self._bind_vlc_output()

        state = self.vlc_player.get_state()
        if state == vlc.State.Stopped:
            return
        if state == vlc.State.NothingSpecial and self.video_duration <= 0:
            return
        if state == vlc.State.Error:
            if not self._vlc_error_shown:
                self._vlc_error_shown = True
                self.status_bar.showMessage(
                    tr("VLC 无法解码此视频")
                )
                QMessageBox.warning(
                    self,
                    tr("预览失败"),
                    tr(
                        "VLC 无法解码此视频。\n"
                        "文件可能已损坏，或不是有效的 FLV/FLASH 视频。\n"
                        "您仍可使用时间输入框手动设置截取区间。"
                    ),
                )
            return

        position_ms = self._vlc_position_ms()
        duration_ms = self._vlc_duration_ms()
        if duration_ms <= 0 and self.video_duration > 0:
            duration_ms = int(self.video_duration * 1000)

        if duration_ms > 0:
            self.position_slider.setEnabled(True)
            slider_value = int(position_ms * 1000 / duration_ms)
            if not self.position_slider.isSliderDown():
                self.position_slider.setValue(min(1000, slider_value))
            self.multi_range_bar.set_position(position_ms / 1000.0)
            self.update_time_label(position_ms, duration_ms)

        if state == vlc.State.Playing:
            self.btn_play.setText(tr("⏸ 暂停"))
            if self._vlc_end_notified:
                self._vlc_end_notified = False
        elif state == vlc.State.Paused:
            self.btn_play.setText(tr("▶ 播放"))
        elif state == vlc.State.Ended:
            self.btn_play.setText(tr("▶ 播放"))
            if duration_ms > 0:
                self.position_slider.setValue(1000)
                self.update_time_label(duration_ms, duration_ms)
            if not self._vlc_end_notified:
                self._vlc_end_notified = True
                self.status_bar.showMessage(tr("播放结束"))
            return

        if state == vlc.State.Playing and self.preview_mode and self.segments:
            pos_sec = position_ms / 1000.0
            if not self.is_position_in_segments(pos_sec):
                next_start = self.get_next_segment_start(pos_sec)
                if next_start is not None:
                    self.vlc_player.set_time(int(next_start * 1000))
                else:
                    self.vlc_player.set_pause(1)
                    self.status_bar.showMessage(
                        tr("所有选区已播放完毕")
                    )

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(6, 6, 6, 6)
        main_layout.setSpacing(0)
        self.main_splitter = QSplitter(
            Qt.Orientation.Horizontal, central_widget
        )
        self.main_splitter.setChildrenCollapsible(False)
        self.main_splitter.setHandleWidth(6)

        # 左侧预览
        left_panel = QWidget()
        left_panel.setMinimumWidth(500)
        left_layout = QVBoxLayout(left_panel)
        self.preview_layout = QVBoxLayout()
        left_layout.addLayout(self.preview_layout, 1)

        control_layout = QVBoxLayout()
        row1 = QHBoxLayout()
        self.btn_play = QPushButton(tr("▶ 播放"))
        self.btn_stop = QPushButton(tr("■ 停止"))
        self.time_label = QLabel("00:00 / 00:00")
        self.position_slider = QSlider(Qt.Orientation.Horizontal)
        self.position_slider.setRange(0, 1000)
        self.position_slider.setEnabled(False)

        row1.addWidget(self.btn_play)
        row1.addWidget(self.btn_stop)
        row1.addWidget(self.position_slider, 1)
        row1.addWidget(self.time_label)
        control_layout.addLayout(row1)

        timeline_row = QHBoxLayout()
        timeline_row.setSpacing(5)
        self.multi_range_bar = MultiRangeBar()
        self.multi_range_bar.setToolTip(
            tr(
                "点击帧线附近可定位时间；\n"
                "空白区域按住左右拖动可平移时间线"
            )
        )
        timeline_row.addWidget(self.multi_range_bar, 1)
        self.btn_zoom_out = QPushButton("−", self)
        self.btn_zoom_out.setFixedWidth(32)
        self.btn_zoom_out.setToolTip(tr("时间线缩小"))
        self.zoom_label = QLabel("ZOOM x1", self)
        self.zoom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.zoom_label.setMinimumWidth(64)
        self.btn_zoom_in = QPushButton("＋", self)
        self.btn_zoom_in.setFixedWidth(32)
        self.btn_zoom_in.setToolTip(tr("时间线放大"))
        self.btn_zoom_fit = QPushButton(tr("复位"), self)
        self.btn_zoom_fit.setToolTip(tr("显示完整时间线"))
        self.frame_step_spin = QSpinBox(self)
        self.frame_step_spin.setRange(1, 9999)
        self.frame_step_spin.setValue(1)
        self.frame_step_spin.setSuffix(tr(" 帧"))
        self.frame_step_spin.setFixedWidth(72)
        self.frame_step_spin.setToolTip(
            tr("左右方向键每次前进/后退的帧数")
        )
        timeline_row.addWidget(self.btn_zoom_out)
        timeline_row.addWidget(self.zoom_label)
        timeline_row.addWidget(self.btn_zoom_in)
        timeline_row.addWidget(self.btn_zoom_fit)
        timeline_row.addSpacing(8)
        timeline_row.addWidget(QLabel(tr("步长:"), self))
        timeline_row.addWidget(self.frame_step_spin)
        control_layout.addLayout(timeline_row)
        left_layout.addLayout(control_layout)

        mark_layout = QHBoxLayout()
        self.btn_mark_start = QPushButton(tr("📍 标记起点"))
        self.btn_mark_end = QPushButton(tr("📍 标记终点"))
        self.btn_clear_markers = QPushButton(tr("清除标记"))
        self.btn_mark_start.setEnabled(False)
        self.btn_mark_end.setEnabled(False)
        self.btn_clear_markers.setEnabled(False)
        mark_layout.addWidget(self.btn_mark_start)
        mark_layout.addWidget(self.btn_mark_end)
        mark_layout.addStretch()
        mark_layout.addWidget(self.btn_clear_markers)
        left_layout.addLayout(mark_layout)

        self.main_splitter.addWidget(left_panel)

        # 右侧控制面板
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)

        theme_row = QHBoxLayout()
        theme_row.addWidget(QLabel(tr("界面主题:")))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems([
            tr("深色主题"),
            tr("浅色主题"),
        ])
        self.theme_combo.setCurrentIndex(0)
        theme_row.addWidget(self.theme_combo, 1)
        right_layout.addLayout(theme_row)

        language_row = QHBoxLayout()
        language_row.addWidget(QLabel(tr("语言:")))
        self.language_combo = QComboBox()
        self.language_combo.addItems(["中文", "English", "日本語"])
        language_index = {"zh": 0, "en": 1, "ja": 2}.get(
            CURRENT_LANGUAGE, 0
        )
        self.language_combo.setCurrentIndex(language_index)
        language_row.addWidget(self.language_combo, 1)
        self.github_button = QPushButton(f"GitHub: {GITHUB_USER}")
        self.github_button.setToolTip(GITHUB_URL)
        self.github_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )
        language_row.addWidget(self.github_button)
        right_layout.addLayout(language_row)

        # 视频队列
        queue_group = QGroupBox(tr("视频队列"))
        queue_layout = QVBoxLayout()
        self.clip_list = QListWidget()
        self.clip_list.setMaximumHeight(120)
        self.clip_list.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.clip_list.setDragDropMode(
            QAbstractItemView.DragDropMode.InternalMove
        )
        self.clip_list.setDefaultDropAction(Qt.DropAction.MoveAction)
        queue_layout.addWidget(self.clip_list)

        self.btn_browse_input = QPushButton(tr("添加视频..."))
        self.btn_remove_clip = QPushButton(tr("移除选中"))
        self.btn_move_clip_up = QPushButton(tr("上移"))
        self.btn_move_clip_down = QPushButton(tr("下移"))
        self.btn_clear_clips = QPushButton(tr("清空队列"))
        queue_button_row1 = QHBoxLayout()
        queue_button_row1.addWidget(self.btn_browse_input)
        queue_button_row1.addWidget(self.btn_remove_clip)
        queue_button_row1.addWidget(self.btn_clear_clips)
        queue_layout.addLayout(queue_button_row1)
        queue_button_row2 = QHBoxLayout()
        queue_button_row2.addWidget(self.btn_move_clip_up)
        queue_button_row2.addWidget(self.btn_move_clip_down)
        queue_button_row2.addStretch()
        queue_layout.addLayout(queue_button_row2)
        self.queue_hint = QLabel(
            tr("队列顺序即输出顺序；没有片段的视频会输出完整内容。")
        )
        self.queue_hint.setWordWrap(True)
        queue_layout.addWidget(self.queue_hint)
        queue_group.setLayout(queue_layout)
        right_layout.addWidget(queue_group)

        # 输出文件
        file_group = QGroupBox(tr("输出文件"))
        file_layout = QVBoxLayout()
        self.input_label = QLineEdit()
        self.input_label.setReadOnly(True)
        self.input_label.setPlaceholderText(tr("当前选中的视频"))
        self.btn_browse_output = QPushButton(tr("选择输出路径..."))
        file_layout.addWidget(QLabel(tr("当前视频:")))
        file_layout.addWidget(self.input_label)
        file_layout.addWidget(self.btn_browse_output)
        file_group.setLayout(file_layout)
        right_layout.addWidget(file_group)

        # 单区间设置
        time_group = QGroupBox(tr("当前区间设置（用于添加）"))
        time_form = QFormLayout()
        self.start_spin = QDoubleSpinBox()
        self.start_spin.setRange(0, 99999)
        self.start_spin.setSingleStep(0.5)
        self.start_spin.setSuffix(tr(" 秒"))
        self.end_spin = QDoubleSpinBox()
        self.end_spin.setRange(0, 99999)
        self.end_spin.setSingleStep(0.5)
        self.end_spin.setSuffix(tr(" 秒"))
        self.start_spin.setValue(0.0)
        self.end_spin.setValue(10.0)
        time_form.addRow(tr("起始:"), self.start_spin)
        time_form.addRow(tr("结束:"), self.end_spin)
        time_group.setLayout(time_form)
        right_layout.addWidget(time_group)

        # 区间管理
        seg_group = QGroupBox(tr("区间列表"))
        seg_layout = QVBoxLayout()
        self.seg_list = QListWidget()
        self.seg_list.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        seg_layout.addWidget(self.seg_list)

        btn_layout = QHBoxLayout()
        self.btn_add_seg = QPushButton(tr("➕ 添加区间"))
        self.btn_del_seg = QPushButton(tr("➖ 删除选中"))
        self.btn_clear_seg = QPushButton(tr("🗑️ 清空所有"))
        btn_layout.addWidget(self.btn_add_seg)
        btn_layout.addWidget(self.btn_del_seg)
        btn_layout.addWidget(self.btn_clear_seg)
        seg_layout.addLayout(btn_layout)

        self.cb_preview_only = QCheckBox(
            tr("🎯 仅播放选区 (预览拼接效果)")
        )
        self.cb_preview_only.setChecked(False)
        seg_layout.addWidget(self.cb_preview_only)

        seg_group.setLayout(seg_layout)
        right_layout.addWidget(seg_group)

        self.info_label = QLabel(tr("未加载视频"))
        right_layout.addWidget(self.info_label)

        # 分辨率
        res_group = QGroupBox(tr("输出分辨率"))
        res_layout = QVBoxLayout()
        row1 = QHBoxLayout()
        self.cb_resize = QCheckBox(tr("调整分辨率"))
        self.cb_resize.setChecked(True)
        self.preset_combo = QComboBox()
        self.preset_combo.addItems([
            tr("原始"),
            "720P",
            "480P",
        ])
        self.cb_keep_ratio = QCheckBox(tr("保持宽高比"))
        self.cb_keep_ratio.setChecked(True)
        row1.addWidget(self.cb_resize)
        row1.addWidget(QLabel(tr("预设:")))
        row1.addWidget(self.preset_combo)
        row1.addWidget(self.cb_keep_ratio)
        row1.addStretch()
        res_layout.addLayout(row1)

        row2 = QHBoxLayout()
        self.width_spin = QSpinBox()
        self.width_spin.setRange(1, 9999)
        self.width_spin.setValue(640)
        self.height_spin = QSpinBox()
        self.height_spin.setRange(1, 9999)
        self.height_spin.setValue(480)
        row2.addWidget(QLabel(tr("宽度:")))
        row2.addWidget(self.width_spin)
        row2.addWidget(QLabel(tr("高度:")))
        row2.addWidget(self.height_spin)
        row2.addStretch()
        res_layout.addLayout(row2)
        res_group.setLayout(res_layout)
        right_layout.addWidget(res_group)

        encoder_group = QGroupBox(tr("输出编码器"))
        encoder_layout = QVBoxLayout()
        encoder_row = QHBoxLayout()
        encoder_row.addWidget(QLabel(tr("编码器:")))
        self.encoder_combo = QComboBox()
        self.encoder_combo.addItems([
            tr("GPU 加速 (NVENC H.264)"),
            tr("GPU 加速 (NVENC H.265)"),
            tr("CPU 软件编码 (H.264)"),
        ])
        self.encoder_combo.setCurrentIndex(1)
        encoder_row.addWidget(self.encoder_combo, 1)
        encoder_layout.addLayout(encoder_row)
        quality_row = QHBoxLayout()
        quality_row.addWidget(QLabel(tr("NVENC 画质:")))
        self.quality_combo = QComboBox()
        self.quality_combo.addItems([
            tr("高 (cq 23)"),
            tr("中 (cq 28)"),
            tr("低 (cq 32)"),
        ])
        self.quality_combo.setCurrentIndex(1)
        quality_row.addWidget(self.quality_combo, 1)
        encoder_layout.addLayout(quality_row)
        self.cb_mute_export = QCheckBox(tr("静音导出"))
        self.cb_mute_export.setChecked(False)
        encoder_layout.addWidget(self.cb_mute_export)
        self.encoder_hint = QLabel(
            tr(
                "H.264 兼容性更好；H.265 压缩率更高。"
                "GPU 编码使用 NVIDIA NVENC。"
            )
        )
        self.encoder_hint.setWordWrap(True)
        encoder_layout.addWidget(self.encoder_hint)
        encoder_group.setLayout(encoder_layout)
        right_layout.addWidget(encoder_group)

        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        right_layout.addWidget(self.progress_bar)

        self.btn_start = QPushButton(tr("开始处理 (拼接所有区间)"))
        self.btn_start.setMinimumHeight(40)
        self.btn_open_folder = QPushButton(tr("打开输出文件夹"))
        self.btn_open_folder.setEnabled(False)
        btn_ops = QHBoxLayout()
        btn_ops.addWidget(self.btn_start)
        btn_ops.addWidget(self.btn_open_folder)
        right_layout.addLayout(btn_ops)

        self.output_path_label = QLabel(tr("输出路径：未设置"))
        self.output_path_label.setWordWrap(True)
        right_layout.addWidget(self.output_path_label)

        right_scroll = QScrollArea()
        self.right_scroll = right_scroll
        right_scroll.setWidgetResizable(True)
        right_scroll.setFrameShape(QFrame.Shape.NoFrame)
        right_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        right_scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        right_scroll.setMinimumWidth(340)
        right_panel.setMinimumWidth(340)
        right_scroll.setWidget(right_panel)
        self.main_splitter.addWidget(right_scroll)
        self.main_splitter.setStretchFactor(0, 1)
        self.main_splitter.setStretchFactor(1, 0)
        self.main_splitter.setSizes([760, 400])
        main_layout.addWidget(self.main_splitter)

    def _connect_signals(self):
        self.theme_combo.currentIndexChanged.connect(self.apply_theme)
        self.language_combo.currentIndexChanged.connect(
            self.change_language
        )
        self.github_button.clicked.connect(self.open_github)
        self.clip_list.itemClicked.connect(self.on_clip_selected)
        self.clip_list.model().rowsMoved.connect(
            self.on_clip_rows_moved
        )
        self.btn_remove_clip.clicked.connect(self.remove_selected_clip)
        self.btn_move_clip_up.clicked.connect(
            lambda: self.move_selected_clip(-1)
        )
        self.btn_move_clip_down.clicked.connect(
            lambda: self.move_selected_clip(1)
        )
        self.btn_clear_clips.clicked.connect(self.clear_clips)
        self.btn_browse_input.clicked.connect(self.browse_input)
        self.btn_browse_output.clicked.connect(self.browse_output)
        self.btn_start.clicked.connect(self.start_processing)
        self.btn_open_folder.clicked.connect(self.open_output_folder)
        self.encoder_combo.currentIndexChanged.connect(self.on_encoder_changed)
        self.quality_combo.currentIndexChanged.connect(
            self.update_auto_output_path
        )

        self.cb_resize.toggled.connect(self.on_resize_toggled)
        self.preset_combo.currentIndexChanged.connect(self.on_preset_changed)
        self.cb_keep_ratio.toggled.connect(self.on_keep_ratio_toggled)

        self.input_label.textChanged.connect(self.auto_set_output_path)

        self.btn_add_seg.clicked.connect(self.add_segment)
        self.btn_del_seg.clicked.connect(self.delete_segment)
        self.btn_clear_seg.clicked.connect(self.clear_segments)
        self.seg_list.itemClicked.connect(self.on_segment_selected)

        self.cb_preview_only.toggled.connect(self.on_preview_mode_toggled)

        self.width_spin.valueChanged.connect(self.on_width_changed)
        self.height_spin.valueChanged.connect(self.on_height_changed)

        self.btn_play.clicked.connect(self.toggle_play)
        self.btn_stop.clicked.connect(self.stop_play)
        self.position_slider.sliderMoved.connect(self.set_position)
        self.position_slider.sliderReleased.connect(
            lambda: self.set_position(self.position_slider.value())
        )
        self.btn_zoom_in.clicked.connect(lambda: self.zoom_timeline(True))
        self.btn_zoom_out.clicked.connect(lambda: self.zoom_timeline(False))
        self.btn_zoom_fit.clicked.connect(self.reset_timeline_zoom)
        self.multi_range_bar.positionClicked.connect(
            self.seek_to_timeline_position
        )
        self.multi_range_bar.viewPanned.connect(
            self.on_timeline_view_panned
        )

        self.btn_mark_start.clicked.connect(self.mark_start)
        self.btn_mark_end.clicked.connect(self.mark_end)
        self.btn_clear_markers.clicked.connect(self.clear_markers)

        self.start_spin.valueChanged.connect(self.update_info_label)
        self.end_spin.valueChanged.connect(self.update_info_label)

    # ---------- 区间管理 ----------
    def add_segment(self):
        if self.video_duration <= 0:
            QMessageBox.warning(
                self, tr("错误"), tr("请先加载视频。")
            )
            return
        start = self.start_spin.value()
        end = self.end_spin.value()
        if start >= end:
            QMessageBox.warning(
                self,
                tr("错误"),
                tr("起始时间必须小于结束时间。"),
            )
            return
        if end > self.video_duration:
            QMessageBox.warning(
                self,
                tr("错误"),
                tr("结束时间不能超过总时长 {duration:.1f}s。").format(
                    duration=self.video_duration
                ),
            )
            return
        self.segments.append((start, end))
        self.segments.sort(key=lambda x: x[0])
        self.refresh_segment_list()
        self.update_range_bar()
        self.refresh_clip_list(
            select_id=self._current_clip_id()
        )

    def delete_segment(self):
        current_item = self.seg_list.currentItem()
        if current_item:
            idx = self.seg_list.row(current_item)
            if 0 <= idx < len(self.segments):
                del self.segments[idx]
                self.refresh_segment_list()
                self.update_range_bar()
                self.refresh_clip_list(
                    select_id=self._current_clip_id()
                )

    def clear_segments(self):
        self.segments.clear()
        self.refresh_segment_list()
        self.update_range_bar()
        self.refresh_clip_list(select_id=self._current_clip_id())

    def refresh_segment_list(self):
        self.seg_list.clear()
        for i, (start, end) in enumerate(self.segments):
            item = QListWidgetItem(
                tr(
                    "片段 {index}: {start:.2f}s → {end:.2f}s "
                    "(时长 {duration:.2f}s)"
                ).format(
                    index=i + 1,
                    start=start,
                    end=end,
                    duration=end - start,
                )
            )
            self.seg_list.addItem(item)

    def on_segment_selected(self, item):
        idx = self.seg_list.row(item)
        if 0 <= idx < len(self.segments):
            start, end = self.segments[idx]
            self.marker_start_sec = start
            self.marker_end_sec = end
            self.start_spin.setValue(start)
            self.end_spin.setValue(end)
            self._sync_marker_display()

    def update_range_bar(self):
        if self.video_duration > 0:
            self.multi_range_bar.set_segments(self.segments, self.video_duration)
            view_start, view_end = self.timeline_view
            if view_end <= view_start:
                view_start = 0.0
                view_end = self.video_duration
            self.multi_range_bar.set_view(view_start, view_end)
            pos = self._vlc_position_ms() / 1000.0
            self.multi_range_bar.set_position(pos)

    def reset_timeline_zoom(self):
        if self.video_duration <= 0:
            return
        self.timeline_view = (0.0, self.video_duration)
        self.zoom_factor = 1.0
        self._refresh_timeline_view()

    def on_timeline_view_panned(self, start_sec, end_sec):
        if self.video_duration <= 0:
            return
        start_sec = max(0.0, min(self.video_duration, start_sec))
        end_sec = max(start_sec, min(self.video_duration, end_sec))
        if end_sec - start_sec <= 0:
            return
        self.timeline_view = (start_sec, end_sec)
        self.zoom_factor = self.video_duration / (end_sec - start_sec)
        self.zoom_label.setText(f"ZOOM x{self.zoom_factor:.0f}")
        self.multi_range_bar.set_view(start_sec, end_sec)
        self.multi_range_bar.update()

    def zoom_timeline(self, zoom_in):
        if self.video_duration <= 0:
            return
        view_start, view_end = self.timeline_view
        if view_end <= view_start:
            view_start = 0.0
            view_end = self.video_duration
        view_duration = view_end - view_start

        min_span = max(0.08, 2.0 / max(1.0, self.video_fps))
        if zoom_in:
            new_span = max(min_span, view_duration / 2.0)
        else:
            new_span = min(self.video_duration, view_duration * 2.0)

        position_sec = self._vlc_position_ms() / 1000.0
        center = max(view_start, min(view_end, position_sec))
        left = center - new_span / 2.0
        right = center + new_span / 2.0
        if left < 0:
            left = 0.0
            right = min(self.video_duration, new_span)
        if right > self.video_duration:
            right = self.video_duration
            left = max(0.0, self.video_duration - new_span)
        if right - left < min_span:
            left = max(0.0, center - min_span / 2.0)
            right = min(self.video_duration, left + min_span)
            left = max(0.0, right - min_span)

        self.timeline_view = (left, right)
        self._refresh_timeline_view()

    def _refresh_timeline_view(self):
        if self.video_duration <= 0:
            return
        view_start, view_end = self.timeline_view
        span = max(0.000001, view_end - view_start)
        self.zoom_factor = self.video_duration / span
        self.zoom_label.setText(f"ZOOM x{self.zoom_factor:.0f}")
        self.update_range_bar()

    def seek_to_timeline_position(self, position_sec):
        if self.video_duration <= 0:
            return
        position_ms = max(
            0.0, min(self.video_duration, position_sec)
        ) * 1000
        state = self.vlc_player.get_state()
        if state == vlc.State.Ended:
            self._vlc_end_notified = False
            self.vlc_player.stop()
        if state in (
            vlc.State.Stopped,
            vlc.State.Ended,
            vlc.State.NothingSpecial,
        ):
            self.vlc_player.play()
            self.vlc_player.set_time(int(position_ms))
            self.vlc_player.set_pause(1)
        else:
            self.vlc_player.set_time(int(position_ms))
        self.position_slider.setValue(
            int(position_ms / 1000.0 / self.video_duration * 1000)
        )
        self.update_time_label(
            int(position_ms), int(self.video_duration * 1000)
        )
        self.multi_range_bar.set_position(position_sec)

    # ---------- 预览模式 ----------
    def on_preview_mode_toggled(self, checked):
        self.preview_mode = checked
        if checked:
            self.status_bar.showMessage(
                tr("预览模式：仅播放选中的区间")
            )
        else:
            self.status_bar.showMessage(
                tr("预览模式：正常播放全部视频")
            )

    def is_position_in_segments(self, pos_sec):
        for start, end in self.segments:
            if start <= pos_sec <= end:
                return True
        return False

    def get_next_segment_start(self, pos_sec):
        for start, end in self.segments:
            if start >= pos_sec:
                return start
        return None

    # ---------- 文件相关 ----------
    def _reset_source_state(self):
        self.input_path = ""
        self.segments = []
        self.refresh_segment_list()
        self.marker_start_sec = None
        self.marker_end_sec = None
        self.multi_range_bar.set_segments([], 0)
        self.multi_range_bar.clear_markers()
        self.btn_clear_markers.setEnabled(False)
        self.timeline_view = (0.0, 0.0)
        self.zoom_factor = 1.0
        self.zoom_label.setText("ZOOM x1")
        self.video_duration = 0.0
        self.video_resolution = (0, 0)
        self.video_fps = 25.0
        self.has_audio = False
        self.start_spin.setValue(0.0)
        self.end_spin.setValue(10.0)
        self.position_slider.setValue(0)
        self.time_label.setText("00:00 / 00:00")
        self.info_label.setText(tr("未加载视频"))

    def _clip_list_text(self, index, clip):
        segment_text = (
            tr("{count} 个片段").format(count=len(clip["segments"]))
            if clip["segments"]
            else tr("完整视频")
        )
        return tr(
            "{index}. {name} | {duration} | {segments}"
        ).format(
            index=index + 1,
            name=clip["name"],
            duration=self._format_time(clip["duration"] * 1000),
            segments=segment_text,
        )

    def _current_clip_id(self):
        if 0 <= self.current_clip_index < len(self.clips):
            return self.clips[self.current_clip_index]["id"]
        return None

    def refresh_clip_list(self, select_id=None):
        self.clip_list.blockSignals(True)
        self.clip_list.clear()
        selected_row = -1
        for index, clip in enumerate(self.clips):
            item = QListWidgetItem(self._clip_list_text(index, clip))
            item.setData(Qt.ItemDataRole.UserRole, clip["id"])
            self.clip_list.addItem(item)
            if clip["id"] == select_id:
                selected_row = index
        self.clip_list.blockSignals(False)
        if selected_row >= 0:
            self.clip_list.setCurrentRow(selected_row)
        elif self.clips:
            self.clip_list.setCurrentRow(0)

    def _activate_clip(self, index):
        if index < 0 or index >= len(self.clips):
            self.current_clip_index = -1
            self._clear_preview_media()
            self._reset_source_state()
            return

        clip = self.clips[index]
        if (
            self.current_clip_index == index
            and self.input_path == clip["path"]
            and self.video_duration > 0
        ):
            return

        self.stop_play()
        self._clear_preview_media()
        self._reset_source_state()
        self.current_clip_index = index
        self._apply_clip_to_editor(clip)
        self.refresh_clip_list(select_id=clip["id"])
        self.load_video_for_preview(clip["path"])
        if not self._output_path_manual:
            self.auto_set_output_path()

    def on_clip_selected(self, item):
        row = self.clip_list.row(item)
        self._activate_clip(row)

    def on_clip_rows_moved(
        self, _parent, _start, _end, _destination, _row
    ):
        current_id = self._current_clip_id()
        ordered_ids = [
            self.clip_list.item(index).data(Qt.ItemDataRole.UserRole)
            for index in range(self.clip_list.count())
        ]
        clips_by_id = {clip["id"]: clip for clip in self.clips}
        self.clips = [
            clips_by_id[clip_id]
            for clip_id in ordered_ids
            if clip_id in clips_by_id
        ]
        self.refresh_clip_list(select_id=current_id)
        if current_id is not None:
            self.current_clip_index = next(
                (
                    index
                    for index, clip in enumerate(self.clips)
                    if clip["id"] == current_id
                ),
                -1,
            )
        if not self._output_path_manual:
            self.auto_set_output_path()

    def remove_selected_clip(self):
        row = self.clip_list.currentRow()
        if row < 0 or row >= len(self.clips):
            return
        active_id = self._current_clip_id()
        removed_id = self.clips[row]["id"]
        was_current = active_id == removed_id
        del self.clips[row]
        if not self.clips:
            self.current_clip_index = -1
            self._clear_preview_media()
            self._reset_source_state()
            self.input_label.clear()
            self.refresh_clip_list()
            self.output_path = ""
            self._output_path_manual = False
            self.output_path_label.setText(tr("输出路径：未设置"))
            return

        next_index = min(row, len(self.clips) - 1)
        if was_current:
            self.current_clip_index = -1
            self.refresh_clip_list(select_id=self.clips[next_index]["id"])
            self._activate_clip(next_index)
        else:
            active_index = next(
                (
                    index
                    for index, clip in enumerate(self.clips)
                    if clip["id"] == active_id
                ),
                -1,
            )
            self.current_clip_index = active_index
            self.refresh_clip_list(select_id=active_id)
        if not self._output_path_manual:
            self.auto_set_output_path()

    def move_selected_clip(self, delta):
        row = self.clip_list.currentRow()
        target = row + delta
        if row < 0 or target < 0 or target >= len(self.clips):
            return
        current_id = None
        if 0 <= self.current_clip_index < len(self.clips):
            current_id = self.clips[self.current_clip_index]["id"]
        self.clips[row], self.clips[target] = (
            self.clips[target],
            self.clips[row],
        )
        self.refresh_clip_list(select_id=current_id)
        if current_id is not None:
            self.current_clip_index = next(
                (
                    index
                    for index, clip in enumerate(self.clips)
                    if clip["id"] == current_id
                ),
                -1,
            )
        else:
            self.current_clip_index = target
        if not self._output_path_manual:
            self.auto_set_output_path()

    def clear_clips(self):
        self.clips.clear()
        self.current_clip_index = -1
        self.stop_play()
        self._clear_preview_media()
        self._reset_source_state()
        self.input_label.clear()
        self.output_path = ""
        self._output_path_manual = False
        self.refresh_clip_list()
        self.output_path_label.setText(tr("输出路径：未设置"))

    def browse_input(self):
        was_playing = (
            hasattr(self, "vlc_player") and self.vlc_player.is_playing()
        )
        if was_playing:
            self.vlc_player.set_pause(1)

        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            tr("选择视频文件"),
            "",
            tr(
                "视频文件 (*.mp4 *.avi *.mkv *.mov *.flv *.wmv);;"
                "所有文件 (*.*)"
            ),
        )
        if not file_paths:
            if was_playing and self.vlc_player.get_state() != vlc.State.Ended:
                self.vlc_player.set_pause(0)
            return

        first_new_index = len(self.clips)
        errors = []
        for file_path in file_paths:
            try:
                info = self._probe_video_info(file_path)
            except Exception as exc:
                errors.append(f"{os.path.basename(file_path)}: {exc}")
                continue
            self._clip_sequence += 1
            self.clips.append({
                "id": self._clip_sequence,
                "path": file_path,
                "name": os.path.basename(file_path),
                "duration": info["duration"],
                "resolution": info["resolution"],
                "fps": info["fps"],
                "has_audio": info["has_audio"],
                "segments": [],
            })

        if errors:
            QMessageBox.warning(
                self,
                tr("读取失败"),
                tr("以下视频无法读取：\n{errors}").format(
                    errors="\n".join(errors)
                ),
            )
        if first_new_index < len(self.clips):
            selected_clip = self.clips[first_new_index]
            self.refresh_clip_list(select_id=selected_clip["id"])
            self._activate_clip(first_new_index)
        elif was_playing:
            if self.vlc_player.get_state() != vlc.State.Ended:
                self.vlc_player.set_pause(0)

    def browse_output(self):
        if self.output_path:
            default_path = self.output_path
        elif self.clips:
            source_path = self.clips[0]["path"]
            default_name = (
                os.path.splitext(os.path.basename(source_path))[0]
                + f"-{self._output_suffix()}.mp4"
            )
            default_path = os.path.join(
                os.path.dirname(source_path), default_name
            )
        else:
            default_path = "output_merged.mp4"
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            tr("保存拼接视频"),
            default_path,
            tr("MP4 文件 (*.mp4);;所有文件 (*.*)"),
        )
        if file_path:
            self.output_path = file_path
            self._output_path_manual = True
            self.output_path_label.setText(
                tr("输出路径：{path}").format(path=file_path)
            )

    def _output_suffix(self):
        encoder_index = self.encoder_combo.currentIndex()
        if encoder_index == 1:
            short_name = "h265"
        elif encoder_index == 0:
            short_name = "h264"
        else:
            return "h264-cpu"
        cq_values = (23, 28, 32)
        cq = cq_values[self.quality_combo.currentIndex()]
        return f"{short_name}-cq{cq}"

    @staticmethod
    def _unique_output_path(candidate_path):
        if not os.path.exists(candidate_path):
            return candidate_path
        root, extension = os.path.splitext(candidate_path)
        index = 1
        while os.path.exists(f"{root}-{index}{extension}"):
            index += 1
        return f"{root}-{index}{extension}"

    def auto_set_output_path(self):
        source_path = self.clips[0]["path"] if self.clips else self.input_path
        if source_path and not self._output_path_manual:
            directory = os.path.dirname(source_path)
            base_name = os.path.splitext(os.path.basename(source_path))[0]
            candidate = os.path.join(
                directory,
                f"{base_name}-{self._output_suffix()}.mp4",
            )
            self.output_path = self._unique_output_path(candidate)
            self.output_path_label.setText(
                tr("输出路径：{path}").format(path=self.output_path)
            )

    def _probe_video_info(self, file_path):
        flags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
        result = subprocess.run(
            [
                _FFPROBE_PATH,
                "-v", "error",
                "-print_format", "json",
                "-show_format",
                "-show_streams",
                file_path,
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=15,
            creationflags=flags,
        )
        if result.returncode != 0:
            raise RuntimeError(
                result.stderr.strip() or tr("FFprobe 读取失败")
            )

        data = json.loads(result.stdout or "{}")
        duration = 0.0
        width = 0
        height = 0
        fps = 25.0
        has_audio = False
        for stream in data.get("streams", []):
            codec_type = stream.get("codec_type")
            if codec_type == "video":
                width = int(stream.get("width") or 0)
                height = int(stream.get("height") or 0)
                try:
                    duration = float(stream.get("duration") or 0)
                except (TypeError, ValueError):
                    duration = 0.0
                parsed_fps = ProcessThread._parse_fraction_rate(
                    stream.get("avg_frame_rate")
                )
                if not parsed_fps:
                    parsed_fps = ProcessThread._parse_fraction_rate(
                        stream.get("r_frame_rate")
                    )
                if parsed_fps:
                    fps = parsed_fps
            elif codec_type == "audio":
                has_audio = True

        format_duration = data.get("format", {}).get("duration")
        if not duration:
            try:
                duration = float(format_duration or 0)
            except (TypeError, ValueError):
                duration = 0.0
        if duration <= 0:
            raise RuntimeError(tr("无法从文件中读取视频时长"))
        if width <= 0 or height <= 0:
            raise RuntimeError(tr("无法从文件中读取视频分辨率"))
        return {
            "duration": duration,
            "resolution": (width, height),
            "fps": fps,
            "has_audio": has_audio,
        }

    def _apply_clip_to_editor(self, clip):
        self.input_path = clip["path"]
        self.video_duration = clip["duration"]
        self.video_resolution = clip["resolution"]
        self.video_fps = clip["fps"]
        self.has_audio = clip["has_audio"]
        self.segments = clip["segments"]
        self.original_ratio = (
            self.video_resolution[0] / self.video_resolution[1]
            if self.video_resolution[1]
            else 1.0
        )
        self.input_label.setText(self.input_path)
        self.start_spin.setMaximum(self.video_duration - 0.1)
        self.end_spin.setMaximum(self.video_duration)
        self.end_spin.setValue(min(10.0, self.video_duration))
        self.start_spin.setValue(0.0)
        self.width_spin.setValue(self.video_resolution[0])
        self.height_spin.setValue(self.video_resolution[1])
        self.refresh_segment_list()
        self.update_info_label()
        self.reset_timeline_zoom()
        self.update_range_bar()

    def load_video_info(self, file_path):
        try:
            info = self._probe_video_info(file_path)
            clip = {
                "id": -1,
                "path": file_path,
                "name": os.path.basename(file_path),
                "duration": info["duration"],
                "resolution": info["resolution"],
                "fps": info["fps"],
                "has_audio": info["has_audio"],
                "segments": [],
            }
            self._apply_clip_to_editor(clip)
        except Exception as e:
            QMessageBox.warning(
                self,
                tr("读取失败"),
                tr("无法加载视频信息：{error}").format(error=e),
            )

    def load_video_for_preview(self, file_path):
        self._clear_preview_media()

        media = self.vlc_instance.media_new(file_path)
        self.vlc_player.set_media(media)
        self.current_vlc_media = media

        self.position_slider.setValue(0)
        self.time_label.setText("00:00 / 00:00")
        self.btn_play.setText(tr("▶ 播放"))
        self.btn_mark_start.setEnabled(True)
        self.btn_mark_end.setEnabled(True)
        self.btn_play.setEnabled(True)
        self.btn_stop.setEnabled(True)
        self.vlc_refresh_timer.start()
        self.status_bar.showMessage(
            tr("视频已加载（VLC 内核）。点击播放开始预览。")
        )

    def toggle_play(self):
        state = self.vlc_player.get_state()
        if state == vlc.State.Playing:
            self.vlc_player.set_pause(1)
            return

        if state == vlc.State.Paused:
            self.vlc_player.set_pause(0)
            return

        target_ms = None
        if (
            state == vlc.State.Stopped
            and self.position_slider.value() > 0
            and self.video_duration > 0
        ):
            target_ms = int(
                self.position_slider.value()
                / 1000.0
                * self.video_duration
                * 1000
            )

        if state == vlc.State.Ended:
            self._vlc_end_notified = False
            self.vlc_player.stop()
            self.vlc_player.set_time(0)

        if self.preview_mode and self.segments:
            pos_sec = self._vlc_position_ms() / 1000.0
            if not self.is_position_in_segments(pos_sec):
                target_ms = int(self.segments[0][0] * 1000)

        if target_ms is not None:
            self.vlc_player.play()
            self.vlc_player.set_time(target_ms)
        else:
            self.vlc_player.play()

    def frame_step(self, direction):
        if (
            not self.input_path
            or self.video_duration <= 0
            or self.video_fps <= 0
        ):
            return

        state = self.vlc_player.get_state()
        frame_ms = 1000.0 / self.video_fps
        duration_ms = int(self.video_duration * 1000)
        position_ms = self._vlc_position_ms()
        if self._pending_frame_position_ms is not None:
            position_ms = self._pending_frame_position_ms

        if state == vlc.State.Playing:
            self.vlc_player.set_pause(1)

        if state == vlc.State.Ended:
            self._vlc_end_notified = False
            position_ms = duration_ms
            self.vlc_player.stop()

        total_frames = max(1, int(round(duration_ms / frame_ms)))
        current_frame = int(round(position_ms / frame_ms))
        step_frames = max(1, self.frame_step_spin.value())
        if direction > 0:
            target_frame = min(
                total_frames - 1, current_frame + step_frames
            )
        else:
            target_frame = max(0, current_frame - step_frames)
        target_ms = int(round(target_frame * frame_ms))

        cold_start = state in (
            vlc.State.Stopped,
            vlc.State.Ended,
            vlc.State.NothingSpecial,
            vlc.State.Opening,
            vlc.State.Buffering,
        )
        if cold_start:
            self._pending_frame_position_ms = target_ms
            self._frame_step_generation += 1
            generation = self._frame_step_generation
            if state in (
                vlc.State.Stopped,
                vlc.State.Ended,
                vlc.State.NothingSpecial,
            ):
                self.vlc_player.play()
            QTimer.singleShot(
                40,
                lambda: self._apply_pending_frame_target(
                    generation, 0
                ),
            )
        else:
            self.vlc_player.set_time(target_ms)

        self._show_frame_step_position(
            target_ms, step_frames, direction
        )

    def _apply_pending_frame_target(self, generation, attempt):
        if generation != self._frame_step_generation:
            return
        target_ms = self._pending_frame_position_ms
        if target_ms is None:
            return
        state = self.vlc_player.get_state()
        if state in (vlc.State.Opening, vlc.State.Buffering) and attempt < 12:
            QTimer.singleShot(
                50,
                lambda: self._apply_pending_frame_target(
                    generation, attempt + 1
                ),
            )
            return
        self._pending_frame_position_ms = None
        self.vlc_player.set_time(target_ms)
        if self.vlc_player.get_state() != vlc.State.Paused:
            self.vlc_player.set_pause(1)

    def _show_frame_step_position(self, target_ms, step_frames, direction):
        duration_ms = int(self.video_duration * 1000)
        frame_ms = 1000.0 / self.video_fps
        self.position_slider.setValue(
            int(target_ms / duration_ms * 1000)
        )
        self.update_time_label(target_ms, duration_ms)
        self.multi_range_bar.set_position(target_ms / 1000.0)
        frame_number = int(round(target_ms / frame_ms))
        self.status_bar.showMessage(
            tr(
                "步进 {steps} 帧 {sign} | "
                "第 {frame} 帧 @ {ms}ms"
            ).format(
                steps=step_frames,
                sign="+" if direction > 0 else "-",
                frame=frame_number + 1,
                ms=target_ms,
            )
        )

    def stop_play(self):
        self._safe_stop_vlc()
        self._vlc_end_notified = False
        self.position_slider.setValue(0)
        self.time_label.setText("00:00 / 00:00")
        self.btn_play.setText(tr("▶ 播放"))
        self.multi_range_bar.set_position(0)
        self.status_bar.showMessage(tr("已停止"))

    def set_position(self, value):
        if self.video_duration <= 0:
            return
        position_ms = int(value / 1000.0 * self.video_duration * 1000)
        state = self.vlc_player.get_state()
        if state == vlc.State.Ended:
            self._vlc_end_notified = False
            self.vlc_player.stop()
            self.vlc_player.set_time(0)
        if state in (
            vlc.State.Stopped,
            vlc.State.Ended,
            vlc.State.NothingSpecial,
        ):
            self.vlc_player.play()
            self.vlc_player.set_time(position_ms)
            self.vlc_player.set_pause(1)
        else:
            self.vlc_player.set_time(position_ms)
        self.update_time_label(
            position_ms, int(self.video_duration * 1000)
        )

    def update_time_label(self, pos_ms, duration_ms):
        if duration_ms > 0:
            pos_str = self._format_time(pos_ms)
            dur_str = self._format_time(duration_ms)
            self.time_label.setText(f"{pos_str} / {dur_str}")
        else:
            self.time_label.setText("00:00 / 00:00")

    def _format_time(self, ms):
        seconds = int(ms / 1000)
        minutes = seconds // 60
        seconds %= 60
        return f"{minutes:02d}:{seconds:02d}"

    def mark_start(self):
        pos_ms = self._vlc_position_ms()
        pos_sec = pos_ms / 1000.0
        if pos_sec < self.video_duration:
            self.marker_start_sec = pos_sec
            self.start_spin.setValue(pos_sec)
            self._sync_marker_display()
            self.status_bar.showMessage(
                tr("已标记起点：{time}").format(
                    time=self._format_time(pos_ms)
                )
            )

    def mark_end(self):
        pos_ms = self._vlc_position_ms()
        pos_sec = pos_ms / 1000.0
        if pos_sec <= self.video_duration:
            self.marker_end_sec = pos_sec
            self.end_spin.setValue(pos_sec)
            self._sync_marker_display()
            self.status_bar.showMessage(
                tr("已标记终点：{time}").format(
                    time=self._format_time(pos_ms)
                )
            )

    def clear_markers(self):
        self.marker_start_sec = None
        self.marker_end_sec = None
        self.multi_range_bar.clear_markers()
        self.btn_clear_markers.setEnabled(False)
        if self.video_duration > 0:
            self.start_spin.setValue(0.0)
            self.end_spin.setValue(min(10.0, self.video_duration))
        self.status_bar.showMessage(
            tr("已清除起点/终点标记")
        )

    def _sync_marker_display(self):
        self.multi_range_bar.set_markers(
            self.marker_start_sec, self.marker_end_sec
        )
        self.btn_clear_markers.setEnabled(
            self.marker_start_sec is not None
            or self.marker_end_sec is not None
        )

    # ---------- 分辨率预设 ----------
    def on_resize_toggled(self, checked):
        self.preset_combo.setEnabled(checked)
        self.width_spin.setEnabled(checked)
        self.height_spin.setEnabled(checked)
        self.cb_keep_ratio.setEnabled(checked)
        if not checked:
            self.width_spin.setValue(self.video_resolution[0] or 640)
            self.height_spin.setValue(self.video_resolution[1] or 480)

    def on_preset_changed(self, preset_index):
        if not self.cb_resize.isChecked() or self.video_resolution == (0, 0):
            return
        w, h = self.video_resolution
        ratio = w / h if h != 0 else 1.0
        if preset_index == 0:
            target_w, target_h = w, h
        elif preset_index == 1:
            target_w = 1280
            target_h = int(target_w / ratio)
            if target_h % 2 == 1: target_h += 1
        elif preset_index == 2:
            target_w = 854 if ratio >= 1.5 else 640
            target_h = int(target_w / ratio)
            if target_h % 2 == 1: target_h += 1
        else:
            return
        self._updating_spins = True
        self.width_spin.setValue(target_w)
        self.height_spin.setValue(target_h)
        self._updating_spins = False

    def on_keep_ratio_toggled(self, checked):
        pass

    def on_width_changed(self, value):
        if self._updating_spins:
            return
        if self.cb_keep_ratio.isChecked() and self.video_resolution[0] > 0:
            ratio = self.video_resolution[0] / self.video_resolution[1]
            new_h = int(value / ratio)
            if new_h % 2 == 1: new_h += 1
            self._updating_spins = True
            self.height_spin.setValue(new_h)
            self._updating_spins = False

    def on_height_changed(self, value):
        if self._updating_spins:
            return
        if self.cb_keep_ratio.isChecked() and self.video_resolution[1] > 0:
            ratio = self.video_resolution[0] / self.video_resolution[1]
            new_w = int(value * ratio)
            if new_w % 2 == 1: new_w += 1
            self._updating_spins = True
            self.width_spin.setValue(new_w)
            self._updating_spins = False

    def update_info_label(self):
        if self.video_duration > 0:
            dur_str = str(timedelta(seconds=int(self.video_duration)))
            res_str = f"{self.video_resolution[0]}x{self.video_resolution[1]}"
            start = self.start_spin.value()
            end = self.end_spin.value()
            self.info_label.setText(
                tr(
                    "时长 {duration} | 原始分辨率 {resolution} | "
                    "当前区间 {start:.1f}s ~ {end:.1f}s "
                    "(时长 {range:.1f}s)"
                ).format(
                    duration=dur_str,
                    resolution=res_str,
                    start=start,
                    end=end,
                    range=end - start,
                )
            )
        else:
            self.info_label.setText(tr("未加载视频"))

    # ---------- 处理 ----------
    def on_encoder_changed(self):
        self._update_quality_enabled()
        self.update_auto_output_path()

    def _update_quality_enabled(self):
        self.quality_combo.setEnabled(
            self.encoder_combo.currentIndex() in (0, 1)
        )

    def update_auto_output_path(self):
        self.auto_set_output_path()

    def start_processing(self):
        if not self.clips:
            QMessageBox.warning(
                self,
                tr("错误"),
                tr("请先添加至少一个视频。"),
            )
            return
        if not self.output_path:
            QMessageBox.warning(
                self, tr("错误"), tr("请设置输出路径。")
            )
            return

        target_size = None
        if self.cb_resize.isChecked():
            target_size = (self.width_spin.value(), self.height_spin.value())

        items = []
        for clip in self.clips:
            if clip["duration"] <= 0:
                continue
            segments = (
                list(clip["segments"])
                if clip["segments"]
                else [(0.0, clip["duration"])]
            )
            items.append({
                "path": clip["path"],
                "duration": clip["duration"],
                "resolution": clip["resolution"],
                "fps": clip["fps"],
                "has_audio": clip["has_audio"],
                "segments": segments,
            })

        if not items:
            QMessageBox.warning(
                self,
                tr("错误"),
                tr("没有可输出的视频。"),
            )
            return

        encoder_index = self.encoder_combo.currentIndex()
        encoder_text = self.encoder_combo.currentText()
        nvenc_cq_values = (23, 28, 32)
        if encoder_index == 0:
            codec = "h264_nvenc"
            preset = "p5"
        elif encoder_index == 1:
            codec = "hevc_nvenc"
            preset = "p5"
        else:
            codec = "libx264"
            preset = "medium"
            ffmpeg_params = None
            self.status_bar.showMessage(
                tr("正在使用 CPU 软件编码（libx264）...")
            )

        if encoder_index in (0, 1):
            # 高/中/低对应 cq 23 / 28 / 32
            nvenc_cq = nvenc_cq_values[self.quality_combo.currentIndex()]
            ffmpeg_params = ["-rc", "vbr", "-cq", str(nvenc_cq)]
            self.status_bar.showMessage(
                tr("正在使用 {encoder} · 画质 {quality} ...").format(
                    encoder=encoder_text,
                    quality=self.quality_combo.currentText(),
                )
            )

        self.output_path = self._unique_output_path(self.output_path)
        self.output_path_label.setText(
            tr("输出路径：{path}").format(path=self.output_path)
        )
        self.btn_start.setEnabled(False)
        self.btn_browse_input.setEnabled(False)
        self.btn_browse_output.setEnabled(False)
        self.btn_remove_clip.setEnabled(False)
        self.btn_move_clip_up.setEnabled(False)
        self.btn_move_clip_down.setEnabled(False)
        self.btn_clear_clips.setEnabled(False)
        self.clip_list.setEnabled(False)
        self.encoder_combo.setEnabled(False)
        self.quality_combo.setEnabled(False)
        self.cb_mute_export.setEnabled(False)
        self.progress_bar.setValue(0)
        self._process_started_at = time.perf_counter()

        self.thread = ProcessThread(
            items,
            self.output_path,
            target_size,
            codec=codec,
            preset=preset,
            ffmpeg_params=ffmpeg_params,
            mute_audio=self.cb_mute_export.isChecked(),
            keep_ratio=self.cb_keep_ratio.isChecked(),
        )
        self.thread.progress_updated.connect(self.update_progress)
        self.thread.status_updated.connect(self.update_status)
        self.thread.finished.connect(self.on_processing_finished)
        self.thread.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        self.status_bar.showMessage(
            tr("正在输出视频... {percent}%").format(percent=value)
        )

    def update_status(self, text):
        self.status_bar.showMessage(text)

    def on_processing_finished(self, success, message):
        self.btn_start.setEnabled(True)
        self.btn_browse_input.setEnabled(True)
        self.btn_browse_output.setEnabled(True)
        self.btn_remove_clip.setEnabled(True)
        self.btn_move_clip_up.setEnabled(True)
        self.btn_move_clip_down.setEnabled(True)
        self.btn_clear_clips.setEnabled(True)
        self.clip_list.setEnabled(True)
        self.encoder_combo.setEnabled(True)
        self.cb_mute_export.setEnabled(True)
        self._update_quality_enabled()
        elapsed = time.perf_counter() - getattr(
            self, "_process_started_at", time.perf_counter()
        )
        encoder_name = self.encoder_combo.currentText()
        if self.encoder_combo.currentIndex() in (0, 1):
            encoder_name += f" · {self.quality_combo.currentText()}"
        time_text = tr(
            "编码器：{encoder}\n用时：{elapsed:.2f} 秒"
        ).format(encoder=encoder_name, elapsed=elapsed)

        if success:
            self.progress_bar.setValue(100)
            self.status_bar.showMessage(
                tr("处理完成，用时 {elapsed:.2f} 秒 ({encoder})").format(
                    elapsed=elapsed,
                    encoder=encoder_name,
                )
            )
            self.btn_open_folder.setEnabled(True)
            QMessageBox.information(
                self, tr("完成"), f"{message}\n\n{time_text}"
            )
        else:
            self.progress_bar.setValue(0)
            self.status_bar.showMessage(tr("处理失败"))
            QMessageBox.critical(
                self, tr("错误"), f"{message}\n\n{time_text}"
            )
        self.thread = None

    def open_output_folder(self):
        if self.output_path:
            folder = os.path.dirname(self.output_path)
            if os.path.exists(folder):
                QDesktopServices.openUrl(QUrl.fromLocalFile(folder))

    def open_github(self):
        QDesktopServices.openUrl(QUrl(GITHUB_URL))
        self.status_bar.showMessage(
            tr("正在打开 GitHub：{url}").format(url=GITHUB_URL)
        )

    def eventFilter(self, watched, event):
        if event.type() == QEvent.Type.KeyPress:
            key = event.key()
            if key in (Qt.Key.Key_Left, Qt.Key.Key_Right):
                if QApplication.activeModalWidget() is not None:
                    return False
                active_window = QApplication.activeWindow()
                if active_window is not None and active_window is not self:
                    return False
                self.frame_step(-1 if key == Qt.Key.Key_Left else 1)
                return True
        return super().eventFilter(watched, event)

    def closeEvent(self, event):
        try:
            left, right = self.main_splitter.sizes()[:2]
            QSettings(GITHUB_USER, APP_NAME).setValue(
                "layout/splitter_sizes", f"{left},{right}"
            )
        except Exception:
            pass
        if getattr(self, "_application", None) is not None:
            self._application.removeEventFilter(self)
        if hasattr(self, "vlc_player"):
            try:
                self._clear_preview_media()
            except Exception:
                pass
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setApplicationName("VideoTrimmerTool")
    app.setOrganizationName(GITHUB_USER)
    settings = QSettings(GITHUB_USER, APP_NAME)
    set_language(settings.value("language", "zh"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
