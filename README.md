# wxHexEditor (Modified Build)

[English](README.md) | [简体中文](README.zh-CN.md)

A fork of [EUA/wxHexEditor](https://github.com/EUA/wxHexEditor), licensed under **GPL v2**.
Upstream project: http://www.wxhexeditor.org

> **Note: All modifications in this fork were made entirely by AI (WorkBuddy).**

Current version: **0.26**. Upstream features are fully retained; highlights of this fork:

## Key Modifications

- **Multi-toolchain build**: MSVC + CMake and MinGW GCC (posix-seh-msvcrt) + make on Windows, Linux (GTK + make) still supported; all three live in separate directories (`build/`, `build-mingw/`, `build-wsl/`) without interfering with each other
- **Chinese UI**: full Simplified/Traditional Chinese translation; menu/toolbar/status-bar translations completed for all 18 languages (including msgids missing from the upstream po files and the dual `Showing Page: %llu/%I64u` printf variants)
- **Unified accelerator keys**: zh_CN/zh_TW now use the "letter-first" style (`&N新的`, `&A另存为`)
- **Glyph fallback**: missing glyphs are automatically taken from a fallback font chain (Win32) — no more tofu boxes for Chinese/emoji
- **Font selection**: the UI font can be chosen in Preferences
- **UI fixes**: hex/text column alignment, scrollbar overlap, selection offset, half-rendered glyphs, row phase, and many other layout fixes
- **Country info removed from language names**: UI and config store plain language names only (e.g. "Chinese (Simplified)")
- `tools/` provides pure-Python PO↔MO scripts — translations can be maintained without gettext

## Building

### Windows + Visual Studio + CMake

```
cmake -G "Visual Studio 17 2022" -A x64 -DCMAKE_BUILD_TYPE=Release ^
      -DwxWidgets_ROOT_DIR=<path to wx 3.3.x vc14x DLL build> ^
      -DwxWidgets_LIB_DIR=<...>/lib/vc14x_x64_dll .
cmake --build . --config Release
```

### Windows + MinGW GCC + make (paired with the gcc build of wxWidgets)

```
cmake -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Release ^
      -DCMAKE_C_COMPILER=<path to gcc> -DCMAKE_CXX_COMPILER=<path to g++> ^
      -DwxWidgets_ROOT_DIR=<path to wx 3.3.x gcc DLL build> ^
      -DwxWidgets_LIB_DIR=<...>/lib/gcc1620_x64_dll ..
make -j1        # avoid parallel builds on memory-constrained machines
```

The toolchain must match the wx DLLs: if the wx DLLs import `msvcrt.dll`, use the **x86_64 + posix + seh + msvcrt** GCC build; ship the toolchain's own `libstdc++-6.dll`, `libgcc_s_seh-1.dll` and `libwinpthread-1.dll` alongside the exe.

### Linux / WSL (GTK)

```
# Ubuntu/Debian deps: build-essential cmake libgtk-3-dev libwxgtk3.2-dev
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j1
```

Binaries go to `bin/` (on Linux the output is the extension-less `wxHexEditor`). The `.mo` translation files must be deployed to `locale/<lang>/` next to the executable (generate them from `locale/*.po` with the scripts in `tools/`).

## License

GPL v2 (see [LICENSE](LICENSE)). All modifications are released under the same license.
