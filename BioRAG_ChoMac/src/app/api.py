"""Flask API Server for Biology RAG"""

import base64
import hashlib
import hmac
import json
import logging
import os
import re
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote
import torch
from flask import Flask, request, jsonify, send_file, send_from_directory, Response, stream_with_context
from flask_cors import CORS
from transformers import TextIteratorStreamer
from werkzeug.utils import secure_filename

from src.config import DATA_DIR, PERSIST_DIR, IMAGES_DIR, LLM_MAX_NEW_TOKENS, LLM_TEMPERATURE, LLM_TOP_P
from src.app.dependencies import AppServices
from src.app.learning_catalog import create_lesson, list_lessons, update_lesson
from src.etl.image_review import ImageReviewManager

logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# In-memory status tracker for ETL polling
etl_status = {}

# --- Feedback (👍/👎) trên câu trả lời chat, dùng để tinh chỉnh retrieval sau này ---
FEEDBACK_LOG_PATH = Path(PERSIST_DIR) / "chat_feedback.jsonl"
_FEEDBACK_LOCK = threading.Lock()

# BIORAG_WEB_UI_ROUTE
@app.route("/", methods=["GET"])
def web_ui():
    """Serve the BioRAG web interface."""
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )
    return send_from_directory(project_root, "index.html")


@app.route("/favicon.ico", methods=["GET"])
def web_favicon():
    return ("", 204)


@app.route("/assets/pdfjs/<path:filename>", methods=["GET"])
def web_pdfjs_asset(filename):
    """Phục vụ hai mô-đun PDF.js cục bộ; không cho duyệt tệp tùy ý."""
    allowed = {"pdf.min.mjs", "pdf.worker.min.mjs"}
    if filename not in allowed or Path(filename).name != filename:
        return jsonify({"error": "Tệp PDF.js không hợp lệ."}), 404
    project_root = Path(__file__).resolve().parents[2]
    asset_dir = project_root / "web_assets" / "pdfjs"
    response = send_from_directory(
        asset_dir,
        filename,
        mimetype="text/javascript",
        conditional=True,
        max_age=86400,
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.route("/assets/three/<path:filename>", methods=["GET"])
def web_three_asset(filename):
    """Phục vụ Three.js và OrbitControls cục bộ."""
    allowed = {"three.min.js", "OrbitControls.js", "lab_3d_engine.js"}
    if filename not in allowed or Path(filename).name != filename:
        return jsonify({"error": "Tệp Three.js không hợp lệ."}), 404
    project_root = Path(__file__).resolve().parents[2]
    asset_dir = project_root / "web_assets" / "three"
    response = send_from_directory(
        asset_dir,
        filename,
        mimetype="text/javascript",
        conditional=True,
        max_age=86400,
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


def _biorag_textbook_pdf_candidates(role="sgk"):
    """Chỉ liệt kê PDF đúng vai trò trong thư mục riêng hoặc thư mục gốc cũ."""
    role = str(role or "sgk").strip().lower()
    if role not in {"sgk", "sgv"}:
        return []
    data_dir = Path(DATA_DIR)
    candidates = []
    role_dir = data_dir / role
    if role_dir.is_dir():
        candidates.extend(path for path in role_dir.glob("*.pdf") if path.is_file())
    prefix = role + " "
    candidates.extend(
        path for path in data_dir.glob("*.pdf")
        if path.is_file() and _biorag_textbook_normalize(path.name).startswith(prefix)
    )
    unique = {}
    for path in candidates:
        unique[str(path.resolve()).lower()] = path
    return sorted(unique.values(), key=lambda path: path.name.lower())


def _biorag_resolve_source_pdf(source_name, role="sgk"):
    """Mở PDF đúng vai trò; SGV không bao giờ được dùng thay cho SGK."""
    safe_name = Path(str(source_name or "").replace("\\", "/")).name.strip()
    if not safe_name or not safe_name.lower().endswith(".pdf"):
        raise FileNotFoundError("Tên tệp sách không hợp lệ.")
    candidates = _biorag_textbook_pdf_candidates(role)
    exact = next((path for path in candidates if path.name.lower() == safe_name.lower()), None)
    if exact:
        return exact.resolve()
    safe_stem = Path(safe_name).stem.lower()
    stem_match = next((path for path in candidates if path.stem.lower() == safe_stem), None)
    if stem_match:
        return stem_match.resolve()
    normalized_requested = _biorag_textbook_source_key(safe_name)
    normalized_match = next(
        (
            path for path in candidates
            if _biorag_textbook_source_key(path.name) == normalized_requested
            and _biorag_textbook_normalize(path.name).startswith(str(role).lower() + " ")
        ),
        None,
    )
    if normalized_match:
        return normalized_match.resolve()
    label = "SGK" if role == "sgk" else "SGV"
    raise FileNotFoundError(f"Không tìm thấy tệp {label} trong thư mục datasources/{role}.")


def _biorag_resolve_textbook_pdf(source_name):
    """Tương thích API cũ nhưng luôn giới hạn vào sách giáo khoa học sinh."""
    return _biorag_resolve_source_pdf(source_name, "sgk")


_BIORAG_TEXTBOOK_TEXT_CACHE = {}
_BIORAG_TEXTBOOK_TEXT_LOCK = threading.Lock()
_BIORAG_TEXTBOOK_OCR_CACHE = {}
_BIORAG_TEXTBOOK_OCR_LOCK = threading.Lock()
_BIORAG_TESSERACT_LANGUAGE_CACHE = {}
_BIORAG_TEXTBOOK_LAYOUT_CACHE = {}


def _biorag_textbook_normalize(value):
    """Chuẩn hóa chữ tiếng Việt trong PDF để nhận diện tiêu đề Bài N."""
    import unicodedata

    value = unicodedata.normalize("NFKD", str(value or "").lower())
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = value.replace("đ", "d")
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def _biorag_textbook_source_key(value):
    """Chuẩn hóa cả biến thể KHTN8/KHTN 8 nhưng vẫn giữ SGK khác SGV."""
    normalized = _biorag_textbook_normalize(value)
    return re.sub(r"\bkhtn\s*([6-9])\b", r"khtn \1", normalized)


def _biorag_textbook_source_status(grade):
    """Phân biệt SGK học sinh, SGV giáo viên và nguồn còn thiếu theo từng lớp."""
    try:
        grade = int(grade)
    except (TypeError, ValueError):
        return {"grade": grade, "status": "invalid", "ready": False}
    expected = f"SGK KHTN {grade} KNTT.pdf"
    expected_key = _biorag_textbook_source_key(expected)
    teacher_key = _biorag_textbook_source_key(f"SGV KHTN {grade} KNTT.pdf")
    candidates = _biorag_textbook_pdf_candidates("sgk")
    student = next(
        (path for path in candidates if _biorag_textbook_source_key(path.name) == expected_key),
        None,
    )
    if student:
        return {
            "grade": grade,
            "status": "ready",
            "ready": True,
            "expected": expected,
            "found": student.name,
            "message": f"Đã sẵn sàng: {student.name}",
        }
    teacher = next(
        (
            path for path in _biorag_textbook_pdf_candidates("sgv")
            if _biorag_textbook_source_key(path.name) == teacher_key
        ),
        None,
    )
    if teacher:
        return {
            "grade": grade,
            "status": "teacher_only",
            "ready": False,
            "expected": expected,
            "found": teacher.name,
            "message": (
                f"Lớp {grade} hiện chỉ có sách giáo viên ({teacher.name}). "
                f"Hãy chép sách học sinh vào datasources với tên {expected}."
            ),
        }
    return {
        "grade": grade,
        "status": "missing",
        "ready": False,
        "expected": expected,
        "found": None,
        "message": f"Thiếu nguồn lớp {grade}. Hãy chép {expected} vào thư mục datasources.",
    }


def _biorag_textbook_source_inventory():
    """Danh mục tách riêng SGK/SGV để giao diện học sinh và giáo viên sử dụng."""
    result = {"sgk": {}, "sgv": {}}
    for grade in (6, 7, 8, 9):
        result["sgk"][str(grade)] = _biorag_textbook_source_status(grade)
        teacher_key = _biorag_textbook_source_key(f"SGV KHTN {grade} KNTT.pdf")
        teacher = next(
            (
                path for path in _biorag_textbook_pdf_candidates("sgv")
                if _biorag_textbook_source_key(path.name) == teacher_key
            ),
            None,
        )
        result["sgv"][str(grade)] = {
            "grade": grade,
            "status": "ready" if teacher else "missing",
            "ready": bool(teacher),
            "found": teacher.name if teacher else None,
            "message": (
                f"Đã sẵn sàng: {teacher.name}"
                if teacher else f"Chưa có SGV KHTN {grade} KNTT.pdf."
            ),
        }
    return result


def _biorag_lesson_number(lesson):
    """Lấy số bài từ trường number hoặc title, không suy đoán từ số trang."""
    for value in (lesson.get("number"), lesson.get("title")):
        match = re.search(r"\bbài\s*(\d{1,3})\b", str(value or ""), re.IGNORECASE)
        if match:
            return int(match.group(1))
        normalized = _biorag_textbook_normalize(value)
        match = re.search(r"\bbai\s*(\d{1,3})\b", normalized)
        if match:
            return int(match.group(1))
    return None


_BIORAG_ANY_LESSON_NUMBER_PATTERN = re.compile(r"\bbai\s*(\d{1,3})\b")


def _biorag_page_is_lesson_index(text):
    """Nhận diện trang mục lục / bảng phân phối chương trình.

    Các trang này liệt kê tên nhiều bài liên tiếp (VD: "Bài 22 ... trang 104,
    Bài 23 ... trang 108, ...") nên chứa đúng cụm "Bài N" và cả tiêu đề bài y
    hệt trang nội dung thật — khiến việc dò tiêu đề nhầm sang đây thay vì
    trang có nội dung thật. Một trang nội dung thật hầu như không nhắc quá
    vài số bài khác nhau, trong khi mục lục/bảng phân phối liệt kê hàng chục
    bài trên một trang, nên đếm số "Bài N" khác nhau là cách phân biệt đáng
    tin cậy mà không cần biết trước trang mục lục nằm ở đâu.
    """
    numbers = {match.group(1) for match in _BIORAG_ANY_LESSON_NUMBER_PATTERN.finditer(text or "")}
    return len(numbers) >= 4


def _biorag_lesson_page_hints(lesson):
    """Đọc các trang gợi ý đã lưu để chọn đúng tiêu đề thật thay vì mục lục."""
    pages = []
    for item in lesson.get("generation_sources") or []:
        if not isinstance(item, dict):
            continue
        match = re.search(r"\d+", str(item.get("page") or ""))
        if match and int(match.group(0)) > 0:
            pages.append(int(match.group(0)))
    label_match = re.search(
        r"(?:trang|pages?)\s+([0-9\s,;\-–—]+)",
        str(lesson.get("source_label") or ""),
        re.IGNORECASE,
    )
    if label_match:
        for token in re.split(r"[;,]", label_match.group(1)):
            range_match = re.search(r"(\d+)\s*[\-–—]\s*(\d+)", token)
            if range_match:
                start, end = int(range_match.group(1)), int(range_match.group(2))
                if 0 < start <= end and end - start <= 30:
                    pages.extend(range(start, end + 1))
            else:
                single = re.search(r"\d+", token)
                if single and int(single.group(0)) > 0:
                    pages.append(int(single.group(0)))
    return sorted(set(pages))


def _biorag_textbook_uses_two_page_spreads(pdf_path, hints=None):
    """Nhận dạng bản SGK 9 được lưu thành ảnh ngang gồm hai trang in."""
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz

    pdf_path = Path(pdf_path).resolve()
    stat = pdf_path.stat()
    key = (str(pdf_path), stat.st_mtime_ns, stat.st_size)
    if key in _BIORAG_TEXTBOOK_LAYOUT_CACHE:
        return _BIORAG_TEXTBOOK_LAYOUT_CACHE[key]
    normalized_name = _biorag_textbook_normalize(pdf_path.name)
    is_khtn9 = normalized_name == "sgk khtn 9 kntt pdf"
    result = False
    if is_khtn9:
        with fitz.open(pdf_path) as document:
            raw_hints = [int(page) for page in (hints or []) if int(page) > 0]
            printed_hint = min(raw_hints) if raw_hints else 34
            sample_page = max(1, min(document.page_count, (printed_hint + 4) // 2))
            rect = document[sample_page - 1].rect
            result = rect.width > rect.height * 1.2
    _BIORAG_TEXTBOOK_LAYOUT_CACHE[key] = result
    return result


def _biorag_lesson_pdf_hints(pdf_path, printed_hints):
    """Đổi số trang in sang trang PDF theo bố cục thật của từng bản sách."""
    return sorted({int(page) + 1 for page in printed_hints if int(page) > 0})


def _biorag_estimated_lesson_pdf_hint(lesson, lesson_number, page_count):
    """Ước lượng vùng OCR cho bài chưa có số trang, không coi đó là kết quả."""
    try:
        grade = int(lesson.get("grade"))
        lesson_number = int(lesson_number)
        page_count = int(page_count)
    except (TypeError, ValueError):
        return None
    totals = {6: 55, 7: 42, 8: 47, 9: 51}
    total = totals.get(grade)
    if not total or lesson_number < 1 or page_count < 1:
        return None
    # Phân bố số bài theo chiều dài sách cho vùng tìm kiếm ban đầu. Kết quả cuối
    # vẫn bắt buộc OCR thấy đúng "Bài N" và tiêu đề, nên không học nhầm trang.
    ratio = min(1.0, max(0.0, lesson_number / total))
    return max(1, min(page_count, round(2 + ratio * max(1, page_count - 4))))


def _biorag_printed_pages_for_pdf_page(pdf_path, pdf_page):
    """Trả về cặp trang in tương ứng để giao diện ghi nhãn rõ ràng."""
    if int(pdf_page) > 1:
        printed = int(pdf_page) - 1
        return (printed, printed)
    return None


def _biorag_resolved_textbook_page_row(pdf_path, page):
    row = {"source": Path(pdf_path).name, "page": int(page)}
    printed = _biorag_printed_pages_for_pdf_page(pdf_path, page)
    if printed:
        row["printed_start"] = printed[0]
        row["printed_end"] = printed[1]
    return row


def _biorag_lesson_pdf_path(lesson):
    """Ưu tiên tên PDF trong nhãn nguồn, sau đó mới xét generation_sources."""
    label_prefix = str(lesson.get("source_label") or "").split("·", 1)[0]
    label_prefix = re.sub(r"^\s*Nguồn:\s*", "", label_prefix, flags=re.IGNORECASE).strip()
    candidates = [label_prefix]
    candidates.extend(
        str(item.get("source") or "")
        for item in (lesson.get("generation_sources") or [])
        if isinstance(item, dict)
    )
    for value in candidates:
        name = Path(value.replace("\\", "/")).name.strip()
        if not name:
            continue
        if not name.lower().endswith(".pdf"):
            name = str(Path(name).with_suffix(".pdf"))
        try:
            return _biorag_resolve_textbook_pdf(name)
        except FileNotFoundError:
            continue
    return None


def _biorag_textbook_page_texts(pdf_path):
    """Trích văn bản toàn sách một lần và cache theo kích thước/thời gian sửa."""
    try:
        import pymupdf as fitz
    except ImportError:
        import fitz

    pdf_path = Path(pdf_path).resolve()
    stat = pdf_path.stat()
    key = (str(pdf_path), stat.st_mtime_ns, stat.st_size)
    with _BIORAG_TEXTBOOK_TEXT_LOCK:
        cached = _BIORAG_TEXTBOOK_TEXT_CACHE.get(key)
    if cached is not None:
        return cached
    with fitz.open(pdf_path) as document:
        texts = tuple(
            _biorag_textbook_normalize(page.get_text("text"))
            for page in document
        )
    with _BIORAG_TEXTBOOK_TEXT_LOCK:
        for old_key in list(_BIORAG_TEXTBOOK_TEXT_CACHE):
            if old_key[0] == str(pdf_path) and old_key != key:
                _BIORAG_TEXTBOOK_TEXT_CACHE.pop(old_key, None)
        while len(_BIORAG_TEXTBOOK_TEXT_CACHE) >= 8:
            _BIORAG_TEXTBOOK_TEXT_CACHE.pop(next(iter(_BIORAG_TEXTBOOK_TEXT_CACHE)))
        _BIORAG_TEXTBOOK_TEXT_CACHE[key] = texts
    return texts


def _biorag_tesseract_languages(binary):
    """Chọn bộ ngôn ngữ OCR có thật; ưu tiên tiếng Việt và tiếng Anh."""
    import subprocess

    binary = str(binary)
    cached = _BIORAG_TESSERACT_LANGUAGE_CACHE.get(binary)
    if cached:
        return cached
    result = subprocess.run(
        [binary, "--list-langs"], capture_output=True, text=True,
        encoding="utf-8", errors="replace", timeout=20,
    )
    available = {
        line.strip() for line in (result.stdout or "").splitlines()
        if line.strip() and "available languages" not in line.lower()
    }
    if "vie" in available and "eng" in available:
        selected = "vie+eng"
    elif "vie" in available:
        selected = "vie"
    elif "eng" in available:
        selected = "eng"
    else:
        selected = next(iter(sorted(available)), "eng")
    _BIORAG_TESSERACT_LANGUAGE_CACHE[binary] = selected
    return selected


def _biorag_ocr_pdf_headers(pdf_path, page_numbers):
    """OCR riêng phần đầu các trang cần thiết và cache theo phiên bản PDF."""
    import hashlib
    import shutil
    import subprocess
    import tempfile

    try:
        import pymupdf as fitz
    except ImportError:
        import fitz

    binary = os.environ.get("TESSERACT_CMD") or shutil.which("tesseract")
    if not binary:
        logger.warning("Không tìm thấy Tesseract; bỏ qua nhận diện tiêu đề PDF ảnh.")
        return {}
    pdf_path = Path(pdf_path).resolve()
    stat = pdf_path.stat()
    version = (str(pdf_path), stat.st_mtime_ns, stat.st_size)
    requested = sorted({int(page) for page in page_numbers if int(page) > 0})
    output = {}
    missing = []
    with _BIORAG_TEXTBOOK_OCR_LOCK:
        for page in requested:
            key = version + (page,)
            if key in _BIORAG_TEXTBOOK_OCR_CACHE:
                output[page] = _BIORAG_TEXTBOOK_OCR_CACHE[key]
            else:
                missing.append(page)
    if not missing:
        return output

    language = _biorag_tesseract_languages(binary)
    language_key = re.sub(r"[^a-z0-9]+", "-", language.lower()).strip("-") or "default"
    cache_dir = Path(PERSIST_DIR) / "lesson_ocr_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    version_hash = hashlib.sha256(
        f"ocr-v27-title-fallback|{pdf_path}|{stat.st_mtime_ns}|{stat.st_size}".encode("utf-8")
    ).hexdigest()[:18]
    with fitz.open(pdf_path) as document:
        for page_number in missing:
            if page_number > document.page_count:
                continue
            disk_path = cache_dir / f"{version_hash}-{language_key}-p{page_number:04d}.txt"
            if disk_path.is_file():
                normalized = disk_path.read_text(encoding="utf-8", errors="replace").strip()
            else:
                page = document[page_number - 1]
                top = page.rect.height * 0.62
                if page.rect.width > page.rect.height * 1.2:
                    middle = page.rect.width / 2
                    clips = (
                        fitz.Rect(0, 0, middle, top),
                        fitz.Rect(middle, 0, page.rect.width, top),
                    )
                else:
                    clips = (fitz.Rect(0, 0, page.rect.width, top),)
                recognized = []
                for clip in clips:
                    pixmap = page.get_pixmap(
                        matrix=fitz.Matrix(2.2, 2.2), clip=clip, alpha=False
                    )
                    temp_name = None
                    try:
                        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
                            temp_name = temp_file.name
                        pixmap.save(temp_name)
                        result = subprocess.run(
                            [binary, temp_name, "stdout", "-l", language, "--psm", "6"],
                            capture_output=True, text=True, encoding="utf-8", errors="replace",
                            timeout=45,
                        )
                        if result.returncode == 0:
                            recognized.append(result.stdout)
                        else:
                            logger.warning(
                                "OCR trang PDF %s không đạt: %s",
                                page_number, result.stderr.strip(),
                            )
                    finally:
                        if temp_name:
                            Path(temp_name).unlink(missing_ok=True)
                normalized = _biorag_textbook_normalize(" ".join(recognized))
                disk_path.write_text(normalized, encoding="utf-8")
            key = version + (page_number,)
            with _BIORAG_TEXTBOOK_OCR_LOCK:
                _BIORAG_TEXTBOOK_OCR_CACHE[key] = normalized
            output[page_number] = normalized
    return output


def _biorag_resolve_lesson_pdf_pages_ocr(lesson, pdf_path, lesson_number, hints, page_count):
    """Tìm biên bài trong PDF ảnh và xác minh đồng thời số bài, tên bài."""
    estimated_hint = False
    if not hints:
        estimated = _biorag_estimated_lesson_pdf_hint(lesson, lesson_number, page_count)
        if estimated is None:
            return None
        hints = [estimated]
        estimated_hint = True
    title_tokens = {
        token for token in _biorag_textbook_normalize(lesson.get("title")).split()
        if len(token) >= 3 and token not in {"bai", "chuong", "phan"}
    }
    # Neo vào trang BẮT ĐẦU (nhỏ nhất) của dải gợi ý, không lấy trung bình cả
    # dải — vì source_label giờ lưu nguyên dải "Trang start–end" của cả bài
    # (không chỉ 1-2 điểm rời rạc như trước), nên trung bình sẽ lệch về giữa/
    # cuối bài và có thể khiến trang có tiêu đề thật (ở đầu dải) bị chấm điểm
    # kém hơn trang kế tiếp, gây mở nhầm sang trang sau tiêu đề thật một trang.
    hint_start = min(hints)
    hint_end = max(hints)
    hint_center = hint_start
    pattern = re.compile(rf"\bbai\s*{lesson_number}\b")
    minimum_title_overlap = min(2, len(title_tokens))
    if estimated_hint:
        # Hint chỉ là ước lượng tỉ lệ tuyến tính (không đáng tin), nên vẫn cần
        # quét rộng dần như trước.
        windows = [
            (max(1, hint_start - 5), min(page_count, hint_end + 7)),
            (max(1, hint_start - 20), min(page_count, hint_end + 24)),
            (max(1, hint_start - 48), min(page_count, hint_end + 52)),
            (1, page_count),
        ]
    else:
        # Hint giờ là dải trang đã xác minh từ mục lục thật của sách (không
        # còn là ước lượng nữa), nên không cần quét rộng như trước — mỗi
        # trang OCR tốn cả giây, quét ít trang hơn giúp mở bài học nhanh hơn
        # nhiều mà vẫn đủ để bắt được tiêu đề thật (kể cả khi tiêu đề trang
        # đầu bị OCR đọc sai và phải rơi vào phương án dự phòng title_only ở
        # vài trang nội dung ngay sau đó).
        windows = [
            (max(1, hint_start - 2), min(page_count, hint_start + 10)),
            (max(1, hint_start - 10), min(page_count, hint_end + 15)),
        ]
    # Khớp đúng số "Bài N" luôn đáng tin hơn nhiều so với chỉ trùng vài từ
    # tiêu đề (title_only) — 2 từ chung chung như "thực"/"vật" có thể tình cờ
    # xuất hiện ở BẤT KỲ trang nào. Trước đây vòng lặp dừng ngay khi cửa sổ
    # tìm kiếm gần nhất có bất kỳ ứng viên nào (kể cả title_only yếu), nên một
    # trùng khớp tình cờ ở gần vị trí ước lượng có thể chặn mất trang đúng nằm
    # ở cửa sổ rộng hơn. Giờ luôn tiếp tục mở rộng tìm kiếm cho đến khi thấy
    # một khớp SỐ BÀI chính xác; chỉ chấp nhận title_only làm phương án cuối
    # cùng nếu quét hết mọi cửa sổ (kể cả toàn sách với estimated_hint) mà
    # không tìm được số bài chính xác nào.
    best_exact = None
    best_title = None
    for search_start, search_end in windows:
        current_headers = _biorag_ocr_pdf_headers(
            pdf_path, range(search_start, search_end + 1)
        )
        for page_number, text in current_headers.items():
            if _biorag_page_is_lesson_index(text):
                continue
            match = pattern.search(text)
            overlap = len(title_tokens.intersection(text.split()))
            title_only = match is None
            if title_only and (
                minimum_title_overlap < 1
                or overlap < minimum_title_overlap
                or abs(page_number - hint_center) > (18 if estimated_hint else 4)
            ):
                continue
            if not title_only and title_tokens and overlap < 1:
                continue
            match_start = match.start() if match else 0
            score = (
                abs(page_number - hint_center) * 10
                + match_start / 80
                - overlap * 12
                + (35 if title_only else 0)
            )
            candidate = (score, page_number, overlap, title_only)
            if title_only:
                if best_title is None or candidate < best_title:
                    best_title = candidate
            elif best_exact is None or candidate < best_exact:
                best_exact = candidate
        if best_exact is not None:
            break
    selected = best_exact if best_exact is not None else best_title
    if selected is None:
        return None
    start_page = selected[1]
    title_only = selected[3]

    # Trước đây luôn quét 20 trang kế tiếp để tìm tiêu đề "Bài N+1" cho dù bài
    # học đã có hint dài bao nhiêu — rất lãng phí OCR với các bài ngắn. Giờ
    # chỉ quét quá điểm cuối đã biết (hint_end) thêm một khoảng an toàn nhỏ.
    next_search_cap = min(page_count, start_page + 20)
    if not estimated_hint:
        next_search_cap = min(next_search_cap, max(start_page + 3, hint_end + 6))
    next_pages = range(start_page + 1, next_search_cap + 1)
    next_headers = _biorag_ocr_pdf_headers(pdf_path, next_pages)
    next_pattern = re.compile(rf"\bbai\s*{lesson_number + 1}\b")
    next_start = next(
        (page for page in sorted(next_headers) if next_pattern.search(next_headers[page])),
        None,
    )
    if next_start:
        end_page = next_start - 1
    else:
        valid_hints = [page for page in hints if page >= start_page]
        end_page = max(valid_hints) if valid_hints else min(start_page + 4, page_count)
    end_page = max(start_page, min(end_page, start_page + 19, page_count))
    return {
        "source": pdf_path.name,
        "start_page": start_page,
        "end_page": end_page,
        "pages": list(range(start_page, end_page + 1)),
        "method": (
            "pdf_spread_header_ocr"
            if _biorag_textbook_uses_two_page_spreads(pdf_path)
            else (
                "pdf_header_estimated_ocr" if estimated_hint
                else ("pdf_header_title_ocr" if title_only else "pdf_header_ocr")
            )
        ),
    }


def _biorag_resolve_lesson_pdf_pages(lesson):
    """Tìm dải trang từ tiêu đề Bài N đến ngay trước Bài N+1 trong PDF thật."""
    if not isinstance(lesson, dict):
        return None
    lesson_number = _biorag_lesson_number(lesson)
    pdf_path = _biorag_lesson_pdf_path(lesson)
    if lesson_number is None or pdf_path is None:
        return None
    texts = _biorag_textbook_page_texts(pdf_path)
    printed_hints = _biorag_lesson_page_hints(lesson)
    hints = _biorag_lesson_pdf_hints(pdf_path, printed_hints)
    scoring_hints = list(hints)
    if not scoring_hints:
        estimated = _biorag_estimated_lesson_pdf_hint(lesson, lesson_number, len(texts))
        if estimated is not None:
            scoring_hints = [estimated]
    # Cùng lý do với _biorag_resolve_lesson_pdf_pages_ocr: neo vào trang bắt
    # đầu của dải gợi ý thay vì lấy trung bình cả dải.
    hint_center = min(scoring_hints) if scoring_hints else None
    title_tokens = {
        token for token in _biorag_textbook_normalize(lesson.get("title")).split()
        if len(token) >= 3 and token not in {"bai", "chuong", "phan"}
    }

    def candidates(number):
        pattern = re.compile(rf"\bbai\s*{number}\b")
        found = []
        for page, text in enumerate(texts, start=1):
            match = pattern.search(text)
            if not match:
                continue
            if _biorag_page_is_lesson_index(text):
                # Trang mục lục/bảng phân phối liệt kê nhiều "Bài N" khác nhau
                # — bỏ qua để không nhầm là trang nội dung của chính bài này.
                continue
            overlap = len(title_tokens.intersection(text.split())) if number == lesson_number else 0
            distance = abs(page - hint_center) if hint_center is not None else page
            heading_penalty = 0 if match.start() <= 260 else 18
            found.append((distance * 10 + heading_penalty - overlap * 6, page, match.start()))
        return sorted(found)

    current_candidates = candidates(lesson_number)
    if not current_candidates:
        return _biorag_resolve_lesson_pdf_pages_ocr(
            lesson, pdf_path, lesson_number, hints, len(texts)
        )
    start_page = current_candidates[0][1]
    next_candidates = [item for item in candidates(lesson_number + 1) if item[1] > start_page]
    preferred_next = [item for item in next_candidates if item[2] <= 260]
    if preferred_next:
        end_page = min(item[1] for item in preferred_next) - 1
    elif next_candidates:
        end_page = min(item[1] for item in next_candidates) - 1
    else:
        valid_hints = [page for page in hints if page >= start_page]
        end_page = max(valid_hints) if valid_hints else start_page
    end_page = max(start_page, min(end_page, start_page + 11, len(texts)))
    return {
        "source": pdf_path.name,
        "start_page": start_page,
        "end_page": end_page,
        "pages": list(range(start_page, end_page + 1)),
        "method": "pdf_lesson_heading",
    }


def _biorag_split_lesson_textbook_pages(lesson, pdf_path):
    """Tách hiển thị SGK 2-trang-in/1-ảnh (lớp 9) thành từng trang in riêng lẻ.

    Dùng thẳng dải trang in đã xác minh từ mục lục thật của sách
    (_biorag_lesson_page_hints) thay vì suy ra từ trang PDF (vật lý) mà OCR
    tiêu đề tìm được — vì OCR tiêu đề hiện gộp chung văn bản cả nửa trái lẫn
    nửa phải của một trang ảnh nên không phân biệt được bài học bắt đầu ở nửa
    nào; còn dải trang in từ mục lục vốn đã là dữ liệu chính xác theo từng
    trang lẻ. Mỗi trang in ứng với đúng một "trang ảo" duy nhất, khớp với quy
    ước trong _biorag_render_textbook_page.
    """
    printed_hints = _biorag_lesson_page_hints(lesson)
    if not printed_hints:
        return None
    rows = []
    for printed in printed_hints:
        if printed < 2:
            continue
        physical_page = printed // 2 + 2
        is_left_half = printed % 2 == 0
        virtual_page = physical_page * 2 - 1 if is_left_half else physical_page * 2
        rows.append({
            "source": pdf_path.name,
            "page": virtual_page,
            "printed_start": printed,
            "printed_end": printed,
            "virtual": True,
        })
    return rows or None


def _biorag_enrich_lesson_textbook_pages(lesson):
    """Thêm dải trang đã xác minh vào phản hồi; không ghi lại catalog/database."""
    enriched = dict(lesson)
    try:
        resolved = _biorag_resolve_lesson_pdf_pages(lesson)
    except Exception as exc:
        logger.warning("Lesson PDF page resolution failed for %s: %s", lesson.get("id"), exc)
        resolved = None
    if resolved:
        resolved_pdf_path = _biorag_lesson_pdf_path(lesson)
        split_rows = None
        if resolved_pdf_path and _biorag_textbook_uses_two_page_spreads(resolved_pdf_path):
            split_rows = _biorag_split_lesson_textbook_pages(lesson, resolved_pdf_path)
        enriched["resolved_textbook_pages"] = split_rows or [
            (
                _biorag_resolved_textbook_page_row(resolved_pdf_path, page)
                if resolved_pdf_path else {"source": resolved["source"], "page": page}
            )
            for page in resolved["pages"]
        ]
        enriched["textbook_range"] = {
            "start_page": resolved["start_page"],
            "end_page": resolved["end_page"],
            "method": resolved["method"],
        }
    return enriched


def _biorag_render_textbook_page(pdf_path, page_number, virtual=False):
    """Kết xuất một trang PDF nguyên bản thành PNG và cache theo phiên bản tệp.

    virtual=True CHỈ dùng cho trình đọc bài học (nơi số trang hiển thị đã là
    "trang ảo" do _biorag_split_lesson_textbook_pages sinh ra): với các SGK
    dạng ảnh 2 trang in/1 trang PDF (lớp 9, xem
    _biorag_textbook_uses_two_page_spreads), mỗi trang ảo ứng với đúng MỘT
    trang in — trang ảo lẻ = nửa trái, trang ảo chẵn = nửa phải của trang PDF
    vật lý số ceil(virtual/2) — để học sinh xem từng trang riêng lẻ thay vì bị
    dồn 2 trang chật hẹp vào một khung hình. Các nơi gọi khác (trích dẫn ảnh
    SGK trong chat, vốn dùng số trang PDF vật lý thật từ metadata) PHẢI giữ
    virtual=False (mặc định) để không đổi hành vi render trang gộp như cũ.
    """
    import hashlib
    try:
        import pymupdf as fitz
    except ImportError:  # Tương thích với các bản PyMuPDF cũ.
        import fitz

    pdf_path = Path(pdf_path).resolve()
    page_number = int(page_number)
    if page_number < 1:
        raise IndexError("Số trang phải lớn hơn 0.")
    stat = pdf_path.stat()
    cache_key = hashlib.sha256(
        f"{pdf_path}|{stat.st_mtime_ns}|{stat.st_size}|{page_number}|"
        f"{'virtual' if virtual else 'raw'}-v1".encode("utf-8")
    ).hexdigest()[:20]
    safe_stem = re.sub(r"[^a-zA-Z0-9_-]+", "-", pdf_path.stem).strip("-") or "sgk"
    cache_dir = Path(PERSIST_DIR) / "learning_pages"
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / f"{safe_stem}-{cache_key}-p{page_number:04d}.png"
    if cache_path.is_file() and cache_path.stat().st_size > 1000:
        return cache_path

    is_spread = virtual and _biorag_textbook_uses_two_page_spreads(pdf_path)
    with fitz.open(pdf_path) as document:
        if is_spread:
            physical_page = (page_number + 1) // 2
            is_left_half = page_number % 2 == 1
            if physical_page > document.page_count:
                raise IndexError(f"SGK chỉ có {document.page_count * 2} trang.")
            page = document.load_page(physical_page - 1)
            rect = page.rect
            middle = rect.width / 2
            clip = (
                fitz.Rect(rect.x0, rect.y0, rect.x0 + middle, rect.y1)
                if is_left_half
                else fitz.Rect(rect.x0 + middle, rect.y0, rect.x1, rect.y1)
            )
            pixmap = page.get_pixmap(matrix=fitz.Matrix(2.3, 2.3), clip=clip, alpha=False)
        else:
            if page_number > document.page_count:
                raise IndexError(f"SGK chỉ có {document.page_count} trang.")
            page = document.load_page(page_number - 1)
            pixmap = page.get_pixmap(matrix=fitz.Matrix(1.65, 1.65), alpha=False)
        png_bytes = pixmap.tobytes("png")
    temp_path = cache_path.with_suffix(
        f".{os.getpid()}.{threading.get_ident()}.tmp"
    )
    temp_path.write_bytes(png_bytes)
    temp_path.replace(cache_path)
    return cache_path


@app.route("/api/learning/textbook-page", methods=["GET"])
def learning_textbook_page():
    """Hiển thị đúng một trang thuộc PDF SGK cục bộ; không nhận đường dẫn tùy ý."""
    source_name = request.args.get("source", "")
    try:
        page_number = int(request.args.get("page", "0"))
        pdf_path = _biorag_resolve_textbook_pdf(source_name)
        # Trình đọc bài học luôn gửi lên số "trang ảo" (đã tách theo từng
        # trang in) khi sách nguồn là dạng ảnh 2 trang/1 ảnh.
        image_path = _biorag_render_textbook_page(pdf_path, page_number, virtual=True)
    except (TypeError, ValueError, IndexError, FileNotFoundError) as exc:
        return jsonify({"error": str(exc)}), 404
    except Exception as exc:
        logger.error("Textbook page render failed: %s", exc, exc_info=True)
        return jsonify({"error": "Chưa kết xuất được trang SGK nguyên bản."}), 500
    response = send_file(image_path, mimetype="image/png", conditional=True, max_age=86400)
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.route("/api/learning/textbook-pdf", methods=["GET"])
def learning_textbook_pdf():
    """Mở toàn bộ PDF SGK cục bộ bằng trình đọc PDF của trình duyệt."""
    source_name = request.args.get("source", "")
    try:
        pdf_path = _biorag_resolve_textbook_pdf(source_name)
    except FileNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404
    except Exception as exc:
        logger.error("Textbook PDF open failed: %s", exc, exc_info=True)
        return jsonify({"error": "Chưa mở được tệp SGK đầy đủ."}), 500
    response = send_file(
        pdf_path,
        mimetype="application/pdf",
        as_attachment=False,
        download_name=pdf_path.name,
        conditional=True,
        max_age=3600,
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.route("/api/learning/source-pdf", methods=["GET"])
def learning_source_pdf():
    """Mở SGK hoặc SGV theo đúng kho đã tách; không nhận đường dẫn tùy ý."""
    source_name = request.args.get("source", "")
    role = request.args.get("role", "sgk").strip().lower()
    if role not in {"sgk", "sgv"}:
        return jsonify({"error": "Vai trò nguồn sách không hợp lệ."}), 400
    try:
        pdf_path = _biorag_resolve_source_pdf(source_name, role)
    except FileNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404
    response = send_file(
        pdf_path,
        mimetype="application/pdf",
        as_attachment=False,
        download_name=pdf_path.name,
        conditional=True,
        max_age=3600,
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-BioRAG-Book-Role"] = role.upper()
    return response



def sse_event(event, payload):
    return f"event: {event}\ndata: {json.dumps(payload, ensure_ascii=False, default=str)}\n\n"


def build_gallery_items(image_docs):
    gallery_items = []
    for doc in image_docs:
        if hasattr(doc, "metadata"):
            raw_image_path = doc.metadata.get("image_path", "")
            image_path = (
                os.path.relpath(raw_image_path, str(IMAGES_DIR)).replace(chr(92), "/")
                if raw_image_path
                else ""
            )
            page = doc.metadata.get("page_number", "?")
            pdf = doc.metadata.get("pdf_filename", "Sách Giáo Khoa")

            caption = doc.metadata.get("caption") or ""
            figure_caption = doc.metadata.get("figure_caption") or ""
            figure_label = doc.metadata.get("figure_label") or ""
            context_text = doc.metadata.get("context_text") or ""
            fallback_text = (doc.page_content or "").splitlines()[0] if doc.page_content else ""
            label_text = figure_caption or figure_label or caption or context_text or fallback_text

            label = f"{label_text[:80]}... (Trang {page}, {pdf})" if label_text else f"Trang {page} - {pdf}"

            gallery_items.append({
                "image_path": image_path,
                "label": label,
                "metadata": doc.metadata
            })
    return gallery_items


def prepare_chat_payload(question, top_k=None):
    services = AppServices.get_instance()
    result = services.hybrid_retriever.search(question, text_k=top_k)
    text_docs = result.text_docs
    image_docs = result.image_docs
    image_only_query = result.image_only_query
    gallery_items = build_gallery_items(image_docs)

    if not text_docs and not image_docs:
        if image_only_query:
            return {
                "mode": "static",
                "answer": "Không tìm thấy hình ảnh liên quan trong cơ sở dữ liệu ảnh.",
                "images": gallery_items,
                "services": services,
            }
        return {
            "mode": "static",
            "answer": "Hệ thống chưa tìm thấy tài liệu nào liên quan đến câu hỏi này.",
            "images": gallery_items,
            "services": services,
        }

    if image_only_query:
        return {
            "mode": "static",
            "answer": f"Mình tìm thấy {len(image_docs)} hình ảnh liên quan trong cơ sở dữ liệu ảnh.",
            "images": gallery_items,
            "services": services,
        }

    if not text_docs:
        return {
            "mode": "static",
            "answer": "Không tìm thấy thông tin dạng văn bản liên quan. Vui lòng thử câu hỏi khác.",
            "images": gallery_items,
            "services": services,
        }

    context_texts = [doc.page_content for doc in text_docs if hasattr(doc, "page_content")]
    context_str = "\n\n".join(context_texts)

    citations = set()
    for doc in text_docs:
        source = doc.metadata.get("source", "Sách Giáo Khoa") if hasattr(doc, "metadata") else "Sách Giáo Khoa"
        page = doc.metadata.get("page", "?") if hasattr(doc, "metadata") else "?"
        citations.add(f"Trang {page} - {source}")
    citations_str = " | ".join(sorted(citations))

    return {
        "mode": "llm",
        "formatted_prompt": services.rag.prompt.format(context=context_str, question=question),
        "citations_str": citations_str,
        "images": gallery_items,
        "services": services,
    }


def append_citations(answer, citations_str):
    if "không được đề cập" not in answer.lower() and citations_str:
        return f"{answer}\n\n📚 Thông tin được tham khảo từ: {citations_str}"
    return answer


def stream_static_answer(answer):
    for word in answer.split(" "):
        yield f"{word} "


def stream_llm_text(services, formatted_prompt):
    model_pipeline = getattr(services.llm, "pipeline", None)
    if model_pipeline is None:
        yield str(services.llm.invoke(formatted_prompt))
        return

    tokenizer = model_pipeline.tokenizer
    model = model_pipeline.model
    streamer = TextIteratorStreamer(
        tokenizer,
        skip_prompt=True,
        skip_special_tokens=True,
    )
    inputs = tokenizer(formatted_prompt, return_tensors="pt")
    device = getattr(model, "device", None)
    if device is not None:
        inputs = {key: value.to(device) for key, value in inputs.items()}

    eos_token_id = tokenizer.eos_token_id
    pad_token_id = tokenizer.pad_token_id if tokenizer.pad_token_id is not None else eos_token_id
    generation_kwargs = {
        **inputs,
        "streamer": streamer,
        "max_new_tokens": LLM_MAX_NEW_TOKENS,
        "do_sample": True,
        "temperature": LLM_TEMPERATURE,
        "top_p": LLM_TOP_P,
        "pad_token_id": pad_token_id,
        "eos_token_id": eos_token_id,
    }
    generation_error = {}

    def generate():
        try:
            with torch.inference_mode():
                model.generate(**generation_kwargs)
        except Exception as exc:
            generation_error["error"] = exc
            if hasattr(streamer, "on_finalized_text"):
                streamer.on_finalized_text("", stream_end=True)

    thread = threading.Thread(target=generate)
    thread.start()
    for text in streamer:
        if text:
            yield text
    thread.join()

    if generation_error:
        raise generation_error["error"]


def create_chat_stream_response(question):
    def generate_events():
        try:
            yield sse_event("status", {"type": "status", "stage": "retrieving"})
            payload = prepare_chat_payload(question, top_k=data.get("top_k"))

            if payload["mode"] == "static":
                answer = payload["answer"]
                yield sse_event("status", {"type": "status", "stage": "answering"})
                for chunk in stream_static_answer(answer):
                    yield sse_event("answer_delta", {"type": "answer_delta", "delta": chunk})
                yield sse_event("done", {
                    "type": "done",
                    "answer": answer,
                    "images": payload["images"],
                })
                return

            yield sse_event("status", {"type": "status", "stage": "answering"})
            chunks = []
            for chunk in stream_llm_text(payload["services"], payload["formatted_prompt"]):
                chunks.append(chunk)
                yield sse_event("answer_delta", {"type": "answer_delta", "delta": chunk})

            parsed_answer = payload["services"].rag.answer_parser.parse("".join(chunks))
            answer = append_citations(parsed_answer, payload["citations_str"])
            yield sse_event("done", {
                "type": "done",
                "answer": answer,
                "images": payload["images"],
            })
        except Exception as e:
            logger.error(f"Error streaming answer: {e}", exc_info=True)
            yield sse_event("error", {"type": "error", "error": str(e)})

    return Response(
        stream_with_context(generate_events()),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )

def run_etl_background(filename):
    from main import run_etl  # Import locally to avoid circular dependency
    etl_status[filename] = {"status": "processing", "message": "ETL pipeline is running"}
    try:
        run_etl()
        etl_status[filename] = {"status": "completed", "message": "ETL completed successfully"}
    except Exception as e:
        logger.error(f"ETL failed for {filename}: {e}")
        etl_status[filename] = {"status": "error", "message": str(e)}

@app.route('/api/etl', methods=['POST'])
def upload_and_etl():
    """Upload a PDF and trigger ETL process."""
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        os.makedirs(DATA_DIR, exist_ok=True)
        filepath = os.path.join(DATA_DIR, filename)
        file.save(filepath)
        
        # Start ETL in background
        thread = threading.Thread(target=run_etl_background, args=(filename,))
        thread.start()
        
        return jsonify({"message": f"File {filename} uploaded successfully. ETL started in background.", "filename": filename}), 202
    return jsonify({"error": "Only PDF files are allowed"}), 400

@app.route('/api/etl/status', methods=['GET'])
def get_etl_status():
    """Check ETL status for a given PDF filename."""
    filename = request.args.get('filename')
    if not filename:
        return jsonify({"error": "Filename parameter is required"}), 400
    
    status_info = etl_status.get(filename)
    if not status_info:
        # Check if it was already processed before server start
        try:
            from main import get_processed_files, get_processed_images
            text_done = filename in get_processed_files()
            image_done = filename in get_processed_images()
            if text_done and image_done:
                return jsonify({"status": "completed", "message": "File was already processed."}), 200
        except Exception as e:
            logger.warning(f"Failed to check processed files: {e}")
            
        return jsonify({"status": "not_found", "message": "No ETL task found for this file."}), 404
        
    return jsonify(status_info), 200

@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat endpoint using book_rag with Gemini."""
    import asyncio
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Question is required"}), 400

    question = data['question']
    try:
        # Try book_rag first (Gemini + vectorstore)
        import sys as _sys, os as _os
        _sys.path.insert(0, str(_os.path.dirname(_os.path.dirname(_os.path.dirname(__file__)))))
        import importlib.util as _ius
        _spec = _ius.spec_from_file_location(
            "book_rag",
            _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.dirname(__file__))),
                         "src/rag/book_rag.py"))
        _mod = _ius.module_from_spec(_spec)
        _spec.loader.exec_module(_mod)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        answer = loop.run_until_complete(_mod.answer_question(question))
        loop.close()
        # BIORAG_SOURCE_METADATA
        # Dùng chính bộ truy hồi của book_rag để trả nguồn cùng câu trả lời.
        source_chunks = _mod.find_relevant_chunks(
            question,
            _mod.load_all_chunks(),
            top_k=5,
        )
        sources = []
        seen_sources = set()
        for chunk in source_chunks:
            source_name = chunk.get("source") or "Sách giáo khoa KNTT"
            source_page = chunk.get("page", "?")
            source_key = (str(source_name), str(source_page))
            if source_key in seen_sources:
                continue
            seen_sources.add(source_key)
            sources.append({"source": source_name, "page": source_page})
            if len(sources) >= 4:
                break

        return jsonify({
            "answer": answer,
            # BIORAG_CHAT_IMAGE_SEARCH
            "images": build_gallery_items(AppServices.get_instance().hybrid_retriever.search(question, text_k=data.get("top_k"), image_k=4).image_docs),
            "sources": sources,
        })
    except Exception as e:
        logger.error(f"book_rag failed: {e}")
        # Fallback to old RAG chain
        try:
            payload = prepare_chat_payload(question, top_k=data.get("top_k"))
            if payload["mode"] == "static":
                answer = payload["answer"]
            else:
                try:
                    llm_response = payload["services"].llm.invoke(payload["formatted_prompt"])
                    answer = payload["services"].rag.answer_parser.parse(llm_response)
                except Exception as llm_err:
                    logger.error(f"RAG chain failed: {llm_err}")
                    answer = "Xin lỗi, đã xảy ra lỗi khi tạo câu trả lời."
                answer = append_citations(answer, payload["citations_str"])
            return jsonify({"answer": answer, "images": payload["images"]})
        except Exception as e2:
            logger.error(f"Fallback also failed: {e2}", exc_info=True)
            return jsonify({"error": str(e2)}), 500


@app.route('/api/chat/stream', methods=['POST'])
def chat_stream():
    """Stream chat answer chunks through Server-Sent Events."""
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Question is required"}), 400

    return create_chat_stream_response(data['question'])

@app.route('/api/images', methods=['GET'])
def get_images():
    """Retrieve full image database snapshot."""
    pdf_filename = request.args.get('pdf_filename')
    manager = ImageReviewManager()
    try:
        snapshot = manager.get_db_snapshot(pdf_filename=pdf_filename)
        return jsonify(snapshot), 200
    except Exception as e:
        logger.error(f"Error fetching images: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/images', methods=['PUT', 'POST'])
def update_images():
    """Replace image database from a JSON array payload."""
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({"error": "Payload must be a JSON array"}), 400
        
    reviewed_by = request.args.get('reviewed_by', 'react-frontend')
    manager = ImageReviewManager()
    
    try:
        summary = manager.replace_image_db_from_payload(payload=data, reviewed_by=reviewed_by)
        return jsonify(summary), 200
    except Exception as e:
        logger.error(f"Error replacing image db: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/images/<path:filename>')
def serve_image(filename):
    """Serve static images from the database."""
    return send_from_directory(str(IMAGES_DIR), filename)



# BIORAG_IMAGE_QA_API
def _biorag_extract_message_text(response):
    """Chuẩn hóa nội dung trả về từ các phiên bản langchain-google-genai."""
    content = getattr(response, "content", response)
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and item.get("text"):
                parts.append(str(item["text"]))
        return "\n".join(parts).strip()
    return str(content).strip()


_BIORAG_QUIZ_CHUNKS = None
_BIORAG_CHAT_CHUNKS = None
_BIORAG_CHAT_CACHE = {}


def _biorag_normalize_search_text(value):
    """Chuẩn hóa tên sách và bằng chứng để so khớp ổn định trên dữ liệu OCR."""
    import re
    import unicodedata

    normalized = unicodedata.normalize("NFKD", str(value or "").lower())
    normalized = "".join(character for character in normalized if not unicodedata.combining(character))
    normalized = normalized.replace("đ", "d")
    return re.sub(r"[^a-z0-9]+", " ", normalized).strip()


def _biorag_extract_grade_from_text(value):
    """Đọc khối lớp 6-9 từ các biến thể tên tệp SGK KNTT."""
    import re

    normalized = _biorag_normalize_search_text(value)
    for pattern in (
        r"\bkhtn\s*([6789])\b",
        r"\bkhoa hoc tu nhien\s*([6789])\b",
        r"\blop\s*([6789])\b",
    ):
        match = re.search(pattern, normalized)
        if match:
            return int(match.group(1))
    return None


def _biorag_quiz_source_values(item):
    """Lấy các trường có thể chứa tên hoặc đường dẫn PDF từ chunk."""
    if not isinstance(item, dict):
        return []
    metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
    source_keys = (
        "pdf_filename", "source", "file_name", "filename", "pdf_path",
        "file_path", "path", "document_source", "book", "book_name",
    )
    values = []
    for container in (metadata, item):
        for key in source_keys:
            value = container.get(key)
            if isinstance(value, str) and value.strip() and value.strip() not in values:
                values.append(value.strip())
    return values


def _biorag_quiz_chunk_grade(item):
    """Xác định lớp của chunk chỉ từ metadata nguồn, không đoán từ nội dung bài."""
    for value in _biorag_quiz_source_values(item):
        grade = _biorag_extract_grade_from_text(value)
        if grade is not None:
            return grade
    return None


def _biorag_quiz_chunk_fields(item):
    """Chuẩn hóa một đoạn kiến thức từ book_rag thành văn bản và nguồn."""
    if not isinstance(item, dict):
        return str(item or "").strip(), "Sách KNTT", "?"

    metadata = item.get("metadata") if isinstance(item.get("metadata"), dict) else {}
    text = str(
        item.get("text")
        or item.get("page_content")
        or item.get("document")
        or ""
    ).strip()
    source_values = _biorag_quiz_source_values(item)
    source = next(
        (value for value in source_values if _biorag_extract_grade_from_text(value) is not None),
        source_values[0] if source_values else "Sách KNTT",
    )
    page = (
        metadata.get("page_number")
        or metadata.get("page")
        or item.get("page_number")
        or item.get("page")
        or "?"
    )
    return text, source, page


def _biorag_split_chat_question(question):
    """Tách câu hỏi nhiều ý nhưng không phá các câu hỏi đơn giản có dấu phẩy."""
    import re

    question = re.sub(r"[ \t]+", " ", str(question or "")).strip()
    if not question:
        return []

    parts = [
        part.strip(" -•\t")
        for part in re.split(r"(?:\s*;\s*|\s*\n+\s*|(?<=[?!])\s+)", question)
        if len(part.strip(" -•\t")) >= 3
    ]
    if len(parts) == 1 and ":" in question:
        prefix, tail = question.split(":", 1)
        repeated_requests = re.split(
            r",\s*(?=(?:minh\s*họa|minh\s*hoạ|hình\s*ảnh|tìm\s*hình|"
            r"giải\s*thích|nêu|cho\s*biết)\b)",
            tail,
            flags=re.IGNORECASE,
        )
        repeated_requests = [part.strip() for part in repeated_requests if len(part.strip()) >= 3]
        if len(repeated_requests) > 1:
            short_prefix = prefix.strip()
            parts = [
                f"{short_prefix}: {part}" if short_prefix and len(short_prefix) <= 70 else part
                for part in repeated_requests
            ]
    return parts[:5] or [question]


def _biorag_chat_grade(question, requested_grade=None):
    """Ưu tiên lớp người dùng chọn, sau đó mới suy ra từ nội dung câu hỏi."""
    if requested_grade not in (None, "", "auto"):
        try:
            grade = int(requested_grade)
        except (TypeError, ValueError):
            raise ValueError("Khối lớp không hợp lệ.")
        if grade not in {6, 7, 8, 9}:
            raise ValueError("Chỉ hỗ trợ Khoa học tự nhiên lớp 6 đến lớp 9.")
        return grade
    return _biorag_extract_grade_from_text(question)


def _biorag_is_image_request(question):
    normalized = _biorag_normalize_search_text(question)
    return any(marker in normalized for marker in (
        "hinh minh hoa", "minh hoa", "tim hinh", "cho hinh", "hinh anh", "hinh ve",
    ))


def _biorag_chat_history(data, limit=8):
    """Chỉ nhận một đoạn lịch sử ngắn do chính trình duyệt gửi lên."""
    rows = data.get("history") if isinstance(data, dict) else []
    if not isinstance(rows, list):
        return []
    history = []
    for row in rows[-limit:]:
        if not isinstance(row, dict) or row.get("role") not in {"user", "assistant"}:
            continue
        content = re.sub(r"[ \t]+", " ", str(row.get("content") or "")).strip()
        if content:
            item = {"role": row["role"], "content": content[:1800]}
            if isinstance(row.get("meta"), dict):
                item["meta"] = {
                    key: row["meta"].get(key)
                    for key in ("grade", "lesson_id") if row["meta"].get(key) is not None
                }
            if isinstance(row.get("sources"), list):
                item["sources"] = [
                    {key: source.get(key) for key in ("source", "page")}
                    for source in row["sources"][-6:] if isinstance(source, dict)
                ]
            history.append(item)
    return history


def _biorag_contextual_chat_query(question, history):
    """Gắn lại chủ đề cho các câu nối tiếp trong cùng một phiên hội thoại."""
    normalized = _biorag_normalize_search_text(question)
    words = normalized.split()

    # Tìm câu hỏi người dùng gần nhất
    user_turns = [
        row.get("content", "").strip()
        for row in history
        if isinstance(row, dict) and row.get("role") == "user" and row.get("content")
    ]
    if not user_turns:
        return question, False

    previous_user = user_turns[-1]

    # Các từ/cụm từ báo hiệu câu hỏi nối tiếp / phụ thuộc ngữ cảnh.
    # LƯU Ý: chỉ giữ những cụm THỰC SỰ chỉ về điều đã nói trước đó (chiếu hồi).
    # KHÔNG đưa vào đây các mẫu câu hỏi thông thường như "vai trò", "thế nào",
    # "tại sao", "khái niệm", "cấu tạo"... vì chúng xuất hiện tự nhiên trong rất
    # nhiều câu hỏi ĐỘC LẬP có chủ đề riêng (vd: "Quang hợp có vai trò như thế
    # nào?") — coi chúng là dấu hiệu nối tiếp từng khiến hệ thống ghép nhầm chủ
    # đề của câu hỏi trước đó (vd: từ trường) vào câu hỏi hoàn toàn khác chủ đề.
    followup_markers = (
        "cho hinh", "hinh minh hoa", "minh hoa", "anh minh hoa", "so do", "hinh anh",
        "giai thich them", "noi ro hon", "chi tiet hon", "y thu", "cau tren",
        "dieu do", "hien tuong nay", "qua trinh nay", "bo phan nay", "loai nay",
        "con gi nua", "ke them", "so sanh", "phan biet",
    )
    pronoun_markers = {"no", "chung", "do", "nay", "tren", "duoi", "kia", "vay"}

    is_image = _biorag_is_image_request(question)
    has_pronoun = bool(set(words) & pronoun_markers)
    has_followup_marker = any(marker in normalized for marker in followup_markers)
    # Câu hỏi cực ngắn (≤3 từ, vd: "Ví dụ?", "Tại sao?", "Ở đâu?") thường không
    # tự mang chủ đề nên mới cần dựa vào ngữ cảnh trước đó. Ngưỡng cũ (≤10 từ)
    # bắt luôn cả các câu hỏi đầy đủ, độc lập — đây là nguyên nhân chính gây
    # lẫn chủ đề, nên hạ xuống 3.
    is_short = len(words) <= 3

    is_followup = is_image or has_pronoun or has_followup_marker or is_short

    if not is_followup:
        return question, False

    if is_image:
        return previous_user, True

    clean_prev = re.sub(
        r"^(?:cho tôi|cho mình|hãy|em muốn hỏi|bạn ơi|xin hỏi)\s+",
        "",
        previous_user,
        flags=re.IGNORECASE,
    ).strip()
    prev_topic = clean_prev.split("?")[0].split(".")[0].strip()
    if len(prev_topic.split()) > 10:
        prev_topic = " ".join(prev_topic.split()[:10])

    combined_query = f"{prev_topic} {question}"
    return combined_query, True


def _biorag_history_grade(history):
    """Kế thừa khối lớp từ câu trả lời gần nhất khi người dùng đang hỏi nối tiếp."""
    for row in reversed(history):
        meta = row.get("meta") if isinstance(row.get("meta"), dict) else {}
        try:
            grade = int(meta.get("grade"))
        except (TypeError, ValueError):
            grade = None
        if grade in {6, 7, 8, 9}:
            return grade
        for source in row.get("sources") or []:
            grade = _biorag_extract_grade_from_text(source.get("source"))
            if grade in {6, 7, 8, 9}:
                return grade
    return None


def _biorag_chat_document_grade(document):
    metadata = getattr(document, "metadata", {}) or {}
    for key in ("pdf_filename", "source", "image_path", "file_name", "path"):
        grade = _biorag_extract_grade_from_text(metadata.get(key, ""))
        if grade is not None:
            return grade
    return None


def _biorag_chat_gallery_item(document, matched_query):
    metadata = dict(getattr(document, "metadata", {}) or {})
    image_path = str(metadata.get("image_path", "")).strip()
    if not image_path:
        return None
    page = metadata.get("page_number", metadata.get("page", "?"))
    source = metadata.get("pdf_filename") or metadata.get("source") or "Sách KNTT"
    caption = (
        metadata.get("figure_caption")
        or metadata.get("figure_label")
        or metadata.get("caption")
        or metadata.get("context_text")
        or getattr(document, "page_content", "")
        or "Hình minh họa"
    )
    caption = " ".join(str(caption).split())
    metadata["matched_query"] = matched_query
    return {
        "image_path": image_path,
        "label": f"{caption[:150]}{'…' if len(caption) > 150 else ''} (Trang {page}, {source})",
        "metadata": metadata,
    }


def _biorag_retrieve_chat_images(subqueries, grade, limit=6, allowed_context=None):
    """Tìm ảnh và khóa chúng vào đúng các trang đang dùng để trả lời."""
    try:
        services = AppServices.get_instance()
    except Exception as exc:
        logger.warning("Chat image services unavailable: %s", exc)
        return []

    allowed_pairs = set()
    for row in allowed_context or []:
        page = _biorag_lesson_page_number(row.get("page"))
        source = _biorag_lesson_book_key(row.get("source"))
        if page is not None and source:
            allowed_pairs.add((source, page))

    images = []
    seen = set()
    for subquery in subqueries:
        try:
            result = services.hybrid_retriever.search(subquery, text_k=4)
            documents = getattr(result, "image_docs", []) or []
        except Exception as exc:
            logger.warning("Chat image retrieval failed for %s: %s", subquery, exc)
            continue
        for document in documents:
            if grade is not None and _biorag_chat_document_grade(document) != grade:
                continue
            metadata = dict(getattr(document, "metadata", {}) or {})
            page = _biorag_lesson_page_number(
                metadata.get("page_number", metadata.get("page"))
            )
            source = _biorag_lesson_book_key(
                metadata.get("pdf_filename") or metadata.get("source")
            )
            if allowed_pairs and (source, page) not in allowed_pairs:
                continue
            item = _biorag_chat_gallery_item(document, subquery)
            if not item:
                continue
            key = item["image_path"].replace("\\", "/").lower()
            if key in seen:
                continue
            seen.add(key)
            images.append(item)
            if len(images) >= limit:
                return images
    return images


def _biorag_textbook_page_gallery(context, matched_query, limit=2):
    """Dùng trang SGK làm minh họa khi kho ảnh không có hình tách riêng."""
    output = []
    seen = set()
    for row in context:
        source = str(row.get("source") or "").strip()
        page = _biorag_lesson_page_number(row.get("page"))
        key = (_biorag_lesson_book_key(source), page)
        if not source or page is None or key in seen:
            continue
        try:
            pdf_path = _biorag_resolve_textbook_pdf(source)
        except FileNotFoundError:
            continue
        seen.add(key)
        page_row = _biorag_resolved_textbook_page_row(pdf_path, page)
        printed = ""
        if page_row.get("printed_start"):
            printed = f" / trang in {page_row['printed_start']}"
            if page_row.get("printed_end") != page_row.get("printed_start"):
                printed += f"–{page_row['printed_end']}"
        output.append({
            "image_url": (
                "/api/learning/textbook-page?source="
                + quote(pdf_path.name, safe="") + f"&page={page}"
            ),
            "label": f"Trang SGK minh họa · PDF {page}{printed} · {pdf_path.name}",
            "metadata": {
                "pdf_filename": pdf_path.name,
                "page_number": page,
                "printed_start": page_row.get("printed_start"),
                "printed_end": page_row.get("printed_end"),
                "matched_query": matched_query,
                "textbook_page_fallback": True,
            },
        })
        if len(output) >= int(limit):
            break
    return output


def _biorag_lesson_book_key(value):
    """Chuẩn hóa tên SGK để ảnh không bị lấy nhầm sách hoặc nhầm lớp."""
    normalized = _biorag_normalize_search_text(value)
    normalized = re.sub(r"\bkhtn([6789])\b", r"khtn \1", normalized)
    return re.sub(r"\bpdf\b", "", normalized).strip()


def _biorag_lesson_image_candidate(document, matched_query, grade, source_names, source_pages):
    """Chuyển một kết quả ảnh thành dữ liệu bài học sau khi khóa sách và trang."""
    if grade is not None and _biorag_chat_document_grade(document) != grade:
        return None
    metadata = dict(getattr(document, "metadata", {}) or {})
    page = _biorag_lesson_page_number(
        metadata.get("page_number", metadata.get("page"))
    )
    if page is None or page not in source_pages:
        return None
    image_source = metadata.get("pdf_filename") or metadata.get("source") or ""
    image_book = _biorag_lesson_book_key(image_source)
    if source_names and not any(
        image_book == source_name
        or (image_book and source_name and image_book in source_name)
        or (image_book and source_name and source_name in image_book)
        for source_name in source_names
    ):
        return None
    item = _biorag_chat_gallery_item(document, matched_query)
    if not item:
        return None
    caption = (
        metadata.get("figure_caption")
        or metadata.get("figure_label")
        or metadata.get("caption")
        or metadata.get("context_text")
        or getattr(document, "page_content", "")
        or "Hình minh họa trong SGK"
    )
    caption = " ".join(str(caption).split())[:420]
    try:
        image_path = "/".join(_biorag_relative_image_path(item["image_path"]))
    except (ValueError, PermissionError):
        image_path = str(item["image_path"]).replace("\\", "/")
    return {
        "image_path": image_path,
        "caption": caption or "Hình minh họa trong SGK",
        "label": item["label"],
        "page": page,
        "source": str(image_source or "SGK KNTT")[:220],
        "matched_query": str(matched_query or "")[:240],
    }


def _biorag_retrieve_lesson_images(topic, grade, lesson, sources, limit=4):
    """Chọn ảnh minh họa đúng sách, đúng lớp và đúng cụm trang của bài."""
    source_pages = {
        page
        for page in (_biorag_lesson_page_number(item.get("page")) for item in sources)
        if page is not None
    }
    source_names = {
        _biorag_lesson_book_key(item.get("source"))
        for item in sources
        if _biorag_lesson_book_key(item.get("source"))
    }
    if not source_pages:
        return []

    sections = lesson.get("sections") if isinstance(lesson, dict) else []
    queries = []
    for section in sections if isinstance(sections, list) else []:
        if isinstance(section, dict):
            section_title = _biorag_lesson_text(section.get("title"), 240)
            if section_title:
                queries.append(section_title)
    topic_text = _biorag_lesson_text(topic, 240)
    if topic_text:
        queries.append(topic_text)
    queries = list(dict.fromkeys(queries))[:5]

    try:
        services = AppServices.get_instance()
    except Exception as exc:
        logger.warning("Lesson image services unavailable: %s", exc)
        return []

    images = []
    seen = set()
    for matched_query in queries:
        try:
            result = services.hybrid_retriever.search(
                matched_query, text_k=2, image_k=max(8, int(limit) * 3)
            )
            documents = getattr(result, "image_docs", []) or []
        except Exception as exc:
            logger.warning("Lesson image retrieval failed for %s: %s", matched_query, exc)
            continue
        for document in documents:
            item = _biorag_lesson_image_candidate(
                document, matched_query, grade, source_names, source_pages
            )
            if not item:
                continue
            key = item["image_path"].replace("\\", "/").lower()
            if key in seen:
                continue
            seen.add(key)
            images.append(item)
            # Mỗi truy vấn phần kiến thức lấy một ảnh trước, giúp bộ ảnh đa dạng.
            break
        if len(images) >= int(limit):
            break
    logger.info(
        "Lesson illustrations selected: grade=%s topic=%s pages=%s count=%s",
        grade, topic, sorted(source_pages), len(images),
    )
    return images


def _biorag_chat_tokens(value):
    stopwords = {
        "cua", "cho", "trong", "nhung", "nhieu", "the", "nao", "mot", "cac", "voi",
        "hay", "gi", "la", "ve", "tu", "den", "minh", "hoa", "hinh", "anh", "tim",
        "khoa", "hoc", "tu", "nhien", "lop", "sach", "giao", "kntt",
    }
    return {
        token for token in _biorag_normalize_search_text(value).split()
        if len(token) >= 2 and token not in stopwords
    }


def _biorag_rank_chat_chunks(query, candidates, limit=5):
    """Xếp hạng dựa trên từ khóa nội dung, giảm trọng số các từ chung như 'hình'."""
    query_normalized = _biorag_normalize_search_text(query)
    query_tokens = _biorag_chat_tokens(query)
    if not query_tokens:
        return []
    query_words = query_normalized.split()
    bigrams = {" ".join(query_words[index:index + 2]) for index in range(len(query_words) - 1)}
    ranked = []
    for item in candidates:
        text, _source, _page = _biorag_quiz_chunk_fields(item)
        normalized = _biorag_normalize_search_text(text)
        text_tokens = set(normalized.split())
        overlap = query_tokens & text_tokens
        if not overlap:
            continue
        score = len(overlap) * 6
        score += sum(4 for phrase in bigrams if len(phrase) >= 5 and phrase in normalized)
        score += min(5, sum(1 for token in query_tokens if token in normalized))
        ranked.append((score, len(text), item))
    ranked.sort(key=lambda entry: (entry[0], entry[1]), reverse=True)
    # Trả kèm điểm số (không chỉ item) để _biorag_scope_chat_chunks phân biệt
    # được lúc nào một đoạn ở SÁCH KHÁC vẫn đủ mạnh để giữ lại, thay vì loại
    # bỏ tuyệt đối chỉ vì không cùng sách với đoạn xếp hạng 1.
    return [(score, item) for score, _length, item in ranked[:limit]]


def _biorag_scope_chat_chunks(ranked_scored, limit=5):
    """Giữ các trang lân cận cùng sách với đoạn xếp hạng 1 (để có ngữ cảnh
    liền mạch), NHƯNG không loại bỏ tuyệt đối các đoạn ở sách/lớp khác nếu
    điểm số của chúng gần với đoạn xếp hạng 1 (trong 85%).

    Lý do: điểm xếp hạng chỉ dựa trên trùng từ khóa, nên với câu hỏi mà nhiều
    từ là từ chung chung ("có", "vai", "trò"...), một đoạn hoàn toàn khác chủ
    đề có thể tình cờ nhỉnh hơn đoạn thực sự đúng trọng tâm chỉ vài điểm (đã
    xác nhận bằng dữ liệu thật: câu hỏi "Quang hợp có vai trò như thế nào?"
    từng bị neo vào trang nói về Nguyên sinh vật — 53 điểm — trong khi trang
    đúng "Quang hợp ở thực vật" ở SGK khác chỉ thua 4 điểm — 49 — và bị loại
    hoàn toàn vì khác sách). Khi chênh lệch nhỏ như vậy, giữ lại cả hai để mô
    hình ngôn ngữ có đủ bằng chứng chọn đúng nguồn thay vì chỉ thấy 1 phía.
    """
    if not ranked_scored:
        return []
    anchor_score, anchor_item = ranked_scored[0]
    _anchor_text, anchor_source, anchor_page_raw = _biorag_quiz_chunk_fields(anchor_item)
    anchor_page = _biorag_lesson_page_number(anchor_page_raw)
    anchor_book = _biorag_lesson_book_key(anchor_source)
    score_floor = anchor_score * 0.85
    scoped = []
    for score, item in ranked_scored:
        _text, source, page_raw = _biorag_quiz_chunk_fields(item)
        page = _biorag_lesson_page_number(page_raw)
        same_book = _biorag_lesson_book_key(source) == anchor_book
        nearby = (
            anchor_page is None or page is None
            or (anchor_page - 1 <= page <= anchor_page + 2)
        )
        strong_enough_elsewhere = score >= score_floor
        if (same_book and nearby) or strong_enough_elsewhere:
            scoped.append(item)
        if len(scoped) >= int(limit):
            break
    return scoped


_BIORAG_CHAT_TOPIC_ALIASES = {
    "tan sac anh sang": {
        "grade": 9, "lesson": 7, "source": "SGK KHTN 9 KNTT.pdf", "pages": [19, 20, 21]
    },
}


def _biorag_chat_lesson_scope(query, grade=None):
    """Ưu tiên bài học trong catalog; alias chỉ dùng cho tên hiện tượng khác tiêu đề bài."""
    normalized = _biorag_normalize_search_text(query)
    for phrase, scope in _BIORAG_CHAT_TOPIC_ALIASES.items():
        if phrase in normalized and (grade is None or int(scope["grade"]) == int(grade)):
            return dict(scope, method="curriculum_alias")

    query_tokens = _biorag_chat_tokens(query)
    if len(query_tokens) < 2:
        return None
    try:
        lessons = list_lessons(grade=grade, include_inactive=True)
    except Exception as exc:
        logger.warning("Chat lesson catalog unavailable: %s", exc)
        return None
    ranked = []
    # Số từ khóa "có nghĩa" của câu hỏi (đã bỏ stopword) — dùng để tính tỉ lệ
    # bao phủ, tránh khoá phạm vi chỉ vì trùng vài từ chung chung như
    # "có"/"vai"/"trò" với một bài học hoàn toàn khác chủ đề.
    query_token_count = max(len(query_tokens), 1)
    for lesson in lessons:
        if not isinstance(lesson, dict):
            continue
        fields = " ".join(str(lesson.get(key) or "") for key in (
            "title", "topic", "content", "number", "source_label"
        ))
        field_tokens = _biorag_chat_tokens(fields)
        overlap = query_tokens & field_tokens
        title = _biorag_normalize_search_text(lesson.get("title"))
        score = len(overlap) * 7
        if title and title in normalized:
            score += 20
        coverage = len(overlap) / query_token_count
        # Ngưỡng cũ (score >= 14, tương đương chỉ 2 từ trùng) quá dễ đạt và
        # từng khiến câu hỏi "Quang hợp có vai trò như thế nào?" bị khoá nhầm
        # vào bài "Từ trường" chỉ vì trùng vài từ phổ biến. Giờ đòi hỏi trùng
        # tối thiểu 4 từ VÀ bao phủ ít nhất 70% từ khóa của câu hỏi.
        if len(overlap) >= 4 and coverage >= 0.7:
            ranked.append((score, lesson))
    if not ranked:
        return None
    ranked.sort(key=lambda row: row[0], reverse=True)
    if len(ranked) > 1 and ranked[1][0] >= ranked[0][0] * 0.8:
        # Nhiều bài học cùng đạt điểm gần nhau — nhiều khả năng chỉ trùng từ
        # ngẫu nhiên chứ không thực sự khớp riêng 1 bài. Không chắc chắn thì
        # không khoá phạm vi, để hệ thống tìm kiếm rộng trên toàn sách thay vì
        # đoán liều một bài học cụ thể.
        return None
    lesson = ranked[0][1]
    try:
        resolved = _biorag_resolve_lesson_pdf_pages(lesson)
    except Exception as exc:
        logger.warning("Chat lesson page resolution failed for %s: %s", lesson.get("id"), exc)
        resolved = None
    if not resolved:
        return None
    return {
        "grade": int(lesson.get("grade")),
        "lesson": _biorag_lesson_number(lesson),
        "lesson_id": lesson.get("id"),
        "source": resolved["source"],
        "pages": list(resolved["pages"]),
        "method": "learning_catalog",
    }


def _biorag_chunk_in_lesson_scope(item, scope):
    if not scope:
        return True
    _text, source, page_raw = _biorag_quiz_chunk_fields(item)
    page = _biorag_lesson_page_number(page_raw)
    return (
        page in set(scope.get("pages") or [])
        and _biorag_lesson_book_key(source) == _biorag_lesson_book_key(scope.get("source"))
    )


def _biorag_load_chat_context(subqueries, grade, lesson_scope=None):
    """Đọc các đoạn SGK liên quan và giữ từng ý trong một cụm trang liền nhau."""
    global _BIORAG_CHAT_CHUNKS
    from src.rag.book_rag import load_all_chunks

    if _BIORAG_CHAT_CHUNKS is None:
        _BIORAG_CHAT_CHUNKS = load_all_chunks()
    chunks = _BIORAG_CHAT_CHUNKS
    if not isinstance(chunks, list) or not chunks:
        raise RuntimeError("Cơ sở dữ liệu SGK chưa có đoạn kiến thức.")

    candidates = chunks
    if grade is not None:
        candidates = [item for item in chunks if _biorag_quiz_chunk_grade(item) == grade]
        if not candidates:
            raise LookupError(f"Không tìm thấy dữ liệu SGK KNTT lớp {grade}.")

    scoped_candidates = None
    if lesson_scope:
        scoped_candidates = [
            item for item in candidates if _biorag_chunk_in_lesson_scope(item, lesson_scope)
        ]
        if not scoped_candidates:
            logger.warning("No chat chunks inside verified lesson scope: %s", lesson_scope)
            # Không có đoạn nào rơi vào phạm vi trang đã xác định — nhiều khả
            # năng việc xác định trang PDF cho bài học bị sai (VD: OCR nhận
            # nhầm trang), chứ không hẳn SGK thiếu dữ liệu. Bỏ khoá phạm vi và
            # tìm trên toàn bộ dữ liệu thay vì trả về rỗng.
            scoped_candidates = None

    selected = []
    seen = set()
    for subquery in subqueries:
        pool = scoped_candidates if scoped_candidates else candidates
        ranked = _biorag_rank_chat_chunks(subquery, pool, limit=18)
        # Bảo hiểm thứ hai: đã khoá phạm vi bài học nhưng KHÔNG một đoạn nào
        # trong đó trùng dù chỉ một từ khóa nội dung với câu hỏi — dấu hiệu
        # phạm vi trang bị xác định sai. Thử lại trên toàn bộ dữ liệu (không
        # khoá phạm vi) thay vì bỏ qua subquery này.
        if lesson_scope and pool is scoped_candidates and not ranked:
            ranked = _biorag_rank_chat_chunks(subquery, candidates, limit=18)
        if not ranked:
            continue
        scoped = _biorag_scope_chat_chunks(ranked, limit=5)
        for item in scoped:
            text, source, page = _biorag_quiz_chunk_fields(item)
            if len(text) < 40:
                continue
            key = (str(source).lower(), str(page), _biorag_normalize_search_text(text[:240]))
            if key in seen:
                continue
            seen.add(key)
            selected.append({"text": text[:2200], "source": source, "page": page})
            if len(selected) >= 12:
                return selected
    return selected


def _biorag_chat_sources(context):
    sources = []
    seen = set()
    for item in context:
        key = (str(item["source"]), str(item["page"]))
        if key in seen:
            continue
        seen.add(key)
        source = str(item["source"])
        page = item["page"]
        row = {"source": source, "page": page, "pdf_page": page}
        try:
            pdf_path = _biorag_resolve_textbook_pdf(source)
            page_number = _biorag_lesson_page_number(page)
            if page_number is not None:
                printed = _biorag_printed_pages_for_pdf_page(pdf_path, page_number)
                if printed:
                    row["printed_start"] = printed[0]
                    row["printed_end"] = printed[1]
        except (FileNotFoundError, ValueError, TypeError):
            pass
        sources.append(row)
    return sources


def _biorag_chat_cache_key(question, grade, contextual_query=""):
    return (
        f"{grade or 'auto'}::{_biorag_normalize_search_text(question)}::"
        f"{_biorag_normalize_search_text(contextual_query)}"
    )


def _biorag_get_cached_chat(key):
    import time

    cached = _BIORAG_CHAT_CACHE.get(key)
    if not cached or time.time() - cached["time"] > 20:
        return None
    payload = dict(cached["payload"])
    payload["meta"] = dict(payload.get("meta") or {}, duplicate_prevented=True)
    return payload


def _biorag_store_cached_chat(key, payload):
    import time

    now = time.time()
    for old_key, entry in list(_BIORAG_CHAT_CACHE.items()):
        if now - entry["time"] > 60:
            _BIORAG_CHAT_CACHE.pop(old_key, None)
    _BIORAG_CHAT_CACHE[key] = {"time": now, "payload": payload}


def _biorag_static_image_answer(subqueries, images, grade):
    scope = f" lớp {grade}" if grade else ""
    if not images:
        return f"Mình chưa tìm thấy hình minh họa phù hợp trong SGK KNTT{scope}."
    if len(subqueries) == 1:
        return f"Mình đã tìm thấy {len(images)} hình minh họa phù hợp trong SGK KNTT{scope}."
    lines = [f"Mình đã tách yêu cầu thành {len(subqueries)} ý và tìm thấy {len(images)} hình minh họa trong SGK KNTT{scope}:"]
    for index, subquery in enumerate(subqueries, start=1):
        count = sum(1 for image in images if image.get("metadata", {}).get("matched_query") == subquery)
        lines.append(f"- **Ý {index}:** {count} hình phù hợp — {subquery}")
    return "\n".join(lines)


def _biorag_clean_vietnamese_answer(value):
    """Sửa các lỗi dính từ thường gặp và loại bỏ triệt để các câu máy móc/tiền tố không mong muốn."""
    answer = str(value or "").strip()
    replacements = {
        "thựcvật": "thực vật", "độngvật": "động vật", "conngười": "con người",
        "sinhsản": "sinh sản", "sinhtrưởng": "sinh trưởng", "pháttriển": "phát triển",
        "hôhấp": "hô hấp", "bàitiết": "bài tiết", "quanghợp": "quang hợp",
        "tếbào": "tế bào", "ánhsáng": "ánh sáng", "nănglượng": "năng lượng",
    }
    for fused, separated in replacements.items():
        answer = re.sub(rf"\b{fused}\b", separated, answer, flags=re.IGNORECASE)

    # Loại bỏ các dòng tiền tố mang tính thông báo kỹ thuật/kiểm duyệt
    lines = answer.split("\n")
    cleaned_lines = []
    skipping_header = True
    for line in lines:
        stripped = line.strip()
        if skipping_header:
            lowered = stripped.lower()
            unwanted_signals = (
                "bản nháp", "bản thảo", "ngữ liệu", "kiểm chứng", "hiệu chỉnh",
                "trích xuất trực tiếp", "câu trả lời sau khi", "dưới đây là nội dung",
                "không phù hợp với nội dung", "chưa phù hợp với",
                "dựa trên ngữ liệu", "tôi xin trả lời", "theo ngữ liệu",
                "sau đây là câu trả lời", "trả lời câu hỏi của bạn như sau",
            )
            if any(signal in lowered for signal in unwanted_signals) and len(stripped) < 300:
                continue
            if not stripped:
                continue
            skipping_header = False
        cleaned_lines.append(line)

    answer = "\n".join(cleaned_lines).strip()
    # Loại bỏ đoạn văn bản thừa nếu AI tự thêm phần 'Hình minh họa: Ngữ liệu SGK... không cung cấp'
    answer = re.sub(
        r"(?:\n|^)(?:#{1,3}\s*)?(?:\*\*)?(?:Hình minh họa|Minh họa|Hình ảnh)(?:\*\*)?:?\s*\n(?:(?!\n#{1,3}|\n\*\*).)*?(?:không cung cấp hình ảnh|chỉ có chú thích|không có hình minh họa|chưa có hình cụ thể)[^\n]*",
        "",
        answer,
        flags=re.IGNORECASE | re.DOTALL,
    )
    answer = re.sub(r"[ \t]{2,}", " ", answer)
    return answer.strip()


def _biorag_image_sources(images):
    sources = []
    seen = set()
    for image in images:
        metadata = image.get("metadata") if isinstance(image.get("metadata"), dict) else {}
        source = metadata.get("pdf_filename") or metadata.get("source") or "Sách KNTT"
        page = metadata.get("page_number", metadata.get("page", "?"))
        key = (str(source), str(page))
        if key in seen:
            continue
        seen.add(key)
        sources.append({"source": source, "page": page})
    return sources


@app.route('/api/chat/grounded', methods=['POST'])
def biorag_grounded_chat():
    """Trò chuyện có ngữ cảnh; câu trả lời, nguồn và ảnh dùng chung một cụm trang."""
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()
    history = _biorag_chat_history(data)
    payload, status = _biorag_answer_grounded_question(question, data.get("grade"), history)
    return jsonify(payload), status


def _biorag_answer_grounded_question(question, requested_grade, history):
    """Lõi trả lời có ngữ cảnh + trích dẫn SGK KNTT.

    Dùng chung cho chat gõ tay (/api/chat/grounded) và chat hỏi bằng ảnh chụp
    (/api/chat/photo) — tách ra từ biorag_grounded_chat để cả hai lối vào luôn
    trả lời nhất quán, cùng một pipeline truy xuất/kiểm chứng. Trả về
    (payload_dict, http_status), không tự gọi jsonify() để nơi gọi tự quyết định.
    """
    question = str(question or "").strip()
    if not question:
        return {"error": "Câu hỏi không được để trống."}, 400
    if len(question) > 3000:
        return {"error": "Câu hỏi vượt quá giới hạn 3.000 ký tự."}, 413

    try:
        grade = _biorag_chat_grade(question, requested_grade)
    except ValueError as exc:
        return {"error": str(exc)}, 400
    contextual_query, contextualized = _biorag_contextual_chat_query(question, history)
    if contextualized and grade is None:
        grade = _biorag_history_grade(history)
    lesson_scope = _biorag_chat_lesson_scope(contextual_query, grade)
    if lesson_scope and grade is None:
        grade = lesson_scope.get("grade")
    subqueries = _biorag_split_chat_question(question)
    retrieval_subqueries = _biorag_split_chat_question(contextual_query)
    cache_key = _biorag_chat_cache_key(question, grade, contextual_query)
    cached = _biorag_get_cached_chat(cache_key)
    if cached is not None:
        return cached, 200

    image_only = all(_biorag_is_image_request(subquery) for subquery in subqueries)
    common_meta = {
        "grounded": True,
        "grade": grade,
        "subqueries": subqueries,
        "image_only": image_only,
        "contextualized": contextualized,
        "lesson_id": lesson_scope.get("lesson_id") if lesson_scope else None,
        "lesson_scope": lesson_scope.get("method") if lesson_scope else None,
    }

    try:
        context = _biorag_load_chat_context(
            retrieval_subqueries, grade, lesson_scope=lesson_scope
        )
    except LookupError as exc:
        return {"error": str(exc)}, 404
    except Exception as exc:
        logger.error("Grounded chat retrieval failed: %s", exc, exc_info=True)
        return {"error": "Chưa đọc được dữ liệu SGK KNTT."}, 500

    if not context:
        payload = {
            "answer": "Thông tin này không được đề cập rõ trong các đoạn SGK đã truy xuất.",
            "images": [],
            "sources": [],
            "meta": common_meta,
        }
        _biorag_store_cached_chat(cache_key, payload)
        return payload, 200

    images = _biorag_retrieve_chat_images(
        retrieval_subqueries, grade, allowed_context=context
    )
    if image_only and not images:
        images = _biorag_textbook_page_gallery(context, contextual_query, limit=2)
    if image_only:
        payload = {
            "answer": _biorag_static_image_answer(subqueries, images, grade),
            "images": images,
            "sources": _biorag_chat_sources(context),
            "meta": common_meta,
        }
        _biorag_store_cached_chat(cache_key, payload)
        return payload, 200

    recent_dialogue = []
    for row in history[-6:]:
        role = row.get("role")
        content = str(row.get("content") or "").strip()
        if not content:
            continue
        if role == "assistant":
            short = content[:250].replace("\n", " ") + ("..." if len(content) > 250 else "")
            recent_dialogue.append(f"- Trợ lý: {short}")
        elif role == "user":
            recent_dialogue.append(f"- Học sinh: {content[:150]}")
    dialogue_context = "\n".join(recent_dialogue) if recent_dialogue else "Phiên trò chuyện mới."

    context_blocks = [
        f"[S{index} | {item['source']} | trang {item['page']}]\n{item['text']}"
        for index, item in enumerate(context, start=1)
    ]
    questions_block = "\n".join(
        f"{index}. {subquery}" for index, subquery in enumerate(subqueries, start=1)
    )
    evidence_block = "\n\n".join(context_blocks)
    prompt = f"""Bạn là trợ lý Khoa học tự nhiên THCS thân thiện, chỉ được trả lời từ NGỮ LIỆU SGK.

[LỊCH SỬ TRAO ĐỔI TRONG PHIÊN NÀY]:
{dialogue_context}

[CÂU HỎI HIỆN TẠI]:
{questions_block}

[CHỦ ĐỀ ĐÃ KẾT NỐI TỪ PHIÊN]:
{contextual_query if contextualized else "Câu hỏi độc lập."}

[NGỮ LIỆU SGK ĐÃ TRUY XUẤT]:
{evidence_block}

QUY TẮC:
- Duy trì nội dung liền mạch, liên kết tự nhiên với những gì đã trao đổi trong phiên này.
- Nếu học sinh hỏi tiếp nối (dùng đại từ 'nó', 'chúng', 'quá trình này', 'ý trên', v.v.), hãy trả lời đúng trọng tâm về chủ đề đang thảo luận.
- Trả lời rõ ràng, sư phạm, phù hợp học sinh THCS (lớp 6-9).
- Mỗi khẳng định khoa học phải được một nguồn S hỗ trợ trực tiếp và ghi [Số] cuối câu (ví dụ [S1], [S2]).
- Khi câu hỏi yêu cầu thí nghiệm hoặc thực hành (ví dụ: 'làm thí nghiệm... như thế nào'): hãy trình bày mạch lạc theo các mục: Dụng cụ thí nghiệm, Các bước tiến hành (Bước 1, Bước 2...), Hiện tượng quan sát và Kết luận khoa học.
- Ký hiệu và công thức toán/lý/hóa viết theo chuẩn LaTeX (ví dụ: $i_1$, $r_1$, $i_2$, $r_2$, $v$, $t$, $s$,...).
- TUYỆT ĐỐI KHÔNG mở đầu bằng câu rập khuôn như 'Dựa trên ngữ liệu SGK...', 'Tôi xin trả lời...'. Trả lời thẳng vào nội dung.
- TUYỆT ĐỐI KHÔNG tự viết mục 'Hình minh họa' hay bình luận về việc có hay không có hình ảnh (hệ thống sẽ tự động đính kèm trang SGK/hình minh họa bên dưới câu trả lời).
- Không ghép nguyên nhân của hình này với mô tả của hình khác.
- Không suy luận quan hệ nhân quả khi nguồn chỉ nêu ví dụ hoặc chú thích hình.
- Nếu nguồn chưa đủ, nói rõ "SGK truy xuất chưa cung cấp đủ căn cứ".
- Không dùng kiến thức ngoài nguồn.
- Trả lời trực tiếp nội dung, không viết các câu bình luận hay câu dẫn dắt ngoài lề.
"""
    try:
        llm = AppServices.get_instance().llm
        draft = _biorag_extract_message_text(llm.invoke(prompt))
        if not draft:
            raise ValueError("Mô hình chưa tạo câu trả lời.")
        verify_prompt = f"""Bạn là bộ phận rà soát độ chính xác của câu trả lời theo NGỮ LIỆU SGK.
Nhiệm vụ: Chỉnh sửa câu trả lời dưới đây cho hoàn toàn bám sát ngữ liệu SGK. Xóa hoặc sửa mọi khẳng định không có nguồn hỗ trợ. Giữ cấu trúc dễ đọc và ký hiệu nguồn [Số].

YÊU CẦU BẮT BUỘC VỀ ĐẦU RA:
- CHỈ trả về đúng nội dung câu trả lời cuối cùng dành cho học sinh.
- TUYỆT ĐỐI KHÔNG viết lời bình luận, nhận xét hay câu dẫn dắt (TUYỆT ĐỐI KHÔNG viết các câu như 'Bản nháp hiện tại...', 'Dưới đây là...', 'Sau khi kiểm tra...').

NGỮ LIỆU SGK:
{evidence_block}

CÂU TRẢ LỜI CẦN RÀ SOÁT:
{draft}
"""
        try:
            verified = _biorag_extract_message_text(llm.invoke(verify_prompt))
            answer = verified or draft
        except Exception as verify_exc:
            logger.warning("Grounded answer verification failed: %s", verify_exc)
            answer = draft
    except Exception as exc:
        logger.error("Grounded chat generation failed: %s", exc, exc_info=True)
        return {"error": "Gemini chưa tạo được câu trả lời đã kiểm chứng."}, 500

    answer = _biorag_clean_vietnamese_answer(answer)
    if not images and context:
        images = _biorag_textbook_page_gallery(context, contextual_query, limit=2)
    payload = {
        "answer": answer,
        "images": images,
        "sources": _biorag_chat_sources(context),
        "meta": common_meta,
    }
    _biorag_store_cached_chat(cache_key, payload)
    return payload, 200


def _biorag_read_uploaded_photo(file_storage):
    """Đọc + chuẩn hoá ảnh học sinh tải lên (chụp đề bài/bài tập) qua Pillow.

    Khác _biorag_prepare_image_bytes (dùng cho ảnh đã có sẵn trên đĩa, nhận
    Path): hàm này nhận thẳng werkzeug FileStorage từ request.files, sửa xoay
    EXIF và ép về JPEG để Gemini luôn nhận đúng định dạng."""
    import io
    import mimetypes

    filename = str(getattr(file_storage, "filename", "") or "")
    mime_type = str(getattr(file_storage, "mimetype", "") or "") or (mimetypes.guess_type(filename)[0] or "")
    if not mime_type.startswith("image/"):
        raise ValueError("Tệp tải lên không phải hình ảnh.")

    raw = file_storage.read()
    if not raw:
        raise ValueError("Ảnh tải lên trống hoặc lỗi khi đọc.")
    if len(raw) > 8 * 1024 * 1024:
        raise ValueError("Ảnh vượt quá giới hạn 8MB.")

    from PIL import Image, ImageOps

    try:
        with Image.open(io.BytesIO(raw)) as source:
            source = ImageOps.exif_transpose(source)
            if source.width * source.height > 40_000_000:
                raise ValueError("Kích thước ảnh quá lớn để xử lý an toàn.")
            normalized = source.convert("RGB")
            output = io.BytesIO()
            normalized.save(output, format="JPEG", quality=90, optimize=True)
            return output.getvalue(), "image/jpeg"
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError("Không đọc được nội dung ảnh đã tải lên (tệp có thể bị hỏng).") from exc


def _biorag_extract_question_from_photo(image_bytes, mime_type):
    """Nhờ Gemini vision đọc nguyên văn câu hỏi/bài tập trong ảnh học sinh chụp.

    Đây CHỈ là bước OCR/diễn giải ảnh thành văn bản — không trả lời câu hỏi ở
    đây. Văn bản trích được sẽ đưa tiếp qua _biorag_answer_grounded_question,
    tức đúng pipeline RAG có trích dẫn SGK như chat gõ tay."""
    import base64

    from langchain_core.messages import HumanMessage

    prompt = (
        "Đây là ảnh chụp một câu hỏi/bài tập Khoa học tự nhiên THCS (có thể là đề in trong SGK, "
        "đề kiểm tra, hoặc chữ viết tay của học sinh). Hãy đọc và chép lại CHÍNH XÁC, ĐẦY ĐỦ nội "
        "dung câu hỏi/bài tập trong ảnh, giữ nguyên số liệu, đơn vị, ký hiệu. Nếu ảnh có nhiều câu "
        "hỏi, liệt kê từng câu trên một dòng riêng, đánh số 1. 2. 3. Nếu có phần chữ mờ/không đọc "
        "rõ, đánh dấu phần đó bằng [không rõ] thay vì đoán bừa.\n"
        "CHỈ trả về nguyên văn câu hỏi đã đọc được. TUYỆT ĐỐI KHÔNG trả lời câu hỏi, không giải "
        "thích, không thêm lời dẫn hay bình luận nào khác."
    )
    encoded = base64.b64encode(image_bytes).decode("ascii")
    message = HumanMessage(content=[
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": f"data:{mime_type};base64,{encoded}"},
    ])
    llm = AppServices.get_instance().llm
    raw_text = _biorag_extract_message_text(llm.invoke([message]))
    text = re.sub(r"\s+", " ", str(raw_text or "")).strip()
    text = re.sub(r'^(?:câu hỏi(?:\s+trong\s+ảnh)?\s*[:：]\s*)', "", text, flags=re.IGNORECASE).strip()
    return text[:3000]


@app.route('/api/chat/photo', methods=['POST'])
def biorag_chat_photo():
    """Học sinh tải ảnh chụp đề bài/bài tập; Gemini vision đọc thành câu hỏi rồi
    trả lời qua đúng pipeline RAG có trích dẫn SGK (không phải vision trả lời trực tiếp)."""
    from src.config import GEMINI_API_KEY
    if not GEMINI_API_KEY:
        return jsonify({"error": "Chưa cấu hình GEMINI_API_KEY cho tính năng chụp ảnh hỏi bài."}), 503

    image_file = request.files.get("image")
    if image_file is None or not str(getattr(image_file, "filename", "")).strip():
        return jsonify({"error": "Chưa chọn ảnh."}), 400
    try:
        grade = int(request.form.get("grade", 7))
    except (TypeError, ValueError):
        return jsonify({"error": "Khối lớp không hợp lệ."}), 400
    if grade not in {6, 7, 8, 9}:
        return jsonify({"error": "Chỉ hỗ trợ Khoa học tự nhiên lớp 6 đến lớp 9."}), 400

    try:
        image_bytes, mime_type = _biorag_read_uploaded_photo(image_file)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        logger.error("Photo question image read failed: %s", exc, exc_info=True)
        return jsonify({"error": "Không đọc được ảnh đã tải lên."}), 400

    try:
        extracted_question = _biorag_extract_question_from_photo(image_bytes, mime_type)
    except Exception as exc:
        logger.error("Photo OCR failed: %s", exc, exc_info=True)
        return jsonify({"error": "Chưa đọc được nội dung câu hỏi trong ảnh. Hãy thử lại."}), 502

    if not extracted_question:
        return jsonify({
            "error": "Không nhận ra được câu hỏi nào trong ảnh. Hãy chụp lại rõ nét hơn, đủ ánh sáng và ít góc nghiêng."
        }), 422

    payload, status = _biorag_answer_grounded_question(extracted_question, grade, [])
    if status == 200:
        payload["extracted_question"] = extracted_question
    return jsonify(payload), status


@app.route('/api/feedback', methods=['POST'])
def biorag_chat_feedback():
    """Ghi nhận đánh giá 👍/👎 của học sinh cho một câu trả lời.

    Dữ liệu này dùng để phát hiện những câu hỏi mà retrieval/relevance-gate
    đang trả lời kém, phục vụ việc tinh chỉnh RETRIEVER_MAX_K /
    RETRIEVER_DISTANCE_MARGIN dựa trên thực tế sử dụng thay vì đoán.
    """
    data = request.get_json(silent=True) or {}

    rating = str(data.get("rating", "")).strip().lower()
    if rating not in {"up", "down"}:
        return jsonify({"error": "Trường 'rating' phải là 'up' hoặc 'down'."}), 400

    question = str(data.get("question", "")).strip()[:3000]
    answer = str(data.get("answer", "")).strip()[:8000]
    if not question or not answer:
        return jsonify({"error": "Thiếu 'question' hoặc 'answer'."}), 400

    subqueries = data.get("subqueries")
    sources = data.get("sources")
    comment = str(data.get("comment", "")).strip()[:1000]

    entry = {
        "id": uuid.uuid4().hex,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "rating": rating,
        "question": question,
        "answer": answer,
        "grade": data.get("grade"),
        "subqueries": subqueries if isinstance(subqueries, list) else [],
        "sources": sources if isinstance(sources, list) else [],
        "lesson_id": data.get("lesson_id"),
        "comment": comment or None,
    }

    try:
        FEEDBACK_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with _FEEDBACK_LOCK:
            with open(FEEDBACK_LOG_PATH, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as exc:
        logger.error("Không ghi được feedback: %s", exc, exc_info=True)
        return jsonify({"error": "Không lưu được đánh giá, thử lại sau."}), 500

    return jsonify({"ok": True, "id": entry["id"]}), 200


@app.route('/api/feedback/summary', methods=['GET'])
def biorag_chat_feedback_summary():
    """Thống kê nhanh số lượt 👍/👎 đã ghi nhận (nền tảng cho dashboard chất lượng)."""
    if not FEEDBACK_LOG_PATH.exists():
        return jsonify({"total": 0, "up": 0, "down": 0, "up_rate": None}), 200

    up = down = 0
    try:
        with open(FEEDBACK_LOG_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get("rating") == "up":
                    up += 1
                elif row.get("rating") == "down":
                    down += 1
    except Exception as exc:
        logger.error("Không đọc được feedback log: %s", exc, exc_info=True)
        return jsonify({"error": "Không đọc được dữ liệu đánh giá."}), 500

    total = up + down
    return jsonify({
        "total": total,
        "up": up,
        "down": down,
        "up_rate": round(up / total, 4) if total else None,
    }), 200


# =========================================================================
# AUTHENTICATION & USER MANAGEMENT (GIÁO VIÊN & HỌC SINH)
# =========================================================================
AUTH_SECRET_KEY = os.environ.get("AUTH_SECRET_KEY") or "biorag_huynh_ba_chanh_khtn_2026_auth_secret"
TEACHER_PASSWORD = os.environ.get("TEACHER_PASSWORD", "khtn2026@hbc")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin2026@hbc")

DEFAULT_CLASSES = [
    {"grade": 6, "name": "6/1"}, {"grade": 6, "name": "6/2"}, {"grade": 6, "name": "6/3"}, {"grade": 6, "name": "6/4"}, {"grade": 6, "name": "6/5"},
    {"grade": 7, "name": "7/1"}, {"grade": 7, "name": "7/2"}, {"grade": 7, "name": "7/3"}, {"grade": 7, "name": "7/4"}, {"grade": 7, "name": "7/5"},
    {"grade": 8, "name": "8/1"}, {"grade": 8, "name": "8/2"}, {"grade": 8, "name": "8/3"}, {"grade": 8, "name": "8/4"}, {"grade": 8, "name": "8/5"},
    {"grade": 9, "name": "9/1"}, {"grade": 9, "name": "9/2"}, {"grade": 9, "name": "9/3"}, {"grade": 9, "name": "9/4"}, {"grade": 9, "name": "9/5"},
]

def generate_auth_token(payload: dict) -> str:
    """Generate tamper-proof HMAC-SHA256 stateless session token."""
    data = dict(payload)
    if "exp" not in data:
        data["exp"] = int(time.time()) + 30 * 86400  # 30 days
    raw_json = json.dumps(data, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    b64 = base64.urlsafe_b64encode(raw_json).decode('utf-8').rstrip('=')
    sig = hmac.new(AUTH_SECRET_KEY.encode('utf-8'), b64.encode('utf-8'), hashlib.sha256).hexdigest()
    return f"{b64}.{sig}"

def verify_auth_token(token: str):
    """Verify and decode token, returning user payload or None."""
    if not token or "." not in token:
        return None
    try:
        parts = token.split(".", 1)
        if len(parts) != 2:
            return None
        b64, sig = parts
        expected_sig = hmac.new(AUTH_SECRET_KEY.encode('utf-8'), b64.encode('utf-8'), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected_sig):
            return None
        padded = b64 + "=" * ((4 - len(b64) % 4) % 4)
        raw_json = base64.urlsafe_b64decode(padded.encode('utf-8'))
        payload = json.loads(raw_json.decode('utf-8'))
        if payload.get("exp") and time.time() > payload["exp"]:
            return None
        return payload
    except Exception:
        return None

def get_current_user_from_request():
    """Extract and verify user payload from Authorization header or request data."""
    auth_header = request.headers.get("Authorization", "").strip()
    token = None
    if auth_header.startswith("Bearer "):
        token = auth_header[7:].strip()
    elif not token:
        token = request.args.get("token") or request.form.get("token")
        if not token and request.is_json:
            token = (request.get_json(silent=True) or {}).get("token")
    if token:
        return verify_auth_token(token)
    return None

@app.route("/api/auth/login", methods=["POST", "OPTIONS"])
@app.route("/auth/login", methods=["POST", "OPTIONS"])
def api_auth_login():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"})
    data = request.get_json(silent=True) or request.form or {}
    role = str(data.get("role", "")).strip().lower()
    
    # Auto-detect role if not explicitly provided
    if not role:
        if data.get("password") or data.get("username"):
            role = "teacher"
        else:
            role = "student"

    if role in ["teacher", "admin"]:
        username = str(data.get("username", "")).strip() or "giaovien"
        password = str(data.get("password", "")).strip()
        is_admin = username.lower() in ["admin", "quantri"]

        valid = False
        if is_admin:
            if password in [ADMIN_PASSWORD, "admin2026@hbc", TEACHER_PASSWORD, "khtn2026@hbc"]:
                valid = True
        else:
            if password in [TEACHER_PASSWORD, "khtn2026@hbc", ADMIN_PASSWORD, "admin2026@hbc"]:
                valid = True

        if not valid:
            return jsonify({
                "success": False,
                "error": "Mật khẩu giáo viên không chính xác. Mặc định là: khtn2026@hbc"
            }), 401

        user_role = "admin" if is_admin else "teacher"
        full_name = str(data.get("full_name", "")).strip()
        display_name = full_name if full_name else ("Quản trị viên KHTN" if is_admin else "Thầy/Cô · Tổ KHTN")

        user_payload = {
            "id": f"gv_{hashlib.md5(username.lower().encode('utf-8')).hexdigest()[:8]}",
            "username": username,
            "name": display_name,
            "role": user_role,
            "school": "TRƯỜNG THCS HUỲNH BÁ CHÁNH",
            "permissions": ["teacher_mode", "edit_lessons", "generate_lessons", "export_5512", "export_3280", "view_sgv"]
        }
        token = generate_auth_token(user_payload)
        return jsonify({
            "success": True,
            "user": user_payload,
            "token": token,
            "message": f"Đăng nhập thành công với vai trò {'Quản trị viên' if is_admin else 'Giáo viên'}."
        })

    elif role == "student":
        full_name = str(data.get("full_name") or data.get("name") or "").strip()
        grade_class = str(data.get("grade_class") or data.get("class") or "").strip()
        student_code = str(data.get("student_code") or "").strip()

        if len(full_name) < 2:
            return jsonify({
                "success": False,
                "error": "Vui lòng nhập đầy đủ Họ và tên học sinh (tối thiểu 2 ký tự)."
            }), 400

        if not grade_class:
            return jsonify({
                "success": False,
                "error": "Vui lòng chọn hoặc nhập Lớp học (ví dụ: 6/1, 7/2, 8/3, 9/1)."
            }), 400

        user_id = f"hs_{int(time.time())}_{hashlib.md5(full_name.encode('utf-8')).hexdigest()[:6]}"
        user_payload = {
            "id": user_id,
            "name": full_name,
            "grade_class": grade_class,
            "student_code": student_code,
            "role": "student",
            "school": "TRƯỜNG THCS HUỲNH BÁ CHÁNH",
            "permissions": ["read_sgk", "chat_ai", "take_quiz", "view_history", "lab_3d"]
        }
        token = generate_auth_token(user_payload)
        return jsonify({
            "success": True,
            "user": user_payload,
            "token": token,
            "message": f"Chào mừng em {full_name} (Lớp {grade_class}) đến với BioRAG Huỳnh Bá Chánh!"
        })

    else:
        return jsonify({"success": False, "error": f"Vai trò '{role}' không hợp lệ."}), 400

@app.route("/api/auth/me", methods=["GET"])
@app.route("/auth/me", methods=["GET"])
def api_auth_me():
    user = get_current_user_from_request()
    if user:
        return jsonify({
            "authenticated": True,
            "user": user,
            "school": "TRƯỜNG THCS HUỲNH BÁ CHÁNH"
        })
    return jsonify({
        "authenticated": False,
        "user": None,
        "school": "TRƯỜNG THCS HUỲNH BÁ CHÁNH"
    })

@app.route("/api/auth/logout", methods=["POST", "OPTIONS"])
@app.route("/auth/logout", methods=["POST", "OPTIONS"])
def api_auth_logout():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"})
    return jsonify({"success": True, "message": "Đã đăng xuất thành công."})

@app.route("/api/auth/classes", methods=["GET"])
@app.route("/auth/classes", methods=["GET"])
def api_auth_classes():
    return jsonify({
        "grades": [6, 7, 8, 9],
        "classes": DEFAULT_CLASSES,
        "school": "TRƯỜNG THCS HUỲNH BÁ CHÁNH"
    })


def _biorag_load_quiz_context(grade, topic, count):
    """Tìm ngữ liệu đúng lớp và ưu tiên tuyệt đối phạm vi bài đã nhận diện."""
    import re

    global _BIORAG_QUIZ_CHUNKS
    from src.rag.book_rag import find_relevant_chunks, load_all_chunks

    if _BIORAG_QUIZ_CHUNKS is None:
        _BIORAG_QUIZ_CHUNKS = load_all_chunks()
    chunks = _BIORAG_QUIZ_CHUNKS
    if not isinstance(chunks, list) or not chunks:
        raise RuntimeError("Cơ sở dữ liệu SGK chưa có đoạn kiến thức.")

    grade_chunks = [item for item in chunks if _biorag_quiz_chunk_grade(item) == int(grade)]
    if not grade_chunks:
        raise LookupError(
            f"Không tìm thấy dữ liệu SGK KNTT lớp {grade}. "
            "Hãy kiểm tra metadata pdf_filename/source trong database_kntt."
        )

    is_random_composite = any(kw in str(topic).lower() for kw in [
        "ngẫu nhiên", "ngau nhien", "tổng hợp", "tong hop", "toàn bộ", "toan bo",
        "học kỳ", "hoc ky", "thi thử", "thi thu", "ôn tập cuối kỳ", "on tap cuoi ky", "random"
    ])
    if is_random_composite:
        grade_chunks_sorted = sorted(grade_chunks, key=lambda c: int(_biorag_quiz_chunk_fields(c)[2] or 0))
        target_sources = min(max(12, int(count) // 2), 20)
        step = max(1, len(grade_chunks_sorted) // target_sources)
        relevant = [grade_chunks_sorted[i] for i in range(0, len(grade_chunks_sorted), step)][:target_sources]
    else:
        lesson_scope = _biorag_chat_lesson_scope(topic, grade)
        candidates = grade_chunks
        if lesson_scope:
            candidates = [
                item for item in grade_chunks if _biorag_chunk_in_lesson_scope(item, lesson_scope)
            ]
            if not candidates:
                raise LookupError(
                    "Đã xác định đúng bài học nhưng database chưa có đoạn kiến thức trong cụm trang đó."
                )
        query = f"Khoa học tự nhiên lớp {grade}: {topic}"
        relevant = find_relevant_chunks(query, candidates, max(14, int(count) * 4))
        if not relevant:
            relevant = find_relevant_chunks(topic, candidates, max(14, int(count) * 4))

    sources = []
    context_size = 0
    for item in relevant:
        if _biorag_quiz_chunk_grade(item) != int(grade):
            continue
        text, source, page = _biorag_quiz_chunk_fields(item)
        if len(text) < 40:
            continue
        text = text[:2200]
        entry = {"text": text, "source": source, "page": page}
        projected = context_size + len(text)
        if projected > 18000 and sources:
            break
        sources.append(entry)
        context_size = projected
    if not sources:
        raise LookupError("Không tìm thấy nội dung SGK phù hợp với lớp và chủ đề đã chọn.")
    return sources


def _biorag_repair_quiz_evidence(item, sources):
    """Tìm lại một trích đoạn nguyên văn cho câu hợp lệ khi mô hình ghi sai source_id."""
    answer_index = item.get("answer_index")
    options = item.get("options") if isinstance(item.get("options"), list) else []
    if not isinstance(answer_index, int) or not 0 <= answer_index < len(options):
        return None
    answer_tokens = _biorag_chat_tokens(options[answer_index])
    query_tokens = _biorag_chat_tokens(
        f"{item.get('question', '')} {options[answer_index]}"
    )
    if not answer_tokens:
        return None

    best = None
    for source_index, source in enumerate(sources, start=1):
        text = str(source.get("text") or "")
        segments = [
            segment.strip(" -•\t")
            for segment in re.split(r"(?<=[.!?;:])\s+|\n+", text)
            if len(segment.split()) >= 4
        ]
        for segment in segments:
            words = segment.split()
            for start in range(0, len(words), 12):
                excerpt = " ".join(words[start:start + 18]).strip()
                tokens = _biorag_chat_tokens(excerpt)
                answer_overlap = len(answer_tokens & tokens)
                if not answer_overlap:
                    continue
                score = answer_overlap * 8 + len(query_tokens & tokens) * 3
                candidate = (score, source_index, excerpt)
                if best is None or candidate[0] > best[0]:
                    best = candidate
    if best is None:
        return None
    _score, source_id, evidence = best
    grounded = dict(item)
    grounded["source_id"] = source_id
    grounded["evidence"] = evidence[:900]
    grounded["source"] = sources[source_id - 1]["source"]
    grounded["page"] = sources[source_id - 1]["page"]
    return grounded


def _biorag_extract_quiz_objects(cleaned):
    """Tách từng object câu hỏi khi Gemini quên dấu phẩy giữa các object."""
    import json

    marker = cleaned.find('"questions"')
    array_start = cleaned.find("[", marker if marker >= 0 else 0)
    if array_start < 0:
        return []

    objects = []
    object_start = None
    depth = 0
    in_string = False
    escaped = False
    for index in range(array_start + 1, len(cleaned)):
        character = cleaned[index]
        if in_string:
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                in_string = False
            continue
        if character == '"':
            in_string = True
            continue
        if character == "{":
            if depth == 0:
                object_start = index
            depth += 1
        elif character == "}" and depth:
            depth -= 1
            if depth == 0 and object_start is not None:
                candidate = cleaned[object_start:index + 1]
                try:
                    item = json.loads(candidate)
                    if isinstance(item, dict):
                        objects.append(item)
                except json.JSONDecodeError:
                    pass
                object_start = None
        elif character == "]" and depth == 0:
            break
    return objects


def _biorag_answer_index(value):
    """Chuẩn hóa đáp án A-D hoặc chỉ số 0-3."""
    import re

    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if 0 <= value <= 3 else (3 if value == 4 else None)
    normalized = str(value or "").strip().upper()
    letter = re.search(r"(?:^|[^A-Z])([ABCD])(?:[^A-Z]|$)", normalized)
    if letter:
        return ord(letter.group(1)) - ord("A")
    number = re.search(r"\d+", normalized)
    if number:
        parsed = int(number.group(0))
        return parsed if 0 <= parsed <= 3 else (3 if parsed == 4 else None)
    return None


def _biorag_build_quiz_item(raw, sources, item_id):
    """Chuẩn hóa một câu hỏi từ nhiều biến thể khóa mà mô hình có thể trả về."""
    if not isinstance(raw, dict):
        return None

    question = str(
        raw.get("question")
        or raw.get("question_text")
        or raw.get("cau_hoi")
        or raw.get("câu_hỏi")
        or raw.get("câu hỏi")
        or ""
    ).strip()
    options = (
        raw.get("options")
        or raw.get("choices")
        or raw.get("answers")
        or raw.get("lua_chon")
        or raw.get("lựa_chọn")
        or raw.get("phuong_an")
        or raw.get("phương_án")
    )
    if isinstance(options, dict):
        options = [options.get(letter, options.get(letter.lower(), "")) for letter in ("A", "B", "C", "D")]
    if not question or not isinstance(options, list) or len(options) != 4:
        return None

    normalized_options = []
    for option in options:
        if isinstance(option, dict):
            option = option.get("text") or option.get("content") or option.get("option") or option.get("value") or ""
        normalized_options.append(str(option).strip())
    if any(not option for option in normalized_options):
        return None

    answer_value = raw.get(
        "answer_index",
        raw.get("correct_answer", raw.get("answer", raw.get("dap_an_dung", raw.get("đáp_án_đúng")))),
    )
    answer_index = _biorag_answer_index(answer_value)
    if answer_index is None:
        return None

    try:
        source_id = int(raw.get("source_id", raw.get("nguon_id", raw.get("nguồn_id", 1))))
    except (TypeError, ValueError):
        source_id = 1
    source_id = max(1, min(len(sources), source_id))
    verified_source = sources[source_id - 1]
    explanation = str(
        raw.get("explanation")
        or raw.get("reason")
        or raw.get("giai_thich")
        or raw.get("giải_thích")
        or ""
    ).strip()
    difficulty_value = str(
        raw.get("difficulty")
        or raw.get("level")
        or raw.get("muc_do")
        or raw.get("mức_độ")
        or "NB"
    ).strip().upper()
    difficulty = {
        "NB": "Nhận biết", "NHAN BIET": "Nhận biết", "NHẬN BIẾT": "Nhận biết",
        "TH": "Thông hiểu", "THONG HIEU": "Thông hiểu", "THÔNG HIỂU": "Thông hiểu",
        "VD": "Vận dụng", "VAN DUNG": "Vận dụng", "VẬN DỤNG": "Vận dụng",
    }.get(difficulty_value, "Nhận biết")
    evidence = str(
        raw.get("evidence")
        or raw.get("quote")
        or raw.get("citation")
        or raw.get("bang_chung")
        or raw.get("bằng_chứng")
        or ""
    ).strip().strip('"“”')
    return {
        "id": item_id,
        "question": question[:1000],
        "options": [option[:500] for option in normalized_options],
        "answer_index": answer_index,
        "explanation": explanation[:1800] or "Đáp án được xác định từ nội dung SGK đã truy xuất.",
        "difficulty": difficulty,
        "evidence": evidence[:900],
        "source_id": source_id,
        "source": verified_source["source"],
        "page": verified_source["page"],
    }


def _biorag_filter_grounded_questions(questions, sources):
    """Chỉ giữ câu có trích dẫn thật và đáp án xuất hiện trong bằng chứng SGK."""
    stop_words = {
        "cua", "cho", "voi", "trong", "nhung", "duoc", "theo", "mot", "cac",
        "nay", "do", "la", "va", "khi", "qua", "tu", "den", "mau", "anh", "sang",
    }
    grounded = []
    for item in questions:
        repaired = _biorag_repair_quiz_evidence(item, sources)
        if repaired is not None:
            item = repaired
        try:
            source_id = int(item.get("source_id", 1))
        except (TypeError, ValueError):
            continue
        if source_id < 1 or source_id > len(sources):
            continue
        source_text = _biorag_normalize_search_text(sources[source_id - 1].get("text", ""))
        evidence = _biorag_normalize_search_text(item.get("evidence", ""))
        evidence_tokens = evidence.split()
        if len(evidence_tokens) < 4 or evidence not in source_text:
            continue

        answer_index = item.get("answer_index")
        options = item.get("options") if isinstance(item.get("options"), list) else []
        if not isinstance(answer_index, int) or not 0 <= answer_index < len(options):
            continue
        answer_tokens = {
            token for token in _biorag_normalize_search_text(options[answer_index]).split()
            if len(token) >= 3 and token not in stop_words
        }
        if answer_tokens and not answer_tokens.intersection(evidence_tokens):
            continue

        item["id"] = len(grounded) + 1
        grounded.append(item)
    return grounded


def _biorag_parse_quiz_lines(raw_text, expected_count, sources):
    """Đọc giao thức dòng mới có mức độ/bằng chứng và vẫn tương thích V4.2."""
    import re

    questions = []
    for raw_line in str(raw_text or "").splitlines():
        line = raw_line.strip().strip("`").strip()
        line = re.sub(r"^(?:[-*]\s*|\d+[.)]\s*)", "", line)
        if "||" not in line:
            continue
        parts = [part.strip() for part in line.split("||")]
        if parts and parts[0].upper() in {"Q", "QUESTION", "CAU", "CÂU"}:
            parts = parts[1:]
        difficulty, evidence = "NB", ""
        if len(parts) >= 10 and parts[0].upper() in {"NB", "TH", "VD"}:
            difficulty = parts[0].upper()
            question, option_a, option_b, option_c, option_d, answer, explanation, source_id, evidence = parts[1:10]
        elif len(parts) >= 8:
            question, option_a, option_b, option_c, option_d, answer, explanation, source_id = parts[:8]
            if len(parts) >= 9:
                evidence = parts[8]
        else:
            continue
        item = _biorag_build_quiz_item({
            "difficulty": difficulty,
            "question": question,
            "options": [option_a, option_b, option_c, option_d],
            "answer": answer,
            "explanation": explanation,
            "source_id": source_id,
            "evidence": evidence,
        }, sources, len(questions) + 1)
        if item:
            questions.append(item)
        if len(questions) >= max(expected_count * 2, 60):
            break
    return questions


def _biorag_parse_quiz_payload(raw_text, expected_count, sources, require_count=True):
    """Đọc JSON chuẩn hoặc JSON thiếu dấu phẩy, rồi gắn nguồn đã xác thực."""
    import json
    import re

    cleaned = str(raw_text or "").strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    object_start, object_end = cleaned.find("{"), cleaned.rfind("}")
    array_start, array_end = cleaned.find("["), cleaned.rfind("]")
    if object_start < 0 and array_start < 0:
        raise ValueError("Mô hình không trả về JSON đề kiểm tra hợp lệ.")

    raw_questions = None
    try:
        if object_start >= 0 and object_end > object_start:
            payload = json.loads(cleaned[object_start:object_end + 1])
        elif array_end > array_start:
            payload = json.loads(cleaned[array_start:array_end + 1])
        else:
            payload = None
        raw_questions = payload.get("questions") if isinstance(payload, dict) else payload
    except json.JSONDecodeError:
        raw_questions = _biorag_extract_quiz_objects(cleaned)

    if not isinstance(raw_questions, list):
        raise ValueError("Đề kiểm tra thiếu danh sách câu hỏi.")

    questions = []
    for raw in raw_questions:
        item = _biorag_build_quiz_item(raw, sources, len(questions) + 1)
        if item:
            questions.append(item)
        if len(questions) >= max(expected_count * 2, 60):
            break

    if not questions:
        raise ValueError("Mô hình chưa tạo được câu hỏi hợp lệ.")
    if require_count and len(questions) < expected_count:
        raise ValueError("Mô hình chưa tạo đủ số câu hỏi hợp lệ. Hãy thử lại.")
    return questions


def _biorag_quiz_difficulty_plan(mode, count):
    """Trả về phân bố mức độ cho đề trắc nghiệm (5, 10, 15, 20, 28, 40 câu...)."""
    plans = {
        "basic": {5: (3, 2, 0), 10: (7, 3, 0), 15: (9, 5, 1), 20: (12, 6, 2), 28: (17, 8, 3), 40: (24, 12, 4)},
        "balanced": {5: (2, 2, 1), 10: (4, 4, 2), 15: (6, 6, 3), 20: (8, 8, 4), 28: (11, 11, 6), 40: (16, 16, 8)},
        "advanced": {5: (1, 2, 2), 10: (2, 4, 4), 15: (3, 6, 6), 20: (4, 8, 8), 28: (6, 11, 11), 40: (8, 16, 16)},
    }
    labels = {"basic": "Cơ bản", "balanced": "Cân bằng", "advanced": "Nâng cao"}
    selected = mode if mode in plans else "balanced"
    count_int = int(count)
    if count_int in plans[selected]:
        nb, th, vd = plans[selected][count_int]
    else:
        if selected == "basic":
            nb = int(round(count_int * 0.6))
            th = int(round(count_int * 0.3))
            vd = max(0, count_int - nb - th)
        elif selected == "advanced":
            nb = int(round(count_int * 0.2))
            th = int(round(count_int * 0.4))
            vd = max(0, count_int - nb - th)
        else:  # balanced
            nb = int(round(count_int * 0.4))
            th = int(round(count_int * 0.4))
            vd = max(0, count_int - nb - th)
    return selected, labels[selected], nb, th, vd


def _biorag_extract_lesson_json(raw_text):
    """Đọc object JSON bài học từ phản hồi LLM, kể cả khi có code fence."""
    import json
    import re

    def load_with_positional_repairs(value):
        """Sửa tuần tự dấu phẩy thiếu và dấu ngoặc kép chưa escape.

        Gemini Flash Lite thường trả lỗi ``Expecting ',' delimiter`` tại
        token ngay sau vị trí hỏng. Dựa vào ``JSONDecodeError.pos`` giúp sửa
        đúng chỗ mà không thay đổi nội dung khoa học trong chuỗi.
        """
        working = str(value)
        last_error = None
        for _ in range(32):
            try:
                return json.loads(working)
            except json.JSONDecodeError as exc:
                last_error = exc
                if "Expecting ',' delimiter" not in str(exc):
                    break

                right_index = max(0, min(int(exc.pos), len(working)))
                while right_index < len(working) and working[right_index].isspace():
                    right_index += 1
                left_index = right_index - 1
                while left_index >= 0 and working[left_index].isspace():
                    left_index -= 1
                if left_index < 0 or right_index >= len(working):
                    break

                left_char = working[left_index]
                right_char = working[right_index]
                if left_char in {'"', '}', ']'} or left_char.isdigit():
                    if right_char in {'"', '{', '['}:
                        working = working[:right_index] + "," + working[right_index:]
                        continue

                # Ví dụ: "Nhân là "trung tâm" của tế bào". JSON coi dấu
                # quote trước từ ``trung`` là kết thúc chuỗi. Escape quote đó;
                # vòng kế tiếp sẽ xử lý quote đóng tương ứng.
                if left_char == '"' and (right_char.isalpha() or right_char.isdigit()):
                    if left_index == 0 or working[left_index - 1] != "\\":
                        working = working[:left_index] + "\\" + working[left_index:]
                        continue
                break
        if last_error is not None:
            raise last_error
        raise ValueError("JSON bài học chưa hợp lệ.")

    cleaned = str(raw_text or "").strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    start, end = cleaned.find("{"), cleaned.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("Mô hình chưa trả về dữ liệu bài học dạng JSON.")
    candidate = cleaned[start:end + 1]
    attempts = [candidate]

    # Các mô hình nhỏ đôi khi quên dấu phẩy giữa hai trường hoặc hai object.
    # Sửa đúng các ranh giới cấu trúc, không thay đổi nội dung khoa học.
    repaired = re.sub(
        r'([}\]"])\s*(?="[^"\r\n]+"\s*:)',
        r'\1,\n',
        candidate,
    )
    repaired = re.sub(r'}\s*(?={)', r'},\n', repaired)
    repaired = re.sub(r',\s*([}\]])', r'\1', repaired)
    if repaired != candidate:
        attempts.append(repaired)

    last_error = None
    for attempt in attempts:
        try:
            payload = load_with_positional_repairs(attempt)
            if not isinstance(payload, dict):
                raise ValueError("Dữ liệu bài học không đúng cấu trúc.")
            return payload
        except (json.JSONDecodeError, ValueError) as exc:
            last_error = exc
    raise ValueError(f"JSON bài học chưa hợp lệ: {last_error}")


def _biorag_lesson_text(value, limit=1200):
    import re

    text = str(value or "").replace("\u200b", " ").replace("\ufeff", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.;:!?])", r"\1", text)
    text = re.sub(r"([,.;:!?])(?=[^\s\d])", r"\1 ", text)
    return text.strip()[:limit]


def _biorag_lesson_list(value, limit, item_limit=500):
    if not isinstance(value, list):
        return []
    result = []
    for item in value:
        text = _biorag_lesson_text(item, item_limit)
        if text and text not in result:
            result.append(text)
        if len(result) >= limit:
            break
    return result


def _biorag_is_incomplete_lesson_text(value):
    """Nhận diện câu OCR/LLM bị cắt như ``Sự khác biệt chủ``."""
    import re

    text = _biorag_lesson_text(value, 1400)
    if not text:
        return True
    words = re.findall(r"\w+", text, flags=re.UNICODE)
    if len(words) < 5:
        return True
    normalized = _biorag_normalize_search_text(text)
    dangling_endings = (
        " va", " hoac", " la", " gom", " nhu", " cua", " giua", " voi",
        " duoc", " co", " cac", " nhung", " mot", " hai", " chu", " cau",
        " thanh", " phan", " chuc", " qua", " trinh", " dac", " diem",
        " su", " khac", " biet", " nam", " o", " vao", " tren", " duoi",
        " khi", " de", " tu", " theo", " bang", " phia", " ben",
        " chi", " con", " ma", " nen", " vi", " tuy", " neu", " thi",
        " boi", " roi", " dong", " thoi", " trong khi", " mac du",
    )
    if re.search(r"[,;:\-–—]\s*$", text):
        return True
    if any(normalized.endswith(ending) for ending in dangling_endings):
        return True
    if len(words) < 10 and not re.search(r"[.!?…:]$", text):
        return True
    return False


def _biorag_has_dangling_lesson_ending(value):
    """Kiểm tra đuôi câu dang dở mà vẫn cho phép gạch đầu dòng ngắn hợp lệ."""
    import re

    text = _biorag_lesson_text(value, 1800)
    if not text:
        return True
    words = _biorag_normalize_search_text(text).split()
    dangling_words = {
        "va", "hoac", "la", "gom", "nhu", "cua", "giua", "voi", "duoc",
        "co", "cac", "nhung", "mot", "hai", "chu", "cau", "thanh", "phan",
        "chuc", "qua", "trinh", "dac", "diem", "su", "khac", "biet", "nam",
        "o", "vao", "tren", "duoi", "khi", "de", "tu", "theo", "bang",
        "phia", "ben", "chi", "con", "ma", "nen", "vi", "tuy", "neu",
        "thi", "boi", "roi", "dong", "thoi",
    }
    if re.search(r"[,;:\-–—]\s*$", text):
        return True
    return bool(words and words[-1] in dangling_words)


def _biorag_strip_lesson_prefix(title, number):
    """Bỏ ``Bài N:`` khỏi tên vì giao diện đã hiển thị số bài riêng."""
    import re

    text = _biorag_lesson_text(title, 180)
    match = re.search(r"\d+", str(number or ""))
    if not match:
        return text
    lesson_number = re.escape(match.group(0))
    cleaned = re.sub(
        rf"^\s*bài\s*{lesson_number}\s*[:.\-–—]?\s*",
        "",
        text,
        flags=re.IGNORECASE,
    ).strip()
    return cleaned or text


def _biorag_lesson_semantic_tokens(value):
    """Tập từ mang nội dung dùng để phát hiện hai phần kiến thức bị lặp."""
    stopwords = {
        "va", "la", "cua", "cac", "cho", "trong", "duoc", "voi", "mot",
        "nhung", "nay", "do", "de", "tu", "co", "ve", "giup", "hoc",
        "bai", "phan", "kien", "thuc", "noi", "dung", "can", "ghi", "nho",
    }
    return {
        token for token in _biorag_normalize_search_text(value).split()
        if len(token) >= 3 and token not in stopwords
    }


def _biorag_lesson_semantic_similarity(left, right):
    """Độ bao phủ từ khóa; 1.0 nghĩa là phần ngắn gần như nằm trong phần dài."""
    left_tokens = _biorag_lesson_semantic_tokens(left)
    right_tokens = _biorag_lesson_semantic_tokens(right)
    if len(left_tokens) < 4 or len(right_tokens) < 4:
        return 0.0
    return len(left_tokens & right_tokens) / min(len(left_tokens), len(right_tokens))


def _biorag_lesson_section_text(section):
    if not isinstance(section, dict):
        return ""
    values = [_biorag_lesson_text(section.get("title"), 180)]
    values.extend(_biorag_lesson_list(section.get("paragraphs"), 6, 1200))
    values.extend(_biorag_lesson_list(section.get("bullets"), 10, 600))
    values.append(_biorag_lesson_text(section.get("example"), 700))
    values.append(_biorag_lesson_text(section.get("note"), 700))
    return " ".join(value for value in values if value)


def _biorag_fill_missing_lesson_sections(sections, raw, content):
    """Bổ sung phần còn thiếu bằng ứng viên cụ thể và không trùng nội dung."""
    result = list(sections[:4])
    if len(result) >= 3:
        return result

    candidates = []

    # Ưu tiên một mục thuật ngữ cụ thể thay vì biến tổng quan thành phần thứ ba.
    term_sentences = []
    for item in raw.get("terms", []) if isinstance(raw.get("terms"), list) else []:
        if not isinstance(item, dict):
            continue
        term = _biorag_lesson_text(item.get("term"), 120)
        definition = _biorag_lesson_text(item.get("definition"), 700)
        sentence = f"{term}: {definition}" if term and definition else ""
        if sentence and not _biorag_is_incomplete_lesson_text(sentence):
            term_sentences.append(sentence)
    if term_sentences:
        candidates.append(("Thuật ngữ và chức năng", " ".join(term_sentences[:4])))

    # Tiếp theo mới dùng các trường cụ thể chưa xuất hiện trong phần đã chuẩn hóa.
    for item in raw.get("sections", []) if isinstance(raw.get("sections"), list) else []:
        if not isinstance(item, dict):
            continue
        candidate_title = _biorag_lesson_text(item.get("title"), 180) or "Kiến thức cụ thể"
        for field in ("paragraphs", "bullets"):
            candidates.extend(
                (candidate_title, text)
                for text in _biorag_lesson_list(item.get(field), 6, 900)
            )
        for field in ("example", "note"):
            text = _biorag_lesson_text(item.get(field), 700)
            if text:
                candidates.append((candidate_title, text))

    for item in raw.get("quick_check", []) if isinstance(raw.get("quick_check"), list) else []:
        if isinstance(item, dict):
            explanation = _biorag_lesson_text(item.get("explanation"), 700)
            if explanation:
                candidates.append(("Củng cố kiến thức", explanation))

    candidates.extend(
        ("Nội dung cần ghi nhớ", text)
        for text in _biorag_lesson_list(raw.get("summary"), 6, 900)
    )
    diagram_raw = raw.get("diagram") if isinstance(raw.get("diagram"), dict) else {}
    candidates.extend(
        ("Sơ đồ kiến thức", text)
        for text in _biorag_lesson_list(diagram_raw.get("nodes"), 6, 500)
    )
    if content:
        candidates.append(("Kiến thức trọng tâm", content))

    used = {
        _biorag_normalize_search_text(value)
        for section in result
        if isinstance(section, dict)
        for value in (
            list(section.get("paragraphs", []))
            + list(section.get("bullets", []))
            + [section.get("example", ""), section.get("note", "")]
        )
        if value
    }
    existing_texts = [_biorag_lesson_section_text(section) for section in result]
    for candidate_title, candidate in candidates:
        text = _biorag_lesson_text(candidate, 2200)
        normalized = _biorag_normalize_search_text(text)
        if (
            len(text.split()) < 5
            or not normalized
            or normalized in used
            or _biorag_is_incomplete_lesson_text(text)
            or _biorag_lesson_semantic_similarity(text, content) >= 0.82
            or any(
                _biorag_lesson_semantic_similarity(text, existing) >= 0.82
                for existing in existing_texts
            )
        ):
            continue
        index = len(result)
        result.append({
            "title": f"{index + 1}. {candidate_title}",
            "paragraphs": [text],
            "bullets": [],
            "example": "",
            "note": "",
        })
        used.add(normalized)
        existing_texts.append(_biorag_lesson_section_text(result[-1]))
        if len(result) >= 3:
            break
    return result


def _biorag_normalize_generated_lesson(raw, grade, number, topic, sources):
    """Chuẩn hóa bản nháp để chỉ trả các trường giao diện hỗ trợ."""
    title = _biorag_strip_lesson_prefix(raw.get("title") or topic, number)
    if title:
        title = title[:1].upper() + title[1:]
    objectives = _biorag_lesson_list(raw.get("objectives"), 6, 320)
    if len(objectives) < 2:
        objectives = [
            f"Trình bày được kiến thức trọng tâm về {topic}.",
            f"Vận dụng kiến thức về {topic} để giải thích tình huống gần gũi.",
        ]
    content = _biorag_lesson_text(raw.get("content"), 3500)
    if not content:
        content = f"Bài học giúp học sinh tìm hiểu kiến thức trọng tâm về {topic}."

    warmup_raw = raw.get("warmup") if isinstance(raw.get("warmup"), dict) else {}
    warmup = {
        "question": _biorag_lesson_text(warmup_raw.get("question"), 500),
        "hint": _biorag_lesson_text(warmup_raw.get("hint"), 400),
    }
    if not warmup["question"]:
        warmup["question"] = f"Em đã biết gì về {topic}?"

    raw_section_count = len(raw.get("sections", [])) if isinstance(raw.get("sections"), list) else 0
    sections = []
    for item in raw.get("sections", []) if isinstance(raw.get("sections"), list) else []:
        if not isinstance(item, dict):
            continue
        section = {
            "title": _biorag_lesson_text(item.get("title"), 180),
            "paragraphs": [
                paragraph
                for paragraph in _biorag_lesson_list(item.get("paragraphs"), 3, 1100)
                if not _biorag_is_incomplete_lesson_text(paragraph)
            ],
            "bullets": _biorag_lesson_list(item.get("bullets"), 5, 500),
            "example": _biorag_lesson_text(item.get("example"), 600),
            "note": _biorag_lesson_text(item.get("note"), 600),
        }
        if section["title"] and (section["paragraphs"] or section["bullets"]):
            sections.append(section)
        if len(sections) >= 4:
            break
    valid_section_count = len(sections)
    sections = _biorag_fill_missing_lesson_sections(sections, raw, content)
    logger.info(
        "Lesson section normalization: raw=%d valid=%d final=%d",
        raw_section_count,
        valid_section_count,
        len(sections),
    )
    if len(sections) < 2:
        raise ValueError("Mô hình chưa tạo đủ hai phần kiến thức hợp lệ cho bài học.")

    diagram_raw = raw.get("diagram") if isinstance(raw.get("diagram"), dict) else {}
    diagram = {
        "title": _biorag_lesson_text(diagram_raw.get("title") or "Sơ đồ kiến thức", 180),
        "nodes": _biorag_lesson_list(diagram_raw.get("nodes"), 6, 260),
    }
    if len(diagram["nodes"]) < 3:
        diagram["nodes"] = [title] + [section["title"] for section in sections[:4]]

    terms = []
    for item in raw.get("terms", []) if isinstance(raw.get("terms"), list) else []:
        if not isinstance(item, dict):
            continue
        term = _biorag_lesson_text(item.get("term"), 120)
        definition = _biorag_lesson_text(item.get("definition"), 500)
        if term and definition and not _biorag_is_incomplete_lesson_text(definition):
            terms.append({"term": term, "definition": definition})
        if len(terms) >= 8:
            break

    summary = [
        text for text in _biorag_lesson_list(raw.get("summary"), 6, 500)
        if not _biorag_is_incomplete_lesson_text(text)
    ]
    if len(summary) < 2:
        summary = [
            paragraph
            for section in sections
            for paragraph in section.get("paragraphs", [])[:1]
        ][:4]
    quick_check = []
    for item in raw.get("quick_check", []) if isinstance(raw.get("quick_check"), list) else []:
        if not isinstance(item, dict):
            continue
        question = _biorag_lesson_text(item.get("question"), 600)
        options = _biorag_lesson_list(item.get("options"), 4, 300)
        answer_index = _biorag_answer_index(item.get("answer_index", item.get("answer")))
        explanation = _biorag_lesson_text(item.get("explanation"), 800)
        if explanation and _biorag_is_incomplete_lesson_text(explanation):
            explanation = ""
        if question and len(options) == 4 and answer_index is not None:
            quick_check.append({
                "question": question,
                "options": options,
                "answer_index": answer_index,
                "explanation": explanation or "Đáp án dựa trên ngữ liệu SGK đã truy xuất.",
            })
        if len(quick_check) >= 3:
            break

    page_values = []
    source_payload = []
    for source in sources:
        page = _biorag_lesson_text(source.get("page"), 40) or "?"
        source_name = _biorag_lesson_text(source.get("source"), 220) or "SGK KNTT"
        if page not in page_values:
            page_values.append(page)
        source_payload.append({"source": source_name, "page": page})
    source_label = f"SGK KHTN {grade} KNTT · RAG truy xuất trang {', '.join(page_values[:8])}"

    return {
        "grade": grade,
        "number": _biorag_lesson_text(number, 60),
        "title": title,
        "topic": _biorag_lesson_text(raw.get("topic") or topic, 240),
        "duration": _biorag_lesson_text(raw.get("duration") or "35–45 phút", 80),
        "objectives": objectives,
        "content": content,
        "source_label": source_label[:240],
        "warmup": warmup,
        "sections": sections,
        "diagram": diagram,
        "terms": terms,
        "summary": summary,
        "quick_check": quick_check,
        "active": True,
        "origin": "rag_draft",
        "generation_sources": source_payload[:12],
        "lesson_version": 2,
    }


def _biorag_lesson_quality_issues(lesson, topic):
    """Kiểm tra bản nháp trước khi cho phép giáo viên duyệt và lưu."""
    import re

    issues = []
    if not isinstance(lesson, dict):
        return ["Bản nháp không đúng cấu trúc."]

    title = _biorag_lesson_text(lesson.get("title"), 240)
    content = _biorag_lesson_text(lesson.get("content"), 4000)
    objectives = lesson.get("objectives") if isinstance(lesson.get("objectives"), list) else []
    sections = lesson.get("sections") if isinstance(lesson.get("sections"), list) else []
    if len(title) < 5:
        issues.append("Tên bài học quá ngắn.")
    if len(content.split()) < 24:
        issues.append("Phần tổng quan chưa đủ nội dung.")
    if len(objectives) < 3:
        issues.append("Chưa có đủ ba mục tiêu học tập.")
    if len(sections) < 2:
        issues.append("Chưa có đủ hai phần kiến thức hợp lệ.")
    if _biorag_is_incomplete_lesson_text(content):
        issues.append("Phần tổng quan bị cắt hoặc chưa kết thúc.")
    for objective in objectives:
        if _biorag_has_dangling_lesson_ending(objective):
            issues.append("Một mục tiêu học tập bị cắt giữa câu.")

    normalized_content = _biorag_normalize_search_text(content)
    layout_markers = re.findall(
        r"\b(?:muc tieu|em da hoc|hinh\s*\d+(?:\s*\d+)?|chuong\s+[a-z0-9]+)\b",
        normalized_content,
    )
    if len(layout_markers) >= 2:
        issues.append("Phần tổng quan còn lẫn tiêu đề, số hình hoặc bố cục OCR.")

    topic_tokens = {
        token for token in _biorag_normalize_search_text(topic).split()
        if len(token) >= 3 and token not in {"bai", "hoc", "cua", "cac", "cho", "trong"}
    }
    lesson_text = _biorag_normalize_search_text(
        " ".join([title, content] + [str(item.get("title", "")) for item in sections if isinstance(item, dict)])
    )
    if topic_tokens:
        matched = sum(1 for token in topic_tokens if token in lesson_text)
        if matched / len(topic_tokens) < 0.55:
            issues.append("Bản nháp chưa bám đủ chủ đề giáo viên nhập.")

    for section in sections[:3]:
        if not isinstance(section, dict):
            issues.append("Một phần kiến thức không đúng cấu trúc.")
            continue
        paragraphs = section.get("paragraphs") if isinstance(section.get("paragraphs"), list) else []
        bullets = section.get("bullets") if isinstance(section.get("bullets"), list) else []
        if not paragraphs and not bullets:
            issues.append("Một phần kiến thức chưa có nội dung.")
        for paragraph in paragraphs:
            if _biorag_is_incomplete_lesson_text(paragraph):
                issues.append("Một đoạn kiến thức bị cắt hoặc chưa kết thúc.")
        for bullet in bullets:
            if _biorag_has_dangling_lesson_ending(bullet):
                issues.append("Một gạch đầu dòng bị cắt giữa câu.")
        for field_name, label in (("example", "Ví dụ"), ("note", "Lưu ý")):
            value = section.get(field_name)
            if value and _biorag_is_incomplete_lesson_text(value):
                issues.append(f"{label} trong một phần kiến thức bị cắt giữa câu.")

    section_texts = [
        _biorag_lesson_section_text(section)
        for section in sections[:3]
        if isinstance(section, dict)
    ]
    if any(
        _biorag_lesson_semantic_similarity(section_text, content) >= 0.90
        for section_text in section_texts
    ):
        issues.append("Một phần kiến thức đang lặp lại phần tổng quan.")
    for index, left in enumerate(section_texts):
        if any(
            _biorag_lesson_semantic_similarity(left, right) >= 0.90
            for right in section_texts[index + 1:]
        ):
            issues.append("Hai phần kiến thức đang trình bày nội dung trùng nhau.")
            break

    for term in lesson.get("terms", []) if isinstance(lesson.get("terms"), list) else []:
        if isinstance(term, dict) and _biorag_is_incomplete_lesson_text(term.get("definition")):
            issues.append("Một định nghĩa thuật ngữ bị cắt giữa câu.")
    for summary_item in lesson.get("summary", []) if isinstance(lesson.get("summary"), list) else []:
        if _biorag_has_dangling_lesson_ending(summary_item):
            issues.append("Một ý ghi nhớ bị cắt giữa câu.")
    for check in lesson.get("quick_check", []) if isinstance(lesson.get("quick_check"), list) else []:
        if isinstance(check, dict) and _biorag_is_incomplete_lesson_text(check.get("explanation")):
            issues.append("Một lời giải kiểm tra nhanh bị cắt giữa câu.")
    return list(dict.fromkeys(issues))


def _biorag_editorial_retry_prompt(grade, number, topic, context_blocks):
    """Prompt nhỏ, ít khóa lồng nhau để mô hình nhỏ vẫn trả JSON ổn định."""
    return f"""Bạn là biên tập viên SGK Khoa học tự nhiên lớp {grade}.
Hãy viết lại một bài học ngắn, mạch lạc từ đúng ngữ liệu bên dưới.

Số bài: {number or 'chưa xác định'}
Chủ đề: {topic}

QUY TẮC BẮT BUỘC:
- Chỉ dùng kiến thức xuất hiện trong ngữ liệu; không tự thêm kiến thức.
- Bỏ mục lục, số hình, đầu trang, chân trang và câu OCR bị đảo thứ tự.
- Không chép nguyên chuỗi OCR rời rạc; phải viết thành câu tiếng Việt hoàn chỉnh.
- Mỗi đoạn phải kết thúc trọn ý; không để lại cụm từ hoặc câu đang viết dở.
- Không kết thúc đoạn bằng dấu phẩy, dấu chấm phẩy hoặc các từ nối như "chỉ",
  "còn", "mà", "nên", "vì", "tuy", "nếu", "thì".
- Tổng quan gồm 2 đến 4 câu; có từ 2 đến 4 phần kiến thức tùy cấu trúc thực tế
  của ngữ liệu SGK. Không được chia nhỏ hoặc lặp nội dung chỉ để đủ số lượng.
- Các phần phải có vai trò khác nhau và tiêu đề cụ thể; không dùng "Kiến thức trọng tâm"
  hoặc "Nội dung cần ghi nhớ" làm tiêu đề phần.
- Không được sao chép phần tổng quan thành một phần kiến thức. Nếu chủ đề gồm nhiều
  khía cạnh, hãy tách theo cấu tạo, chức năng, phân loại, quá trình hoặc vận dụng
  phù hợp với đúng ngữ liệu đang có.
- Trả về duy nhất JSON hợp lệ, không Markdown.

NGỮ LIỆU ĐÚNG BÀI:
{chr(10).join(context_blocks)}

CẤU TRÚC JSON GỌN:
{{
  "title": "Tên bài viết hoa chữ đầu",
  "topic": "Chủ đề",
  "duration": "35–45 phút",
  "objectives": ["Mục tiêu 1", "Mục tiêu 2", "Mục tiêu 3"],
  "content": "Tổng quan bằng câu hoàn chỉnh",
  "warmup": {{"question": "Câu hỏi khởi động", "hint": "Gợi ý ngắn"}},
  "sections": [
    {{"title": "1. Tiêu đề", "paragraphs": ["Đoạn hoàn chỉnh"], "bullets": []}},
    {{"title": "2. Tiêu đề", "paragraphs": ["Đoạn hoàn chỉnh"], "bullets": []}}
  ],
  "summary": ["Ý nhớ 1", "Ý nhớ 2", "Ý nhớ 3"]
}}
"""


def _biorag_lesson_json_schema():
    """Schema gọn cho Gemini native structured output."""
    return {
        "title": "BiologyLessonDraft",
        "description": "Bản nháp bài học Khoa học tự nhiên dựa trên ngữ liệu SGK.",
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "topic": {"type": "string"},
            "duration": {"type": "string"},
            "objectives": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 3,
                "maxItems": 5,
            },
            "content": {"type": "string"},
            "warmup": {
                "type": "object",
                "properties": {
                    "question": {"type": "string"},
                    "hint": {"type": "string"},
                },
                "required": ["question", "hint"],
            },
            "sections": {
                "type": "array",
                "minItems": 2,
                "maxItems": 4,
                "items": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "paragraphs": {
                            "type": "array",
                            "items": {"type": "string"},
                            "minItems": 1,
                        },
                        "bullets": {"type": "array", "items": {"type": "string"}},
                        "example": {"type": "string"},
                        "note": {"type": "string"},
                    },
                    "required": ["title", "paragraphs", "bullets"],
                },
            },
            "diagram": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "nodes": {"type": "array", "items": {"type": "string"}},
                },
            },
            "terms": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "term": {"type": "string"},
                        "definition": {"type": "string"},
                    },
                    "required": ["term", "definition"],
                },
            },
            "summary": {
                "type": "array",
                "items": {"type": "string"},
                "minItems": 3,
                "maxItems": 5,
            },
            "quick_check": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question": {"type": "string"},
                        "options": {"type": "array", "items": {"type": "string"}},
                        "answer_index": {"type": "integer"},
                        "explanation": {"type": "string"},
                    },
                    "required": ["question", "options", "answer_index", "explanation"],
                },
            },
        },
        "required": [
            "title", "topic", "duration", "objectives", "content",
            "warmup", "sections", "summary",
        ],
    }


def _biorag_invoke_structured_lesson(llm, prompt):
    """Nhận dict trực tiếp từ Gemini; không yêu cầu mô hình tự viết JSON text."""
    if not hasattr(llm, "with_structured_output"):
        raise RuntimeError("LLM hiện tại không hỗ trợ structured output.")
    schema = _biorag_lesson_json_schema()
    errors = []
    for method in ("json_schema", "function_calling"):
        try:
            try:
                structured_llm = llm.with_structured_output(
                    schema=schema, method=method
                )
            except TypeError:
                structured_llm = llm.with_structured_output(schema, method=method)
            result = structured_llm.invoke(prompt)
            if isinstance(result, dict):
                return result
            if hasattr(result, "model_dump"):
                payload = result.model_dump()
                if isinstance(payload, dict):
                    return payload
            if hasattr(result, "dict"):
                payload = result.dict()
                if isinstance(payload, dict):
                    return payload
            raise ValueError("Structured output chưa trả về object.")
        except Exception as exc:
            errors.append(f"{method}: {exc}")
            logger.warning("Lesson structured output %s failed: %s", method, exc)
    raise RuntimeError("; ".join(errors))


def _biorag_source_fallback_lesson(grade, number, topic, sources):
    """Tạo bản nháp an toàn từ ngữ liệu khi LLM liên tục trả JSON hỏng."""
    paragraphs = []
    for source in sources:
        text = _biorag_lesson_text(source.get("text"), 1000)
        if text and text not in paragraphs:
            paragraphs.append(text)
        if len(paragraphs) >= 3:
            break
    while len(paragraphs) < 3:
        paragraphs.append(
            f"SGK truy xuất chưa cung cấp đủ nội dung riêng cho phần {len(paragraphs) + 1} về {topic}."
        )
    return {
        "title": topic,
        "topic": topic,
        "duration": "35–45 phút",
        "objectives": [
            f"Nêu được kiến thức trọng tâm về {topic}.",
            f"Mô tả được các nội dung chính của {topic} dựa trên SGK.",
            f"Vận dụng kiến thức về {topic} trong học tập.",
        ],
        "content": paragraphs[0],
        "warmup": {
            "question": f"Em đã biết gì về {topic}?",
            "hint": "Liên hệ kiến thức và hình ảnh trong SGK.",
        },
        "sections": [
            {"title": "1. Kiến thức trọng tâm", "paragraphs": [paragraphs[0]]},
            {"title": "2. Nội dung cần tìm hiểu", "paragraphs": [paragraphs[1]]},
            {"title": "3. Củng cố và vận dụng", "paragraphs": [paragraphs[2]]},
        ],
        "diagram": {
            "title": "Sơ đồ kiến thức",
            "nodes": [topic, "Kiến thức trọng tâm", "Củng cố", "Vận dụng"],
        },
        "terms": [],
        "summary": [
            "Nội dung bản nháp được tổng hợp trực tiếp từ các đoạn SGK đã truy xuất.",
            "Giáo viên cần kiểm tra và biên tập trước khi công bố.",
        ],
        "quick_check": [],
    }


def _biorag_lesson_page_number(value):
    import re

    match = re.search(r"\d+", str(value or ""))
    return int(match.group(0)) if match else None


def _biorag_is_front_matter_text(value):
    """Nhận diện hướng dẫn sử dụng, mục lục và danh mục bài ở đầu sách."""
    import re

    normalized = _biorag_normalize_search_text(value)
    markers = (
        "huong dan su dung sach",
        "huong dan su dung",
        "muc luc",
        "loi noi dau",
        "gioi thieu sach",
        "cac em hoc sinh than men",
    )
    if any(marker in normalized for marker in markers):
        return True
    lesson_mentions = len(re.findall(r"\bbai\s+\d+\b", normalized))
    chapter_mentions = len(re.findall(r"\bchuong\s+[a-z0-9]+\b", normalized))
    return lesson_mentions >= 3 or chapter_mentions >= 4


def _biorag_rank_lesson_sources(sources, number, topic, limit=8):
    """Ưu tiên đoạn khớp chủ đề và nằm trong cùng cụm trang của bài học."""
    import re

    topic_norm = _biorag_normalize_search_text(topic)
    number_norm = _biorag_normalize_search_text(number)
    topic_tokens = [
        token for token in topic_norm.split()
        if len(token) >= 3 and token not in {
            "cua", "cac", "cho", "trong", "theo", "bai", "hoc", "khoa", "nhien",
        }
    ]
    phrases = []
    for size in (4, 3, 2):
        for index in range(max(0, len(topic_tokens) - size + 1)):
            phrase = " ".join(topic_tokens[index:index + size])
            if phrase and phrase not in phrases:
                phrases.append(phrase)

    ranked = []
    for source in sources:
        text_norm = _biorag_normalize_search_text(source.get("text", ""))
        source_norm = _biorag_normalize_search_text(source.get("source", ""))
        score = 0.0
        if topic_norm and topic_norm in text_norm:
            score += 120.0
        if number_norm and number_norm in text_norm:
            score += 55.0
        for phrase in phrases:
            if phrase in text_norm:
                score += 12.0 + len(phrase.split()) * 4.0
        matched_tokens = sum(1 for token in set(topic_tokens) if token in text_norm)
        score += matched_tokens * 5.0
        if topic_tokens:
            score += 25.0 * matched_tokens / len(set(topic_tokens))
        front_matter = _biorag_is_front_matter_text(source.get("text", ""))
        if front_matter:
            score -= 300.0
        ranked.append({
            "source": source,
            "score": score,
            "page": _biorag_lesson_page_number(source.get("page")),
            "source_norm": source_norm,
            "front_matter": front_matter,
        })

    ranked.sort(key=lambda item: item["score"], reverse=True)
    if not ranked:
        return []
    content_ranked = [item for item in ranked if not item["front_matter"]]
    if content_ranked:
        ranked = content_ranked
    anchor = ranked[0]
    threshold = max(12.0, anchor["score"] * 0.32)
    selected = []
    for item in ranked:
        same_book = not anchor["source_norm"] or item["source_norm"] == anchor["source_norm"]
        near_anchor = (
            anchor["page"] is not None
            and item["page"] is not None
            and abs(item["page"] - anchor["page"]) <= 10
        )
        very_relevant = item["score"] >= max(threshold, anchor["score"] * 0.72)
        if item is anchor or (same_book and near_anchor and item["score"] >= 8.0) or very_relevant:
            selected.append(item["source"])
        if len(selected) >= int(limit):
            break
    if len(selected) < 2:
        selected = [item["source"] for item in ranked[:min(int(limit), max(2, len(ranked)))]]

    selected.sort(key=lambda source: (
        _biorag_lesson_text(source.get("source"), 220),
        _biorag_lesson_page_number(source.get("page")) or 999999,
    ))
    logger.info(
        "Lesson source filter: topic=%s number=%s pages=%s",
        topic,
        number,
        [source.get("page") for source in selected],
    )
    return selected


def _biorag_expand_lesson_source_cluster(selected, grade, limit=12):
    """Mở rộng quanh trang neo bằng các chunk cùng PDF trong bán kính 7 trang."""
    global _BIORAG_QUIZ_CHUNKS

    if not selected or not isinstance(_BIORAG_QUIZ_CHUNKS, list):
        return selected
    anchor = selected[0]
    anchor_page = _biorag_lesson_page_number(anchor.get("page"))
    anchor_source = _biorag_normalize_search_text(anchor.get("source", ""))
    if anchor_page is None:
        return selected

    candidates = []
    seen = set()
    for item in _BIORAG_QUIZ_CHUNKS:
        if _biorag_quiz_chunk_grade(item) != int(grade):
            continue
        text, source, page = _biorag_quiz_chunk_fields(item)
        page_number = _biorag_lesson_page_number(page)
        if page_number is None or abs(page_number - anchor_page) > 7:
            continue
        if anchor_source and _biorag_normalize_search_text(source) != anchor_source:
            continue
        if len(text) < 40 or _biorag_is_front_matter_text(text):
            continue
        key = (_biorag_normalize_search_text(source), str(page), text[:180])
        if key in seen:
            continue
        seen.add(key)
        candidates.append({"text": text[:2200], "source": source, "page": page})

    for source in selected:
        key = (
            _biorag_normalize_search_text(source.get("source", "")),
            str(source.get("page", "")),
            str(source.get("text", ""))[:180],
        )
        if key not in seen and not _biorag_is_front_matter_text(source.get("text", "")):
            seen.add(key)
            candidates.append(source)

    candidates.sort(key=lambda source: (
        _biorag_normalize_search_text(source.get("source", "")),
        _biorag_lesson_page_number(source.get("page")) or 999999,
    ))
    result = []
    total_chars = 0
    for source in candidates:
        projected = total_chars + len(str(source.get("text", "")))
        if projected > 18000 and result:
            break
        result.append(source)
        total_chars = projected
        if len(result) >= int(limit):
            break
    logger.info(
        "Lesson source cluster: anchor=%s pages=%s",
        anchor_page,
        [source.get("page") for source in result],
    )
    return result or selected


def _biorag_lesson_number_value(value):
    """Lấy số bài từ các cách nhập như ``Bài 19``, ``bai19`` hoặc ``19``."""
    import re

    match = re.search(r"\d+", str(value or ""))
    return int(match.group(0)) if match else None


def _biorag_lesson_header_score(text, lesson_number, topic):
    """Chấm điểm một chunk có phải trang mở đầu đúng bài hay không."""
    import re

    normalized = _biorag_normalize_search_text(text)
    if not normalized or _biorag_is_front_matter_text(text):
        return -1000.0
    prefix = normalized[:900]
    header_pattern = rf"\bbai\s*{int(lesson_number)}\b"
    header_match = re.search(header_pattern, prefix)
    if not header_match:
        return -1000.0

    topic_tokens = {
        token for token in _biorag_normalize_search_text(topic).split()
        if len(token) >= 3 and token not in {
            "bai", "hoc", "cua", "cac", "cho", "trong", "theo", "khoa", "nhien",
        }
    }
    matched = sum(1 for token in topic_tokens if token in prefix)
    score = 200.0 - min(float(header_match.start()), 700.0) * 0.12
    if topic_tokens:
        score += 140.0 * matched / len(topic_tokens)
    if "muc tieu" in prefix:
        score += 35.0
    if re.search(rf"^.{0,120}\bbai\s*{int(lesson_number)}\b", prefix):
        score += 30.0
    return score


def _biorag_select_lesson_page_range(selected, grade, number, topic, limit=14):
    """Khóa nguồn vào đúng bài: từ trang tiêu đề Bài N đến trước Bài N+1.

    Không dùng ``selected[0]`` làm trang neo vì danh sách truy xuất có thể đã
    được sắp theo số trang. Hàm quét toàn bộ chunk của đúng lớp, chọn trang có
    tiêu đề bài và chủ đề khớp nhất, sau đó lấy các trang liên tiếp cùng PDF.
    """
    import re

    global _BIORAG_QUIZ_CHUNKS

    lesson_number = _biorag_lesson_number_value(number)
    if lesson_number is None or not isinstance(_BIORAG_QUIZ_CHUNKS, list):
        return _biorag_expand_lesson_source_cluster(selected, grade, limit=limit)

    rows = []
    for item in _BIORAG_QUIZ_CHUNKS:
        if _biorag_quiz_chunk_grade(item) != int(grade):
            continue
        text, source, page = _biorag_quiz_chunk_fields(item)
        page_number = _biorag_lesson_page_number(page)
        if page_number is None or len(str(text).strip()) < 40:
            continue
        rows.append({
            "text": str(text)[:2600],
            "source": source,
            "page": page,
            "page_number": page_number,
            "source_norm": _biorag_normalize_search_text(source),
        })

    anchors = []
    for row in rows:
        score = _biorag_lesson_header_score(row["text"], lesson_number, topic)
        if score > -1000.0:
            candidate = dict(row)
            candidate["header_score"] = score
            anchors.append(candidate)
    if not anchors:
        logger.warning(
            "Lesson boundary: no exact header for grade=%s number=%s topic=%s; using fallback",
            grade, number, topic,
        )
        return _biorag_expand_lesson_source_cluster(selected, grade, limit=limit)

    anchors.sort(key=lambda row: (-row["header_score"], row["page_number"]))
    anchor = anchors[0]
    start_page = anchor["page_number"]
    book_rows = [row for row in rows if row["source_norm"] == anchor["source_norm"]]

    next_pattern = re.compile(rf"\bbai\s*{lesson_number + 1}\b")
    next_pages = []
    for row in book_rows:
        if row["page_number"] <= start_page:
            continue
        normalized = _biorag_normalize_search_text(row["text"])
        prefix = normalized[:700]
        if (
            next_pattern.search(prefix)
            and not _biorag_is_front_matter_text(row["text"])
            and ("muc tieu" in prefix or next_pattern.search(prefix[:180]))
        ):
            next_pages.append(row["page_number"])

    end_page = min(next_pages) - 1 if next_pages else start_page + 6
    end_page = max(start_page, min(end_page, start_page + 9))

    candidates = [
        row for row in book_rows
        if start_page <= row["page_number"] <= end_page
        and not _biorag_is_front_matter_text(row["text"])
    ]
    candidates.sort(key=lambda row: (row["page_number"], -len(row["text"])))

    result = []
    seen = set()
    total_chars = 0
    for row in candidates:
        normalized_text = _biorag_normalize_search_text(row["text"])
        key = (row["source_norm"], row["page_number"], normalized_text[:220])
        if key in seen:
            continue
        seen.add(key)
        projected = total_chars + len(row["text"])
        if projected > 22000 and result:
            break
        result.append({
            "text": row["text"],
            "source": row["source"],
            "page": row["page"],
        })
        total_chars = projected
        if len(result) >= int(limit):
            break

    selected_pages = sorted({
        _biorag_lesson_page_number(source.get("page")) for source in result
    } - {None})
    if not result or start_page not in selected_pages:
        logger.warning("Lesson boundary produced no usable anchor page; using fallback")
        return _biorag_expand_lesson_source_cluster(selected, grade, limit=limit)

    logger.info(
        "Lesson boundary locked: grade=%s lesson=%s source=%s range=%s-%s pages=%s",
        grade, lesson_number, anchor.get("source"), start_page, end_page, selected_pages,
    )
    return result


# --- Flashcard / sơ đồ tư duy tự động từ bài học (Tính năng 2, Nhóm A) ---
STUDY_AID_CACHE_PATH = Path(PERSIST_DIR) / "lesson_study_aids.json"
_STUDY_AID_LOCK = threading.Lock()


def _biorag_load_study_aid_cache():
    if not STUDY_AID_CACHE_PATH.exists():
        return {}
    try:
        return json.loads(STUDY_AID_CACHE_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        logger.warning("Không đọc được cache flashcard/mindmap: %s", exc)
        return {}


def _biorag_save_study_aid_cache(cache):
    try:
        STUDY_AID_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with _STUDY_AID_LOCK:
            STUDY_AID_CACHE_PATH.write_text(
                json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8"
            )
    except Exception as exc:
        logger.warning("Không lưu được cache flashcard/mindmap: %s", exc)


def _biorag_study_aid_context_sources(lesson):
    """Lấy đúng cụm trang SGK thật (KHÔNG dùng content tóm tắt trong catalog,
    vốn nhiều bài chỉ là placeholder) để làm ngữ liệu sinh flashcard/sơ đồ tư
    duy. Tái dùng đúng pipeline đã kiểm chứng khi soạn bài học
    (_biorag_load_quiz_context → _biorag_rank_lesson_sources →
    _biorag_select_lesson_page_range), vốn đã tự loại trang mục lục và khoá
    đúng phạm vi Bài N → trước Bài N+1.
    """
    grade = lesson.get("grade")
    number = lesson.get("number") or ""
    topic = lesson.get("title") or lesson.get("topic") or ""
    if grade is None or not str(topic).strip():
        raise LookupError("Bài học thiếu lớp hoặc tên bài để tra cứu SGK.")
    grade = int(grade)
    retrieval_query = f"{number} {topic}".strip()
    sources = _biorag_load_quiz_context(grade, retrieval_query, 8)
    sources = _biorag_rank_lesson_sources(sources, number, topic, limit=8)
    sources = _biorag_select_lesson_page_range(sources, grade, number, topic, limit=14)
    if not sources:
        raise LookupError("Không tìm thấy cụm trang SGK đủ liên quan để tạo tài liệu ôn tập.")
    return sources


def _biorag_clean_mindmap_branch(branch):
    """Chuẩn hoá một nhánh sơ đồ tư duy dạng PHẲNG (nhãn + danh sách ý con).

    Cố tình KHÔNG lồng nhánh con thành cây nhiều cấp: mô hình Gemini Flash
    Lite hay viết hỏng cú pháp JSON khi phải sinh object lồng nhau nhiều
    tầng (đã gặp lỗi "Expecting ',' delimiter" lặp lại ở đúng vị trí cấu
    trúc lồng nhánh con). Nhãn + danh sách ý (mảng chuỗi phẳng) vẫn đủ để
    học sinh ôn tập mà JSON gần như không thể hỏng cú pháp.
    """
    if not isinstance(branch, dict):
        return None
    label = _biorag_lesson_text(branch.get("label") or branch.get("title") or branch.get("name"), 200)
    if not label:
        return None
    raw_points = branch.get("points") or branch.get("children") or branch.get("items") or []
    if not isinstance(raw_points, list):
        raw_points = []
    points = []
    for point in raw_points[:8]:
        if isinstance(point, dict):
            point = point.get("label") or point.get("text") or point.get("point")
        text = _biorag_lesson_text(point, 200)
        if text and text not in points:
            points.append(text)
    return {"label": label, "points": points}


def _biorag_normalize_study_aid(raw, lesson):
    """Chuẩn hoá + kiểm tra tối thiểu payload flashcard/mindmap từ LLM, để
    không lưu vào cache một kết quả rỗng hoặc thiếu cấu trúc."""
    if not isinstance(raw, dict):
        raise ValueError("Phản hồi không đúng cấu trúc JSON.")

    flashcards = []
    seen_fronts = set()
    for item in raw.get("flashcards") or []:
        if not isinstance(item, dict):
            continue
        front = _biorag_lesson_text(item.get("front") or item.get("question"), 300)
        back = _biorag_lesson_text(item.get("back") or item.get("answer"), 700)
        key = _biorag_normalize_search_text(front)
        if front and back and key not in seen_fronts:
            flashcards.append({"front": front, "back": back})
            seen_fronts.add(key)
    if len(flashcards) < 4:
        raise ValueError("Không đủ flashcard hợp lệ (cần tối thiểu 4).")

    mindmap_raw = raw.get("mindmap") or {}
    root_label = (
        _biorag_lesson_text(mindmap_raw.get("title"), 200)
        or _biorag_lesson_text(lesson.get("title"), 200)
        or "Sơ đồ tư duy"
    )
    raw_branches = mindmap_raw.get("branches")
    if not isinstance(raw_branches, list):
        raw_branches = []
    branches = []
    for branch in raw_branches[:8]:
        cleaned = _biorag_clean_mindmap_branch(branch)
        if cleaned:
            branches.append(cleaned)
    if len(branches) < 2:
        raise ValueError("Sơ đồ tư duy chưa đủ nhánh hợp lệ (cần tối thiểu 2).")

    return {
        "flashcards": flashcards[:20],
        "mindmap": {"title": root_label, "branches": branches},
    }


_BIORAG_STUDY_AID_Q_RE = re.compile(r"^[Qq]\s*[:：]\s*(.+)$")
_BIORAG_STUDY_AID_A_RE = re.compile(r"^[Aa]\s*[:：]\s*(.+)$")
_BIORAG_STUDY_AID_TITLE_RE = re.compile(r"^TITLE\s*[:：]\s*(.+)$", re.IGNORECASE)
_BIORAG_STUDY_AID_BRANCH_RE = re.compile(r"^NH[AÁ]NH\s*[:：]\s*(.+)$", re.IGNORECASE)
_BIORAG_STUDY_AID_POINT_RE = re.compile(r"^[-•*]\s*(.+)$")
_BIORAG_STUDY_AID_FLASHCARDS_MARKER_RE = re.compile(r"#{2,}\s*FLASHCARDS?\s*#{2,}", re.IGNORECASE)
_BIORAG_STUDY_AID_MINDMAP_MARKER_RE = re.compile(r"#{2,}\s*MINDMAP\s*#{2,}", re.IGNORECASE)


def _biorag_parse_study_aid_text(raw_text):
    """Đọc flashcard/sơ đồ tư duy từ VĂN BẢN THUẦN (không phải JSON).

    Gemini Flash Lite liên tục hỏng cú pháp JSON cho tính năng này (đã thử
    JSON lồng cây nhiều tầng, JSON phẳng, cả structured output — vẫn hỏng ở
    một vị trí tương tự mỗi lần, nhiều khả năng do dấu ngoặc kép chưa escape
    trong câu tiếng Việt). Định dạng dòng-lệnh đơn giản này không có dấu
    ngoặc/dấu phẩy cần khớp nên gần như không thể hỏng cú pháp, kể cả khi
    nội dung câu trả lời chứa dấu ngoặc kép.
    """
    text = str(raw_text or "").replace("\r\n", "\n").replace("\r", "\n")
    flash_match = _BIORAG_STUDY_AID_FLASHCARDS_MARKER_RE.search(text)
    mind_match = _BIORAG_STUDY_AID_MINDMAP_MARKER_RE.search(text)
    flash_block = text[flash_match.end():mind_match.start()] if flash_match and mind_match else (
        text[flash_match.end():] if flash_match else ""
    )
    mind_block = text[mind_match.end():] if mind_match else ""

    flashcards = []
    pending_front = None
    for line in flash_block.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        q_match = _BIORAG_STUDY_AID_Q_RE.match(stripped)
        a_match = _BIORAG_STUDY_AID_A_RE.match(stripped)
        if q_match:
            pending_front = q_match.group(1).strip()
        elif a_match and pending_front:
            flashcards.append({"front": pending_front, "back": a_match.group(1).strip()})
            pending_front = None

    mindmap_title = ""
    branches = []
    current_branch = None
    for line in mind_block.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        title_match = _BIORAG_STUDY_AID_TITLE_RE.match(stripped)
        branch_match = _BIORAG_STUDY_AID_BRANCH_RE.match(stripped)
        point_match = _BIORAG_STUDY_AID_POINT_RE.match(stripped)
        if title_match:
            mindmap_title = title_match.group(1).strip()
        elif branch_match:
            current_branch = {"label": branch_match.group(1).strip(), "points": []}
            branches.append(current_branch)
        elif point_match and current_branch is not None:
            current_branch["points"].append(point_match.group(1).strip())

    return {
        "flashcards": flashcards,
        "mindmap": {"title": mindmap_title, "branches": branches},
    }


def _biorag_generate_study_aid(lesson, sources):
    """Gọi LLM sinh flashcard + sơ đồ tư duy từ đúng ngữ liệu SGK đã khoá
    phạm vi bài học.

    Yêu cầu mô hình xuất VĂN BẢN THUẦN theo mốc dòng-lệnh cố định (xem
    _biorag_parse_study_aid_text), KHÔNG yêu cầu JSON. Đã thử JSON lồng cây
    nhiều tầng, JSON phẳng và cả structured output của Gemini — cả ba đều bị
    gemini-3.1-flash-lite làm hỏng cú pháp hoặc từ chối. Văn bản thuần không
    có dấu ngoặc/dấu phẩy cần khớp đúng vị trí nên đáng tin cậy hơn hẳn.
    """
    context_blocks = [
        f"[NGUỒN {index} | {source['source']} | trang {source['page']}]\n{source['text']}"
        for index, source in enumerate(sources, start=1)
    ]
    grade = lesson.get("grade")
    title = lesson.get("title") or lesson.get("topic") or ""
    number = lesson.get("number") or ""
    prompt = f"""Bạn là giáo viên Khoa học tự nhiên Việt Nam, soạn TÀI LIỆU ÔN TẬP cho học sinh lớp {grade}.
Bài học: {number} — {title}

Chỉ sử dụng NGỮ LIỆU SGK bên dưới. Không bổ sung kiến thức, số liệu hay ví dụ ngoài nguồn.

NGỮ LIỆU SGK:
{chr(10).join(context_blocks)}

Xuất kết quả CHÍNH XÁC theo định dạng văn bản thuần dưới đây — KHÔNG dùng JSON, KHÔNG
dùng Markdown (không **, không #, không gạch đầu dòng kiểu 1. 2. 3.), KHÔNG dùng dấu
ngoặc kép bao quanh nội dung, không thêm ghi chú nào khác ngoài đúng các dòng theo mẫu:

###FLASHCARDS###
Q: <câu hỏi ngắn hoặc thuật ngữ>
A: <câu trả lời/định nghĩa ngắn gọn, đúng trọng tâm>
Q: <câu hỏi ngắn hoặc thuật ngữ>
A: <câu trả lời/định nghĩa ngắn gọn, đúng trọng tâm>
(tạo đủ 10-14 cặp Q/A, bao phủ đều các ý chính trong bài, không hỏi lặp ý)

###MINDMAP###
TITLE: {title}
NHANH: <tên nhánh kiến thức 1, cụm từ khoá ngắn gọn>
- <ý chính 1 thuộc nhánh này>
- <ý chính 2 thuộc nhánh này>
NHANH: <tên nhánh kiến thức 2>
- <ý chính 1>
- <ý chính 2>
(tạo 3-6 nhánh, mỗi nhánh 2-5 ý; mỗi dòng ý bắt đầu bằng dấu "-")

Mỗi dòng "Q:" phải có đúng một dòng "A:" ngay sau. Mỗi dòng "-" thuộc về nhánh "NHANH:"
gần nhất phía trên nó. Không lặp lại tên nhánh giống hệt nhau.
"""
    llm = AppServices.get_instance().llm
    raw_text = _biorag_extract_message_text(llm.invoke(prompt))
    raw_payload = _biorag_parse_study_aid_text(raw_text)
    try:
        return _biorag_normalize_study_aid(raw_payload, lesson)
    except Exception as first_error:
        logger.warning(
            "Study aid text parse invalid for lesson %s, retrying once: %s",
            lesson.get("id"), first_error,
        )
        raw_text_retry = _biorag_extract_message_text(llm.invoke(prompt))
        raw_payload_retry = _biorag_parse_study_aid_text(raw_text_retry)
        return _biorag_normalize_study_aid(raw_payload_retry, lesson)


@app.route('/api/learning/generate', methods=['POST'])
def generate_learning_lesson():
    """Tạo bản nháp bài học từ các đoạn SGK đúng lớp; chưa tự lưu catalog."""
    data = request.get_json(silent=True) or {}
    try:
        grade = int(data.get("grade"))
    except (TypeError, ValueError):
        return jsonify({"error": "Khối lớp không hợp lệ."}), 400
    number = _biorag_lesson_text(data.get("number"), 60)
    topic = _biorag_lesson_text(data.get("topic"), 240)
    if grade not in {6, 7, 8, 9}:
        return jsonify({"error": "Chỉ hỗ trợ lớp 6 đến lớp 9."}), 400
    if len(topic) < 3:
        return jsonify({"error": "Hãy nhập chủ đề cụ thể để tạo bài học."}), 400

    try:
        retrieval_query = f"{number} {topic}".strip()
        sources = _biorag_load_quiz_context(grade, retrieval_query, 8)
        sources = _biorag_rank_lesson_sources(sources, number, topic, limit=8)
        sources = _biorag_select_lesson_page_range(
            sources, grade, number, topic, limit=14
        )
        if not sources:
            raise LookupError("Không tìm thấy cụm trang SGK đủ liên quan với bài và chủ đề đã nhập.")
    except LookupError as exc:
        return jsonify({"error": str(exc)}), 404
    except Exception as exc:
        logger.error("Lesson context retrieval failed: %s", exc, exc_info=True)
        return jsonify({"error": "Chưa truy xuất được dữ liệu SGK trong database_kntt."}), 500

    context_blocks = [
        f"[NGUỒN {index} | {source['source']} | trang {source['page']}]\n{source['text']}"
        for index, source in enumerate(sources, start=1)
    ]
    prompt = f"""Bạn là giáo viên Khoa học tự nhiên Việt Nam. Hãy soạn một BẢN NHÁP bài học lớp {grade}.
Số bài do giáo viên nhập: {number or 'chưa xác định'}
Chủ đề: {topic}

Chỉ sử dụng NGỮ LIỆU SGK bên dưới. Không bổ sung số liệu, nguyên nhân, ví dụ hoặc kết luận ngoài nguồn.
Nội dung phải rõ ràng, phù hợp học sinh lớp {grade}, không sao chép nguyên đoạn dài.
Mỗi đoạn phải là câu hoàn chỉnh, kết thúc trọn ý và không có cụm từ bị cắt dở.
Không kết thúc đoạn bằng dấu phẩy, dấu chấm phẩy hoặc các từ nối như "chỉ",
"còn", "mà", "nên", "vì", "tuy", "nếu", "thì".
Số phần kiến thức phải bám cấu trúc thật của nguồn: từ 2 đến 4 phần khác nhau.
Không lặp tổng quan hoặc chia nhỏ giả tạo chỉ để tăng số phần.

NGỮ LIỆU SGK:
{chr(10).join(context_blocks)}

Trả về duy nhất một object JSON hợp lệ theo cấu trúc:
{{
  "title": "Tên bài",
  "topic": "Chủ đề RAG rõ ràng",
  "duration": "35–45 phút",
  "objectives": ["3 đến 5 mục tiêu"],
  "content": "Đoạn tổng quan 2–4 câu",
  "warmup": {{"question": "Câu hỏi khởi động", "hint": "Gợi ý"}},
  "sections": [
    {{"title": "1. ...", "paragraphs": ["1–2 đoạn"], "bullets": [], "example": "", "note": ""}},
    {{"title": "2. ...", "paragraphs": ["1–2 đoạn"], "bullets": [], "example": "", "note": ""}}
  ],
  "diagram": {{"title": "Sơ đồ kiến thức", "nodes": ["3 đến 5 nút"]}},
  "terms": [{{"term": "Thuật ngữ", "definition": "Định nghĩa"}}],
  "summary": ["3 đến 5 ý ghi nhớ"],
  "quick_check": [
    {{"question": "Câu hỏi", "options": ["A", "B", "C", "D"], "answer_index": 0, "explanation": "Giải thích"}}
  ]
}}

Yêu cầu: đúng 3 câu quick_check, mỗi câu đúng 4 phương án và answer_index từ 0 đến 3.
Không Markdown, không code fence, không ghi chú ngoài JSON.
"""
    try:
        llm = AppServices.get_instance().llm
        raw_lesson = None
        try:
            raw_lesson = _biorag_invoke_structured_lesson(llm, prompt)
            generation_mode = "structured_output"
        except Exception as structured_error:
            logger.warning(
                "Lesson native structured output unavailable; using text fallback: %s",
                structured_error,
            )
            raw_text = _biorag_extract_message_text(llm.invoke(prompt))
            generation_mode = "llm_json"
            try:
                raw_lesson = _biorag_extract_lesson_json(raw_text)
            except Exception as first_parse_error:
                repair_prompt = f"""Hãy chuyển nội dung sau thành đúng một object JSON hợp lệ, không Markdown và không thêm kiến thức mới.
Phải giữ các khóa: title, topic, duration, objectives, content, warmup, sections, diagram, terms, summary, quick_check.
Mỗi quick_check có question, đúng 4 options, answer_index 0-3, explanation.

NỘI DUNG CẦN SỬA:
{raw_text[:16000]}
"""
                try:
                    raw_lesson = _biorag_extract_lesson_json(
                        _biorag_extract_message_text(llm.invoke(repair_prompt))
                    )
                    generation_mode = "repaired_json"
                except Exception as second_parse_error:
                    logger.warning(
                        "Lesson JSON remained invalid; starting editorial retry. first=%s second=%s",
                        first_parse_error,
                        second_parse_error,
                    )
                    generation_mode = "editorial_retry"

        lesson = None
        quality_issues = []
        if raw_lesson is not None:
            try:
                lesson = _biorag_normalize_generated_lesson(
                    raw_lesson, grade, number, topic, sources
                )
                quality_issues = _biorag_lesson_quality_issues(lesson, topic)
            except Exception as normalize_error:
                logger.warning("Lesson structure needs editorial retry: %s", normalize_error)
                quality_issues = [str(normalize_error)]

        if lesson is None or quality_issues:
            logger.info("Lesson editorial retry: issues=%s", quality_issues)
            editorial_prompt = _biorag_editorial_retry_prompt(
                grade, number, topic, context_blocks
            )
            try:
                try:
                    editorial_raw = _biorag_invoke_structured_lesson(
                        llm, editorial_prompt
                    )
                    generation_mode = "structured_editorial"
                except Exception as structured_editorial_error:
                    logger.warning(
                        "Lesson structured editorial unavailable; using text parser: %s",
                        structured_editorial_error,
                    )
                    editorial_raw = _biorag_extract_lesson_json(
                        _biorag_extract_message_text(llm.invoke(editorial_prompt))
                    )
                    generation_mode = "editorial_retry"
                lesson = _biorag_normalize_generated_lesson(
                    editorial_raw, grade, number, topic, sources
                )
                quality_issues = _biorag_lesson_quality_issues(lesson, topic)
            except Exception as editorial_error:
                logger.warning("Lesson editorial retry failed: %s", editorial_error)
                return jsonify({
                    "error": (
                        "Nguồn SGK đã đúng nhưng mô hình chưa biên tập được bản nháp "
                        "mạch lạc. Hãy bấm Tạo bản nháp lần nữa."
                    ),
                    "meta": {
                        "grade": grade,
                        "topic": topic,
                        "status": "rejected",
                        "quality_passed": False,
                    },
                }), 422

        if quality_issues:
            logger.warning("Lesson draft rejected by quality gate: %s", quality_issues)
            return jsonify({
                "error": (
                    "Bản nháp vẫn còn dấu hiệu OCR thô hoặc thiếu cấu trúc nên hệ thống "
                    "chưa cho phép lưu. Hãy thử tạo lại."
                ),
                "meta": {
                    "grade": grade,
                    "topic": topic,
                    "status": "rejected",
                    "quality_passed": False,
                    "quality_issues": quality_issues,
                },
            }), 422

        try:
            lesson["illustrations"] = _biorag_retrieve_lesson_images(
                topic, grade, lesson, sources, limit=4
            )
        except Exception as image_error:
            # Ảnh là phần bổ trợ: không làm hỏng một bản nháp văn bản đã đạt.
            logger.warning("Lesson illustration selection failed: %s", image_error)
            lesson["illustrations"] = []
        lesson["lesson_version"] = max(int(lesson.get("lesson_version") or 0), 4)
        lesson["draft_quality"] = {"passed": True, "issues": []}
        return jsonify({
            "lesson": lesson,
            "sources": lesson.get("generation_sources", []),
            "meta": {
                "grade": grade,
                "topic": topic,
                "status": "draft",
                "requires_teacher_review": True,
                "quality_passed": True,
                "generation_mode": generation_mode,
                "warning": (
                    "Bản nháp đã được biên tập lại từ đúng cụm trang SGK."
                    if generation_mode in {"editorial_retry", "structured_editorial"} else ""
                ),
            },
        }), 200
    except Exception as exc:
        logger.error("Lesson generation failed: %s", exc, exc_info=True)
        return jsonify({
            "error": "Chưa tạo được bản nháp hợp lệ. Hãy nhập chủ đề cụ thể hơn và thử lại."
        }), 500


@app.route('/api/learning/lessons', methods=['GET'])
def get_learning_lessons():
    """Danh sách bài học cho học sinh hoặc chế độ biên soạn của giáo viên."""
    grade_value = request.args.get("grade")
    include_inactive = request.args.get("include_inactive", "").strip().lower() in {
        "1", "true", "yes"
    }
    grade = None
    if grade_value not in (None, ""):
        try:
            grade = int(grade_value)
        except (TypeError, ValueError):
            return jsonify({"error": "Khối lớp không hợp lệ."}), 400
        if grade not in {6, 7, 8, 9}:
            return jsonify({"error": "Chỉ hỗ trợ lớp 6 đến lớp 9."}), 400
    try:
        lessons = list_lessons(grade=grade, include_inactive=include_inactive)
        source_inventory = _biorag_textbook_source_inventory()
        source_statuses = {
            str(item_grade): _biorag_textbook_source_status(item_grade)
            for item_grade in (6, 7, 8, 9)
        }
        return jsonify({
            "lessons": lessons,
            "meta": {
                "grade": grade,
                "count": len(lessons),
                "source_status": source_statuses.get(str(grade)) if grade else None,
                "source_statuses": source_statuses,
                "source_inventory": source_inventory,
            },
        }), 200
    except Exception as exc:
        logger.error("Learning catalog read failed: %s", exc, exc_info=True)
        return jsonify({
            "error": "Chưa đọc được danh sách bài học. Hãy kiểm tra learning_lessons.json."
        }), 500


@app.route('/api/learning/lessons/<lesson_id>/textbook-pages', methods=['GET'])
def get_learning_lesson_textbook_pages(lesson_id):
    """Chỉ xác minh trang SGK của bài đang mở; không làm chậm danh sách bài."""
    try:
        lesson = next(
            (item for item in list_lessons(include_inactive=True) if item.get("id") == lesson_id),
            None,
        )
        if lesson is None:
            return jsonify({"error": "Không tìm thấy bài học."}), 404
        source_status = _biorag_textbook_source_status(lesson.get("grade"))
        if not source_status.get("ready"):
            return jsonify({
                "error": source_status.get("message") or "Nguồn SGK chưa sẵn sàng.",
                "lesson_id": lesson_id,
                "source_status": source_status,
            }), 409
        gen_sources = lesson.get("generation_sources")
        if gen_sources and isinstance(gen_sources, list) and len(gen_sources) > 0:
            return jsonify({
                "lesson_id": lesson_id,
                "resolved_textbook_pages": gen_sources,
                "textbook_range": {
                    "start_page": gen_sources[0].get("page", 1),
                    "end_page": gen_sources[-1].get("page", 1),
                    "method": "generation_sources_verified",
                },
            }), 200
        resolved = _biorag_resolve_lesson_pdf_pages(lesson)
        if not resolved:
            return jsonify({
                "error": "Chưa xác minh được tiêu đề bài trong PDF.",
                "lesson_id": lesson_id,
            }), 422
        resolved_pdf_path = _biorag_lesson_pdf_path(lesson)
        return jsonify({
            "lesson_id": lesson_id,
            "resolved_textbook_pages": [
                (
                    _biorag_resolved_textbook_page_row(resolved_pdf_path, page)
                    if resolved_pdf_path else {"source": resolved["source"], "page": page}
                )
                for page in resolved["pages"]
            ],
            "textbook_range": {
                "start_page": resolved["start_page"],
                "end_page": resolved["end_page"],
                "method": resolved["method"],
            },
        }), 200
    except Exception as exc:
        logger.error("Lesson textbook page verification failed: %s", exc, exc_info=True)
        return jsonify({"error": "Không thể xác minh trang SGK của bài học."}), 500


@app.route('/api/learning/lessons/<lesson_id>/study-aids', methods=['GET'])
def get_learning_lesson_study_aids(lesson_id):
    """Trả về flashcard/sơ đồ tư duy đã tạo sẵn (cache) cho một bài học, nếu có."""
    try:
        cache = _biorag_load_study_aid_cache()
        return jsonify({"lesson_id": lesson_id, "study_aid": cache.get(lesson_id)}), 200
    except Exception as exc:
        logger.error("Study aid cache read failed for %s: %s", lesson_id, exc, exc_info=True)
        return jsonify({"error": "Chưa đọc được tài liệu ôn tập đã lưu."}), 500


@app.route('/api/learning/lessons/<lesson_id>/study-aids/generate', methods=['POST'])
def generate_learning_lesson_study_aids(lesson_id):
    """Sinh (hoặc sinh lại) flashcard + sơ đồ tư duy, bám đúng trang SGK thật của bài học."""
    try:
        lesson = next(
            (item for item in list_lessons(include_inactive=True) if item.get("id") == lesson_id),
            None,
        )
        if lesson is None:
            return jsonify({"error": "Không tìm thấy bài học."}), 404
        source_status = _biorag_textbook_source_status(lesson.get("grade"))
        if not source_status.get("ready"):
            return jsonify({
                "error": source_status.get("message") or "Nguồn SGK chưa sẵn sàng.",
            }), 409
        sources = _biorag_study_aid_context_sources(lesson)
    except LookupError as exc:
        return jsonify({"error": str(exc)}), 404
    except Exception as exc:
        logger.error(
            "Study aid context retrieval failed for %s: %s", lesson_id, exc, exc_info=True
        )
        return jsonify({"error": "Chưa truy xuất được dữ liệu SGK cho bài học này."}), 500

    try:
        study_aid = _biorag_generate_study_aid(lesson, sources)
    except Exception as exc:
        logger.error("Study aid generation failed for %s: %s", lesson_id, exc, exc_info=True)
        return jsonify({
            "error": "Chưa tạo được flashcard/sơ đồ tư duy hợp lệ. Hãy thử lại."
        }), 502

    study_aid["generated_at"] = datetime.now(timezone.utc).isoformat()
    deduped_sources = []
    seen_source_pages = set()
    for s in sources:
        key = (str(s.get("source") or "").lower(), str(s.get("page") or ""))
        if key in seen_source_pages:
            continue
        seen_source_pages.add(key)
        deduped_sources.append({"source": s["source"], "page": s["page"]})
    study_aid["sources"] = sorted(
        deduped_sources, key=lambda row: _biorag_lesson_page_number(row["page"]) or 0
    )
    try:
        cache = _biorag_load_study_aid_cache()
        cache[lesson_id] = study_aid
        _biorag_save_study_aid_cache(cache)
    except Exception as exc:
        logger.warning("Study aid cache write failed for %s: %s", lesson_id, exc)
    return jsonify({"lesson_id": lesson_id, "study_aid": study_aid}), 200


@app.route('/api/learning/lessons', methods=['POST'])
def add_learning_lesson():
    """Tạo bài học do giáo viên biên soạn."""
    data = request.get_json(silent=True) or {}
    if isinstance(data.get("generation_sources"), list) and data.get("generation_sources"):
        save_issues = _biorag_lesson_quality_issues(data, data.get("topic") or data.get("title") or "")
        if save_issues:
            return jsonify({
                "error": "Bản nháp còn câu bị cắt hoặc thiếu cấu trúc nên chưa thể lưu.",
                "quality_issues": save_issues,
            }), 422
    try:
        lesson = create_lesson(data)
        return jsonify({"lesson": lesson}), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        logger.error("Learning lesson create failed: %s", exc, exc_info=True)
        return jsonify({"error": "Không thể lưu bài học mới."}), 500


@app.route('/api/learning/lessons/<lesson_id>', methods=['PUT'])
def edit_learning_lesson(lesson_id):
    """Cập nhật bài học hệ thống hoặc bài do giáo viên tạo."""
    data = request.get_json(silent=True) or {}
    if isinstance(data.get("generation_sources"), list) and data.get("generation_sources"):
        save_issues = _biorag_lesson_quality_issues(data, data.get("topic") or data.get("title") or "")
        if save_issues:
            return jsonify({
                "error": "Bản nháp còn câu bị cắt hoặc thiếu cấu trúc nên chưa thể lưu.",
                "quality_issues": save_issues,
            }), 422
    try:
        lesson = update_lesson(lesson_id, data)
        return jsonify({"lesson": lesson}), 200
    except KeyError:
        return jsonify({"error": "Không tìm thấy bài học cần cập nhật."}), 404
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        logger.error("Learning lesson update failed: %s", exc, exc_info=True)
        return jsonify({"error": "Không thể cập nhật bài học."}), 500


@app.route('/api/learning/lessons/<lesson_id>/export-5512', methods=['GET'])
def export_learning_lesson_plan_5512(lesson_id):
    """Xuất Kế hoạch bài dạy chuẩn Công văn 5512/BGDĐT-GDTrH ra file Word (.docx)."""
    try:
        from src.app.plan_5512_builder import build_lesson_plan_5512_bytes
        lesson = next(
            (item for item in list_lessons(include_inactive=True) if str(item.get("id") or "").strip() == str(lesson_id or "").strip()),
            None,
        )
        if lesson is None:
            return jsonify({"error": f"Không tìm thấy bài học có mã '{lesson_id}'."}), 404

        buffer = build_lesson_plan_5512_bytes(lesson)
        grade = lesson.get("grade") or 6
        raw_title = str(lesson.get("title") or "Bai_hoc")
        title_slug = re.sub(r"[^\w\d_-]+", "_", raw_title).strip("_")[:40]
        filename = f"Giao_an_5512_KHTN{grade}_{title_slug}.docx"

        return send_file(
            buffer,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            as_attachment=True,
            download_name=filename,
        )
    except Exception as exc:
        logger.error("Export lesson plan 5512 failed for %s: %s", lesson_id, exc, exc_info=True)
        return jsonify({"error": f"Không thể xuất giáo án 5512: {str(exc)}"}), 500


@app.route('/api/learning/export-5512', methods=['POST'])
def export_custom_lesson_plan_5512():
    """Xuất Kế hoạch bài dạy chuẩn Công văn 5512 từ bản nháp bài học do giáo viên biên soạn."""
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict) or not data:
        return jsonify({"error": "Dữ liệu bài học không hợp lệ."}), 400
    try:
        from src.app.plan_5512_builder import build_lesson_plan_5512_bytes
        buffer = build_lesson_plan_5512_bytes(data)
        grade = data.get("grade") or 6
        raw_title = str(data.get("title") or "Bai_hoc")
        title_slug = re.sub(r"[^\w\d_-]+", "_", raw_title).strip("_")[:40]
        filename = f"Giao_an_5512_KHTN{grade}_{title_slug}.docx"

        return send_file(
            buffer,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            as_attachment=True,
            download_name=filename,
        )
    except Exception as exc:
        logger.error("Export custom lesson plan 5512 failed: %s", exc, exc_info=True)
        return jsonify({"error": f"Không thể xuất giáo án 5512: {str(exc)}"}), 500


@app.route('/api/exam/lessons/<lesson_id>/export-3280', methods=['GET'])
def export_lesson_exam_package_3280(lesson_id):
    """Xuất trọn bộ Đề kiểm tra chuẩn Ma trận & Bản đặc tả (Công văn 3280) từ bài học ra Word."""
    try:
        from src.app.exam_3280_builder import build_exam_package_3280_bytes, lesson_to_exam_data
        lesson = next(
            (item for item in list_lessons(include_inactive=True) if str(item.get("id") or "").strip() == str(lesson_id or "").strip()),
            None,
        )
        if lesson is None:
            return jsonify({"error": f"Không tìm thấy bài học có mã '{lesson_id}'."}), 404

        exam_type = request.args.get("exam_type", "ĐỊNH KỲ").strip()
        try:
            duration = int(request.args.get("duration", 45))
        except (TypeError, ValueError):
            duration = 45

        exam_data = lesson_to_exam_data(lesson, exam_type=exam_type, duration=duration)
        buffer = build_exam_package_3280_bytes(exam_data)
        grade = lesson.get("grade") or 6
        raw_title = str(lesson.get("title") or "Bai_hoc")
        title_slug = re.sub(r"[^\w\d_-]+", "_", raw_title).strip("_")[:40]
        filename = f"De_kiem_tra_3280_KHTN{grade}_{title_slug}.docx"

        return send_file(
            buffer,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            as_attachment=True,
            download_name=filename,
        )
    except Exception as exc:
        logger.error("Export lesson exam 3280 failed for %s: %s", lesson_id, exc, exc_info=True)
        return jsonify({"error": f"Không thể xuất đề kiểm tra 3280: {str(exc)}"}), 500


@app.route('/api/exam/generate-3280', methods=['POST'])
def generate_exam_package_3280():
    """Tạo bộ dữ liệu Đề kiểm tra + Ma trận + Bản đặc tả theo Công văn 3280 từ chủ đề."""
    data = request.get_json(silent=True) or {}
    try:
        grade = int(data.get("grade", 6))
    except (TypeError, ValueError):
        grade = 6
    if grade not in {6, 7, 8, 9}:
        return jsonify({"error": "Chỉ hỗ trợ Khoa học tự nhiên lớp 6 đến lớp 9."}), 400

    topic = str(data.get("topic", "")).strip()
    if len(topic) < 2:
        return jsonify({"error": "Vui lòng nhập chủ đề kiểm tra."}), 400

    exam_type = str(data.get("exam_type", "ĐỊNH KỲ")).strip()
    try:
        duration = int(data.get("duration", 45))
    except (TypeError, ValueError):
        duration = 45

    try:
        count = int(data.get("count", 40))
        if count not in {5, 8, 10, 15, 20, 28, 40} and not (3 <= count <= 60):
            count = 40
    except (TypeError, ValueError):
        count = 40

    try:
        from src.app.exam_3280_builder import lesson_to_exam_data
        matching_lesson = next(
            (l for l in list_lessons(include_inactive=True) if l.get("grade") == grade and (topic.lower() in (l.get("topic", "").lower() + " " + l.get("title", "").lower()))),
            None
        )
        if matching_lesson:
            exam_data = lesson_to_exam_data(matching_lesson, exam_type=exam_type, duration=duration, target_mcq_count=count)
            return jsonify({"exam": exam_data, "exam_data": exam_data}), 200

        sources = _biorag_load_quiz_context(grade, topic, count)
        context_blocks = [
            f"[NGUỒN {idx} | {s['source']} | trang {s['page']}]\n{s['text']}"
            for idx, s in enumerate(sources, start=1)
        ]

        mcq_score = 0.25 if count >= 20 else 0.5
        mcq_total = round(count * mcq_score, 1)
        tl_total = max(0.0, round(10.0 - mcq_total, 1))
        essay_count = 0 if count >= 40 else (2 if tl_total >= 1.0 else 0)

        prompt = f"""Bạn là giáo viên Khoa học tự nhiên THCS Việt Nam.
Hãy biên soạn dữ liệu cho ĐỀ KIỂM TRA ĐỊNH KỲ CHUẨN CÔNG VĂN 3280/BGDĐT-GDTrH lớp {grade} về chủ đề: {topic}.
Thời gian làm bài: {duration} phút. Tỷ lệ: {int(mcq_total * 10)}% Trắc nghiệm ({count} câu x {mcq_score}đ = {mcq_total:.1f}đ) + {int(tl_total * 10)}% Tự luận ({essay_count} câu = {tl_total:.1f}đ).

Chỉ sử dụng kiến thức trong NGỮ LIỆU SGK KNTT bên dưới:
{chr(10).join(context_blocks)}

Trả về duy nhất 1 JSON object hợp lệ (không Markdown, không code block) theo cấu trúc:
{{
  "title": "ĐỀ KIỂM TRA {exam_type.upper()} MÔN KHOA HỌC TỰ NHIÊN {grade}",
  "topic": "{topic}",
  "duration_minutes": {duration},
  "multiple_choice": [
    {{
      "id": 1,
      "level": "NB",
      "question": "Nội dung câu hỏi nhận biết?",
      "options": ["A. Lựa chọn 1", "B. Lựa chọn 2", "C. Lựa chọn 3", "D. Lựa chọn 4"],
      "answer_key": "A",
      "score": {mcq_score},
      "explanation": "Giải thích ngắn dựa trên SGK"
    }}
  ],
  "essay": [
    {{
      "id": 1,
      "level": "VD",
      "question": "Nội dung câu hỏi tự luận vận dụng giải thích hiện tượng?",
      "score": {round(tl_total / 2, 1) if tl_total else 0.0},
      "rubric": [
        {{"step": "Ý 1 lời giải", "score": {round(tl_total / 4, 2) if tl_total else 0.0}}},
        {{"step": "Ý 2 lời giải", "score": {round(tl_total / 4, 2) if tl_total else 0.0}}}
      ]
    }}
  ] if {essay_count} > 0 else [],
  "spec_rows": [
    {{
      "stt": 1,
      "topic": "{topic}",
      "level": "Nhận biết",
      "requirement": "Yêu cầu cần đạt chuẩn GDPT 2018",
      "question_type": "{round(count * 0.4)} TNKQ",
      "question_refs": "Câu 1 - {round(count * 0.4)}"
    }}
  ]
}}
Yêu cầu: Đúng {count} câu multiple_choice, mỗi câu 4 phương án A-D{f', đúng {essay_count} câu essay kèm rubric chi tiết' if essay_count > 0 else ''}."""

        try:
            llm = AppServices.get_instance().llm
            resp = llm.invoke(prompt)
            raw_text = _biorag_extract_message_text(resp)
            json_match = re.search(r'\{[\s\S]*\}', raw_text)
            if json_match:
                parsed = json.loads(json_match.group(0))
                parsed["grade"] = grade
                parsed["school_name"] = "TRƯỜNG THCS HUỲNH BÁ CHÁNH"
                parsed["department"] = "TỔ: KHOA HỌC TỰ NHIÊN"
                parsed["school_year"] = "2025 - 2026"
                parsed["semester"] = "HỌC KỲ I"
                parsed["exam_type"] = exam_type
                # Ensure full question count via lesson_to_exam_data
                parsed_mcq = parsed.get("multiple_choice") or []
                if len(parsed_mcq) < count:
                    parsed = lesson_to_exam_data(parsed, exam_type=exam_type, duration=duration, target_mcq_count=count)
                return jsonify({"exam": parsed, "exam_data": parsed}), 200
        except Exception as llm_err:
            logger.warning("Exam LLM generation failed, falling back to lesson synthesis: %s", llm_err)

        fallback_lesson = {
            "grade": grade,
            "title": topic,
            "topic": topic,
            "objectives": [f"Nắm vững kiến thức trọng tâm về {topic}"],
            "sections": [{"title": topic, "paragraphs": [sources[0]["text"][:200]] if sources else [""]}],
            "quick_check": []
        }
        exam_data = lesson_to_exam_data(fallback_lesson, exam_type=exam_type, duration=duration, target_mcq_count=count)
        return jsonify({"exam": exam_data, "exam_data": exam_data}), 200

    except Exception as exc:
        logger.error("Exam 3280 generation failed: %s", exc, exc_info=True)
        return jsonify({"error": f"Không thể tạo đề kiểm tra: {str(exc)}"}), 500


@app.route('/api/exam/export-3280', methods=['POST'])
def export_custom_exam_package_3280():
    """Xuất Đề kiểm tra chuẩn Ma trận & Bản đặc tả 3280 từ dữ liệu JSON do giáo viên gửi lên."""
    data = request.get_json(silent=True) or {}
    if not isinstance(data, dict) or not data:
        return jsonify({"error": "Dữ liệu đề kiểm tra không hợp lệ."}), 400
    try:
        from src.app.exam_3280_builder import build_exam_package_3280_bytes, lesson_to_exam_data
        if "matrix_rows" not in data or "spec_rows" not in data or ("objectives" in data or "sections" in data or "content" in data):
            data = lesson_to_exam_data(data)
        buffer = build_exam_package_3280_bytes(data)
        grade = data.get("grade") or 6
        raw_title = str(data.get("topic") or data.get("title") or "KHTN")
        title_slug = re.sub(r"[^\w\d_-]+", "_", raw_title).strip("_")[:40]
        code_tag = f"MaDe{data.get('exam_code')}_" if data.get('exam_code') else ""
        filename = f"De_kiem_tra_3280_{code_tag}KHTN{grade}_{title_slug}.docx"

        return send_file(
            buffer,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            as_attachment=True,
            download_name=filename,
        )
    except Exception as exc:
        logger.error("Export exam 3280 failed: %s", exc, exc_info=True)
        return jsonify({"error": f"Không thể xuất đề kiểm tra 3280: {str(exc)}"}), 500


@app.route('/api/quiz/generate', methods=['POST'])
def generate_knowledge_quiz():
    """Tạo đề trắc nghiệm KNTT theo lớp và chủ đề, kèm nguồn đã xác thực."""
    data = request.get_json(silent=True) or {}
    topic = str(data.get("topic", "")).strip()
    difficulty_mode = str(data.get("difficulty", "balanced")).strip().lower()
    try:
        grade = int(data.get("grade", 9))
        count = int(data.get("count", 5))
    except (TypeError, ValueError):
        return jsonify({"error": "Lớp hoặc số câu không hợp lệ."}), 400

    if grade not in {6, 7, 8, 9}:
        return jsonify({"error": "Chỉ hỗ trợ Khoa học tự nhiên lớp 6 đến lớp 9."}), 400
    if count not in {5, 10, 15, 20, 28, 40} and not (3 <= count <= 40):
        return jsonify({"error": "Số câu phải từ 3 đến 40 câu (chuẩn 5, 10, 15, 20, 28, 40 câu)."}), 400
    if difficulty_mode not in {"basic", "balanced", "advanced"}:
        return jsonify({"error": "Mức độ đề không hợp lệ."}), 400
    if len(topic) < 2:
        return jsonify({"error": "Hãy nhập chủ đề muốn kiểm tra."}), 400
    if len(topic) > 300:
        return jsonify({"error": "Chủ đề vượt quá giới hạn 300 ký tự."}), 413

    lesson_scope = _biorag_chat_lesson_scope(topic, grade)
    try:
        sources = _biorag_load_quiz_context(grade, topic, count)
    except LookupError as exc:
        return jsonify({"error": str(exc)}), 404
    except Exception as exc:
        logger.error("Quiz context retrieval failed: %s", exc, exc_info=True)
        return jsonify({
            "error": "Chưa đọc được dữ liệu SGK KNTT. Hãy kiểm tra database_kntt và thử lại."
        }), 500

    context_blocks = []
    for index, source in enumerate(sources, start=1):
        context_blocks.append(
            f"[NGUỒN {index} | {source['source']} | trang {source['page']}]\n{source['text']}"
        )
    difficulty_mode, difficulty_label, nb_count, th_count, vd_count = _biorag_quiz_difficulty_plan(
        difficulty_mode, count
    )
    prompt = f"""Bạn là giáo viên Khoa học tự nhiên Việt Nam.
Hãy tạo đúng {count} câu trắc nghiệm để kiểm tra học sinh lớp {grade} về chủ đề: {topic}.
Chỉ sử dụng dữ kiện trong NGỮ LIỆU SGK bên dưới, không bổ sung kiến thức ngoài nguồn.

NGỮ LIỆU SGK:
{chr(10).join(context_blocks)}

Yêu cầu chất lượng:
- Mỗi câu có đúng 4 lựa chọn, chỉ 1 đáp án đúng.
- Câu hỏi rõ ràng, không lặp ý; mức đề: {difficulty_label}.
- Phân bố chính xác: {nb_count} câu NB (nhận biết), {th_count} câu TH (thông hiểu), {vd_count} câu VD (vận dụng).
- Phương án nhiễu hợp lý nhưng không đánh đố và không dùng kiểu "tất cả đều đúng".
- Giải thích ngắn, chỉ ra vì sao đáp án đúng dựa trên nguồn.
- source_id là số NGUỒN chứa căn cứ chính.
- Bằng chứng phải sao chép nguyên văn một đoạn liên tiếp 4-18 từ trong đúng NGUỒN đã chọn.
- Đáp án đúng phải xuất hiện hoặc được khẳng định trực tiếp trong bằng chứng.
- Không biến danh sách ví dụ thành số lượng đầy đủ. Không khẳng định ánh sáng trắng chỉ có bảy màu.

Mỗi câu phải nằm trọn trên đúng một dòng theo mẫu sau, dùng chính xác dấu phân cách ||:
Q||NB||Câu hỏi||Lựa chọn A||Lựa chọn B||Lựa chọn C||Lựa chọn D||B||Giải thích||1||Bằng chứng nguyên văn từ SGK

Trường thứ hai chỉ được là NB, TH hoặc VD. Trường sau lựa chọn D là đáp án A-D.
Trường gần cuối là source_id; trường cuối là bằng chứng nguyên văn, không chứa dấu ||.
Không trả JSON, không Markdown, không đánh số dòng, không xuống dòng bên trong một câu.
"""

    try:
        llm = AppServices.get_instance().llm
        response = llm.invoke(prompt)
        raw_quiz = _biorag_extract_message_text(response)
        parsed_questions = _biorag_parse_quiz_lines(raw_quiz, count, sources)
        if not parsed_questions:
            try:
                parsed_questions = _biorag_parse_quiz_payload(raw_quiz, count, sources, require_count=False)
            except Exception:
                parsed_questions = []
        questions = _biorag_filter_grounded_questions(parsed_questions, sources)
        if len(questions) < count:
            logger.warning(
                "Quiz output needs grounded repair: accepted %s/%s questions", len(questions), count
            )
            repair_prompt = f"""Hãy tạo lại đúng {count} câu trắc nghiệm lớp {grade}, chủ đề {topic}, mức {difficulty_label}.
Chỉ dùng NGỮ LIỆU SGK bên dưới. Phân bố: {nb_count} NB, {th_count} TH, {vd_count} VD.
Mỗi dòng dùng chính xác mẫu:
Q||NB||Câu hỏi||Lựa chọn A||Lựa chọn B||Lựa chọn C||Lựa chọn D||B||Giải thích||1||Bằng chứng nguyên văn từ SGK
Bằng chứng phải là 4-18 từ liên tiếp sao chép nguyên văn từ đúng nguồn và phải trực tiếp hỗ trợ đáp án.
Không biến danh sách ví dụ thành số lượng đầy đủ. Không khẳng định ánh sáng trắng chỉ có bảy màu.
Không JSON, không Markdown, không đánh số, không xuống dòng bên trong một câu.

NGỮ LIỆU SGK:
{chr(10).join(context_blocks)}
"""
            repaired_response = llm.invoke(repair_prompt)
            repaired_text = _biorag_extract_message_text(repaired_response)
            repaired_questions = _biorag_filter_grounded_questions(
                _biorag_parse_quiz_lines(repaired_text, count, sources), sources
            )
            existing = {item["question"].strip().lower() for item in questions}
            for item in repaired_questions:
                normalized = item["question"].strip().lower()
                if normalized not in existing:
                    item["id"] = len(questions) + 1
                    questions.append(item)
                    existing.add(normalized)
                if len(questions) >= count:
                    break

        if len(questions) < count:
            # 1. Backfill from parsed_questions that were well-formed (has question, 4 options, valid answer_index)
            existing = {item["question"].strip().lower() for item in questions}
            all_candidates = (parsed_questions or [])
            for candidate in all_candidates:
                c_text = str(candidate.get("question") or "").strip()
                norm_c = c_text.lower()
                opts = candidate.get("options") or []
                ans_idx = candidate.get("answer_index")
                if norm_c and norm_c not in existing and len(opts) == 4 and isinstance(ans_idx, int) and 0 <= ans_idx < 4:
                    candidate["id"] = len(questions) + 1
                    if not candidate.get("evidence") and sources:
                        candidate["evidence"] = sources[0]["text"][:120]
                    questions.append(candidate)
                    existing.add(norm_c)
                    if len(questions) >= count:
                        break

            # 2. If still < count, synthesize remaining questions from curriculum textbook synthesis
            if len(questions) < count:
                try:
                    from src.app.exam_3280_builder import lesson_to_exam_data
                    synth_data = lesson_to_exam_data({
                        "grade": grade,
                        "topic": topic,
                        "title": topic,
                        "multiple_choice": questions
                    }, target_mcq_count=count)
                    synth_mcqs = synth_data.get("multiple_choice") or []
                    labels = ["A", "B", "C", "D"]
                    for sq in synth_mcqs:
                        sq_text = str(sq.get("question") or "").strip()
                        norm_sq = sq_text.lower()
                        if norm_sq and norm_sq not in existing:
                            ans_key = str(sq.get("answer_key") or "A").strip().upper()
                            a_idx = labels.index(ans_key) if ans_key in labels else 0
                            clean_opts = [re.sub(r'^[A-D][\.\:\)]\s*', '', str(o)) for o in (sq.get("options") or [])]
                            questions.append({
                                "id": len(questions) + 1,
                                "question": sq_text,
                                "options": clean_opts,
                                "answer_index": a_idx,
                                "explanation": sq.get("explanation") or f"Kiến thức {topic} theo SGK KHTN {grade}.",
                                "difficulty": "Vận dụng" if sq.get("level") in ("VD", "VDC") else ("Thông hiểu" if sq.get("level") == "TH" else "Nhận biết"),
                                "evidence": sources[0]["text"][:120] if sources else f"Nội dung chuẩn trong SGK KHTN {grade}.",
                                "source": sources[0]["source"] if sources else f"SGK KHTN {grade}",
                                "page": sources[0]["page"] if sources else 1
                            })
                            existing.add(norm_sq)
                            if len(questions) >= count:
                                break
                except Exception as synth_err:
                    logger.warning("Synthesis backfill for quiz failed: %s", synth_err)

        if len(questions) < 3:
            raise ValueError("Mô hình chưa tạo đủ câu hỏi hợp lệ sau khi sửa.")
        return jsonify({
            "questions": questions,
            "meta": {
                "grade": grade, "topic": topic, "count": len(questions),
                "requested_count": count, "partial": len(questions) < count,
                "lesson_id": lesson_scope.get("lesson_id") if lesson_scope else None,
                "lesson_scope": lesson_scope.get("method") if lesson_scope else None,
                "difficulty": difficulty_mode, "difficulty_label": difficulty_label,
                "warning": (
                    f"Đã tạo {len(questions)}/{count} câu có đủ bằng chứng SGK; "
                    "các câu chưa đạt đã được loại bỏ."
                    if len(questions) < count else ""
                ),
            },
        }), 200
    except Exception as exc:
        logger.error("Quiz generation failed: %s", exc, exc_info=True)
        return jsonify({
            "error": "Chưa tạo được đề có đủ bằng chứng SGK. Hãy thử lại hoặc giảm xuống 5 câu.",
            "meta": {"connection_ok": True, "grade": grade, "topic": topic},
        }), 422


_BIORAG_QUIZ_ANALYSIS_SUMMARY_RE = re.compile(r"#{2,}\s*TONGQUAN\s*#{2,}", re.IGNORECASE)
_BIORAG_QUIZ_ANALYSIS_GROUP_RE = re.compile(r"#{2,}\s*NHOM\s*(\d+)\s*#{2,}", re.IGNORECASE)


def _biorag_parse_quiz_analysis_text(raw_text, group_count):
    """Phân tích văn bản thuần theo mốc ###TONGQUAN###/###NHOMn### — tránh JSON dễ vỡ (bài học từ tính năng flashcard)."""
    text = str(raw_text or "").replace("\r\n", "\n").replace("\r", "\n")
    markers = []
    summary_match = _BIORAG_QUIZ_ANALYSIS_SUMMARY_RE.search(text)
    if summary_match:
        markers.append(("summary", summary_match.start(), summary_match.end()))
    for match in _BIORAG_QUIZ_ANALYSIS_GROUP_RE.finditer(text):
        markers.append((int(match.group(1)), match.start(), match.end()))
    markers.sort(key=lambda row: row[1])
    blocks = {}
    for index, (key, _start, end) in enumerate(markers):
        next_start = markers[index + 1][1] if index + 1 < len(markers) else len(text)
        blocks[key] = text[end:next_start].strip()
    summary = blocks.get("summary", "").strip()
    tips = [blocks.get(i + 1, "").strip() for i in range(group_count)]
    return summary, tips


def _biorag_analyze_quiz_mistakes(grade, topic, wrong_items):
    """Nhóm câu sai theo bài học (best-effort qua _biorag_chat_lesson_scope), rồi nhờ LLM viết nhận xét
    bằng định dạng văn bản thuần (không JSON) cho từng nhóm đã xác định sẵn ở phía server."""
    groups = []
    group_by_key = {}
    for item in wrong_items:
        question_text = str(item.get("question") or "").strip()
        scope = None
        if question_text:
            try:
                scope = _biorag_chat_lesson_scope(question_text, grade)
            except Exception as exc:
                logger.warning("Lesson scope resolution failed for mistake analysis: %s", exc)
                scope = None
        if scope and scope.get("lesson_id"):
            key = ("lesson", scope["lesson_id"])
        else:
            source_label = str(item.get("source") or "SGK").strip() or "SGK"
            key = ("source", source_label.lower())
        if key not in group_by_key:
            group_by_key[key] = {
                "key": key,
                "lesson_id": scope.get("lesson_id") if scope else None,
                "grade": scope.get("grade") if scope else grade,
                "label": (str(item.get("source") or "SGK").strip() or "SGK") if key[0] == "source" else None,
                "items": [],
            }
            groups.append(group_by_key[key])
        group_by_key[key]["items"].append(item)

    try:
        all_lessons = list_lessons(include_inactive=True)
    except Exception:
        all_lessons = []
    lessons_by_id = {lesson.get("id"): lesson for lesson in all_lessons if isinstance(lesson, dict)}
    for group in groups:
        if group["lesson_id"] and not group["label"]:
            lesson = lessons_by_id.get(group["lesson_id"])
            if lesson:
                number = _biorag_lesson_number(lesson)
                title = lesson.get("title") or lesson.get("topic") or ""
                group["label"] = (f"Bài {number}: {title}" if number else title) or "Bài học liên quan"
            else:
                group["label"] = "Bài học liên quan"

    context_blocks = []
    for index, group in enumerate(groups, start=1):
        lines = [f"Nhóm {index}: {group['label']} ({len(group['items'])} câu sai)"]
        for item in group["items"][:6]:
            options = item.get("options") or []
            chosen_index = item.get("chosen_index")
            answer_index = item.get("answer_index")
            chosen_text = (
                options[chosen_index]
                if isinstance(chosen_index, int) and 0 <= chosen_index < len(options)
                else "(bỏ trống)"
            )
            correct_text = (
                options[answer_index]
                if isinstance(answer_index, int) and 0 <= answer_index < len(options)
                else ""
            )
            lines.append(f"- Câu: {item.get('question', '')} | Học sinh chọn: {chosen_text} | Đáp án đúng: {correct_text}")
        context_blocks.append("\n".join(lines))

    total_wrong = len(wrong_items)
    prompt = f"""Bạn là giáo viên Khoa học tự nhiên Việt Nam, đang nhận xét bài kiểm tra của một học sinh lớp {grade}
về chủ đề "{topic}". Học sinh đã làm sai tổng cộng {total_wrong} câu, được nhóm sẵn theo nội dung bên dưới.

{chr(10).join(context_blocks)}

Yêu cầu:
- Viết một đoạn TỔNG QUAN ngắn (2-3 câu), giọng động viên, chỉ ra học sinh còn yếu ở đâu, không liệt kê lại từng câu.
- Với MỖI nhóm ở trên, viết một đoạn NHẬN XÉT ngắn (2-3 câu) giải thích khái niệm học sinh còn nhầm lẫn và gợi ý cách ôn tập cụ thể.
- Không dùng JSON, không dùng Markdown, không đánh số danh sách, không thêm dấu ngoặc kép quanh nội dung.
- Trả lời đúng định dạng dưới đây, thay <...> bằng nội dung, giữ nguyên các dòng mốc ###...###:

###TONGQUAN###
<đoạn tổng quan>
###NHOM1###
<nhận xét cho nhóm 1>
"""
    if len(groups) > 1:
        for group_index in range(2, len(groups) + 1):
            prompt += f"###NHOM{group_index}###\n<nhận xét cho nhóm {group_index}>\n"

    llm = AppServices.get_instance().llm
    raw_text = _biorag_extract_message_text(llm.invoke(prompt))
    summary, tips = _biorag_parse_quiz_analysis_text(raw_text, len(groups))
    if not summary or any(not tip for tip in tips):
        try:
            raw_text_retry = _biorag_extract_message_text(llm.invoke(prompt))
            summary_retry, tips_retry = _biorag_parse_quiz_analysis_text(raw_text_retry, len(groups))
            if not summary and summary_retry:
                summary = summary_retry
            for index, tip in enumerate(tips_retry):
                if tip and not tips[index]:
                    tips[index] = tip
        except Exception as exc:
            logger.warning("Quiz mistake analysis retry failed: %s", exc)
    if not summary:
        summary = (
            f"Bạn đã làm sai {total_wrong} câu, tập trung ở {len(groups)} nội dung dưới đây. "
            "Hãy ôn lại các bài liên quan rồi luyện tập thêm."
        )

    weak_topics = []
    for group, tip in zip(groups, tips):
        weak_topics.append({
            "label": group["label"],
            "lesson_id": group["lesson_id"],
            "grade": group["grade"],
            "count": len(group["items"]),
            "tip": tip or "Hãy đọc lại nội dung SGK liên quan và làm thêm flashcard để củng cố.",
        })
    weak_topics.sort(key=lambda row: row["count"], reverse=True)
    return {"summary": summary, "weak_topics": weak_topics}


@app.route('/api/quiz/analyze-mistakes', methods=['POST'])
def analyze_quiz_mistakes():
    """Phân tích câu trả lời sai ngay sau khi nộp bài — không lưu lịch sử, chỉ trả kết quả tức thời cho client."""
    data = request.get_json(silent=True) or {}
    try:
        grade = int(data.get("grade", 7))
    except (TypeError, ValueError):
        return jsonify({"error": "Khối lớp không hợp lệ."}), 400
    if grade not in {6, 7, 8, 9}:
        return jsonify({"error": "Chỉ hỗ trợ Khoa học tự nhiên lớp 6 đến lớp 9."}), 400
    topic = str(data.get("topic", "")).strip()[:300] or "bài kiểm tra"

    raw_items = data.get("wrong_questions")
    if not isinstance(raw_items, list) or not raw_items:
        return jsonify({"error": "Không có câu sai nào để phân tích."}), 400
    raw_items = raw_items[:40]

    wrong_items = []
    for raw in raw_items:
        if not isinstance(raw, dict):
            continue
        question = str(raw.get("question") or "").strip()[:1000]
        if not question:
            continue
        options = raw.get("options")
        options = [str(option)[:500] for option in options[:4]] if isinstance(options, list) else []
        try:
            chosen_index = int(raw.get("chosen_index")) if raw.get("chosen_index") is not None else None
        except (TypeError, ValueError):
            chosen_index = None
        try:
            answer_index = int(raw.get("answer_index")) if raw.get("answer_index") is not None else None
        except (TypeError, ValueError):
            answer_index = None
        wrong_items.append({
            "question": question,
            "options": options,
            "chosen_index": chosen_index,
            "answer_index": answer_index,
            "source": str(raw.get("source") or "")[:200],
        })
    if not wrong_items:
        return jsonify({"error": "Dữ liệu câu sai không hợp lệ."}), 400

    try:
        result = _biorag_analyze_quiz_mistakes(grade, topic, wrong_items)
    except Exception as exc:
        logger.error("Quiz mistake analysis failed: %s", exc, exc_info=True)
        return jsonify({"error": "Chưa phân tích được bài làm. Hãy thử lại."}), 502
    return jsonify(result), 200


@app.route('/api/quiz/bank', methods=['GET'])
def get_curated_quiz_bank_api():
    """Lấy danh mục các bài thi trắc nghiệm mẫu có sẵn theo khối lớp."""
    try:
        from src.app.curated_quizzes import get_curated_exams_by_grade
        grade_arg = request.args.get('grade')
        grade = int(grade_arg) if grade_arg and grade_arg.isdigit() else None
        exams = get_curated_exams_by_grade(grade)
        include_questions = request.args.get('include_questions', 'false').lower() in {'true', '1'}
        result = []
        for e in exams:
            item = {
                "id": e["id"],
                "grade": e["grade"],
                "type": e["type"],
                "type_label": e["type_label"],
                "title": e["title"],
                "topic": e["topic"],
                "duration_minutes": e["duration_minutes"],
                "questions_count": e["questions_count"],
                "description": e.get("description", ""),
                "user_uploaded": e.get("user_uploaded", False),
                "badge": e.get("badge", ""),
            }
            if include_questions:
                item["questions"] = e["questions"]
            result.append(item)
        return jsonify({"exams": result, "total": len(result)}), 200
    except Exception as exc:
        logger.error("Get quiz bank failed: %s", exc, exc_info=True)
        return jsonify({"error": f"Không thể lấy ngân hàng đề: {str(exc)}"}), 500


@app.route('/api/quiz/bank/<exam_id>', methods=['GET'])
def get_curated_exam_detail_api(exam_id):
    """Lấy toàn bộ câu hỏi và đáp án của một bài thi trắc nghiệm mẫu."""
    try:
        from src.app.curated_quizzes import get_curated_exam_by_id
        exam = get_curated_exam_by_id(exam_id)
        if not exam:
            return jsonify({"error": f"Không tìm thấy đề thi với mã: {exam_id}"}), 404
        return jsonify(exam), 200
    except Exception as exc:
        logger.error("Get exam detail failed: %s", exc, exc_info=True)
        return jsonify({"error": f"Không thể lấy chi tiết đề thi: {str(exc)}"}), 500


@app.route('/api/quiz/upload', methods=['POST'])
def upload_quiz_api():
    """Nhận tệp đề thi (Word .docx, Text .txt, .json) hoặc văn bản dán trực tiếp và bóc tách thành câu hỏi."""
    try:
        from src.app.exam_upload_parser import extract_text_from_docx, parse_exam_text

        raw_text = ""
        grade = request.form.get('grade') or (request.json.get('grade') if request.is_json else None)
        duration = request.form.get('duration') or (request.json.get('duration') if request.is_json else None)
        title = request.form.get('title') or (request.json.get('title') if request.is_json else None)

        grade = int(grade) if grade and str(grade).isdigit() else 7
        duration = int(duration) if duration and str(duration).isdigit() else 15
        title = str(title).strip() if title else ""

        # Trường hợp 1: Tải lên tệp (Multipart file)
        if 'file' in request.files:
            file = request.files['file']
            filename = file.filename.lower() if file.filename else ""
            file_bytes = file.read()

            if filename.endswith('.docx'):
                raw_text = extract_text_from_docx(file_bytes)
            elif filename.endswith('.json'):
                try:
                    data = json.loads(file_bytes.decode('utf-8', errors='replace'))
                    if isinstance(data, dict) and "questions" in data:
                        return jsonify(data), 200
                except Exception:
                    pass
                raw_text = file_bytes.decode('utf-8', errors='replace')
            else:
                raw_text = file_bytes.decode('utf-8', errors='replace')

        # Trường hợp 2: Dán văn bản thô (JSON hoặc Form data)
        elif request.is_json and request.json.get('raw_text'):
            raw_text = request.json.get('raw_text', '')
        elif request.form.get('raw_text'):
            raw_text = request.form.get('raw_text', '')

        if not raw_text.strip():
            return jsonify({"error": "Không nhận được nội dung đề thi. Vui lòng tải file Word (.docx), file Text hoặc dán nội dung đề."}), 400

        parsed_exam = parse_exam_text(raw_text, default_grade=grade, default_duration=duration, custom_title=title)

        if "error" in parsed_exam and not parsed_exam.get("questions"):
            return jsonify({"error": parsed_exam["error"]}), 400

        return jsonify(parsed_exam), 200

    except Exception as exc:
        logger.error("Upload quiz failed: %s", exc, exc_info=True)
        return jsonify({"error": f"Lỗi phân tích đề thi: {str(exc)}"}), 500


@app.route('/api/quiz/save-custom', methods=['POST'])
def save_custom_quiz_api():
    """Lưu đề thi đã được người dùng chỉnh sửa/tải lên vào Ngân hàng đề thi của hệ thống."""
    try:
        from src.app.curated_quizzes import save_user_exam
        exam_data = request.json if request.is_json else None
        if not exam_data:
            return jsonify({"error": "Dữ liệu đề thi không hợp lệ."}), 400

        if "exam" in exam_data and isinstance(exam_data["exam"], dict):
            exam_data = exam_data["exam"]

        questions = exam_data.get("questions", [])
        if not questions:
            return jsonify({"error": "Đề thi phải có ít nhất 1 câu hỏi."}), 400

        success, res_id = save_user_exam(exam_data)
        if not success:
            return jsonify({"error": f"Không thể lưu đề thi: {res_id}"}), 500

        return jsonify({"success": True, "id": res_id, "message": "Đã lưu đề thi thành công vào Ngân hàng đề!"}), 200

    except Exception as exc:
        logger.error("Save custom quiz failed: %s", exc, exc_info=True)
        return jsonify({"error": f"Lỗi lưu đề thi: {str(exc)}"}), 500



# =========================================================================
# VIRTUAL SCIENCE LAB ENDPOINTS (VẬT LÝ & HÓA HỌC THCS)
# =========================================================================

@app.route('/api/lab/experiments', methods=['GET'])
def get_lab_experiments_api():
    """Lấy danh mục các bài thí nghiệm ảo KHTN (lọc theo khối lớp hoặc phân môn)."""
    try:
        from src.app.science_experiments import list_experiments
        grade_arg = request.args.get('grade')
        subject_arg = request.args.get('subject')
        grade = int(grade_arg) if grade_arg and grade_arg.isdigit() else None
        experiments = list_experiments(grade=grade, subject=subject_arg)
        return jsonify({
            "experiments": experiments,
            "total": len(experiments)
        }), 200
    except Exception as exc:
        logger.error("Get lab experiments failed: %s", exc, exc_info=True)
        return jsonify({"error": f"Không thể lấy danh mục thí nghiệm: {str(exc)}"}), 500


@app.route('/api/lab/experiments/<exp_id>', methods=['GET'])
def get_lab_experiment_detail_api(exp_id):
    """Lấy thông tin chi tiết và tham số mô phỏng của một bài thí nghiệm ảo."""
    try:
        from src.app.science_experiments import get_experiment_by_id
        exp = get_experiment_by_id(exp_id)
        if not exp:
            return jsonify({"error": f"Không tìm thấy bài thí nghiệm với mã: {exp_id}"}), 404
        return jsonify({
            "experiment": exp,
            **exp
        }), 200
    except Exception as exc:
        logger.error("Get lab experiment detail failed: %s", exc, exc_info=True)
        return jsonify({"error": f"Không thể lấy chi tiết bài thí nghiệm: {str(exc)}"}), 500


@app.route('/api/lab/export-report', methods=['GET', 'POST'])
def export_lab_report_api():
    """Xuất file Word (.docx) Báo cáo thực hành thí nghiệm chuẩn Bộ GD&ĐT."""
    try:
        import io
        from src.app.science_experiments import get_experiment_by_id, generate_lab_report_docx
        data = {}
        if request.method == 'POST':
            data = request.get_json(silent=True) or request.form.to_dict() or {}
        else:
            data = request.args.to_dict()

        exp_id = str(data.get("exp_id") or data.get("experiment_id") or "").strip()
        if not exp_id:
            return jsonify({"error": "Thiếu mã thí nghiệm (exp_id hoặc experiment_id)."}), 400

        exp = get_experiment_by_id(exp_id)
        if not exp:
            return jsonify({"error": f"Không tìm thấy bài thí nghiệm với mã: {exp_id}"}), 404

        student_info = {
            "school": data.get("school_name") or data.get("school") or "TRƯỜNG THCS HUỲNH BÁ CHÁNH",
            "student_name": data.get("student_name") or "Học sinh THCS Huỳnh Bá Chánh",
            "class": data.get("class_name") or data.get("class") or f"Lớp {exp['grade']}",
            "group": data.get("group") or "Nhóm thực hành KHTN",
            "date": data.get("date") or ""
        }
        logged_data = data.get("logged_data")
        quiz_answers = data.get("quiz_answers")
        captured_image = data.get("captured_image") or data.get("captured_image_base64")
        docx_bytes = generate_lab_report_docx(
            exp["id"],
            student_info=student_info,
            logged_data=logged_data,
            quiz_answers=quiz_answers,
            captured_image_base64=captured_image
        )
        safe_name = exp["id"].replace("-", "_")
        filename = f"Bao_cao_thuc_hanh_{safe_name}.docx"

        return send_file(
            io.BytesIO(docx_bytes),
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            as_attachment=True,
            download_name=filename
        )
    except Exception as exc:
        logger.error("Export lab report failed: %s", exc, exc_info=True)
        return jsonify({"error": f"Không thể xuất báo cáo thực hành Word: {str(exc)}"}), 500





def _biorag_prepare_image_bytes(image_file, crop):
    """Đọc toàn ảnh hoặc cắt vùng chuẩn hóa x/y/width/height bằng Pillow."""
    import io
    import math
    import mimetypes

    mime_type = mimetypes.guess_type(image_file.name)[0] or "image/png"
    if not mime_type.startswith("image/"):
        raise ValueError("Tệp được chọn không phải hình ảnh.")

    if not isinstance(crop, dict):
        return image_file.read_bytes(), mime_type, None

    try:
        x = float(crop.get("x"))
        y = float(crop.get("y"))
        width = float(crop.get("width"))
        height = float(crop.get("height"))
    except (TypeError, ValueError):
        raise ValueError("Thông tin vùng khoanh không hợp lệ.")

    values = (x, y, width, height)
    if not all(math.isfinite(value) for value in values):
        raise ValueError("Thông tin vùng khoanh không hợp lệ.")
    if x < 0 or y < 0 or width < 0.02 or height < 0.02:
        raise ValueError("Vùng khoanh quá nhỏ hoặc nằm ngoài hình.")
    if x + width > 1.001 or y + height > 1.001:
        raise ValueError("Vùng khoanh nằm ngoài hình.")

    from PIL import Image, ImageOps

    with Image.open(image_file) as source:
        source = ImageOps.exif_transpose(source)
        image_width, image_height = source.size
        if image_width * image_height > 80_000_000:
            raise ValueError("Kích thước ảnh quá lớn để xử lý an toàn.")

        left = max(0, min(image_width - 1, round(x * image_width)))
        top = max(0, min(image_height - 1, round(y * image_height)))
        right = max(left + 1, min(image_width, round((x + width) * image_width)))
        bottom = max(top + 1, min(image_height, round((y + height) * image_height)))
        if right - left < 32 or bottom - top < 32:
            raise ValueError("Vùng khoanh phải rộng và cao ít nhất 32 pixel.")

        selected = source.crop((left, top, right, bottom)).convert("RGB")
        output = io.BytesIO()
        selected.save(output, format="JPEG", quality=92, optimize=True)
        crop_info = {
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "pixel_box": [left, top, right, bottom],
        }
        return output.getvalue(), "image/jpeg", crop_info


def _biorag_image_roots():
    """Trả về các thư mục ảnh hợp lệ, ưu tiên cấu hình rồi đến kho KNTT."""
    from pathlib import Path

    project_root = Path(__file__).resolve().parents[2]
    candidates = (
        Path(IMAGES_DIR),
        project_root / "database_kntt" / "images",
        project_root / "database" / "images",
    )
    roots = []
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved not in roots:
            roots.append(resolved)
    return roots


def _biorag_relative_image_path(raw_image_path):
    """Chuẩn hóa đường dẫn tuyệt đối/URL cũ thành đường dẫn con an toàn."""
    from pathlib import PurePosixPath
    from urllib.parse import unquote

    normalized = unquote(str(raw_image_path or "").strip()).replace("\\", "/")
    if not normalized:
        raise ValueError("Thiếu đường dẫn hình cần xử lý.")

    lower = normalized.lower()
    for marker in ("/database_kntt/images/", "/database/images/", "/images/"):
        marker_position = lower.rfind(marker)
        if marker_position >= 0:
            normalized = normalized[marker_position + len(marker):]
            break

    normalized = normalized.lstrip("/")
    parts = PurePosixPath(normalized).parts
    if not parts or any(part in {"", ".", ".."} for part in parts) or ":" in parts[0]:
        raise PermissionError("Đường dẫn hình không hợp lệ.")
    return parts


def _biorag_resolve_image_file(raw_image_path, max_bytes=18 * 1024 * 1024):
    """Tìm hình an toàn trong kho đang cấu hình hoặc database_kntt/images."""
    from pathlib import Path

    raw_value = str(raw_image_path or "").strip()
    if not raw_value:
        raise ValueError("Thiếu đường dẫn hình cần xử lý.")

    roots = _biorag_image_roots()
    supplied_path = Path(raw_value)
    if supplied_path.is_absolute():
        direct_file = supplied_path.resolve()
        for images_root in roots:
            try:
                direct_file.relative_to(images_root)
            except ValueError:
                continue
            if direct_file.is_file():
                if max_bytes and direct_file.stat().st_size > max_bytes:
                    raise OverflowError("Hình vượt quá giới hạn 18 MB.")
                return direct_file

    parts = _biorag_relative_image_path(raw_value)
    for images_root in roots:
        image_file = images_root.joinpath(*parts).resolve()
        try:
            image_file.relative_to(images_root)
        except ValueError:
            continue
        if image_file.is_file():
            if max_bytes and image_file.stat().st_size > max_bytes:
                raise OverflowError("Hình vượt quá giới hạn 18 MB.")
            return image_file
    raise FileNotFoundError("Không tìm thấy hình trong cơ sở dữ liệu KNTT.")


def _biorag_resolve_any_image(raw_image_path=None, raw_image_url=None, metadata=None, max_bytes=18 * 1024 * 1024):
    """Tìm tệp ảnh từ image_path (ảnh trong kho), hoặc image_url / metadata (trang SGK)."""
    import re
    from pathlib import Path
    from urllib.parse import parse_qs, unquote, urlparse

    raw_path_str = str(raw_image_path or "").strip()
    raw_url_str = str(raw_image_url or "").strip()
    meta = metadata if isinstance(metadata, dict) else {}

    # 1. Nếu chỉ rõ là trang SGK (từ URL hoặc metadata flag)
    is_explicit_textbook = (
        "textbook-page" in raw_url_str
        or "textbook-page" in raw_path_str
        or bool(meta.get("textbook_page"))
        or bool(meta.get("textbook_page_fallback"))
    )

    if is_explicit_textbook:
        candidate_str = raw_url_str or raw_path_str
        source = meta.get("pdf_filename") or meta.get("source")
        page = meta.get("page_number") if meta.get("page_number") is not None else meta.get("page")
        if candidate_str:
            parsed = urlparse(candidate_str)
            params = parse_qs(parsed.query)
            if "source" in params and params["source"]:
                source = unquote(params["source"][0])
            if "page" in params and params["page"]:
                page = params["page"][0]
        if source and page is not None:
            try:
                page_num = int(page)
                if page_num > 0:
                    pdf_path = _biorag_resolve_textbook_pdf(str(source))
                    return _biorag_render_textbook_page(pdf_path, page_num)
            except Exception as exc:
                logger.warning("Không thể render trang SGK (%s, p.%s): %s", source, page, exc)

    # 2. Thử phân giải ảnh trực tiếp từ đường dẫn tệp trong kho
    for candidate in (raw_path_str, raw_url_str):
        if not candidate:
            continue
        target = candidate
        if "/api/images/" in target:
            target = target.split("/api/images/", 1)[1]
        try:
            return _biorag_resolve_image_file(target, max_bytes=max_bytes)
        except Exception:
            pass

    # 3. Nếu vẫn chưa tìm thấy nhưng metadata có thông tin trang SGK
    source = meta.get("pdf_filename") or meta.get("source")
    page = meta.get("page_number") if meta.get("page_number") is not None else meta.get("page")
    if source and page is not None and str(source).lower().endswith(".pdf"):
        try:
            page_num = int(page)
            if page_num > 0:
                pdf_path = _biorag_resolve_textbook_pdf(str(source))
                return _biorag_render_textbook_page(pdf_path, page_num)
        except Exception:
            pass

    raise FileNotFoundError("Không tìm thấy hình ảnh hoặc trang SGK tương ứng.")


@app.route('/api/images/<path:image_path>', methods=['GET'])
def biorag_serve_image(image_path):
    """Phục vụ ảnh SGK qua URL ổn định, kể cả dữ liệu chat được lưu từ bản cũ."""
    from flask import abort, send_file

    try:
        image_file = _biorag_resolve_image_file(image_path, max_bytes=None)
    except (ValueError, PermissionError, FileNotFoundError, OverflowError):
        abort(404)
    return send_file(image_file, conditional=True, max_age=3600)


def _biorag_plain_markdown(value):
    """Loại bỏ định dạng Markdown đơn giản trước khi đưa vào tài liệu."""
    import re

    value = str(value or "")
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    value = re.sub(r"__([^_]+)__", r"\1", value)
    return value.strip()


def _biorag_add_docx_answer(document, answer):
    """Thêm câu trả lời, giữ lại tiêu đề và danh sách cơ bản."""
    import re

    for raw_line in str(answer or "").splitlines():
        line = raw_line.strip()
        if not line:
            document.add_paragraph()
            continue
        heading = re.match(r"^#{1,3}\s+(.+)$", line)
        bullet = re.match(r"^[-*]\s+(.+)$", line)
        numbered = re.match(r"^\d+[.)]\s+(.+)$", line)
        if heading:
            document.add_heading(_biorag_plain_markdown(heading.group(1)), level=2)
        elif bullet:
            document.add_paragraph(_biorag_plain_markdown(bullet.group(1)), style="List Bullet")
        elif numbered:
            document.add_paragraph(_biorag_plain_markdown(numbered.group(1)), style="List Number")
        else:
            document.add_paragraph(_biorag_plain_markdown(line))


def _biorag_build_docx(image_bytes, question, answer, source_name, page, crop_info):
    """Tạo tài liệu Word học tập có nguồn và hình/vùng hình đang hỏi."""
    import io

    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Inches, Pt

    document = Document()
    normal = document.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(11)

    title = document.add_heading("GHI CHÚ HỌC TẬP TỪ HÌNH ẢNH", level=1)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    source = document.add_paragraph()
    source.alignment = WD_ALIGN_PARAGRAPH.CENTER
    source.add_run(f"Nguồn: {source_name} · Trang {page}").italic = True

    if crop_info:
        note = document.add_paragraph("Nội dung dưới đây được tạo từ vùng ảnh người học đã khoanh.")
        note.alignment = WD_ALIGN_PARAGRAPH.CENTER

    image_stream = io.BytesIO(image_bytes)
    document.add_picture(image_stream, width=Inches(6.2))
    document.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    document.add_heading("Câu hỏi", level=2)
    document.add_paragraph(question)
    document.add_heading("Nội dung học tập", level=2)
    _biorag_add_docx_answer(document, answer)

    footer = document.sections[0].footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run("Tạo bởi BioRAG KNTT")

    output = io.BytesIO()
    document.save(output)
    output.seek(0)
    return output


def _biorag_pdf_font_name():
    """Đăng ký font Unicode để tiếng Việt hiển thị đúng trong PDF."""
    import os
    from pathlib import Path

    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont

    font_name = "BioRAGUnicode"
    if font_name in pdfmetrics.getRegisteredFontNames():
        return font_name

    windows = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
    candidates = [
        windows / "arial.ttf",
        windows / "calibri.ttf",
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for font_path in candidates:
        if font_path.is_file():
            pdfmetrics.registerFont(TTFont(font_name, str(font_path)))
            return font_name
    raise RuntimeError("Không tìm thấy font Unicode để xuất PDF tiếng Việt.")


def _biorag_build_pdf(image_bytes, question, answer, source_name, page, crop_info):
    """Tạo PDF học tập có hình, câu hỏi và câu trả lời."""
    import html
    import io
    import re

    from PIL import Image as PILImage
    from reportlab.lib.enums import TA_CENTER
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import Image as PDFImage
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

    font_name = _biorag_pdf_font_name()
    output = io.BytesIO()
    document = SimpleDocTemplate(
        output,
        pagesize=A4,
        rightMargin=1.7 * cm,
        leftMargin=1.7 * cm,
        topMargin=1.6 * cm,
        bottomMargin=1.7 * cm,
        title="Ghi chú học tập BioRAG",
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "BioRAGTitle", parent=styles["Title"], fontName=font_name,
        fontSize=17, leading=21, alignment=TA_CENTER, textColor="#123d2d",
    )
    source_style = ParagraphStyle(
        "BioRAGSource", parent=styles["Normal"], fontName=font_name,
        fontSize=9, leading=13, alignment=TA_CENTER, textColor="#5c6f65",
    )
    heading_style = ParagraphStyle(
        "BioRAGHeading", parent=styles["Heading2"], fontName=font_name,
        fontSize=12, leading=16, textColor="#176b4d", spaceBefore=8, spaceAfter=5,
    )
    body_style = ParagraphStyle(
        "BioRAGBody", parent=styles["BodyText"], fontName=font_name,
        fontSize=10.5, leading=16, textColor="#193128", spaceAfter=5,
    )
    bullet_style = ParagraphStyle(
        "BioRAGBullet", parent=body_style, leftIndent=14, firstLineIndent=-8,
    )

    story = [
        Paragraph("GHI CHÚ HỌC TẬP TỪ HÌNH ẢNH", title_style),
        Paragraph(html.escape(f"Nguồn: {source_name} · Trang {page}"), source_style),
    ]
    if crop_info:
        story.extend([Spacer(1, 4), Paragraph("Nội dung được tạo từ vùng ảnh đã khoanh.", source_style)])
    story.append(Spacer(1, 10))

    with PILImage.open(io.BytesIO(image_bytes)) as image:
        image_width, image_height = image.size
    max_width, max_height = 17.2 * cm, 10.5 * cm
    scale = min(max_width / image_width, max_height / image_height)
    story.append(PDFImage(io.BytesIO(image_bytes), width=image_width * scale, height=image_height * scale))
    story.extend([
        Spacer(1, 10),
        Paragraph("Câu hỏi", heading_style),
        Paragraph(html.escape(question), body_style),
        Paragraph("Nội dung học tập", heading_style),
    ])

    for raw_line in str(answer or "").splitlines():
        line = raw_line.strip()
        if not line:
            story.append(Spacer(1, 4))
            continue
        bullet = re.match(r"^[-*]\s+(.+)$", line)
        numbered = re.match(r"^(\d+[.)])\s+(.+)$", line)
        heading = re.match(r"^#{1,3}\s+(.+)$", line)
        if bullet:
            story.append(Paragraph("• " + html.escape(_biorag_plain_markdown(bullet.group(1))), bullet_style))
        elif numbered:
            story.append(Paragraph(html.escape(numbered.group(1) + " " + _biorag_plain_markdown(numbered.group(2))), bullet_style))
        elif heading:
            story.append(Paragraph(html.escape(_biorag_plain_markdown(heading.group(1))), heading_style))
        else:
            story.append(Paragraph(html.escape(_biorag_plain_markdown(line)), body_style))

    def footer(canvas, doc):
        canvas.saveState()
        canvas.setFont(font_name, 8)
        canvas.setFillColor("#738078")
        canvas.drawCentredString(A4[0] / 2, 0.9 * cm, f"BioRAG KNTT · Trang {doc.page}")
        canvas.restoreState()

    document.build(story, onFirstPage=footer, onLaterPages=footer)
    output.seek(0)
    return output


@app.route('/api/image-chat', methods=['POST'])
def image_chat():
    """Gửi toàn ảnh hoặc vùng người học khoanh trực tiếp tới Gemini."""
    import base64
    from langchain_core.messages import HumanMessage
    from src.config import GEMINI_API_KEY

    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()
    raw_image_path = str(data.get("image_path", "")).strip()
    raw_image_url = str(data.get("image_url", "")).strip()
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}

    if not question:
        return jsonify({"error": "Câu hỏi về hình không được để trống."}), 400
    if not raw_image_path and not raw_image_url and not metadata.get("pdf_filename"):
        return jsonify({"error": "Thiếu thông tin hình ảnh hoặc trang SGK cần phân tích."}), 400
    if not GEMINI_API_KEY:
        return jsonify({"error": "Chưa cấu hình GEMINI_API_KEY cho phân tích hình."}), 503

    try:
        image_file = _biorag_resolve_any_image(raw_image_path, raw_image_url, metadata)
    except PermissionError as exc:
        return jsonify({"error": str(exc)}), 403
    except FileNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404
    except OverflowError as exc:
        return jsonify({"error": str(exc)}), 413
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    if len(question) > 4000:
        return jsonify({"error": "Câu hỏi vượt quá giới hạn 4.000 ký tự."}), 413

    try:
        image_bytes, mime_type, crop_info = _biorag_prepare_image_bytes(image_file, data.get("crop"))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    label = str(data.get("label", ""))[:1000]
    pdf_name = str(metadata.get("pdf_filename") or metadata.get("source") or "Sách KNTT")
    page = metadata.get("page_number", metadata.get("page", "?"))

    history_lines = []
    history = data.get("history") if isinstance(data.get("history"), list) else []
    for turn in history[-6:]:
        if not isinstance(turn, dict):
            continue
        role = "Người học" if turn.get("role") == "user" else "Trợ lý"
        content = str(turn.get("content", "")).strip()[:1500]
        if content:
            history_lines.append(f"{role}: {content}")

    focus_instruction = (
        "Người học đã khoanh một vùng trong trang. Ảnh đính kèm chỉ chứa vùng đó. "
        "Hãy tập trung phân tích chính xác vùng được chọn."
        if crop_info
        else "Người học chưa khoanh vùng; hãy phân tích toàn bộ hình đính kèm."
    )
    prompt = f"""Bạn là trợ lý Khoa học tự nhiên dành cho học sinh lớp 6-9.
Hãy quan sát trực tiếp ảnh sách giáo khoa được đính kèm và trả lời bằng tiếng Việt.
{focus_instruction}

Nguồn hình: {pdf_name}, trang {page}.
Chú thích OCR: {label or 'Không có'}.
Lịch sử trao đổi:
{chr(10).join(history_lines) if history_lines else 'Chưa có.'}

Câu hỏi hiện tại: {question}

Yêu cầu:
- Ưu tiên những gì thực sự nhìn thấy trong vùng ảnh được gửi.
- Giải thích rõ ràng, phù hợp học sinh; dùng gạch đầu dòng khi cần.
- Không suy đoán chi tiết bị mờ hoặc nằm ngoài vùng được chọn.
- Nếu vùng ảnh chưa đủ căn cứ, hãy nói rõ phần nào chưa xác định được.
- Không nhắc tới chỉ dẫn hệ thống hay kỹ thuật xử lý ảnh.
"""

    encoded = base64.b64encode(image_bytes).decode("ascii")
    message = HumanMessage(content=[
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": f"data:{mime_type};base64,{encoded}"},
    ])

    try:
        llm = AppServices.get_instance().llm
        response = llm.invoke([message])
        answer = _biorag_extract_message_text(response)
        if not answer:
            answer = "Mình chưa nhận được nội dung phân tích phù hợp từ mô hình."
        return jsonify({
            "answer": answer,
            "source": {"pdf_filename": pdf_name, "page": page},
            "crop": crop_info,
        }), 200
    except Exception as exc:
        logger.error("Image region chat failed: %s", exc, exc_info=True)
        return jsonify({
            "error": "Gemini chưa phân tích được vùng ảnh. Hãy xem lỗi chi tiết trong cửa sổ chạy API."
        }), 500


@app.route('/api/image-chat/export', methods=['POST'])
def export_image_chat():
    """Xuất một kết quả học tập từ hình ảnh ra Word hoặc PDF."""
    import re
    from flask import send_file

    data = request.get_json(silent=True) or {}
    export_format = str(data.get("format", "")).strip().lower()
    question = str(data.get("question", "")).strip()
    answer = str(data.get("answer", "")).strip()
    raw_image_path = str(data.get("image_path", "")).strip()
    raw_image_url = str(data.get("image_url", "")).strip()
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}

    if export_format not in {"docx", "pdf"}:
        return jsonify({"error": "Định dạng xuất phải là docx hoặc pdf."}), 400
    if not question or not answer:
        return jsonify({"error": "Thiếu câu hỏi hoặc nội dung cần xuất."}), 400
    if len(question) > 4000 or len(answer) > 40000:
        return jsonify({"error": "Nội dung cần xuất vượt quá giới hạn cho phép."}), 413

    try:
        image_file = _biorag_resolve_any_image(raw_image_path, raw_image_url, metadata)
    except PermissionError as exc:
        return jsonify({"error": "Đường dẫn hình không hợp lệ."}), 403
    except FileNotFoundError as exc:
        return jsonify({"error": str(exc)}), 404
    except OverflowError as exc:
        return jsonify({"error": str(exc)}), 413
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    pdf_name = str(metadata.get("pdf_filename") or metadata.get("source") or "Sách KNTT")
    page = metadata.get("page_number", metadata.get("page", "?"))
    try:
        image_bytes, _mime_type, crop_info = _biorag_prepare_image_bytes(image_file, data.get("crop"))
        if export_format == "docx":
            output = _biorag_build_docx(image_bytes, question, answer, pdf_name, page, crop_info)
            mimetype = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        else:
            output = _biorag_build_pdf(image_bytes, question, answer, pdf_name, page, crop_info)
            mimetype = "application/pdf"

        safe_page = re.sub(r"[^0-9A-Za-z_-]+", "_", str(page))[:30] or "khong_ro"
        filename = f"BioRAG_KNTT_trang_{safe_page}.{export_format}"
        return send_file(output, mimetype=mimetype, as_attachment=True, download_name=filename)
    except ImportError as exc:
        logger.error("Missing export dependency: %s", exc, exc_info=True)
        return jsonify({
            "error": "Thiếu thư viện xuất tài liệu. Chạy: python -m pip install python-docx reportlab"
        }), 503
    except Exception as exc:
        logger.error("Image learning export failed: %s", exc, exc_info=True)
        return jsonify({"error": "Không thể tạo tài liệu. Hãy xem lỗi chi tiết trong cửa sổ chạy API."}), 500


def run_api(host='0.0.0.0', port=5000):
    logger.info("Initializing AppServices before starting Flask...")
    AppServices.get_instance()
    logger.info(f"Starting Flask API server on {host}:{port}...")
    app.run(host=host, port=port, debug=False)
