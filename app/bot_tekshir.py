"""Telegram token va bot holatini tekshiradi. Tokenni EKRANGA CHIQARMAYDI."""

from __future__ import annotations

import baza
import tg


def main() -> None:
    fayl = baza.DB.with_name(tg.TOKEN_FAYL)
    t = tg.token()

    print("=" * 60)
    print("  OBER — Telegram bot tekshiruvi")
    print("=" * 60)
    print(f"\n  Token fayli: {fayl}")

    if not t:
        print("  Token: YO'Q\n")
        print("  Nima qilish kerak:")
        print("   1. Telegramda @BotFather -> /newbot")
        print("   2. Bot nomi 'bot' bilan tugasin (masalan: ober_uz_bot)")
        print("   3. Berilgan tokenni shu faylga bitta qator qilib saqlang:")
        print(f"      {fayl}\n")
        return

    print(f"  Token: BOR ({len(t)} belgi)")
    nom = tg.bot_nomi()
    if nom:
        print(f"  Bot: @{nom}")
        print("  Telegram bilan aloqa: ISHLAYAPTI\n")
    else:
        print("  Bot: aloqa yo'q")
        print("  Token noto'g'ri bo'lishi yoki internet yopiq bo'lishi mumkin.\n")
        return

    with baza.ulan() as c:
        jami = c.execute("SELECT COUNT(*) n FROM sotuvchilar").fetchone()["n"]
        ulangan = c.execute("SELECT COUNT(*) n FROM sotuvchilar"
                            " WHERE telegram_id IS NOT NULL").fetchone()["n"]
    print(f"  Sotuvchilar: {jami} ta, Telegramga ulangani: {ulangan} ta\n")


if __name__ == "__main__":
    main()
