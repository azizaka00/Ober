"""OBER O‘zbek/Rus interfeys poydevori uchun tez regressiya testi."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


def tekshir(shart: bool, nom: str) -> None:
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
    tekshir('"Siz yozasiz. Bozor javob beradi.":"Вы пишете. Рынок отвечает."' in i18n,
            "bosh sahifa ruscha lug‘atda bor")
    tekshir('"Sotuvchi sifatida boshlang":"Начать как продавец"' in i18n,
            "sotuvchi onboarding ruscha lug‘atda bor")
    tekshir('"Bildirishnomalar":"Уведомления"' in i18n,
            "chat va notification ruscha lug‘atda bor")
    tekshir('MutationObserver' in i18n,
            "API dan keyin chizilgan dinamik matn ham tarjima qilinadi")
    tekshir('u.path == "/i18n.js"' in server,
            "server markaziy til faylini uzatadi")
    for name, html in pages.items():
        tekshir('<script src="/i18n.js"></script>' in html,
                f"{name} til tizimiga ulangan")
        tekshir('class="lang-slot"' in html,
                f"{name} til almashtirgich joyiga ega")

    print("\nI18N SINOVI: 13/13")


if __name__ == "__main__":
    main()
