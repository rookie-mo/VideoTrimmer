# VideoTrimmer

Windows 视频截取、拼接与转码工具，支持 VLC 预览、多区段裁剪、
时间线缩放、逐帧定位，以及 NVIDIA NVENC H.264 / H.265 硬件编码。

GitHub: [rookie-mo/VideoTrimmer](https://github.com/rookie-mo/VideoTrimmer)

## 功能

- VLC 预览 FLV、MP4、MKV、MOV、AVI、WMV 等视频
- 添加多个截取区间并自动拼接
- 可点击、缩放和平移的裁剪时间线
- 起点/终点标记与选区配色显示
- 左右方向键逐帧前进或后退，可设置每次步进的帧数
- CPU H.264 编码
- NVIDIA NVENC H.264 / H.265 硬件编码
- 高 / 中 / 低三档 NVENC 画质
- 输出进度、编码器和耗时统计
- 中文、English、日本語界面
- 深色 / 浅色主题

## 下载

请在 [Releases](https://github.com/rookie-mo/VideoTrimmer/releases)
下载打包好的 Windows 版本。

发布包是目录版，需要保留整个目录，不能只复制其中的 exe。

## 系统要求

- Windows 10 / 11 64-bit
- 使用 GPU 编码时需要 NVIDIA 显卡和较新的驱动

## 从源码运行

1. 安装 Python 3.11。
2. 安装 VLC Desktop 3.x。
3. 将 `ffmpeg.exe` 和 `ffprobe.exe` 放入项目根目录。
4. 安装 Python 依赖：

```powershell
pip install -r requirements.txt
```

5. 启动程序：

```powershell
python video_trimmer_gui.py
```

## 打包

默认 VLC 安装目录为：

```text
C:\Program Files\VideoLAN\VLC
```

确认 `ffmpeg.exe`、`ffprobe.exe` 和 VLC 存在后执行：

```powershell
python -m PyInstaller --noconfirm --clean video_trimmer.spec
```

输出目录：

```text
dist\VideoTrimmerTool\
```

## 快捷键

| 按键 | 功能 |
|---|---|
| `←` | 按设定帧数后退 |
| `→` | 按设定帧数前进 |

## 许可证

本项目使用 [GPL-3.0](LICENSE) 发布。

由于当前版本使用 GPLv3 授权的 PyQt6 和 GPL 版 FFmpeg，
发布二进制版本时需要同时提供对应源码和第三方许可证说明。
详细信息见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

## 作者

[rookie-mo](https://github.com/rookie-mo)
