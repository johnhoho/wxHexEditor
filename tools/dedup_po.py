# -*- coding: utf-8 -*-
"""去重 po（msgid 重复时保留首次出现位置、采用最新译文），并重编译全部 .mo。"""
import os, sys, re
sys.path.insert(0, r"C:\tmp\wxtest")
from pomo import write_mo

LOCALE = r"C:\tmp\wxHexEditor\locale"
BIN_LOC = r"C:\tmp\wxHexEditor\bin\locale"
REL_LOC = r"C:\tmp\wxHexEditor\bin\Release\locale"

def unquote(s):
    s = s.strip()
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            n = s[i+1] if i+1 < len(s) else ""
            out.append({"n":"\n","t":"\t","r":"\r","\\":"\\","\"":'"'}.get(n, n)); i += 2
        else:
            out.append(c); i += 1
    return "".join(out)

def process(path):
    lines = open(path, encoding="utf-8").read().splitlines(keepends=True)
    # 找出每个 msgid 块范围: 从 'msgid "' 行到下一个 'msgid "' 行前
    starts = [i for i,l in enumerate(lines) if l.startswith('msgid ')]
    blocks = []   # (start, end_exclusive, msgid, msgstr, is_multiline_flag)
    for bi, st in enumerate(starts):
        en = starts[bi+1] if bi+1 < len(starts) else len(lines)
        text = "".join(lines[st:en])
        m1 = re.search(r'msgid "((?:[^"\\]|\\.)*)"', text)
        m2 = re.search(r'msgstr "((?:[^"\\]|\\.)*)"', text)
        mid = unquote('"%s"' % m1.group(1)) if m1 else None
        mstr = unquote('"%s"' % m2.group(1)) if m2 else ""
        blocks.append((st, en, mid, mstr))
    # 头块 (msgid "") 与正文; 重复 msgid: 保留首块, 用最后出现的 msgstr, 其余块删除
    lastval = {}
    for st, en, mid, mstr in blocks:
        if mid is not None:
            if mstr.strip():
                lastval[mid] = mstr
    drop = set()
    seen = set()
    for st, en, mid, mstr in blocks:
        if mid is None or mid == "":
            continue
        if mid in seen:
            drop.update(range(st, en))
        else:
            seen.add(mid)
    # 写回: 首块保留但 msgstr 用 lastval
    out = list(lines)
    # 从后往前删除重复块
    for st, en, mid, mstr in sorted(blocks, key=lambda b: -b[0]):
        if st in drop:
            del out[st:en]
    # 更新首块 msgstr
    starts2 = [i for i,l in enumerate(out) if l.startswith('msgid ')]
    for bi, st in enumerate(starts2):
        en = starts2[bi+1] if bi+1 < len(starts2) else len(out)
        m1 = re.search(r'msgid "((?:[^"\\]|\\.)*)"', out[st])
        mid = unquote('"%s"' % m1.group(1)) if m1 else None
        if mid in lastval:
            for i in range(st, en):
                if out[i].startswith("msgstr "):
                    out[i] = 'msgstr "%s"\n' % lastval[mid].replace("\\","\\\\").replace('"','\\"').replace("\n","\\n")
                    break
    open(path, "w", encoding="utf-8", newline="").write("".join(out))
    # 重编译 mo
    sys.path.insert(0, r"C:\tmp\wxtest")
    from pomo import parse_po
    entries = parse_po(path)
    lang = os.path.basename(os.path.dirname(path))
    for dst in (os.path.join(BIN_LOC, lang, "wxHexEditor.mo"),
                os.path.join(REL_LOC, lang, "wxHexEditor.mo")):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        write_mo(entries, dst)
    return len(entries), lastval

def read_mo(p):
    d = open(p, "rb").read()
    magic, ver, n, koff, voff, _, _ = struct.unpack("<IIIIIII", d[:28])
    out = {}
    for i in range(n):
        kl, ko = struct.unpack("<II", d[koff+i*8:koff+i*8+8])
        vl, vo = struct.unpack("<II", d[voff+i*8:voff+i*8+8])
        out[d[ko:ko+kl].decode()] = d[vo:vo+vl].decode()
    return out

import struct
CHECK = ["Save &As","XORView Thru","Import TAGs","Export TAGs","TAG Panel",
         "Import Template","Hex2Color Mode","Open Memory SPD"]
total_dropped = 0
for lang in sorted(os.listdir(LOCALE)):
    po = os.path.join(LOCALE, lang, "wxHexEditor.po")
    if not os.path.isfile(po): continue
    before = sum(1 for _ in open(po, encoding="utf-8"))
    n, lv = process(po)
    after = sum(1 for _ in open(po, encoding="utf-8"))
    m = read_mo(os.path.join(BIN_LOC, lang, "wxHexEditor.mo"))
    bad = [k for k in CHECK if k in m and not m[k].strip()]
    print("%-6s lines %d->%d, mo entries %d, empty-check:%s" % (lang, before, after, n, bad or "ok"))
print("done")
