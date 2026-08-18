#!/usr/bin/env python3
"""Validate both Bridge Dental AcroForm work orders and create temporary fill tests."""

from pathlib import Path
import re
import textwrap

from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject,
    DecodedStreamObject,
    DictionaryObject,
    FloatObject,
    NameObject,
    TextStringObject,
)


ROOT = Path(__file__).resolve().parents[1]
PDF_DIR = ROOT / "output" / "pdf"
GERMAN_PDF = PDF_DIR / "bridge-dental-munkalap-kitoltheto.pdf"
HUNGARIAN_PDF = PDF_DIR / "bridge-dental-munkalap-kitoltheto-hu.pdf"
GERMAN_SAMPLE = Path("/private/tmp/bridge-dental-munkalap-de-filled-test.pdf")
HUNGARIAN_SAMPLE = Path("/private/tmp/bridge-dental-munkalap-hu-filled-test.pdf")

# ReportLab's embedded Arial Narrow subset maps the Hungarian accented glyphs
# to these single-byte codes. ASCII characters keep their regular codepoints.
HUNGARIAN_FORM_FONT_CODES = {
    "Á": 0x01, "É": 0x02, "Í": 0x03, "Ó": 0x04, "Ö": 0x05, "Ő": 0x06,
    "Ú": 0x07, "Ü": 0x08, "Ű": 0x09, "á": 0x0A, "é": 0x0B, "í": 0x0C,
    "ó": 0x0D, "ö": 0x0E, "ő": 0x0F, "ú": 0x10, "ü": 0x11, "ű": 0x12,
}


def encode_hungarian_form_text(value: str) -> bytes:
    encoded = bytearray()
    for character in value:
        if character in HUNGARIAN_FORM_FONT_CODES:
            encoded.append(HUNGARIAN_FORM_FONT_CODES[character])
        elif ord(character) <= 0x7F:
            encoded.append(ord(character))
        else:
            raise ValueError(f"A mezőbetűkészlet nem támogatja ezt a karaktert: {character}")
    return bytes(encoded)


def field_widgets(reader: PdfReader):
    widgets = []
    for annotation_ref in reader.pages[0].get("/Annots") or []:
        widget = annotation_ref.get_object()
        if widget.get("/Subtype") == "/Widget":
            widgets.append(widget)
    return widgets


def widget_value(reader: PdfReader, field_name: str):
    for widget in field_widgets(reader):
        if str(widget.get("/T", "")) == field_name:
            return widget.get("/V")
    raise KeyError(field_name)


def validate_structure(path: Path) -> None:
    reader = PdfReader(str(path))
    fields = reader.get_fields() or {}
    widgets = field_widgets(reader)
    if len(reader.pages) != 1:
        raise ValueError(f"{path.name}: expected 1 page, found {len(reader.pages)}")
    width = float(reader.pages[0].mediabox.width)
    height = float(reader.pages[0].mediabox.height)
    if abs(width - 595.5) > 1 or abs(height - 842.25) > 1:
        raise ValueError(f"{path.name}: expected A4, found {width} x {height} pt")
    if len(fields) != 56 or len(widgets) != 56:
        raise ValueError(f"{path.name}: expected 56 fields/widgets, found {len(fields)}/{len(widgets)}")
    if any(not widget.get("/AP") or not widget["/AP"].get("/N") for widget in widgets):
        raise ValueError(f"{path.name}: at least one widget lacks a normal appearance")
    if path == HUNGARIAN_PDF:
        acro_form = reader.trailer["/Root"]["/AcroForm"].get_object()
        field_ids = [reference.idnum for reference in acro_form["/Fields"]]
        widget_ids = [reference.idnum for reference in reader.pages[0]["/Annots"]]
        if field_ids != widget_ids or len(set(field_ids)) != 56:
            raise ValueError(f"{path.name}: field tree and page widgets are not the same 56 unique objects")
    print(f"{path.name}: 1 A4 page, 56 fields, 56 widgets, all appearances present")


def fill_german_sample() -> None:
    reader = PdfReader(str(GERMAN_PDF))
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    values = {
        "praxis_name": "Musterpraxis GmbH",
        "zahnarzt": "Dr. Max Mustermann",
        "datum_abdruck": "18.08.2026",
        "zahnfarbe": "A2",
        "menge_praezisionsabdruck": "2",
        "tooth_11": "/Yes",
        "arbeitsbeschreibung": "Digitale Planung und Funktionskontrolle vor der finalen Fertigstellung.",
    }
    writer.update_page_form_field_values(writer.pages[0], values, auto_regenerate=False)
    with GERMAN_SAMPLE.open("wb") as stream:
        writer.write(stream)
    reopened = PdfReader(str(GERMAN_SAMPLE))
    if widget_value(reopened, "praxis_name") != values["praxis_name"]:
        raise ValueError("German sample value was not preserved after reopening")
    print(f"German filled sample saved and reopened: {GERMAN_SAMPLE}")


def unicode_appearance(writer: PdfWriter, widget, font_ref, value: str) -> None:
    rect = widget["/Rect"]
    width = float(rect[2]) - float(rect[0])
    height = float(rect[3]) - float(rect[1])
    da = str(widget.get("/DA", "/ArialNarrowHU 9 Tf 0 g"))
    size_match = re.search(r"\s([0-9.]+)\s+Tf", da)
    font_size = float(size_match.group(1)) if size_match else 9.0
    is_multiline = bool(int(widget.get("/Ff", 0)) & (1 << 12))
    if is_multiline:
        lines = textwrap.wrap(value, width=96) or [""]
    else:
        lines = [value]

    commands = [
        "q",
        "/Tx BMC",
        "q",
        f"2 1 {max(1, width - 4):.3f} {max(1, height - 2):.3f} re W n",
        "BT",
        f"/ArialNarrowHU {font_size:.1f} Tf 0 g",
        f"2 {max(font_size + 1, height - font_size - 2):.3f} Td",
    ]
    for index, line in enumerate(lines):
        if index:
            commands.append(f"0 {-font_size * 1.25:.3f} Td")
        commands.append(f"<{encode_hungarian_form_text(line).hex().upper()}> Tj")
    commands.extend(["ET", "Q", "EMC", "Q"])

    appearance = DecodedStreamObject()
    appearance.set_data(("\n".join(commands) + "\n").encode("ascii"))
    appearance[NameObject("/Type")] = NameObject("/XObject")
    appearance[NameObject("/Subtype")] = NameObject("/Form")
    appearance[NameObject("/FormType")] = FloatObject(1)
    appearance[NameObject("/BBox")] = ArrayObject(
        [FloatObject(0), FloatObject(0), FloatObject(width), FloatObject(height)]
    )
    appearance[NameObject("/Resources")] = DictionaryObject(
        {
            NameObject("/Font"): DictionaryObject(
                {NameObject("/ArialNarrowHU"): font_ref}
            )
        }
    )
    widget[NameObject("/V")] = TextStringObject(value)
    widget[NameObject("/AP")][NameObject("/N")] = writer._add_object(appearance)


def fill_hungarian_sample() -> None:
    reader = PdfReader(str(HUNGARIAN_PDF))
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)
    acro_form = writer.root_object["/AcroForm"].get_object()
    font_ref = acro_form["/DR"].get_object()["/Font"].get_object()["/ArialNarrowHU"]
    values = {
        "praxis_name": "Őrmező Fogászat",
        "zahnarzt": "Dr. Müller Ágnes",
        "praxisadresse": "1011 Budapest, Minta utca 1.",
        "patient_name": "Teszt Páciens",
        "patient_alter": "42",
        "datum_abdruck": "2026.08.18.",
        "zahnfarbe": "A2",
        "zahnersatz_material": "Zirkonoxid",
        "termin_fertigstellung": "2026.09.02.",
        "menge_praezisionsabdruck": "2",
        "arbeitsbeschreibung": (
            "Teljes íves implantátumos restauráció. Kérjük a digitális terv, a funkció, "
            "az okklúzió és az esztétikai megjelenés ellenőrzését a végleges készrevitel előtt."
        ),
    }
    for annotation_ref in writer.pages[0]["/Annots"]:
        widget = annotation_ref.get_object()
        name = str(widget.get("/T", ""))
        if name in values:
            unicode_appearance(writer, widget, font_ref, values[name])
        elif name in {"metallrand", "tooth_11", "tooth_21"}:
            widget[NameObject("/V")] = NameObject("/Yes")
            widget[NameObject("/AS")] = NameObject("/Yes")

    with HUNGARIAN_SAMPLE.open("wb") as stream:
        writer.write(stream)
    reopened = PdfReader(str(HUNGARIAN_SAMPLE))
    if widget_value(reopened, "arbeitsbeschreibung") != values["arbeitsbeschreibung"]:
        raise ValueError("Hungarian multiline value was not preserved after reopening")
    if widget_value(reopened, "praxis_name") != values["praxis_name"]:
        raise ValueError("Hungarian accented value was not preserved after reopening")
    print(f"Hungarian filled sample saved and reopened: {HUNGARIAN_SAMPLE}")


def main() -> None:
    validate_structure(GERMAN_PDF)
    validate_structure(HUNGARIAN_PDF)
    fill_german_sample()
    fill_hungarian_sample()


if __name__ == "__main__":
    main()
