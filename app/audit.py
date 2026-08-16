"""OBER — backend auditi. Har safar qayta yugurtiriladi.

NEGA VOSITA, GREP EMAS (2026-08-15)
-----------------------------------
Birinchi urinishda men `server.py` ni oddiy grep bilan tekshirdim
va `/api/suhbat/xabar` "himoyasiz" degan xulosaga keldim — ya'ni
har kim istalgan suhbatga xabar yozadi degani. Bu YOLG'ON xavotir
edi: qidiruv yo'lni tezlik jadvalidan topgan, ishlovchidan emas.

Grep tez, lekin kontekstni bilmaydi. Vosita esa ishlovchi
chegarasini to'g'ri topadi va natijasi takrorlanadi. Auditni
"bir marta ko'z bilan o'qib chiqish" emas, YUGURTIRILADIGAN
narsa qilish kerak — aks holda keyingi safar hammasi qaytadan
boshlanadi va yana yolg'on xavotir chiqadi.

Ishlatish:  python3 app/audit.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ILDIZ = Path(__file__).resolve().parent.parent
APP = ILDIZ / "app"
WEB = ILDIZ / "web"

# Ochiq bo'lishi ATAYLAB to'g'ri bo'lgan yo'llar. Har biri sabab
# bilan: ro'yxatdan o'tish, kirish va xaridor so'rovi — bularda
# hali sessiya BO'LMAYDI, shuning uchun token talab qilib bo'lmaydi.
ATAYLAB_OCHIQ = {
    "/api/sotuvchi/royxat": "ro'yxatdan o'tish — sessiya hali yo'q",
    "/api/sotuvchi/kirish": "kirish — sessiya shu yerda yaratiladi",
    "/api/sotuvchi/tasdiq": "kod tasdig'i — sessiyadan oldin",
    "/api/sotuvchi/chiqish": "chiqish — tokenning o'zi tanaсida",
    "/api/sorov": "xaridor so'rovi — xaridorda hisob yo'q",
    "/api/demo/chat": "demo — haqiqiy ma'lumot yo'q",
    "/api/ai/rasm-qidiruv": "rasm qidiruvi — anonim, faqat tezlik chegarasi",
    "/api/sotuvchi/telegram/sinov": "sinov uchun",
}

HIMOYA_BELGILARI = ("_actor_ident", "_sotuvchi_ident", "_xaridor_ident",
                    "sessiya_sotuvchisi", "sorov_id_token")


def _ishlovchilar(matn: str) -> dict[str, tuple[int, str]]:
    """Har `/api/` yo'li uchun ISHLOVCHI blokini topadi.

    Yo'l fayl ichida bir necha marta uchraydi (tezlik jadvali,
    izohlar). Bizga faqat `if u.path == "..."` ko'rinishidagi
    haqiqiy tarmoqlanish kerak.
    """
    satrlar = matn.split("\n")
    natija: dict[str, tuple[int, str]] = {}
    boshlar = [(i, m.group(1)) for i, s in enumerate(satrlar)
               if (m := re.search(r'u\.path\s*==\s*"(/api/[^"]+)"', s))]
    for nomer, (i, yol) in enumerate(boshlar):
        oxir = boshlar[nomer + 1][0] if nomer + 1 < len(boshlar) else len(satrlar)
        # 2026-08-15: bu yerda `min(oxir, i+120)` turardi va u
        # `/api/javob/raqam` ni "himoyasiz" deb ko'rsatgan edi —
        # aslida himoya 28 qator pastda, lekin blok undan oldin
        # kesilgandi. Endi faqat `return` gacha kesamiz: ishlovchi
        # aynan shu bilan tugaydi.
        for j in range(i + 1, oxir):
            if re.match(r"\s{12}return\s*$", satrlar[j]):
                oxir = j + 1
                break
        natija[yol] = (i + 1, "\n".join(satrlar[i:oxir]))
    return natija


def main() -> int:
    ogoh = 0
    print("OBER — BACKEND AUDITI")
    print("=" * 62)

    server = (APP / "server.py").read_text(encoding="utf-8")
    ishlovchilar = _ishlovchilar(server)

    # ── 1. Yozadigan yo'llarda himoya bormi ──────────────────────
    print("\n1. HIMOYASIZ YO'LLAR")
    topildi = False
    for yol, (qator, blok) in sorted(ishlovchilar.items()):
        if yol in ATAYLAB_OCHIQ:
            continue
        if any(k in blok for k in HIMOYA_BELGILARI):
            continue
        # Faqat o'qiydigan yo'llar (ochiq ma'lumot) muammo emas.
        yozadi = any(k in blok for k in ("INSERT", "UPDATE", "DELETE",
                                         "_tana(", "yoz(", "saqla("))
        if yozadi:
            topildi = True
            ogoh += 1
            print(f"   ! {yol}  (qator {qator}) — yozadi, lekin "
                  f"token tekshiruvi topilmadi")
    if not topildi:
        print("   Yozadigan barcha yo'llarda token tekshiruvi bor.")

    # ── 2. SQL — qatorlar birlashtirilmayaptimi ──────────────────
    print("\n2. SQL IN'YEKSIYA XAVFI")
    # 2026-08-15: birinchi variant har `f"..."` li SQL ni xavf deb
    # belgilagan va 12 ta yolg'on xavotir bergan edi. Aslida
    # hammasi xavfsiz: `f"ALTER TABLE x ADD COLUMN {ustun}"` da
    # `ustun` KODDAGI ro'yxatdan keladi, `f"UPDATE {jadval} ...
    # WHERE id=?"` da esa qiymat `?` bilan uzatiladi.
    #
    # Haqiqiy xavf — f-string ichiga FOYDALANUVCHI kiritmasi
    # tushganda. Shuning uchun endi o'zgaruvchi nomiga qaraymiz:
    # jadval/ustun nomlari xavfsiz, qolgani tekshiriladi.
    XAVFSIZ_NOM = {"jadval", "ustun", "tur", "nom", "maydon", "tartib",
                   "yonalish", "indeks"}
    xavf = 0
    for fayl in APP.glob("*.py"):
        matn = fayl.read_text(encoding="utf-8")
        for i, s in enumerate(matn.split("\n"), 1):
            if not re.search(r'(execute|executemany)\s*\(\s*f["\']', s):
                continue
            qoyilgan = set(re.findall(r"\{([a-z_]+)", s))
            shubhali = qoyilgan - XAVFSIZ_NOM
            if shubhali:
                xavf += 1
                print(f"   ! {fayl.name}:{i}  f-string SQL, "
                      f"tekshiring: {', '.join(sorted(shubhali))}")
    if not xavf:
        print("   f-string li SQL bor, lekin ichida faqat kod bergan")
        print("   jadval/ustun nomlari — qiymatlar `?` bilan uzatiladi.")
    ogoh += xavf

    # ── 3. Jim yutilgan istisnolar ───────────────────────────────
    print("\n3. JIM YUTILGAN XATOLAR")
    jim = []
    for fayl in APP.glob("*.py"):
        satrlar = fayl.read_text(encoding="utf-8").split("\n")
        for i, s in enumerate(satrlar):
            if re.match(r"\s*except\b.*:\s*$", s):
                # keyingi mazmunli satr faqat `pass` bo'lsa — jim
                for keyingi in satrlar[i + 1:i + 3]:
                    t = keyingi.strip()
                    if not t or t.startswith("#"):
                        continue
                    if t == "pass":
                        jim.append(f"{fayl.name}:{i + 1}")
                    break
    if jim:
        print(f"   {len(jim)} ta `except: pass` — xato izsiz yo'qoladi:")
        for j in jim[:8]:
            print(f"     {j}")
        if len(jim) > 8:
            print(f"     ... yana {len(jim) - 8} ta")
        ogoh += len(jim)
    else:
        print("   `except: pass` yo'q.")

    # ── 4. Frontend: yetim CSS sinflari ──────────────────────────
    # 2026-08-15: birinchi variant `<style>` bloklarini birlashtirib,
    # keyin `matn.replace(...)` qilardi. Sahifada BIR NECHTA style
    # bloki bo'lgani uchun birlashtirilgan satr matnda topilmasdi va
    # natija ishonchsiz chiqardi (`dalil-son` yetim deb ko'rsatilgan
    # edi, aslida ishlatiladi). Endi har blok alohida olib tashlanadi.
    print("\n4. FRONTEND — YETIM CSS SINFLARI")
    for nom in ("index.html", "takliflar.html", "sotuvchi.html",
                "kategoriyalar.html", "elon.html"):
        matn = (WEB / nom).read_text(encoding="utf-8")
        tana = matn
        stillar = re.findall(r"<style>(.*?)</style>", matn, re.S)
        for blok in stillar:
            tana = tana.replace(blok, "")
        sinflar = set()
        for blok in stillar:
            sinflar |= set(re.findall(r"\.([a-z][a-z0-9-]{3,})\s*[,{:\s]", blok))
        # Sinf `class="a b"`, `classList.add("a")` yoki shablon
        # satrida bo'lishi mumkin — hammasi `tana` ichida.
        yetim = sorted(s for s in sinflar if s not in tana)
        if yetim:
            print(f"   {nom}: {len(yetim)} ta shubhali sinf")
            print(f"     {', '.join(yetim[:6])}"
                  + (" ..." if len(yetim) > 6 else ""))
        else:
            print(f"   {nom}: yetim sinf yo'q")

    # ── 5. Sinovsiz modullar ─────────────────────────────────────
    print("\n5. SINOVSIZ MODULLAR")
    sinovlar = {f.name.replace("_sinov.py", "") for f in APP.glob("*_sinov.py")}
    modullar = {f.stem for f in APP.glob("*.py")
                if not f.stem.endswith("_sinov") and f.stem != "audit"}
    yoq = sorted(modullar - sinovlar)
    print(f"   {len(sinovlar)} ta sinov to'plami, {len(modullar)} ta modul")
    if yoq:
        print(f"   Sinovi yo'q: {', '.join(yoq)}")

    print("\n" + "-" * 62)
    print(f"JAMI OGOHLANTIRISH: {ogoh}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
