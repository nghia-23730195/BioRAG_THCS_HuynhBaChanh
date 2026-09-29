"""Text cleaning utilities for Vietnamese textbook content."""

import re
import unicodedata

# Common Vietnamese OCR merged words and misrecognitions in textbooks
VIETNAMESE_OCR_FIXES = {
    r"\bthựcvật\b": "thực vật",
    r"\bđộngvật\b": "động vật",
    r"\bconngười\b": "con người",
    r"\bsinhsản\b": "sinh sản",
    r"\bsinhtrưởng\b": "sinh trưởng",
    r"\bpháttriển\b": "phát triển",
    r"\bhôhấp\b": "hô hấp",
    r"\bbàitiết\b": "bài tiết",
    r"\bquanghợp\b": "quang hợp",
    r"\btếbào\b": "tế bào",
    r"\blụclạp\b": "lục lạp",
    r"\bkhíkhổng\b": "khí khổng",
    r"\bkhoảnggianbào\b": "khoảng gian bào",
    r"\bmạchgỗ\b": "mạch gỗ",
    r"\bmạchrây\b": "mạch rây",
    r"\bánhsáng\b": "ánh sáng",
    r"\bnănglượng\b": "năng lượng",
    r"\bđộtbiến\b": "đột biến",
    r"\bnhiễmsắcthể\b": "nhiễm sắc thể",
    r"\bsinhvật\b": "sinh vật",
    r"\bnguyênsinh\b": "nguyên sinh",
    r"\bthínghiệm\b": "thí nghiệm",
    r"\bthựcnghiệm\b": "thực nghiệm",
    r"\bđơnchất\b": "đơn chất",
    r"\bhợpchất\b": "hợp chất",
    r"\bnguyêntử\b": "nguyên tử",
    r"\bphântử\b": "phân tử",
    r"\bnguyêntố\b": "nguyên tố",
    r"\bkhốilượng\b": "khối lượng",
    r"\btrọnglượng\b": "trọng lượng",
    r"\bápchất\b": "áp suất",
    r"\bápsuất\b": "áp suất",
    r"\blựcđẩy\b": "lực đẩy",
    r"\bkhúcxạ\b": "khúc xạ",
    r"\bphảnxạ\b": "phản xạ",
    r"\btánsắc\b": "tán sắc",
    r"\blăngkính\b": "lăng kính",
    r"\bthấukính\b": "thấu kính",
    r"\bhộitụ\b": "hội tụ",
    r"\bphankì\b": "phân kì",
    r"\bphânkì\b": "phân kì",
}


def clean_vietnamese_text(text: str) -> str:
    """Clean and normalize Vietnamese text extracted from PDF or OCR."""
    if not text:
        return ""

    # Normalize unicode to NFC
    text = unicodedata.normalize("NFC", str(text))

    # Rejoin hyphenated line breaks (e.g., 'quang-\nhợp' -> 'quang hợp')
    text = re.sub(r"(\b\w+)-\s*\n\s*(\w+\b)", r"\1\2", text)

    # Filter non-printable control chars (keep \n and \t)
    text = "".join(
        char for char in text
        if not unicodedata.category(char).startswith("C") or char in "\n\t"
    )

    # Fix scientific formulas / symbols
    text = re.sub(r"\bC02\b", "CO2", text)
    text = re.sub(r"\bCO\s*2\b", "CO2", text)
    text = re.sub(r"\b02\b(?=\s*(khí|oxygen|O2|thở|hô hấp))", "O2", text, flags=re.IGNORECASE)
    text = re.sub(r"\bO\s*2\b", "O2", text)
    text = re.sub(r"\bH20\b", "H2O", text)
    text = re.sub(r"\bH\s*2\s*O\b", "H2O", text)
    text = re.sub(r"\bPH\s*([0-9]+)\b", r"pH \1", text)

    # Fix OCR merged words
    for pattern, replacement in VIETNAMESE_OCR_FIXES.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # Normalize spaces and line breaks
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    return text.strip()


def clean_gemini_ocr_text(text: str) -> str:
    """Clean text produced by Gemini Vision OCR."""
    if not text:
        return ""

    # Normalize unicode first
    text = unicodedata.normalize("NFC", text)

    # Remove markdown code block wrappers
    text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
    text = re.sub(r"\n?```\s*$", "", text)

    # Remove markdown bold/italic markers but keep the text
    text = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", text)

    # Remove markdown headers (keep the text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)

    return clean_vietnamese_text(text)


