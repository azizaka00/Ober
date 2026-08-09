"""
OBER — NARX SAHIFALARI (o'sish dvigateli)

NEGA BU ENG MUHIM ISH:
Thumbtack ham, Carwow ham asosan SHU yo'l bilan o'sgan — yuzlab ming
sahifa: "Denverdagi santexniklar", "sell-my-car/london". Odam Google'da
qidiradi, ularni topadi.

Bizda ular bermaydigan narsa bor: NARX ORALIG'I. OLX "kobalt fara
qancha turadi" degan savolga javob bermaydi — u faqat e'lon ko'rsatadi.
Biz 12 000+ e'londan hisoblab, aniq javob beramiz.

MUHIM TEXNIK SHART: bu sahifalar SERVERDA tayyorlanadi.
Bosh sahifamiz JavaScript bilan chiziladi — Google uni yaxshi
o'qimasligi mumkin. Narx sahifalari esa toza HTML bo'lib chiqadi.

Har sahifa oxirida "Sotuvchilardan so'rash" — ya'ni SEO to'g'ridan-to'g'ri
jonli halqaga ulanadi. Trafik kelib, ketib qolmaydi.
"""

from __future__ import annotations

import html
import time

import baza
import qidiruv
from lugat import QISMLAR

_KESH: dict = {"vaqt": 0.0, "royxat": []}
KESH_UMRI = 3600            # soniya


def _som(n) -> str:
    try:
        return f"{int(n):,}".replace(",", " ") + " so'm"
    except (TypeError, ValueError):
        return "—"


def _slug(model: str, qism: str) -> str:
    """`gaz_ballon` -> `gaz-ballon`. Pastki chiziq manzilda yaramaydi."""
    return f"{model}-{qism}".replace("_", "-").replace(" ", "-")


def _nom(model: str, qism: str) -> str:
    """Ko'rsatiladigan nom: `gaz_ballon` -> `gaz ballon`."""
    return f"{model} {qism}".replace("_", " ")


def _mantiqiymi(model: str, qism: str) -> bool:
    """Soxta juftlikni chiqarib tashlaydi.

    2026-08-02: eng katta "yo'nalish" `gaz + gaz_ballon` chiqdi (344 ta).
    Bu GAZ mashinasining qismi emas — "gaz ballon" so'zidagi "gaz"
    model deb tanilgan. Bunday sahifa Google oldida obro' yo'qotadi.

    Qoida: model nomi qism nomining ichida bo'lsa — bu moslik emas,
    bu bir so'zning ikki marta tanilishi.
    """
    m, q = model.lower(), qism.lower()
    return m not in q and q not in m


def kombinatsiyalar(eng_kam: int = 6, limit: int = 800) -> list[dict]:
    """Sahifa yasashga arziydigan (model + qism) juftliklari.

    Faqat yetarli e'lon bor juftliklar olinadi — aks holda bo'sh
    sahifa yasab, Google oldida obro' yo'qotamiz.
    """
    if _KESH["royxat"] and time.time() - _KESH["vaqt"] < KESH_UMRI:
        return _KESH["royxat"]

    baza.init()
    hisob: dict[tuple[str, str], int] = {}
    with baza.ulan() as c:
        for r in c.execute(
                # SARLAVHADAN tanilgan qism olinadi (`tan_nom_qismlar`),
                # OLX kategoriyasidan emas. Sabab: OLX'ning "Кузовные
                # детали" kabi keng kategoriyasi o'nlab boshqa narsani
                # bitta tegga yig'adi va sahifa aniqligini yo'qotadi.
                "SELECT tan_modellar, tan_nom_qismlar FROM elonlar"
                " WHERE faol=1 AND narx_som IS NOT NULL"
                "   AND tan_modellar <> '' AND tan_nom_qismlar <> ''"):
            modellar = [x for x in (r["tan_modellar"] or "").split(",") if x]
            qismlar = [x for x in (r["tan_nom_qismlar"] or "").split(",") if x]
            for m in modellar[:2]:
                for q in qismlar[:2]:
                    hisob[(m, q)] = hisob.get((m, q), 0) + 1

    royxat = [{"model": m, "qism": q, "soni": n, "slug": _slug(m, q)}
              for (m, q), n in hisob.items()
              if n >= eng_kam and _mantiqiymi(m, q)]
    royxat.sort(key=lambda x: -x["soni"])
    royxat = royxat[:limit]

    _KESH.update(vaqt=time.time(), royxat=royxat)
    return royxat


def slugdan(slug: str) -> tuple[str, str] | None:
    """`kobalt-fara` -> ('kobalt', 'fara'). Faqat mavjud juftlik."""
    for k in kombinatsiyalar():
        if k["slug"] == slug:
            return k["model"], k["qism"]
    return None


# ── HTML ─────────────────────────────────────────────────────────────────────

def _e(s) -> str:
    return html.escape(str(s or ""), quote=True)


_USLUB = """
:root{--navy:#0B2559;--navy2:#081B42;--fon:#FBFBFA;--sirt:#fff;
 --chiziq:#E8E8E6;--matn:#16181D;--kul:#6B7280}
*{box-sizing:border-box}
body{margin:0;background:var(--fon);color:var(--matn);
 font:16px/1.55 -apple-system,"Segoe UI",Roboto,Arial,sans-serif}
a{color:var(--navy)}
header{background:var(--sirt);border-bottom:1px solid var(--chiziq)}
.ic{max-width:860px;margin:0 auto;padding:18px}
.brend{font-weight:800;font-size:22px;letter-spacing:-.5px;
 color:var(--navy);text-decoration:none}
h1{font-size:clamp(24px,4vw,34px);letter-spacing:-.02em;margin:0 0 8px}
h2{font-size:19px;letter-spacing:-.01em;margin:32px 0 12px}
.katta{font-size:clamp(28px,5vw,40px);font-weight:800;color:var(--navy);
 letter-spacing:-.02em;margin:0}
.karta{background:var(--sirt);border:1px solid var(--chiziq);
 border-radius:16px;padding:22px;margin:18px 0}
.olcham{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;
 margin-top:18px;padding-top:16px;border-top:1px solid var(--chiziq)}
.olcham span{display:block;color:var(--kul);font-size:12.5px}
.olcham strong{font-size:17px}
.cta{display:inline-flex;align-items:center;min-height:52px;padding:0 26px;
 background:var(--navy);color:#fff;text-decoration:none;border-radius:13px;
 font-weight:750;font-size:15px}
.cta:hover{background:var(--navy2)}
.rasmlar{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));
 gap:12px;margin:16px 0}
.rasm{background:var(--sirt);border:1px solid var(--chiziq);
 border-radius:13px;overflow:hidden;text-decoration:none;color:inherit;
 display:block}
.rasm img{width:100%;aspect-ratio:4/3;object-fit:cover;display:block;
 background:#f1f1ef}
.rasm .ich{padding:10px 11px}
.rasm .nomi{font-size:13px;line-height:1.35;height:2.7em;overflow:hidden}
.rasm .p{margin-top:6px;font-weight:750;color:var(--navy);font-size:14.5px}
.rasm .j{color:var(--kul);font-size:11.5px;margin-top:2px}
table{width:100%;border-collapse:collapse;font-size:14.5px}
td,th{text-align:left;padding:10px 8px;border-bottom:1px solid var(--chiziq)}
th{color:var(--kul);font-size:12.5px;font-weight:600}
.narx{font-weight:700;white-space:nowrap}
.chip{display:inline-block;margin:0 6px 6px 0;padding:6px 12px;
 background:#eef2f9;color:var(--navy);border-radius:99px;
 font-size:13px;text-decoration:none}
footer{color:var(--kul);font-size:13px;padding:30px 18px 50px;
 max-width:860px;margin:0 auto}
"""


def _qobiq(sarlavha: str, tavsif: str, tana: str, kanonik: str) -> bytes:
    return f"""<!DOCTYPE html>
<html lang="uz"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{_e(sarlavha)}</title>
<meta name="description" content="{_e(tavsif)}">
<link rel="canonical" href="https://ober.uz{_e(kanonik)}">
<meta property="og:title" content="{_e(sarlavha)}">
<meta property="og:description" content="{_e(tavsif)}">
<meta property="og:type" content="website">
<style>{_USLUB}</style>
</head><body>
<header><div class="ic"><a class="brend" href="/">ober</a></div></header>
<main class="ic">{tana}</main>
<footer>OBER — nima kerak bo'lsa, topamiz. Narxlar ochiq e'lonlardan
hisoblangan va o'zgarishi mumkin.</footer>
</body></html>""".encode()


def narx_sahifasi(model: str, qism: str) -> bytes | None:
    """Bitta (model + qism) uchun narx sahifasi."""
    d = qidiruv.qidir(f"{model} {qism}", limit=12)
    if not d.get("natijalar"):
        return None

    nom = _nom(model, qism).title()
    sarlavha = f"{nom} narxi — O'zbekiston | OBER"
    tavsif = (f"{nom}: {d.get('jami', 0)} ta taklif, "
              f"{_som(d.get('eng_arzon'))} dan boshlab. "
              f"Bugun kimda borligini sotuvchilardan so'rang.")

    # RASMLI KARTALAR — sahifaning yuzi.
    # Rasmsiz sahifa Google'da ham, odam ko'zida ham zaif. Bizda rasm
    # bor (yangi parserdan keyin ~98%), ishlatmaslik ahmoqlik bo'lardi.
    rasmlilar = [x for x in d["natijalar"] if x.get("rasm")][:8]
    kartalar = "".join(
        f"<a class='rasm' href='{_e(x.get('havola') or '#')}'"
        f"   target='_blank' rel='noopener nofollow'>"
        f"<img src='{_e(x['rasm'])}' loading='lazy'"
        f"     alt='{_e(x['nom'])[:80]}'>"
        f"<div class='ich'><div class='nomi'>{_e(x['nom'])[:60]}</div>"
        f"<div class='p'>{_som(x.get('narx_som'))}</div>"
        f"<div class='j'>{_e(x.get('joy_nom') or '')}</div></div></a>"
        for x in rasmlilar)
    rasm_bloki = (f"<h2>Bozordagi namunalar</h2>"
                  f"<div class='rasmlar'>{kartalar}</div>") if kartalar else ""

    qatorlar = "".join(
        f"<tr><td>{_e(x['nom'])[:70]}</td>"
        f"<td>{_e(x.get('joy_nom') or '')}</td>"
        f"<td class='narx'>{_som(x.get('narx_som'))}</td></tr>"
        for x in d["natijalar"][:12])

    # Ichki havolalar — Google sahifalarni shular orqali topadi
    boshqalar = [k for k in kombinatsiyalar()
                 if k["model"] == model and k["qism"] != qism][:8]
    boshqalar += [k for k in kombinatsiyalar()
                  if k["qism"] == qism and k["model"] != model][:8]
    havolalar = "".join(
        f"<a class='chip' href='/narx/{_e(k['slug'])}'>"
        f"{_e(_nom(k['model'], k['qism']).title())}</a>" for k in boshqalar)

    tana = f"""
<h1>{_e(nom)} narxi</h1>
<p style="color:var(--kul);margin:0 0 18px">
O'zbekistondagi ochiq e'lonlardan hisoblangan. Yangilandi: bugun.</p>

<div class="karta">
  <p style="color:var(--kul);font-size:12.5px;margin:0 0 6px;
     letter-spacing:.06em;text-transform:uppercase">Hozirgi takliflar</p>
  <p class="katta">{_som(d.get('eng_arzon'))} dan</p>
  <p style="color:var(--kul);font-size:13px;margin:6px 0 0">
     Narxlar e'lon egalari tomonidan qo'yilgan. O'rtacha hisoblamaymiz —
     hammasini ko'rsatamiz, tanlash sizda.</p>
  <div class="olcham">
    <div><span>Takliflar</span><strong>{d.get('jami', 0)} ta</strong></div>
    <div><span>Narxi ko'rsatilgan</span><strong>{d.get('narxli_soni', 0)} ta</strong></div>
    <div><span>Manba</span><strong>Ochiq e'lonlar</strong></div>
  </div>
</div>

<div class="karta" style="border-color:#cbd5e5;background:linear-gradient(180deg,#f6f9ff,#fff)">
  <h2 style="margin:0 0 6px">Bugun aniq kerakmi?</h2>
  <p style="color:var(--kul);margin:0 0 16px">
    Yuqoridagi narxlar e'lonlardan. Hozir kimda borligini va qanchaga
    berishini sotuvchilarning o'zidan so'raymiz — telefon raqami
    so'ralmaydi.</p>
  <a class="cta" href="/?q={_e(model)}+{_e(qism)}">Sotuvchilardan so'rash</a>
</div>

{rasm_bloki}

<h2>Hozirgi takliflar</h2>
<table><tr><th>Nomi</th><th>Joyi</th><th>Narxi</th></tr>{qatorlar}</table>

<h2>Boshqa narxlar</h2>
<div>{havolalar}</div>
"""
    return _qobiq(sarlavha, tavsif, tana, f"/narx/{model}-{qism}")


def royxat_sahifasi() -> bytes:
    k = kombinatsiyalar()
    guruh: dict[str, list] = {}
    for x in k:
        guruh.setdefault(x["model"], []).append(x)

    bolaklar = []
    for model in sorted(guruh):
        ichi = "".join(
            f"<a class='chip' href='/narx/{_e(x['slug'])}'>"
            f"{_e(x['qism'].replace('_', ' '))} "
            f"<span style='color:var(--kul)'>{x['soni']}</span></a>"
            for x in sorted(guruh[model], key=lambda y: -y["soni"]))
        bolaklar.append(f"<h2>{_e(model.title())}</h2><div>{ichi}</div>")

    tana = (f"<h1>Narxlar ma'lumotnomasi</h1>"
            f"<p style='color:var(--kul)'>{len(k)} ta yo'nalish bo'yicha "
            f"O'zbekistondagi odatiy narxlar.</p>" + "".join(bolaklar))
    return _qobiq("Avto ehtiyot qismlar narxi — O'zbekiston | OBER",
                  "Model va qism bo'yicha odatiy narxlar, ochiq e'lonlardan "
                  "hisoblangan.", tana, "/narx")


def sitemap() -> bytes:
    k = kombinatsiyalar()
    yollar = ["/", "/narx"] + [f"/narx/{x['slug']}" for x in k]
    ichi = "".join(
        f"<url><loc>https://ober.uz{y}</loc>"
        f"<changefreq>daily</changefreq></url>" for y in yollar)
    return (f'<?xml version="1.0" encoding="UTF-8"?>'
            f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            f'{ichi}</urlset>').encode()


def robots() -> bytes:
    return (b"User-agent: *\nAllow: /\n"
            b"Sitemap: https://ober.uz/sitemap.xml\n")
