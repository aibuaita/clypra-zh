# Clypra 简体中文汉化补丁

这是一个给 Windows 版 Clypra 使用的简体中文汉化补丁。

它不会提供 Clypra 原程序，也不会上传修改后的 `clypra.exe`。这个补丁只是在你自己的电脑上，把已经安装好的 Clypra 改成中文界面。

## 适用版本

- Clypra `0.1.0-alpha.1`
- Windows 版
- 默认安装位置：`C:\Users\你的用户名\AppData\Local\Clypra\clypra.exe`

如果你的 Clypra 更新过，补丁可能会失效。失效时脚本会停止，不会强行乱改。

## 使用方法

### 第一步：安装 Python

如果你电脑里已经安装过 Python，可以跳过这一步。

没有安装的话，先去 Python 官网下载安装：

[https://www.python.org/downloads/](https://www.python.org/downloads/)

安装时一定要勾选：

```text
Add python.exe to PATH
```

### 第二步：下载这个汉化补丁

在本页面点击绿色的 `Code` 按钮，然后点 `Download ZIP`。

下载后，把压缩包解压到任意位置，比如桌面。

### 第三步：关闭 Clypra

汉化前请先退出 Clypra。

如果 Clypra 还在后台运行，也请在任务栏或任务管理器里结束它。

### 第四步：运行汉化

打开解压后的文件夹，双击：

```text
run_patch.bat
```

第一次运行时，它会自动安装需要的小组件，然后开始汉化。

看到窗口里没有报错，并且最后出现类似：

```text
Press any key to continue . . .
```

就表示运行结束了。按任意键关闭窗口，然后重新打开 Clypra。

## 如果打不开 bat 文件

如果 Windows 弹出安全提示，可以选择“更多信息”，再点“仍要运行”。

如果双击后窗口一闪而过，通常是 Python 没装好。请重新安装 Python，并确认安装时勾选了 `Add python.exe to PATH`。

## 如何恢复英文原版

补丁运行时会自动备份原来的程序文件。

备份文件一般在这个文件夹里：

```text
C:\Users\你的用户名\AppData\Local\Clypra
```

名字类似：

```text
clypra.exe.bak-20260607-091120
```

恢复方法：

1. 退出 Clypra。
2. 删除当前的 `clypra.exe`。
3. 把备份文件改名为 `clypra.exe`。
4. 重新打开 Clypra。

## 汉化范围

主要汉化了这些界面：

- 启动页
- 项目列表
- 媒体库
- 时间线
- 预览窗口
- 属性面板
- 设置页
- 关于页
- 导出窗口
- FFmpeg 状态和导出进度

部分技术名称会保留英文，比如 `FFmpeg`、`ProRes`、`H.264`、`H.265` 等。

## 说明

这是非官方汉化补丁，和 Clypra 官方无关。

建议在使用前备份自己的重要项目文件。本仓库不包含 Clypra 的原始程序、版权资源或修改后的可执行文件。
