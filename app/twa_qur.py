"""OBER — Play Store uchun TWA paketini quradi.

NEGA BU SKRIPT BOR (2026-08-14)
-------------------------------
`bubblewrap init` va `bubblewrap build` — interaktiv wizard. Ular
ichida `inquirer` ishlatadi, `inquirer` esa `process.stdin.isTTY`
ni tekshiradi.

Avtomatik skriptdan ishga tushirilganda stdin quvurga ulanadi,
`isTTY` false bo'ladi va wizard savolni cheksiz qayta chizadi —
jurnal ANSI boshqaruv belgilari bilan to'ladi (`30D`, `30C`) va
jarayon osilib qoladi. Muammo kodda emas, muhitda edi.

`yes | bubblewrap` ham yordam bermaydi: quvur ham TTY ni yo'q
qiladi. Ya'ni javobni "yuborib" bo'lmaydi — TTY berish kerak.

YECHIM: `TWA-QUR.bat` ni ikki marta bosib oching. Ochilgan cmd
oynasi haqiqiy konsol. Bu skript bubblewrap'ni chaqirganda
`subprocess` bolaga stdin/stdout'ni MEROS qoldiradi — demak
bubblewrap o'sha haqiqiy TTY'ni ko'radi va normal ishlaydi.
Shuning uchun bu yerda `capture_output` ISHLATILMAYDI: chiqishni
ushlab qolsak, TTY yana yo'qoladi va muammo qaytadi.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ILDIZ = Path(__file__).resolve().parent.parent
LOYIHA = ILDIZ / "twa-ober"
PAROLFAYL = LOYIHA / "parol.txt"

# Bubblewrap o'zi yuklab olgan vositalar. Yo'l boshqacha bo'lsa
# shu ikki qatorni tuzating.
JDK = Path(r"C:\Users\PC\.bubblewrap\jdk\jdk-17.0.20+8")
SDK = Path(r"C:\Users\PC\.bubblewrap\android_sdk")


def chiziq(belgi: str = "-") -> None:
    print(belgi * 60)


def tekshir() -> str | None:
    """Qurishdan oldingi shartlar. Xato bo'lsa matn qaytaradi."""
    if not (JDK / "bin" / "java.exe").is_file():
        return (f"JDK topilmadi:\n  {JDK}\n"
                "Yo'l boshqacha bo'lsa app/twa_qur.py boshida tuzating.")
    if not (LOYIHA / "twa-manifest.json").is_file():
        return f"twa-manifest.json topilmadi:\n  {LOYIHA}"
    if not (LOYIHA / "android.keystore").is_file():
        return (f"android.keystore topilmadi:\n  {LOYIHA}\n"
                "Kalitsiz paket imzolanmaydi va Play qabul qilmaydi.")
    return None


def parol_togrimi(parol: str) -> bool:
    """Parolni QURISHDAN OLDIN tekshiradi.

    2026-08-14 saboqi: parol faqat eng oxirgi qadamda — `apksigner`
    imzolayotganda — tekshirilardi. Gradle 5 daqiqa ishlab, hamma
    narsa muvaffaqiyatli tugab, keyin `keystore password was
    incorrect` chiqardi. Butun qurish behuda ketdi.

    `keytool -list` bir soniyada javob beradi. Xato parolni shu
    yerda ushlash — bepul.
    """
    natija = subprocess.run(
        [str(JDK / "bin" / "keytool.exe"), "-list",
         "-keystore", str(LOYIHA / "android.keystore"),
         "-storepass", parol, "-alias", "ober"],
        capture_output=True, text=True)
    return natija.returncode == 0


def parol_ol() -> str | None:
    """Parolni fayldan yoki so'rab oladi va DARHOL tekshiradi."""
    if PAROLFAYL.is_file():
        p = PAROLFAYL.read_text(encoding="utf-8").strip()
        if p and parol_togrimi(p):
            print(f"Parol {PAROLFAYL.name} dan olindi va tekshirildi.")
            return p
        if p:
            print(f"OGOHLANTIRISH: {PAROLFAYL} dagi parol noto'g'ri.")
            print()

    print("Keystore paroli kerak.")
    print("Har safar so'ralmasligi uchun uni bitta satr qilib shu")
    print(f"faylga saqlang: {PAROLFAYL}")
    print("Bu fayl git'ga tushmaydi (.gitignore da yozilgan).")
    print()

    for urinish in range(1, 4):
        parol = input(f"Parol ({urinish}/3): ").strip()
        if not parol:
            continue
        if parol_togrimi(parol):
            print("Parol to'g'ri.")
            return parol
        print("Parol noto'g'ri — kalit ochilmadi.")
        if urinish == 1:
            print("Eslatma: kalit `keytool -genkeypair` bilan yaratilganda")
            print("qaysi `-storepass` berilgan bo'lsa, o'sha kerak.")
        print()
    return None


def main() -> int:
    chiziq("=")
    print("  OBER — Play Store uchun paket qurish")
    chiziq("=")
    print()

    xato = tekshir()
    if xato:
        print("XATO:", xato)
        return 1

    parol = parol_ol()
    if not parol:
        print()
        print("XATO: to'g'ri parol kiritilmadi — qurish boshlanmadi.")
        print("Gradle'ni behuda yugurtirmaslik uchun shu yerda to'xtadik.")
        return 1

    muhit = os.environ.copy()
    muhit["JAVA_HOME"] = str(JDK)
    muhit["ANDROID_HOME"] = str(SDK)
    muhit["ANDROID_SDK_ROOT"] = str(SDK)
    muhit["PATH"] = str(JDK / "bin") + os.pathsep + muhit.get("PATH", "")
    # Bu ikki nom bubblewrap'ning build.js kodidan olingan — parol shu
    # yo'l bilan berilsa u parol so'ramaydi (bitta interaktiv savol kamayadi).
    muhit["BUBBLEWRAP_KEYSTORE_PASSWORD"] = parol
    muhit["BUBBLEWRAP_KEY_PASSWORD"] = parol

    print()
    print("Qurish boshlanmoqda. Birinchi marta Gradle va Android")
    print("build-tools yuklanadi — bu bir necha daqiqa vaqt oladi.")
    print()
    print("DIQQAT — bubblewrap bitta savol beradi:")
    print("    would you like to regenerate your project?  Y/n")
    print("Javob:  y  keyin Enter.")
    print()
    print("Bu savol shu oynada normal ishlaydi, chunki bu haqiqiy")
    print("konsol. Avtomatik skriptda ishlamas edi — sabab yuqorida.")
    chiziq()
    print()

    try:
        # `shell=True` — Windows'da `bubblewrap` npm shim'i (.cmd) bo'ladi.
        # Chiqish USHLANMAYDI: bola stdin/stdout'ni meros oladi va TTY
        # saqlanadi. Aynan shu narsa muammoni hal qiladi.
        natija = subprocess.run("bubblewrap build", shell=True,
                                cwd=str(LOYIHA), env=muhit)
    except KeyboardInterrupt:
        print("\nTo'xtatildi.")
        return 1
    except OSError as e:
        print(f"\nXATO: bubblewrap ishga tushmadi: {e}")
        print("O'rnatilganmi? Tekshiring:  npm i -g @bubblewrap/cli")
        return 1

    print()
    chiziq()
    aab = LOYIHA / "app-release-bundle.aab"
    apk = LOYIHA / "app-release-signed.apk"

    if not aab.is_file():
        print("QURISH TUGAMADI.")
        print(f"bubblewrap chiqish kodi: {natija.returncode}")
        print()
        print("Ko'p uchraydigan sabablar:")
        print("  1. Android SDK litsenziyasi qabul qilinmagan.")
        print("  2. Internet uzilgan — Gradle yuklab ololmagan.")
        print("  3. Java xotirasi yetmagan.")
        print()
        print("Parol EMAS — u qurishdan oldin tekshirilgan.")
        return 1

    print("  TAYYOR")
    chiziq()
    print()
    print("Play Console'ga yuklanadigan fayl:")
    print(f"  {aab}   ({aab.stat().st_size // 1024} KB)")
    if apk.is_file():
        print()
        print("Telefonda sinash uchun (ixtiyoriy):")
        print(f"  {apk}   ({apk.stat().st_size // 1024} KB)")
    print()
    print("KEYINGI QADAM — assetlinks.json.")
    print("Usiz ilova ochilganda tepada brauzer manzil satri ko'rinib")
    print("turadi va ilova veb-saytga o'xshab qoladi. Xato xabari")
    print("chiqmaydi — shunchaki ishlamaydi.")
    print()
    print("  Play Console -> Test and release -> Setup -> App signing")
    print("  SHA-256 ni nusxa oling, keyin ASSETLINKS.bat ni oching.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
