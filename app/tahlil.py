"""
OBER — E'LONLARNI OLDINDAN TAHLIL QILISH

Muammo (2026-07-30 vizual sinovda o'lchandi): qidiruv 3-5 soniya davom
etardi, chunki HAR SO'ROVDA 1600+ e'lonning hammasi qayta tahlil qilinardi
(lug'at, imlo, qo'shimchalar).

To'g'ri yo'l: e'lon BIR MARTA tahlil qilinadi, natija bazaga yoziladi.
Keyin qidiruv oddiy filtrga aylanadi — millisoniyalar.

Yangi e'lon qo'shilganda yoki lug'at o'zgarganda qayta yuritiladi.
"""

from __future__ import annotations

import json
import time

import baza
from lugat import modellarni_top, normalla, qismlarni_top


def _xususiyat_qiymatlari(xom: str | None) -> list[str]:
    """`xususiyatlar` JSON'idan qidiriladigan so'zlarni ajratadi.

    OLX har e'longa o'z tavsiflarini qo'yadi: kvartira uchun xona soni
    va qavat, telefon uchun xotira va holat. Ular indeksga tushsa,
    qidiruv har kategoriyada ishlaydi va biz lug'at yozmaymiz.
    """
    if not xom:
        return []
    try:
        royxat = json.loads(xom)
    except (ValueError, TypeError):
        return []
    natija = []
    for x in royxat if isinstance(royxat, list) else []:
        if isinstance(x, dict):
            for kalit in ("n", "q"):          # nom va qiymat
                q = str(x.get(kalit) or "").strip()
                if q and len(q) < 60:
                    natija.append(q)
    return natija


def kesh_belgila() -> None:
    """Qidiruvga yangi tahlil to‘liq tayyor bo‘lganini bildiradi."""
    belgi = baza.DB.with_name("qidiruv-kesh.version")
    belgi.parent.mkdir(parents=True, exist_ok=True)
    belgi.write_text(str(time.time_ns()), encoding="ascii")


def bitta(elon_id: int) -> None:
    """Bitta e'lonni darhol tahlil qiladi — yangi OBER e'loni uchun.

    E'lon joylashtirilgach /api/elon shuni chaqiradi: FTS indeksiga
    darhol qo'shilishi kerak, to'liq tahlil sikli (navbatchi yoki tunlik)
    kutib qolmasin. `main()` dagi bitta qator logikasi — qolgan
    e'lonlarsiz.
    """
    baza.init()
    with baza.ulan() as c:
        r = c.execute(
            "SELECT id, nom, qism_turi, kategoriya, xususiyatlar, tavsif"
            " FROM elonlar WHERE id=?", (elon_id,)).fetchone()
    if not r:
        return
    atamalar = baza.atama_xaritasi()
    matn = f"{r['nom']} {r['qism_turi'] or ''}"
    modellar = sorted(modellarni_top(matn))
    qismlar = sorted(qismlarni_top(matn))
    # FTS indeksi: nom + kategoriya + xususiyatlar + tavsif.
    # OBER e'lonida OLX'ning `xususiyatlar` JSON'i yo'q — tavsif bor.
    # Shuning uchun ularni to'ldiradi (main() OLX uchun xususiyat oladi).
    qoshimcha = [r["kategoriya"] or ""]
    for x in _xususiyat_qiymatlari(r["xususiyatlar"]):
        qoshimcha.append(x)
        juft = atamalar.get(x.lower())
        if juft:
            qoshimcha.append(juft)
    tavsif = (r["tavsif"] or "").strip()
    if tavsif:
        qoshimcha.append(tavsif)
    baza.fts_yoz([(r["id"],
                   normalla(matn + " " + " ".join(qoshimcha)),
                   " ".join(modellar + qismlar))])
    with baza.ulan() as c:
        c.execute(
            "UPDATE elonlar SET tan_modellar=?, tan_qismlar=?,"
            " tan_nom_qismlar=? WHERE id=?",
            (",".join(modellar), ",".join(qismlar),
             ",".join(sorted(qismlarni_top(r["nom"] or ""))), elon_id))


def main(qayta: bool = False) -> None:
    baza.init()
    boshlandi = time.time()

    with baza.ulan() as c:
        if qayta:
            qatorlar = c.execute(
                "SELECT id, nom, qism_turi, kategoriya, xususiyatlar"
                " FROM elonlar WHERE faol=1").fetchall()
        else:
            qatorlar = c.execute(
                "SELECT id, nom, qism_turi, kategoriya, xususiyatlar"
                " FROM elonlar WHERE faol=1 AND (tan_qismlar IS NULL"
                " OR tan_nom_qismlar IS NULL)").fetchall()

    print("=" * 60)
    print("  OBER — e'lonlarni tahlil qilish")
    print("=" * 60)

    if not qatorlar:
        kesh_belgila()
        print("\n  Hammasi allaqachon tahlil qilingan.")
        print("  Lug'at o'zgargan bo'lsa:  python tahlil.py qayta\n")
        return

    print(f"\n  {len(qatorlar)} ta e'lon tahlil qilinadi...\n")

    atamalar = baza.atama_xaritasi()
    if atamalar:
        print(f"  Atama lug'ati: {len(atamalar)} ta so'z (uz <-> ru)\n")

    natijalar = []
    fts = []
    for i, r in enumerate(qatorlar, 1):
        matn = f"{r['nom']} {r['qism_turi'] or ''}"
        modellar = sorted(modellarni_top(matn))
        qismlar = sorted(qismlarni_top(matn))
        # tan_nom_qismlar — FAQAT sarlavhadan. Qidiruv ishonchli va
        # kategoriya orqali kelgan moslikni shu orqali ajratadi.
        natijalar.append((
            ",".join(modellar),
            ",".join(qismlar),
            ",".join(sorted(qismlarni_top(r["nom"] or ""))),
            r["id"]))
        # FTS indeksi: normallashtirilgan matn + teglar.
        # OLX BERGAN TAVSIFLAR ham indeksga kiradi — shu tufayli
        # "2 xonali", "128 gb", "yangi" kabi so'rovlar HAR KATEGORIYADA
        # ishlaydi, lug'at yozmasdan (2026-08-02).
        qoshimcha = [r["kategoriya"] or ""]
        for x in _xususiyat_qiymatlari(r["xususiyatlar"]):
            qoshimcha.append(x)
            # IKKINCHI TIL. "Yangi" indekslansa "Новый" ham indekslanadi —
            # ruscha qidirgan odam ham topadi (Aziz, 2026-08-02).
            juft = atamalar.get(x.lower())
            if juft:
                qoshimcha.append(juft)
        fts.append((r["id"],
                    normalla(matn + " " + " ".join(qoshimcha)),
                    " ".join(modellar + qismlar)))
        if i % 200 == 0:
            print(f"    {i}/{len(qatorlar)}")

    baza.fts_yoz(fts)

    with baza.ulan() as c:
        c.executemany(
            "UPDATE elonlar SET tan_modellar=?, tan_qismlar=?,"
            " tan_nom_qismlar=? WHERE id=?",
            natijalar)
    kesh_belgila()

    vaqt = time.time() - boshlandi
    with baza.ulan() as c:
        bilan = c.execute("SELECT COUNT(*) n FROM elonlar "
                          "WHERE faol=1 AND tan_qismlar <> ''").fetchone()["n"]
        jami = c.execute("SELECT COUNT(*) n FROM elonlar WHERE faol=1").fetchone()["n"]

    print(f"\n  Tayyor — {vaqt:.1f} soniya")
    print(f"  Qism turi aniqlangan: {bilan}/{jami} "
          f"({bilan * 100 // max(jami, 1)}%)")
    print("\n  Endi qidiruv tez ishlaydi.\n")


if __name__ == "__main__":
    import sys
    main(qayta="qayta" in sys.argv)
