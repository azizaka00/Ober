"""OBER qidiruv relevansi uchun deterministik regressiya sinovi.

Haqiqiy bazadagi e'lon soni o'zgaradi. Shu sabab sinov kichik sun'iy indeksda
model, qism va umumiy e'lon qoidalarini qat'iy tekshiradi.
"""

from __future__ import annotations

import time

import qidiruv
from lugat import modellarni_top, qismlarni_top


def elon(tashqi_id: str, nom: str) -> dict:
    """Qidiruv kutadigan minimal, oldindan tahlil qilingan e'lon."""
    return {
        "tashqi_id": tashqi_id,
        "nom": nom,
        "narx_som": 250_000,
        "narx_asl": "250 000 so'm",
        "holat": "yangi",
        "viloyat": "Toshkent shahri",
        "shahar": "Toshkent shahri",
        "tuman": "Chilonzor",
        "sana": "2026-08-01",
        "havola": f"https://example.test/{tashqi_id}",
        "rasm": "https://example.test/rasm.jpg",
        "biznes": 0,
        "qism_turi": "",
        "sotuvchi_nomi": "Sinov",
        "tan_modellar": ",".join(sorted(modellarni_top(nom))),
        "tan_qismlar": ",".join(sorted(qismlarni_top(nom))),
    }


def main() -> None:
    indeks = [
        elon("nexia", "Nexia old tormoz kolodkasi"),
        elon("umumiy", "Tormoz kolodkalari barcha avtomobillar uchun"),
        elon("range", "Range Rover orqa tormoz kolodkasi"),
        elon("bentley", "Bentley Bentayga old kolodka"),
        elon("kolonka", "Nexia rulavoy kalonka ideal"),
        elon("tesla", "Tesla model 3 old kolodka"),
        elon("buick", "Buick Velite 6 kolodka"),
        elon("cadillac", "Cadillac Escalade kolodka"),
        elon("jeep", "Jeep Wrangler kolodka"),
        elon("aeolus", "Aelous Shine kolodka"),
        elon("mustang", "Ford Mustang old kolodka"),
        elon("traverse", "Chevrolet Travers old kolodka"),
    ]

    eski_nomzodlar = qidiruv._nomzodlar
    # Deterministik sun'iy indeks real SQLite FTS jadvalida yo'q. Sinovda
    # nomzodlar aynan yuqoridagi kichik ro'yxatdan olinadi.
    qidiruv._nomzodlar = lambda *_: indeks
    try:
        # Server ishga tushganda lug'at/kesh bir marta qiziydi. Qabul mezoni
        # foydalanuvchi ko'radigan keyingi issiq qidiruv uchun o'lchanadi.
        qidiruv.qidir("Neksiya kolodka", limit=20)
        boshlandi = time.perf_counter()
        nexia = qidiruv.qidir("Neksiya kolodka", limit=20)
        vaqt_ms = (time.perf_counter() - boshlandi) * 1000
        nexia_id = {x["tashqi_id"] for x in nexia["natijalar"]}

        range_natija = qidiruv.qidir("Range Rover kolodka", limit=20)
        range_id = {x["tashqi_id"] for x in range_natija["natijalar"]}
    finally:
        qidiruv._nomzodlar = eski_nomzodlar

    sinovlar = [
        ("nexia" in nexia_id, "Nexia kolodkasi qoldi"),
        ("umumiy" in nexia_id, "modeli yozilmagan umumiy kolodka qoldi"),
        ("range" not in nexia_id, "Range Rover Nexia natijasidan kesildi"),
        ("bentley" not in nexia_id, "Bentley Nexia natijasidan kesildi"),
        ("tesla" not in nexia_id, "Tesla Nexia natijasidan kesildi"),
        (not {"buick", "cadillac", "jeep", "aeolus"} & nexia_id,
         "Buick, Cadillac, Jeep va Aeolus Nexia natijasidan kesildi"),
        (not {"mustang", "traverse"} & nexia_id,
         "Mustang va Traverse Nexia natijasidan kesildi"),
        ("kolonka" not in nexia_id, "rul kolonkasi kolodkaga aralashmadi"),
        (nexia["jami"] == 2, "Nexia so'rovida faqat aniq va umumiy natija qoldi"),
        (nexia["kesildi_model"] == 9, "to'qqizta boshqa model kesilgan deb sanaldi"),
        ("range" in range_id, "Range Rover o'z so'rovida chiqdi"),
        ("nexia" not in range_id and "bentley" not in range_id,
         "Range Rover so'rovida boshqa modellar kesildi"),
        (vaqt_ms < 500, f"issiq qidiruv 500 ms dan tez ({vaqt_ms:.1f} ms)"),
    ]

    print("=" * 64)
    print("  OBER — RELEVANS REGRESSIYA SINOVI")
    print("=" * 64)
    xato = 0
    for shart, nom in sinovlar:
        print(f"  [{'OK  ' if shart else 'XATO'}] {nom}")
        xato += not shart
    print("-" * 64)
    print(f"  NATIJA: {len(sinovlar) - xato} to'g'ri · {xato} xato")
    if xato:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
