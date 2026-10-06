#!/usr/bin/env python3
"""Regression checks for the October HU/DE content and hero updates."""
from html import unescape
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
checks = 0


def check(condition, message):
    global checks
    checks += 1
    assert condition, message


def source(name):
    return (ROOT / name).read_text(encoding="utf-8")


def visible(html):
    html = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", "", html, flags=re.S)
    return " ".join(unescape(re.sub(r"<[^>]*>", " ", html)).split())


def section(html, selector):
    return re.search(r'<section\b[^>]*' + selector + r'[^>]*>.*?</section>', html, re.S).group()


home = source("index.html")
about = source("bridge-dental-kennenlernen.html")
contact = source("kontakt.html")
required = {
    "index.html": [
        "Wo digitale Technologie auf fachliche Erfahrung trifft.",
        "Warum unsere Partner mit uns arbeiten.",
        "Seit der Gründung von Bridge Dental arbeiten wir mit Partnerpraxen in Deutschland und Österreich zusammen.",
        "zur Unterstützung stabiler, langfristiger Ergebnisse.",
        "In der Praxis bedeutet das weniger unerwartete Situationen.",
        "damit von der Planung bis zur Umsetzung jedes Detail klar ist.",
        "Den Versand nach Deutschland und in die Schweiz",
        "Dokumentierte Qualität und Sicherheit",
        "UNSERE AUFTRAGGEBER", "Unsere Fachgebiete",
        "All-on-X- / Full-Arch-Rehabilitationen",
        "Präzise Planung, stabile Konstruktion", "Stabile Basis, natürliche Ästhetik.",
        "Präzise und reproduzierbare digitale Prothesen",
        "Mit der TrueDent-Technologie von Stratasys entstehen Prothesenbasis und Zähne",
        "Präzise Informationen, abgestimmte Zusammenarbeit",
        "Natürliche Ästhetik, individueller Charakter",
        "Veneers, Kronen, Inlays und Onlays aus Lithiumdisilikat",
        "Eigene digitale Fertigung", "Jedes Detail zählt.",
        "Digitale Planungen, Fertigungsdaten und verwendete Materialien sind dokumentiert und rückverfolgbar.",
        "Eine Auswahl unserer Arbeiten",
        "Ihr Behandlungskonzept, unsere zahntechnische Kompetenz.",
        "ARBEITSAUFTRAG HERUNTERLADEN",
    ],
    "bridge-dental-kennenlernen.html": [
        "Zahntechnischer Rückhalt, auf den Ihre Praxis langfristig bauen kann.",
        "Von der Diagnose bis zur Übergabe der definitiven Restauration",
        "Konsequente Qualität", "Verlässliche Zusammenarbeit",
        "Wir klären offene Fragen vor der Fertigung",
        "Schon vor der Gründung von Bridge Dental", "25+",
        "Gute Zahntechnik ist das Ergebnis gemeinsamer Arbeit.",
        "Unsere fachlichen Grundsätze", "Gemeinsame Planung",
        "Wir denken in digitalen Systemen",
        "Eine wirklich gute Restauration fällt nicht als solche auf.",
        "ein konsequent reproduzierbares fachliches Niveau.",
        "Langfristige Zusammenarbeit",
        "Dokumentierte, verlässliche Materialsysteme",
        "Materialauswahl passend zu Indikation und Konstruktion",
        "Fachliche Anerkennung", "unter 49 Teilnehmenden aus 16 Ländern den 6. Platz.",
        "Wissen gehört genauso zur Entwicklung wie Technologie.",
        "ICDE-Partnerlabor", "Interne fachliche Weiterbildung",
        "Internationale fachliche Präsenz",
        "Mehr als zwei Jahrzehnte internationale Zusammenarbeit.",
        "Verlässliche Zusammenarbeit – auch über mehrere Hundert Kilometer",
        "keine gesonderte „internationale Dienstleistung“",
        "Deutschsprachige fachliche Kommunikation",
        "Lernen wir uns bei einem Fachgespräch kennen.", "FACHGESPRÄCH ANFRAGEN",
    ],
    "kontakt.html": [
        "Besprechen wir, wie wir Sie unterstützen können.",
        "Sie haben einen konkreten Fall oder suchen einen langfristigen Laborpartner?",
        "Fachliche Abstimmung und Kommunikation auf Deutsch",
        "Rechnungsstellung, Monatsabrechnungen und Bescheinigungen",
        "Deutschsprachige Kundenbetreuung", "Bridge Dental Dentallabor",
        "Schreiben Sie uns, wobei Sie auf uns zählen möchten.",
        "Ein Mitglied unseres Teams wird sich mit Ihnen in Verbindung setzen.",
        "Allgemeine Zusammenarbeit",
    ],
}
for path, phrases in required.items():
    html = source(path)
    text = visible(html)
    for phrase in phrases:
        check(phrase in text, f"{path}: missing {phrase}")
    check(len(re.findall(r"<h1\b", html)) == 1, f"{path}: h1 count")
    ids = re.findall(r'\bid="([^"]+)"', html)
    check(len(ids) == len(set(ids)), f"{path}: duplicate IDs")
    for script in re.findall(r"<script(?![^>]*\bsrc=)[^>]*>(.*?)</script>", html, re.S):
        result = subprocess.run(["node", "-e", "new(require('vm').Script)(require('fs').readFileSync(0,'utf8'))"], input=script, text=True, capture_output=True)
        check(result.returncode == 0, f"{path}: JavaScript syntax: {result.stderr}")

for name in ["index.html", "hu/index.html"]:
    html = source(name)
    check('cinematic-shell home-hero' in html, f"{name}: hero scope")
    check('assets/home/hero-layout.css?v=20261006' in html, f"{name}: shared hero layout")
    check('hero-ska-4081.webp' in html, f"{name}: hero photograph")
    check('service-metal-free-ceramics-0014.webp' in html, f"{name}: ceramics photograph")
    check(html.index('id="miert"') < html.index('id="velemenyek"') < html.index('class="partner-cta"') < html.index('id="technologia"'), f"{name}: reviews and CTA placement")
    check(len(re.findall(r'class="service-kicker"', html)) == 6, f"{name}: six specialty subtitles")

check('id="innovacio"' not in about and 'MILESTONES' not in about, "About: removed innovation timeline")
development = section(about, 'id="fejlodes"')
check(re.findall(r'<h3>(.*?)</h3>', development) == ['ICDE-Partnerlabor', 'Interne fachliche Weiterbildung', 'Internationale fachliche Präsenz'], "About: development order")
check('<a ' not in section(about, 'id="nemzetkozi-tapasztalat"'), "About: old international CTA")
check(about.index('id="kulisszak-mogott"') < about.index('class="section about-contact"') < about.index('<footer'), "About: final CTA placement")
check('object-fit: contain;' in about[about.index('.hitvallas-photo-filled img'):about.index('.story-placeholder-ring')], "About: founder image fit")
check(len(re.findall(r'class="offer-item"', section(about, 'id="mashogy"'))) == 3, "About: three material claims")
main = re.search(r'<main>(.*?)</main>', contact, re.S).group(1)
check(main.count('href="tel:+36703966653"') == 1, "Contact: no duplicate Attila phone")
form = re.search(r'<form>(.*?)</form>', contact, re.S).group(1)
check(re.findall(r'<(?:input|select|textarea)\b[^>]*\bid="([^"]+)"', form) == ['nev','rendelo','email','telefon','targy','uzenet'], "Contact: six fields")
check('B2B-Laborpartner' not in main, "Contact: old badge removed")
print(f"Validated {checks} October content, structure and JavaScript checks.")
