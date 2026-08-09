"""
OBER — MA'LUMOT BAZASI (SQLite)

Nega SQLite: server kerak emas, bitta fayl, tez. Hajm oshganda
PostgreSQL'ga ko'chiriladi — sxema o'zgarmaydi.
"""

from __future__ import annotations

import re
import sqlite3
import threading
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent          # ober/
DB = BASE / "data" / "ober.db"
_INIT_QILINDI: set[str] = set()
_INIT_QULF = threading.Lock()
FTS_BOR = False          # SQLite'da FTS5 bormi (init() aniqlaydi)


_HOVUZ: list[sqlite3.Connection] = []
_HOVUZ_QULF = threading.Lock()
_HOVUZ_KATTALIGI = 12


class _Ulanish:
    """Hovuzdan olingan ulanish. `with` tugagach hovuzga qaytadi.

    NEGA HOVUZ (2026-08-04)
    -----------------------
    Ilgari `ulan()` HAR CHAQIRUVDA yangi ulanish ochardi va uning
    ustiga uchta PRAGMA yugurtirardi (journal_mode, synchronous,
    busy_timeout). Bitta so'rov uchun bu ko'rinmaydi.

    Lekin `takliflar` sahifasi har 3.5 soniyada, bildirishnomalar esa
    har 5 soniyada so'rov yuboradi. Aziz brauzerida 32 ta tab ochiq
    edi — ya'ni sekundiga o'nlab so'rov, har biri yangi ulanish va
    yangi PRAGMA. Ustiga yig'uvchi ham to'xtovsiz yozadi.

    2026-08-04, soat 11:39: sayt javob berishdan to'xtadi, qorovul
    uni 11:41 da qayta yoqdi. Caddy jurnalida so'rovlar 20-100
    soniyagacha osilib turgani ko'rindi — hammasi `/api/suhbat` va
    `/api/bildirishnomalar`, ya'ni aynan so'rab turadigan yo'llar.

    Endi ulanishlar qayta ishlatiladi. Hovuz to'lgan bo'lsa yangisi
    ochiladi va ishlatilgach yopiladi — ya'ni yuk cho'qqisida ham
    ishlayveradi, faqat tejamsizroq.
    """

    __slots__ = ("c",)

    def __init__(self) -> None:
        with _HOVUZ_QULF:
            self.c = _HOVUZ.pop() if _HOVUZ else None
        if self.c is None:
            self.c = _yangi_ulanish()

    def __enter__(self) -> sqlite3.Connection:
        return self.c

    def __exit__(self, tur, qiymat, iz) -> None:
        try:
            if tur is None:
                self.c.commit()
            else:
                self.c.rollback()
        except sqlite3.Error:
            # Ulanish buzilgan — hovuzga qaytarmaymiz.
            try:
                self.c.close()
            except sqlite3.Error:
                pass
            return
        with _HOVUZ_QULF:
            if len(_HOVUZ) < _HOVUZ_KATTALIGI:
                _HOVUZ.append(self.c)
                return
        self.c.close()


def ulan() -> _Ulanish:
    """Hovuzdan SQLite ulanishi. Har doim `with ulan() as c:` bilan."""
    DB.parent.mkdir(parents=True, exist_ok=True)
    return _Ulanish()


def _yangi_ulanish() -> sqlite3.Connection:
    """SQLite ulanishi — WAL rejimida.

    2026-08-01 o'lchov: bir xil ish hajmida qidiruv 145 ms dan 6 735 ms
    gacha sakrardi. Sabab indeks emas, QULF edi: standart rejimda bitta
    yozuv (qidiruv jurnali, to'lqin yuborish, bot) butun bazani bloklaydi
    va o'qiyotgan so'rov kutib turadi.

    WAL'da o'qish va yozish bir-birini to'sib qo'ymaydi.
    `busy_timeout` — yozuvlar to'qnashsa darhol xato bermay, kutadi.
    """
    DB.parent.mkdir(parents=True, exist_ok=True)
    # `check_same_thread=False` — ulanish hovuzda turadi va boshqa oqimga
    # o'tishi mumkin. Bir vaqtda faqat bitta oqim ishlatadi: hovuzdan
    # olingan ulanish qaytarilmaguncha boshqa hech kimga berilmaydi.
    c = sqlite3.connect(str(DB), timeout=15, check_same_thread=False)
    c.row_factory = sqlite3.Row
    try:
        c.execute("PRAGMA journal_mode=WAL")
        c.execute("PRAGMA synchronous=NORMAL")
        c.execute("PRAGMA busy_timeout=15000")
    except sqlite3.DatabaseError:
        pass
    return c


def init() -> None:
    # Har HTTP so‘rovda CREATE TABLE/INDEX qayta yurishi baza mtime'ini
    # o‘zgartirib, qidiruv keshini bekor qilardi. Har DB faylini bir processda
    # faqat bir marta migratsiya qilamiz; boshqa process o‘z initini qiladi.
    kalit = str(DB.resolve())
    if kalit in _INIT_QILINDI and DB.exists():
        return
    with _INIT_QULF:
        if kalit in _INIT_QILINDI and DB.exists():
            return
        _init_ichki()
        _INIT_QILINDI.add(kalit)


def _init_ichki() -> None:
    with ulan() as c:
        c.execute("""
        CREATE TABLE IF NOT EXISTS elonlar (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            manba         TEXT NOT NULL,        -- olx / birbir / telegram
            tashqi_id     TEXT NOT NULL,        -- manbadagi ID
            nom           TEXT NOT NULL,
            narx_som      INTEGER,              -- so'mga keltirilgan
            narx_asl      TEXT,                 -- asl matn: "95 000 сум"
            valyuta       TEXT,                 -- som / usd
            kelishiladi   INTEGER DEFAULT 0,    -- "Договорная"
            holat         TEXT,                 -- yangi / b_u
            viloyat       TEXT,                 -- Toshkent viloyati, Samarqand...
            shahar        TEXT,                 -- Ташкент, Самарканд, Нукус...
            tuman         TEXT,                 -- Чиланзарский (faqat Toshkentda)
            sana          TEXT,                 -- manbadagi matn
            havola        TEXT,
            rasm          TEXT,
            telefon       TEXT,                 -- e'lon sahifasidan (keyingi bosqich)
            biznes        INTEGER DEFAULT 0,    -- do'konmi
            qism_turi     TEXT,                 -- "Тормозная система"
            tavsif        TEXT,
            sotuvchi_id   TEXT,                 -- manbadagi sotuvchi profili
            olindi        REAL,                 -- yig'ilgan vaqt
            UNIQUE(manba, tashqi_id)
        )""")
        # Eski bazaga yangi ustun qo'shish (migratsiya)
        mavjud = {r["name"] for r in c.execute("PRAGMA table_info(elonlar)")}
        # tan_* — e'lon BIR MARTA tahlil qilinib, natija saqlanadi.
        # Aks holda har qidiruvda 1600+ e'lon qayta tahlil qilinadi va
        # qidiruv 3-5 soniya davom etadi (2026-07-30 vizual sinovda o'lchandi).
        for ustun, tur in (("viloyat", "TEXT"), ("sotuvchi_nomi", "TEXT"),
                           ("rasmlar", "TEXT"),
                           ("tan_modellar", "TEXT"), ("tan_qismlar", "TEXT"),
                           # Faqat SARLAVHADAN tanilgan qismlar. OLX ning
                           # keng kategoriyasi ("Автосвет") tumanka va
                           # stopni ham `fara` qilib qo'yadi — ishonchli
                           # moslikni ajratish uchun alohida ustun kerak.
                           ("tan_nom_qismlar", "TEXT"),
                           ("faol", "INTEGER NOT NULL DEFAULT 1"),
                           ("korilmadi", "INTEGER NOT NULL DEFAULT 0"),
                           ("oxirgi_korildi", "REAL"),
                           ("oxirgi_sikl", "TEXT"),
                           # Qaysi bozor bo'limidan kelgan ("Mebel",
                           # "Kvartira ijara"). Qidiruvda va filtrda kerak.
                           ("kategoriya", "TEXT"),
                           # E'lonning BARCHA tavsiflari (OLX bergan):
                           # kvartira uchun xona/qavat/maydon, telefon
                           # uchun model/xotira. JSON ro'yxat.
                           # Bu har kategoriya uchun TAYYOR lug'at —
                           # qo'lda yozish shart emas (2026-08-02).
                           ("xususiyatlar", "TEXT"),
                           ("olx_kategoriya", "TEXT"),
                           # OBER E'LONLARI — o'z marketplace (2026-08-06):
                           # sotuvchi OBER'da o'z e'lonini joylashtiradi.
                           # `egasi` — OBER sotuvchilar.id (manba='ober' da).
                           # `elon_holati` — 'faol'|'sotildi'|'ochirildi'.
                           # DIQQAT: `holat` ustuni BAND (OLX: yangi/b_u),
                           # shuning uchun yangi nom ishlatiladi.
                           ("egasi", "INTEGER"),
                           ("elon_holati", "TEXT NOT NULL DEFAULT 'faol'"),
                           ("yangilandi", "REAL"),
                           ("rasmlar_ober", "TEXT")):
            if ustun not in mavjud:
                c.execute(f"ALTER TABLE elonlar ADD COLUMN {ustun} {tur}")

        # ── FTS5: TO'LIQ-MATN INDEKSI ────────────────────────────────────
        # 2026-08-01: qidiruv HAMMA e'lonni xotiraga yuklardi. 11 500 da
        # bu tez edi (23 ms), lekin barcha kategoriyalar yig'ilgach baza
        # 100 000+ ga chiqadi va xotira yetmaydi (kompyuterda 8 GB, 82%
        # band). Endi qidiruv indeksda bajariladi — xotiraga hech narsa
        # yuklanmaydi.
        #
        # `norm` — normallashtirilgan matn (kirill -> lotin, q->k ...).
        # So'rov ham aynan shunday normallashtiriladi, shuning uchun
        # imlo va alifbo farqi indeks darajasida hal bo'ladi.
        # `teg`  — lug'at tanigan model va qism kalitlari.
        #
        # DIQQAT: `content=''` (kontentsiz) QILINMAYDI.
        # 2026-08-01 xato: kontentsiz jadvaldan DELETE qilib bo'lmaydi
        # ("cannot DELETE from contentless fts5 table"), e'lon yangilanganda
        # esa indeksni yangilash kerak. Oddiy FTS5 jadvali o'z nusxasini
        # saqlaydi — 200 000 e'lon uchun ~15 MB, arzimas narx.
        global FTS_BOR
        try:
            eski = c.execute("SELECT sql FROM sqlite_master"
                             " WHERE name='elonlar_fts'").fetchone()
            if eski and "content=''" in (eski["sql"] or ""):
                c.execute("DROP TABLE elonlar_fts")   # eski, yaroqsiz shakl
            c.execute("CREATE VIRTUAL TABLE IF NOT EXISTS elonlar_fts"
                      " USING fts5(norm, teg)")
            FTS_BOR = True
        except sqlite3.OperationalError:
            FTS_BOR = False        # FTS5 yo'q — eski usulga qaytamiz

        c.execute("CREATE INDEX IF NOT EXISTS ix_nom ON elonlar (nom)")
        c.execute("CREATE INDEX IF NOT EXISTS ix_narx ON elonlar (narx_som)")
        c.execute("CREATE INDEX IF NOT EXISTS ix_joy ON elonlar (viloyat, shahar, tuman)")
        c.execute("CREATE INDEX IF NOT EXISTS ix_faol_manba ON elonlar (faol, manba)")

        # Narx tarixi — bizning asosiy aktivimiz.
        # Har safar narx o'zgarsa yangi qator qo'shiladi.
        c.execute("""
        CREATE TABLE IF NOT EXISTS narx_tarix (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            manba     TEXT, tashqi_id TEXT,
            narx_som  INTEGER,
            vaqt      REAL
        )""")
        c.execute("CREATE INDEX IF NOT EXISTS ix_tarix ON narx_tarix (manba, tashqi_id)")

        # ── QIDIRUVLAR — butun biznesning urug'i.
        # Har qidiruv yoziladi. Bir oydan keyin sotuvchiga aytish mumkin:
        # "Sergelida sizning tovaringizni 47 marta qidirishdi, hech biri
        # sizga yetib bormadi." Bu eng kuchli argument.
        # Bir vaqtda: lug'atdagi bo'shliq, keyingi kategoriya, narx tahlili.
        c.execute("""
        CREATE TABLE IF NOT EXISTS qidiruvlar (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            sorov        TEXT NOT NULL,
            modellar     TEXT,          -- tanilgan modellar, vergul bilan
            qismlar      TEXT,          -- tanilgan qism turlari
            tuman        TEXT,          -- qayerdan qidirildi
            natija_soni  INTEGER,
            kesildi      INTEGER,       -- boshqa model bo'lgani uchun
            narx_min     INTEGER,
            narx_max     INTEGER,
            vaqt         REAL
        )""")
        c.execute("CREATE INDEX IF NOT EXISTS ix_qid_vaqt ON qidiruvlar (vaqt)")
        c.execute("CREATE INDEX IF NOT EXISTS ix_qid_qism ON qidiruvlar (qismlar)")

        # ── SO'ROVLAR — xaridor sotuvchilardan so'raydi.
        # Qidiruv natija bermasa yoki jonli javob kerak bo'lsa shu yerga tushadi.
        # AYNAN SHU JOYDA qidiruv bozorga aylanadi.
        c.execute("""
        CREATE TABLE IF NOT EXISTS sorovlar (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            matn       TEXT NOT NULL,
            modellar   TEXT,
            qismlar    TEXT,
            tuman      TEXT,
            byudjet    INTEGER,         -- ixtiyoriy. TALAB emas, byudjet.
            aloqa      TEXT,            -- telefon yoki telegram
            holat      TEXT DEFAULT 'yangi',   -- yangi|yuborildi|javob_bor|yopildi
            yaratildi  REAL,
            yopiladi   REAL             -- 2 soatdan keyin
        )""")
        sorov_ustunlari = {r["name"] for r in c.execute(
            "PRAGMA table_info(sorovlar)")}
        for ustun, tur in (("yonalishlar", "TEXT"),
                           ("oxirgi_faol", "REAL"),
                           ("vaqt_yashir", "INTEGER NOT NULL DEFAULT 0"),
                           ("ism", "TEXT"),
                           ("token", "TEXT")):
            if ustun not in sorov_ustunlari:
                c.execute(f"ALTER TABLE sorovlar ADD COLUMN {ustun} {tur}")
        import secrets
        for r in c.execute("SELECT id FROM sorovlar"
                           " WHERE token IS NULL OR token='' ").fetchall():
            c.execute("UPDATE sorovlar SET token=? WHERE id=?",
                      (secrets.token_urlsafe(32), r["id"]))
        c.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_sorov_token"
                  " ON sorovlar (token)")
        c.execute("CREATE INDEX IF NOT EXISTS ix_sorov_holat ON sorovlar (holat)")

        # ── JAVOBLAR — sotuvchi bir tegishda javob beradi
        c.execute("""
        CREATE TABLE IF NOT EXISTS javoblar (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            sorov_id   INTEGER,
            sotuvchi   TEXT,
            holat      TEXT,            -- bor | yoq | oxshash
            narx       INTEGER,
            izoh       TEXT,
            tanlandi    INTEGER DEFAULT 0,
            vaqt       REAL
        )""")
        javob_ustunlari = {r["name"] for r in c.execute(
            "PRAGMA table_info(javoblar)")}
        if "tanlandi" not in javob_ustunlari:
            c.execute("ALTER TABLE javoblar ADD COLUMN tanlandi INTEGER DEFAULT 0")
        c.execute("CREATE INDEX IF NOT EXISTS ix_javob ON javoblar (sorov_id)")

        # ── SOTUVCHILAR — ro'yxat 30 soniya: "nima sotasiz?" + joy.
        # Kategoriya daraxti YO'Q — odam o'z so'zi bilan yozadi, AI tushunadi.
        # Xatti-harakat sozlamadan aniqroq: javob bergan turdagi so'rovlar
        # ko'payadi, javobsiz qoldirgani kamayadi.
        c.execute("""
        CREATE TABLE IF NOT EXISTS sotuvchilar (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            nom         TEXT,
            nima_sotadi TEXT NOT NULL,     -- o'z so'zi bilan
            qismlar     TEXT,              -- AI tushungani
            modellar    TEXT,
            tuman       TEXT,
            aloqa       TEXT NOT NULL,
            faol        INTEGER DEFAULT 1,
            javob_soni  INTEGER DEFAULT 0,
            yaratildi   REAL
        )""")
        sotuvchi_ustunlari = {r["name"] for r in c.execute(
            "PRAGMA table_info(sotuvchilar)")}
        for ustun, tur in (("yonalishlar", "TEXT"),
                           # Telegram — sotuvchining ASOSIY kanali.
                           # Sotuvchi saytni ochib o'tirmaydi; so'rov
                           # telefoniga keladi va javob ham o'sha yerda
                           # beriladi. `ulash_kodi` — bir martalik kod,
                           # u orqali Telegram akkaunti bog'lanadi.
                           ("telegram_id", "TEXT"),
                           ("ulash_kodi", "TEXT"),
                           # Onlayn holat: "hozir onlayn" yoki "5 daqiqa
                           # oldin". Chatda odam tirikligini ko'rsatadi.
                           ("oxirgi_faol", "REAL"),
                           # Xohlasa vaqtini yashiradi (Telegramdagi kabi)
                           ("vaqt_yashir", "INTEGER NOT NULL DEFAULT 0")):
            if ustun not in sotuvchi_ustunlari:
                c.execute(f"ALTER TABLE sotuvchilar ADD COLUMN {ustun} {tur}")
        c.execute("CREATE INDEX IF NOT EXISTS ix_sot_tg"
                  " ON sotuvchilar (telegram_id)")
        c.execute("CREATE INDEX IF NOT EXISTS ix_sot_tuman ON sotuvchilar (tuman)")

        # OBER ichidagi yozishma. Har ijobiy taklif o'z suhbatiga ega;
        # telefon raqamlari bu jadvallarga ko'chirilmaydi.
        c.execute("""
        CREATE TABLE IF NOT EXISTS suhbatlar (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            sorov_id     INTEGER NOT NULL,
            javob_id     INTEGER NOT NULL UNIQUE,
            sotuvchi_id  INTEGER NOT NULL,
            yaratildi    REAL,
            yangilandi   REAL
        )""")
        c.execute("CREATE INDEX IF NOT EXISTS ix_suhbat_sorov ON suhbatlar (sorov_id)")
        c.execute("CREATE INDEX IF NOT EXISTS ix_suhbat_sotuvchi ON suhbatlar (sotuvchi_id)")
        c.execute("""
        CREATE TABLE IF NOT EXISTS xabarlar (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            suhbat_id        INTEGER NOT NULL,
            rol              TEXT NOT NULL,
            matn             TEXT,
            rasm             TEXT,
            vaqt             REAL,
            xaridor_oqidi    INTEGER DEFAULT 0,
            sotuvchi_oqidi   INTEGER DEFAULT 0
        )""")
        c.execute("CREATE INDEX IF NOT EXISTS ix_xabar_suhbat ON xabarlar (suhbat_id, id)")
        xabar_ustunlari = {r["name"] for r in c.execute(
            "PRAGMA table_info(xabarlar)")}
        # Joylashuv — chatda "shu yerdaman" deyish uchun. "lat,lon".
        if "joy" not in xabar_ustunlari:
            c.execute("ALTER TABLE xabarlar ADD COLUMN joy TEXT")
        if "tg_yuborildi" not in xabar_ustunlari:
            # Xaridor xabari sotuvchining Telegramiga uzatildimi.
            # Sotuvchi xaridorni KO'RISHI kerak — aks holda "bor/yo'q"
            # bosish bo'shliqqa gapirgandek tuyuladi (Aziz, 2026-08-01).
            c.execute("ALTER TABLE xabarlar ADD COLUMN"
                      " tg_yuborildi INTEGER NOT NULL DEFAULT 0")

        # SO'ROV KIMGA YUBORILDI — to'lqin bo'yicha.
        # Ilgari sotuvchi o'zi mos so'rovlarni "tortib" olardi va so'rov
        # avtomatik ravishda HAMMA mos sotuvchiga ko'rinardi. Natijada:
        #   1) xaridorga nechta sotuvchiga yetgani noma'lum edi;
        #   2) sotuvchi soni o'sganda har so'rov hammaga borib spam bo'lardi.
        # Endi yuborish yozib boriladi va to'lqinlarga bo'linadi.
        c.execute("""
        CREATE TABLE IF NOT EXISTS yuborishlar (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            sorov_id     INTEGER NOT NULL,
            sotuvchi_id  INTEGER NOT NULL,
            tolqin       INTEGER NOT NULL DEFAULT 1,
            vaqt         REAL,
            -- Telegramga xabar ketdimi. Ikki marta yubormaslik uchun.
            xabar        INTEGER NOT NULL DEFAULT 0,
            UNIQUE (sorov_id, sotuvchi_id)
        )""")
        yub_ustunlari = {r["name"] for r in c.execute(
            "PRAGMA table_info(yuborishlar)")}
        if "xabar" not in yub_ustunlari:
            c.execute("ALTER TABLE yuborishlar ADD COLUMN"
                      " xabar INTEGER NOT NULL DEFAULT 0")
        c.execute("CREATE INDEX IF NOT EXISTS ix_yub_sorov ON yuborishlar (sorov_id)")
        c.execute("CREATE INDEX IF NOT EXISTS ix_yub_sotuvchi"
                  " ON yuborishlar (sotuvchi_id, sorov_id)")

        # ATAMALAR — o'zbekcha va ruscha juftlik.
        # "Yangi" <-> "Новый", "Akkumulyatorlar" <-> "Аккумуляторы".
        # Qidiruv ikki tilda ishlashi uchun (Aziz, 2026-08-02).
        c.execute("""
        CREATE TABLE IF NOT EXISTS atamalar (
            kalit  TEXT NOT NULL,
            uz     TEXT NOT NULL,
            ru     TEXT NOT NULL,
            PRIMARY KEY (uz, ru)
        )""")

        # YIG'ISH HOLATI — uzoq yig'ishni to'xtatib, keyin DAVOM ETTIRISH.
        # Barcha kategoriya x viloyat juftligi soatlab davom etadi;
        # kompyuter o'chsa yoki Ctrl+C bosilsa, ish boshidan boshlanmasin.
        c.execute("""
        CREATE TABLE IF NOT EXISTS yigish_holati (
            kategoriya  TEXT NOT NULL,
            viloyat     TEXT NOT NULL,
            sahifa      INTEGER NOT NULL DEFAULT 0,
            tugadi      INTEGER NOT NULL DEFAULT 0,
            topildi     INTEGER NOT NULL DEFAULT 0,
            vaqt        REAL,
            PRIMARY KEY (kategoriya, viloyat)
        )""")

        # ── SESSIYA VA KIRISH KODI ──────────────────────────────────────
        # 2026-08-06: kabinet endi telefon raqam + bir martalik kod orqali
        # ochiladi. Ilgari sotuvchi ID raqami faqat localStorage'da turardi:
        # boshqa qurilmada kabinet yo'qolardi, ID'ni bilgan har kim ham
        # kira olardi. Endi kirishda sessiya tokeni beriladi.
        c.execute("""
        CREATE TABLE IF NOT EXISTS sessiyalar (
            token       TEXT PRIMARY KEY,
            sotuvchi_id INTEGER NOT NULL,
            yaratildi   REAL,
            oxirgi_faol REAL
        )""")
        c.execute("CREATE INDEX IF NOT EXISTS ix_sessiya_sotuvchi"
                  " ON sessiyalar (sotuvchi_id)")
        c.execute("""
        CREATE TABLE IF NOT EXISTS kirish_kodlari (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            aloqa       TEXT NOT NULL,
            kod         TEXT NOT NULL,
            yaratildi   REAL,
            ishlatildi  INTEGER NOT NULL DEFAULT 0
        )""")
        c.execute("CREATE INDEX IF NOT EXISTS ix_kirish_aloqa"
                  " ON kirish_kodlari (aloqa)")


def sotuvchi_yoz(nom: str, nima: str, qismlar: list, modellar: list,
                 tuman: str, aloqa: str, yonalishlar: list | None = None) -> int:
    init()
    with ulan() as c:
        cur = c.execute(
            "INSERT INTO sotuvchilar (nom, nima_sotadi, qismlar, modellar,"
            " tuman, aloqa, yonalishlar, yaratildi) VALUES (?,?,?,?,?,?,?,?)",
            (nom, nima, ",".join(qismlar), ",".join(modellar), tuman, aloqa,
             ",".join(yonalishlar or []), time.time()))
        sotuvchi_id = cur.lastrowid
    # Yangi sotuvchi faqat kelajakdagi so'rovlarni kutib qolmasin: shu
    # paytda hali ochiq va javobsiz bo'lgan mos talablar darhol kabinetiga
    # tushadi. Bu ro'yxatdan o'tishning birinchi qiymatini ko'rsatadi.
    _yangi_sotuvchiga_ochiq_sorovlar(sotuvchi_id)
    return sotuvchi_id


# ── KIRISH VA SESSIYA ────────────────────────────────────────────────────────
# 2026-08-06: kabinet endi telefon raqam + bir martalik kod orqali ochiladi.
# Oldin faqat localStorage'da ID turardi — boshqa qurilmada kabinet yo'qolardi
# va ID'ni bilgan har kim kira olardi. Endi:
#   kirish_kod_yarat(aloqa)  — kod yaratadi (Telegram'ga yuboriladi)
#   kirish_kod_tekshir(...)  — kodni tekshirib sotuvchi_id qaytaradi
#   sessiya_yarat(id)        — kabinet uchun token beradi
#   sessiya_sotuvchisi(tok)  — tokenni tekshirib id qaytaradi

KOD_MUDDATI = 10 * 60          # kirish kodi 10 daqiqa amal qiladi
SESSIYA_MUDDATI = 30 * 24 * 3600   # sessiya 30 kun


def kirish_kod_soni(aloqa: str) -> int:
    """So'nggi soatda shu raqamga necha marta kod so'ralgan.

    2026-08-06: boshqa odam raqamni bilgan bo'lsa, kod so'rab turib
    asl kodlarni bekor qilishi mumkin (har yangi kod eskisini o'chiradi).
    Shu sababli bitta raqamga soatiga 5 tadan ortiq kod bermaymiz.
    """
    init()
    with ulan() as c:
        return c.execute(
            "SELECT COUNT(*) n FROM kirish_kodlari WHERE aloqa=? AND yaratildi > ?",
            (aloqa, time.time() - 3600)).fetchone()["n"]


def kirish_kod_bekor(aloqa: str) -> None:
    """Yuborilmagan kodni o'chiradi (Telegram xatosi bo'lsa)."""
    init()
    with ulan() as c:
        c.execute("DELETE FROM kirish_kodlari WHERE aloqa=?", (aloqa,))


def kirish_kod_yarat(aloqa: str) -> str:
    """Telefon raqamiga 6 xonali bir martalik kirish kodi."""
    import secrets
    init()
    kod = f"{secrets.randbelow(1000000):06d}"
    with ulan() as c:
        # Eski ishlatilmagan kodlar o'chiriladi — har kirishda bitta kod.
        c.execute("DELETE FROM kirish_kodlari WHERE aloqa=?", (aloqa,))
        c.execute("INSERT INTO kirish_kodlari (aloqa, kod, yaratildi)"
                  " VALUES (?,?,?)", (aloqa, kod, time.time()))
    return kod


def kirish_kod_tekshir(aloqa: str, kod: str) -> int | None:
    """Kod to'g'ri bo'lsa sotuvchi_id qaytaradi, aks holda None."""
    init()
    with ulan() as c:
        r = c.execute("SELECT * FROM kirish_kodlari WHERE aloqa=? AND kod=?",
                      (aloqa, kod)).fetchone()
        if not r:
            return None
        if time.time() - r["yaratildi"] > KOD_MUDDATI:
            c.execute("DELETE FROM kirish_kodlari WHERE id=?", (r["id"],))
            return None
        c.execute("DELETE FROM kirish_kodlari WHERE id=?", (r["id"],))
        s = c.execute("SELECT id FROM sotuvchilar WHERE aloqa=?",
                      (aloqa,)).fetchone()
        return s["id"] if s else None


def sessiya_yarat(sotuvchi_id: int) -> str:
    """Kabinet uchun tasodifiy token. Faqat server biladi va boshqa
    qurilmada ham ishlaydi — telefon raqami orqali qayta olinadi."""
    import secrets
    init()
    token = secrets.token_urlsafe(32)
    with ulan() as c:
        c.execute("INSERT INTO sessiyalar (token, sotuvchi_id, yaratildi,"
                  " oxirgi_faol) VALUES (?,?,?,?)",
                  (token, sotuvchi_id, time.time(), time.time()))
        # Muddati o'tgan sessiyalarni tozalab turamiz (xotira/baza kengayishi)
        c.execute("DELETE FROM sessiyalar WHERE oxirgi_faol < ?",
                  (time.time() - SESSIYA_MUDDATI,))
    return token


def sessiya_bekor(token: str) -> bool:
    """Chiqish: sessiyani server tomondan bekor qiladi.
    Token qaytadan ishlamaydi — kabinetga faqat yangi kirish kodi
    bilan qaytish mumkin. Yaroqsiz token uchun ham True (farq
    bildirmaymiz — hech qanday foyda yo'q)."""
    if not token:
        return True
    init()
    with ulan() as c:
        c.execute("DELETE FROM sessiyalar WHERE token=?", (token,))
    return True


def sessiya_sotuvchisi(token: str) -> int | None:
    """Token orqali sotuvchi_id. Yaroqsiz yoki muddati o'tgan bo'lsa None."""
    if not token:
        return None
    init()
    with ulan() as c:
        r = c.execute("SELECT sotuvchi_id, oxirgi_faol FROM sessiyalar"
                      " WHERE token=?", (token,)).fetchone()
        if not r:
            return None
        if time.time() - r["oxirgi_faol"] > SESSIYA_MUDDATI:
            c.execute("DELETE FROM sessiyalar WHERE token=?", (token,))
            return None
        c.execute("UPDATE sessiyalar SET oxirgi_faol=? WHERE token=?",
                  (time.time(), token))
        return r["sotuvchi_id"]


def sorov_tokeni(sorov_id: int) -> str:
    """Xaridorning taxmin qilib bo'lmaydigan so'rov sessiyasi tokeni."""
    if not sorov_id:
        return ""
    init()
    with ulan() as c:
        r = c.execute("SELECT token FROM sorovlar WHERE id=?",
                      (sorov_id,)).fetchone()
    return (r["token"] or "") if r else ""


def sorov_id_token(token: str) -> int | None:
    """Xaridor tokenini ichki so'rov IDga yechadi."""
    if not token or token.isdigit():
        return None
    init()
    with ulan() as c:
        r = c.execute("SELECT id FROM sorovlar WHERE token=?",
                      (token,)).fetchone()
    return r["id"] if r else None


def sotuvchi_aloqasi(aloqa: str) -> dict | None:
    """Telefon raqami bo'yicha sotuvchini topadi (kirish uchun)."""
    init()
    with ulan() as c:
        r = c.execute("SELECT * FROM sotuvchilar WHERE aloqa=?",
                      (aloqa,)).fetchone()
    return dict(r) if r else None


def sotuvchi_profil(sotuvchi_id: int) -> dict | None:
    """Kabinetdagi profil uchun: ism/biznes nomi, nima sotasiz,
    qayerda, yo'nalish. Telefon raqami va ichki ustunlar qaytmaydi —
    profil o'z egasiga ham keraksiz tafsilotni ko'rsatmasin."""
    init()
    with ulan() as c:
        r = c.execute(
            "SELECT id, nom, nima_sotadi, tuman, yonalishlar,"
            " javob_soni, yaratildi FROM sotuvchilar WHERE id=?",
            (sotuvchi_id,)).fetchone()
    return dict(r) if r else None


# ── TO'LQINLI YUBORISH ───────────────────────────────────────────────────────
#
# Qaror (2026-08-01, Aziz): tetik VAQT bo'yicha, "necha marta qidirdi"
# bo'yicha emas. Qayta qidiruv ko'pincha tasodifiy (sahifa yangilandi,
# imlo tuzatildi); sabrli odam esa bir marta qidirib kutadi va unga
# ikkinchi to'lqin hech qachon bormasdi.
TOLQIN_JADVALI = (0, 3 * 60, 8 * 60)      # soniyada: 0, 3 va 8 daqiqa

# BOSHLANG'ICH REJIM. Hozir sotuvchi kam — so'rov mos keladigan hammaga
# boradi. Sabab qamrov emas: har sotuvchi OBER qanday ishlashini KO'RISHI
# kerak, aks holda tizimni tushunmay tashlab ketadi.
BOSHLANGICH = True
CHEGARA_BOSHLANGICH = 50

# ODATIY CHEGARA — 30 emas, 6.
#
# 2026-08-02 tadqiqot: dunyoda ishlayotgan teskari bozorlarning raqami
# butunlay boshqa. Justdial bir so'rovni 4-7 ta ta'minotchiga, Bark
# ~5 tasiga yuboradi. 30 emas.
#
# Sabab arifmetikada: 30 tadan bittasi yutsa, sotuvchining yutish
# ehtimoli 3%. Beshtadan bittasi — 20%. Birinchi holatda sotuvchi
# ikki-uch martadan keyin javob berishni tashlaydi; ikkinchisida javob
# berish arziydi. Xaridor uchun ham 30 ta taklif tanlov emas, shovqin.
#
# Va pul: 30 taga tarqatilgan so'rov uchun hech kim to'lamaydi.
CHEGARA_ODATIY = 6

# Kategoriyada shuncha faol sotuvchi bo'lgach, boshlang'ich rejim
# avtomatik o'chadi va CHEGARA_ODATIY ishlaydi.
ZICHLIK_CHEGARASI = 20


def _mos_sotuvchilar(c, sorov) -> list:
    """So'rovga mos sotuvchilar, eng mosi birinchi bo'lib."""
    from lugat import normalla

    from lugat import sorovni_tozala

    sorov_qismlari = {x for x in (sorov["qismlar"] or "").split(",") if x}
    sorov_yonalishlari = {x for x in (sorov["yonalishlar"] or "").split(",") if x}

    # SO'ROV SO'ZLARI — lug'at tanimaganda ASOSIY yo'l.
    #
    # 2026-08-01: Azizning sotuvchi hisobi (#70) hech qachon so'rov
    # olmagan, chunki u yozgan matnni lug'at tanimagan. Tizim bu haqda
    # hech narsa demagan — sotuvchi jimgina "o'lik" holatda qolgan.
    #
    # 2026-08-04: shu yerda yana bir to'siq topildi. Yuqorida shunday
    # qator turardi:
    #
    #     if not (sorov_qismlari or sorov_yonalishlari):
    #         return []          # tushunilmagan so'rov yuborilmaydi
    #
    # Ya'ni pastdagi "zaxira yo'l" faqat so'rov ALLAQACHON tanilgan
    # bo'lsa ishlardi — eng kerak bo'lgan holatda esa ishlamasdi.
    # "Gilam kerak" degan xaridor hech kimga yetib bormasdi.
    #
    # Lug'at endi ikkala tomonda ham BONUS: tanisa moslik aniqroq,
    # tanimasa odamlarning o'z so'zlari bo'yicha ishlaydi.
    sozlar, _ = sorovni_tozala(sorov["matn"] or "")
    sorov_sozlari = {w for w in sozlar if len(w) > 2}
    if not (sorov_qismlari or sorov_yonalishlari or sorov_sozlari):
        return []                       # umuman mazmun yo'q

    mos = []
    for s in c.execute("SELECT * FROM sotuvchilar WHERE faol=1"):
        s_qism = {x for x in (s["qismlar"] or "").split(",") if x}
        s_yon = {x for x in (s["yonalishlar"] or "").split(",") if x}

        aniq = False
        if sorov_yonalishlari and (sorov_yonalishlari & s_yon):
            aniq = True
        elif sorov_qismlari and (sorov_qismlari & s_qism):
            aniq = True

        xom = False
        if not aniq and sorov_sozlari:
            # So'z BOSHI bo'yicha solishtiramiz, oddiy `in` bilan emas.
            # `"usta" in "kapusta"` -> True bo'lib ketardi va kapusta
            # sotuvchiga usta so'rovi ketardi.
            s_sozlari = normalla(s["nima_sotadi"] or "").split()
            xom = any(sw.startswith(w) or w.startswith(sw)
                      for w in sorov_sozlari for sw in s_sozlari
                      if len(sw) > 2)

        if not (aniq or xom):
            continue                    # mos emas — bezovta qilmaymiz

        yaqin = bool(sorov["tuman"] and s["tuman"] and sorov["tuman"] == s["tuman"])
        # Tartib: aniq moslik -> yaqinlik -> tajriba
        mos.append((not aniq, not yaqin, -int(s["javob_soni"] or 0), int(s["id"])))
    mos.sort()
    return [x[3] for x in mos]


def _yangi_sotuvchiga_ochiq_sorovlar(sotuvchi_id: int,
                                     limit: int = 20) -> int:
    """Yangi sotuvchiga faol, hali javobsiz mos talablarni bir marta berish."""
    now = time.time()
    yuboriladigan: list[int] = []
    with ulan() as c:
        sorovlar = c.execute(
            "SELECT * FROM sorovlar"
            " WHERE holat IN ('yangi','yuborildi') AND yopiladi > ?"
            " ORDER BY id DESC LIMIT 200", (now,)).fetchall()
        for sorov in sorovlar:
            if sotuvchi_id in _mos_sotuvchilar(c, sorov):
                yuboriladigan.append(int(sorov["id"]))
                if len(yuboriladigan) >= limit:
                    break
        if yuboriladigan:
            c.executemany(
                "INSERT OR IGNORE INTO yuborishlar"
                " (sorov_id, sotuvchi_id, tolqin, vaqt) VALUES (?,?,1,?)",
                [(sorov_id, sotuvchi_id, now)
                 for sorov_id in yuboriladigan])
    return len(yuboriladigan)


def tolqin_yubor(sorov_id: int) -> dict:
    """Vaqti kelgan to'lqinni yuboradi. Har chaqiruvda xavfsiz.

    Qaytaradi: {"yuborildi": jami, "tolqin": nechanchi, "mos": mos jami}
    """
    init()
    now = time.time()
    with ulan() as c:
        sorov = c.execute("SELECT * FROM sorovlar WHERE id=?",
                          (sorov_id,)).fetchone()
        if not sorov:
            return {"yuborildi": 0, "tolqin": 0, "mos": 0}

        allaqachon = {r["sotuvchi_id"] for r in c.execute(
            "SELECT sotuvchi_id FROM yuborishlar WHERE sorov_id=?", (sorov_id,))}
        mos = _mos_sotuvchilar(c, sorov)
        jami_mos = len(mos)

        # Javob kelgan bo'lsa to'lqin to'xtaydi — odam allaqachon javobga ega.
        javob_bor = c.execute(
            "SELECT COUNT(*) n FROM javoblar WHERE sorov_id=? AND holat<>'yoq'",
            (sorov_id,)).fetchone()["n"]

        otgan = now - float(sorov["yaratildi"] or now)
        tolqin = sum(1 for t in TOLQIN_JADVALI if otgan >= t)
        if javob_bor:
            tolqin = min(tolqin, 1)

        # ZICHLIK O'ZI HAL QILADI.
        # Yo'nalishda sotuvchi kam bo'lsa — hammasiga (o'rgatish uchun).
        # Yetarli bo'lgach — eng mos 6 tasiga. Qo'lda o'zgartirish shart
        # emas, tizim o'zi o'tadi.
        zich = jami_mos >= ZICHLIK_CHEGARASI
        if BOSHLANGICH and not zich:
            ruxsat = min(CHEGARA_BOSHLANGICH, jami_mos)
        else:
            # Har to'lqinda chegaraning bir qismi ochiladi:
            # 1-to'lqin 2 ta, keyin 4, keyin 6.
            ruxsat = max(2, round(CHEGARA_ODATIY * tolqin
                                  / len(TOLQIN_JADVALI)))
            ruxsat = min(ruxsat, CHEGARA_ODATIY, jami_mos)

        yangi = [i for i in mos[:ruxsat] if i not in allaqachon]
        if yangi:
            c.executemany(
                "INSERT OR IGNORE INTO yuborishlar"
                " (sorov_id, sotuvchi_id, tolqin, vaqt) VALUES (?,?,?,?)",
                [(sorov_id, i, tolqin, now) for i in yangi])
            if sorov["holat"] == "yangi":
                c.execute("UPDATE sorovlar SET holat='yuborildi' WHERE id=?",
                          (sorov_id,))

        yuborildi = len(allaqachon) + len(yangi)
    return {"yuborildi": yuborildi, "tolqin": tolqin, "mos": jami_mos}


# ── TELEGRAM ─────────────────────────────────────────────────────────────────

def ulash_kodi_ol(sotuvchi_id: int) -> str:
    """Sotuvchi uchun bir martalik ulash kodi (Telegram deep-link uchun)."""
    import secrets
    init()
    with ulan() as c:
        r = c.execute("SELECT ulash_kodi FROM sotuvchilar WHERE id=?",
                      (sotuvchi_id,)).fetchone()
        if r and r["ulash_kodi"]:
            return r["ulash_kodi"]
        kod = secrets.token_urlsafe(9)
        c.execute("UPDATE sotuvchilar SET ulash_kodi=? WHERE id=?",
                  (kod, sotuvchi_id))
    return kod


def telegram_ulash(kod: str, telegram_id: str) -> dict | None:
    """Deep-link kodini Telegram akkauntiga bog'laydi."""
    init()
    with ulan() as c:
        r = c.execute("SELECT * FROM sotuvchilar WHERE ulash_kodi=?",
                      (kod,)).fetchone()
        if not r:
            return None
        c.execute("UPDATE sotuvchilar SET telegram_id=? WHERE id=?",
                  (str(telegram_id), r["id"]))
        return dict(r)


def telegram_ulanganmi(sotuvchi_id: int) -> bool:
    init()
    with ulan() as c:
        r = c.execute("SELECT telegram_id FROM sotuvchilar WHERE id=?",
                      (sotuvchi_id,)).fetchone()
    return bool(r and r["telegram_id"])


def sotuvchi_telegramdan(telegram_id: str) -> dict | None:
    init()
    with ulan() as c:
        r = c.execute("SELECT * FROM sotuvchilar WHERE telegram_id=?",
                      (str(telegram_id),)).fetchone()
    return dict(r) if r else None


def yuborilmagan_xabarlar(limit: int = 30) -> list[dict]:
    """Telegramga hali xabar ketmagan yuborishlar."""
    init()
    now = time.time()
    with ulan() as c:
        rows = c.execute(
            "SELECT y.id yid, y.sorov_id, y.sotuvchi_id,"
            "       s.matn, s.tuman, s.byudjet,"
            "       t.telegram_id, t.nom"
            " FROM yuborishlar y"
            " JOIN sorovlar s ON s.id = y.sorov_id"
            " JOIN sotuvchilar t ON t.id = y.sotuvchi_id"
            " WHERE y.xabar = 0 AND t.telegram_id IS NOT NULL"
            "   AND s.yopiladi > ? AND s.holat IN ('yangi','yuborildi','javob_bor')"
            " ORDER BY y.id LIMIT ?", (now, limit)).fetchall()
    return [dict(r) for r in rows]


def tg_kutayotgan_chat(limit: int = 20) -> list[dict]:
    """Xaridordan kelgan, sotuvchining Telegramiga hali uzatilmagan xabarlar."""
    init()
    with ulan() as c:
        rows = c.execute(
            "SELECT x.id, x.matn, x.suhbat_id, sh.sotuvchi_id, sh.sorov_id,"
            "       t.telegram_id, sr.matn sorov_matni"
            " FROM xabarlar x"
            " JOIN suhbatlar sh ON sh.id = x.suhbat_id"
            " JOIN sotuvchilar t ON t.id = sh.sotuvchi_id"
            " JOIN sorovlar sr ON sr.id = sh.sorov_id"
            " WHERE x.rol='xaridor' AND x.tg_yuborildi=0"
            "   AND t.telegram_id IS NOT NULL"
            " ORDER BY x.id LIMIT ?", (limit,)).fetchall()
    return [dict(r) for r in rows]


def tg_chat_belgila(xabar_id: int) -> None:
    init()
    with ulan() as c:
        c.execute("UPDATE xabarlar SET tg_yuborildi=1 WHERE id=?", (xabar_id,))


def sotuvchi_oxirgi_suhbati(sotuvchi_id: int) -> dict | None:
    """Sotuvchining eng so'nggi faol suhbati — Telegramdan javob yozish uchun."""
    init()
    with ulan() as c:
        r = c.execute(
            "SELECT sh.id, sh.sorov_id, sr.matn sorov_matni"
            " FROM suhbatlar sh JOIN sorovlar sr ON sr.id = sh.sorov_id"
            " WHERE sh.sotuvchi_id=? ORDER BY sh.yangilandi DESC, sh.id DESC"
            " LIMIT 1", (sotuvchi_id,)).fetchone()
    return dict(r) if r else None


def tg_holat() -> dict:
    """Telegram bog'lanishi bo'yicha qisqa hisobot (tashxis uchun)."""
    init()
    now = time.time()
    with ulan() as c:
        ulangan = c.execute("SELECT COUNT(*) n FROM sotuvchilar"
                            " WHERE telegram_id IS NOT NULL").fetchone()["n"]
        sotuvchilar = c.execute("SELECT COUNT(*) n FROM sotuvchilar").fetchone()["n"]
        kutayotgan = c.execute(
            "SELECT COUNT(*) n FROM yuborishlar y"
            " JOIN sorovlar s ON s.id=y.sorov_id"
            " JOIN sotuvchilar t ON t.id=y.sotuvchi_id"
            " WHERE y.xabar=0 AND t.telegram_id IS NOT NULL"
            "   AND s.yopiladi > ?", (now,)).fetchone()["n"]
        yuborilgan = c.execute("SELECT COUNT(*) n FROM yuborishlar"
                               " WHERE xabar=1").fetchone()["n"]
        ochiq = c.execute("SELECT COUNT(*) n FROM sorovlar"
                          " WHERE yopiladi > ?", (now,)).fetchone()["n"]
        # Kim ulangan va U NIMA SOTADI — xabar kelmasligining eng ko'p
        # uchraydigan sababi shu: sotuvchining yo'nalishi so'rovga mos
        # kelmaydi. Buni ko'rmasdan sabab topib bo'lmaydi.
        kimlar = [dict(r) for r in c.execute(
            "SELECT id, nom, nima_sotadi, qismlar, yonalishlar, tuman"
            " FROM sotuvchilar WHERE telegram_id IS NOT NULL")]
    return {"sotuvchilar": sotuvchilar, "telegramga_ulangan": ulangan,
            "ochiq_sorov": ochiq, "tg_kutayotgan": kutayotgan,
            "tg_yuborilgan": yuborilgan, "ulanganlar": kimlar}


# ── FTS5 INDEKSI ─────────────────────────────────────────────────────────────

def fts_yoz(qatorlar: list[tuple[int, str, str]]) -> None:
    """(elon_id, normallashtirilgan matn, teglar) — indeksga yozadi."""
    if not FTS_BOR or not qatorlar:
        return
    try:
        with ulan() as c:
            c.executemany("DELETE FROM elonlar_fts WHERE rowid=?",
                          [(i,) for i, _, _ in qatorlar])
            c.executemany("INSERT INTO elonlar_fts (rowid, norm, teg)"
                          " VALUES (?,?,?)", qatorlar)
    except sqlite3.OperationalError as e:
        # Indeks yozilmasa ham TAHLIL YO'QOLMASIN. Ilgari shu yerdagi
        # xato butun tahlilni to'xtatib, 1 533 e'lonlik ishni behuda
        # qilgan edi (2026-08-01).
        print(f"  [fts] indeks yozilmadi: {e}")


def _fts_token(s: str) -> str:
    """FTS5 uchun xavfsiz token."""
    t = "".join(ch if ch.isalnum() else " " for ch in s).strip()
    return f'"{t}"' if t else ""


def fts_nomzodlar(teglar: list[str], sozlar: list[str],
                  limit: int = 4000) -> list[int]:
    """Indeksdan nomzod e'lon id'larini oladi.

    Aniq ballash Python tomonida davom etadi — bu yerda faqat 100 000
    e'londan bir necha mingtasini ajratib olamiz.
    """
    if not FTS_BOR:
        return []
    bolaklar = []
    if teglar:
        ichi = " OR ".join(x for x in (_fts_token(t) for t in teglar) if x)
        if ichi:
            bolaklar.append(f"teg:({ichi})")
    if sozlar:
        ichi = " OR ".join(x for x in (_fts_token(w) for w in sozlar) if x)
        if ichi:
            bolaklar.append(f"norm:({ichi})")
    if not bolaklar:
        return []
    # Teg bo'lsa u MAJBURIY (qism turi shart), so'zlar qo'shimcha.
    ifoda = bolaklar[0] if len(bolaklar) == 1 else f"{bolaklar[0]} OR {bolaklar[1]}"
    try:
        with ulan() as c:
            return [r["rowid"] for r in c.execute(
                "SELECT rowid FROM elonlar_fts WHERE elonlar_fts MATCH ?"
                " ORDER BY rank LIMIT ?", (ifoda, limit))]
    except sqlite3.OperationalError:
        return []


ERKIN_CHEGARA = 900          # bir so'rovda ballanadigan eng ko'p e'lon


_YANGI_KESH: dict = {"vaqt": 0.0, "n": 0, "royxat": []}


def yangi_elonlar(n: int = 12) -> list[dict]:
    """Eng yangi, rasmli va narxli e'lonlar — bosh sahifa uchun.

    Bosh sahifada haqiqiy tovar ko'rinishi kerak. Shartlar qat'iy:
    rasmi bor, narxi bor, sanasi bor. Rasmsiz yoki narxsiz karta
    bo'sh joy kabi ko'rinadi va sahifani yana shablonga qaytaradi.

    Har so'rovda bazani bezovta qilmaymiz — 2 daqiqalik kesh yetarli,
    e'lonlar undan tez o'zgarmaydi.
    """
    import time as _t
    if (_YANGI_KESH["royxat"] and _YANGI_KESH["n"] >= n
            and _t.time() - _YANGI_KESH["vaqt"] < 120):
        return _YANGI_KESH["royxat"][:n]
    init()
    with ulan() as c:
        # HAR KATEGORIYADAN ENG YANGISI — "ENG YANGI"NING O'ZI EMAS.
        #
        # 2026-08-04 o'lchov. Avval bu yerda oddiy `ORDER BY olindi DESC`
        # turardi va lentada 12 ta kartaning 12 tasi ham KOMPYUTER edi.
        # Sabab yig'uvchining ishlash tartibida: u kategoriyalarni
        # birma-bir aylanadi, shuning uchun "eng yangi" e'lonlar deyarli
        # har doim bitta kategoriyadan bo'ladi. Tekshirdim — eng yangi
        # 96, 240, 480, 1200 va hatto 3000 e'lonning HAMMASI bitta
        # yuqori kategoriyadan chiqdi. Ya'ni ro'yxatni kengaytirish
        # yordam bermaydi, so'rovni o'zgartirish kerak.
        #
        # Lenta bizning VITRINAMIZ. "Butun bozor bitta qidiruvda" degan
        # va'dani 12 ta kompyuter isbotlamaydi — 12 xil narsa isbotlaydi.
        #
        # `ROW_NUMBER() OVER (PARTITION BY ...)` har kategoriyadan eng
        # yangi 3 tasini beradi. O'lchandi: 0.45 s, kesh esa 120 s —
        # ya'ni har 2 daqiqada bir marta. Lenta sahifadan alohida
        # (`/api/yangi`) yuklanadi, demak sahifa ochilishini kutdirmaydi.
        rows = c.execute(
            "SELECT manba, nom, narx_som, havola, rasm, sana, kategoriya,"
            "       viloyat, shahar, tuman"
            "  FROM (SELECT manba, nom, narx_som, havola, rasm, sana,"
            "               kategoriya, viloyat, shahar, tuman, olindi,"
            "               ROW_NUMBER() OVER ("
            "                 PARTITION BY substr(kategoriya,1,"
            "                              instr(kategoriya||'/','/')-1)"
            "                 ORDER BY olindi DESC) rn"
            "          FROM elonlar"
            "         WHERE faol=1 AND rasm IS NOT NULL AND rasm<>''"
            "           AND narx_som IS NOT NULL AND narx_som > 0)"
            " WHERE rn <= 3"
            # `rn` bo'yicha saralash kategoriyalarni ARALASHTIRADI: avval
            # har kategoriyaning birinchisi, keyin ikkinchisi. Aks holda
            # lentada "2 ta avto, 2 ta bolalar, 2 ta uy" bo'lib juft-juft
            # turardi va yana bir xillik hissi qolardi.
            " ORDER BY rn, olindi DESC").fetchall()

    royxat = []
    korilgan = set()
    kat_soni: dict[str, int] = {}
    for r in rows:
        e = dict(r)
        nom = (e.get("nom") or "").strip()

        # 1. SAVOL — e'lon emas, suhbat.
        #    2026-08-04 da lentada "Тошкентда ким бор?" degan karta
        #    2 560 000 so'm narx bilan turgan edi. Bu kanaldagi oddiy
        #    xabar, uning ichidagi raqam esa narx emas.
        if nom.endswith("?") or nom.endswith("？"):
            continue

        # 2. NUSXA. O'sha bir e'lon kanalga qayta-qayta tashlanadi.
        #    Aziz suratida "Kozoynaklar likvidatsiyasi" ketma-ket ikki
        #    marta turardi — vitrina o'zini takrorlab ko'rsatardi.
        kalit = nom.casefold()[:60]
        if kalit in korilgan:
            continue
        korilgan.add(kalit)

        # 3. AQLDAN TASHQARI NARX. Yuqori chegara — telefon raqami yoki
        #    ID narx bo'lib olinganini tutadi ("Logistika Dispatcher
        #    kerak — 312 180 973 so'm"). Uy-joy 3 mlrd gacha chiqadi,
        #    shuning uchun chegara baland qo'yilgan: faqat aniq xatoni
        #    kesadi, haqiqiy qimmat tovarni emas.
        narx = e.get("narx_som") or 0
        if narx < 10_000 or narx > 4_000_000_000:
            continue

        # 4. XILMA-XILLIK. So'rov allaqachon har kategoriyadan 3 tadan
        #    beryapti, lekin filtrlardan keyin bir kategoriya ustunlik
        #    qilib qolmasin — ikkitadan ko'p olinmaydi.
        kat = (e.get("kategoriya") or "").split("/")[0].strip() or "?"
        if kat_soni.get(kat, 0) >= 2:
            continue
        kat_soni[kat] = kat_soni.get(kat, 0) + 1

        royxat.append(e)
        if len(royxat) >= n:
            break

    # Xilma-xillik sharti tufayli yetarli karta yig'ilmasa (masalan
    # yig'uvchi endigina ishga tushgan bo'lsa), shartni yumshatib
    # ro'yxatni to'ldiramiz. Bo'sh lenta eng yomon variant.
    if len(royxat) < n:
        for r in rows:
            if len(royxat) >= n:
                break
            e = dict(r)
            nom = (e.get("nom") or "").strip()
            narx = e.get("narx_som") or 0
            kalit = nom.casefold()[:60]
            if (not nom or nom.endswith(("?", "？")) or kalit in korilgan
                    or narx < 10_000 or narx > 4_000_000_000):
                continue
            korilgan.add(kalit)
            royxat.append(e)

    _YANGI_KESH.update({"vaqt": _t.time(), "n": n, "royxat": royxat})
    return royxat[:n]


def fts_erkin(sozlar: list[str], limit: int = ERKIN_CHEGARA) -> list[int]:
    """LUG'ATSIZ matn qidiruvi — indeksning o'zidan.

    2026-08-02 o'lchov: bazada 101 381 e'lon bor edi, lekin qidiruv
    faqat avtoqismni topardi. Sabab kraulerda emas: `qidir()` lug'at
    model yoki qism tanimasa darhol bo'sh qaytarardi, `lugat.py` esa
    faqat mashinani biladi. Ya'ni yig'ilgan ma'lumotning ~99% i
    ko'rinmasdi.

    Endi lug'at SHART emas, BONUS. Hech narsa tanilmasa shu funksiya
    ishlaydi. Uch bosqich: avval barcha so'z bor e'lonlar, keyin
    so'z boshi bo'yicha (chala yozilgan bo'lishi mumkin), oxirida
    kamida bitta so'z. Birinchi natija bergan bosqichda to'xtaydi —
    shuning uchun aniqroq javob har doim oldinda.

    Faqat rowid olinadi. `norm` ustuni ham qaytarilardi (matnni qayta
    normallashtirmaslik uchun), lekin 2 500 qator uchun katta matn
    ustunini o'qish qidiruvni 4 781 ms ga cho'zdi (2026-08-02, "kvartira").
    Sarlavhani normallashtirish undan arzonroq.
    """
    if not FTS_BOR or not sozlar:
        return []
    toklar = [t for t in (_fts_token(w) for w in sozlar) if t]
    if not toklar:
        return []
    prefiks = [t + "*" for t in toklar]
    urinishlar = []
    if len(toklar) > 1:
        urinishlar.append(" AND ".join(toklar))
        urinishlar.append(" AND ".join(prefiks))
    else:
        urinishlar.append(toklar[0])
        urinishlar.append(prefiks[0])
    urinishlar.append(" OR ".join(prefiks))
    for ifoda in urinishlar:
        try:
            with ulan() as c:
                idlar = [r["rowid"] for r in c.execute(
                    "SELECT rowid FROM elonlar_fts WHERE elonlar_fts MATCH ?"
                    " ORDER BY rank LIMIT ?", (f"norm:({ifoda})", limit))]
        except sqlite3.OperationalError:
            continue
        if idlar:
            return idlar
    return []


def elonlar_idlardan(idlar: list[int]) -> list[dict]:
    if not idlar:
        return []
    natija: list[dict] = []
    with ulan() as c:
        for i in range(0, len(idlar), 900):        # SQLite parametr chegarasi
            bolak = idlar[i:i + 900]
            belgi = ",".join("?" * len(bolak))
            natija.extend(dict(r) for r in c.execute(
                # `manba` SHART. Ilgari tanlanmasdi va sahifada har e'lon
                # "olx" deb belgilanardi — Telegramdan kelgani ham.
                # Xaridorga yolg'on manba ko'rsatish ishonchni buzadi
                # (2026-08-02).
                "SELECT id, manba, tashqi_id, nom, narx_som, narx_asl, holat,"
                " viloyat, shahar, tuman, sana, havola, rasm, biznes,"
                " qism_turi, sotuvchi_nomi, kategoriya, tan_modellar,"
                " tan_qismlar, tan_nom_qismlar"
                f" FROM elonlar WHERE faol=1 AND id IN ({belgi})", bolak))
    return natija


# ── UZOQ YIG'ISH: to'xtatib, davom ettirish ──────────────────────────────────

def atama_yoz(juftlar: list[tuple]) -> None:
    """(kalit, o'zbekcha, ruscha) juftliklarini saqlaydi."""
    if not juftlar:
        return
    init()
    with ulan() as c:
        c.executemany("INSERT OR IGNORE INTO atamalar (kalit, uz, ru)"
                      " VALUES (?,?,?)", juftlar)


_ATAMA_KESH: dict = {"vaqt": 0.0, "xarita": {}}


def atama_xaritasi() -> dict:
    """`{o'zbekcha: ruscha, ruscha: o'zbekcha}` — ikki tomonlama."""
    import time as _t
    if _ATAMA_KESH["xarita"] and _t.time() - _ATAMA_KESH["vaqt"] < 600:
        return _ATAMA_KESH["xarita"]
    init()
    xarita: dict[str, str] = {}
    with ulan() as c:
        for r in c.execute("SELECT uz, ru FROM atamalar"):
            xarita[r["uz"].lower()] = r["ru"]
            xarita[r["ru"].lower()] = r["uz"]
    _ATAMA_KESH.update(vaqt=_t.time(), xarita=xarita)
    return xarita


def yigish_holati_ol(kategoriya: str, viloyat: str) -> dict:
    init()
    with ulan() as c:
        r = c.execute("SELECT * FROM yigish_holati WHERE kategoriya=? AND viloyat=?",
                      (kategoriya, viloyat)).fetchone()
    return dict(r) if r else {"kategoriya": kategoriya, "viloyat": viloyat,
                              "sahifa": 0, "tugadi": 0, "topildi": 0}


def yigish_holati_yoz(kategoriya: str, viloyat: str, sahifa: int,
                      tugadi: bool, topildi: int) -> None:
    init()
    with ulan() as c:
        c.execute(
            "INSERT INTO yigish_holati (kategoriya, viloyat, sahifa, tugadi,"
            " topildi, vaqt) VALUES (?,?,?,?,?,?)"
            " ON CONFLICT(kategoriya, viloyat) DO UPDATE SET"
            "   sahifa=excluded.sahifa, tugadi=excluded.tugadi,"
            "   topildi=yigish_holati.topildi+excluded.topildi,"
            "   vaqt=excluded.vaqt",
            (kategoriya, viloyat, sahifa, int(tugadi), topildi, time.time()))


def yigish_hisoboti() -> dict:
    init()
    with ulan() as c:
        r = c.execute(
            "SELECT COUNT(*) juft, SUM(tugadi) tugagan, SUM(topildi) topildi"
            " FROM yigish_holati").fetchone()
    return {"juftlar": r["juft"] or 0, "tugagan": r["tugagan"] or 0,
            "topildi": r["topildi"] or 0}


def yigishni_boshdan() -> None:
    """Hammasini qaytadan yig'ish uchun holatni tozalaydi."""
    init()
    with ulan() as c:
        c.execute("DELETE FROM yigish_holati")


def xabar_belgila(yuborish_id: int) -> None:
    init()
    with ulan() as c:
        c.execute("UPDATE yuborishlar SET xabar=1 WHERE id=?", (yuborish_id,))


def sorov_ochiqmi(sorov_id: int) -> dict | None:
    init()
    now = time.time()
    with ulan() as c:
        r = c.execute(
            "SELECT * FROM sorovlar WHERE id=? AND yopiladi > ?"
            "  AND holat IN ('yangi','yuborildi','javob_bor')",
            (sorov_id, now)).fetchone()
    return dict(r) if r else None


def javob_berilganmi(sorov_id: int, sotuvchi_id: int) -> bool:
    init()
    with ulan() as c:
        return bool(c.execute(
            "SELECT 1 FROM javoblar WHERE sorov_id=? AND sotuvchi=? LIMIT 1",
            (sorov_id, str(sotuvchi_id))).fetchone())


def yuborilgan_soni(sorov_id: int) -> int:
    init()
    with ulan() as c:
        return c.execute("SELECT COUNT(*) n FROM yuborishlar WHERE sorov_id=?",
                         (sorov_id,)).fetchone()["n"]


_TOLQIN_OXIRGI = {"vaqt": 0.0}


def ochiq_sorovlarni_yurit() -> None:
    """Ochiq so'rovlarning keyingi to'lqinini ochadi (dangasa jadval).

    CHEKLANGAN: har sahifa so'rovida yurgizilsa, ochiq so'rovlar soniga
    ko'paytirilgan yozuv oqimi hosil bo'ladi va qidiruv sekinlashadi
    (2026-08-01 da o'lchandi). To'lqin jadvali daqiqalar bilan
    o'lchanadi — 20 soniyada bir marta tekshirish yetarli.
    """
    if time.time() - _TOLQIN_OXIRGI["vaqt"] < 20:
        return
    _TOLQIN_OXIRGI["vaqt"] = time.time()
    init()
    now = time.time()
    with ulan() as c:
        idlar = [r["id"] for r in c.execute(
            "SELECT id FROM sorovlar WHERE holat IN ('yangi','yuborildi')"
            " AND yopiladi > ?", (now,))]
    for i in idlar:
        tolqin_yubor(i)


def sotuvchi_sorovlari(sotuvchi_id: int, limit: int = 20) -> list[dict]:
    """Shu sotuvchiga tegishli OCHIQ so'rovlar.

    Faqat o'z yo'nalishi va hududi — aks holda spam bo'lib, uchinchi kuni
    tashlab ketadi."""
    init()
    now = time.time()
    # Vaqti kelgan to'lqinlarni ochamiz — alohida jadval xizmati kerak emas.
    ochiq_sorovlarni_yurit()

    with ulan() as c:
        s = c.execute("SELECT * FROM sotuvchilar WHERE id=?",
                      (sotuvchi_id,)).fetchone()
        if not s:
            return []

        # Endi moslik shu yerda emas, YUBORISHDA hal qilinadi.
        # Sotuvchi faqat unga ATAYLAB yuborilgan so'rovni ko'radi.
        qatorlar = c.execute(
            "SELECT sr.* FROM sorovlar sr"
            " JOIN yuborishlar y ON y.sorov_id = sr.id"
            " WHERE y.sotuvchi_id = ?"
            "   AND sr.holat IN ('yangi','yuborildi','javob_bor')"
            "   AND sr.yopiladi > ?"
            " ORDER BY sr.id DESC LIMIT 200", (sotuvchi_id, now)).fetchall()

        javob_berilgan = {r["sorov_id"] for r in c.execute(
            "SELECT sorov_id FROM javoblar WHERE sotuvchi=?",
            (str(sotuvchi_id),))}

    natija = []
    for r in qatorlar:
        if r["id"] in javob_berilgan:
            continue
        # Hudud: bir xil tuman bo'lsa albatta, aks holda ham ko'rsatamiz
        # (lekin pastroqda) — chunki yetkazib berish mumkin
        yaqin = bool(r["tuman"] and s["tuman"] and r["tuman"] == s["tuman"])
        ochiq = dict(r)
        ochiq.pop("aloqa", None)  # xaridor raqami sotuvchiga ochilmaydi
        natija.append({**ochiq, "yaqin": yaqin})

    natija.sort(key=lambda x: (not x["yaqin"], -x["id"]))
    return natija[:limit]


def sotuvchi_talabi(sotuvchi_id: int, kun: int = 7) -> dict:
    """Shu sotuvchining yo'nalishida qancha qidiruv bo'lgani.

    NEGA BU KERAK (2026-08-02):
    Kabinet ishlaydi, lekin unda QAYTIB KELISH SABABI yo'q. Sotuvchi
    kirsa va so'rov bo'lmasa, bo'sh sahifa ko'radi va boshqa qaytmaydi.

    Bizda esa javob bor: har qidiruv `qidiruvlar` jadvaliga yoziladi.
    "Bu hafta sizning yo'nalishingizda 12 marta qidirishdi, 3 tasi
    javobsiz qoldi" degan jumla bo'sh sahifadan cheksiz kuchli. U bir
    vaqtda ikki ish qiladi: sotuvchini qaytaradi va bizga qaysi
    yo'nalishda taklif yetishmayotganini ko'rsatadi.

    Raqamlar HAQIQIY. Bo'rttirilmaydi: bitta yolg'on son butun ishonchni
    buzadi va sotuvchi buni birinchi kuniyoq sezadi.
    """
    init()
    chegara = time.time() - kun * 86400
    with ulan() as c:
        s = c.execute("SELECT qismlar, yonalishlar, tuman FROM sotuvchilar"
                      " WHERE id=?", (sotuvchi_id,)).fetchone()
        if not s:
            return {}
        teglar = {x for x in ((s["qismlar"] or "").split(",")
                              + (s["yonalishlar"] or "").split(",")) if x}
        if not teglar:
            return {}

        qatorlar = c.execute(
            "SELECT sorov, qismlar, tuman, natija_soni FROM qidiruvlar"
            " WHERE vaqt > ?", (chegara,)).fetchall()

        # Sotuvchiga yuborilgan va JAVOBSIZ qolgan so'rovlar — eng og'riqli
        # raqam. "Sizga keldi, siz javob bermadingiz" deb yuzlashtirmaymiz;
        # shunchaki yo'nalishdagi javobsiz talabni ko'rsatamiz.
        javobsiz = c.execute(
            "SELECT COUNT(*) n FROM sorovlar sr"
            " WHERE sr.yaratildi > ?"
            "   AND NOT EXISTS (SELECT 1 FROM javoblar j"
            "                   WHERE j.sorov_id = sr.id AND j.holat<>'yoq')",
            (chegara,)).fetchone()["n"]

    jami, shu_hududda = 0, 0
    namunalar: list[str] = []
    for r in qatorlar:
        q = {x for x in (r["qismlar"] or "").split(",") if x}
        if not (q & teglar):
            continue
        jami += 1
        if s["tuman"] and r["tuman"] == s["tuman"]:
            shu_hududda += 1
        matn = (r["sorov"] or "").strip()
        if matn and matn not in namunalar and len(namunalar) < 5:
            namunalar.append(matn[:60])

    return {"kun": kun, "jami": jami, "hududda": shu_hududda,
            "javobsiz": javobsiz, "namunalar": namunalar,
            "tuman": s["tuman"] or ""}


def javob_yoz(sorov_id: int, sotuvchi_id: int, holat: str,
              narx: int | None, izoh: str = "", rasm: str = "") -> int | None:
    init()
    now = time.time()
    with ulan() as c:
        cur = c.execute(
            "INSERT INTO javoblar (sorov_id, sotuvchi, holat, narx, izoh, vaqt)"
            " VALUES (?,?,?,?,?,?)",
            (sorov_id, str(sotuvchi_id), holat, narx, izoh, now))
        javob_id = cur.lastrowid
        c.execute("UPDATE sotuvchilar SET javob_soni = javob_soni + 1"
                  " WHERE id=?", (sotuvchi_id,))
        if holat in {"bor", "oxshash"}:
            c.execute("UPDATE sorovlar SET holat='javob_bor' WHERE id=?",
                      (sorov_id,))
            suhbat = c.execute(
                "INSERT INTO suhbatlar (sorov_id, javob_id, sotuvchi_id, yaratildi, yangilandi)"
                " VALUES (?,?,?,?,?)",
                (sorov_id, javob_id, sotuvchi_id, now, now))
            suhbat_id = suhbat.lastrowid
            if izoh or rasm:
                c.execute(
                    "INSERT INTO xabarlar (suhbat_id, rol, matn, rasm, vaqt,"
                    " xaridor_oqidi, sotuvchi_oqidi) VALUES (?,?,?,?,?,?,?)",
                    (suhbat_id, "sotuvchi", izoh, rasm, now, 0, 1))
            return suhbat_id
        return None


def sorov_javoblari(sorov_id: int) -> list[dict]:
    """Xaridorga kelgan ijobiy javoblar, aloqa raqamlarisiz.

    Taklif, rasm va yozishma OBER ichida qoladi. Xaridor ham, sotuvchi
    ham bir-birining telefon raqamini API orqali olmaydi.
    """
    init()
    with ulan() as c:
        rows = c.execute(
            "SELECT j.*, s.nom, s.tuman FROM javoblar j"
            " LEFT JOIN sotuvchilar s ON s.id = CAST(j.sotuvchi AS INTEGER)"
            " WHERE j.sorov_id=? AND j.holat IN ('bor','oxshash')"
            " ORDER BY j.narx IS NULL, j.narx", (sorov_id,)).fetchall()
    return [dict(r) for r in rows]


def raqam_ochildi(javob_id: int) -> None:
    """Xaridor raqamni ochdi — bu bizning eng kuchli natija belgisi.

    Bitim bizdan tashqarida bo'ladi, shuning uchun uni ko'ra olmaymiz.
    Raqam ochilishi esa "odam qo'ng'iroq qilmoqchi" degani — konversiya
    o'lchovi shu."""
    init()
    with ulan() as c:
        ustunlar = {r["name"] for r in c.execute("PRAGMA table_info(javoblar)")}
        if "raqam_ochildi" not in ustunlar:
            c.execute("ALTER TABLE javoblar ADD COLUMN"
                      " raqam_ochildi INTEGER NOT NULL DEFAULT 0")
        c.execute("UPDATE javoblar SET raqam_ochildi = raqam_ochildi + 1"
                  " WHERE id=?", (javob_id,))


def _vaqt_matni(vaqt: float | None) -> str:
    if not vaqt:
        return ""
    return time.strftime("%H:%M", time.localtime(vaqt))


def sorov_takliflari(sorov_id: int) -> dict:
    """Xaridor uchun takliflar lentasi; aloqa raqamlari ataylab olinmaydi."""
    init()
    with ulan() as c:
        sorov = c.execute(
            "SELECT id, matn, tuman, byudjet, holat, yaratildi FROM sorovlar WHERE id=?",
            (sorov_id,)).fetchone()
        if not sorov:
            return {"sorov": None, "takliflar": []}
        rows = c.execute(
            "SELECT j.id javob_id, j.holat, j.narx, j.izoh, j.tanlandi, j.vaqt,"
            " s.id sotuvchi_id, s.nom, s.tuman, sh.id suhbat_id"
            " FROM javoblar j"
            " LEFT JOIN sotuvchilar s ON s.id=CAST(j.sotuvchi AS INTEGER)"
            " LEFT JOIN suhbatlar sh ON sh.javob_id=j.id"
            " WHERE j.sorov_id=? AND j.holat IN ('bor','oxshash')"
            " ORDER BY j.tanlandi DESC, j.vaqt DESC", (sorov_id,)).fetchall()
        takliflar = []
        for row in rows:
            d = dict(row)
            oxirgi = None
            oqilmagan = 0
            if d["suhbat_id"]:
                oxirgi = c.execute(
                    "SELECT rol, matn, rasm, vaqt FROM xabarlar"
                    " WHERE suhbat_id=? ORDER BY id DESC LIMIT 1",
                    (d["suhbat_id"],)).fetchone()
                oqilmagan = c.execute(
                    "SELECT COUNT(*) n FROM xabarlar WHERE suhbat_id=?"
                    " AND rol='sotuvchi' AND xaridor_oqidi=0",
                    (d["suhbat_id"],)).fetchone()["n"]
            d["oxirgi_xabar"] = ((oxirgi["matn"] or "Rasm yuborildi")
                                  if oxirgi else (d["izoh"] or "Taklif yuborildi"))
            d["oxirgi_rasm"] = oxirgi["rasm"] if oxirgi else ""
            d["oxirgi_vaqt"] = _vaqt_matni(
                oxirgi["vaqt"] if oxirgi else d["vaqt"])
            d["oqilmagan"] = oqilmagan
            takliflar.append(d)
        takliflar.sort(key=lambda x: (-int(x["tanlandi"] or 0),
                                      -int(x["oqilmagan"] or 0),
                                      -float(x["vaqt"] or 0)))
    return {"sorov": dict(sorov), "takliflar": takliflar}


def sotuvchi_suhbatlari(sotuvchi_id: int) -> list[dict]:
    init()
    with ulan() as c:
        rows = c.execute(
            "SELECT sh.id suhbat_id, sh.sorov_id, sh.javob_id, sh.yangilandi,"
            " sr.matn sorov_matni, sr.tuman, sr.ism xaridor_ism, j.narx, j.tanlandi"
            " FROM suhbatlar sh JOIN sorovlar sr ON sr.id=sh.sorov_id"
            " JOIN javoblar j ON j.id=sh.javob_id"
            " WHERE sh.sotuvchi_id=? ORDER BY sh.yangilandi DESC",
            (sotuvchi_id,)).fetchall()
        natija = []
        for row in rows:
            d = dict(row)
            oxirgi = c.execute(
                "SELECT rol, matn, rasm, vaqt FROM xabarlar"
                " WHERE suhbat_id=? ORDER BY id DESC LIMIT 1",
                (d["suhbat_id"],)).fetchone()
            d["oxirgi_xabar"] = ((oxirgi["matn"] or "Rasm yuborildi")
                                  if oxirgi else "Taklif yuborildi")
            d["oxirgi_rasm"] = oxirgi["rasm"] if oxirgi else ""
            d["oxirgi_vaqt"] = _vaqt_matni(oxirgi["vaqt"] if oxirgi else d["yangilandi"])
            d["oqilmagan"] = c.execute(
                "SELECT COUNT(*) n FROM xabarlar WHERE suhbat_id=?"
                " AND rol='xaridor' AND sotuvchi_oqidi=0",
                (d["suhbat_id"],)).fetchone()["n"]
            natija.append(d)
    return natija


def bildirishnomalar_ol(rol: str, actor_id: int, limit: int = 20) -> dict:
    """Rolga tegishli o‘qilmagan ichki xabarlar.

    Bildirishnoma alohida nusxa bo‘lib saqlanmaydi: xabar — yagona haqiqat
    manbasi. Shu sabab chat ochilganda badge ham darhol yo‘qoladi.
    """
    if rol not in {"xaridor", "sotuvchi"} or actor_id <= 0:
        return {"jami": 0, "bildirishnomalar": []}
    init()
    if rol == "xaridor":
        actor_shart = "sh.sorov_id=?"
        unread_shart = "x.rol='sotuvchi' AND x.xaridor_oqidi=0"
    else:
        actor_shart = "sh.sotuvchi_id=?"
        unread_shart = "x.rol='xaridor' AND x.sotuvchi_oqidi=0"
    asos = (
        " FROM xabarlar x JOIN suhbatlar sh ON sh.id=x.suhbat_id"
        " JOIN sorovlar sr ON sr.id=sh.sorov_id"
        " JOIN javoblar j ON j.id=sh.javob_id"
        " JOIN sotuvchilar s ON s.id=sh.sotuvchi_id"
        f" WHERE {actor_shart} AND {unread_shart}"
    )
    with ulan() as c:
        jami = c.execute("SELECT COUNT(*) n" + asos, (actor_id,)).fetchone()["n"]
        rows = c.execute(
            "SELECT x.id xabar_id, x.suhbat_id, x.matn, x.rasm, x.vaqt,"
            " sr.matn sorov_matni, sr.ism xaridor_ism, s.nom sotuvchi_nomi, j.narx" + asos +
            " ORDER BY x.id DESC LIMIT ?",
            (actor_id, max(1, min(limit, 50)))).fetchall()
    bildirishnomalar = []
    for row in rows:
        d = dict(row)
        # 2026-08-08: sarlavha ROLLI bo'ladi — chatdagi yorliqlar bilan bir xil.
        # Xaridor ko'rsa: "Sotuvchi · Nexia Usta"; sotuvchi ko'rsa: "Xaridor · Azizdan
        # yangi xabar" (ism bo'lsa) yoki "Xaridordan yangi xabar".
        if rol == "xaridor":
            d["sarlavha"] = (f"Sotuvchi · {d['sotuvchi_nomi']}"
                             if d.get("sotuvchi_nomi") else "Sotuvchi")
        else:
            d["sarlavha"] = (f"Xaridor · {d['xaridor_ism']}dan yangi xabar"
                             if d.get("xaridor_ism")
                             else "Xaridordan yangi xabar")
        d["matn"] = d["matn"] or "Rasm yuborildi"
        d["vaqt_matni"] = _vaqt_matni(d["vaqt"])
        bildirishnomalar.append(d)
    return {"jami": jami, "bildirishnomalar": bildirishnomalar}


def bildirishnomalar_oqildi(rol: str, actor_id: int) -> int:
    """Faqat actorning o‘z suhbatlaridagi qarshi tomon xabarlarini o‘qilgan qiladi."""
    if rol not in {"xaridor", "sotuvchi"} or actor_id <= 0:
        return 0
    init()
    with ulan() as c:
        if rol == "xaridor":
            cur = c.execute(
                "UPDATE xabarlar SET xaridor_oqidi=1 WHERE rol='sotuvchi'"
                " AND xaridor_oqidi=0 AND suhbat_id IN"
                " (SELECT id FROM suhbatlar WHERE sorov_id=?)", (actor_id,))
        else:
            cur = c.execute(
                "UPDATE xabarlar SET sotuvchi_oqidi=1 WHERE rol='xaridor'"
                " AND sotuvchi_oqidi=0 AND suhbat_id IN"
                " (SELECT id FROM suhbatlar WHERE sotuvchi_id=?)", (actor_id,))
        return cur.rowcount


def suhbat_ol(suhbat_id: int, rol: str, actor_id: int) -> dict | None:
    init()
    with ulan() as c:
        info = c.execute(
            "SELECT sh.id, sh.sorov_id, sh.sotuvchi_id, sh.javob_id,"
            " sr.matn sorov_matni, sr.tuman, sr.ism xaridor_ism, j.narx, j.tanlandi,"
            " s.nom sotuvchi_nomi, s.aloqa sotuvchi_aloqa,"
            " s.oxirgi_faol s_faol, s.vaqt_yashir s_yashir,"
            " sr.oxirgi_faol x_faol, sr.vaqt_yashir x_yashir"
            " FROM suhbatlar sh JOIN sorovlar sr ON sr.id=sh.sorov_id"
            " JOIN javoblar j ON j.id=sh.javob_id"
            " JOIN sotuvchilar s ON s.id=sh.sotuvchi_id WHERE sh.id=?",
            (suhbat_id,)).fetchone()
        if not info:
            return None
        if rol == "sotuvchi" and info["sotuvchi_id"] != actor_id:
            return None
        if rol == "xaridor" and info["sorov_id"] != actor_id:
            return None
        if rol == "sotuvchi":
            c.execute("UPDATE xabarlar SET sotuvchi_oqidi=1"
                      " WHERE suhbat_id=? AND rol='xaridor'", (suhbat_id,))
        else:
            c.execute("UPDATE xabarlar SET xaridor_oqidi=1"
                      " WHERE suhbat_id=? AND rol='sotuvchi'", (suhbat_id,))
        c.execute(
            f"UPDATE {'sorovlar' if rol == 'xaridor' else 'sotuvchilar'}"
            " SET oxirgi_faol=? WHERE id=?", (time.time(), actor_id))
        rows = c.execute(
            "SELECT id, rol, matn, rasm, joy, vaqt FROM xabarlar"
            " WHERE suhbat_id=? ORDER BY id", (suhbat_id,)).fetchall()
    xabarlar = []
    for row in rows:
        d = dict(row)
        d["vaqt_matni"] = _vaqt_matni(d["vaqt"])
        xabarlar.append(d)

    s = dict(info)
    # SUHBATDOSH HOLATI — kim bilan gaplashayotganini ko'rish uchun.
    # O'z holatingiz emas, QARSHI TOMONNIKI ko'rsatiladi.
    if rol == "xaridor":
        s["suhbatdosh"] = s.get("sotuvchi_nomi") or "Sotuvchi"
        s["suhbatdosh_holati"] = holat_matni(s.pop("s_faol", None),
                                             s.pop("s_yashir", 0))
        s.pop("x_faol", None); s.pop("x_yashir", None)
        s["men_yashirdim"] = bool(info["x_yashir"])
    else:
        s["suhbatdosh"] = "Xaridor"
        s["suhbatdosh_holati"] = holat_matni(s.pop("x_faol", None),
                                             s.pop("x_yashir", 0))
        s.pop("s_faol", None); s.pop("s_yashir", None)
        s["men_yashirdim"] = bool(info["s_yashir"])
        s.pop("sotuvchi_aloqa", None)      # o'z raqamini qaytarish shart emas
    return {"suhbat": s, "xabarlar": xabarlar}


# ── ONLAYN HOLAT ─────────────────────────────────────────────────────────────
# Chatda odam tirikligi ko'rinishi kerak: "hozir onlayn" yoki "5 daqiqa
# oldin". Xohlagan odam buni yashira oladi (Telegramdagi kabi).

def faollik_belgila(rol: str, actor_id: int) -> None:
    if rol not in {"xaridor", "sotuvchi"} or not actor_id:
        return
    init()
    jadval = "sorovlar" if rol == "xaridor" else "sotuvchilar"
    with ulan() as c:
        c.execute(f"UPDATE {jadval} SET oxirgi_faol=? WHERE id=?",
                  (time.time(), actor_id))


def vaqt_yashirish(rol: str, actor_id: int, yashir: bool) -> None:
    init()
    jadval = "sorovlar" if rol == "xaridor" else "sotuvchilar"
    with ulan() as c:
        c.execute(f"UPDATE {jadval} SET vaqt_yashir=? WHERE id=?",
                  (int(bool(yashir)), actor_id))


def holat_matni(oxirgi: float | None, yashirilgan: int | None) -> str:
    """'hozir onlayn' | '5 daqiqa oldin' | 'yaqinda' (yashirilgan bo'lsa)."""
    if yashirilgan:
        return "yaqinda"
    if not oxirgi:
        return ""
    farq = time.time() - float(oxirgi)
    if farq < 90:
        return "hozir onlayn"
    if farq < 3600:
        return f"{int(farq // 60)} daqiqa oldin"
    if farq < 86400:
        return f"{int(farq // 3600)} soat oldin"
    return f"{int(farq // 86400)} kun oldin"


def suhbat_xabar_yoz(suhbat_id: int, rol: str, actor_id: int,
                     matn: str = "", rasm: str = "",
                     joy: str = "") -> int | None:
    if rol not in {"xaridor", "sotuvchi"} or (not matn and not rasm and not joy):
        return None
    init()
    now = time.time()
    with ulan() as c:
        info = c.execute(
            "SELECT sorov_id, sotuvchi_id FROM suhbatlar WHERE id=?",
            (suhbat_id,)).fetchone()
        if not info:
            return None
        if rol == "sotuvchi" and info["sotuvchi_id"] != actor_id:
            return None
        if rol == "xaridor" and info["sorov_id"] != actor_id:
            return None
        cur = c.execute(
            "INSERT INTO xabarlar (suhbat_id, rol, matn, rasm, joy, vaqt,"
            " xaridor_oqidi, sotuvchi_oqidi) VALUES (?,?,?,?,?,?,?,?)",
            (suhbat_id, rol, matn, rasm, joy, now,
             int(rol == "xaridor"), int(rol == "sotuvchi")))
        c.execute("UPDATE suhbatlar SET yangilandi=? WHERE id=?", (now, suhbat_id))
        jadval = "sorovlar" if rol == "xaridor" else "sotuvchilar"
        c.execute(f"UPDATE {jadval} SET oxirgi_faol=? WHERE id=?",
                  (now, actor_id))
        return cur.lastrowid


def taklif_tanla(sorov_id: int, javob_id: int) -> int | None:
    init()
    with ulan() as c:
        row = c.execute(
            "SELECT sh.id FROM javoblar j JOIN suhbatlar sh ON sh.javob_id=j.id"
            " WHERE j.id=? AND j.sorov_id=? AND j.holat IN ('bor','oxshash')",
            (javob_id, sorov_id)).fetchone()
        if not row:
            return None
        c.execute("UPDATE javoblar SET tanlandi=0 WHERE sorov_id=?", (sorov_id,))
        c.execute("UPDATE javoblar SET tanlandi=1 WHERE id=?", (javob_id,))
        c.execute("UPDATE sorovlar SET holat='tanlandi' WHERE id=?", (sorov_id,))
        return row["id"]


def suhbat_demo_holat() -> dict:
    """Faqat lokal vizual sinov sahifasini ochish uchun demo identifikatorlari."""
    init()
    with ulan() as c:
        row = c.execute(
            "SELECT sr.id sorov_id, sr.token sorov_token,"
            " sh.sotuvchi_id, sh.id suhbat_id"
            " FROM sorovlar sr JOIN suhbatlar sh ON sh.sorov_id=sr.id"
            " WHERE sr.aloqa='demo-chat-buyer' ORDER BY sh.id LIMIT 1").fetchone()
    return dict(row) if row else {}


def qidiruv_yoz(sorov: str, natija: dict, tuman: str = "") -> None:
    """Har qidiruvni yozadi. Xato bo'lsa ham qidiruvni to'xtatmaydi."""
    try:
        init()
        t = natija.get("tushunildi") or {}
        with ulan() as c:
            c.execute(
                "INSERT INTO qidiruvlar (sorov, modellar, qismlar, tuman,"
                " natija_soni, kesildi, narx_min, narx_max, vaqt)"
                " VALUES (?,?,?,?,?,?,?,?,?)",
                (sorov, ",".join(t.get("modellar") or []),
                 ",".join(t.get("qismlar") or []), tuman,
                 natija.get("jami", 0), natija.get("kesildi_model", 0),
                 natija.get("narx_min"), natija.get("narx_max"), time.time()))
    except Exception:                    # noqa: BLE001 — yozuv muhim, lekin
        pass                             # qidiruvdan muhimroq emas


def sorov_yoz(matn: str, tuman: str, aloqa: str,
              byudjet: int | None, modellar: list, qismlar: list,
              yonalishlar: list | None = None, ism: str | None = None) -> int:
    """So'rovni saqlaydi. `ism` ixtiyoriy (2026-08-08) — xaridor
    yozsa, sotuvchi chatda 'Xaridor · Ism' deb ko'radi."""
    init()
    import secrets
    now = time.time()
    token = secrets.token_urlsafe(32)
    with ulan() as c:
        cur = c.execute(
            "INSERT INTO sorovlar (matn, modellar, qismlar, tuman, byudjet,"
            " aloqa, holat, yaratildi, yopiladi, yonalishlar, ism, token)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (matn, ",".join(modellar), ",".join(qismlar), tuman, byudjet,
             aloqa, "yangi", now, now + 2 * 3600,
             ",".join(yonalishlar or []), ism or None, token))
        return cur.lastrowid


def sikl_boshlash(manba: str) -> str:
    """Yig‘ish sikli uchun noyob belgi yaratadi.

    Belgini ko‘rgan e’lonlarga yozamiz. Faqat to‘liq sikl muvaffaqiyatli
    tugagach, shu belgini olmagan e’lonlarning `korilmadi` soni oshadi.
    """
    if not manba or not manba.replace("_", "").replace("-", "").isalnum():
        raise ValueError("manba kaliti noto‘g‘ri")
    return f"{manba}-{time.time_ns()}"


def sikl_yakunla(manba: str, sikl: str, toliq: bool = False) -> dict:
    """Ko‘rilmagan e’lonlarni xavfsiz hisoblaydi.

    Sinov/partial siklda faqat ko‘rilganlar qayta faollashadi. To‘liq siklda
    ko‘rinmagan faol e’lon bir pog‘ona oshadi va ketma-ket 3 marta yo‘qolsa
    `faol=0` bo‘ladi. Nol natijali sikl hech qachon nofaollashtirmaydi.
    """
    init()
    with ulan() as c:
        korildi = c.execute(
            "SELECT COUNT(*) n FROM elonlar WHERE manba=? AND oxirgi_sikl=?",
            (manba, sikl)).fetchone()["n"]
        natija = {"korildi": korildi, "otkazildi": 0, "nofaol_qilindi": 0,
                  "toliq": False}
        if not toliq or korildi == 0:
            return natija

        cur = c.execute(
            "UPDATE elonlar SET korilmadi=korilmadi+1 "
            "WHERE manba=? AND faol=1 AND COALESCE(oxirgi_sikl, '')<>?",
            (manba, sikl))
        natija["otkazildi"] = cur.rowcount
        cur = c.execute(
            "UPDATE elonlar SET faol=0 WHERE manba=? AND faol=1 AND korilmadi>=3",
            (manba,))
        natija["nofaol_qilindi"] = cur.rowcount
        natija["toliq"] = True
        return natija


def saqla(e: dict, sikl: str = "") -> str:
    """E'lonni yozadi.

    Qaytaradi: `yangi`, `yangilandi`, `qaytdi` yoki `ozgarmadi`.
    """
    init()
    now = time.time()
    with ulan() as c:
        eski = c.execute(
            "SELECT id, narx_som, rasm, tuman, shahar, qism_turi, tavsif,"
            " sotuvchi_id, sotuvchi_nomi, xususiyatlar, faol FROM elonlar"
            " WHERE manba=? AND tashqi_id=?",
            (e["manba"], e["tashqi_id"])).fetchone()

        if eski is None:
            c.execute("""
                INSERT INTO elonlar
                (manba, tashqi_id, nom, narx_som, narx_asl, valyuta, kelishiladi,
                 holat, viloyat, shahar, tuman, sana, havola, rasm, telefon, biznes,
                 qism_turi, tavsif, sotuvchi_id, sotuvchi_nomi, kategoriya,
                 xususiyatlar, olx_kategoriya,
                 olindi, faol, korilmadi, oxirgi_korildi, oxirgi_sikl)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
                e["manba"], e["tashqi_id"], e["nom"], e.get("narx_som"),
                e.get("narx_asl"), e.get("valyuta"), int(e.get("kelishiladi", 0)),
                e.get("holat"), e.get("viloyat"), e.get("shahar"), e.get("tuman"),
                e.get("sana"), e.get("havola"), e.get("rasm"), e.get("telefon"),
                int(e.get("biznes", 0)), e.get("qism_turi"), e.get("tavsif"),
                e.get("sotuvchi_id"), e.get("sotuvchi_nomi"),
                e.get("kategoriya"),
                e.get("xususiyatlar"), e.get("olx_kategoriya"), now,
                1, 0, now, sikl or None))
            if e.get("narx_som"):
                c.execute("INSERT INTO narx_tarix (manba, tashqi_id, narx_som, vaqt)"
                          " VALUES (?,?,?,?)",
                          (e["manba"], e["tashqi_id"], e["narx_som"], now))
            return "yangi"

        # Mavjud — narx o'zgarganmi yoki oldin nofaol bo'lganmi?
        ozgardi = e.get("narx_som") and e["narx_som"] != eski["narx_som"]
        qaytdi = not bool(eski["faol"])

        # YO'QOTMAYMIZ. E'lon sahifasidan olingan rasm/tuman ro'yxat
        # sahifasida bo'lmasligi mumkin — bo'sh qiymat bilan ustidan
        # yozib yuborsak, avval yig'ilgan mehnat yo'qoladi.
        for maydon in ("rasm", "tuman", "shahar", "qism_turi", "tavsif",
                       "sotuvchi_id", "sotuvchi_nomi"):
            if not e.get(maydon) and eski[maydon]:
                e[maydon] = eski[maydon]
        # Xususiyatlar bo'sh kelsa eskisini saqlaymiz
        if not e.get("xususiyatlar") or e.get("xususiyatlar") == "[]":
            try:
                e["xususiyatlar"] = eski["xususiyatlar"]
            except (IndexError, KeyError):
                pass

        # tan_qismlar NULLga qaytariladi: nom yoki qism_turi yangilangan
        # bo'lishi mumkin, demak tahlil qayta qilinishi kerak.
        c.execute("""UPDATE elonlar SET nom=?, narx_som=?, narx_asl=?, valyuta=?,
                     kelishiladi=?, holat=?, viloyat=?, shahar=?, tuman=?, sana=?,
                     havola=?, rasm=?, biznes=?, qism_turi=?, tavsif=?,
                     sotuvchi_id=?, sotuvchi_nomi=?,
                     kategoriya=COALESCE(?, kategoriya),
                     xususiyatlar=COALESCE(?, xususiyatlar),
                     olx_kategoriya=COALESCE(?, olx_kategoriya),
                     tan_qismlar=NULL,
                     olindi=?, faol=1, korilmadi=0, oxirgi_korildi=?,
                     oxirgi_sikl=COALESCE(?, oxirgi_sikl) WHERE id=?""", (
            e["nom"], e.get("narx_som"), e.get("narx_asl"), e.get("valyuta"),
            int(e.get("kelishiladi", 0)), e.get("holat"), e.get("viloyat"),
            e.get("shahar"), e.get("tuman"), e.get("sana"), e.get("havola"),
            e.get("rasm"), int(e.get("biznes", 0)), e.get("qism_turi"),
            e.get("tavsif"), e.get("sotuvchi_id"), e.get("sotuvchi_nomi"),
            e.get("kategoriya") or None,
            e.get("xususiyatlar") or None, e.get("olx_kategoriya") or None,
            now, now, sikl or None, eski["id"]))
        if ozgardi:
            c.execute("INSERT INTO narx_tarix (manba, tashqi_id, narx_som, vaqt)"
                      " VALUES (?,?,?,?)",
                      (e["manba"], e["tashqi_id"], e["narx_som"], now))
        if qaytdi:
            return "qaytdi"
        if ozgardi:
            return "yangilandi"
        return "ozgarmadi"


# ── OBER E'LONLARI — o'z marketplace (2026-08-06) ───────────────────────────
# Sotuvchi OBER'da o'z e'lonini joylashtiradi. E'lon `manba='ober'` bilan
# odatdagi `elonlar` jadvaliga tushadi — qidiruv, narx tarixi, filtr hammasi
# mavjud yo'ldan ishlaydi. `egasi` ustuni e'lon egasini (sotuvchilar.id)
# ko'rsatadi; faqat egasi tahrirlaydi va o'chiradi.

def _ober_narx(narx) -> int | None:
    """OBER e'lon narxini tozalaydi: '2 500 000' -> 2500000.

    Sotuvchi formada bo'shliq bilan yozadi; `int('2 500 000')`
    yiqiladi va narx tushib qolardi (2026-08-06 sinovda topildi).
    """
    if narx is None or narx == "":
        return None
    son = re.sub(r"[^\d]", "", str(narx))
    if not son:
        return None
    n = int(son)
    return n if 1_000 <= n <= 50_000_000_000 else None


def _toshkent_bugun() -> str:
    """Toshkent vaqtida bugungi sana (ISO `YYYY-MM-DD`).

    2026-08-07: server UTC edi — 19:00 UTC dan keyin (Toshkentda
    yarim tun bo'lgach) yangi e'lon "Kecha" bo'lib ko'rinardi.
    Toshkent UTC+5, DST yo'q (1991 dan beri) — qat'iy +5 soat.
    """
    import datetime as _dt
    now = _dt.datetime.now(_dt.timezone.utc) + _dt.timedelta(hours=5)
    return now.strftime("%Y-%m-%d")


def ober_elon_yoz(egasi: int, e: dict) -> int:
    """Sotuvchi o'z e'loni. `egasi` — sotuvchilar.id.

    Qaytaradi: yangi `elonlar.id`. Tashqi id `ober-{id}` shaklida.
    """
    init()
    now = time.time()
    with ulan() as c:
        # Tashqi_id UNIQUE(manba, tashqi_id) bo'lishi shart — vaqt asosida
        # yozib, keyin `ober-{id}` ga o'zgartiramiz (ikkalasi ham unikal).
        nom = (e.get("nom") or "").strip()
        narx = _ober_narx(e.get("narx_som"))
        # Narxga aylanmagan matn ("500", "abc") — narx tushmaydi, lekin
        # "kelishiladi" belgisi ham tushmasin (2026-08-06 kod-review).
        kelishiladi = 1 if narx is None else int(e.get("kelishiladi", 0))
        # SANА — ISO bugun. 2026-08-06: ilgari yozilmasdi (NULL) — yangi
        # e'lon "Bugun" deb ko'rinmasdi va qidiruvda yangilik bonusi
        # olmasdi (yosh=99 → 0 ball). Natijada sotuvchining yangi e'loni
        # minglab eski OLX e'lonlari orasida ko'rinmay qolardi.
        sana = _toshkent_bugun()
        cur = c.execute("""
            INSERT INTO elonlar
            (manba, tashqi_id, nom, narx_som, kelishiladi, holat, sana,
             viloyat, shahar, tuman, kategoriya, tavsif, rasm, rasmlar_ober,
             telefon, biznes, olindi, faol, korilmadi, oxirgi_korildi,
             egasi, elon_holati, yangilandi)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
                "ober", f"ober-{time.time_ns()}", nom, narx,
                kelishiladi, "yangi", sana,
                (e.get("viloyat") or "").strip(),
                (e.get("shahar") or "").strip(),
                (e.get("tuman") or "").strip(),
                (e.get("kategoriya") or "").strip(),
                (e.get("tavsif") or "").strip(),
                (e.get("rasm") or "").strip(),
                (e.get("rasmlar_ober") or "").strip(),
                (e.get("telefon") or "").strip(),
                int(e.get("biznes", 0)),
                now, 1, 0, now, egasi, "faol", now))
        elon_id = cur.lastrowid
        c.execute("UPDATE elonlar SET tashqi_id=? WHERE id=?",
                  (f"ober-{elon_id}", elon_id))
        if narx:
            c.execute("INSERT INTO narx_tarix (manba, tashqi_id, narx_som, vaqt)"
                      " VALUES (?,?,?,?)", ("ober", f"ober-{elon_id}", narx, now))
    return elon_id


def ober_elon_yangila(egasi: int, elon_id: int, e: dict) -> bool:
    """E'lonni tahrirlaydi. FAQAT egasi — boshqa birov chaqirsa False.

    Narx o'zgarsa narx tarixiga yoziladi (aktivimiz). Tahrirlashdan
    keyin `tan_qismlar=NULL` — tahlil qayta qilinishi kerak (qidiruv
    yangi nom bo'yicha ishlasin).
    """
    init()
    now = time.time()
    nom = (e.get("nom") or "").strip()
    # Bo'sh nom bilan tahrir — shart emas: funksiya muvaffaqiyatni
    # yolg'on aytmasin (server qatlami ham tekshiradi).
    if not nom:
        return False
    with ulan() as c:
        r = c.execute("SELECT egasi, narx_som, tashqi_id, elon_holati,"
                      " kategoriya, viloyat, shahar, tuman, rasm, rasmlar_ober"
                      " FROM elonlar WHERE id=? AND manba='ober'", (elon_id,)).fetchone()
        if not r:
            return False
        r = dict(r)
        if r["egasi"] != egasi:
            return False
        # O'chirilgan yoki sotilgan e'lon tahrirlanmaydi
        if r["elon_holati"] != "faol":
            return False
        narx = _ober_narx(e.get("narx_som"))
        # Narxga aylanmagan matn — "kelishiladi" belgisi qo'yilsin.
        kelishiladi = 1 if narx is None else int(e.get("kelishiladi", 0))
        # YO'QOTMAYMIZ: bo'sh kelgan maydon eski qiymatni yemasin.
        # Forma hamma maydonni yuboradi, lekin xato yuborilgan bo'lsa
        # ham avvalgi ma'lumot saqlanadi (saqla() dagi qoida bilan bir xil).
        # RASMLAR ham shu qoidaga bo'ysunadi: forma tahrirlanganda
        # rasmlarni yubormasa, eski rasmlar saqlanib qoladi (2026-08-06
        # kod-review: tahrirlashda rasmlar o'chib ketardi).
        def yangi(maydon, eski):
            qiymat = (e.get(maydon) or "").strip()
            return qiymat if qiymat else eski
        # Tahrirlash — e'lon yangilandi: `sana` ham bugunga o'tadi.
        # Aks holda eski sana qolib, qidiruvda yangilik bonusi yo'qoladi
        # va karta "10 kun oldin" ko'rinishida qolardi.
        sana = _toshkent_bugun()
        c.execute("""UPDATE elonlar SET nom=?, narx_som=?, kelishiladi=?,
                     viloyat=?, shahar=?, tuman=?, kategoriya=?, tavsif=?,
                     rasm=?, rasmlar_ober=?, sana=?, yangilandi=?,
                     tan_qismlar=NULL
                     WHERE id=?""", (
                nom, narx, kelishiladi,
                yangi("viloyat", r["viloyat"] or ""),
                yangi("shahar", r["shahar"] or ""),
                yangi("tuman", r["tuman"] or ""),
                yangi("kategoriya", r["kategoriya"] or ""),
                (e.get("tavsif") or "").strip(),
                yangi("rasm", r.get("rasm") or ""),
                yangi("rasmlar_ober", r.get("rasmlar_ober") or ""),
                sana, now, elon_id))
        if narx and narx != r["narx_som"]:
            c.execute("INSERT INTO narx_tarix (manba, tashqi_id, narx_som, vaqt)"
                      " VALUES (?,?,?,?)",
                      ("ober", r["tashqi_id"], narx, now))
    return True


def ober_elon_ochir(egasi: int, elon_id: int) -> bool:
    """E'lonni o'chiradi (elon_holati='ochirildi'). FAQAT egasi.

    O'chirilgan e'lon qidiruvda chiqmaydi: qidiruv `faol=1` ni oladi,
    biz `faol=0` qilamiz. Qator o'chirilmaydi — tarix saqlanadi.
    """
    init()
    with ulan() as c:
        r = c.execute("SELECT egasi, elon_holati FROM elonlar"
                      " WHERE id=? AND manba='ober'", (elon_id,)).fetchone()
        if not r or r["egasi"] != egasi:
            return False
        # Allaqachon o'chirilgan/sotilgan e'lonni qayta o'chirish shart emas
        if r["elon_holati"] != "faol":
            return True
        c.execute("UPDATE elonlar SET elon_holati='ochirildi', faol=0, "
                  "yangilandi=? WHERE id=?", (time.time(), elon_id))
        # FTS'dan ham olib tashlaymiz — qidiruvda qolmasin
        if FTS_BOR:
            try:
                c.execute("DELETE FROM elonlar_fts WHERE rowid=?", (elon_id,))
            except sqlite3.OperationalError:
                pass
    return True


def ober_elonlari(egasi: int) -> list[dict]:
    """Kabinetdagi 'E'lonlarim' — faqat o'z e'lonlari."""
    init()
    with ulan() as c:
        qatorlar = c.execute(
            "SELECT id, nom, narx_som, kelishiladi, kategoriya, tuman, rasm,"
            " elon_holati, olindi, yangilandi FROM elonlar"
            " WHERE manba='ober' AND egasi=? ORDER BY olindi DESC",
            (egasi,)).fetchall()
    return [dict(r) for r in qatorlar]


def ober_elon_ol(elon_id: int) -> dict | None:
    """Bitta OBER e'loni — /elon/{id} sahifasi uchun. Yo'q bo'lsa None.

    `egasi_nomi` — sotuvchilar jadvalidan qo'shiladi: ober_elon_yoz
    `sotuvchi_nomi` ni yozmaydi, shuning uchun alohida join kerak.
    """
    init()
    with ulan() as c:
        r = c.execute(
            "SELECT e.id, e.nom, e.narx_som, e.narx_asl, e.kelishiladi,"
            " e.viloyat, e.shahar, e.tuman, e.kategoriya, e.tavsif, e.rasm,"
            " e.rasmlar_ober, e.egasi, e.elon_holati, e.olindi,"
            " e.sana, e.manba,"
            " s.nom AS egasi_nomi"
            " FROM elonlar e LEFT JOIN sotuvchilar s ON s.id=e.egasi"
            " WHERE e.id=? AND e.manba='ober'", (elon_id,)).fetchone()
    if not r:
        return None
    d = dict(r)
    if d.get("elon_holati") != "faol":
        d["ochirilgan"] = True
    return d


def statistika() -> dict:
    init()
    with ulan() as c:
        jami = c.execute("SELECT COUNT(*) n FROM elonlar").fetchone()["n"]
        faol = c.execute("SELECT COUNT(*) n FROM elonlar WHERE faol=1").fetchone()["n"]
        nofaol = jami - faol
        manbalar = c.execute(
            "SELECT manba, COUNT(*) n FROM elonlar WHERE faol=1 GROUP BY manba"
        ).fetchall()
        narxli = c.execute(
            "SELECT COUNT(*) n FROM elonlar WHERE faol=1 AND narx_som IS NOT NULL"
        ).fetchone()["n"]
        tumanlar = c.execute(
            "SELECT COUNT(DISTINCT tuman) n FROM elonlar WHERE faol=1 AND tuman <> ''"
        ).fetchone()["n"]
        viloyatlar = c.execute(
            "SELECT viloyat, COUNT(*) n FROM elonlar WHERE faol=1 AND viloyat IS NOT NULL"
            " GROUP BY viloyat ORDER BY n DESC").fetchall()
    return {"jami": jami, "faol": faol, "nofaol": nofaol,
            "narxli": narxli, "tumanlar": tumanlar,
            "manbalar": {r["manba"]: r["n"] for r in manbalar},
            "viloyatlar": {r["viloyat"]: r["n"] for r in viloyatlar}}
