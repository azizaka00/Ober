"""
TO'LIQ OQIM SINOVI — xaridor va sotuvchi birgalikda.

NEGA BU FAYL BOR (2026-08-12)
-----------------------------
Redesign ishlaridan keyin har bir yuklashdan so'ng saytning ENG MUHIM
oqimi buzilmaganini tekshirish kerak: xaridor qidiradi -> so'rov
yuboradi -> sotuvchi javob beradi -> chat ochiladi.

Oldin bu qo'lda bajarilardi va 9 bosqichni qamrab olardi. Endi bu
sinov shu oqimni jonli server API'si orqali o'tkazadi:

    [1] Xaridor qidiradi (indeks ishlayaptimi)
    [2] Sotuvchi ro'yxatdan o'tadi (token oladi)
    [3] Xaridor so'rov yuboradi (mos sotuvchiga tarqatiladi)
    [4] Sotuvchi ochiq so'rovlarni ko'radi
    [5] Sotuvchi javob yozadi (suhbat yaratiladi)
    [6] Xaridor javobni ko'radi
    [7] Chatda xabar almashadi (har ikki tomondan)
    [8] O'z test ma'lumotlarini tozalaydi

MUHIM:
- Sinov server JONLI bo'lishini talab qiladi (http://127.0.0.1:8800).
  Server o'chiganda aniq xato ko'rsatadi, boshqa sinovlarni buzmaydi.
- Yaratilgan test sotuvchi va test so'rov sinov oxirida O'CHIRILADI —
  bazada hech narsa qoldirmaydi (hatto xato bo'lsa ham — `finally`).
- Ikki marta ishga tushirilsa ham xavfsiz: test raqam qayta
  ishlatiladi, eski yozuvlar tozalanadi.
- MAHALLIY ISHLAB CHIQISH BAZASI UCHUN (data/ober.db). Serverda
  ishlatilmaydi — u yerda jonli foydalanuvchi ma'lumotlari bor.
"""
from __future__ import annotations

import json
import sqlite3
import sys
import urllib.parse
import urllib.request
from pathlib import Path

API = "http://127.0.0.1:8800"
BAZA = Path(__file__).resolve().parent.parent / "data" / "ober.db"

# Test identifikatorlari — boshqa hech narsaga tegmaydi.
TEST_ALOQA = "998900000001"     # 'Test Sotuvchi'
TEST_NOM = "Test Sotuvchi"
TEST_MATN = "divan yangi 2 orinli, Toshkent"
TEST_ISM = "Test Xaridor"

_xato = 0


def ok(shart: bool, nom: str, tafsilot: str = "") -> None:
    """Har bosqich natijasini chiqaradi va xatolarni sanaydi."""
    global _xato
    belgi = "OK " if shart else "XATO"
    if not shart:
        _xato += 1
    print(f"  [{belgi}] {nom}" + (f"  ({tafsilot})" if tafsilot else ""))


def get(yol: str) -> dict:
    with urllib.request.urlopen(API + yol, timeout=15) as r:
        return json.loads(r.read().decode())


def post(yol: str, d: dict) -> dict:
    req = urllib.request.Request(
        API + yol, data=json.dumps(d).encode(),
        headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())


def tozala_test_yozuvlari(sorov_ids: list[int], sotuvchi_ids: list[int]) -> None:
    """Sinov yaratgan yozuvlarni bazadan o'chiradi.

    Faqat aniq test belgilari bilan: TEST_ISM + TEST_MATN bo'lgan
    so'rovlar va TEST_ALOQA + TEST_NOM bo'lgan sotuvchilar. Haqiqiy
    foydalanuvchi ma'lumotlariga tegmaydi.
    """
    if not BAZA.exists():
        return
    c = sqlite3.connect(BAZA)
    c.row_factory = sqlite3.Row
    try:
        # Sinov so'rovlari (aniq ikkala belgi birga)
        ids = sorov_ids or [r["id"] for r in c.execute(
            "SELECT id FROM sorovlar WHERE ism=? AND matn=?",
            (TEST_ISM, TEST_MATN))]
        for sid in ids:
            c.execute("DELETE FROM yuborishlar WHERE sorov_id=?", (sid,))
            jav = c.execute("SELECT id FROM javoblar WHERE sorov_id=?",
                            (sid,)).fetchall()
            for j in jav:
                c.execute("DELETE FROM javoblar WHERE id=?", (j["id"],))
            suh = c.execute("SELECT id, javob_id FROM suhbatlar"
                            " WHERE sorov_id=?", (sid,)).fetchall()
            for s in suh:
                c.execute("DELETE FROM xabarlar WHERE suhbat_id=?",
                          (s["id"],))
                if s["javob_id"]:
                    c.execute("DELETE FROM javoblar WHERE id=?",
                              (s["javob_id"],))
                c.execute("DELETE FROM suhbatlar WHERE id=?", (s["id"],))
            c.execute("DELETE FROM sorovlar WHERE id=?", (sid,))
        # Test sotuvchilari (aniq ikkala belgi birga)
        sids = sotuvchi_ids or [r["id"] for r in c.execute(
            "SELECT id FROM sotuvchilar WHERE (aloqa=? OR aloqa=?)"
            " AND nom=?",
            ("+" + TEST_ALOQA, TEST_ALOQA, TEST_NOM))]
        for sid in sids:
            c.execute("DELETE FROM yuborishlar WHERE sotuvchi_id=?", (sid,))
            c.execute("DELETE FROM suhbatlar WHERE sotuvchi_id=?", (sid,))
            c.execute("DELETE FROM sotuvchilar WHERE id=?", (sid,))
        c.commit()
    finally:
        c.close()


def main() -> None:
    print("=" * 60)
    print("  OBER - TO'LIQ OQIM SINOVI (xaridor + sotuvchi)")
    print("=" * 60)
    print()

    # Xoh oqim tugasin, xoh xato chiqsin — test yozuvlari albatta
    # tozalanadi. Ilgari tozalash faqat [8]-bosqichda edi: skript
    # o'rtasida yiqilsa, bazada test so'rov qolib ketardi.
    sorov_id = None
    sotuvchi_id = None

    # ── [1] XARIDOR QIDIRUVI ────────────────────────────────────────
    print("[1] Xaridor qidiradi")
    try:
        q = get("/api/qidir?q=" + urllib.parse.quote("divan yangi"))
        ok(q.get("jami", 0) > 0, "indeks natija qaytardi",
           f"jami={q.get('jami')}")
    except Exception as e:
        ok(False, "indeks ishlayapti", f"{e}")
        print()
        print(f"  DIQQAT: server {API} da ishlamayapti yoki qidiruv buzilgan.")
        print("  `python server.py` ishga tushirib qayta urinib ko'ring.")
        sys.exit(1)

    # ── [2] SOTUVCHI RO'YXATDAN O'TADI ──────────────────────────────
    print("[2] Sotuvchi ro'yxatdan o'tadi")
    sotuvchi_token = None
    sotuvchi_id = None
    try:
        d = post("/api/sotuvchi/royxat", {"nom": TEST_NOM, "aloqa": TEST_ALOQA,
                                          "nima": "divanlar sotaman",
                                          "tuman": "Toshkent"})
        ok(d.get("ok"), "token olindi")
        sotuvchi_token = d.get("token")
        sotuvchi_id = d.get("id")
    except Exception as e:
        ok(False, "ro'yxatdan o'tish", f"{e}")

    # ── [3] XARIDOR SO'ROV YUBORADI ─────────────────────────────────
    print("[3] Xaridor so'rov yuboradi")
    sorov_token = None
    sorov_id = None
    try:
        d = post("/api/sorov", {"matn": TEST_MATN, "tuman": "Toshkent",
                                "ism": TEST_ISM})
        sorov_token = d.get("token")
        sorov_id = d.get("id")
        ok(d.get("ok") and d.get("yuborildi", 0) > 0,
           "so'rov mos sotuvchilarga tarqatildi", f"yuborildi={d.get('yuborildi')}")
    except Exception as e:
        ok(False, "so'rov yuborish", f"{e}")

    # ── [4] SOTUVCHI OCHIQ SO'ROVNILARNI KO'RADI ────────────────────
    print("[4] Sotuvchi ochiq so'rovlarni ko'radi")
    try:
        d = get(f"/api/sotuvchi/sorovlar?id={sotuvchi_token}")
        royxat = d if isinstance(d, list) else d.get("sorovlar", [])
        ko_rdi = any(s.get("id") == sorov_id or s.get("sorov_id") == sorov_id
                     for s in royxat)
        ok(ko_rdi, "yangi so'rov sotuvchiga ko'rindi", f"jami={len(royxat)}")
    except Exception as e:
        ok(False, "sotuvchi so'rovlari", f"{e}")

    # ── [5] SOTUVCHI JAVOB YOZADI ───────────────────────────────────
    print("[5] Sotuvchi javob yozadi (suhbat yaratiladi)")
    suhbat_id = None
    try:
        d = post("/api/sotuvchi/javob", {"sorov_id": sorov_id, "holat": "bor",
                                         "narx": 1500000,
                                         "izoh": "Divan bor, yangi.",
                                         "sotuvchi_id": sotuvchi_token})
        suhbat_id = d.get("suhbat_id")
        ok(d.get("ok") and suhbat_id, "javob qabul qilindi, suhbat ochildi",
           f"suhbat_id={suhbat_id}")
    except Exception as e:
        ok(False, "javob yozish", f"{e}")

    # ── [6] XARIDOR JAVOBNI KO'RADI ─────────────────────────────────
    print("[6] Xaridor javobni ko'radi")
    try:
        d = get(f"/api/sorov/javoblar?id={sorov_token}")
        javoblar = d.get("javoblar", [])
        ok(len(javoblar) >= 1, "taklif xaridorga ko'rindi",
           f"{len(javoblar)} ta")
    except Exception as e:
        ok(False, "xaridor javoblari", f"{e}")

    # ── [7] CHAT XABAR ALMASHISH ────────────────────────────────────
    print("[7] Chatda xabar almashish")
    try:
        d = post("/api/suhbat/xabar", {"suhbat_id": suhbat_id,
                                       "matn": "Salom, divan bor",
                                       "rol": "sotuvchi",
                                       "actor_id": sotuvchi_token})
        ok(d.get("ok"), "sotuvchi xabar yozdi")
        d = post("/api/suhbat/xabar", {"suhbat_id": suhbat_id,
                                       "matn": "Qabul qilaman",
                                       "rol": "xaridor",
                                       "actor_id": sorov_token})
        ok(d.get("ok"), "xaridor xabar yozdi")
        d = get(f"/api/suhbat?id={suhbat_id}&rol=sotuvchi"
                f"&actor={sotuvchi_token}")
        xabarlar = d.get("xabarlar", []) if isinstance(d, dict) else []
        ok(len(xabarlar) >= 2, "suhbat tarixi har ikki xabarni ko'rsatdi",
           f"{len(xabarlar)} ta")
    except Exception as e:
        ok(False, "chat xabarlari", f"{e}")

    # ── [8] TOZALASH (always-finally) ──────────────────────────────
    print("[8] Test ma'lumotlarini tozalash")
    try:
        tozala_test_yozuvlari([sorov_id], [sotuvchi_id])
        qolgan = 0
        if BAZA.exists():
            c = sqlite3.connect(BAZA)
            try:
                qolgan = c.execute(
                    "SELECT COUNT(*) FROM sorovlar WHERE ism=? AND matn=?",
                    (TEST_ISM, TEST_MATN)).fetchone()[0]
            finally:
                c.close()
        ok(qolgan == 0, "test so'rovlar bazadan o'chirildi")
    except Exception as e:
        ok(False, "tozalash", f"{e}")

    # ── YAKUN ───────────────────────────────────────────────────────
    print()
    print("-" * 60)
    if _xato == 0:
        print("  NATIJA: hammasi yashil")
        sys.exit(0)
    print(f"  NATIJA: {_xato} ta xato")
    sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    finally:
        # Kutilmagan xatoda ham test yozuvlari tozalanadi — oqim
        # o'rtasida yiqilsa, bazada test so'rov qolib ketmaydi.
        # Bo'sh ro'yxat: funksiya belgilarga qarab o'zi qidiradi.
        try:
            tozala_test_yozuvlari([], [])
        except Exception:
            pass
