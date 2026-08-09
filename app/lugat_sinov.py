"""
OBER — LUG'AT SINOVI

O'xshashlik moslashtiruvi to'g'ri ishlayaptimi tekshiradi:
xato yozilgan so'zlar to'g'ri modelga tushyaptimi, va
NOTO'G'RI moslik bo'lmayaptimi (bu yomonroq bo'lardi).
"""

from __future__ import annotations

import baza
from lugat import modellarni_top, qismlarni_top

# (matn, kutilgan model, kutilgan qism)
SINOVLAR = [
    # Sinovda topilgan haqiqiy xato yozilishlar
    ("Ковальт амортизатор передний",        "cobalt",  "amortizator"),
    ("Qoblt bufer oq rangli",               "cobalt",  "bamper"),
    ("Koblt bufer oldi va orqa",            "cobalt",  "bamper"),
    ("Орка бампер экюнокс",                 "equinox", "bamper"),
    ("Nexi 2 rul ideal",                    "nexia",   "rul"),
    # To'g'ri yozilganlar ham ishlashi kerak
    ("Кобальт бу фара сатылады",            "cobalt",  "fara"),
    ("neksiya kolodka",                     "nexia",   "kolodka"),
    ("нексия колодка",                      "nexia",   "kolodka"),
    ("Матиз бампер",                        "matiz",   "bamper"),
    ("Amartizator Haval M6",                "haval",   "amortizator"),
    # NOTO'G'RI moslik bo'lmasligi kerak (model yo'q)
    ("Антифриз теплоноситель",              None,      None),
    ("Гидрокарчер профессионал",            None,      None),
    # 2026-07-30 da topilgan yolg'on moslik: gel akkumulyator -> Geely
    ("Гелевы аккумлятор gelviy geliviy",    None,      "akkumulyator"),
    ("gel akumlyator 100Ah",                None,      "akkumulyator"),
    # Lekin haqiqiy Geely tanilishi SHART
    ("Geely Coolray fara",                  "geely",   "fara"),
    ("Джили Эмгранд бампер",                "geely",   "bamper"),
    # 2026-07-30: lug'atda yo'q so'z noto'g'ri yozuvga yopishgan edi
    ("Galofka sonc 1.6",                    "nexia",   "lampa"),
    ("Галофка сотилади 35w аргинал",        None,      "lampa"),
    ("Nexia sons Опорный диски суппорт",    "nexia",   "suport"),
    ("Нексия 2 туманка",                    "nexia",   "tumanka"),
    ("Katushka neksiya Katushka dons",      "nexia",   "katushka"),
]

HISOBOT = baza.BASE / "data" / "lugat-sinov.txt"
_s: list[str] = []


def q(x: str = "") -> None:
    print(x)
    _s.append(x)


def main() -> None:
    q("=" * 66)
    q("  OBER — LUG'AT SINOVI (o'xshashlik moslashtiruvi)")
    q("=" * 66)
    q("")

    ok = xato = 0
    for matn, kutilgan_model, kutilgan_qism in SINOVLAR:
        m = modellarni_top(matn)
        p = qismlarni_top(matn)

        model_ok = (kutilgan_model in m) if kutilgan_model else not m
        qism_ok = (kutilgan_qism in p) if kutilgan_qism else True

        belgi = "OK  " if (model_ok and qism_ok) else "XATO"
        if model_ok and qism_ok:
            ok += 1
        else:
            xato += 1

        q(f"  [{belgi}] {matn[:38]:40}")
        q(f"          model: {sorted(m) or '(yo`q)'}"
          f"   kutilgan: {kutilgan_model or '(yo`q)'}")
        q(f"          qism : {sorted(p) or '(yo`q)'}"
          f"   kutilgan: {kutilgan_qism or '(yo`q)'}")
        q("")

    q("-" * 66)
    q(f"  Natija: {ok} to'g'ri · {xato} xato  ({len(SINOVLAR)} tadan)")
    q("")

    HISOBOT.parent.mkdir(parents=True, exist_ok=True)
    HISOBOT.write_text("\n".join(_s), encoding="utf-8")
    print(f"  Saqlandi: {HISOBOT}\n")


if __name__ == "__main__":
    main()
