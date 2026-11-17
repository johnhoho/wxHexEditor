# -*- coding: utf-8 -*-
"""Minimal PO -> MO compiler (gettext little-endian MO format)."""
import re, struct, sys

def unquote(s):
    s = s.strip()
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1]
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c == "\\":
            n = s[i+1]
            out.append({"n":"\n","t":"\t","r":"\r","\\":"\\","\"":'"'}.get(n, n))
            i += 2
        else:
            out.append(c); i += 1
    return "".join(out)

def parse_po(path):
    entries = {}
    msgid = msgstr = None
    mode = None
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("msgid "):
            if msgid is not None:
                entries[msgid] = msgstr
            msgid, msgstr, mode = unquote(line[6:]), "", "id"
        elif line.startswith("msgstr "):
            msgstr = unquote(line[7:]); mode = "str"
        elif line.startswith("\""):
            v = unquote(line)
            if mode == "id": msgid += v
            else: msgstr += v
    if msgid is not None:
        entries[msgid] = msgstr
    # NOTE: keep the empty msgid header entry -- gettext needs it to read the
    # charset declaration, otherwise wx falls back to the ANSI codepage and
    # renders UTF-8 translations as mojibake.
    return entries

def write_mo(entries, path):
    keys = sorted(entries.keys())
    offsets, ids, strs = [], [], []
    for k in keys:
        kb, vb = k.encode("utf-8"), entries[k].encode("utf-8")
        offsets.append((len(ids), len(kb), len(strs), len(vb)))
        ids.append(kb); strs.append(vb)
    keystart = 7*4 + 16*len(keys)
    valuestart = keystart + sum(len(x)+1 for x in ids)  # keys + NUL separators
    koffsets, voffsets = [], []
    koff, voff = keystart, valuestart
    for _, kl, _, vl in offsets:
        koffsets.append((kl, koff)); koff += kl + 1  # +1 for NUL separator
        voffsets.append((vl, voff)); voff += vl + 1
    output = struct.pack("<IIIIIII", 0x950412de, 0, len(keys), 7*4, 7*4+len(keys)*8, 0, 0)
    for l, o in koffsets: output += struct.pack("<II", l, o)
    for l, o in voffsets: output += struct.pack("<II", l, o)
    for b in ids: output += b + b"\x00"
    for b in strs: output += b + b"\x00"
    open(path, "wb").write(output)
    print("wrote", path, len(keys), "entries")

if __name__ == "__main__":
    po, mo = sys.argv[1], sys.argv[2]
    write_mo(parse_po(po), mo)
