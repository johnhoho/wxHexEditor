# -*- coding: utf-8 -*-
"""补充菜单翻译: Import Template / Hex2Color Mode / Open Memory SPD / 相关 tooltip,
并修正 zh_CN 的 Save &As、TAG 术语与 XORView Thru。然后重新编译 .mo。"""
import os, sys, subprocess
sys.path.insert(0, r"C:\tmp\wxtest")
from pomo import parse_po, write_mo

LOCALE = r"C:\tmp\wxHexEditor\locale"
BIN_LOC = r"C:\tmp\wxHexEditor\bin\locale"
REL_LOC = r"C:\tmp\wxHexEditor\bin\Release\locale"

NEW = {
 "Import Template": {
  "zh_CN":"导入模板","zh_TW":"匯入範本","ja_JP":"テンプレートをインポート","ko":"템플릿 가져오기",
  "ru":"Импорт шаблона","de":"Vorlage importieren","fr":"Importer un modèle","es":"Importar plantilla",
  "it":"Importa modello","pt_BR":"Importar modelo","tr":"Şablon İçe Aktar","ar":"استيراد قالب",
  "th":"นำเข้าเทมเพลต","nl_NL":"Sjabloon importeren","hu_HU":"Sablon importálása","pl":"Importuj szablon",
  "cs":"Importovat šablonu","ro":"Importare șablon"},
 "Hex2Color Mode": {
  "zh_CN":"Hex2Color 模式","zh_TW":"Hex2Color 模式","ja_JP":"Hex2Color モード","ko":"Hex2Color 모드",
  "ru":"Режим Hex2Color","de":"Hex2Color-Modus","fr":"Mode Hex2Color","es":"Modo Hex2Color",
  "it":"Modalità Hex2Color","pt_BR":"Modo Hex2Color","tr":"Hex2Color Modu","ar":"وضع Hex2Color",
  "th":"โหมด Hex2Color","nl_NL":"Hex2Color-modus","hu_HU":"Hex2Color mód","pl":"Tryb Hex2Color",
  "cs":"Režim Hex2Color","ro":"Mod Hex2Color"},
 "Open Memory SPD": {
  "zh_CN":"打开内存 SPD","zh_TW":"開啟記憶體 SPD","ja_JP":"メモリ SPD を開く","ko":"메모리 SPD 열기",
  "ru":"Открыть SPD памяти","de":"Speicher-SPD öffnen","fr":"Ouvrir le SPD de la mémoire",
  "es":"Abrir SPD de memoria","it":"Apri SPD della memoria","pt_BR":"Abrir SPD da memória",
  "tr":"Bellek SPD'sini Aç","ar":"فتح SPD الذاكرة","th":"เปิด SPD หน่วยความจำ",
  "nl_NL":"Geheugen-SPD openen","hu_HU":"Memória SPD megnyitása","pl":"Otwórz SPD pamięci",
  "cs":"Otevřít SPD paměti","ro":"Deschide SPD memorie"},
 "Colorize HEX values with representing colors.": {
  "zh_CN":"用对应颜色为十六进制值着色。","zh_TW":"以對應顏色為十六進位值著色。",
  "ja_JP":"16 進値を対応する色で着色します。","ko":"16진수 값을 해당 색상으로 표시합니다.",
  "ru":"Раскрашивать HEX-значения соответствующими цветами.",
  "de":"HEX-Werte mit den zugehörigen Farben einfärben.",
  "fr":"Colorier les valeurs hexadécimales avec leurs couleurs.",
  "es":"Colorear los valores HEX con sus colores.","it":"Colora i valori HEX con i colori corrispondenti.",
  "pt_BR":"Colorir valores HEX com as cores correspondentes.",
  "tr":"HEX değerlerini karşılık gelen renklerle renklendir.","ar":"تلوين القيم السداسية عشرية بالألوان المقابلة.",
  "th":"ระบายสีค่า HEX ด้วยสีที่สอดคล้องกัน","nl_NL":"HEX-waarden kleuren met bijbehorende kleuren.",
  "hu_HU":"HEX értékek színezése a megfelelő színekkel.",
  "pl":"Kolorowanie wartości HEX odpowiadającymi im kolorami.",
  "cs":"Barevné odlišení HEX hodnot odpovídajícími barvami.",
  "ro":"Colorare valorilor HEX cu culorile corespunzătoare."},
 "Allow to edit Memory SPD values": {
  "zh_CN":"允许编辑内存 SPD 数值","zh_TW":"允許編輯記憶體 SPD 數值",
  "ja_JP":"メモリ SPD の値を編集できます","ko":"메모리 SPD 값을 편집할 수 있습니다",
  "ru":"Позволяет редактировать значения SPD памяти",
  "de":"Ermöglicht das Bearbeiten der Speicher-SPD-Werte",
  "fr":"Permet de modifier les valeurs SPD de la mémoire",
  "es":"Permite editar los valores SPD de la memoria",
  "it":"Consente di modificare i valori SPD della memoria",
  "pt_BR":"Permite editar os valores SPD da memória",
  "tr":"Bellek SPD değerlerinin düzenlenmesine izin verir",
  "ar":"يسمح بتعديل قيم SPD الذاكرة",
  "th":"อนุญาตให้แก้ไขค่า SPD ของหน่วยความจำ",
  "nl_NL":"Maakt bewerken van geheugen-SPD-waarden mogelijk",
  "hu_HU":"Lehetővé teszi a memória SPD értékek szerkesztését",
  "pl":"Umożliwia edycję wartości SPD pamięci",
  "cs":"Umožňuje upravovat hodnoty SPD paměti",
  "ro":"Permite editarea valorilor SPD ale memoriei"},
}

# 指定语言的定向修改 (lang, msgid, new msgstr)——仅当原文已存在
UPDATE = [
 ("zh_CN", "Save &As",     "另存为(&A)"),
 ("zh_CN", "XORView Thru", "XOR 透视查看"),
 ("zh_CN", "Import TAGs",  "导入标记"),
 ("zh_CN", "Export TAGs",  "导出标记"),
 ("zh_CN", "TAG Panel",    "标记面板"),
 ("ja_JP", "XORView Thru", "XOR 透過表示"),
]
# 仅当 msgstr 为空时才填充
FILL_EMPTY = [
 ("ko","XORView Thru","XOR 뷰"), ("ar","XORView Thru","عرض XOR"),
 ("th","XORView Thru","มุมมอง XOR"), ("hu_HU","XORView Thru","XOR nézet"),
]

def esc(s):
    return s.replace("\\","\\\\").replace('"','\\"').replace("\n","\\n")

for lang in sorted(os.listdir(LOCALE)):
    po = os.path.join(LOCALE, lang, "wxHexEditor.po")
    if not os.path.isfile(po): continue
    entries = parse_po(po)
    changed = []
    # 追加缺失条目
    for msgid, table in NEW.items():
        val = table.get(lang)
        if val is None: continue
        if msgid not in entries:
            changed.append((msgid, val))
    # 定向修改
    for lg, msgid, val in UPDATE:
        if lg == lang and msgid in entries and entries[msgid] != val:
            changed.append((msgid, val))
    # 空翻译填充
    for lg, msgid, val in FILL_EMPTY:
        if lg == lang and msgid in entries and not entries[msgid].strip():
            changed.append((msgid, val))
    if not changed:
        continue
    with open(po, "a", encoding="utf-8") as f:
        f.write("\n")
        for msgid, val in changed:
            f.write('#: menu translation supplement\nmsgid "%s"\nmsgstr "%s"\n\n' % (esc(msgid), esc(val)))
    # 重新解析并写回 mo (dict 去重: 后写覆盖前面)
    entries = parse_po(po)
    for msgid, val in changed:
        entries[msgid] = val
    for dst in (os.path.join(BIN_LOC, lang, "wxHexEditor.mo"),
                os.path.join(REL_LOC, lang, "wxHexEditor.mo")):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        write_mo(entries, dst)
    print(lang, "updated:", [m for m,_ in changed])
print("done")
