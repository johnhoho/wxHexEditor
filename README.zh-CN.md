# wxHexEditor（修改版）

[English](README.md) | 简体中文

基于 [EUA/wxHexEditor](https://github.com/EUA/wxHexEditor) 的二次开发版本，遵循 **GPL v2**。
上游官网：http://www.wxhexeditor.org

本版本在保留上游全部功能的基础上，做了以下改进（当前版本 **0.26**）：

## 主要修改

> **说明：本仓库的全部修改均由 AI（WorkBuddy）自动完成。**

- **多工具链构建**：Windows 上同时支持 MSVC + CMake 与 MinGW GCC（posix-seh-msvcrt）+ make，Linux（GTK + make）保持可用；三套构建互不干扰（`build/`、`build-mingw/`、`build-wsl/` 独立目录）
- **中文界面**：完整简繁中文翻译；18 种语言的菜单/工具栏/状态栏翻译补全（含上游 po 缺失的 msgid 与 `Showing Page: %llu/%I64u` 双 printf 变体）
- **菜单加速键统一**：zh_CN/zh_TW 统一为"字母在前"格式（`&N新的`、`&A另存为`）
- **字形回退**：当前字体缺字时自动从回退字体链补字（Win32），中文/emoji 不再显示方块
- **字体选择**：偏好设置中可选界面字体
- **界面修复**：hex 区与文本列对齐、滚动条遮挡、选区偏移、半边字、行相位等大量布局修复
- **语言名称去国家信息**：界面与配置只保留语言名（如 "Chinese (Simplified)"）
- `tools/` 目录提供纯 Python 的 PO↔MO 工具脚本，无需 gettext 即可维护翻译

## 编译

### Windows + Visual Studio + CMake

```
cmake -G "Visual Studio 17 2022" -A x64 -DCMAKE_BUILD_TYPE=Release ^
      -DwxWidgets_ROOT_DIR=<wx 3.3.x vc14x DLL 版路径> ^
      -DwxWidgets_LIB_DIR=<...>/lib/vc14x_x64_dll .
cmake --build . --config Release
```

### Windows + MinGW GCC + make（与 gcc 版 wxWidgets 配套）

```
cmake -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release ^
      -DCMAKE_C_COMPILER=<gcc路径> -DCMAKE_CXX_COMPILER=<g++路径> ^
      -DwxWidgets_ROOT_DIR=<wx 3.3.x gcc DLL 版路径> ^
      -DwxWidgets_LIB_DIR=<...>/lib/gcc1620_x64_dll ..
make -j1        # 内存受限时勿用多线程
```

工具链选型须与 wx DLL 匹配：wx DLL 导入 `msvcrt.dll` 时用 **x86_64 + posix + seh + msvcrt** 版 GCC；运行时须随程序部署工具链自带的 `libstdc++-6.dll`、`libgcc_s_seh-1.dll`、`libwinpthread-1.dll`。

### Linux / WSL（GTK）

```
# Ubuntu/Debian: 依赖 build-essential cmake libgtk-3-dev libwxgtk3.2-dev
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j1
```

产物输出到 `bin/`（Linux 生成无扩展名的 `wxHexEditor`）。翻译文件 `.mo` 需部署到 exe 同目录的 `locale/<语言>/` 下（`tools/` 脚本可从 `locale/*.po` 生成）。

## License

GPL v2（见 [LICENSE](LICENSE)），修改部分同样以 GPL v2 发布。
