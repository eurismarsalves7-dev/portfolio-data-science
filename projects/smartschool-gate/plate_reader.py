"""OCR demonstrativo de placas; não é um detector de placas certificado."""
import re
from functools import lru_cache

import cv2
import easyocr
import numpy as np

# Brazilian plate patterns: old ABC1234 and Mercosul ABC1D23.
PLATE_PATTERNS = (
    re.compile(r"^[A-Z]{3}[0-9]{4}$"),
    re.compile(r"^[A-Z]{3}[0-9][A-Z][0-9]{2}$"),
)


def normalize_plate(value: str) -> str:
    return re.sub(r"[^A-Z0-9]", "", value.upper())


def looks_like_plate(value: str) -> bool:
    return any(pattern.fullmatch(value) for pattern in PLATE_PATTERNS)


@lru_cache(maxsize=1)
def get_reader():
    # EasyOCR may download model files on first use.
    return easyocr.Reader(["pt", "en"], gpu=False, verbose=False)


def extract_plate(image_bytes: bytes) -> tuple[str | None, str]:
    """Return (plate_candidate, OCR text). Image bytes are processed in memory."""
    encoded = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(encoded, cv2.IMREAD_COLOR)
    if image is None:
        return None, ""

    # Resize very large images to limit memory usage while preserving readability.
    height, width = image.shape[:2]
    longest = max(height, width)
    if longest > 1600:
        scale = 1600 / longest
        image = cv2.resize(image, (int(width * scale), int(height * scale)))

    reader = get_reader()
    results = reader.readtext(image, detail=1, paragraph=False)
    candidates = []
    recognized_text = []
    for _bbox, text, confidence in results:
        recognized_text.append(text)
        normalized = normalize_plate(text)
        if confidence >= 0.25 and looks_like_plate(normalized):
            candidates.append((confidence, normalized))

    best = max(candidates, default=None, key=lambda item: item[0])
    return (best[1] if best else None), " | ".join(recognized_text)
