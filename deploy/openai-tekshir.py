"""OBER OpenAI ulanishini maxfiy kalitni chiqarmasdan tekshiradi.

Bir dona juda kichik Responses API so'rovi yuboradi. Natijada faqat HTTP
holati va OpenAI xato kodi/turi chiqariladi; API kaliti hech qachon loglanmaydi.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ENV_FAYL = Path("/etc/ober-ai.env")


def _env_oqi() -> None:
    if not ENV_FAYL.exists():
        raise SystemExit("ENV_FILE=MISSING")
    for xom in ENV_FAYL.read_text(encoding="utf-8-sig").splitlines():
        qator = xom.strip()
        if not qator or qator.startswith("#") or "=" not in qator:
            continue
        nom, qiymat = qator.split("=", 1)
        os.environ.setdefault(nom.strip(), qiymat.strip())


def main() -> None:
    _env_oqi()
    kalit = (os.environ.get("OPENAI_API_KEY") or "").strip()
    model = (os.environ.get("OBER_VISION_MODEL") or "gpt-5.6-luna").strip()
    if not kalit:
        raise SystemExit("OPENAI_API_KEY=MISSING")

    tana = json.dumps(
        {
            "model": model,
            "input": "Return only OK.",
            "max_output_tokens": 64,
            "store": False,
        }
    ).encode("utf-8")
    sorov = Request(
        "https://api.openai.com/v1/responses",
        data=tana,
        headers={
            "Authorization": f"Bearer {kalit}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urlopen(sorov, timeout=30) as javob:  # noqa: S310 - fixed HTTPS URL
            natija = json.loads(javob.read(512 * 1024).decode("utf-8"))
            print(f"HTTP={javob.status}")
            print(f"MODEL={natija.get('model') or model}")
            print("OPENAI=READY")
    except HTTPError as xato:
        try:
            tana = json.loads(xato.read(512 * 1024).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            tana = {}
        tafsilot = tana.get("error") if isinstance(tana, dict) else {}
        tafsilot = tafsilot if isinstance(tafsilot, dict) else {}
        print(f"HTTP={xato.code}")
        print(f"ERROR_CODE={tafsilot.get('code') or 'UNKNOWN'}")
        print(f"ERROR_TYPE={tafsilot.get('type') or 'UNKNOWN'}")
        print("OPENAI=NOT_READY")
        raise SystemExit(2) from None
    except (URLError, TimeoutError, OSError) as xato:
        print(f"NETWORK_ERROR={type(xato).__name__}")
        print("OPENAI=NOT_READY")
        raise SystemExit(3) from None


if __name__ == "__main__":
    main()
