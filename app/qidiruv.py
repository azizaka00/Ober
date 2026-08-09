"""
OBER — QIDIRUV

Vazifasi: tartibsiz so'rovni tushunish va mos e'lonlarni topish.

OLX'ning muammosi (o'lchangan): "neksiya kolodka" -> 10 natija, 4 tasi
boshqa mashina. Biz shuni tuzatamiz:

  1. Model mos kelmasa — KESAMIZ (Эквинокс kolodka Neksiya so'roviga chiqmaydi)
  2. Modeli yo'q umumiy e'lon — qoladi, lekin pastroqda
  3. Imlo va alifbo farqi — lug'at orqali birlashtiriladi
  4. Saralash: moslik > yaqinlik (tuman) > narx > yangilik
"""

from __future__ import annotations

import os
import re
import time

import baza
import joylar
from lugat import modellarni_top, normalla, qismlarni_top, sorovni_tozala
from yonalishlar import yonalish_nomlari, yonalishlarni_top


# Ulgurji/to'plam e'lonlari — bitta dona narxi emas
ULGURJI = re.compile(r"optom|оптом|ulgurji|to'plam|komplekt|комплект|"
                     r"\bnabor\b|набор", re.I)

# "BUTUN NARSA" kategoriyalari — mahsulotning o'zi, qismi emas.
# Qism so'ralganda bular chiqmaydi: fara so'ragan odamga mashina
# kerak emas. So'rovning o'zida shu so'z bo'lsa — chiqadi.
BUTUN_NARSA = re.compile(
    r"yengil avtomash|yuk mashina|avtobus|mototsikl|\bmoto\b|"
    r"maxsus texnika|qishloq xo'jaligi texnika|suv transport|tirkama|"
    r"kvartira|xususiy uy|yer uchastka|tijorat bino|dacha", re.I)


def _yosh_kun(sana: str) -> int:
    """E'lon qanchalik eski (taxminiy kunlarda). Aniq emas — saralash uchun."""
    if not sana:
        return 99
    # Yangi manba (holat bloki) ISO sana beradi: "2026-07-29"
    m_iso = re.match(r"(\d{4})-(\d{2})-(\d{2})", sana)
    if m_iso:
        y, oy, kun = (int(x) for x in m_iso.groups())
        # Toshkent vaqti (UTC+5, DST yo'q). `sana` endi Toshkent bo'yicha
        # yoziladi (baza._toshkent_bugun) — taqqoslash ham shu vaqtda.
        # 2026-08-07: server UTC edi, 19:00 dan keyin e'lonlar "1 kun
        # eski" bo'lib saralanardi.
        import datetime as _dt
        hozir = _dt.datetime.now(_dt.timezone.utc) + _dt.timedelta(hours=5)
        farq = ((hozir.year - y) * 365 + (hozir.month - oy) * 30
                + (hozir.day - kun))
        return max(0, min(farq, 365))
    s = sana.lower()
    if "сегодня" in s or "bugun" in s:
        return 0
    if "вчера" in s or "kecha" in s:
        return 1
    oylar = {"январ": 1, "феврал": 2, "март": 3, "апрел": 4, "ма": 5, "июн": 6,
             "июл": 7, "август": 8, "сентябр": 9, "октябр": 10, "ноябр": 11,
             "декабр": 12}
    m = re.search(r"(\d{1,2})\s+([а-я]+)", s)
    if not m:
        return 30
    kun = int(m.group(1))
    oy = next((v for k, v in oylar.items() if m.group(2).startswith(k)), 0)
    if not oy:
        return 30
    hozir = time.localtime()
    farq = (hozir.tm_mon - oy) * 30 + (hozir.tm_mday - kun)
    return max(0, min(farq, 365))


# ── E'lonlar xotirada ────────────────────────────────────────────────────────
# 8 500 e'londa har qidiruvda bazadan o'qish sezilarli vaqt oladi. E'lonlar
# kuniga bir-ikki marta o'zgaradi, so'rov esa har soniyada keladi — shuning
# uchun ular xotirada turadi va baza fayli o'zgargandagina qayta o'qiladi.
_KESH: list = []
_KESH_VAQT: float = -1.0


def _elonlar() -> list:
    global _KESH, _KESH_VAQT
    # DB faylining mtime'i qidiruv statistikasi yozilganda ham o‘zgaradi.
    # Kesh faqat `tahlil.py` barcha yangi e’lonni tayyorlab bo‘lgach yaratgan
    # alohida belgi orqali yangilanadi. Yig‘ish davomida eski, barqaror kesh
    # xizmat qiladi; yarim tahlil qilingan minglab qator issiq yo‘lga kirmaydi.
    belgi = baza.DB.with_name("qidiruv-kesh.version")
    try:
        ozgardi = os.path.getmtime(belgi)
    except OSError:
        try:
            ozgardi = os.path.getmtime(baza.DB)
        except OSError:
            ozgardi = 0.0
    if ozgardi != _KESH_VAQT or not _KESH:
        with baza.ulan() as c:
            _KESH = [dict(r) for r in c.execute(
                "SELECT id, manba, tashqi_id, nom, narx_som, narx_asl, holat,"
                " viloyat, shahar, tuman, sana, havola, rasm, biznes,"
                " qism_turi, kategoriya, sotuvchi_nomi, tan_modellar,"
                " tan_qismlar, tan_nom_qismlar"
                " FROM elonlar WHERE faol=1 AND tan_qismlar IS NOT NULL")]
        _KESH_VAQT = ozgardi
    return _KESH


def keshni_tayyorla() -> int:
    """Server ochilishidan oldin qidiriladigan e’lonlarni xotiraga oladi.

    FTS5 bor bo'lsa xotiraga hech narsa yuklanmaydi — indeks ishlatiladi.
    """
    if baza.FTS_BOR:
        with baza.ulan() as c:
            return c.execute("SELECT COUNT(*) n FROM elonlar_fts").fetchone()["n"]
    return len(_elonlar())


def _nomzodlar(sorov_modellar, sorov_qismlar, sozlar) -> list:
    """Qidiriladigan e'lonlar to'plami.

    FTS5 bor bo'lsa — indeksdan bir necha ming nomzod. Bo'lmasa — eski
    yo'l (hammasini xotiraga yuklash). Ikkala holatda ham keyingi ballash
    bir xil ishlaydi, ya'ni natija sifati o'zgarmaydi.
    """
    if not baza.FTS_BOR:
        return _elonlar()
    teglar = sorted(sorov_qismlar) or sorted(sorov_modellar)
    idlar = baza.fts_nomzodlar(teglar, sozlar)
    if not idlar:
        return []
    return baza.elonlar_idlardan(idlar)


def _yakunla(r: dict, ball: float, tuman: str, ishonchli: bool,
             e_modellar: set, e_qismlar: set) -> dict:
    """Umumiy qo'shimcha ballar va ko'rsatish maydonlari.

    Ikkala rejim (lug'atli va erkin) ham shu yerdan o'tadi — saralash
    qoidasi bir xil bo'lishi uchun.
    """
    # YAQINLIK. Joy lug'at orqali toza nomga aylantiriladi: OLX'dagi
    # "Риштан" -> Farg'ona / Rishton. Ilgari faqat "tuman" ustuni
    # solishtirilardi va Toshkentdan tashqarida hech qachon ishlamasdi.
    e_viloyat, e_joy = joylar.tani(r["shahar"] or "", r["tuman"] or "",
                                   r["viloyat"] or "")
    yaqinmi = bool(tuman and joylar.moslikmi(tuman, e_viloyat, e_joy))
    if yaqinmi:
        ball += 25
    if r["narx_som"]:
        ball += 5                            # narxi bor
    if r["biznes"]:
        ball += 4                            # do'kon — ishonchliroq
    if r["rasm"]:
        ball += 3
    yosh = _yosh_kun(r["sana"] or "")
    ball += max(0, 10 - yosh / 3)            # yangiroq — yuqoriroq
    # OBER'NING O'Z E'LONI — birinchi qo'l ma'lumot.
    # Yig'ilgan OLX/Telegram e'lonlaridan bitta muhim farqi bor:
    # sotuvchi ro'yxatdan o'tib, OBER'ning o'ziga qo'ygan. Engil
    # ustunlik beriladi — aks holda 100 000+ yig'ilgan e'lon orasida
    # yangi sotuvchining e'loni ko'rinmay qolardi (2026-08-06 o'lchov:
    # "divan" so'rovida yangi OBER e'loni TOP-60 ga kirmasdi).
    if r.get("manba") == "ober":
        ball += 18
    return {**r, "ball": round(ball, 1), "yosh_kun": yosh,
            # KO'RSATISH uchun toza nom: "Риштан" o'rniga "Rishton · Farg'ona"
            "joy_nom": (f"{e_joy}, {e_viloyat}" if e_joy and e_viloyat
                        else e_joy or e_viloyat or ""),
            # nima uchun qoldi — sozlash va xatoni topish uchun
            "_ishonchli": ishonchli,
            "_yaqin": yaqinmi,
            "_modellar": sorted(e_modellar),
            "_qismlar": sorted(e_qismlar)}


def qidir(sorov: str, tuman: str = "", limit: int = 20,
          tartib: str = "moslik", narx_dan: int = 0, narx_gacha: int = 0,
          faqat_rasm: bool = False, faqat_yangi: bool = False,
          faqat_dokon: bool = False, byudjetsiz: bool = False) -> dict:
    """So'rovni tahlil qilib, mos e'lonlarni qaytaradi."""
    _t0 = time.perf_counter()
    baza.init()

    sorov_modellar = modellarni_top(sorov)
    sorov_qismlar = qismlarni_top(sorov)
    sorov_yonalishlar = yonalishlarni_top(sorov)

    # SO'ROVNI TOZALASH.
    # Aziz, 2026-08-03: xaridor erkin yozadi -
    #   "menga soat kerak bambino 6, kim 800.000 so'mga beradi?"
    # Qidiruvga faqat SOAT va BAMBINO 6 ketishi kerak; "menga", "kerak",
    # "kim", "beradi" - shovqin, "800 000 so'm" esa byudjet.
    # Ilgari hammasi indeksga yuborilardi.
    #
    # Qisqa so'zlar tashlanadi, LEKIN raqamlar qoladi: "iphone 13" da
    # "13" - modelning o'zi, "bambino 6" da "6" ham shunday.
    sorov_soz, sorov_byudjet = sorovni_tozala(sorov)

    # Xaridor byudjet aytgan bo'lsa, u narx chegarasiga aylanadi.
    # Foydalanuvchi filtri ustun: u ataylab boshqa chegara qo'ygan bo'lsa
    # biz uni bosib o'tmaymiz.
    if sorov_byudjet and not narx_gacha and not byudjetsiz:
        narx_gacha = sorov_byudjet

    # ERKIN REJIM — lug'at hech narsa tanimaganda.
    #
    # 2026-08-02 gacha bu yerda shunchaki bo'sh javob qaytarilardi.
    # O'lchov: bazada 101 381 e'lon, lekin "divan", "iphone 13",
    # "kvartira", "velosiped" — hammasi 0 natija berardi. Ya'ni tun bo'yi
    # yig'ilgan ma'lumotning deyarli hammasi ko'rinmasdi, chunki lug'at
    # faqat mashinani biladi.
    #
    # Endi lug'at SHART emas. Tanisa — model kesish va ishonchli moslik
    # ishlaydi (avtoqismda sifat shundan). Tanimasa — indeksdagi matn
    # bo'yicha qidiramiz. Yomonrog'i emas, boshqasi: kamroq aniq, lekin
    # butun bozor ochiq.
    erkin = not sorov_modellar and not sorov_qismlar
    if erkin and not sorov_soz:
        return {
            "sorov": sorov,
            "tushunildi": {"modellar": [], "qismlar": [],
                           "yonalishlar": yonalish_nomlari(sorov_yonalishlar)},
            "jami": 0, "kesildi_model": 0, "narxli_soni": 0,
            "eng_arzon": None, "tartib": tartib, "erkin": True,
            "natijalar": [],
            "jonli_sorov": bool(sorov_yonalishlar),
            "aniqlash_kerak": not bool(sorov_yonalishlar),
        }

    # Model so'zlarini ajratamiz. XATO EDI: "neksiya kolodka" so'rovida
    # "neksiya" so'zi mos kelgani uchun ball berilardi va NEKSIYANING
    # BOSHQA QISMLARI (туманка, katushka, климат) tepaga chiqardi.
    # Endi qism so'zi alohida tekshiriladi.
    model_sozlari = {w for w in sorov_soz if modellarni_top(w)}
    tanish_qism_sozlari = {w for w in sorov_soz if qismlarni_top(w)}
    erkin_sozlar = [w for w in sorov_soz
                    if w not in model_sozlari and w not in tanish_qism_sozlari]

    ms_lugat = round((time.perf_counter() - _t0) * 1000)
    _t = time.perf_counter()
    if erkin:
        hammasi = baza.elonlar_idlardan(baza.fts_erkin(sorov_soz))
    else:
        hammasi = _nomzodlar(sorov_modellar, sorov_qismlar,
                             sorov_soz if not sorov_qismlar else erkin_sozlar)
    ms_indeks = round((time.perf_counter() - _t) * 1000)
    nomzod_soni = len(hammasi)
    _t = time.perf_counter()

    natijalar = []
    kesildi_model = 0

    # ── ERKIN REJIM: matn bo'yicha ballash ────────────────────────────
    # Indeksda sarlavhadan tashqari kategoriya va OLX bergan tavsiflar
    # ("2 xonali", "128 GB") ham bor. Sarlavhada topilgan so'z og'irroq:
    # "divan" sarlavhada bo'lsa — bu divan; faqat kategoriyada bo'lsa —
    # mebel bo'limidagi boshqa narsa bo'lishi mumkin.
    if erkin:
        # 2026-08-02 birinchi o'lchov: "divan" so'roviga changyutgich
        # birinchi chiqdi ("...mыйt pol kovr i divan 3v1"), "iphone 13" ga
        # esa USB kabel ("...11,12,13,14/pro/max"). Ikkalasida ham so'z
        # sarlavhada BOR edi — demak borligining o'zi yetmaydi.
        #
        # To'rtta signal qo'shildi:
        #   1. So'zlar KETMA-KET turibdimi ("iphone 13" <-> "iphone 13 pro")
        #   2. So'z sarlavhaning BOSHIDAmi ("Divan sotiladi" <-> "...i divan")
        #   3. Sarlavha QISQAmi (kalit so'z tiqilgan e'lonlar pastga tushadi)
        #   4. Butun so'zmi (qism-satr emas)
        sorov_matn = " ".join(sorov_soz)
        # O'lcham va model raqamlari FTS nomzodlarini kengaytiradi, lekin
        # o'zi mahsulot ma'nosi emas. Masalan, "25 kv banner 5 ga 5"
        # so'rovi ilgari faqat "5" soni uchragani uchun kvartira, shina va
        # tirkamalarni ham chiqarardi. Harfli so'z mavjud bo'lsa, natijada
        # kamida bittasi uchrashi shart; raqamlar esa keyingi ballashda
        # aniqlikni oshirishda davom etadi ("iphone 13" saqlanadi).
        miqdor_sozlari = {
            "kv", "kvadrat", "metr", "metri", "metrlik", "sm",
            "santimetr", "mm", "kg", "gramm", "dona", "ta",
        }
        mazmun_sozlari = [w for w in sorov_soz
                          if not w.isdigit() and w not in miqdor_sozlari]
        kat_kesh: dict = {}
        for r in hammasi:
            n_nom = normalla(r["nom"] or "")
            sozlari = n_nom.split()
            nomda, eng_erta = 0, 99
            for w in sorov_soz:
                for i, x in enumerate(sozlari):
                    if x == w or x.startswith(w):
                        nomda += 1
                        if i < eng_erta:
                            eng_erta = i
                        break
            # Sarlavha + kategoriya. Kategoriya nomi minglab e'londa
            # takrorlanadi — bir marta normallashtirilib keshlanadi.
            kat = r.get("kategoriya") or ""
            if kat not in kat_kesh:
                kat_kesh[kat] = normalla(kat)
            n_hammasi = n_nom + " " + kat_kesh[kat]
            if (mazmun_sozlari
                    and not any(w in n_hammasi for w in mazmun_sozlari)):
                continue
            qayerda = sum(1 for w in sorov_soz if w in n_hammasi)
            if not qayerda:
                continue
            ball = 8.0 * qayerda + 10.0 * nomda
            if qayerda == len(sorov_soz):
                ball += 25                       # so'rovning hammasi bor
            if nomda == len(sorov_soz):
                ball += 30                       # va aynan sarlavhada
            if len(sorov_soz) > 1 and sorov_matn in n_nom:
                ball += 45                       # ketma-ket — eng kuchli belgi
            if eng_erta < 99:
                ball += 14 * max(0.0, 1 - eng_erta / 8)
            if sozlari:
                ball += 10 * max(0.0, 1 - len(sozlari) / 14)
            natijalar.append(_yakunla(r, ball, tuman,
                                      nomda == len(sorov_soz), set(), set()))
        hammasi = []                 # asosiy halqa bo'sh o'tadi

    for r in hammasi:
        matn = f"{r['nom']} {r['qism_turi'] or ''}"
        # TEZLIK: tahlil oldindan qilingan bo'lsa o'shani olamiz.
        # Aks holda har so'rovda 1600+ e'lon qayta tahlil qilinadi va
        # qidiruv 3-5 soniya davom etadi (o'lchangan).
        if r["tan_qismlar"] is not None:
            e_modellar = {x for x in (r["tan_modellar"] or "").split(",") if x}
            e_qismlar = {x for x in (r["tan_qismlar"] or "").split(",") if x}
        else:
            e_modellar = modellarni_top(matn)
            e_qismlar = qismlarni_top(matn)

        # TEZLIK-2: normalla() har e'lon uchun chaqirilardi. 8 500 e'londa
        # bu behuda ish — u faqat lug'at qismni tanimagan holda kerak.
        # Endi faqat kerak bo'lganda hisoblanadi.
        n_matn = None

        ball = 0.0
        ishonchli = True            # sarlavhaning o'zi tasdiqlaydimi?

        # ── 0. QISM SO'RALSA, BUTUN NARSA CHIQMASIN
        #
        # 2026-08-02: "kobalt fara" so'roviga 135-170 MLN so'mlik
        # e'lonlar chiqdi — bular fara emas, butun mashina edi.
        # Narx oralig'i shundan buzilgan.
        #
        # Sabab ikkita edi: lug'atda "svet" fara deb yozilgan (o'zbekchada
        # u RANG), va tizimda "qism so'ralganda butun narsa chiqmasin"
        # degan qoida yo'q edi. Birinchisi tuzatildi, bu — ikkinchisi.
        #
        # Qoida umumiy: mashina qismini so'ragan odamga mashinaning
        # o'zi kerak emas. Kvartira ta'miri so'ralganda kvartira,
        # telefon ekrani so'ralganda telefon ham shunday.
        if sorov_qismlar and BUTUN_NARSA.search(r.get("kategoriya") or ""):
            if not BUTUN_NARSA.search(sorov):
                continue

        # ── 1. Qism turi — MAJBURIY (agar so'rovda ko'rsatilgan bo'lsa)
        if sorov_qismlar:
            if sorov_qismlar & e_qismlar:
                # KUCHLI va KUCHSIZ moslikni ajratamiz.
                #
                # 2026-08-01 o'lchov: "kobalt fara" so'roviga
                # "Cobolt tumanka Radnoy orginal" chiqdi. Sabab —
                # OLX kategoriyasi "Автосвет" bo'lib, u lug'atda `fara`ga
                # bog'langan. Bitta keng kategoriya tumanka, stop, lampa
                # va LED lentani ham `fara` qilib qo'yadi.
                #
                # Sarlavhaning O'ZIDA qism nomi bo'lsa — ishonchli.
                # Faqat OLX kategoriyasidan kelgan bo'lsa — pastroq ball
                # va narx hisobiga kiritilmaydi.
                nq = r.get("tan_nom_qismlar")
                nom_qismlari = ({x for x in nq.split(",") if x}
                                if nq is not None
                                else qismlarni_top(r["nom"] or ""))
                ishonchli = bool(sorov_qismlar & nom_qismlari)
                ball += 50 if ishonchli else 26
            else:
                # E’lonlar oldindan aynan shu lug‘at bilan tahlil qilingan.
                # Har mos kelmagan e’londa yana fuzzy tahlil qilish 10 ming
                # qatorda qidiruvni soniyalarga cho‘zardi.
                continue            # boshqa qism — kerak emas

        # ── 2. Model tekshiruvi — ASOSIY TUZATISH
        if sorov_modellar:
            if sorov_modellar & e_modellar:
                ball += 40                       # aynan shu mashina
            elif e_modellar:
                kesildi_model += 1               # BOSHQA mashina -> kesamiz
                continue
            else:
                ball += 5                        # modeli ko'rsatilmagan (umumiy)

        # ── 3. Qolgan so'zlar (shu yerga kam e'lon yetib keladi)
        if erkin_sozlar:
            if n_matn is None:
                n_matn = normalla(matn)
            ball += 4 * sum(1 for w in erkin_sozlar if w in n_matn)

        if ball <= 0:
            continue

        natijalar.append(_yakunla(r, ball, tuman, ishonchli,
                                  e_modellar, e_qismlar))

    ms_ballash = round((time.perf_counter() - _t) * 1000)
    _t = time.perf_counter()

    # ── FILTR — xaridorning o'z tanlovi.
    #
    # 2026-08-02, Azizning qarori: narx oralig'i, o'rtacha narx va
    # gistogramma OLIB TASHLANDI. Sabab: OLX narxlarini oddiy odamlar
    # o'z bilganicha yozadi. Bunday ma'lumot ustidan hisoblangan har
    # qanday o'rtacha yolg'on chiqadi va biz uni cheksiz tuzatib
    # yuraveramiz (svet -> mashinalar, 10 000 so'mlik fara, ulgurji...).
    #
    # O'rniga: hammasini ko'rsatamiz, saralash va filtrni xaridorga
    # beramiz. Filtr hech qachon yolg'on gapirmaydi.
    if narx_dan:
        natijalar = [x for x in natijalar
                     if x["narx_som"] and x["narx_som"] >= narx_dan]
    if narx_gacha:
        natijalar = [x for x in natijalar
                     if x["narx_som"] and x["narx_som"] <= narx_gacha]
    if faqat_rasm:
        natijalar = [x for x in natijalar if x["rasm"]]
    if faqat_yangi:
        natijalar = [x for x in natijalar if x["holat"] == "yangi"]
    if faqat_dokon:
        natijalar = [x for x in natijalar if x["biznes"]]

    # ── SARALASH
    if tartib == "arzon":
        natijalar.sort(key=lambda x: (x["narx_som"] is None,
                                      x["narx_som"] or 0, -x["ball"]))
    elif tartib == "qimmat":
        natijalar.sort(key=lambda x: (x["narx_som"] is None,
                                      -(x["narx_som"] or 0), -x["ball"]))
    elif tartib == "yangi":
        natijalar.sort(key=lambda x: (x["yosh_kun"], -x["ball"]))
    elif tartib == "yaqin":
        # Tanlangan joydagilar oldinda; joy tanlanmagan bo'lsa moslik
        natijalar.sort(key=lambda x: (not x["_yaqin"], -x["ball"]))
    else:                                        # moslik (asosiy)
        natijalar.sort(key=lambda x: (-x["ball"], x["narx_som"] or 10**12))

    # ── NUSXALARNI BIRLASHTIRISH
    #
    # 2026-08-03: bitta mashina ro'yxatda ikki marta chiqardi. Sabab —
    # `moshina` va `moshina_bozorim` kanallari bir xil e'lonni joylaydi.
    # OLX'da ham bir sotuvchi bir tovarni bir necha viloyatga qo'yadi.
    # Xaridor uchun bir xil karta ikki marta — sayt buzuq ko'rinadi.
    #
    # Kalit: normallashtirilgan nom + narx. Saralashdan KEYIN qilinadi,
    # shuning uchun har guruhdan eng yuqori o'rindagisi qoladi.
    # O'chirmaymiz — faqat ko'rsatmaymiz: manba boshqa bo'lishi mumkin
    # va sotuvchi ham boshqa bo'lishi mumkin.
    korilgan = set()
    yagona = []
    for x in natijalar:
        kalit = (normalla(x["nom"] or "")[:70], x["narx_som"])
        if kalit in korilgan:
            continue
        korilgan.add(kalit)
        yagona.append(x)
    nusxa_soni = len(natijalar) - len(yagona)
    natijalar = yagona

    top = natijalar[:limit]

    # FAQAT FAKT. O'rtacha, oraliq va gistogramma yo'q — ular hisoblangan
    # taxmin edi va noto'g'ri chiqardi. "Eng arzoni" esa hisob emas,
    # ro'yxatdagi haqiqiy eng past narx: uni xaridor bosib ko'rishi mumkin.
    narxlar = sorted(x["narx_som"] for x in natijalar if x["narx_som"])

    return {
        "sorov": sorov,
        "tushunildi": {"modellar": sorted(sorov_modellar),
                       "qismlar": sorted(sorov_qismlar),
                       "yonalishlar": yonalish_nomlari(sorov_yonalishlar)},
        "jami": len(natijalar),
        "kesildi_model": kesildi_model,
        "narxli_soni": len(narxlar),
        "eng_arzon": narxlar[0] if narxlar else None,
        "tartib": tartib,
        "erkin": erkin,
        # Chegaraga tegdimi. Tegsa ekranda "900+" deb yoziladi — "900 ta"
        # deb yozish yolg'on bo'lardi, chunki aslida ko'proq.
        "chegarada": erkin and nomzod_soni >= baza.ERKIN_CHEGARA,
        "sozlar": sorov_soz,
        # Xaridor byudjet aytgan bo'lsa - ekranda ko'rsatiladi, chunki
        # u natijani jimgina cheklab turibdi.
        "byudjet": None if byudjetsiz else sorov_byudjet,
        "nusxa": nusxa_soni,
        # O'LCHOV, taxmin emas. Qaysi bosqich sekin ekanini ko'rsatadi:
        # indeks (SQLite) yoki ballash (Python). 2026-08-02 da "kvartira"
        # 4 781 ms edi va sabab noma'lum edi — shuning uchun qo'shildi.
        "_ms": {"lugat": ms_lugat, "indeks": ms_indeks,
                "ballash": ms_ballash,
                "saralash": round((time.perf_counter() - _t) * 1000),
                "jami": round((time.perf_counter() - _t0) * 1000),
                "nomzod": nomzod_soni},
        "natijalar": top,
    }
