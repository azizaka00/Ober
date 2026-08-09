"""
OBER — BAZANI KO'RISH

Yig'ilgan ma'lumot sifatini tekshiradi: parser to'g'ri ishladimi,
narxlar mantiqiymi, tuman ajralganmi, spam bormi.
"""

from __future__ import annotations

import statistics

import baza

# Natija ekranga ham, faylga ham yoziladi — shunda Claude o'zi o'qiy oladi
HISOBOT = baza.BASE / "data" / "hisobot.txt"
_satrlar: list[str] = []


def qator(s: str = "") -> None:
    print(s)
    _satrlar.append(s)


def main() -> None:
    baza.init()
    with baza.ulan() as c:
        hammasi = c.execute("SELECT COUNT(*) n FROM elonlar").fetchone()["n"]
        jami = c.execute("SELECT COUNT(*) n FROM elonlar WHERE faol=1").fetchone()["n"]
        nofaol = hammasi - jami
        if not jami:
            qator("Baza bo'sh. Avval YIG-OLX.bat ni yuriting.")
            return

        qator("=" * 62)
        qator(f"  BAZADA {jami} FAOL E'LON · {nofaol} NOFAOL")
        qator("=" * 62)

        # ── Viloyatlar
        qator("\n  VILOYATLAR")
        for r in c.execute("SELECT viloyat, COUNT(*) n FROM elonlar WHERE faol=1 "
                           "GROUP BY viloyat ORDER BY n DESC"):
            qator(f"    {str(r['viloyat'] or '(bo`sh)'):24} {r['n']:5}")

        # ── Tumanlar (Toshkent)
        qator("\n  TUMANLAR (eng ko'p 10 ta)")
        for r in c.execute("SELECT tuman, COUNT(*) n FROM elonlar "
                           "WHERE faol=1 AND tuman <> '' GROUP BY tuman "
                           "ORDER BY n DESC LIMIT 10"):
            qator(f"    {r['tuman']:28} {r['n']:5}")

        # ── 1-bosqich sifati (ro'yxat sahifasidan)
        qator("\n  1-BOSQICH (ro'yxat sahifasi)")
        nrx = c.execute("SELECT COUNT(*) n FROM elonlar "
                        "WHERE faol=1 AND narx_som IS NOT NULL AND narx_som > 0").fetchone()["n"]
        tmn = c.execute("SELECT COUNT(*) n FROM elonlar WHERE faol=1 AND tuman <> ''").fetchone()["n"]
        hlt = c.execute("SELECT COUNT(*) n FROM elonlar WHERE faol=1 AND holat <> ''").fetchone()["n"]
        for nom, n in (("narxi bor", nrx), ("tumani bor", tmn), ("holati bor", hlt)):
            qator(f"    {nom:16} {n:5}  ({n * 100 // jami}%)")

        # ── 2-bosqich sifati (e'lon sahifasidan)
        qator("\n  2-BOSQICH (e'lon sahifasi)")
        tel = c.execute("SELECT COUNT(*) n FROM elonlar "
                        "WHERE faol=1 AND telefon IS NOT NULL AND telefon <> ''").fetchone()["n"]
        rsm = c.execute("SELECT COUNT(*) n FROM elonlar "
                        "WHERE faol=1 AND rasm IS NOT NULL AND rasm <> ''").fetchone()["n"]
        biz = c.execute("SELECT COUNT(*) n FROM elonlar WHERE faol=1 AND biznes=1").fetchone()["n"]
        qsm = c.execute("SELECT COUNT(*) n FROM elonlar "
                        "WHERE faol=1 AND qism_turi IS NOT NULL AND qism_turi <> ''").fetchone()["n"]
        tvs = c.execute("SELECT COUNT(*) n FROM elonlar "
                        "WHERE faol=1 AND tavsif IS NOT NULL AND tavsif <> ''").fetchone()["n"]
        sot = c.execute("SELECT COUNT(*) n FROM elonlar "
                        "WHERE faol=1 AND sotuvchi_id IS NOT NULL AND sotuvchi_id <> ''").fetchone()["n"]
        oqildi = c.execute("SELECT COUNT(*) n FROM elonlar "
                           "WHERE faol=1 AND sotuvchi_nomi IS NOT NULL "
                           "AND sotuvchi_nomi <> ''").fetchone()["n"]
        for nom, n in (("o'qilgan", oqildi), ("telefon", tel), ("rasm", rsm),
                       ("do'kon (biznes)", biz), ("qism turi", qsm),
                       ("tavsif", tvs), ("sotuvchi id", sot)):
            qator(f"    {nom:16} {n:5}  ({n * 100 // jami}%)")

        if oqildi:
            qator(f"\n    O'QILGANLAR ICHIDA: telefon {tel}/{oqildi} "
                  f"({tel * 100 // oqildi}%) · rasm {rsm * 100 // max(oqildi,1)}%")
            qator("\n    NAMUNA:")
            for r in c.execute(
                    "SELECT nom, sotuvchi_nomi, telefon, biznes, qism_turi, rasm "
                    "FROM elonlar WHERE faol=1 AND sotuvchi_nomi <> '' LIMIT 6"):
                qator(f"      {(r['sotuvchi_nomi'] or '')[:18]:20} "
                      f"tel:{r['telefon'] or '-':13} "
                      f"{'DO`KON' if r['biznes'] else 'shaxs '} "
                      f"{'RASM' if r['rasm'] else '----'}  "
                      f"{(r['qism_turi'] or '-')[:20]}")
        else:
            qator("    ! 2-bosqich hali ishlamagan")

        # ── Narx mantiqiymi
        narxlar = [r["narx_som"] for r in c.execute(
            "SELECT narx_som FROM elonlar WHERE faol=1 AND narx_som > 0 ORDER BY narx_som")]
        if narxlar:
            qator("\n  NARX (so'm)")
            qator(f"    eng past    {narxlar[0]:>15,}")
            qator(f"    o'rtacha    {int(statistics.median(narxlar)):>15,}")
            qator(f"    eng yuqori  {narxlar[-1]:>15,}")
            shubha = [n for n in narxlar if n < 5000 or n > 500_000_000]
            if shubha:
                qator(f"    ! shubhali  {len(shubha)} ta (juda past yoki yuqori)")

        # ── Valyuta
        qator("\n  VALYUTA")
        for r in c.execute("SELECT valyuta, COUNT(*) n FROM elonlar WHERE faol=1 "
                           "GROUP BY valyuta ORDER BY n DESC"):
            qator(f"    {str(r['valyuta'] or '(yo`q)'):8} {r['n']:5}")

        # ── Takroriy spam belgisi
        qator("\n  TAKRORIY SARLAVHA (spam belgisi)")
        takror = c.execute(
            "SELECT nom, COUNT(*) n FROM elonlar WHERE faol=1 GROUP BY nom "
            "HAVING n > 2 ORDER BY n DESC LIMIT 5").fetchall()
        if takror:
            for r in takror:
                qator(f"    {r['n']:3}x  {r['nom'][:52]}")
        else:
            qator("    yo'q")

        # ── Namunalar
        qator("\n  NAMUNA (10 ta tasodifiy)")
        qator("  " + "-" * 60)
        for r in c.execute("SELECT nom, narx_asl, holat, viloyat, tuman, sana "
                           "FROM elonlar WHERE faol=1 ORDER BY RANDOM() LIMIT 10"):
            joy = r["tuman"] or r["viloyat"] or "?"
            qator(f"    {r['nom'][:44]}")
            qator(f"      {r['narx_asl'] or '(narx yo`q)':<22} "
                  f"{r['holat'] or '?':<6} {joy[:20]:<20} {r['sana'] or ''}")

    qator("\n" + "=" * 62 + "\n")

    HISOBOT.parent.mkdir(parents=True, exist_ok=True)
    HISOBOT.write_text("\n".join(_satrlar), encoding="utf-8")
    print(f"  Hisobot saqlandi: {HISOBOT}")


if __name__ == "__main__":
    main()
