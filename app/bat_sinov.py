"""OBER — .bat fayllar sintaksis tekshiruvi.

NEGA KERAK (2026-08-13)
-----------------------
NAVBATCHI.bat oyna ochilib darhol yopilardi: `if exist (...)` blokidagi
izoh satridan `rem` prefiksi tushib ketgan edi — satr bajariladigan
buyruqqa aylanib, ichidagi `).` belgisi blokni buzgan (`. was
unexpected at this time.`). Xato satrni ko'z bilan topish qiyin:
cmd blok qavslarini satr bo'yicha sanaydi va bitta bekorchi `)`
butun faylni ishdan chiqaradi.

Bu skript barcha `*.bat` fayllarni tekshiradi:
1. Blok qavslari muvozanati — bekorchi `)` yoki yopilmagan blok.
2. `goto` yorliqlari — yo'q yorliqqa havola faylni to'xtatadi.
3. no-ASCII baytlar — batch izohlarida maxsus belgilar kodlashni buzadi.
4. Satr oxiri — cmd uchun CRLF standart; aralash holat xavfli.

Ishlatish:
    python bat_sinov.py            # hamma *.bat ni tekshiradi
    python bat_sinov.py fayl.bat   # faqat bitta fayl
"""
from __future__ import annotations

import glob
import re
import sys


def tekshir(yol: str) -> tuple[list[str], list[str]]:
    """Bitta .bat faylni tekshiradi. Qaytaradi: (xatolar, ogohlantirishlar)."""
    xatolar: list[str] = []
    ogoh: list[str] = []
    try:
        raw = open(yol, "rb").read()
    except OSError as e:
        return [f"ochib bo'lmadi: {e}"], []

    # --- no-ASCII va satr oxiri ---
    no_ascii = [i + 1 for i, b in enumerate(raw) if b > 127]
    if no_ascii:
        ogoh.append(f"no-ASCII baytlar: {no_ascii[:10]}{'...' if len(no_ascii) > 10 else ''}")
    crlf = raw.count(b"\r\n")
    lf = raw.count(b"\n") - crlf
    if lf > 0 and crlf > 0:
        ogoh.append(f"aralash satr oxiri (CRLF={crlf}, LF={lf}) — cmd uchun xavfli")

    text = raw.decode("utf-8", errors="replace").splitlines()

    # --- goto yorliqlari ---
    yorliqlar = {m.group(1) for s in text if (m := re.match(r"\s*:([A-Za-z0-9_.]+)", s))}
    for i, s in enumerate(text):
        for g in re.findall(r"\bgoto\s+:?([A-Za-z0-9_.]+)\b", s, re.I):
            if g not in yorliqlar:
                ogoh.append(f"satr {i + 1}: `goto {g}` — yorliq faylda topilmadi")

    # --- qavs bloklari muvozanati ---
    # cmd blok qavslarini ( ) sanaydi va IZOH SATRLARINI HAM hisobga
    # oladi. Shuning uchun blok ichidagi rem satrida qavs bo'lmasligi
    # yoki juft bo'lishi shart. Yopuvchi `)` dan ko'p ochuvchi `(` dan
    # ortiq bo'lgan har qanday satr — shubhali.
    chuqur = 0
    for_set = False        # ko'p qatorli `for %%f in (` holati
    for i, s in enumerate(text):
        s_t = s.strip()
        if not s_t or s_t.startswith("::"):
            continue
        if s_t.lower().startswith("rem"):
            och = s.count("(") - s.count(")")
            if chuqur > 0 and och != 0:
                ogoh.append(f"satr {i + 1}: rem izohidagi qavslar muvozanatsiz "
                            f"(net {och:+d}) — blokni buzishi mumkin")
            continue
        s_q = re.sub(r'"[^"]*"', "", s)

        # ko'p qatorli for to'plami: for %%f in ( ... ) do (
        if for_set:
            if re.match(r"^\)\s+do\s+\($", s_t, re.I):
                for_set = False
                chuqur += 1
            continue
        if re.match(r"^for\s+%%\w+\s+in\s+\($", s_t, re.I):
            for_set = True
            continue

        # blok yopuvchi: `)` yoki `) else (`
        if re.match(r"^\)(\s*(else|do|then)\s*\()?$", s_t):
            yop = s_q.count(")")
            och = s_q.count("(")
            chuqur += och - yop
            if chuqur < 0:
                xatolar.append(f"satr {i + 1}: ortiqcha `)` — ochilmagan blok yopilgan")
                chuqur = 0
            continue

        # bitta qatorli for: for %%f in (a b c) do (
        if re.match(r"^for\s+%%\w+\s+in\s+\([^)]*\)\s+do\s+\($", s_t, re.I):
            chuqur += 1
            continue

        # blok ochuvchi: if ... (  else (  do (  && (  || (
        if re.search(r"(&&|\|\||if\s|else\s|do\s|while\s).*\(\s*$", s_t, re.I):
            oxirgi = s_q.rfind("(")
            oldin = s_q[:oxirgi]
            chuqur += 1 + (oldin.count("(") - oldin.count(")"))
            continue

        # blok ichidagi oddiy satr: `)` `(` dan ko'p bo'lmasin
        if chuqur > 0:
            och = s_q.count("(")
            yop = s_q.count(")")
            if yop > och:
                xatolar.append(f"satr {i + 1}: blok ichida bekorchi `)` "
                               f"(och={och}, yop={yop}) — NAVBATCHI'dagi xato turi")
    if chuqur > 0:
        xatolar.append(f"blok yopilmagan (chuqur={chuqur})")
    return xatolar, ogoh


def main() -> int:
    fayllar = sys.argv[1:] or sorted(glob.glob("*.bat"))
    jami_xato = 0
    for yol in fayllar:
        xatolar, ogoh = tekshir(yol)
        holat = "OK" if not xatolar else f"XATO({len(xatolar)})"
        print(f"{yol:<42} {holat}")
        for x in xatolar:
            print(f"    ! {x}")
        for o in ogoh:
            print(f"    ? {o}")
        jami_xato += len(xatolar)
    print("-" * 52)
    if jami_xato:
        print(f"YAKUN: {jami_xato} xato — tuzatish kerak")
        return 1
    print("YAKUN: barcha .bat fayllar toza")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
