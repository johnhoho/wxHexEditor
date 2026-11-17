# -*- coding: utf-8 -*-
"""补全工具栏/面板/状态栏翻译（18 语言），并处理 Showing Page 的两种 printf 变体。"""
import os, sys
sys.path.insert(0, r"C:\tmp\wxtest")
from pomo import parse_po, write_mo

ROOT = r"C:\tmp\wxHexEditor"
LOCALE = os.path.join(ROOT, "locale")
BINS = [os.path.join(ROOT, "bin", "locale"), os.path.join(ROOT, "bin", "Release", "locale")]

T = {
 "Find and Replace": {
  "zh_CN":"查找并替换","zh_TW":"尋找並取代","ja_JP":"検索と置換","ko":"찾기 및 바꾸기",
  "ru":"Поиск и замена","de":"Suchen und Ersetzen","fr":"Rechercher et remplacer",
  "es":"Buscar y reemplazar","it":"Trova e sostituisci","pt_BR":"Localizar e substituir",
  "tr":"Bul ve Değiştir","ar":"بحث واستبدال","th":"ค้นหาและแทนที่",
  "nl_NL":"Zoeken en vervangen","hu_HU":"Keresés és csere","pl":"Znajdź i zamień",
  "cs":"Najít a nahradit","ro":"Căutare și înlocuire"},
 "Cut selected block and copies to clipboard": {
  "zh_CN":"剪切所选块并复制到剪贴板","zh_TW":"剪下所選區塊並複製到剪貼簿",
  "ja_JP":"選択ブロックを切り取ってクリップボードにコピー",
  "ko":"선택한 블록을 잘라내어 클립보드에 복사",
  "ru":"Вырезать выбранный блок и скопировать в буфер обмена",
  "de":"Ausgewählten Block ausschneiden und in die Zwischenablage kopieren",
  "fr":"Couper le bloc sélectionné et le copier dans le presse-papiers",
  "es":"Cortar el bloque seleccionado y copiarlo al portapapeles",
  "it":"Taglia il blocco selezionato e lo copia negli appunti",
  "pt_BR":"Recortar o bloco selecionado e copiar para a área de transferência",
  "tr":"Seçili bloğu kesip panoya kopyala","ar":"قص الكتلة المحددة ونسخها إلى الحافظة",
  "th":"ตัดบล็อกที่เลือกและคัดลอกไปยังคลิปบอร์ด",
  "nl_NL":"Geselecteerd blok knippen en naar klembord kopiëren",
  "hu_HU":"Kijelölt blokk kivágása és vágólapra másolása",
  "pl":"Wytnij zaznaczony blok i skopiuj do schowka",
  "cs":"Vyjmout vybraný blok a zkopírovat do schránky",
  "ro":"Taie blocul selectat și îl copiază în clipboard"},
 "Delete selected block": {
  "zh_CN":"删除所选块","zh_TW":"刪除所選區塊","ja_JP":"選択ブロックを削除","ko":"선택한 블록 삭제",
  "ru":"Удалить выбранный блок","de":"Ausgewählten Block löschen",
  "fr":"Supprimer le bloc sélectionné","es":"Eliminar el bloque seleccionado",
  "it":"Elimina il blocco selezionato","pt_BR":"Excluir o bloco selecionado",
  "tr":"Seçili bloğu sil","ar":"حذف الكتلة المحددة","th":"ลบบล็อกที่เลือก",
  "nl_NL":"Geselecteerd blok verwijderen","hu_HU":"Kijelölt blokk törlése",
  "pl":"Usuń zaznaczony blok","cs":"Odstranit vybraný blok","ro":"Șterge blocul selectat"},
 "Insert block": {
  "zh_CN":"插入块","zh_TW":"插入區塊","ja_JP":"ブロックを挿入","ko":"블록 삽입",
  "ru":"Вставить блок","de":"Block einfügen","fr":"Insérer un bloc","es":"Insertar bloque",
  "it":"Inserisci blocco","pt_BR":"Inserir bloco","tr":"Blok ekle","ar":"إدراج كتلة",
  "th":"แทรกบล็อก","nl_NL":"Blok invoegen","hu_HU":"Blokk beszúrása","pl":"Wstaw blok",
  "cs":"Vložit blok","ro":"Inserare bloc"},
 "Hide": {
  "zh_CN":"隐藏","zh_TW":"隱藏","ja_JP":"隠す","ko":"숨기기","ru":"Скрыть","de":"Ausblenden",
  "fr":"Masquer","es":"Ocultar","it":"Nascondi","pt_BR":"Ocultar","tr":"Gizle","ar":"إخفاء",
  "th":"ซ่อน","nl_NL":"Verbergen","hu_HU":"Elrejtés","pl":"Ukryj","cs":"Skrýt","ro":"Ascunde"},
 "Convert TAGs": {
  "zh_CN":"转换标记","zh_TW":"轉換標籤","ja_JP":"タグを変換","ko":"태그 변환",
  "ru":"Преобразовать теги","de":"TAGs konvertieren","fr":"Convertir les balises",
  "es":"Convertir etiquetas","it":"Converti tag","pt_BR":"Converter tags",
  "tr":"Etiketleri Dönüştür","ar":"تحويل الوسوم","th":"แปลงแท็ก",
  "nl_NL":"Tags converteren","hu_HU":"Címkék átalakítása","pl":"Konwertuj znaczniki",
  "cs":"Převést značky","ro":"Convertire marcaje"},
 "Cut": {"hu_HU":"Kivágás"},
 "Delete": {"hu_HU":"Törlés"},
 "Insert": {"hu_HU":"Beszúrás"},
 "Find and replace": {"hu_HU":"Keresés és csere"},
}
# Showing Page: 源码拼接出两种 msgid（MinGW/Linux: %llu，MSVC: %I64u）
SP = {
 "zh_CN":"显示页：%s","zh_TW":"顯示頁：%s","ja_JP":"ページ表示: %s","ko":"페이지 표시: %s",
 "ru":"Показана страница: %s","de":"Seite angezeigt: %s","fr":"Page affichée : %s",
 "es":"Mostrando página: %s","it":"Pagina visualizzata: %s","pt_BR":"Exibindo página: %s",
 "tr":"Gösterilen sayfa: %s","ar":"الصفحة المعروضة: %s","th":"แสดงหน้า: %s",
 "nl_NL":"Weergegeven pagina: %s","hu_HU":"Megjelenített oldal: %s","pl":"Wyświetlana strona: %s",
 "cs":"Zobrazená stránka: %s","ro":"Pagina afișată: %s"}
SPECS = ["%llu", "%I64u"]
T["Showing Page: %llu"] = {l: v.replace("%s", "%llu") for l, v in SP.items()}
T["Showing Page: %I64u"] = {l: v.replace("%s", "%I64u") for l, v in SP.items()}

def esc(s):
    return s.replace("\\","\\\\").replace('"','\\"')

for lang in sorted(os.listdir(LOCALE)):
    po = os.path.join(LOCALE, lang, "wxHexEditor.po")
    if not os.path.isfile(po): continue
    entries = parse_po(po)
    changed = []
    for msgid, table in T.items():
        val = table.get(lang)
        if val is None: continue
        if msgid not in entries:
            changed.append((msgid, val))
        elif not entries[msgid].strip() and val:   # 空翻译填充
            changed.append((msgid, val))
    if not changed: continue
    # 追加缺失/空翻译条目（空翻译的 msgid 已存在 -> 先删除原空块再追加，避免重复）
    lines = open(po, encoding="utf-8").read().splitlines(keepends=True)
    drop_ids = {m for m, _ in changed if m in entries}
    if drop_ids:
        import re
        starts = [i for i, l in enumerate(lines) if l.startswith('msgid ')]
        drop = set()
        for bi, st in enumerate(starts):
            en = starts[bi+1] if bi+1 < len(starts) else len(lines)
            m = re.search(r'msgid "((?:[^"\\]|\\.)*)"', "".join(lines[st:en]))
            if not m: continue
            raw = m.group(1)
            for e_, ch in [("\\n","\n"),("\\t","\t"),('\\"','"'),("\\\\","\\")]:
                raw = raw.replace(e_, ch)
            if raw in drop_ids:
                drop.update(range(st, en))
        for st in sorted(drop, reverse=True):
            del lines[st:en]
        open(po, "w", encoding="utf-8", newline="").write("".join(lines))
    with open(po, "a", encoding="utf-8") as f:
        f.write("\n")
        for msgid, val in changed:
            f.write('#: i18n supplement\nmsgid "%s"\nmsgstr "%s"\n\n' % (esc(msgid), esc(val)))
    entries = parse_po(po)
    for msgid, val in changed:
        entries[msgid] = val
    for b in BINS:
        dst = os.path.join(b, lang, "wxHexEditor.mo")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        write_mo(entries, dst)
    print(lang, "updated:", len(changed))
print("done")
