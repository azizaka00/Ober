"""`mcp_server` sinovi — jonli bazaga TEGMASDAN, o'z vaqtinchalik bazasida.

ENG MUHIM SINOV: AGENTGA YOLG'ON JAVOB KETMASIN.

Odam "bu men so'raganim emas" deb o'zi filtrlaydi. Agent esa
natijani haqiqiy javob deb foydalanuvchiga uzatadi — shuning uchun
`qidir` ishonchsiz natijani "topildi" deb qaytarmasligi kerak.

Ikkinchi muhim sinov: `sorov_yubor` — yagona YOZADIGAN vosita.
U aloqasiz yozmasin, nusxa yozmasin, chegarasiz spamlamasin.

XAVFSIZLIK
----------
Bu skript `baza.DB` ni vaqtinchalik faylga yo'naltiradi va jonli
`data/ober.db` ga BIR MARTA HAM yozmaydi. Yakunda buni tekshiradi.

`OBER_API` ataylab bo'sh qilinadi — sinov MAHALLIY rejimda yuradi
va ober.uz ga bitta so'rov ham yubormaydi. Aks holda har sinov
jonli sotuvchilarga soxta talab yuborardi.

ISHLATISH
---------
    python app/mcp_sinov.py
"""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

# MAHALLIY REJIM — importdan OLDIN. `mcp_server.API` modul
# yuklanayotganda o'qiladi, keyin o'zgartirsak kech bo'ladi.
os.environ["OBER_API"] = ""

import baza                                             # noqa: E402

# ── JONLI BAZANI HIMOYA QILISH — HAR NARSADAN OLDIN ──────────────────
JONLI = baza.DB
JONLI_HOLAT = (JONLI.stat().st_mtime, JONLI.stat().st_size) \
    if JONLI.exists() else None

VAQTINCHA = Path(tempfile.mkdtemp(prefix="ober-mcp-sinov-"))
baza.DB = VAQTINCHA / "sinov.db"

import mcp_server as ms                                    # noqa: E402
import qidiruv                                             # noqa: E402
import tahlil                                              # noqa: E402
from yonalishlar import belgilar as yonalishlar_belgilar   # noqa: E402

jami = 0
xato = 0


def tekshir(shart: bool, izoh: str) -> None:
    global jami, xato
    jami += 1
    if not shart:
        xato += 1
        print(f"  XATO  {izoh}")


def chaqir(usul: str, params=None, id_=1):
    return ms.ishla({"jsonrpc": "2.0", "id": id_, "method": usul,
                     "params": params or {}})


def vosita(nom: str, arg: dict) -> dict:
    """`tools/call` orqali chaqirib, ichidagi JSON'ni qaytaradi."""
    j = chaqir("tools/call", {"name": nom, "arguments": arg})
    matn = j["result"]["content"][0]["text"]
    return json.loads(matn)


# ── SINOV BAZASI ─────────────────────────────────────────────────────

ELONLAR = [
    # nom, narx, kategoriya
    ("Divan yangi 2 orinli sotiladi", 3_000_000, "Uy va bog' / Mebel"),
    ("Divan burchakli katta", 5_500_000, "Uy va bog' / Mebel"),
    ("Charmhoo cotecho R13 shina", 900_000, "Transport / Shina"),
    ("Nexia kolodka original oldingi", 250_000, "Transport / Ehtiyot qism"),
    ("Velosiped bolalar uchun", 1_200_000, "Sport / Velosiped"),
    ("Muzlatgich Artel yangi", 4_000_000, "Uy va bog' / Texnika"),
    # BU E'LON ATAYLAB SHU YERDA. Jonli indeksda "zzqqxx yoq narsa"
    # so'rovi 181 ta natija bergan edi, chunki "narsa" — haqiqiy
    # o'zbekcha so'z va `fts_erkin` OR bosqichida uni topadi.
    # Shu e'lonsiz "yolg'on so'rov" sinovi bo'sh indeksga urilib
    # o'tib ketardi va hech narsani qo'riqlamasdi.
    ("Ishlab turgan narsa arzon", 100_000, "Uy va bog' / Texnika"),
]


def baza_tayyorla() -> None:
    baza.init()
    for i, (nom, narx, kat) in enumerate(ELONLAR):
        baza.saqla({"manba": "sinov", "tashqi_id": f"s{i}", "nom": nom,
                    "narx_som": narx, "kategoriya": kat,
                    "viloyat": "Toshkent shahri", "shahar": "Toshkent",
                    "tuman": "Chilonzor", "sana": "2026-08-17",
                    "havola": f"https://sinov.uz/{i}"})
    tahlil.main()
    # `_umumiy_soz` ULUSH bo'yicha ishlaydi: 6 e'lonli bazada har so'z
    # "umumiy" bo'lib chiqishi mumkin edi. Jonli indeks hajmi qo'yiladi,
    # shunda sinov jonli holatdagidek yuradi.
    baza._JAMI_KESH[:] = [time.time(), 400_000]
    qidiruv._KESH_VAQT = -1.0


def main() -> int:
    print("\n  MCP SERVER SINOVI\n" + "-" * 52)
    baza_tayyorla()

    # ── 0. MANBA — SINOV JONLI SAYTGA CHIQMASIN ────────────────────
    tekshir(ms.API == "",
            f"sinov mahalliy rejimda yursin ({ms.API!r})")
    # STANDART QIYMAT — SAYT. Ya'ni `OBER_API` ni sozlashni unutish
    # xavfsiz tomonga tushadi: talab haqiqiy sotuvchilarga boradi,
    # eski mahalliy nusxaga emas (2026-08-17 o'lchovi: mahalliy
    # bazada 126 873 e'lon va 13 sotuvchi, saytda 523 000+).
    tekshir(ms.ODATIY_API == "https://ober.uz",
            f"standart manba sayt bo'lsin ({ms.ODATIY_API})")

    # ── 1. PROTOKOL ────────────────────────────────────────────────
    j = chaqir("initialize")
    tekshir(j["result"]["protocolVersion"] == ms.PROTOKOL,
            "initialize: protokol versiyasi")
    tekshir(j["result"]["serverInfo"]["name"] == "ober",
            "initialize: server nomi")
    tekshir(j["jsonrpc"] == "2.0" and j["id"] == 1,
            "initialize: JSON-RPC konverti")

    tekshir(ms.ishla({"jsonrpc": "2.0",
                      "method": "notifications/initialized"}) is None,
            "bildirishnomaga javob qaytmasin (id yo'q)")

    j = chaqir("tools/list")
    nomlar = [t["name"] for t in j["result"]["tools"]]
    tekshir(nomlar == ["qidir", "sorov_yubor", "javoblar"],
            f"tools/list: uchala vosita ({nomlar})")
    tekshir(all("inputSchema" in t and t["inputSchema"].get("required")
                for t in j["result"]["tools"]),
            "har vositada majburiy maydonlar e'lon qilingan")
    tekshir("aloqa" in j["result"]["tools"][1]["inputSchema"]["required"],
            "sorov_yubor: `aloqa` MAJBURIY")

    j = chaqir("yoq/usul")
    tekshir(j.get("error", {}).get("code") == -32601,
            "noma'lum usul -32601 qaytarsin")
    j = chaqir("tools/call", {"name": "yoq_vosita", "arguments": {}})
    tekshir(j.get("error", {}).get("code") == -32601,
            "noma'lum vosita -32601 qaytarsin")

    # ── 2. QIDIR — TOPILADIGAN HOLAT ───────────────────────────────
    r = vosita("qidir", {"sorov": "divan"})
    tekshir(r["holat"] == "topildi", f"«divan» topilsin ({r['holat']})")
    tekshir(r["topildi"] >= 1, "«divan» kamida 1 ta e'lon")
    tekshir(all("divan" in (e["nom"] or "").lower() for e in r["elonlar"]),
            "«divan» natijalarining hammasida divan bo'lsin")
    tekshir(all(e["havola"] for e in r["elonlar"]),
            "HAR natijada havola bo'lsin — havolasiz e'lon foydasiz")

    # ── 3. BO'SH NATIJA MUAMMOSI — ASOSIY SINOV ────────────────────
    #
    # 2026-08-16 o'lchovi: `qidir("zzqqxx yoq narsa")` 10 ta begona
    # e'lon qaytargan edi. Sabab: `fts_erkin` "kamida bitta so'z"
    # (OR) bosqichiga tushadi va "narsa" haqiqiy so'z.
    r = vosita("qidir", {"sorov": "zzqqxx yoq narsa"})
    tekshir(r["topildi"] == 0, "yolg'on so'rov: hech narsa topilmasin")
    tekshir(r["elonlar"] == [], "yolg'on so'rov: `elonlar` BO'SH bo'lsin")
    tekshir(r["holat"] == "aniq_moslik_yoq",
            f"yolg'on so'rov OR bosqichiga tushsin ({r.get('holat')})")
    tekshir(bool(r.get("soralgani_emas")),
            "yolg'on so'rov: OR bosqichi haqiqatan e'lon topgan bo'lsin "
            "— aks holda bu sinov hech narsani qo'riqlamaydi")
    tekshir(r.get("keyingi_qadam") == "sorov_yubor",
            "bo'sh natijada agentga keyingi qadam ko'rsatilsin")

    # ANIQ MOSLIK YO'Q: "divan" bor, "charm divan" yo'q. Indeksda
    # "Charmhoo" (charm PREFIKSI) bor — ilgari u javobga tushardi.
    r = vosita("qidir", {"sorov": "divan charm"})
    tekshir(r["topildi"] == 0,
            f"«divan charm» aniq mos emas — 0 qaytsin ({r['topildi']})")
    tekshir(r["holat"] == "aniq_moslik_yoq",
            f"«divan charm» holati ({r.get('holat')})")
    tekshir(r["elonlar"] == [], "«divan charm»: `elonlar` bo'sh")
    namuna = r.get("soralgani_emas") or []
    tekshir(bool(namuna), "yaqin e'lonlar NOMI ko'rsatilsin (izoh uchun)")
    tekshir(all(isinstance(x, str) for x in namuna),
            "`soralgani_emas` faqat NOM — narx va HAVOLA bo'lmasin")
    tekshir("ogohlantirish" in r,
            "`soralgani_emas` yonida ogohlantirish bo'lsin")

    # LUG'AT TASODIFAN MODEL TANIGAN HOLAT.
    # `qidir("zzz vvv yyy")` jonli bazada 1404 natija qaytargan edi:
    # "vvv" lug'atda `volkswagen`. Mazmunli so'z yo'q -> ishonch yo'q.
    tekshir(ms._ishonchli_natijalar({"sozlar": [], "natijalar": [
        {"_ishonchli": True, "nom": "x"}]}) == [],
        "so'z chiqmagan so'rov ishonchli bo'lmasin (sozlar bo'sh)")
    tekshir(len(ms._ishonchli_natijalar({"sozlar": ["divan"], "natijalar": [
        {"_ishonchli": False}, {"_ishonchli": True}]})) == 1,
        "faqat `_ishonchli` natijalar o'tsin")

    # ── 4. NARX CHEGARASI YOLG'ON GAPIRMASIN ───────────────────────
    r = vosita("qidir", {"sorov": "divan", "narx_max": 1000})
    tekshir(r["topildi"] == 0, "1000 so'mlik divan yo'q")
    tekshir(r["holat"] == "narx_boyicha_yoq",
            f"narx sababi ayrilsin ({r.get('holat')})")
    tekshir(r.get("eng_arzon_som") == 3_000_000,
            f"haqiqiy eng arzon narx aytilsin ({r.get('eng_arzon_som')})")

    r = vosita("qidir", {"sorov": "divan", "narx_max": 4_000_000})
    tekshir(r["holat"] == "topildi", "4 mln gacha divan topilsin")
    tekshir(all(e["narx_som"] <= 4_000_000 for e in r["elonlar"]),
            "narx chegarasi hurmat qilinsin")

    r = vosita("qidir", {"sorov": ""})
    tekshir("xato" in r, "bo'sh so'rov xato qaytarsin")

    # ── 5. SOROV_YUBOR — VALIDATSIYA ───────────────────────────────
    r = vosita("sorov_yubor", {"matn": "charm divan kerak"})
    tekshir("xato" in r, "aloqasiz so'rov yozilmasin")
    tekshir("so'rang" in (r.get("maslahat") or "").lower()
            or "so'rang" in (r.get("xato") or "").lower(),
            "agentga: raqamni FOYDALANUVCHIDAN so'ra")

    r = vosita("sorov_yubor", {"matn": "charm divan", "aloqa": "123"})
    tekshir("xato" in r, "qisqa raqam qabul qilinmasin")

    r = vosita("sorov_yubor", {"matn": "charm divan",
                               "aloqa": "111111111"})
    tekshir("xato" in r, "to'qilgan raqam (111111111) qabul qilinmasin")

    r = vosita("sorov_yubor", {"matn": "a", "aloqa": "998901234567"})
    tekshir("xato" in r, "juda qisqa matn qabul qilinmasin")

    with baza.ulan() as c:
        n = c.execute("SELECT COUNT(*) n FROM sorovlar").fetchone()["n"]
    tekshir(n == 0, f"xato validatsiyalardan keyin baza toza ({n})")

    # ── 6. SOROV_YUBOR — HAQIQIY YOZUV ─────────────────────────────
    r = vosita("sorov_yubor", {
        "matn": "charm divan 3 orinli kerak, 5 mln gacha",
        "aloqa": "+998 90 123 45 67", "tuman": "Chilonzor",
        "ism": "Aziz"})
    tekshir(r.get("ok") is True, f"so'rov yozilsin ({r})")
    sid = r.get("sorov_id")
    tekshir(bool(sid), "sorov_id qaytsin")
    tekshir(r.get("kuzatish", "").startswith("https://ober.uz/takliflar?kalit="),
            "xaridorga kuzatish havolasi berilsin")
    tekshir(len(r.get("kuzatish", "").split("kalit=")[-1]) > 20,
            "kuzatish kaliti taxmin qilib bo'lmaydigan bo'lsin")
    tekshir(r.get("byudjet") == 5_000_000,
            f"byudjet matndan olinsin ({r.get('byudjet')})")
    tekshir(r.get("muddat_soat") == 24, "muddat aytilsin")

    with baza.ulan() as c:
        s = dict(c.execute("SELECT * FROM sorovlar WHERE id=?",
                           (sid,)).fetchone())
    tekshir(s["aloqa"] == "998901234567",
            f"raqam bir xil shaklda saqlansin ({s['aloqa']})")
    tekshir(s["ism"] == "Aziz", "ism saqlansin")
    tekshir(s["tuman"] == "Chilonzor", "joy saqlansin")

    # JAVOBDA SOTUVCHI RAQAMI BO'LMASIN
    matn = json.dumps(r, ensure_ascii=False)
    tekshir("998901234567" not in matn.replace(s["aloqa"], "", 1)
            or matn.count("998901234567") == 0,
            "javobda telefon raqami qaytarilmasin")

    # ── 7. NUSXA YOZILMASIN ────────────────────────────────────────
    r2 = vosita("sorov_yubor", {
        "matn": "charm divan 3 orinli kerak, 5 mln gacha",
        "aloqa": "998901234567"})
    tekshir(r2.get("holat") == "allaqachon_yuborilgan",
            f"aynan shu talab takror yozilmasin ({r2.get('holat')})")
    tekshir(r2.get("sorov_id") == sid, "eski so'rov ID qaytsin")
    with baza.ulan() as c:
        n = c.execute("SELECT COUNT(*) n FROM sorovlar").fetchone()["n"]
    tekshir(n == 1, f"bazada bitta so'rov qolsin ({n})")

    # ── 8. TALAB HAQIQATAN SOTUVCHIGA BORADIMI ─────────────────────
    #
    # OBERning butun nishasi shu zanjirda: agent so'radi -> indeksda
    # yo'q -> talab JONLI SOTUVCHIGA bordi. Zanjir uzilsa vosita
    # ishlayotgandek ko'rinadi, lekin hech kimga yetib bormaydi —
    # 2026-08-01/08-04 da sayt tomonida aynan shunday bo'lgan edi.
    sot = baza.sotuvchi_yoz(
        "Mebel dokoni", "divan, kreslo, mebel sotaman", [], [],
        "Chilonzor", "998911112233",
        sorted(yonalishlar_belgilar("divan, kreslo, mebel sotaman")))
    tekshir(bool(sot), "sinov sotuvchisi yozilsin")

    r = vosita("sorov_yubor", {"matn": "charm divan kerak 3 orinli",
                               "aloqa": "998901239999"})
    tekshir(r.get("yuborildi", 0) >= 1,
            f"talab mos sotuvchiga yetib borsin ({r.get('yuborildi')})")
    tekshir(r.get("holat") == "yuborildi",
            f"holat: yuborildi ({r.get('holat')})")
    with baza.ulan() as c:
        n = c.execute("SELECT COUNT(*) n FROM yuborishlar WHERE sorov_id=?",
                      (r["sorov_id"],)).fetchone()["n"]
    tekshir(n >= 1, f"`yuborishlar` jadvalida yozuv bo'lsin ({n})")

    # O'ZINGGA O'Z SO'ROVING KELMASIN. `baza._mos_sotuvchilar` buni
    # oxirgi 9 raqam bo'yicha qiladi (2026-08-15). Agent raqamni O'ZI
    # beradi — turli shaklda ("+998 91 111 22 33") kelsa ham ishlasin.
    r = vosita("sorov_yubor", {"matn": "yana divan kerak boshqa rangda",
                               "aloqa": "+998 91 111 22 33"})
    tekshir(r.get("yuborildi", 0) == 0,
            f"so'rov egasiga o'z talabi bormasin ({r.get('yuborildi')})")

    # ── 9. TEZLIK CHEKLOVI ─────────────────────────────────────────
    #
    # Sayt tomonidagi soatiga 60 ta chegara HTTP qatlamida (server.py).
    # MCP `baza` ni to'g'ridan chaqiradi — u chegara bu yerda ISHLAMAYDI
    # va qayta qo'yilgan. Shu sinov o'sha qoidani qo'riqlaydi.
    tekshir(ms.YOZISH_SOATIGA <= 60,
            "MCP chegarasi sayt chegarasidan qattiqroq bo'lsin")
    ms._YOZISH_VAQTLARI[:] = [time.time()] * ms.YOZISH_SOATIGA
    r = vosita("sorov_yubor", {"matn": "boshqa narsa kerak endi",
                               "aloqa": "998901234500"})
    tekshir(r.get("holat") == "tezlik_chegarasi",
            f"soatlik chegara ushlasin ({r.get('holat')})")

    ms._YOZISH_VAQTLARI[:] = [time.time()] * ms.YOZISH_DAQIQADA
    r = vosita("sorov_yubor", {"matn": "yana boshqa narsa kerak",
                               "aloqa": "998901234501"})
    tekshir(r.get("holat") == "tezlik_chegarasi",
            f"daqiqalik chegara ushlasin ({r.get('holat')})")

    ms._YOZISH_VAQTLARI[:] = []

    # ── 10. JAVOBLAR — 3-QADAM ─────────────────────────────────────
    #
    # Zanjirning oxirgi bo'g'ini: agent so'radi -> sotuvchi javob
    # berdi -> agent odamga aytdi. Bo'g'in uzilsa `sorov_yubor`
    # bajarib bo'lmaydigan va'daga aylanadi.
    sot2 = baza.sotuvchi_yoz(
        "Charm ustaxona", "kreslo va divan charm qoplama", [], [],
        "Yunusobod", "998922223344",
        sorted(yonalishlar_belgilar("kreslo va divan charm qoplama")))
    tekshir(bool(sot2), "ikkinchi sinov sotuvchisi yozilsin")

    r = vosita("sorov_yubor", {"matn": "kreslo kerak charm qora",
                               "aloqa": "998901237777"})
    tekshir(r.get("yuborildi", 0) >= 2,
            f"talab ikkala sotuvchiga borsin ({r.get('yuborildi')})")
    kalit = r["kalit"]
    kuzatish = r["kuzatish"]
    tekshir(bool(kalit) and not kalit.isdigit(),
            "sorov_yubor kalit qaytarsin (raqamli ID emas)")
    tekshir(r.get("keyingi_qadam") == "javoblar",
            "sorov_yubor keyingi qadamni ko'rsatsin")
    sid2 = r["sorov_id"]

    # KIRISH — FAQAT KALIT BILAN
    r = vosita("javoblar", {"kalit": str(sid2)})
    tekshir("xato" in r, "raqamli ID bilan begona talab ochilmasin")
    # `baza.sorov_id_token` raqamni allaqachon rad etadi, ya'ni yuqoridagi
    # tekshiruv MCP qatlamidagi qo'riqchi olib tashlansa ham o'tadi.
    # Agent uchun farq bor: "topilmadi" degan javob uni qayta urinishga
    # undaydi, aniq maslahat esa to'g'ri yo'lni ko'rsatadi.
    tekshir(bool(r.get("maslahat")),
            "raqamli ID xatosida agentga aniq maslahat berilsin")
    r = vosita("javoblar", {"kalit": "yoq-bunday-kalit-12345"})
    tekshir("xato" in r, "noto'g'ri kalit rad etilsin")
    r = vosita("javoblar", {"kalit": ""})
    tekshir("xato" in r, "bo'sh kalit rad etilsin")

    # `javoblar` BEGONA TALABGA TEGMASIN.
    #
    # Sayt xaridor sahifasi umumiy `ochiq_sorovlarni_yurit()` ni
    # chaqiradi — u BARCHA ochiq so'rovlarga tegadi. MCP'da ataylab
    # faqat shu so'rovning to'lqini ochiladi.
    #
    # NEGA SPY, `yuborishlar` SANOG'I EMAS (2026-08-17 da o'rganildi).
    # Avval sanoq bilan yozilgan edi va mutatsiya sinovidan O'TIB
    # KETDI: `baza.sotuvchi_yoz` yangi sotuvchiga barcha ochiq mos
    # talablarni o'zi yuboradi (`_yangi_sotuvchiga_ochiq_sorovlar`,
    # 581-qator). Ya'ni umumiy chaqiruv ham qo'shimcha qator
    # yozmasdi — nojo'ya ta'sir bu fikstura ichida KO'RINMAYDI.
    # Shuning uchun qoida to'g'ridan-to'g'ri tekshiriladi.
    umumiy = []
    asl_umumiy = baza.ochiq_sorovlarni_yurit
    tolqinlar = []
    asl_tolqin = baza.tolqin_yubor
    baza.ochiq_sorovlarni_yurit = lambda: umumiy.append(1)
    baza.tolqin_yubor = lambda i: (tolqinlar.append(i), asl_tolqin(i))[1]
    try:
        # HAVOLANING O'ZI ham ishlasin — agent ko'pincha shuni qaytaradi.
        r = vosita("javoblar", {"kalit": kuzatish})
    finally:
        baza.ochiq_sorovlarni_yurit = asl_umumiy
        baza.tolqin_yubor = asl_tolqin
    tekshir(not umumiy,
            "javoblar UMUMIY to'lqinni yurgizmasin — begona talablarga "
            "tegmaydi")
    tekshir(tolqinlar == [sid2],
            f"javoblar faqat O'Z so'rovining to'lqinini ochsin ({tolqinlar})")

    tekshir(r.get("ok") is True, f"butun havola qabul qilinsin ({r})")
    tekshir(r["holat"] == "kutilmoqda",
            f"javob yo'q — holat `kutilmoqda` ({r.get('holat')})")
    tekshir(r["javoblar"] == [], "javob yo'q — ro'yxat bo'sh")
    tekshir(r["talab"] == "kreslo kerak charm qora", "talab matni qaytsin")

    # SOTUVCHI JAVOB BERDI
    with baza.ulan() as c:
        s_id = c.execute("SELECT id FROM sotuvchilar WHERE aloqa=?",
                         ("998911112233",)).fetchone()["id"]
    tekshir(baza.javob_yoz(sid2, s_id, "bor", 2_400_000,
                           "Qora charm, tayyor") is not None,
            "1-sotuvchi javobi yozilsin")
    tekshir(baza.javob_yoz(sid2, sot2, "oxshash", 1_900_000,
                           "Mato bor") is not None,
            "2-sotuvchi javobi yozilsin")

    r = vosita("javoblar", {"kalit": kalit})
    tekshir(r["holat"] == "javob_bor", f"javob keldi ({r.get('holat')})")
    tekshir(r["javob_soni"] == 2, f"ikkala javob ko'rinsin ({r['javob_soni']})")
    turlar = sorted(x["turi"] for x in r["javoblar"])
    tekshir(turlar == ["aynan", "oxshash"],
            f"`bor`/`oxshash` agent tiliga o'girilsin ({turlar})")
    tekshir(r.get("eng_arzon_som") == 1_900_000,
            f"eng arzon narx hisoblansin ({r.get('eng_arzon_som')})")

    # TELEFON RAQAMI VA ICHKI ID SIZIB CHIQMASIN
    matn = json.dumps(r, ensure_ascii=False)
    tekshir("998911112233" not in matn,
            "javobda SOTUVCHI telefoni bo'lmasin")
    tekshir("998901237777" not in matn,
            "javobda XARIDOR telefoni bo'lmasin")
    tekshir(all(k not in x for x in r["javoblar"]
                for k in ("sotuvchi_id", "suhbat_id", "javob_id")),
            "ichki ID lar javobga tushmasin")

    # `javoblar` YANGI TALAB YARATMASIN
    with baza.ulan() as c:
        oldin = c.execute("SELECT COUNT(*) n FROM sorovlar").fetchone()["n"]
    vosita("javoblar", {"kalit": kalit})
    vosita("javoblar", {"kalit": kalit})
    with baza.ulan() as c:
        keyin = c.execute("SELECT COUNT(*) n FROM sorovlar").fetchone()["n"]
    tekshir(oldin == keyin,
            f"`javoblar` yangi so'rov yozmasin ({oldin} -> {keyin})")

    # ── 10b. KALIT VA MUDDAT — SOF FUNKSIYALAR ─────────────────────
    tekshir(ms._kalit_ol("https://ober.uz/takliflar?kalit=abc123&rol=x")
            == "abc123", "havoladan kalit ajratilsin")
    tekshir(ms._kalit_ol("  abc123  ") == "abc123",
            "yalang'och kalit ham ishlasin")
    tekshir(ms._kalit_ol("") == "", "bo'sh kirish — bo'sh natija")
    hozir = time.time()
    tekshir(ms._ochiqmi({"holat": "yuborildi", "yaratildi": hozir}),
            "yangi talab ochiq")
    tekshir(not ms._ochiqmi({"holat": "yuborildi",
                             "yaratildi": hozir - 25 * 3600}),
            "24 soatdan eski talab yopiq")
    tekshir(not ms._ochiqmi({"holat": "yopildi", "yaratildi": hozir}),
            "yopilgan talab ochiq emas")

    # ── 11. VOSITALAR RO'YXATI ─────────────────────────────────────
    tekshir(set(ms.ISHLOVCHILAR) == {"qidir", "sorov_yubor", "javoblar"},
            "vositalar ro'yxati kengaymasin")
    tekshir(not any("javob_ber" in k or "yoz" in k or "kelish" in k
                    for k in ms.ISHLOVCHILAR),
            "sotuvchiga JAVOB YOZADIGAN vosita qo'shilmasin — "
            "savdolashish odamning ishi")

    # ── 12. JONLI BAZAGA TEGILMAGANMI ──────────────────────────────
    if JONLI_HOLAT:
        hozir = (JONLI.stat().st_mtime, JONLI.stat().st_size)
        tekshir(hozir == JONLI_HOLAT,
                "JONLI BAZA O'ZGARMASIN — sinov unga yozmaydi")
    tekshir(str(baza.DB).startswith(str(VAQTINCHA)),
            "sinov o'z vaqtinchalik bazasida yurdi")

    shutil.rmtree(VAQTINCHA, ignore_errors=True)

    print("-" * 52)
    print(f"  NATIJA: {jami - xato} to'g'ri · {xato} xato  ({jami} tadan)\n")
    return 1 if xato else 0


if __name__ == "__main__":
    raise SystemExit(main())
