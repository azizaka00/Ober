"""
OBER — OLX 2-BOSQICH: e'lon sahifasi

Ro'yxat sahifasida yo'q, faqat e'lon sahifasida bor ma'lumot:
  - TELEFON        (sotuvchi nomi sifatida ochiq turadi)
  - RASMLAR        (to'liq o'lchamda, JSON ichida — ro'yxatda lazy-load bo'lgani
                    uchun ko'pchiligi ko'rinmaydi)
  - "Бизнес"       (do'konmi yoki shaxsmi)
  - Qism turi      ("Вид запчасти: Тормозная система")
  - Tavsif         (mahsulot kodi shu yerda bo'ladi)
  - Sotuvchi profili (uning butun assortimenti)

Zond topilmasi (2026-07-30): sahifada JSON blok bor, lekin ikki marta
qochirilgan holda (\\" va \\u002F). Shuning uchun aniq maydonlarni
maqsadli regex bilan olamiz — bu butun blokni JSON deb o'qishdan barqarorroq.
"""

from __future__ import annotations

import html as _html
import re
import time

import baza
from olx import MANBA, _matn, yukla

KUTISH = 3.0                       # e'lon sahifalari orasida — sekinroq, hurmat bilan


def _unesc(s: str) -> str:
    """\\u002F -> /  va boshqa qochirishlarni ochadi."""
    return (s.replace("\\u002F", "/").replace("\\/", "/")
             .replace('\\"', '"').replace("\\\\", "\\"))


def sahifani_oqi(html: str) -> dict:
    d: dict = {}

    # ── Sotuvchi nomi. BA'ZI sotuvchilarda u telefon raqamining o'zi bo'ladi
    #    (2026-07-30 tekshiruvi: bu UMUMIY QOIDA EMAS — ko'pchilik do'kon nomini
    #    qo'yadi). Shuning uchun nomni doim saqlaymiz, raqam bo'lsa telefon deb
    #    belgilaymiz.
    m = re.search(r'data-testid="user-profile-user-name"[^>]*>(.*?)</h\d>', html, re.S)
    if m:
        nom = _matn(m.group(1))
        d["sotuvchi_nomi"] = nom
        raqam = re.sub(r"[^\d]", "", nom)
        if len(raqam) >= 9 and len(re.sub(r"[\d\s+()-]", "", nom)) == 0:
            d["telefon"] = raqam

    # ── Sotuvchi profili (uning barcha e'lonlari)
    m = re.search(r'href="/list/user/([A-Za-z0-9]+)/?"', html)
    if m:
        d["sotuvchi_id"] = m.group(1)

    # ── Biznes (do'kon)
    m = re.search(r'\\"isBusiness\\":\s*(true|false)', html)
    if m:
        d["biznes"] = 1 if m.group(1) == "true" else 0

    # ── Rasmlar. JSON ichida URL'lar qochirilgan holda: https:\u002F\u002F...
    #    XATO EDI: oldingi regex teskari chiziqni rad qilardi va hech narsa
    #    topmasdi. Endi qochirilgan matnni to'liq olib, keyin ochamiz.
    rasmlar: list[str] = []
    m = re.search(r'photos\\?":\s*\[(.*?)\]', html, re.S)
    if m:
        for xom in re.findall(r'https:(?:\\u002F|\\?/|[^"\\,\]])+', m.group(1)):
            u = _unesc(xom).rstrip('\\"')
            if u.startswith("https://") and len(u) > 20:
                rasmlar.append(u)
    if not rasmlar:                       # zaxira: oddiy HTML'dagi rasmlar
        rasmlar = re.findall(
            r'<img[^>]+src="(https://[^"]*apollo\.olxcdn[^"]*)"', html)
    if rasmlar:
        d["rasm"] = rasmlar[0]
        d["rasmlar"] = rasmlar

    # ── Qism turi va holati (HTML matnida ochiq)
    m = re.search(r"Вид запчасти:\s*([^<]+)", html)
    if m:
        d["qism_turi"] = _html.unescape(m.group(1)).strip()
    m = re.search(r"Состояние:\s*([^<]+)", html)
    if m:
        h = _html.unescape(m.group(1)).strip()
        d["holat"] = "yangi" if h.startswith("Нов") else "b_u"

    # ── Tavsif
    m = re.search(r'data-testid="ad_description"[^>]*>(.*?)</div>', html, re.S)
    if m:
        t = _matn(m.group(1))
        # Sarlavha va boshqa bezaklardan tozalash
        d["tavsif"] = t[:2000]

    return d


def kerakli_elonlar(limit: int) -> list[dict]:
    """Hali batafsil o'qilmagan e'lonlar.

    Belgi sifatida `sotuvchi_nomi` ishlatiladi — u har e'londa bo'ladi
    (telefon esa faqat ba'zilarida, shuning uchun belgi bo'la olmaydi)."""
    baza.init()
    with baza.ulan() as c:
        rows = c.execute(
            "SELECT id, tashqi_id, havola FROM elonlar "
            "WHERE manba=? AND (sotuvchi_nomi IS NULL OR sotuvchi_nomi='') "
            "ORDER BY id LIMIT ?", (MANBA, limit)).fetchall()
    return [dict(r) for r in rows]


def yangila(elon_id: int, d: dict) -> None:
    if not d:
        return
    maydonlar, qiymatlar = [], []
    for k in ("telefon", "sotuvchi_id", "sotuvchi_nomi", "biznes", "rasm",
              "qism_turi", "holat", "tavsif"):
        if k in d and d[k] not in (None, ""):
            maydonlar.append(f"{k}=?")
            qiymatlar.append(d[k])
    if d.get("rasmlar"):
        maydonlar.append("rasmlar=?")
        qiymatlar.append("|".join(d["rasmlar"][:10]))
    if not maydonlar:
        return
    qiymatlar.append(elon_id)
    with baza.ulan() as c:
        c.execute(f"UPDATE elonlar SET {', '.join(maydonlar)} WHERE id=?", qiymatlar)


def main(limit: int = 40) -> None:
    print("=" * 62)
    print("  OBER — OLX 2-bosqich: e'lon sahifalari")
    print(f"  (telefon, rasm, qism turi, tavsif, sotuvchi)")
    print("=" * 62)

    ruyxat = kerakli_elonlar(limit)
    if not ruyxat:
        print("\n  Barcha e'lonlar allaqachon o'qilgan.\n")
        return

    print(f"\n  {len(ruyxat)} ta e'lon o'qiladi "
          f"(~{len(ruyxat) * KUTISH / 60:.1f} daqiqa)\n")

    hisob = {"ok": 0, "telefon": 0, "rasm": 0, "biznes": 0, "xato": 0}

    for i, e in enumerate(ruyxat, 1):
        try:
            html = yukla(e["havola"])
            d = sahifani_oqi(html)
            yangila(e["id"], d)
            hisob["ok"] += 1
            if d.get("telefon"):
                hisob["telefon"] += 1
            if d.get("rasm"):
                hisob["rasm"] += 1
            if d.get("biznes"):
                hisob["biznes"] += 1
            belgi = ("T" if d.get("telefon") else "-") + \
                    ("R" if d.get("rasm") else "-") + \
                    ("B" if d.get("biznes") else "-")
            print(f"  [{i}/{len(ruyxat)}] {belgi}  {e['tashqi_id']}")
        except Exception as ex:                              # noqa: BLE001
            hisob["xato"] += 1
            print(f"  [{i}/{len(ruyxat)}] XATO {type(ex).__name__}: {str(ex)[:60]}")
        time.sleep(KUTISH)

    print("\n" + "-" * 62)
    print(f"  O'qildi {hisob['ok']} · telefon {hisob['telefon']} · "
          f"rasm {hisob['rasm']} · do'kon {hisob['biznes']} · xato {hisob['xato']}")
    print("\n  Sifatni ko'rish uchun: KOR.bat\n")


if __name__ == "__main__":
    import sys
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 40)
