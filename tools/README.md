# i18n 工具脚本

本项目 18 种语言的 `wxHexEditor.po` 翻译与编译工具（纯 Python，无 gettext 依赖）。

| 脚本 | 用途 |
|---|---|
| `pomo.py` | 极简 PO→MO 编译器（gettext 小端 MO 格式）。用法：`python pomo.py xx.po xx.mo` |
| `update_menu_i18n.py` | 补充菜单项翻译（Import Template / Hex2Color Mode / Open Memory SPD 等） |
| `update_toolbar_i18n.py` | 补充工具栏/面板/状态栏翻译（含 Showing Page 的 %llu/%I64u 双变体） |
| `unify_accel.py` | 统一中文加速键格式（字母在前无空格：&N新的 / &S保存） |
| `dedup_po.py` | po 按 msgid 去重（保留首次出现位置、采用最新译文）并重编译 .mo |

生成的 .mo 需部署到程序同目录的 `locale/<语言>/wxHexEditor.mo`（Linux 下注意 NTFS 挂载无执行/权限位问题）。
