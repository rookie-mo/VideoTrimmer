# VideoTrimmer v1.0.0

首个公开版本。

## 功能

- VLC 视频预览，支持 FLV、MP4、MKV、MOV、AVI、WMV 等格式
- 多区段视频截取与自动拼接
- 可缩放、可平移的时间线
- 起点/终点标记和选区颜色显示
- 左右方向键逐帧定位，帧步长可配置
- CPU H.264 编码
- NVIDIA NVENC H.264 / H.265 硬件编码
- NVENC 高 / 中 / 低三档画质
- 输出进度、编码方式和耗时统计
- 中文、English、日本語界面
- 深色 / 浅色主题

## 系统要求

- Windows 10 / 11 64-bit
- NVENC 编码需要 NVIDIA 显卡和较新的驱动

## 下载说明

发布包是目录版，解压后请保留整个 `VideoTrimmerTool` 文件夹，
不要只移动其中的 exe。

## 校验值

```text
VideoTrimmer-v1.0.0-win64.zip
SHA256: 9CEF361733E6FF0FC4937D48ABCC127903698892D7BBEBF8A68D64C0A146C93B
```

## 许可证

本项目使用 GPL-3.0 发布。发布包包含 PyQt6、Qt、VLC、FFmpeg、
Python 和 PyInstaller 等第三方组件，许可证及源码信息见
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

本版本对应的完整源码：
https://github.com/rookie-mo/VideoTrimmer/tree/v1.0.0
