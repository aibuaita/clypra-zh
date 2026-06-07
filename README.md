# Clypra 简体中文汉化补丁

这是 Clypra Windows 版的简体中文汉化补丁器。仓库不包含 Clypra 原程序，也不分发修改后的 `clypra.exe`；脚本会在用户本机安装目录中自动备份原文件、修改内嵌前端资源并清理 WebView 代码缓存。

## 适配版本

- Clypra `0.1.0-alpha.1`
- Windows x64
- 默认安装路径：`%LOCALAPPDATA%\Clypra\clypra.exe`

如果 Clypra 更新后资源结构变化，脚本会停止并报错，不会强行修改未知版本。

## 使用方法

1. 安装依赖：

```powershell
python -m pip install -r requirements.txt
```

2. 运行补丁：

```powershell
python .\clypra_han\apply_clypra_zh.py
```

如果 Clypra 不在默认路径：

```powershell
python .\clypra_han\apply_clypra_zh.py --exe "C:\path\to\clypra.exe"
```

也可以先测试不写入文件：

```powershell
python .\clypra_han\apply_clypra_zh.py --dry-run
```

## 回滚

脚本会在同目录生成备份，例如：

```text
clypra.exe.bak-YYYYMMDD-HHMMSS
```

要回滚，退出 Clypra 后把备份文件重命名/复制回 `clypra.exe` 即可。

## 汉化范围

覆盖启动页、项目列表、媒体库、时间线、预览窗口、属性面板、设置页、关于页、导出弹窗、FFmpeg 状态和导出进度等主要可见文案。

保留 `FFmpeg`、`ProRes`、`H.264/H.265`、`Tauri/React/Rust` 等技术名，避免影响导出和运行时逻辑。

## 免责声明

这是非官方社区补丁。使用前请自行备份重要项目文件。仓库仅提供本地补丁逻辑和翻译表，不包含 Clypra 的版权文件、原始资源或修改后的可执行文件。
