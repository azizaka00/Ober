"""OBER — sotuvchi jalb qilish uchun NISHONLI ro'yxat.

MUAMMO (2026-08-15 o'lchovi)
----------------------------
    so'rovlar   60    javob olgan 21 (35%)
    sotuvchilar 14    Telegramga ulangan 8

39 ta xaridor so'radi va jimlik eshitdi. Sabab dizaynda emas:
o'sha toifada OBER'da sotuvchi yo'q.

NEGA BU VOSITA "HAMMAGA XABAR YUBORISH" EMAS
--------------------------------------------
Uch sabab, va ular tartib bilan:

  1. Texnik jihatdan MUMKIN EMAS. O'lchov: 126 873 e'londan
     birortasida ham telefon yo'q — OLX raqamni sahifada ochiq
     bermaydi. Ularni majburan yig'ish boshqa toifadagi ish va
     biz uni qilmaymiz.
  2. Bu spam bo'lardi. Ruxsatsiz ommaviy xabar huquqiy xavf
     tug'diradi.
  3. U baribir ishlamaydi. "Bizda ro'yxatdan o'ting" degan xabar
     mingtadan bittasiga javob oladi, brend esa bir marta kuyadi.

Bark va IndiaMART boshqa yo'l tutadi va u ishlaydi: sotuvchiga
TAKLIF emas, TAYYOR MIJOZ ko'rsatiladi. "Sizning sohangizda
3 ta xaridor javob kutmoqda" — bu reklama emas, ish.

Shu vosita aynan shuni tayyorlaydi: har javobsiz so'rov uchun
indeksdagi MOS sotuvchilarni topadi. Xabarni Aziz o'zi, qo'lda,
kam sonli odamga yozadi.

VOSITA HECH KIMGA HECH NARSA YUBORMAYDI. U faqat ro'yxat chiqaradi.

Ishlatish:
    python3 app/jalb.py            # ekranga
    python3 app/jalb.py --fayl     # data/jalb-nishon.txt ga
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import baza  # noqa: E402
import qidiruv  # noqa: E402

ILDIZ = Path(__file__).resolve().parent.parent
CHIQISH = ILDIZ / "data" / "jalb-nishon.txt"

# Bitta so'rov uchun nechta nomzod. Ko'p bo'lsa ro'yxat o'qilmaydi
# va qo'lda ishlash imkonsiz bo'ladi — maqsad aynan qo'lda ishlash.
NOMZOD = 5


def javobsiz_sorovlar(kun: int = 14) -> list[dict]:
    """Javob olmagan so'rovlar — eng yangisi birinchi."""
    import time
    chegara = time.time() - kun * 86400
    with baza.ulan() as c:
        return [dict(r) for r in c.execute(
            "SELECT s.id, s.matn, s.tuman, s.yonalishlar, s.yaratildi"
            "  FROM sorovlar s"
            " WHERE s.yaratildi > ?"
            "   AND LENGTH(TRIM(s.matn)) > 4"
            "   AND NOT EXISTS (SELECT 1 FROM javoblar j"
            "                    WHERE j.sorov_id = s.id AND j.holat <> 'yoq')"
            " ORDER BY s.yaratildi DESC", (chegara,))]


def nomzodlar(sorov: dict, n: int = NOMZOD) -> list[dict]:
    """So'rov matniga mos e'lonlar va ularning sotuvchilari.

    Indeksning o'zi qidiruv vositasi — alohida lug'at kerak emas
    (loyihaning asosiy qoidasi). `qidir` matnni o'zi tushunadi.

    TELEFON YO'Q — VA BU TO'G'RI (2026-08-15 o'lchovi).

    Dastlab bu funksiya `telefon` maydoni bo'yicha ishlagan edi.
    O'lchov ko'rsatdi: 126 873 e'londan BIRORTASIDA ham telefon
    yo'q. OLX raqamni sahifada ochiq bermaydi ("Ko'rsatish" tugmasi
    ortida), yig'uvchimiz esa uni olmaydi.

    Bu kamchilik emas, qaror: raqamlarni majburan yig'ish —
    boshqa toifadagi ish va biz uni qilmaymiz.

    Shuning uchun vosita HAVOLA beradi. Aziz e'lonni ochadi,
    sotuvchi bilan o'sha yerda — OLX'ning o'z vositasi orqali —
    bog'lanadi. Bu sekinroq, lekin bittalab va nishonli, ya'ni
    aynan kerak bo'lgan usul.
    """
    try:
        natija = qidiruv.qidir(sorov["matn"], limit=60)
    except Exception as e:                     # noqa: BLE001
        print(f"  [jalb] qidiruv xatosi ({sorov['id']}): "
              f"{type(e).__name__}: {e}", file=sys.stderr)
        return []
    # `qidir()` lug'at qaytaradi, e'lonlar `natijalar` kalitida.
    # (2026-08-15: avval `elonlar` deb yozgandim va satrlar ustida
    #  `.get()` chaqirilib xato bergan edi.)
    elonlar = natija.get("natijalar") if isinstance(natija, dict) else natija
    if not isinstance(elonlar, list):
        return []

    # Bitta sotuvchining o'nta e'loni chiqmasin — nomi bo'yicha
    # noyoblik. Nomi yo'q bo'lsa havola bo'yicha.
    korilgan: set[str] = set()
    chiqdi: list[dict] = []
    for e in elonlar or []:
        havola = (e.get("havola") or "").strip()
        if not havola:
            continue
        nom = (e.get("sotuvchi_nomi") or "").strip()
        kalit = nom.lower() or havola
        if kalit in korilgan:
            continue
        korilgan.add(kalit)
        chiqdi.append({
            "nom": nom or "—",
            "joy": (e.get("joy_nom") or e.get("shahar") or "").strip(),
            "elon": (e.get("nom") or "")[:46],
            "havola": havola,
        })
        if len(chiqdi) >= n:
            break
    return chiqdi


def main() -> int:
    faylga = "--fayl" in sys.argv
    satrlar: list[str] = []

    def yoz(s: str = "") -> None:
        satrlar.append(s)
        if not faylga:
            print(s)

    sorovlar = javobsiz_sorovlar()
    yoz("OBER — JAVOBSIZ SO'ROVLAR VA MOS SOTUVCHILAR")
    yoz("=" * 64)
    yoz(f"Javobsiz so'rov: {len(sorovlar)} ta (oxirgi 14 kun)")
    yoz()
    yoz("Har so'rov ostida — indeksda o'sha narsani sotayotgan odamlar.")
    yoz("Ularga YOZILADIGAN gap taklif emas, ish bo'lsin:")
    yoz('  "Sizning sohangizda OBER\'da xaridor javob kutmoqda:')
    yoz('   <so\'rov matni>. Javob berasizmi?"')
    yoz()
    yoz("BU VOSITA HECH KIMGA XABAR YUBORMAYDI. Qo'lda yoziladi.")
    yoz("=" * 64)

    jami_nomzod = 0
    sotuvchi_sorovlari: dict[str, list[str]] = defaultdict(list)

    for s in sorovlar:
        n = nomzodlar(s)
        yoz()
        yoz(f"[{s['id']}] {s['matn'][:60]}"
            + (f"   ({s['tuman']})" if s.get("tuman") else ""))
        if not n:
            yoz("     mos e'lon topilmadi — indeksda bu toifa yo'q")
            continue
        for k in n:
            jami_nomzod += 1
            if k["nom"] != "—":
                sotuvchi_sorovlari[k["nom"]].append(str(s["id"]))
            joy = f" · {k['joy']}" if k["joy"] else ""
            yoz(f"     {k['nom'][:24]:<24}{joy}")
            yoz(f"       {k['elon']}")
            yoz(f"       {k['havola']}")

    yoz()
    yoz("=" * 64)
    yoz(f"Jami nomzod: {jami_nomzod} ta, noyob sotuvchi: {len(sotuvchi_sorovlari)} ta")

    # BIR NECHTA SO'ROVGA MOS KELADIGANLAR — eng qimmatli nomzodlar.
    # Ular bitta emas, bir nechta tayyor mijoz ko'radi, ya'ni
    # OBER'ning foydasi ular uchun darhol ko'rinadi.
    kop = sorted(((t, s) for t, s in sotuvchi_sorovlari.items() if len(s) > 1),
                 key=lambda x: -len(x[1]))
    if kop:
        yoz()
        yoz("BIRINCHI NAVBATDA SHULARGA — bir nechta xaridor kutmoqda:")
        for nom, sids in kop[:15]:
            yoz(f"  {nom[:28]:<28} {len(sids)} ta so'rov (#{', #'.join(sids[:6])})")

    if faylga:
        CHIQISH.parent.mkdir(parents=True, exist_ok=True)
        CHIQISH.write_text("\n".join(satrlar) + "\n", encoding="utf-8")
        print(f"Yozildi: {CHIQISH}")
        print(f"So'rov {len(sorovlar)} ta, nomzod {jami_nomzod} ta.")
        print("DIQQAT: faylda sotuvchi nomlari bor — git'ga tushmaydi.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
