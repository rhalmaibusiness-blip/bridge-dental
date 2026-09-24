"""Change only the printed phone text, keeping the existing AcroForm intact."""

import io
import re
import subprocess
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ByteStringObject, TextStringObject


ROOT = Path(__file__).resolve().parents[1]
GERMAN_PHONE = "(+36) 70 396-66-53"
HUNGARIAN_PHONE = "(+36) 70 396-66-56"


def set_german_phone(page):
    fonts = page["/Resources"]["/Font"]
    maps = {}
    for name, reference in fonts.items():
        font = reference.get_object()
        if "PTSans-Regular" in str(font.get("/BaseFont")):
            pairs = re.findall(rb"<([0-9A-Fa-f]{4})>\s*<([0-9A-Fa-f]{4})>", font["/ToUnicode"].get_data())
            maps[name] = {bytes.fromhex(a.decode()): chr(int(b, 16)) for a, b in pairs}
    content = page.get_contents()
    font_name = None
    found = 0
    for operands, operator in content.operations:
        if operator == b"Tf":
            font_name = operands[0]
        if operator != b"TJ" or font_name not in maps:
            continue
        mapping = maps[font_name]
        runs = operands[0]
        text_indices = [i for i, item in enumerate(runs) if isinstance(item, (TextStringObject, ByteStringObject))]
        decoded = "".join(mapping.get(bytes(runs[i].original_bytes), "") for i in text_indices)
        if decoded not in {"(+36)70396-66-56", "(+36)70396-66-53"}:
            continue
        # Only the final glyph changes; all original spacing and drawing operators remain.
        three = next(code for code, character in mapping.items() if character == "3")
        runs[text_indices[-1]] = ByteStringObject(three)
        found += 1
    if found != 1:
        raise ValueError(f"Expected one printed German phone number, found {found}")
    page.replace_contents(content)
    page.compress_content_streams()


def set_hungarian_phone(page):
    content = page.get_contents()
    found = 0
    for operands, operator in content.operations:
        if operator == b"Tj" and str(operands[0]) in {"+36 70 396 6653", HUNGARIAN_PHONE}:
            operands[0] = TextStringObject(HUNGARIAN_PHONE)
            found += 1
    if found != 1:
        raise ValueError(f"Expected one printed Hungarian phone number, found {found}")
    page.replace_contents(content)
    page.compress_content_streams()


def update_published_copies():
    """Use the committed baseline, never silently import an unrelated local PDF edit."""
    for language, filename, change in [
        ("de", "bridge-dental-munkalap-kitoltheto.pdf", set_german_phone),
        ("hu", "bridge-dental-munkalap-kitoltheto-hu.pdf", set_hungarian_phone),
    ]:
        relative = f"output/pdf/{filename}"
        baseline = subprocess.check_output(["git", "show", f"HEAD:{relative}"], cwd=ROOT)
        reader = PdfReader(io.BytesIO(baseline))
        writer = PdfWriter()
        writer.clone_document_from_reader(reader)
        change(writer.pages[0])
        with (ROOT / relative).open("wb") as stream:
            writer.write(stream)
        reopened = PdfReader(ROOT / relative)
        if len(reopened.get_fields() or {}) != 56:
            raise ValueError(f"{language}: form field count changed")
        print(f"{language}: printed phone updated; 56 form fields preserved")


if __name__ == "__main__":
    update_published_copies()
