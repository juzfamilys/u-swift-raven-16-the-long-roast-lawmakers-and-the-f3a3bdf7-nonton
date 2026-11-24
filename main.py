"""The Long Roast: Lawmakers and the File They Cannot Convert.

Writes exactly one paragraph to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output). Pure Python stdlib, no network, deterministic.
"""

import os

PARAGRAPH = (
    "Dear lawmakers, you spent a decade debating the file format and still "
    "cannot convert it, which is almost impressive: most people fail faster "
    "and cheaper, but you turned a two-minute export into a ten-year public "
    "works project with hearings, a committee, and a PDF explaining why the "
    "PDF cannot be opened."
)


def validate(text: str) -> None:
    """Guard the paragraph before and after writing it to disk."""
    if not text:
        raise ValueError("paragraph must not be empty")
    if text != text.strip():
        raise ValueError("paragraph must not have leading/trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("paragraph must be a single line (no newline chars)")
    if "  " in text:
        raise ValueError("paragraph must not contain a double space")
    if not text.endswith("."):
        raise ValueError("paragraph must end with a full stop")
    if len(text) > 2000:
        raise ValueError("paragraph must be at most 2000 characters")


def main() -> None:
    validate(PARAGRAPH)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Exact UTF-8 bytes, no trailing newline.
    with open(path, "wb") as fh:
        fh.write(PARAGRAPH.encode("utf-8"))
    # Read the file back and re-validate the exact bytes on disk.
    with open(path, "rb") as fh:
        on_disk = fh.read()
    if on_disk != PARAGRAPH.encode("utf-8"):
        raise ValueError("bytes on disk do not match the paragraph")
    validate(on_disk.decode("utf-8"))


if __name__ == "__main__":
    main()
