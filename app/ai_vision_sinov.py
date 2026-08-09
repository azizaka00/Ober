"""Tarmoq va pullik API chaqirmasdan rasmli qidiruv adapteri testi."""

from __future__ import annotations

import base64
import io
import json
import os
from urllib.error import HTTPError
from unittest.mock import patch

import ai_vision


PNG = b"\x89PNG\r\n\x1a\n" + b"test-image"
DATA = "data:image/png;base64," + base64.b64encode(PNG).decode()


def tekshir(shart: bool, nom: str) -> None:
    if not shart:
        raise AssertionError(nom)
    print(f"  OK  {nom}")


def main() -> None:
    eski = os.environ.pop("OPENAI_API_KEY", None)
    try:
        try:
            ai_vision.tahlil(DATA)
            raise AssertionError("kalitsiz so‘rov to‘xtashi kerak")
        except ai_vision.VisionXato as xato:
            tekshir(xato.kod == "AI_SOZLANMAGAN" and xato.http_kod == 503,
                    "API kalitisiz rasm tashqariga yuborilmaydi")

        os.environ["OPENAI_API_KEY"] = "sinov-kaliti"
        model_javobi = {
            "qidiruv_matni": "Chevrolet Cobalt chap fara",
            "kategoriya": "avto ehtiyot qismlari",
            "mahsulot": "old fara",
            "brend": "Chevrolet",
            "model": "Cobalt",
            "variant": "chap",
            "rang": "",
            "korinadigan_matn": ["GM"],
            "atributlar": ["old tomon"],
            "aniqlashtirish": "",
            "ishonch": 0.91,
        }
        api_javobi = {
            "output": [{"type": "message", "content": [
                {"type": "output_text", "text": json.dumps(model_javobi)}
            ]}]
        }
        with patch.object(ai_vision, "_api_chaqir", return_value=api_javobi) as chaqir:
            natija = ai_vision.tahlil(DATA, "originali kerak")
        tekshir(chaqir.call_count == 1, "vision provider bir marta chaqiriladi")
        tekshir(natija["qidiruv"] == "originali kerak Chevrolet Cobalt chap fara",
                "rasm va matn bitta gibrid so‘rovga birlashadi")
        tekshir(natija["ishonch"] == 0.91 and natija["model"] == "Cobalt",
                "tuzilmali atributlar saqlanadi")

        with patch.object(ai_vision, "_api_chaqir", return_value=api_javobi) as chaqir:
            ikkinchi = ai_vision.tahlil(DATA, "originali kerak")
        tekshir(chaqir.call_count == 0 and ikkinchi == natija,
                "bir xil rasm+matn keshdan olinadi, qayta xarajat yo‘q")

        yomon = "data:image/png;base64," + base64.b64encode(b"not-png").decode()
        try:
            ai_vision._rasmni_tekshir(yomon)
            raise AssertionError("soxta PNG o'tmasligi kerak")
        except ai_vision.VisionXato as xato:
            tekshir(xato.kod == "RASM_BUZILGAN", "MIME emas, fayl signaturasi tekshiriladi")

        noaniq = dict(model_javobi, qidiruv_matni="noaniq buyum",
                      aniqlashtirish="Bu qaysi mahsulot?", ishonch=0.2)
        try:
            ai_vision._tozala(noaniq, "")
            raise AssertionError("ishonchi past rasm ko'r-ko'rona qidirilmasligi kerak")
        except ai_vision.VisionXato as xato:
            tekshir(xato.kod == "AI_NOANIQ" and xato.http_kod == 422,
                    "ishonchi past rasm uchun aniqlashtirish so'raladi")

        kredit_xatosi = HTTPError(
            ai_vision.API_URL,
            429,
            "Too Many Requests",
            {},
            io.BytesIO(json.dumps({
                "error": {
                    "code": "credit_balance_exhausted",
                    "type": "insufficient_quota",
                }
            }).encode()),
        )
        with patch.object(ai_vision, "urlopen", side_effect=kredit_xatosi):
            try:
                ai_vision._api_chaqir({"model": "sinov"})
                raise AssertionError("kredit xatosi aniq ko'rsatilishi kerak")
            except ai_vision.VisionXato as xato:
                tekshir(xato.kod == "AI_KREDIT" and xato.http_kod == 503,
                        "OpenAI krediti tugasa foydalanuvchiga aniq xabar qaytadi")
    finally:
        if eski is None:
            os.environ.pop("OPENAI_API_KEY", None)
        else:
            os.environ["OPENAI_API_KEY"] = eski

    print("\nAI VISION SINOVI: 8/8")


if __name__ == "__main__":
    main()
