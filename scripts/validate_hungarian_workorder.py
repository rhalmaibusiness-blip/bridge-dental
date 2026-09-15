#!/usr/bin/env python3
"""Exercise the Hungarian AcroForm using PDFium's actual form editing engine.

Run with the PDF runtime's pypdf, pypdfium2, pdfplumber and Pillow packages.
Only temporary QA files are written; the published blank PDF is never filled.
"""

import argparse
import ctypes
from pathlib import Path

import pdfplumber
import pypdfium2 as pdfium
from pypdfium2 import raw
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF = ROOT / "output/pdf/bridge-dental-munkalap-kitoltheto-hu.pdf"
QUANTITIES = (
    "menge_praezisionsabdruck", "menge_gegenbiss", "menge_biss",
    "menge_implantat_abutment", "menge_abdruckpfosten", "menge_modellanalog",
)


def validate_saved(path, expected):
    reader = PdfReader(path)
    fields = reader.get_fields() or {}
    assert len(reader.pages) == 1 and set(fields) == set(expected)
    page = reader.pages[0]
    assert abs(float(page.mediabox.width) - 595.5) < 0.01
    assert abs(float(page.mediabox.height) - 842.25) < 0.01
    widgets = [ref for ref in page["/Annots"] if ref.get_object().get("/Subtype") == "/Widget"]
    canonical = reader.trailer["/Root"]["/AcroForm"]["/Fields"]
    assert len(widgets) == len(canonical) == 56
    assert {(ref.idnum, ref.generation) for ref in canonical} == {
        (ref.idnum, ref.generation) for ref in widgets
    }, "Canonical fields and page widgets differ"
    assert sum(f["/FT"] == "/Tx" for f in fields.values()) == 22
    assert sum(f["/FT"] == "/Btn" for f in fields.values()) == 34
    for ref in widgets:
        widget = ref.get_object()
        name = widget["/T"]
        assert widget.get("/V", "") == fields[name].get("/V", "") == expected[name], name
        assert not (int(widget.get("/Ff", 0)) & 1), f"Read-only field: {name}"
        normal = widget["/AP"]["/N"].get_object()
        if widget["/FT"] == "/Btn":
            assert widget["/AS"] == expected[name], name
            normal = normal[widget["/AS"]].get_object()
        assert normal.get_data().strip(), f"Missing appearance: {name}"
        if name in QUANTITIES:
            assert widget["/Q"] == 1 and widget["/MaxLen"] == 3, name
    return reader


def render(path, output):
    with pdfium.PdfDocument(path) as document:
        document.init_forms()
        page = document[0]
        bitmap = page.render(scale=2.5)
        bitmap.to_pil().save(output)
        bitmap.close()
        page.close()


def edit_and_save(source, destination, values):
    reader = PdfReader(source)
    with pdfium.PdfDocument(source) as document:
        document.init_forms()
        page = document[0]
        for index, ref in enumerate(reader.pages[0]["/Annots"]):
            widget = ref.get_object()
            if widget.get("/Subtype") != "/Widget":
                continue
            name = widget["/T"]
            value = values[name]
            if widget["/FT"] == "/Btn":
                if widget.get("/V", "/Off") != value:
                    annotation = raw.FPDFPage_GetAnnot(page, index)
                    try:
                        assert raw.FORM_SetFocusedAnnot(document.formenv, annotation), name
                        assert raw.FORM_OnChar(document.formenv, page, 32, 0), name
                        raw.FORM_ForceToKillFocus(document.formenv)
                    finally:
                        raw.FPDFPage_CloseAnnot(annotation)
            else:
                annotation = raw.FPDFPage_GetAnnot(page, index)
                try:
                    assert raw.FORM_SetFocusedAnnot(document.formenv, annotation), name
                    assert raw.FORM_SelectAllText(document.formenv, page), name
                    encoded = ctypes.create_string_buffer((value + "\0").encode("utf-16-le"))
                    raw.FORM_ReplaceSelection(
                        document.formenv, page,
                        ctypes.cast(encoded, ctypes.POINTER(ctypes.c_ushort)),
                    )
                    raw.FORM_ForceToKillFocus(document.formenv)
                finally:
                    raw.FPDFPage_CloseAnnot(annotation)
        document.save(destination)
        page.close()


def validate_printed_geometry(path):
    # Check actual drawing commands and font metrics in the generated PDF.
    with pdfplumber.open(path) as pdf:
        page = pdf.pages[0]
        for x, top, width in [(464, 149, 82)] + [
            (x, top, 40) for x in (341, 506) for top in (289, 314, 339)
        ]:
            matches = [r for r in page.rects if all(abs(a - b) < 0.05 for a, b in zip(
                (r["x0"], r["top"], r["x1"], r["bottom"]), (x, top, x + width, top + 20)
            ))]
            assert matches and matches[-1]["stroke"], (x, top, "missing outline")
        for left, box_x in [(243, 341), (406, 506)]:
            for top in (289, 314, 339):
                chars = [c for c in page.chars if "ArialNarrow-Bold" in c["fontname"]
                         and left - 1 <= c["x0"] < box_x and top < c["top"] < top + 20]
                assert chars, (left, top, "missing label")
                assert abs(min(c["x0"] for c in chars) - left) < 0.05
                assert max(c["x1"] for c in chars) <= box_x - 6
                assert all(abs(c["size"] - 9.4) < 0.05 for c in chars)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "tmp/pdfs/hu-workorder-qa")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    fields = PdfReader(args.pdf).get_fields()
    empty_values = {name: "/Off" if field["/FT"] == "/Btn" else "" for name, field in fields.items()}
    validate_saved(args.pdf, empty_values)
    validate_printed_geometry(args.pdf)
    render(args.pdf, args.output_dir / "empty.png")

    values = {
        "praxis_name": "Őrmező Fogászat - teszt", "zahnarzt": "Dr. Teszt Ágnes",
        "praxisadresse": "Tesztcím: 1111 Budapest, Minta utca 1.",
        "patient_name": "Teszt Páciens", "patient_alter": "42",
        "zahnfarbe": "A2", "zahnersatz_material": "Cirkónium",
        "arbeitsbeschreibung": "ÁÉÍÓÖŐÚÜŰ áéíóöőúüű\r\nKitöltési próba: a dátum és a darabszámok ellenőrzése.",
    }
    source = args.pdf
    for index, (quantity, date) in enumerate([
        ("1", "2026.09.15."), ("12", "2026. 09. 15."), ("123", "2026.09.15."),
    ]):
        expected = dict(values)
        expected["datum_abdruck"] = date
        for name, field in fields.items():
            if name in QUANTITIES:
                expected[name] = quantity
            elif name.startswith("termin_"):
                expected[name] = "2026.09.30."
            elif field["/FT"] == "/Btn":
                expected[name] = "/Yes" if index != 1 else "/Off"
        assert set(expected) == set(fields), "Test must exercise every field"
        destination = args.output_dir / f"filled-{quantity}.pdf"
        edit_and_save(source, destination, expected)
        validate_saved(destination, expected)
        render(destination, destination.with_suffix(".png"))
        print(f"PASS: all 56 fields saved/reopened; six quantities={quantity}; date={date}; accents and checkboxes")
        source = destination
    print(f"PASS: full date/quantity borders and label clearance. Visual QA files: {args.output_dir}")


if __name__ == "__main__":
    main()
