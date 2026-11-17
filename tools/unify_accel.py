# -*- coding: utf-8 -*-
"""统一 zh_CN / zh_TW 菜单加速键格式: 字母在前 + 无空格 (&N新的 / &S保存)。"""
import sys, os
sys.path.insert(0, r"C:\tmp\wxtest")
from pomo import parse_po, write_mo

ROOT = r"C:\tmp\wxHexEditor"

ZH_CN = {
 "&File":   "&F文件",
 "&Edit":   "&E编辑",
 "&View":   "&V查看",
 "&Save":   "&S保存",
 "&Quit":   "&Q退出",
 "&Undo":   "&U撤销",
 "&Redo":   "&R重做",
 "&About":  "&A关于",       # 原 '& 关于'，加速键丢失
 "Tools":   "&T工具",       # 上游 msgid 无 &，译文补上
 "Devices": "&D设备",
 "Options": "&O选项",
 "Import TAGs":    "&I导入标记",
 "Export TAGs":    "&E导出标记",
 "Import Template":"&T导入模板",
}
ZH_TW = {
 "&File":   "&F檔案",
 "&Edit":   "&E編輯",
 "&View":   "&V檢視",
 "&Save":   "&S儲存",
 "&Quit":   "&Q結束",      # 原 '結束(&Q)'
 "&Undo":   "&U復原",
 "&Redo":   "&R重做",
 "&About":  "&A關於",      # 原 '& 關於'
 "Tools":   "&T工具",
 "Devices": "&D裝置",
 "Options": "&O選項",
 "Save &As":"&A另存新檔",   # 原 '另存新檔(&A)'
 "Import TAGs":    "&I匯入標籤",
 "Export TAGs":    "&E匯出標籤",
 "Import Template":"&T匯入範本",
}

def apply(lang, table):
    po = os.path.join(ROOT, "locale", lang, "wxHexEditor.po")
    entries = parse_po(po)
    applied = {}
    for mid, val in table.items():
        if mid in entries and entries[mid] != val:
            applied[mid] = (entries[mid], val)
    # 原地替换 (msgstr 整行, 针对每个 msgid 首次出现处)
    lines = open(po, encoding="utf-8").read().splitlines(keepends=True)
    idx = 0
    while idx < len(lines):
        if lines[idx].startswith("msgid "):
            import re
            m = re.match(r'msgid "((?:[^"\\]|\\.)*)"', lines[idx])
            key = m.group(1).encode().decode("unicode_escape") if m else None
            # 简单 unquote
            key = m.group(1) if m else ""
            for esc, ch in [("\\n","\n"),("\\t","\t"),('\\"','"'),("\\\\","\\")]:
                key = key.replace(esc, ch)
            if key in table:
                j = idx + 1
                while j < len(lines) and not lines[j].startswith("msgstr "):
                    j += 1
                if j < len(lines) and lines[j].rstrip("\r\n") != 'msgstr "%s"' % table[key].replace("\\","\\\\").replace('"','\\"'):
                    lines[j] = 'msgstr "%s"\n' % table[key].replace("\\","\\\\").replace('"','\\"')
                idx = j
        idx += 1
    open(po, "w", encoding="utf-8", newline="").write("".join(lines))
    # 重编译 .mo
    entries = parse_po(po)
    for mid, val in table.items():
        if mid in entries:
            entries[mid] = val
    for dst in (os.path.join(ROOT, "bin", "locale", lang, "wxHexEditor.mo"),
                os.path.join(ROOT, "bin", "Release", "locale", lang, "wxHexEditor.mo")):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        write_mo(entries, dst)
    for mid, (old, new) in applied.items():
        print("  %-16s %r -> %r" % (mid, old, new))
    print(lang, "done, changed:", len(applied))

apply("zh_CN", ZH_CN)
apply("zh_TW", ZH_TW)
print("all done")
