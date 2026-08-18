#!/usr/bin/env python3
"""Validate Bridge Dental's paired German and Hungarian static pages."""

from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse
import re
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://rhalmaibusiness-blip.github.io/bridge-dental/"

PAIRS = {
    "index.html": "hu/index.html",
    "bridge-dental-kennenlernen.html": "hu/ismerje-meg-a-bridge-dentalt.html",
    "all-on-x-rehabilitationen.html": "hu/full-arch-implantatumos-rehabilitaciok.html",
    "implantatgetragene-zirkonoxidrestaurationen.html": "hu/implantatumos-cirkonium-restauraciok.html",
    "truedent-digitale-prothesen.html": "hu/digitalis-fogsorok.html",
    "digitaler-workflow.html": "hu/digitalis-tervezes.html",
    "metallfreie-keramikrestaurationen.html": "hu/esztetikai-keramia.html",
    "cad-cam-technologie.html": "hu/digitalis-fogtechnika.html",
    "referenzen.html": "hu/referenciak.html",
    "kontakt.html": "hu/kapcsolat.html",
    "impressum.html": "hu/impresszum.html",
    "zusammenarbeit/index.html": "hu/egyuttmukodes/index.html",
}

REDIRECTS = {
    "ismerje-meg-a-bridge-dentalt.html": "bridge-dental-kennenlernen.html",
    "full-arch-implantatumos-rehabilitaciok.html": "all-on-x-rehabilitationen.html",
    "implantatumos-cirkonium-restauraciok.html": "implantatgetragene-zirkonoxidrestaurationen.html",
    "digitalis-fogsorok.html": "truedent-digitale-prothesen.html",
    "digitalis-tervezes.html": "digitaler-workflow.html",
    "esztetikai-keramia.html": "metallfreie-keramikrestaurationen.html",
    "digitalis-fogtechnika.html": "cad-cam-technologie.html",
    "referenciak.html": "referenzen.html",
    "kapcsolat.html": "kontakt.html",
    "egyuttmukodes/index.html": "zusammenarbeit/index.html",
    "rolunk.html": "bridge-dental-kennenlernen.html",
    "rolunk-2.html": "bridge-dental-kennenlernen.html",
    "hu/rolunk.html": "hu/ismerje-meg-a-bridge-dentalt.html",
    "hu/rolunk-2.html": "hu/ismerje-meg-a-bridge-dentalt.html",
}


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html_lang = ""
        self.links: list[dict[str, str]] = []
        self.resources: list[str] = []
        self.ids: set[str] = set()
        self.text_parts: list[str] = []
        self.meta: list[dict[str, str]] = []
        self.in_switcher = 0
        self.skip_text = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        if tag == "html":
            self.html_lang = values.get("lang", "")
        if "id" in values:
            self.ids.add(values["id"])
        if tag in {"style", "svg"}:
            self.skip_text += 1
        if tag == "nav" and "bd-language-switcher" in values.get("class", "").split():
            self.in_switcher += 1
        if tag == "meta":
            self.meta.append(values)
        if tag == "a" and "href" in values:
            values["in_switcher"] = str(bool(self.in_switcher))
            self.links.append(values)
        for attribute in ("src", "poster"):
            if values.get(attribute):
                self.resources.append(values[attribute])
        if values.get("srcset"):
            for item in values["srcset"].split(","):
                self.resources.append(item.strip().split()[0])

    def handle_endtag(self, tag: str) -> None:
        if tag in {"style", "svg"} and self.skip_text:
            self.skip_text -= 1
        if tag == "nav" and self.in_switcher:
            self.in_switcher -= 1

    def handle_data(self, data: str) -> None:
        if not self.skip_text and data.strip():
            self.text_parts.append(" ".join(data.split()))


def local_target(page_path: str, raw_url: str) -> Path | None:
    parsed = urlparse(raw_url)
    if parsed.scheme or parsed.netloc or raw_url.startswith(("mailto:", "tel:", "data:")):
        return None
    path = unquote(parsed.path)
    if not path:
        return ROOT / page_path
    return (ROOT / Path(page_path).parent / path).resolve()


def expected_url(path: str) -> str:
    return BASE_URL + path


def validate_page(path: str, pair: str, language: str, errors: list[str]) -> None:
    source = ROOT / path
    if not source.is_file():
        errors.append(f"{path}: missing page")
        return
    html = source.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(html)

    expected_lang = "de-DE" if language == "de" else "hu-HU"
    if parser.html_lang != expected_lang:
        errors.append(f"{path}: lang={parser.html_lang!r}, expected {expected_lang!r}")

    canonical = re.findall(r'<link\s+rel="canonical"\s+href="([^"]+)"', html)
    if canonical != [expected_url(path)]:
        errors.append(f"{path}: incorrect canonical {canonical}")

    alternates = dict(re.findall(r'<link\s+rel="alternate"\s+hreflang="([^"]+)"\s+href="([^"]+)"', html))
    de_path, hu_path = (path, pair) if language == "de" else (pair, path)
    expected_alternates = {
        "de": expected_url(de_path),
        "hu": expected_url(hu_path),
        "x-default": expected_url(de_path),
    }
    if alternates != expected_alternates:
        errors.append(f"{path}: incorrect hreflang links {alternates}")

    switcher_links = [link for link in parser.links if link.get("in_switcher") == "True"]
    if len(switcher_links) != 2:
        errors.append(f"{path}: expected 2 language-switcher links, found {len(switcher_links)}")
    else:
        by_lang = {link.get("hreflang"): link for link in switcher_links}
        for code, target_path in (("de", de_path), ("hu", hu_path)):
            link = by_lang.get(code)
            target = local_target(path, link.get("href", "")) if link else None
            if not link or target != (ROOT / target_path).resolve():
                errors.append(f"{path}: {code} switcher does not resolve to {target_path}")
            if link and code == language and link.get("aria-current") != "page":
                errors.append(f"{path}: active {code} switcher lacks aria-current=page")

    for link in parser.links:
        href = link.get("href", "")
        parsed = urlparse(href)
        target = local_target(path, href)
        if target is not None and parsed.path and not target.exists():
            errors.append(f"{path}: broken link {href}")
        if not parsed.path and parsed.fragment and parsed.fragment not in parser.ids and href != "#":
            errors.append(f"{path}: missing fragment target {href}")
        if link.get("target") == "_blank" and href.lower().endswith(".pdf"):
            if "noopener" not in link.get("rel", "").split():
                errors.append(f"{path}: PDF link lacks rel=noopener: {href}")
            if "download" in link:
                errors.append(f"{path}: PDF link still has a download attribute: {href}")
        if link.get("in_switcher") != "True" and parsed.path:
            normalized = str(target.relative_to(ROOT)) if target and target.is_relative_to(ROOT) else ""
            if language == "de" and normalized.startswith("hu/"):
                errors.append(f"{path}: German content links to Hungarian page {href}")
            if language == "hu" and normalized in PAIRS:
                errors.append(f"{path}: Hungarian content links to German page {href}")

    for resource in parser.resources:
        target = local_target(path, resource)
        if target is not None and urlparse(resource).path and not target.exists():
            errors.append(f"{path}: missing resource {resource}")

    # Static image paths used by JavaScript-rendered cards are not visible to
    # HTMLParser, so validate those separately as well.
    for resource in re.findall(r"\b(?:logo|src)\s*:\s*['\"]([^'\"]+)['\"]", html):
        if "${" in resource:
            continue
        target = local_target(path, resource)
        if target is not None and not target.exists():
            errors.append(f"{path}: missing JavaScript resource {resource}")

    text = " ".join(parser.text_parts)
    if language == "de":
        for fragment in (
            "ISMERJE MEG", "SZAKTERÜLETEINK", "MUNKALAP", "KAPCSOLATFELVÉTEL",
            "Üzenet küldése", "Adatkezelési tájékoztató", "Még több",
        ):
            if fragment.casefold() in text.casefold():
                errors.append(f"{path}: Hungarian visible text remains: {fragment}")
    else:
        for fragment in (
            "UNSERE LEISTUNGEN", "KONTAKTAUFNAHME", "NACHRICHT SENDEN",
            "DATENSCHUTZHINWEISE", "MEHR LESEN", "WIR SIND SEIT", "WIR ARBEITEN",
            "VIELEN DANK", "SPEZIALIST FÜR", "DIGITALE PLANUNG", "DIGITALE ZAHNTECHNIK",
        ):
            if fragment.casefold() in text.casefold():
                errors.append(f"{path}: German visible text remains: {fragment}")


def validate_redirects(errors: list[str]) -> None:
    for source_path, target_path in REDIRECTS.items():
        source = ROOT / source_path
        if not source.is_file():
            errors.append(f"{source_path}: missing redirect")
            continue
        html = source.read_text(encoding="utf-8")
        if expected_url(target_path) not in html:
            errors.append(f"{source_path}: redirect does not point to {target_path}")


def validate_sitemap(errors: list[str]) -> None:
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.is_file():
        errors.append("sitemap.xml: missing")
        return
    root = ET.parse(sitemap).getroot()
    namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locations = {node.text for node in root.findall("s:url/s:loc", namespace)}
    expected = {expected_url(path) for pair in PAIRS.items() for path in pair}
    if locations != expected:
        errors.append(f"sitemap.xml: expected {len(expected)} paired URLs, found {len(locations)}")


def validate_workorder_links(errors: list[str]) -> None:
    de_pdf = "output/pdf/bridge-dental-munkalap-kitoltheto.pdf"
    hu_pdf = "output/pdf/bridge-dental-munkalap-kitoltheto-hu.pdf"
    counts = {"de": 0, "hu": 0}
    for language, pages, pdf_name in (
        ("de", PAIRS.keys(), de_pdf),
        ("hu", PAIRS.values(), hu_pdf),
    ):
        for path in pages:
            html = (ROOT / path).read_text(encoding="utf-8")
            parser = PageParser()
            parser.feed(html)
            for link in parser.links:
                href = link.get("href", "")
                if href.lower().endswith(".pdf"):
                    target = local_target(path, href)
                    expected = (ROOT / pdf_name).resolve()
                    if target != expected:
                        errors.append(f"{path}: wrong {language} PDF target {href}")
                    counts[language] += 1
    if not all(counts.values()):
        errors.append(f"work-order links missing for a language: {counts}")
    else:
        print(f"Work-order preview links: {counts['de']} German, {counts['hu']} Hungarian")


def main() -> None:
    errors: list[str] = []
    for de_path, hu_path in PAIRS.items():
        validate_page(de_path, hu_path, "de", errors)
        validate_page(hu_path, de_path, "hu", errors)
    validate_redirects(errors)
    validate_sitemap(errors)
    validate_workorder_links(errors)
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors))
        raise SystemExit(1)
    print(f"Validated {len(PAIRS)} German–Hungarian page pairs, redirects, assets and SEO metadata.")


if __name__ == "__main__":
    main()
