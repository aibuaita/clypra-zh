# -*- coding: utf-8 -*-
from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

import brotli
import struct


DEFAULT_EXE = Path(os.environ.get("LOCALAPPDATA", "")) / "Clypra" / "clypra.exe"
WEBVIEW_CODE_CACHE = (
    Path(os.environ.get("LOCALAPPDATA", ""))
    / "com.clypra.editor"
    / "EBWebView"
    / "Default"
    / "Code Cache"
)
ASSET_RE = re.compile(
    rb"/assets/[A-Za-z0-9._~!$&()+,;=@%\-]+\.(?:js|css|woff2|woff|webp|png|jpg|jpeg|svg|ico)"
)


INDEX_MAP = {
    "Dark": "深色",
    "Classic dark": "经典深色",
    "Midnight": "午夜",
    "Deep blue tones": "深蓝色调",
    "Ocean": "海洋",
    "Cool cyan accents": "青色冷调",
    "Forest": "森林",
    "Natural green hues": "自然绿色",
    "Custom": "自定义",
    "Your custom theme": "你的自定义主题",
    "System": "系统",
    "Mono": "等宽",
    "Clypra Logo": "Clypra 标志",
    "VIDEO EDITOR": "视频编辑器",
    "Settings": "设置",
    "Start a new project": "新建项目",
    "Begin with a 16:9 landscape canvas optimized for YouTube and widescreen content, or open a recent project below.": "使用适合 YouTube 和宽屏内容的 16:9 横向画布开始，或打开下方最近项目。",
    "Recent Projects": "最近项目",
    "No recent projects": "暂无最近项目",
    "Create a new project to get started": "创建新项目开始使用",
    "More options": "更多选项",
    "Rename Project": "重命名项目",
    "Project name": "项目名称",
    "Cancel": "取消",
    "Delete Project": "删除项目",
    "This action cannot be undone. All project data will be permanently deleted.": "此操作无法撤销。所有项目数据都将被永久删除。",
    "Back to Home": "返回首页",
    "Export Current Frame (PNG)": "导出当前帧 (PNG)",
    "Media": "媒体",
    "Success": "成功",
    "Error": "错误",
    "Warning": "警告",
    "Added": "已添加",
    "Add to Track": "添加到轨道",
    "No media imported": "未导入媒体",
    "Import videos, audio, or images to get started": "导入视频、音频或图片开始使用",
    "Remove from Timeline": "从时间线移除",
    "Delete": "删除",
    "Whoosh": "呼啸声",
    "Thunder Storm": "雷暴",
    "Cinematic Boom": "电影冲击",
    "Explosion": "爆炸",
    "Button Click": "按钮点击",
    "Swoosh": "嗖声",
    "Upbeat Corporate": "商务律动",
    "Cinematic Epic": "史诗配乐",
    "Lo-fi Chill": "Lo-fi 放松",
    "Sound Effects": "音效",
    "Music": "音乐",
    "Title": "标题",
    "Subtitle": "副标题",
    "Lower Third": "下三分之一字幕",
    "Caption": "字幕",
    "Headline": "主标题",
    "Quote": "引用",
    "Sample Text": "示例文本",
    "Thumbs Up": "点赞",
    "Fire": "火焰",
    "Heart": "爱心",
    "Star": "星星",
    "Lightning": "闪电",
    "Sparkles": "闪光",
    "Party": "派对",
    "Rocket": "火箭",
    "Trophy": "奖杯",
    "Crown": "皇冠",
    "Clap": "鼓掌",
    "Search stickers...": "搜索贴纸...",
    "Blur": "模糊",
    "Gaussian blur": "高斯模糊",
    "Black & White": "黑白",
    "Grayscale": "灰度",
    "Sepia": "棕褐色",
    "Vintage tone": "复古色调",
    "Vignette": "暗角",
    "Darken edges": "边缘变暗",
    "Sharpen": "锐化",
    "Enhance details": "增强细节",
    "Glow": "发光",
    "Soft glow": "柔光",
    "Chromatic": "色差",
    "RGB split": "RGB 分离",
    "Pixelate": "像素化",
    "Mosaic effect": "马赛克效果",
    "Brightness": "亮度",
    "Adjust light": "调整光线",
    "Contrast": "对比度",
    "Enhance depth": "增强层次",
    "Saturation": "饱和度",
    "Color intensity": "色彩强度",
    "Noise": "噪点",
    "Film grain": "胶片颗粒",
    "Fade": "淡化",
    "Smooth fade": "平滑淡化",
    "Dissolve": "溶解",
    "Cross dissolve": "交叉溶解",
    "Wipe": "擦除",
    "Directional wipe": "方向擦除",
    "Slide": "滑动",
    "Slide motion": "滑动运动",
    "Zoom": "缩放",
    "Spin": "旋转",
    "Rotate effect": "旋转效果",
    "Push": "推入",
    "Default": "默认",
    "Standard white text with black outline": "标准白字黑边",
    "Bold": "粗体",
    "Heavy weight with strong contrast": "粗字重对比",
    "Minimal": "极简",
    "Clean and simple appearance": "干净简洁",
    "Boxed": "背景框",
    "Text with background box": "带背景框文字",
    "Outlined": "描边",
    "Thick outline, no fill": "粗描边无填充",
    "Shadow": "阴影",
    "Drop shadow effect": "投影效果",
    "Caption Styles": "字幕样式",
    "Audio": "音频",
    "Text": "文字",
    "Stickers": "贴纸",
    "Effects": "效果",
    "Transitions": "转场",
    "Captions": "字幕",
    "GPU Preview Initializing...": "GPU 预览初始化中...",
    "Check console (F12) for details": "查看控制台 (F12) 了解详情",
    "Playing": "播放中",
    "Previewing": "预览中",
    "Close (Esc)": "关闭 (Esc)",
    "In:": "入点:",
    "Out:": "出点:",
    "Duration:": "时长:",
    "Clear marks": "清除标记",
    "Mark In (I)": "标记入点 (I)",
    "Mark Out (O)": "标记出点 (O)",
    "Play marked region": "播放标记区间",
    "Loading preview...": "正在加载预览...",
    "Program Preview": "节目预览",
    "— Timeline": "— 时间线",
    "Toggle render telemetry": "切换渲染遥测",
    "Stats": "统计",
    "No clips in sequence": "序列中没有片段",
    "Import media or drag clips to timeline": "导入媒体或将片段拖到时间线",
    "Render Telemetry": "渲染遥测",
    "Eval:": "计算:",
    "Raster:": "栅格:",
    "Total:": "总计:",
    "Cache:": "缓存:",
    "Active:": "活跃:",
    "Dropped:": "丢帧:",
    "Max Drift:": "最大漂移:",
    "Playback speed": "播放速度",
    "Preview aspect ratio": "预览宽高比",
    "Properties": "属性",
    "Select a clip to edit": "选择片段进行编辑",
    "Clip Properties": "片段属性",
    "Transform": "变换",
    "Fit Mode": "适配模式",
    "Contain": "包含",
    "Cover": "覆盖",
    "Fill": "填充",
    "Stretch": "拉伸",
    "Original": "原始",
    "Reset Transform": "重置变换",
    "Width": "宽度",
    "Height": "高度",
    "Rotation": "旋转",
    "Opacity": "不透明度",
    "Clip": "片段",
    "Some controls below are not fully functional yet.": "下方部分控件尚未完全可用。",
    "Speed": "速度",
    "Not fully functional": "尚未完全可用",
    "Trim In (s)": "裁剪入点 (秒)",
    "Basic mode": "基础模式",
    "Trim Out (s)": "裁剪出点 (秒)",
    "Undo (Cmd+Z)": "撤销 (Cmd+Z)",
    "Redo (Cmd+Shift+Z)": "重做 (Cmd+Shift+Z)",
    "Free move mode": "自由移动模式",
    "Insert mode": "插入模式",
    "Ripple move mode": "波纹移动模式",
    "Swap selected clips (Ctrl+Shift+S)": "交换选中片段 (Ctrl+Shift+S)",
    "Delete left at playhead (Q)": "删除播放头左侧 (Q)",
    "Delete right at playhead (W)": "删除播放头右侧 (W)",
    "Split all at playhead (S)": "在播放头处分割全部 (S)",
    "Snap": "吸附",
    "Ripple edit mode (R) - Hold Shift while trimming": "波纹编辑模式 (R) - 修剪时按住 Shift",
    "Delete selected clip(s)": "删除选中片段",
    "Duplicate selected clip(s) (Cmd/Ctrl+D)": "复制选中片段 (Cmd/Ctrl+D)",
    "Close gaps": "关闭间隙",
    "Zoom Out": "缩小",
    "Zoom In": "放大",
    "Track": "轨道",
    "No tracks": "无轨道",
    "Locked": "已锁定",
    "Drop media here • I to import": "将媒体拖到这里 • 按 I 导入",
    "Something went wrong": "出错了",
    "Try Again": "重试",
    "Desktop Video Editor": "桌面视频编辑器",
    "v1.0.1 Stable Release": "v1.0.1 稳定版",
    "Engineered for Performance.": "为性能而生。",
    "Download Desktop Builds": "下载桌面版安装包",
    "Clypra compiles to optimized native executables for hardware acceleration, native file explorer integration, and robust multithreading.": "Clypra 会编译为优化过的原生可执行文件，支持硬件加速、原生文件管理器集成和稳定的多线程处理。",
    "macOS Build": "macOS 版本",
    "Universal DMG (.dmg)": "通用 DMG (.dmg)",
    "Windows Build": "Windows 版本",
    "x64 MSI Installer (.msi)": "x64 MSI 安装包 (.msi)",
    "Linux Build": "Linux 版本",
    "x64 AppImage (.AppImage)": "x64 AppImage (.AppImage)",
    "Bypassing Smart-Screen & Gatekeeper Controls": "绕过 SmartScreen 与 Gatekeeper 限制",
    "01 / MACOS USER INSTALLATION": "01 / MACOS 用户安装",
    "Open with Control-Click": "按住 Control 点击打开",
    "02 / WINDOWS USER INSTALLATION": "02 / WINDOWS 用户安装",
    "Windows SmartScreen Bypass": "绕过 Windows SmartScreen",
    "03 / LINUX USER INSTALLATION": "03 / LINUX 用户安装",
    "Make File Executable": "赋予文件可执行权限",
    "Core NLE Platform Architecture": "核心非线性编辑平台架构",
    "Clypra features premium architectural layers that rival industry-standard desktop non-linear editors.": "Clypra 采用高级架构层，体验可媲美行业标准桌面非线性编辑器。",
    "Infinite Multi-Track Sequencing": "无限多轨序列",
    "Arrange and sequence video, audio, text, and visual overlays on layers with clean, responsive drag-and-drop clips and snap-to-edge alignment precision.": "在图层上编排视频、音频、文字和视觉叠加，支持顺滑响应的拖放片段与精准边缘吸附对齐。",
    "A canvas-based, real-time render surface that accurately updates, scales, and scales visual clip layers using custom DPR scaling configurations.": "基于画布的实时渲染表面，可通过自定义 DPR 缩放配置准确更新和缩放视觉片段图层。",
    "Preset-Driven FFmpeg Exporters": "预设驱动的 FFmpeg 导出器",
    "Built with Tauri, React & Rust": "使用 Tauri、React 和 Rust 构建",
    "Appearance": "外观",
    "Editor": "编辑器",
    "About": "关于",
    "Custom Theme": "自定义主题",
    "Custom Theme Editor": "自定义主题编辑器",
    "Import theme from JSON file": "从 JSON 文件导入主题",
    "Export theme to JSON file": "导出主题为 JSON 文件",
    "Base:": "基础:",
    "Copy all colors from selected base theme": "复制所选基础主题的全部颜色",
    "Reset to default dark theme": "重置为默认深色主题",
    "Search colors...": "搜索颜色...",
    "Apply Custom Theme": "应用自定义主题",
    "Theme": "主题",
    "Font": "字体",
    "Timeline": "时间线",
    "Snap to grid": "吸附到网格",
    "Clips snap to ruler ticks when dragging": "拖动时片段吸附到标尺刻度",
    "Auto-ripple": "自动波纹",
    "Automatically close gaps when deleting clips": "删除片段时自动关闭间隙",
    "Sequence Settings": "序列设置",
    "Aspect ratio": "宽高比",
    "Canvas dimensions for export": "导出画布尺寸",
    "Frame rate": "帧率",
    "Frames per second for this project": "此项目每秒帧数",
    "Defaults": "默认值",
    "Auto-save": "自动保存",
    "Periodically save project state": "定期保存项目状态",
    "Default frame rate": "默认帧率",
    "Frame rate for new projects": "新项目帧率",
    "Version 1.0.1": "版本 1.0.1",
    "A modern, native video editor built with Tauri, React, and FFmpeg. Designed for speed and creative freedom.": "一款使用 Tauri、React 和 FFmpeg 构建的现代原生视频编辑器，为速度与创作自由而设计。",
    "Loading...": "正在加载...",
    "${x.position+1} undo actions available": "${x.position+1} 个撤销操作可用",
    "${x.size-x.position-1} redo actions available": "${x.size-x.position-1} 个重做操作可用",
    "Search ${s===\"effects\"?\"sound effects\":\"music\"}...": "搜索${s===\"effects\"?\"音效\":\"音乐\"}...",
}


EXPORT_MAP = {
    "720p Fast": "720p 快速",
    "1080p Fast": "1080p 快速",
    "1080p Quality": "1080p 高质量",
    "4K Quality": "4K 高质量",
    "Fast": "快速",
    "Quality": "高质量",
    "Professional": "专业",
    "percent": "百分比",
    "Video": "视频",
    "Export failed": "导出失败",
    "Export Video": "导出视频",
    "Export Preset": "导出预设",
    "Checking FFmpeg…": "正在检查 FFmpeg…",
    "FFmpeg ready": "FFmpeg 已就绪",
    "FFmpeg missing": "未找到 FFmpeg",
    "Install FFmpeg and add to PATH": "请安装 FFmpeg 并添加到 PATH",
    "Project": "项目",
    "Name": "名称",
    "Save Name": "保存名称",
    "Click to rename project": "点击重命名项目",
    "Duration": "时长",
    "Canvas": "画布",
    "Frame Rate": "帧率",
    "Export Settings": "导出设置",
    "Resolution": "分辨率",
    "Codec": "编码器",
    "Quality": "质量",
    "Pixel Format": "像素格式",
    "Est. File Size": "预计文件大小",
    "Output": "输出",
    "No output file selected…": "未选择输出文件…",
    "Browse": "浏览",
    "No content to export": "没有可导出的内容",
    "Add clips to the timeline before exporting.": "请先将片段添加到时间线。",
    "FFmpeg is required": "需要 FFmpeg",
    "Video export requires FFmpeg to be installed and available in your system PATH.": "视频导出需要安装 FFmpeg，并确保它在系统 PATH 中可用。",
    "Frame ": "帧 ",
    "ETA ": "剩余 ",
    "Encoding ": "正在编码 ",
    "Do not close this window during export": "导出期间请勿关闭此窗口",
    "Export Complete": "导出完成",
    "Your video has been exported successfully.": "视频已成功导出。",
    " frames": " 帧",
    " ms/frame": " 毫秒/帧",
    "Reveal in Finder": "在文件夹中显示",
    "Export Another": "继续导出",
    "Export Failed": "导出失败",
    "An unexpected error occurred during export.": "导出过程中发生意外错误。",
    "Try Again": "重试",
    "Cancel": "取消",
    "Export": "导出",
    "Close": "关闭",
    "Done": "完成",
}


def esc(s: str, quote: str) -> str:
    s = s.replace("\\", "\\\\")
    if quote == '"':
        return s.replace('"', '\\"')
    if quote == "'":
        return s.replace("'", "\\'")
    return s.replace("`", "\\`")


def replace_string_literals(text: str, mapping: dict[str, str]) -> tuple[str, int, int]:
    hits = {}
    for old, new in sorted(mapping.items(), key=lambda item: len(item[0]), reverse=True):
        count = 0
        for quote in ['"', "'", "`"]:
            before = f"{quote}{esc(old, quote)}{quote}"
            after = f"{quote}{esc(new, quote)}{quote}"
            found = text.count(before)
            if found:
                text = text.replace(before, after)
                count += found
        if count:
            hits[old] = count
    return text, sum(hits.values()), len(mapping) - len(hits)


def read_pe_sections(exe_bytes: bytes) -> tuple[int, list[dict[str, int | str]]]:
    pe_offset = struct.unpack_from("<I", exe_bytes, 0x3C)[0]
    if exe_bytes[pe_offset:pe_offset + 4] != b"PE\0\0":
        raise RuntimeError("目标文件不是有效的 PE 可执行文件。")
    coff = pe_offset + 4
    _, section_count, _, _, _, optional_header_size, _ = struct.unpack_from("<HHIIIHH", exe_bytes, coff)
    optional_header = coff + 20
    magic = struct.unpack_from("<H", exe_bytes, optional_header)[0]
    if magic != 0x20B:
        raise RuntimeError("当前补丁器只支持 64 位 Clypra。")
    image_base = struct.unpack_from("<Q", exe_bytes, optional_header + 24)[0]
    section_table = optional_header + optional_header_size
    sections: list[dict[str, int | str]] = []
    for idx in range(section_count):
        offset = section_table + idx * 40
        name = exe_bytes[offset:offset + 8].rstrip(b"\0").decode("ascii", "replace")
        virtual_size, virtual_address, raw_size, raw_pointer = struct.unpack_from("<IIII", exe_bytes, offset + 8)
        sections.append(
            {
                "name": name,
                "virtual_size": virtual_size,
                "virtual_address": virtual_address,
                "raw_size": raw_size,
                "raw_pointer": raw_pointer,
            }
        )
    return image_base, sections


def file_offset_to_va(file_offset: int, image_base: int, sections: list[dict[str, int | str]]) -> int:
    for section in sections:
        raw_pointer = int(section["raw_pointer"])
        raw_size = int(section["raw_size"])
        if raw_pointer <= file_offset < raw_pointer + raw_size:
            return image_base + int(section["virtual_address"]) + (file_offset - raw_pointer)
    raise RuntimeError(f"无法将文件偏移 0x{file_offset:x} 转为虚拟地址。")


def list_assets(exe_bytes: bytes) -> list[dict[str, int | str]]:
    assets: list[dict[str, int | str]] = []
    seen_offsets: set[int] = set()
    for match in ASSET_RE.finditer(exe_bytes):
        if match.start() in seen_offsets:
            continue
        seen_offsets.add(match.start())
        assets.append({"path": match.group().decode("ascii"), "offset": match.start(), "name_end": match.end()})
    assets.sort(key=lambda item: int(item["offset"]))
    for idx, item in enumerate(assets):
        item["next_offset"] = int(assets[idx + 1]["offset"]) if idx + 1 < len(assets) else len(exe_bytes)
        item["stored_len_guess"] = int(item["next_offset"]) - int(item["name_end"])
    return assets


def choose_asset(assets: list[dict[str, int | str]], pattern: str) -> dict[str, int | str]:
    matches = [item for item in assets if re.fullmatch(pattern, str(item["path"]))]
    if len(matches) != 1:
        found = ", ".join(str(item["path"]) for item in matches) or "无"
        raise RuntimeError(f"无法唯一定位资源 {pattern}，找到：{found}")
    return matches[0]


def find_resource_record(
    exe_bytes: bytes,
    data_va: int,
    path_va: int,
    path_len: int,
    max_data_len: int,
) -> tuple[int, int]:
    pointer = struct.pack("<Q", data_va)
    refs: list[int] = []
    start = 0
    while True:
        pos = exe_bytes.find(pointer, start)
        if pos < 0:
            break
        refs.append(pos)
        start = pos + 1
    candidates: list[tuple[int, int]] = []
    for ref in refs:
        if ref + 16 > len(exe_bytes):
            continue
        data_len = struct.unpack_from("<Q", exe_bytes, ref + 8)[0]
        prev_path_va = struct.unpack_from("<Q", exe_bytes, ref - 16)[0] if ref >= 16 else 0
        prev_path_len = struct.unpack_from("<Q", exe_bytes, ref - 8)[0] if ref >= 8 else 0
        if (
            0 < data_len <= max_data_len
            and prev_path_va == path_va
            and prev_path_len == path_len
        ):
            candidates.append((ref, data_len))
    if len(candidates) != 1:
        raise RuntimeError(f"无法唯一定位资源表记录 data_va=0x{data_va:x}，候选数：{len(candidates)}")
    return candidates[0]


def patch_asset(
    exe_bytes: bytearray,
    asset: dict[str, int | str],
    image_base: int,
    sections: list[dict[str, int | str]],
    mapping: dict[str, str],
) -> tuple[str, int, int, int]:
    path = str(asset["path"])
    name_end = int(asset["name_end"])
    stored_len_guess = int(asset["stored_len_guess"])
    path_va = file_offset_to_va(int(asset["offset"]), image_base, sections)
    data_va = file_offset_to_va(name_end, image_base, sections)
    record_offset, old_len = find_resource_record(
        bytes(exe_bytes),
        data_va=data_va,
        path_va=path_va,
        path_len=len(path.encode("ascii")),
        max_data_len=stored_len_guess,
    )
    source = brotli.decompress(bytes(exe_bytes[name_end:name_end + old_len])).decode("utf-8")
    translated, replacement_count, missing_count = replace_string_literals(source, mapping)
    if replacement_count == 0:
        raise RuntimeError(f"{path} 没有发生任何替换，可能版本不匹配。")
    packed = brotli.compress(translated.encode("utf-8"), quality=11)
    if len(packed) > old_len:
        raise RuntimeError(f"{path} 压缩后 {len(packed)} 字节，超过原槽位 {old_len} 字节。")
    exe_bytes[name_end:name_end + len(packed)] = packed
    exe_bytes[name_end + len(packed):name_end + old_len] = b"\0" * (old_len - len(packed))
    struct.pack_into("<Q", exe_bytes, record_offset + 8, len(packed))
    decoded = brotli.decompress(bytes(exe_bytes[name_end:name_end + len(packed)])).decode("utf-8")
    if decoded != translated:
        raise RuntimeError(f"{path} 写回后 Brotli 校验失败。")
    if not any("\u4e00" <= ch <= "\u9fff" for ch in decoded):
        raise RuntimeError(f"{path} 写回后未检测到中文。")
    return path, replacement_count, missing_count, len(packed)


def stop_running_clypra() -> None:
    subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-Command",
            "Get-Process clypra -ErrorAction SilentlyContinue | Stop-Process -Force",
        ],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def clear_webview_code_cache() -> None:
    for child in [WEBVIEW_CODE_CACHE / "js", WEBVIEW_CODE_CACHE / "wasm"]:
        if child.exists():
            shutil.rmtree(child, ignore_errors=True)
        child.mkdir(parents=True, exist_ok=True)


def make_backup(exe: Path) -> Path:
    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = exe.with_name(f"{exe.name}.bak-{timestamp}")
    shutil.copy2(exe, backup)
    return backup


def normalize_exe_path(value: str | os.PathLike[str] | Path) -> Path:
    raw = str(value).strip().strip('"').strip("'")
    exe = Path(raw).expanduser()
    if exe.is_dir():
        exe = exe / "clypra.exe"
    return exe


def ask_for_exe_path() -> Path:
    print("未在默认位置找到 Clypra。")
    print("如果你把 Clypra 安装在 D 盘或其他位置，请粘贴 clypra.exe 的完整路径。")
    print(r"示例：D:\Programs\Clypra\clypra.exe")
    while True:
        raw = input("请输入 clypra.exe 路径，直接回车退出：").strip()
        if not raw:
            raise FileNotFoundError(f"找不到 Clypra：{DEFAULT_EXE}")
        exe = normalize_exe_path(raw)
        if exe.exists():
            return exe
        print(f"这个路径不存在：{exe}")


def resolve_exe_path(explicit_path: str | None) -> Path:
    if explicit_path:
        return normalize_exe_path(explicit_path)
    if DEFAULT_EXE.exists():
        return DEFAULT_EXE
    if sys.stdin.isatty():
        return ask_for_exe_path()
    return DEFAULT_EXE


def patch_exe(exe: Path, dry_run: bool = False, keep_process: bool = False) -> None:
    if not exe.exists():
        raise FileNotFoundError(f"找不到 Clypra：{exe}")
    if not keep_process:
        stop_running_clypra()
    exe_bytes = bytearray(exe.read_bytes())
    image_base, sections = read_pe_sections(bytes(exe_bytes))
    assets = list_assets(bytes(exe_bytes))
    export_asset = choose_asset(assets, r"/assets/ExportDialog-[A-Za-z0-9_-]+\.js")
    index_asset = choose_asset(assets, r"/assets/index-[A-Za-z0-9_-]+\.js")

    patched = bytearray(exe_bytes)
    results = [
        patch_asset(patched, export_asset, image_base, sections, EXPORT_MAP),
        patch_asset(patched, index_asset, image_base, sections, INDEX_MAP),
    ]

    for path, replacements, missing, packed_len in results:
        print(f"{path}: 替换 {replacements} 处，未命中翻译 {missing} 条，压缩后 {packed_len} 字节")
    if dry_run:
        print("dry-run 模式：未写入文件。")
        return

    backup = make_backup(exe)
    exe.write_bytes(patched)
    clear_webview_code_cache()
    print(f"已备份原文件：{backup}")
    print(f"已写入汉化补丁：{exe}")
    print("已清理 WebView Code Cache。")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Clypra 简体中文汉化补丁器")
    parser.add_argument(
        "exe_path",
        nargs="?",
        help="可选：clypra.exe 路径。也可以把 clypra.exe 直接拖到 run_patch.bat 上。",
    )
    parser.add_argument(
        "--exe",
        default=None,
        help=f"clypra.exe 路径，默认：{DEFAULT_EXE}",
    )
    parser.add_argument("--dry-run", action="store_true", help="只检测和构建补丁，不写入文件")
    parser.add_argument("--keep-process", action="store_true", help="不自动结束正在运行的 clypra 进程")
    args = parser.parse_args(argv)
    if args.exe_path and args.exe:
        parser.error("请只使用一种路径写法：直接写路径，或者使用 --exe。")

    try:
        exe = resolve_exe_path(args.exe_path or args.exe)
        patch_exe(exe, dry_run=args.dry_run, keep_process=args.keep_process)
        return 0
    except Exception as exc:
        print(f"失败：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
