#!/usr/bin/env python3
"""Build the Hungarian interactive Bridge Dental laboratory work order PDF."""

from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import (
    ArrayObject,
    BooleanObject,
    DecodedStreamObject,
    DictionaryObject,
    FloatObject,
    NameObject,
    NumberObject,
    TextStringObject,
)
from reportlab.lib.colors import black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PDF = ROOT / "assets" / "bridge-dental-munkalap.pdf"
TEMP_DIR = ROOT / "tmp" / "pdfs"
OVERLAY_PDF = TEMP_DIR / "bridge-dental-munkalap-hu-overlay.pdf"
OUTPUT_PDF = ROOT / "output" / "pdf" / "bridge-dental-munkalap-kitoltheto-hu.pdf"

PAGE_WIDTH = 595.5
PAGE_HEIGHT = 842.25
TEXT_FIELD_FLAGS = 0
MULTILINE_FIELD_FLAGS = 1 << 12
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial Narrow.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf"


def pdf_box(x0: float, top: float, x1: float, bottom: float, inset: float = 1.5):
    return (
        x0 + inset,
        PAGE_HEIGHT - bottom + inset,
        (x1 - x0) - (2 * inset),
        (bottom - top) - (2 * inset),
    )


def build_overlay() -> list[str]:
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    pdfmetrics.registerFont(TTFont("ArialNarrow", FONT_REGULAR))
    pdfmetrics.registerFont(TTFont("ArialNarrowBold", FONT_BOLD))

    pdf = canvas.Canvas(str(OVERLAY_PDF), pagesize=(PAGE_WIDTH, PAGE_HEIGHT))
    pdf.setTitle("Bridge Dental - kitölthető magyar munkalap")
    pdf.setAuthor("Bridge Dental Kft.")

    # Keep the complete Hungarian alphabet in the embedded form font so values
    # entered later can contain every Hungarian accented character.
    pdf.setFillAlpha(0)
    pdf.setFont("ArialNarrow", 1)
    pdf.drawString(0, 0, "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzÁÉÍÓÖŐÚÜŰáéíóöőúüű")
    pdf.setFillAlpha(1)

    def erase(x0: float, top: float, x1: float, bottom: float) -> None:
        pdf.setFillColor(white)
        pdf.setStrokeColor(white)
        pdf.rect(x0, PAGE_HEIGHT - bottom, x1 - x0, bottom - top, fill=1, stroke=0)

    def label(
        text: str,
        x: float,
        top: float,
        *,
        size: float = 9.4,
        bold: bool = True,
    ) -> None:
        pdf.setFillColor(black)
        pdf.setFont("ArialNarrowBold" if bold else "ArialNarrow", size)
        pdf.drawString(x, PAGE_HEIGHT - top - size, text)

    def two_line(text1: str, text2: str, x: float, top: float, *, size: float = 9.4) -> None:
        label(text1, x, top, size=size)
        label(text2, x, top + size + 1.5, size=size)

    # Replace only printed German labels. The original lines, logo, tooth grid and
    # restoration drawing remain untouched below this white-and-text overlay.
    translated_labels = [
        ((454, 31, 547, 48), "+36 70 396 6653", 458, 34, 9.0, False),
        ((49, 89, 139, 110), "Rendelő neve", 50, 91, 9.6, True),
        ((302, 89, 350, 110), "Fogorvos", 303, 91, 9.6, True),
        ((49, 119, 139, 140), "Rendelő címe", 50, 121, 9.6, True),
        ((49, 149, 139, 170), "Páciens neve, életkora", 50, 151, 9.2, True),
        ((368, 149, 464, 170), "Lenyomat dátuma", 369, 151, 9.2, True),
        ((74, 180, 139, 201), "Fémszegély", 75, 182, 9.6, True),
        ((74, 226, 139, 254), "Kerámiaváll", 75, 230, 9.6, True),
        ((177, 259, 227, 280), "Fogszín", 178, 261, 9.6, True),
        ((351, 259, 444, 280), "Fogpótlás anyaga", 352, 261, 9.3, True),
        ((49, 277, 139, 291), "IDŐPONTOK:", 50, 278, 9.6, True),
        ((49, 289, 139, 310), "Egyéni kanál", 50, 291, 9.4, True),
        ((49, 314, 139, 335), "Harapásvétel", 50, 316, 9.4, True),
        ((49, 339, 139, 360), "Vázpróba", 50, 341, 9.4, True),
        ((49, 364, 139, 385), "Nyerspróba", 50, 366, 9.4, True),
        ((49, 389, 139, 410), "Modellöntés", 50, 391, 9.4, True),
        ((49, 414, 139, 435), "Felállítási próba", 50, 416, 9.4, True),
        ((254, 289, 340, 310), "Precíziós lenyomat", 255, 291, 8.6, True),
        ((242, 314, 340, 335), "Antagonista lenyomat", 243, 316, 8.4, True),
        ((314, 339, 340, 360), "Harapás", 315, 341, 9.0, True),
        ((405, 289, 506, 310), "Implantátum-felépítmény", 406, 291, 8.0, True),
        ((428, 314, 506, 335), "Lenyomati fej", 429, 316, 9.0, True),
        ((436, 339, 506, 360), "Modellanalóg", 437, 341, 9.0, True),
        ((49, 487, 222, 516), "MUNKALEÍRÁS:", 50, 491, 9.8, True),
    ]
    for rect, text, x, top, size, bold in translated_labels:
        erase(*rect)
        label(text, x, top, size=size, bold=bold)

    erase(49, 437, 139, 466)
    two_line("Készrevitel", "Átadás", 50, 439, size=9.0)

    # The source sheet has a single, slim quantity box whose right-hand side
    # contains the German unit label ("Stk").  Only mask the letters: masking
    # the whole right side would also cut the original box border in PDF viewers.
    for x0, x1, top in [
        (364, 388, 289), (364, 388, 314), (364, 388, 339),
        (529, 548, 289), (529, 548, 314), (529, 548, 339),
    ]:
        erase(x0 + 2, top + 4, x1 - 2, top + 15)
        label("db", x0 + 3, top + 4, size=7.5, bold=False)

    form = pdf.acroForm
    field_names: list[str] = []

    def text_field(
        name: str,
        tooltip: str,
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
            tooltip=tooltip,
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
        tooltip: str,
        rect: tuple[float, float, float, float],
        *,
        size: float = 14,
    ) -> None:
        x0, top, x1, bottom = rect
        x = x0 + ((x1 - x0) - size) / 2
        y = PAGE_HEIGHT - bottom + ((bottom - top) - size) / 2
        form.checkbox(
            name=name,
            tooltip=tooltip,
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

    text_field("praxis_name", "Rendelő neve", (140.0, 89.0, 290.8, 109.0))
    text_field("zahnarzt", "Fogorvos", (351.6, 89.0, 546.0, 109.0))
    text_field("praxisadresse", "Rendelő címe", (140.0, 119.0, 546.0, 139.0))
    text_field("patient_name", "Páciens neve", (140.0, 149.0, 312.0, 169.0))
    text_field("patient_alter", "Páciens életkora", (322.0, 149.0, 342.0, 169.0), font_size=8, max_length=3)
    text_field("datum_abdruck", "Lenyomat dátuma", (464.0, 149.0, 546.0, 169.0), max_length=20)

    checkbox("metallrand", "Fémszegély", (50.0, 180.0, 70.0, 200.0), size=15)
    checkbox("keramikschulter", "Kerámiaváll", (50.0, 229.0, 70.0, 249.0), size=15)

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
            checkbox(f"tooth_{tooth}", f"{tooth}. fog", (cell_x0, top, cell_x0 + cell_width, bottom), size=12)

    text_field("zahnfarbe", "Fogszín", (228.2, 258.8, 331.4, 278.8))
    text_field("zahnersatz_material", "Fogpótlás anyaga", (444.9, 259.0, 546.0, 279.0), font_size=8)

    schedule_fields = [
        ("termin_individueller_loeffel", "Egyéni kanál időpontja", (140.0, 288.8, 228.2, 308.8)),
        ("termin_bissnahme", "Harapásvétel időpontja", (140.0, 313.8, 228.2, 333.8)),
        ("termin_geruestprobe", "Vázpróba időpontja", (140.0, 338.8, 228.2, 358.8)),
        ("termin_rohbrand", "Nyerspróba időpontja", (140.0, 363.8, 228.2, 383.8)),
        ("termin_modellguss", "Modellöntés időpontja", (140.0, 388.8, 228.2, 408.8)),
        ("termin_aufstellungsprobe", "Felállítási próba időpontja", (140.0, 413.8, 228.2, 433.8)),
        ("termin_fertigstellung", "Készrevitel / átadás időpontja", (140.0, 438.8, 228.2, 458.8)),
    ]
    for name, tooltip, rect in schedule_fields:
        text_field(name, tooltip, rect, font_size=8, max_length=24)

    quantity_fields = [
        ("menge_praezisionsabdruck", "Precíziós lenyomat darabszáma", (341.0, 289.0, 365.0, 309.0)),
        ("menge_gegenbiss", "Antagonista lenyomat darabszáma", (341.0, 314.0, 365.0, 334.0)),
        ("menge_biss", "Harapás darabszáma", (341.0, 339.0, 365.0, 359.0)),
        ("menge_implantat_abutment", "Implantátum-felépítmény darabszáma", (506.0, 289.0, 530.0, 309.0)),
        ("menge_abdruckpfosten", "Lenyomati fej darabszáma", (506.0, 314.0, 530.0, 334.0)),
        ("menge_modellanalog", "Modellanalóg darabszáma", (506.0, 339.0, 530.0, 359.0)),
    ]
    for name, tooltip, rect in quantity_fields:
        text_field(name, tooltip, rect, font_size=8, max_length=3, inset=1.0)

    text_field(
        "arbeitsbeschreibung",
        "Munkaleírás",
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
        raise ValueError("A Bridge Dental munkalapnak egyoldalasnak kell maradnia.")

    writer = PdfWriter()
    writer.clone_document_from_reader(overlay)
    # Draw the original page below the Hungarian labels and form widgets.
    writer.pages[0].merge_page(source.pages[0], over=False)
    writer.pages[0][NameObject("/Tabs")] = NameObject("/A")

    # ReportLab stores a second copy of each widget in the AcroForm field tree.
    # Point the field tree at the actual page widgets so edits made by browser
    # PDF viewers are persisted in the same objects that are rendered.
    acro_form = writer.root_object["/AcroForm"].get_object()
    page_widgets = ArrayObject(
        annotation_ref
        for annotation_ref in writer.pages[0].get("/Annots") or []
        if annotation_ref.get_object().get("/Subtype") == "/Widget"
    )
    acro_form[NameObject("/Fields")] = page_widgets

    def embed_unicode_form_font():
        """Embed a full Unicode Type0 font for values entered into text fields."""
        form_font = TTFont("ArialNarrowFormHU", FONT_REGULAR)
        face = form_font.face

        font_file = DecodedStreamObject()
        font_bytes = Path(FONT_REGULAR).read_bytes()
        font_file.set_data(font_bytes)
        font_file[NameObject("/Length1")] = NumberObject(len(font_bytes))
        font_file_ref = writer._add_object(font_file)

        descriptor = DictionaryObject(
            {
                NameObject("/Type"): NameObject("/FontDescriptor"),
                NameObject("/FontName"): NameObject("/ArialNarrowHU"),
                NameObject("/FontFamily"): TextStringObject("Arial Narrow"),
                NameObject("/Flags"): NumberObject(4),
                NameObject("/FontBBox"): ArrayObject(FloatObject(v) for v in face.bbox),
                NameObject("/ItalicAngle"): FloatObject(face.italicAngle),
                NameObject("/Ascent"): FloatObject(face.ascent),
                NameObject("/Descent"): FloatObject(face.descent),
                NameObject("/CapHeight"): FloatObject(face.capHeight),
                NameObject("/StemV"): FloatObject(face.stemV),
                NameObject("/MissingWidth"): FloatObject(face.defaultWidth),
                NameObject("/FontFile2"): font_file_ref,
            }
        )
        descriptor_ref = writer._add_object(descriptor)

        cid_to_gid = bytearray(65536 * 2)
        for codepoint, glyph_id in face.charToGlyph.items():
            if 0 <= codepoint <= 0xFFFF:
                cid_to_gid[codepoint * 2:codepoint * 2 + 2] = int(glyph_id).to_bytes(2, "big")
        cid_map_stream = DecodedStreamObject()
        cid_map_stream.set_data(bytes(cid_to_gid))
        cid_map_ref = writer._add_object(cid_map_stream)

        width_entries = ArrayObject()
        codepoints = sorted(cp for cp in face.charToGlyph if 0 <= cp <= 0xFFFF)
        run: list[int] = []
        run_start = 0

        def flush_run() -> None:
            if not run:
                return
            width_entries.append(NumberObject(run_start))
            width_entries.append(
                ArrayObject(FloatObject(face.charWidths.get(cp, face.defaultWidth)) for cp in run)
            )

        previous = None
        for codepoint in codepoints:
            if previous is None or codepoint != previous + 1:
                flush_run()
                run = []
                run_start = codepoint
            run.append(codepoint)
            previous = codepoint
        flush_run()

        cid_font = DictionaryObject(
            {
                NameObject("/Type"): NameObject("/Font"),
                NameObject("/Subtype"): NameObject("/CIDFontType2"),
                NameObject("/BaseFont"): NameObject("/ArialNarrowHU"),
                NameObject("/CIDSystemInfo"): DictionaryObject(
                    {
                        NameObject("/Registry"): TextStringObject("Adobe"),
                        NameObject("/Ordering"): TextStringObject("Identity"),
                        NameObject("/Supplement"): NumberObject(0),
                    }
                ),
                NameObject("/FontDescriptor"): descriptor_ref,
                NameObject("/CIDToGIDMap"): cid_map_ref,
                NameObject("/DW"): FloatObject(face.defaultWidth),
                NameObject("/W"): width_entries,
            }
        )
        cid_font_ref = writer._add_object(cid_font)

        to_unicode = DecodedStreamObject()
        to_unicode.set_data(
            b"/CIDInit /ProcSet findresource begin\n"
            b"12 dict begin\n"
            b"begincmap\n"
            b"/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def\n"
            b"/CMapName /Adobe-Identity-UCS def\n"
            b"/CMapType 2 def\n"
            b"1 begincodespacerange\n<0000> <FFFF>\nendcodespacerange\n"
            b"1 beginbfrange\n<0000> <FFFF> <0000>\nendbfrange\n"
            b"endcmap\n"
            b"CMapName currentdict /CMap defineresource pop\n"
            b"end\nend\n"
        )
        to_unicode_ref = writer._add_object(to_unicode)

        type0_font = DictionaryObject(
            {
                NameObject("/Type"): NameObject("/Font"),
                NameObject("/Subtype"): NameObject("/Type0"),
                NameObject("/BaseFont"): NameObject("/ArialNarrowHU"),
                NameObject("/Encoding"): NameObject("/Identity-H"),
                NameObject("/DescendantFonts"): ArrayObject([cid_font_ref]),
                NameObject("/ToUnicode"): to_unicode_ref,
            }
        )
        return writer._add_object(type0_font)

    # Reuse the already embedded Arial Narrow font from the Hungarian label
    # layer. Unlike a second, hand-built CID font this is stable in Chrome,
    # Preview and Acrobat form renderers.
    page_fonts = writer.pages[0]["/Resources"]["/Font"].get_object()
    hungarian_font_ref = next(
        (
            reference
            for reference in page_fonts.values()
            if "ArialNarrow" in str(reference.get_object().get("/BaseFont", ""))
            and "Bold" not in str(reference.get_object().get("/BaseFont", ""))
        ),
        None,
    )
    if hungarian_font_ref is None:
        raise ValueError("A magyar űrlap betűkészlete nem található.")

    def transparent_appearance(source_stream, content: bytes):
        source_object = source_stream.get_object()
        replacement = DecodedStreamObject()
        for key in ("/Type", "/Subtype", "/FormType", "/BBox", "/Matrix", "/Resources"):
            if key in source_object:
                replacement[NameObject(key)] = source_object[key]
        replacement.set_data(content)
        return writer._add_object(replacement)

    for annotation_ref in writer.pages[0].get("/Annots") or []:
        widget = annotation_ref.get_object()
        if widget.get("/Subtype") != "/Widget":
            continue
        if widget.get("/FT") == "/Tx":
            old_da = str(widget.get("/DA", "/Helv 9 Tf 0 g"))
            widget[NameObject("/DA")] = TextStringObject(old_da.replace("/Helv", "/ArialNarrowHU"))
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
                raise ValueError("A jelölőnégyzet megjelenése nem dolgozható fel.")
            states[NameObject("/Off")] = transparent_appearance(off_stream, b"q\nQ\n")
            states[NameObject("/Yes")] = transparent_appearance(yes_stream, yes_data[checkmark_start:])
            appearance.pop(NameObject("/D"), None)
        else:
            bbox = normal.get_object().get("/BBox")
            width = float(bbox[2]) if bbox else 1
            height = float(bbox[3]) if bbox else 1
            empty_text_appearance = f"/Tx BMC\nq\n0 0 {width:.3f} {height:.3f} re W n\nQ\nEMC\n".encode("ascii")
            appearance[NameObject("/N")] = transparent_appearance(normal, empty_text_appearance)

    acro_form[NameObject("/NeedAppearances")] = BooleanObject(False)
    fields = writer.get_fields() or {}

    acro_fonts = acro_form["/DR"].get_object()["/Font"].get_object()
    acro_fonts[NameObject("/ArialNarrowHU")] = hungarian_font_ref
    acro_form[NameObject("/DA")] = TextStringObject("/ArialNarrowHU 0 Tf 0 g")
    for name in field_names:
        if name.startswith("menge_"):
            fields[name][NameObject("/Q")] = NumberObject(1)

    writer.add_metadata(
        {
            "/Title": "Bridge Dental - kitölthető magyar munkalap",
            "/Author": "Bridge Dental Kft.",
            "/Subject": "Interaktív fogtechnikai munkalap",
            "/Lang": "hu-HU",
        }
    )
    with OUTPUT_PDF.open("wb") as output_stream:
        writer.write(output_stream)


def validate_output(expected_field_names: list[str]) -> None:
    reader = PdfReader(str(OUTPUT_PDF))
    fields = reader.get_fields() or {}
    if len(reader.pages) != 1:
        raise ValueError(f"Egy oldal helyett {len(reader.pages)} oldal készült.")
    if set(fields) != set(expected_field_names):
        raise ValueError("A mezőfa nem egyezik a várt 56 mezővel.")

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
            raise ValueError(f"A(z) {name} mezőnek nincs megjelenési rétege.")

    if len(widget_names) != len(expected_field_names) or set(widget_names) != set(expected_field_names):
        raise ValueError("Az oldal widgetjei nem egyeznek a mezőfával.")


def main() -> None:
    field_names = build_overlay()
    if len(field_names) != 56 or len(set(field_names)) != 56:
        raise ValueError(f"56 egyedi mező helyett {len(field_names)} készült.")
    merge_with_source(field_names)
    validate_output(field_names)
    OVERLAY_PDF.unlink(missing_ok=True)
    print(f"Created {OUTPUT_PDF} with {len(field_names)} interactive fields.")


if __name__ == "__main__":
    main()
