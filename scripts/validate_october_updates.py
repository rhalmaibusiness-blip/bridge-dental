#!/usr/bin/env python3
"""Regression checks for the October HU/DE content and hero updates."""
from html import unescape
from pathlib import Path
import re
import subprocess
from html.parser import HTMLParser
from validate_bilingual_site import PAIRS, local_target

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
        "Schreiben Sie uns, wie wir Sie unterstützen können.",
        "Ein Mitglied unseres Teams wird sich mit Ihnen in Verbindung setzen.",
        "Allgemeine Zusammenarbeit",
    ],
    "hu/full-arch-implantatumos-rehabilitaciok.html": [
        "FULL-ARCH / ALL-ON-X",
        "Fogtechnikai háttér komplex implantációs rehabilitációkhoz.",
        "A tervezéstől a végleges restaurációig összehangolt digitális munkafolyamattal és saját gyártási háttérrel támogatjuk a teljes íves implantációs eseteket.",
        "Összehangolt digitális workflow a tervezéstől a végleges restaurációig",
        "Egy Full-Arch rehabilitációnál a pontos végeredményhez már a tervezés előtt megfelelő információkra van szükség. Ezért a beérkező adatokat ellenőrizzük, a kezelési koncepciót egyeztetjük, majd a tervezés, a prototípus és a végleges restauráció egymásra épülő digitális munkafolyamatban készül.",
        "Nyitott digitális együttműködés",
        "A rendelők különböző digitális rendszereiből érkező adatokkal is tudunk dolgozni. A beérkező információkat a tervezés előtt ellenőrizzük, és szükség esetén egyeztetjük a kezelőorvossal.",
        "A tervezéshez szükséges információk",
        "Full-Arch eseteknél a tervezés többféle klinikai és digitális információ összehangolására épül. A scanadatokat a harapási információkkal, fotókkal, videókkal, valamint az esztétikai és funkcionális paraméterekkel együtt értékeljük.",
        "A klinikai helyzetnek és a választott restaurációs koncepciónak megfelelően többféle Full-Arch megoldást készítünk:",
        "monolitikus teljes cirkónium restaurációk", "titánbázisú (Ti-Base) restaurációk",
        "titán iBar-ra épülő cirkónium restaurációk", "Toronto Bridge megoldások", "PMMA ideiglenes restaurációk",
        "A megfelelő restaurációs koncepció kiválasztását a kezelőorvossal közösen egyeztetjük.",
        "MIÉRT BRIDGE DENTAL?", "Komplex Full-Arch esetek, összehangolt szakmai háttérrel.",
        "A teljes íves implantációs rehabilitációknál a pontos információ, a közös tervezés és az összehangolt gyártási folyamat különösen fontos.",
        "01 – Közös tervezés",
        "Komplex eseteknél a gyártás előtt ellenőrizzük a rendelkezésre álló információkat, és szükség esetén egyeztetünk a kezelőorvossal.",
        "02 – Saját digitális gyártás",
        "A restaurációk tervezése és gyártása saját digitális rendszerünkben történik, így a munkafolyamat egyes lépései házon belül kontrollálhatók.",
        "03 – Funkció és esztétika együtt",
        "A restauráció kialakításánál a biomechanikai követelményeket, a rendelkezésre álló helyet és az esztétikai szempontokat egyaránt figyelembe vesszük.",
        "04 – Kiszámítható együttműködés",
        "Átlátható munkafolyamat, közvetlen szakmai kommunikáció és következetes minőségellenőrzés támogatja az esetek végigvitelét.",
        "A megfelelő restaurációs koncepció kiválasztása",
        "Nem minden Full-Arch rehabilitáció igényel azonos restaurációs megoldást.",
        "A megfelelő konstrukció kiválasztásánál figyelembe vesszük az implantátumok helyzetét, a rendelkezésre álló protetikai teret, a biomechanikai követelményeket, valamint a funkcionális és esztétikai szempontokat.",
        "A lehetséges restaurációs koncepciókat már a tervezési szakaszban egyeztetjük a kezelőorvossal, és szakmai támogatást nyújtunk az adott klinikai helyzethez megfelelő konstrukció kiválasztásához.",
        "Komplex Full-Arch esete van?",
        "Beszéljük át az esetet és a restaurációs lehetőségeket egy rövid szakmai egyeztetésen.",
        "Írjon nekünk, munkatársunk hamarosan felveszi Önnel a kapcsolatot.",
        "KÉREK EGY SZAKMAI EGYEZTETÉST",
    ],
    "all-on-x-rehabilitationen.html": [
        "FULL-ARCH / ALL-ON-X",
        "Zahntechnischer Rückhalt für komplexe implantologische Rehabilitationen.",
        "Von der Planung bis zur definitiven Restauration unterstützen wir implantatgetragene Full-Arch-Versorgungen mit einem abgestimmten digitalen Workflow und eigener Fertigung.",
        "Ein abgestimmter digitaler Workflow von der Planung bis zur definitiven Restauration",
        "Bei einer Full-Arch-Rehabilitation sind schon vor der Planung die richtigen Informationen entscheidend für ein präzises Ergebnis. Deshalb prüfen wir die eingehenden Daten und stimmen das Behandlungskonzept ab. Anschließend entstehen Planung, Prototyp und definitive Restauration in einem aufeinander aufbauenden digitalen Workflow.",
        "Offene digitale Zusammenarbeit",
        "Wir können Daten aus den unterschiedlichen digitalen Systemen der Praxen verarbeiten. Vor der Planung prüfen wir die eingehenden Informationen und stimmen offene Fragen bei Bedarf mit dem behandelnden Zahnarzt ab.",
        "Die erforderlichen Planungsinformationen",
        "Bei Full-Arch-Versorgungen müssen verschiedene klinische und digitale Informationen aufeinander abgestimmt werden. Wir bewerten die Scandaten gemeinsam mit Bissinformationen, Fotos, Videos sowie ästhetischen und funktionellen Parametern.",
        "Abgestimmt auf die klinische Situation und das gewählte Restaurationskonzept fertigen wir unterschiedliche Full-Arch-Lösungen:",
        "monolithische Vollzirkonoxidrestaurationen", "Restaurationen auf Titanbasen (Ti-Base)",
        "Zirkonoxidrestaurationen auf Titan-iBars", "Toronto-Bridge-Lösungen", "provisorische PMMA-Restaurationen",
        "Das passende Restaurationskonzept wählen wir in gemeinsamer Abstimmung mit dem behandelnden Zahnarzt aus.",
        "WARUM BRIDGE DENTAL?", "Komplexe Full-Arch-Versorgungen mit abgestimmter fachlicher Unterstützung.",
        "Bei implantatgetragenen Full-Arch-Rehabilitationen sind präzise Informationen, gemeinsame Planung und ein abgestimmter Fertigungsprozess besonders wichtig.",
        "01 – Gemeinsame Planung",
        "Bei komplexen Fällen prüfen wir vor der Fertigung die verfügbaren Informationen und stimmen uns bei Bedarf mit dem behandelnden Zahnarzt ab.",
        "02 – Eigene digitale Fertigung",
        "Planung und Fertigung der Restaurationen erfolgen in unserem eigenen digitalen System. So lassen sich die einzelnen Schritte des Workflows intern kontrollieren.",
        "03 – Funktion und Ästhetik im Einklang",
        "Bei der Gestaltung der Restauration berücksichtigen wir die biomechanischen Anforderungen, die verfügbaren Platzverhältnisse und die ästhetischen Gesichtspunkte gleichermaßen.",
        "04 – Planbare Zusammenarbeit",
        "Transparente Arbeitsabläufe, direkte fachliche Kommunikation und konsequente Qualitätskontrolle unterstützen die Umsetzung jedes Falls.",
        "Das passende Restaurationskonzept auswählen",
        "Nicht jede Full-Arch-Rehabilitation erfordert dieselbe restaurative Lösung.",
        "Bei der Auswahl der passenden Konstruktion berücksichtigen wir die Position der Implantate, den verfügbaren prothetischen Raum, die biomechanischen Anforderungen sowie funktionelle und ästhetische Gesichtspunkte.",
        "Mögliche Restaurationskonzepte stimmen wir bereits in der Planungsphase mit dem behandelnden Zahnarzt ab. Wir unterstützen ihn fachlich dabei, die für die jeweilige klinische Situation geeignete Konstruktion auszuwählen.",
        "Sie haben einen komplexen Full-Arch-Fall?",
        "Lassen Sie uns den Fall und die Restaurationsmöglichkeiten in einem kurzen Fachgespräch besprechen.",
        "Schreiben Sie uns. Ein Mitglied unseres Teams wird sich zeitnah bei Ihnen melden.",
        "FACHGESPRÄCH ANFRAGEN",
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

for name, cta in [
    ('hu/full-arch-implantatumos-rehabilitaciok.html', 'KÉREK EGY SZAKMAI EGYEZTETÉST'),
    ('all-on-x-rehabilitationen.html', 'FACHGESPRÄCH ANFRAGEN'),
]:
    html = source(name)
    check('pilot' not in html.lower(), f'{name}: pilot offer, option and obsolete styles removed')
    workflow = section(html, 'class="digital-workflow"')
    check(len(re.findall(r'<article\b[^>]*class="digital-workflow-detail(?:\s|\")', workflow)) == 2, f'{name}: two workflow detail cards')
    options = section(html, 'id="rehabilitacios-lehetosegek"')
    check(len(re.findall(r'<li\b', options)) == 5, f'{name}: exactly five restoration options')
    reasons = section(html, 'id="miert-valasztanak-partnereink"')
    check(re.findall(r'class="partner-reason-number">(.*?)</span>', reasons) == ['01 –', '02 –', '03 –', '04 –'], f'{name}: four reasons in requested order')
    expected_photos = ['partner-01-0994.webp', 'partner-02-0907.webp', 'partner-03-0517.webp', 'partner-04-1786.webp', 'partner-05-0008.webp', 'partner-06-1294.webp']
    check(re.findall(r'src="(?:\.\./)?assets/all-on-x/([^"]+)"', reasons) == expected_photos, f'{name}: all six original photographs, once each, in approved order')
    check('assets/all-on-x/partner-reasons.css?v=20261013' in html, f'{name}: shared approved layout stylesheet')
    check('aria-labelledby="partner-reasons-title"' in reasons and 'id="partner-reasons-title"' in reasons, f'{name}: named benefits section')
    check(reasons.index('class="partner-reasons-visual"') < reasons.index('class="partner-reasons-content"') < reasons.index('class="partner-collage-benefits"'), f'{name}: visual column, content column, then full-width proof strip')
    check(len(re.findall(r'class="partner-collage-benefit"', reasons)) == 4, f'{name}: four original proof labels')
    check(reasons.count('class="partner-collage-statement"') == 1 and '<figcaption' not in reasons, f'{name}: original statement moved below the pictures')
    concept = section(html, 'id="restauracios-koncepcio"')
    check(concept.count('class="restoration-concept-copy') == 3, f'{name}: three concept paragraphs')
    check(f'href="#kapcsolat">{cta}</a>' in concept, f'{name}: consultation CTA links to existing contact section')
    check(re.search(r'<button\b[^>]*class="btn-form-submit"[^>]*>(.*?)</button>', html).group(1) == cta, f'{name}: updated submit label')
    check(html.index('id="restauracios-koncepcio"') < html.index('id="kapcsolat"') < html.index('<footer'), f'{name}: consultation section at end')

for name in ["index.html", "hu/index.html"]:
    html = source(name)
    check('cinematic-shell home-hero' in html, f"{name}: hero scope")
    check('assets/home/hero-layout.css?v=20261006' in html, f"{name}: shared hero layout")
    check('hero-ska-4081.webp' in html, f"{name}: hero photograph")
    check('service-metal-free-ceramics-0014.webp' in html, f"{name}: ceramics photograph")
    check(html.index('id="miert"') < html.index('id="velemenyek"') < html.index('id="technologia"'), f"{name}: reviews directly after partner benefits")
    cta = section(html, 'class="partner-cta"')
    check(html.index('id="munkaink"') < html.index(cta) < html.index('<footer'), f"{name}: final CTA placement")
    check('<section' not in html[html.index(cta) + len(cta):html.index('<footer')], f"{name}: no section below the final CTA")
    check(len(re.findall(r'class="service-kicker"', html)) == 6, f"{name}: six specialty subtitles")

check('id="innovacio"' not in about and 'MILESTONES' not in about, "About: removed innovation timeline")
development = section(about, 'id="fejlodes"')
check(re.findall(r'<h3>(.*?)</h3>', development) == ['Interne fachliche Weiterbildung', 'ICDE-Partnerlabor', 'Internationale fachliche Präsenz'], "About: ICDE centered in German")
development_hu = section(source('hu/ismerje-meg-a-bridge-dentalt.html'), 'id="fejlodes"')
check(re.findall(r'<h3>(.*?)</h3>', development_hu) == ['Belső szakmai képzés', 'ICDE partner labor', 'Nemzetközi szakmai jelenlét'], "About: ICDE centered in Hungarian")
check('<a ' not in section(about, 'id="nemzetkozi-tapasztalat"'), "About: old international CTA")
check(about.index('id="kulisszak-mogott"') < about.index('class="section about-contact"') < about.index('<footer'), "About: final CTA placement")
check('object-fit: contain;' in about[about.index('.hitvallas-photo-filled img'):about.index('.story-placeholder-ring')], "About: founder image fit")
check(len(re.findall(r'class="offer-item"', section(about, 'id="mashogy"'))) == 3, "About: three material claims")
main = re.search(r'<main>(.*?)</main>', contact, re.S).group(1)
check(main.count('href="tel:+36703966653"') == 1, "Contact: no duplicate Attila phone")
form = re.search(r'<form>(.*?)</form>', contact, re.S).group(1)
check(re.findall(r'<(?:input|select|textarea)\b[^>]*\bid="([^"]+)"', form) == ['nev','rendelo','email','telefon','targy','uzenet'], "Contact: six fields")
check('B2B-Laborpartner' not in main, "Contact: old badge removed")

class FooterLogoParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_footer = False
        self.anchor = None
        self.logos = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'footer':
            self.in_footer = True
        if tag == 'a':
            self.anchor = attrs
        if tag == 'img' and self.in_footer and 'logo' in attrs.get('src', ''):
            self.logos.append(self.anchor)

    def handle_endtag(self, tag):
        if tag == 'footer':
            self.in_footer = False
        if tag == 'a':
            self.anchor = None

for de, hu in PAIRS.items():
    for name, home_path in [(de, 'index.html'), (hu, 'hu/index.html')]:
        html = source(name)
        parser = FooterLogoParser()
        parser.feed(html)
        check(len(parser.logos) == 1 and parser.logos[0] is not None, f'{name}: footer logo is a link')
        check(local_target(name, parser.logos[0]['href']) == ROOT / home_path, f'{name}: footer logo goes to localized home')
        check('assets/funding.css?v=20261008' in html, f'{name}: updated footer stylesheet')
        check(not re.search(r'href="[^"]*galer(?:ie|ia)\.html', html), f'{name}: no removed gallery links')
    de_html = source(de)
    for obsolete in ['Bisheriger Vorteil', 'Seiten mit einem Karussell', '${p + 1}. oldal', 'dr.kovacs@fogaszat.hu', '>Furniere<', 'Prothesenvorbereitung', 'Pilotenberatungsformular', 'Az űrlap jelenleg prototípus']:
        check(obsolete not in de_html, f'{de}: untranslated or incorrect German: {obsolete}')
check('body { padding-bottom: 0; }' in source('assets/funding.css'), 'No padding outside the footer')
print(f"Validated {checks} October content, structure and JavaScript checks.")
