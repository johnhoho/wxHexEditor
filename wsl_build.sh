#!/usr/bin/env bash
# =============================================================================
# wxHexEditor - WSL (Linux/GTK) 一键构建脚本
# 用法:  在 WSL 里执行  bash /mnt/c/tmp/wxHexEditor/wsl_build.sh
#        或在 Windows 下双击同目录的 build_wsl.bat
# 说明:  -j1 串行编译，内存占用最小；全部输出写入 wsl_build.log
# =============================================================================
set -o pipefail

PROJ_WIN='C:\tmp\wxHexEditor'
PROJ=/mnt/c/tmp/wxHexEditor
LOG=$PROJ/wsl_build.log
RESULT=$PROJ/wsl_build_result.txt
BUILD=$PROJ/build-wsl

: > "$LOG"
exec > >(tee -a "$LOG") 2>&1

step() { echo; echo "=============================================================="; echo "== $*"; echo "=============================================================="; }
fail() { echo; echo "[FAILED] $*"; echo "FAILED: $*" > "$RESULT"; exit 1; }
ok()   { echo; echo "[OK] $*"; }

step "0. 环境信息"
if grep -qi microsoft /proc/version; then echo "WSL: yes ($(head -1 /proc/version))"; else echo "WSL: NO - 请在 WSL 内运行本脚本"; fi
. /etc/os-release 2>/dev/null && echo "Distro: $PRETTY_NAME"
echo "Kernel: $(uname -r)"
echo "CPU cores: $(nproc)"
free -h || true
command -v gcc   >/dev/null && echo "gcc:   $(gcc --version | head -1)"   || echo "gcc:   未安装"
command -v cmake >/dev/null && echo "cmake: $(cmake --version | head -1)" || echo "cmake: 未安装"
command -v wx-config >/dev/null && echo "wxWidgets: $(wx-config --version) ($(wx-config --selected-config 2>/dev/null | tr '\n' ' '))" || echo "wxWidgets: 未安装"

# ---------------------------------------------------------------------------
step "1. 安装依赖（需要 sudo 密码；已装则跳过）"
PKGS="build-essential cmake pkg-config file libgtk-3-dev gettext"
if command -v apt-get >/dev/null; then
    # 选择系统中可用的 wxWidgets 开发包（3.2 优先，其次 3.0）
    WXPKG=""
    for c in libwxgtk3.2-dev libwxgtk3.0-gtk3-dev libwxgtk3.0gtk3-dev libwxgtk-common-dev; do
        apt-cache show "$c" >/dev/null 2>&1 && { WXPKG="$c"; break; }
    done
    [ -z "$WXPKG" ] && WXPKG="libwxgtk3.2-dev"
    echo "将安装: $PKGS $WXPKG"
    sudo apt-get update -y || echo "[warn] apt-get update 失败，继续尝试"
    sudo DEBIAN_FRONTEND=noninteractive apt-get install -y $PKGS "$WXPKG" || fail "依赖安装失败，请查看上方 apt 报错"
elif command -v dnf >/dev/null; then
    sudo dnf install -y gcc gcc-c++ cmake make pkgconfig gtk3-devel wxGTK3-devel || fail "依赖安装失败"
elif command -v pacman >/dev/null; then
    sudo pacman -S --noconfirm base-devel cmake gtk3 wxwidgets-gtk3 || fail "依赖安装失败"
else
    fail "未识别的发行版（无 apt/dnf/pacman），请手动安装 build-essential cmake libgtk-3-dev libwxgtk3.x-dev 后重跑"
fi

ok "依赖就绪"
echo "wx-config: $(wx-config --version 2>/dev/null || echo 未找到)" || true
command -v wx-config >/dev/null || fail "wx-config 仍不存在，wxWidgets 开发包安装异常"

# ---------------------------------------------------------------------------
step "2. CMake 配置（build-wsl 目录，与 Windows 构建互不影响）"
mkdir -p "$BUILD" && cd "$BUILD"
cmake -DCMAKE_BUILD_TYPE=Release "$PROJ" 2>&1 | tail -25
[ ${PIPESTATUS[0]} -ne 0 ] && fail "CMake 配置失败"

# ---------------------------------------------------------------------------
step "3. 编译（-j1 串行，防内存不足；预计 10~20 分钟）"
make -j1 2>&1 | tail -40
RC=${PIPESTATUS[0]}
[ $RC -ne 0 ] && fail "编译失败 (exit $RC)，请把 wsl_build.log 末尾报错发回来"

# ---------------------------------------------------------------------------
step "4. 结果"
# CMake 把可执行文件输出到项目根的 bin/（与 Windows 版共用目录，名字不带 .exe）
EXE="$PROJ/bin/wxHexEditor"
[ -f "$EXE" ] || EXE=$(find "$BUILD" "$PROJ/bin" -name wxHexEditor -type f 2>/dev/null | grep -v '\.exe$' | head -1)
[ -z "$EXE" ] && fail "编译完成但未找到可执行文件"
ls -lh "$EXE"

# /mnt/c 是 NTFS 挂载，ELF 没有可执行位 → 拷到 WSL 原生 ext4 再运行
RUNDIR="$HOME/wxHexEditor-wsl"
mkdir -p "$RUNDIR"
cp -f "$EXE" "$RUNDIR/wxHexEditor" && chmod +x "$RUNDIR/wxHexEditor"
RUNEXE="$RUNDIR/wxHexEditor"
ls -lh "$RUNEXE"

# 多语言翻译文件也要拷到 exe 同目录（程序按 "exe所在目录/locale" 查找）
# 编译好的 .mo 在项目的 bin/locale 下（CMake 会把 exe 输出到 bin/）；locale/ 只有 .po 源
if [ -d "$PROJ/bin/locale" ]; then
    cp -rf "$PROJ/bin/locale" "$RUNDIR/locale" && echo "locale → $RUNDIR/locale (已复制，含 .mo)"
else
    cp -rf "$PROJ/locale" "$RUNDIR/locale" && echo "locale → $RUNDIR/locale (仅 .po 源，需 msgfmt 编译)"
fi

# 便捷启动脚本：过滤 GTK 噪音断言；Wayland 下自动走 X11 后端避免光标瑕疵
cat > "$RUNDIR/run_wxhex.sh" <<'EOS'
#!/usr/bin/env bash
DIR="$(cd "$(dirname "$0")" && pwd)"
# Wayland 会话下自动切 X11 后端，避免上游提示的光标显示瑕疵
if [ -n "$WAYLAND_DISPLAY" ] || [ "$XDG_SESSION_TYPE" = "wayland" ]; then
    [ -z "$GDK_BACKEND" ] && export GDK_BACKEND=x11
fi
"$DIR/wxHexEditor" "$@" 2> >(grep -v "gtk_box_gadget_distribute\|Gtk-CRITICAL" >&2)
EOS
chmod +x "$RUNDIR/run_wxhex.sh"

echo
echo "=== 运行试试（WSLg 图形界面，直接在 WSL 终端里执行）==="
echo "  $RUNEXE            （或用静音包装: $RUNDIR/run_wxhex.sh）"
echo "  （或打开一个文件）:  $RUNEXE /mnt/c/tmp/unicode_test.txt"
ok "构建成功 → $RUNEXE"
echo "OK: $RUNEXE" > "$RESULT"
echo "（日志: $LOG）"
