"""
OBER — QIDIRUV SINOVI

Haqiqiy so'rovlar bilan sinaydi va natijani faylga yozadi.
Maqsad: qidiruv OLX'dan yaxshiroq ishlayaptimi — ko'z bilan ko'rish.
"""

from __future__ import annotations

import baza
from qidiruv import qidir

# Haqiqiy odam qanday yozsa — shunday. Ataylab tartibsiz.
SOROVLAR = [
    ("neksiya kolodka", ""),
    ("нексия колодка", ""),
    ("kobalt fara", ""),
    ("akumlyator", "Сергелийский"),
    ("матиз бампер", ""),
    ("spark rul", ""),
    ("lasetti amortizator", ""),
    ("chexol", ""),
    ("gazel dvigatel", ""),
    ("byd disk", ""),
]

HISOBOT = baza.BASE / "data" / "qidiruv-sinov.txt"
_s: list[str] = []


def q(x: str = "") -> None:
    print(x)
    _s.append(x)


def som(n) -> str:
    return f"{n:,}".replace(",", " ") if n else "-"


def main() -> None:
    q("=" * 66)
    q("  OBER — QIDIRUV SINOVI")
    q("=" * 66)

    with baza.ulan() as c:
        jami = c.execute("SELECT COUNT(*) n FROM elonlar").fetchone()["n"]
    q(f"\n  Bazada {jami} e'lon\n")

    for sorov, tuman in SOROVLAR:
        r = qidir(sorov, tuman, limit=5)
        q("-" * 66)
        q(f"  SO'ROV: \"{sorov}\"" + (f"   [tuman: {tuman}]" if tuman else ""))

        t = r["tushunildi"]
        q(f"  Tushunildi -> model: {t['modellar'] or '(yo`q)'}   "
          f"qism: {t['qismlar'] or '(yo`q)'}")

        q(f"  Topildi: {r['jami']} ta" +
          (f"   ·  boshqa mashina bo'lgani uchun kesildi: {r['kesildi_model']}"
           if r["kesildi_model"] else ""))

        if r["eng_arzon"]:
            q(f"  Eng arzon haqiqiy taklif: {som(r['eng_arzon'])} so'm")

        if not r["natijalar"]:
            q("  ! natija yo'q")
            q("")
            continue

        q("")
        for i, e in enumerate(r["natijalar"], 1):
            joy = e["tuman"] or e["shahar"] or e["viloyat"] or "?"
            belgi = ("D" if e["biznes"] else " ") + ("R" if e["rasm"] else " ")
            q(f"   {i}. [{e['ball']:5.1f}]{belgi} {e['nom'][:44]}")
            q(f"          {som(e['narx_som']):>12} so'm  ·  {joy[:22]:24}"
              f"  ·  {e['sana'] or ''}")
            # Nima uchun qoldi — xatoni topish uchun
            q(f"          tanildi -> model:{e['_modellar'] or '-'} "
              f"qism:{e['_qismlar'] or '-'}")
        q("")

    HISOBOT.parent.mkdir(parents=True, exist_ok=True)
    HISOBOT.write_text("\n".join(_s), encoding="utf-8")
    q("=" * 66)
    print(f"\n  Saqlandi: {HISOBOT}\n")


if __name__ == "__main__":
    main()
