"""Persistent learning catalog for the BioRAG student learning area.

The catalog is intentionally separate from ChromaDB.  Teacher-authored lesson
metadata lives in ``PERSIST_DIR/learning_lessons.json`` while quizzes continue
to use the existing grounded RAG quiz endpoint.
"""

from __future__ import annotations

import json
import re
import threading
import unicodedata
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
from uuid import uuid4

from src.config import PERSIST_DIR
from src.app.complete_lessons import COMPLETE_LESSON_VERSION, get_complete_lessons


CATALOG_PATH = Path(PERSIST_DIR) / "learning_lessons.json"
_CATALOG_LOCK = threading.RLock()
_VALID_GRADES = {6, 7, 8, 9}
_MAX_TITLE = 180
_MAX_TOPIC = 240
_MAX_NUMBER = 60
_MAX_CONTENT = 12000
_MAX_OBJECTIVES = 12
_MAX_OBJECTIVE_LENGTH = 320


DEFAULT_LESSONS: List[Dict[str, Any]] = [
    {
        "id": "k6-te-bao",
        "grade": 6,
        "number": "Chủ đề 1",
        "title": "Tế bào – đơn vị cơ sở của sự sống",
        "topic": "Tế bào là đơn vị cơ sở của sự sống",
        "objectives": [
            "Nêu được khái niệm tế bào.",
            "Nhận biết được một số thành phần chính của tế bào.",
        ],
        "content": (
            "Tế bào là đơn vị cấu trúc và chức năng cơ bản của cơ thể sống. "
            "Các tế bào có hình dạng, kích thước khác nhau nhưng đều thực hiện "
            "những hoạt động sống cần thiết."
        ),
        "source_label": "SGK KHTN 6 KNTT · Giáo viên có thể bổ sung",
        "order": 10,
        "active": True,
        "origin": "system",
    },
    {
        "id": "k7-ho-hap-te-bao",
        "grade": 7,
        "number": "Bài 25",
        "title": "Hô hấp tế bào",
        "topic": "Hô hấp tế bào",
        "objectives": [
            "Nêu được khái niệm hô hấp tế bào.",
            "Mô tả được chất tham gia, sản phẩm và vai trò của quá trình.",
        ],
        "content": (
            "Hô hấp tế bào là quá trình phân giải chất hữu cơ, tạo thành nước, "
            "carbon dioxide và giải phóng năng lượng ATP cho các hoạt động sống."
        ),
        "source_label": "SGK KHTN 7 KNTT · Trang 112–115",
        "order": 10,
        "active": True,
        "origin": "system",
    },
    {
        "id": "k8-he-van-dong",
        "grade": 8,
        "number": "Chủ đề 1",
        "title": "Hệ vận động ở người",
        "topic": "Hệ vận động ở người",
        "objectives": [
            "Nêu được cấu tạo khái quát của hệ vận động.",
            "Giải thích được sự phối hợp giữa cơ, xương và khớp.",
        ],
        "content": (
            "Hệ vận động gồm bộ xương, các khớp và hệ cơ. Sự co cơ tạo lực kéo "
            "lên xương qua khớp, nhờ đó cơ thể thực hiện được vận động."
        ),
        "source_label": "SGK KHTN 8 KNTT · Giáo viên có thể bổ sung",
        "order": 10,
        "active": True,
        "origin": "system",
    },
    {
        "id": "k9-tan-sac-anh-sang",
        "grade": 9,
        "number": "Bài 7",
        "title": "Tán sắc ánh sáng",
        "topic": "Tán sắc ánh sáng qua lăng kính",
        "objectives": [
            "Mô tả được hiện tượng tán sắc ánh sáng.",
            "Giải thích được vai trò của lăng kính trong thí nghiệm.",
        ],
        "content": (
            "Khi một chùm ánh sáng trắng hẹp đi qua lăng kính, ánh sáng bị tách "
            "thành nhiều chùm sáng màu khác nhau, tạo thành một dải màu liên tục."
        ),
        "source_label": "SGK KHTN 9 KNTT · Trang 19–21",
        "order": 10,
        "active": True,
        "origin": "system",
    },
]

# The compact records above are kept for compatibility with older patches.
# New installations and upgrades use the four fully structured sample lessons.
DEFAULT_LESSONS = get_complete_lessons()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _clean_text(value: Any, max_length: int, field_name: str, required: bool = False) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    if required and not text:
        raise ValueError(f"Trường {field_name} không được để trống.")
    if len(text) > max_length:
        raise ValueError(f"Trường {field_name} vượt quá {max_length} ký tự.")
    return text


def _clean_content(value: Any) -> str:
    text = str(value or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    text = "\n".join(line.rstrip() for line in text.splitlines())
    if not text:
        raise ValueError("Nội dung bài học không được để trống.")
    if len(text) > _MAX_CONTENT:
        raise ValueError(f"Nội dung bài học vượt quá {_MAX_CONTENT} ký tự.")
    return text


def _clean_objectives(value: Any) -> List[str]:
    if isinstance(value, str):
        raw_items: Iterable[Any] = value.splitlines()
    elif isinstance(value, (list, tuple)):
        raw_items = value
    else:
        raw_items = []

    objectives = []
    for raw_item in raw_items:
        item = _clean_text(raw_item, _MAX_OBJECTIVE_LENGTH, "mục tiêu")
        if item and item not in objectives:
            objectives.append(item)
    if not objectives:
        raise ValueError("Bài học cần ít nhất một mục tiêu.")
    if len(objectives) > _MAX_OBJECTIVES:
        raise ValueError(f"Bài học chỉ được có tối đa {_MAX_OBJECTIVES} mục tiêu.")
    return objectives


def _slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value.lower())
    plain = "".join(char for char in normalized if unicodedata.category(char) != "Mn")
    plain = plain.replace("đ", "d")
    slug = re.sub(r"[^a-z0-9]+", "-", plain).strip("-")
    return slug[:70] or "bai-hoc"


def _normalized_lesson(payload: Dict[str, Any], existing: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    base = deepcopy(existing or {})
    try:
        grade = int(payload.get("grade", base.get("grade")))
    except (TypeError, ValueError):
        raise ValueError("Khối lớp phải là 6, 7, 8 hoặc 9.")
    if grade not in _VALID_GRADES:
        raise ValueError("Khối lớp phải là 6, 7, 8 hoặc 9.")

    title = _clean_text(payload.get("title", base.get("title")), _MAX_TITLE, "tiêu đề", required=True)
    topic = _clean_text(payload.get("topic", base.get("topic") or title), _MAX_TOPIC, "chủ đề RAG", required=True)
    number = _clean_text(payload.get("number", base.get("number")), _MAX_NUMBER, "số bài")
    content = _clean_content(payload.get("content", base.get("content")))
    objectives = _clean_objectives(payload.get("objectives", base.get("objectives")))
    source_label = _clean_text(
        payload.get("source_label", base.get("source_label") or "SGK KNTT · Giáo viên bổ sung"),
        240,
        "nguồn",
    )

    try:
        order = int(payload.get("order", base.get("order", 100)))
    except (TypeError, ValueError):
        order = 100
    order = max(0, min(order, 9999))

    lesson_id = str(base.get("id") or "").strip()
    if not lesson_id:
        lesson_id = f"k{grade}-{_slugify(title)}-{uuid4().hex[:8]}"

    now = _now_iso()
    lesson = {
        "id": lesson_id,
        "grade": grade,
        "number": number,
        "title": title,
        "topic": topic,
        "objectives": objectives,
        "content": content,
        "source_label": source_label,
        "order": order,
        "active": bool(payload.get("active", base.get("active", True))),
        "origin": str(base.get("origin") or "teacher"),
        "created_at": str(base.get("created_at") or now),
        "updated_at": now,
    }
    # Preserve the structured teaching blocks of a complete system lesson when
    # a teacher edits one of its basic fields in the current form.
    for field in ("duration", "warmup", "sections", "diagram", "terms", "summary", "quick_check", "illustrations", "generation_sources", "lesson_version"):
        if field in payload:
            lesson[field] = deepcopy(payload[field])
        elif field in base:
            lesson[field] = deepcopy(base[field])
    return lesson


def _default_document() -> Dict[str, Any]:
    now = _now_iso()
    lessons = []
    for item in DEFAULT_LESSONS:
        normalized = _normalized_lesson(item)
        normalized["id"] = item["id"]
        normalized["origin"] = "system"
        normalized["created_at"] = now
        normalized["updated_at"] = now
        lessons.append(normalized)
    return {"version": 1, "updated_at": now, "lessons": lessons}


def _write_document(document: Dict[str, Any]) -> None:
    CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    document = deepcopy(document)
    document["version"] = 1
    document["updated_at"] = _now_iso()
    temp_path = CATALOG_PATH.with_name(f"{CATALOG_PATH.name}.tmp")
    temp_path.write_text(
        json.dumps(document, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    temp_path.replace(CATALOG_PATH)


def _read_document() -> Dict[str, Any]:
    with _CATALOG_LOCK:
        if not CATALOG_PATH.is_file():
            document = _default_document()
            _write_document(document)
            return document
        document = json.loads(CATALOG_PATH.read_text(encoding="utf-8-sig"))
        if not isinstance(document, dict) or not isinstance(document.get("lessons"), list):
            raise ValueError("File learning_lessons.json không đúng cấu trúc.")
        # Upgrade only the four bundled system samples. Teacher-created lessons
        # have different ids and are retained byte-for-byte in the same catalog.
        by_id = {
            str(item.get("id") or ""): index
            for index, item in enumerate(document["lessons"])
            if isinstance(item, dict)
        }
        changed = False
        for sample in get_complete_lessons():
            index = by_id.get(sample["id"])
            if index is None:
                normalized = _normalized_lesson(sample)
                normalized["id"] = sample["id"]
                normalized["origin"] = "system"
                document["lessons"].append(normalized)
                changed = True
                continue
            current = document["lessons"][index]
            if int(current.get("lesson_version") or 0) >= COMPLETE_LESSON_VERSION:
                continue
            normalized = _normalized_lesson(sample)
            normalized["id"] = sample["id"]
            normalized["origin"] = "system"
            normalized["created_at"] = current.get("created_at") or normalized["created_at"]
            normalized["active"] = bool(current.get("active", True))
            document["lessons"][index] = normalized
            changed = True
        if changed:
            _write_document(document)
        return document


def list_lessons(grade: Optional[int] = None, include_inactive: bool = False) -> List[Dict[str, Any]]:
    document = _read_document()
    lessons = []
    for item in document["lessons"]:
        if not isinstance(item, dict):
            continue
        if grade is not None and int(item.get("grade") or 0) != int(grade):
            continue
        if not include_inactive and not bool(item.get("active", True)):
            continue
        lessons.append(deepcopy(item))
    lessons.sort(key=lambda item: (int(item.get("grade") or 0), int(item.get("order") or 0), item.get("title") or ""))
    return lessons


def create_lesson(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("Dữ liệu bài học không hợp lệ.")
    lesson = _normalized_lesson(payload)
    with _CATALOG_LOCK:
        document = _read_document()
        document["lessons"].append(lesson)
        _write_document(document)
    return deepcopy(lesson)


def update_lesson(lesson_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    lesson_id = str(lesson_id or "").strip()
    if not lesson_id or not isinstance(payload, dict):
        raise ValueError("Dữ liệu cập nhật bài học không hợp lệ.")
    with _CATALOG_LOCK:
        document = _read_document()
        for index, existing in enumerate(document["lessons"]):
            if str(existing.get("id") or "") != lesson_id:
                continue
            lesson = _normalized_lesson(payload, existing=existing)
            lesson["id"] = lesson_id
            lesson["origin"] = existing.get("origin") or "teacher"
            document["lessons"][index] = lesson
            _write_document(document)
            return deepcopy(lesson)
    raise KeyError(lesson_id)

