"""
OBER — TALAB HISOBOTI

Qidiruvlar va so'rovlardan nima o'rganilganini ko'rsatadi.

Bu shunchaki statistika emas — sotuvchini olib keladigan DALIL:
  "Sergelida sizning tovaringizni oyiga 47 marta qidirishdi.
   Ularning hech biri sizga yetib bormadi."

Va bir vaqtda:
  - lug'atdagi bo'shliq (nima qidirilyapti-yu topilmayapti)
  - qaysi kategoriyani keyin ochish kerak
  - qaysi tumanda talab ko'p
"""

from __future__ import annotations

import time

import baza

HISOBOT = baza.BASE / "data" / "talab.txt"
_s: list[str] = []


def q(x: str = "") -> None:
    print(x)
    _s.append(x)


def main() -> None:
    baza.init()
    with baza.ulan() as c:
        jami = c.execute("SELECT COUNT(*) n FROM qidiruvlar").fetchone()["n"]

        q("=" * 66)
        q("  OBER — TALAB HISOBOTI")
        q("=" * 66)

        if not jami:
            q("\n  Hali qidiruv yo'q. KOR-BRAUZERDA.bat ni ochib bir necha")
            q("  marta qidiring — keyin bu hisobot ma'noga ega bo'ladi.\n")
            _saqla()
            return

        q(f"\n  Jami {jami} ta qidiruv\n")

        # ── Eng ko'p qidirilgan qism turlari
        q("  ENG KO'P QIDIRILGAN QISMLAR")
        for r in c.execute(
                "SELECT qismlar, COUNT(*) n FROM qidiruvlar "
                "WHERE qismlar <> '' GROUP BY qismlar ORDER BY n DESC LIMIT 12"):
            q(f"    {r['qismlar']:26} {r['n']:4}")

        # ── Eng ko'p qidirilgan modellar
        q("\n  ENG KO'P QIDIRILGAN MASHINALAR")
        for r in c.execute(
                "SELECT modellar, COUNT(*) n FROM qidiruvlar "
                "WHERE modellar <> '' GROUP BY modellar ORDER BY n DESC LIMIT 12"):
            q(f"    {r['modellar']:26} {r['n']:4}")

        # ── Javobsiz qolgan qidiruvlar — ENG QIMMATLI RO'YXAT
        q("\n  JAVOBSIZ QOLGAN QIDIRUVLAR  (talab bor, taklif yo'q)")
        q("  Bu — bozordagi bo'shliq. Sotuvchi topilsa, darhol pul.")
        bosh = c.execute(
            "SELECT sorov, tuman, COUNT(*) n FROM qidiruvlar "
            "WHERE natija_soni = 0 GROUP BY sorov ORDER BY n DESC LIMIT 15"
        ).fetchall()
        if bosh:
            for r in bosh:
                joy = f" [{r['tuman']}]" if r["tuman"] else ""
                q(f"    {r['n']:3}x  {r['sorov'][:40]}{joy}")
        else:
            q("    yo'q — har qidiruvga javob topildi")

        # ── Tumanlar kesimida
        q("\n  QAYERDAN QIDIRILYAPTI")
        for r in c.execute(
                "SELECT tuman, COUNT(*) n FROM qidiruvlar "
                "WHERE tuman <> '' GROUP BY tuman ORDER BY n DESC LIMIT 10"):
            q(f"    {r['tuman']:26} {r['n']:4}")

        # ── So'rovlar
        q("\n  QOLDIRILGAN SO'ROVLAR")
        sorovlar = c.execute("SELECT COUNT(*) n FROM sorovlar").fetchone()["n"]
        q(f"    Jami: {sorovlar}")
        if sorovlar:
            for r in c.execute(
                    "SELECT matn, tuman, byudjet, holat, yaratildi "
                    "FROM sorovlar ORDER BY id DESC LIMIT 10"):
                yosh = (time.time() - (r["yaratildi"] or 0)) / 60
                byu = f" · byudjet {r['byudjet']:,}" if r["byudjet"] else ""
                q(f"    [{r['holat']:9}] {r['matn'][:34]:36}"
                  f" {r['tuman'] or '-':14}{byu}  ({yosh:.0f} daq oldin)")

        # ── Sotuvchiga ko'rsatiladigan dalil
        q("\n" + "-" * 66)
        q("  SOTUVCHIGA AYTILADIGAN GAP (shu ma'lumotdan):")
        eng = c.execute(
            "SELECT qismlar, tuman, COUNT(*) n FROM qidiruvlar "
            "WHERE qismlar <> '' GROUP BY qismlar, tuman "
            "ORDER BY n DESC LIMIT 1").fetchone()
        if eng and eng["n"] > 1:
            joy = eng["tuman"] or "O'zbekistonda"
            q(f'\n    "{joy}da «{eng["qismlar"]}» {eng["n"]} marta qidirildi.')
            q('     Ularning hech biri sizga yetib bormadi."')
        else:
            q("\n    (ma'lumot hali kam — bir necha kun ishlatilsin)")

    q("")
    _saqla()


def _saqla() -> None:
    HISOBOT.parent.mkdir(parents=True, exist_ok=True)
    HISOBOT.write_text("\n".join(_s), encoding="utf-8")
    print(f"  Saqlandi: {HISOBOT}\n")


if __name__ == "__main__":
    main()
