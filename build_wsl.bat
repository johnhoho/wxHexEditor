@echo off
rem ============================================================
rem  双击运行: 在 WSL 里构建 wxHexEditor（Linux/GTK 版）
rem  结果日志: C:\tmp\wxHexEditor\wsl_build.log
rem  结果标记: C:\tmp\wxHexEditor\wsl_build_result.txt
rem ============================================================
chcp 65001 >nul
cd /d C:\tmp\wxHexEditor

echo 正在 WSL 中构建 wxHexEditor（串行编译，约 10~20 分钟）...
echo 全部输出同时写入 wsl_build.log，本窗口可随时关闭（编译会中断）。
echo.

wsl -e bash -c "bash /mnt/c/tmp/wxHexEditor/wsl_build.sh"

echo.
if exist wsl_build_result.txt type wsl_build_result.txt
echo.
echo ======== 完毕，请把 wsl_build.log 的内容反馈给助手 ========
pause
