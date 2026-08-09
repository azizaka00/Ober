"""Mavjud OLX yig‘uvchisini umumiy adapter interfeysiga ulaydi."""

from __future__ import annotations

import olx as eski_olx

MANBA = eski_olx.MANBA
NOM = eski_olx.NOM
KUTISH = eski_olx.KUTISH


def bosh(cheklov: int = 1, faqat: str = "") -> dict:
    """Eng yangi sahifalarni oladi; boshqa e’lonlarni nofaol qilmaydi."""
    return eski_olx.main(max(1, cheklov), faqat, toliq=False)


def chuqur(sahifalar: int = 25, faqat: str = "") -> dict:
    """Barcha viloyatlarni chuqur yig‘adi va faollik siklini yakunlaydi."""
    return eski_olx.main(max(1, sahifalar), faqat, toliq=not bool(faqat))
