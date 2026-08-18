#!/usr/bin/env python3
"""Build the interactive Bridge Dental laboratory work order PDF."""

from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import BooleanObject, DecodedStreamObject, NameObject, NumberObject
from reportlab.lib.colors import black
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PDF = ROOT / "assets" / "bridge-dental-munkalap.pdf"
TEMP_DIR = ROOT / "tmp" / "pdfs"
OVERLAY_PDF = TEMP_DIR / "bridge-dental-munkalap-form-overlay.pdf"
OUTPUT_PDF = ROOT / "output" / "pdf" / "bridge-dental-munkalap-kitoltheto.pdf"

PAGE_WIDTH = 595.5
PAGE_HEIGHT = 842.25
TEXT_FIELD_FLAGS = 0
MULTILINE_FIELD_FLAGS = 1 << 12


def pdf_box(x0: float, top: float, x1: float, bottom: float, inset: float = 1.5):
    """Convert a top-origin source-PDF rectangle to ReportLab coordinates."""
    return (
        x0 + inset,
        PAGE_HEIGHT - bottom + inset,
        (x1 - x0) - (2 * inset),
        (bottom - top) - (2 * inset),
    )


def build_overlay() -> list[str]:
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)

    pdf = canvas.Canvas(str(OVERLAY_PDF), pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle("Bridge Dental - kitoltheto munkalap")
    pdf.setAuthor("Bridge Dental Kft.")
    form = pdf.acroForm
    field_names: list[str] = []

    def text_field(
        name: str,
        label: str,
        rect: tuple[float, float, float, float],
        *,
        font_size: float = 9,
        max_length: int = 120,
        flags: int = TEXT_FIELD_FLAGS,
        inset: float = 1.5,
    ) -> None:
        x, y, width, height = pdf_box(*rect, inset=inset)
        form.textfield(
            name=name,
            tooltip=label,
            value="",
            x=x,
            y=y,
            width=width,
            height=height,
            borderWidth=0,
            borderColor=None,
            fillColor=None,
            textColor=black,
            forceBorder=False,
            fontName="Helvetica",
            fontSize=font_size,
            fieldFlags=flags,
            maxlen=max_length,
        )
        field_names.append(name)

    def checkbox(
        name: str,
        label: str,
        rect: tuple[float, float, float, float],
        *,
        size: float = 14,
    ) -> None:
        x0, top, x1, bottom = rect
        x = x0 + ((x1 - x0) - size) / 2
        y = PAGE_HEIGHT - bottom + ((bottom - top) - size) / 2
        form.checkbox(
            name=name,
            tooltip=label,
            checked=False,
            x=x,
            y=y,
            size=size,
            buttonStyle="check",
            borderWidth=0,
            borderColor=None,
            fillColor=None,
            textColor=black,
            forceBorder=False,
        )
        field_names.append(name)

    # Practice and patient data, in the intended keyboard tab order.
    text_field("praxis_name", "Praxis - Name", (140.0, 89.0, 290.8, 109.0))
    text_field("zahnarzt", "Zahnarzt", (351.6, 89.0, 546.0, 109.0))
    text_field("praxisadresse", "Praxisadresse", (140.0, 119.0, 546.0, 139.0))
    text_field("patient_name", "Patient Name", (140.0, 149.0, 312.0, 169.0))
    text_field("patient_alter", "Patient Alter", (322.0, 149.0, 342.0, 169.0), font_size=8, max_length=3)
    text_field("datum_abdruck", "Datum des Abdrucks", (464.0, 149.0, 546.0, 169.0), max_length=20)

    checkbox("metallrand", "Metallrand", (50.0, 180.0, 70.0, 200.0), size=15)
    checkbox("keramikschulter", "Keramikschulter", (50.0, 229.0, 70.0, 249.0), size=15)

    # Tooth selection checkboxes occupy the blank cells beside the printed tooth numbers.
    tooth_rows = [
        ((18, 17, 16, 15, 14, 13, 12, 11), 140.0, 331.1, 179.0, 199.0),
        ((21, 22, 23, 24, 25, 26, 27, 28), 354.9, 546.0, 179.0, 199.0),
        ((48, 47, 46, 45, 44, 43, 42, 41), 140.0, 331.1, 229.0, 249.0),
        ((31, 32, 33, 34, 35, 36, 37, 38), 354.9, 546.0, 229.0, 249.0),
    ]
    for teeth, x0, x1, top, bottom in tooth_rows:
        cell_width = (x1 - x0) / len(teeth)
        for index, tooth in enumerate(teeth):
            cell_x0 = x0 + index * cell_width
            checkbox(
                f"tooth_{tooth}",
                f"Zahn {tooth}",
                (cell_x0, top, cell_x0 + cell_width, bottom),
                size=12,
            )

    text_field("zahnfarbe", "Zahnfarbe", (228.2, 258.8, 331.4, 278.8))
    text_field("zahnersatz_material", "Zahnersatz Material", (444.9, 259.0, 546.0, 279.0), font_size=8)

    # Appointment/date fields.
    schedule_fields = [
        ("termin_individueller_loeffel", "Termin Individueller Loffel", (140.0, 288.8, 228.2, 308.8)),
        ("termin_bissnahme", "Termin Bissnahme", (140.0, 313.8, 228.2, 333.8)),
        ("termin_geruestprobe", "Termin Gerustprobe", (140.0, 338.8, 228.2, 358.8)),
        ("termin_rohbrand", "Termin Rohbrand", (140.0, 363.8, 228.2, 383.8)),
        ("termin_modellguss", "Termin Modellguss", (140.0, 388.8, 228.2, 408.8)),
        ("termin_aufstellungsprobe", "Termin Aufstellungsprobe", (140.0, 413.8, 228.2, 433.8)),
        ("termin_fertigstellung", "Termin Fertigstellung / Liefertermin", (140.0, 438.8, 228.2, 458.8)),
    ]
    for name, label, rect in schedule_fields:
        text_field(name, label, rect, font_size=8, max_length=24)

    # Quantity fields use only the unlabelled left side of each existing Stk box.
    quantity_fields = [
        ("menge_praezisionsabdruck", "Menge Prazisionsabdruck", (341.0, 289.0, 365.0, 309.0)),
        ("menge_gegenbiss", "Menge Gegenbiss / Antagonis", (341.0, 314.0, 365.0, 334.0)),
        ("menge_biss", "Menge Biss", (341.0, 339.0, 365.0, 359.0)),
        ("menge_implantat_abutment", "Menge Implantat-Abutment", (506.0, 289.0, 530.0, 309.0)),
        ("menge_abdruckpfosten", "Menge Abdruckpfosten", (506.0, 314.0, 530.0, 334.0)),
        ("menge_modellanalog", "Menge Modellanalog", (506.0, 339.0, 530.0, 359.0)),
    ]
    for name, label, rect in quantity_fields:
        text_field(name, label, rect, font_size=8, max_length=3, inset=1.0)

    text_field(
        "arbeitsbeschreibung",
        "Arbeitsbeschreibung",
        (50.0, 505.0, 546.0, 790.0),
        font_size=9,
        max_length=3000,
        flags=MULTILINE_FIELD_FLAGS,
        inset=0,
    )

    pdf.showPage()
    pdf.save()
    return field_names


def merge_with_source(field_names: list[str]) -> None:
    source = PdfReader(str(SOURCE_PDF))
    overlay = PdfReader(str(OVERLAY_PDF))
    if len(source.pages) != 1 or len(overlay.pages) != 1:
        raise ValueError("The Bridge Dental work order must remain a single-page PDF.")

    writer = PdfWriter()
    writer.clone_document_from_reader(overlay)
    writer.pages[0].merge_page(source.pages[0])
    writer.pages[0][NameObject("/Tabs")] = NameObject("/A")

    def transparent_appearance(source_stream, content: bytes):
        source_object = source_stream.get_object()
        replacement = DecodedStreamObject()
        for key in ("/Type", "/Subtype", "/FormType", "/BBox", "/Matrix", "/Resources"):
            if key in source_object:
                replacement[NameObject(key)] = source_object[key]
        replacement.set_data(content)
        return writer._add_object(replacement)

    # ReportLab defaults empty fields to a blue background. Remove that paint
    # while keeping complete, valid appearance streams for every widget.
    for annotation_ref in writer.pages[0].get("/Annots") or []:
        widget = annotation_ref.get_object()
        if widget.get("/Subtype") != "/Widget":
            continue

        mk = widget.get("/MK")
        if mk:
            mk.pop(NameObject("/BG"), None)
            mk.pop(NameObject("/BC"), None)

        appearance = widget.get("/AP")
        normal = appearance.get("/N") if appearance else None
        if not normal:
            continue

        if widget.get("/FT") == "/Btn":
            states = normal.get_object()
            off_stream = states[NameObject("/Off")]
            yes_stream = states[NameObject("/Yes")]
            yes_data = yes_stream.get_object().get_data()
            checkmark_start = yes_data.find(b"q 0 0 0 rg")
            if checkmark_start < 0:
                raise ValueError("Could not isolate the checkbox checkmark appearance.")
            states[NameObject("/Off")] = transparent_appearance(off_stream, b"q\nQ\n")
            states[NameObject("/Yes")] = transparent_appearance(yes_stream, yes_data[checkmark_start:])
            appearance.pop(NameObject("/D"), None)
        else:
            bbox = normal.get_object().get("/BBox")
            width = float(bbox[2]) if bbox else 1
            height = float(bbox[3]) if bbox else 1
            empty_text_appearance = (
                f"/Tx BMC\nq\n0 0 {width:.3f} {height:.3f} re W n\nQ\nEMC\n".encode("ascii")
            )
            appearance[NameObject("/N")] = transparent_appearance(normal, empty_text_appearance)

    acro_form = writer.root_object["/AcroForm"].get_object()
    acro_form[NameObject("/NeedAppearances")] = BooleanObject(False)

    fields = writer.get_fields() or {}
    for name in field_names:
        if name.startswith("menge_"):
            fields[name][NameObject("/Q")] = NumberObject(1)

    writer.add_metadata(
        {
            "/Title": "Bridge Dental - kitoltheto munkalap",
            "/Author": "Bridge Dental Kft.",
            "/Subject": "Interaktiv fogtechnikai munkalap",
        }
    )
    with OUTPUT_PDF.open("wb") as output_stream:
        writer.write(output_stream)


def validate_output(expected_field_names: list[str]) -> None:
    reader = PdfReader(str(OUTPUT_PDF))
    fields = reader.get_fields() or {}
    if len(reader.pages) != 1:
        raise ValueError(f"Expected one output page, found {len(reader.pages)}.")
    if set(fields) != set(expected_field_names):
        missing = sorted(set(expected_field_names) - set(fields))
        unexpected = sorted(set(fields) - set(expected_field_names))
        raise ValueError(f"Form field mismatch. Missing: {missing}; unexpected: {unexpected}.")

    widget_names: list[str] = []
    for annotation_ref in reader.pages[0].get("/Annots") or []:
        widget = annotation_ref.get_object()
        if widget.get("/Subtype") != "/Widget":
            continue
        parent = widget.get("/Parent")
        name = widget.get("/T") or (parent.get_object().get("/T") if parent else None)
        widget_names.append(str(name))
        appearance = widget.get("/AP")
        if not appearance or not appearance.get("/N"):
            raise ValueError(f"Widget {name} has no normal appearance stream.")

    if len(widget_names) != len(expected_field_names) or set(widget_names) != set(expected_field_names):
        raise ValueError("The page widget annotations do not match the canonical field tree.")


def main() -> None:
    field_names = build_overlay()
    if len(field_names) != 56 or len(set(field_names)) != 56:
        raise ValueError(f"Expected 56 unique form fields, found {len(field_names)}.")
    merge_with_source(field_names)
    validate_output(field_names)
    OVERLAY_PDF.unlink(missing_ok=True)
    print(f"Created {OUTPUT_PDF} with {len(field_names)} interactive fields.")


if __name__ == "__main__":
    main()
