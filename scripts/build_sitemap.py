#!/usr/bin/env python3
"""Generate the bilingual Bridge Dental sitemap with reciprocal alternates."""

from pathlib import Path
from xml.sax.saxutils import escape


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://rhalmaibusiness-blip.github.io/bridge-dental/"
PAIRS = [
    ("index.html", "hu/index.html"),
    ("bridge-dental-kennenlernen.html", "hu/ismerje-meg-a-bridge-dentalt.html"),
    ("all-on-x-rehabilitationen.html", "hu/full-arch-implantatumos-rehabilitaciok.html"),
    ("implantatgetragene-zirkonoxidrestaurationen.html", "hu/implantatumos-cirkonium-restauraciok.html"),
    ("truedent-digitale-prothesen.html", "hu/digitalis-fogsorok.html"),
    ("digitaler-workflow.html", "hu/digitalis-tervezes.html"),
    ("metallfreie-keramikrestaurationen.html", "hu/esztetikai-keramia.html"),
    ("cad-cam-technologie.html", "hu/digitalis-fogtechnika.html"),
    ("referenzen.html", "hu/referenciak.html"),
    ("kontakt.html", "hu/kapcsolat.html"),
    ("impressum.html", "hu/impresszum.html"),
    ("zusammenarbeit/index.html", "hu/egyuttmukodes/index.html"),
]


def url_entry(location: str, de_path: str, hu_path: str) -> str:
    de_url = escape(BASE_URL + de_path)
    hu_url = escape(BASE_URL + hu_path)
    return "\n".join(
        (
            "  <url>",
            f"    <loc>{escape(BASE_URL + location)}</loc>",
            f'    <xhtml:link rel="alternate" hreflang="de" href="{de_url}"/>',
            f'    <xhtml:link rel="alternate" hreflang="hu" href="{hu_url}"/>',
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{de_url}"/>',
            "  </url>",
        )
    )


entries = [url_entry(path, de_path, hu_path) for de_path, hu_path in PAIRS for path in (de_path, hu_path)]
document = "\n".join(
    (
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
        *entries,
        "</urlset>",
        "",
    )
)
(ROOT / "sitemap.xml").write_text(document, encoding="utf-8")
print(f"Created sitemap.xml with {len(entries)} bilingual URLs.")
