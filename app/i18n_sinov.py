"""OBER O‘zbek/Rus interfeys poydevori uchun tez regressiya testi."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


SON = 0


def tekshir(shart: bool, nom: str) -> None:
    global SON
    SON += 1
    if not shart:
        raise AssertionError(nom)
    print(f"  OK  {nom}")


def main() -> None:
    i18n = (ROOT / "web" / "i18n.js").read_text(encoding="utf-8")
    server = (ROOT / "app" / "server.py").read_text(encoding="utf-8")
    pages = {
        name: (ROOT / "web" / name).read_text(encoding="utf-8")
        for name in ("index.html", "sotuvchi.html", "takliflar.html")
    }

    tekshir('const STORAGE_KEY = "ober_lang"' in i18n,
            "tanlangan til lokal saqlanadi")
    tekshir('lang === "ru" ? "ru-RU" : "uz-UZ"' in i18n,
            "narx va sonlar tilga mos formatlanadi")
    # 2026-08-13: marketplace hooki ikki matn tugunidan iborat.
    tekshir('"Bir qidiruv.":"Один поиск."' in i18n and
            '"Butun bozor.":"Весь рынок."' in i18n and
            '"OBER — bir qidiruv, butun bozor"' in i18n,
            "bosh sahifa ruscha lug‘atda bor")
    tekshir('"Sotuvchi sifatida boshlang":"Начать как продавец"' in i18n,
            "sotuvchi onboarding ruscha lug‘atda bor")
    tekshir('"Bildirishnomalar":"Уведомления"' in i18n,
            "chat va notification ruscha lug‘atda bor")
    tekshir('MutationObserver' in i18n,
            "API dan keyin chizilgan dinamik matn ham tarjima qilinadi")
    tekshir('"Bildirishnomani sinash":"Проверить уведомление"' in i18n and
            '"Test xabar yuborildi. Telegramni tekshiring."' in i18n and
            '"Test xabar yuborilmadi. Botni ochib /start bosing, keyin qayta sinang"' in i18n,
            "Telegram test holatlari ruscha lug‘atda bor")
    # 2026-08-12: elon.html yopilgan-xabar holatlari — JS orqali
    # yoziladi, rus interfeysda o'zbekcha qolib ketmasligi uchun.
    for soz in ('"Bu e‘lon yopilgan":"Это объявление закрыто"',
                '"← Bosh sahifaga":"← На главную"'):
        tekshir(soz in i18n, f"elon xabar holatlari ruscha lug‘atda bor: {soz.split(':')[0]}")
    # 2026-08-12: kabinet ichidagi 'Yangi e'lon' formasi matnlari
    # ruscha lug'atda bo'lmasa, rus interfeysda o'zbekcha qolib ketadi.
    for soz in ('"Nima sotyapsiz?":"Что продаёте?"',
                '"Narx (so‘m)":"Цена (сум)"',
                '"Tavsif (ixtiyoriy)":"Описание (необязательно)"',
                '"Rasmlar (ixtiyoriy, 5 tagacha)":"Фото (необязательно, до 5)"',
                '"Joylashtirish":"Опубликовать"',
                '"E’lonni tahrirlash":"Редактирование объявления"',
                '"qo‘shish":"добавить"'):
        tekshir(soz in i18n, f"e'lon formasi ruscha lug‘atda bor: {soz.split(':')[0]}")
    tekshir('u.path == "/i18n.js"' in server,
            "server markaziy til faylini uzatadi")
    for name, html in pages.items():
        tekshir('<script src="/i18n.js"></script>' in html,
                f"{name} til tizimiga ulangan")
        tekshir('class="lang-slot"' in html,
                f"{name} til almashtirgich joyiga ega")

    print(f"\nI18N SINOVI: {SON}/{SON}")


if __name__ == "__main__":
    main()
