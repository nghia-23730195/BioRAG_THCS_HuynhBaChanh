# -*- coding: utf-8 -*-
"""Update and clean learning_lessons.json terms across src/ and api/ directories."""

import json
import os
import re
import sys

sys.path.insert(0, os.path.abspath("."))
from api._textbook_renderer import ENCYCLOPEDIA_KHTN

def clean_term_definition(term_name, current_def, lesson):
    if not any(phrase in current_def for phrase in ["thể hiện bản chất quy luật", "khái niệm khoa học cốt lõi", "khái niệm khoa học trọng tâm"]):
        return current_def

    t_clean = term_name.lower().strip()
    
    # 1. Check ENCYCLOPEDIA_KHTN
    for k, v in ENCYCLOPEDIA_KHTN.items():
        if k == t_clean or k in t_clean or t_clean in k:
            return v.get("definition", "")

    # 2. Extract from lesson content if it mentions the term
    content = lesson.get("content", "")
    if content and term_name.lower() in content.lower():
        sentences = re.split(r'[.!?\n]+', content)
        for s in sentences:
            s_clean = s.strip()
            if len(s_clean) > 25 and term_name.lower() in s_clean.lower() and (" là " in s_clean or " gồm " in s_clean or " có " in s_clean or " được " in s_clean):
                return s_clean + "."

    # 3. Extract from objectives or summary
    for item in lesson.get("objectives", []) + lesson.get("summary", []):
        if len(item) > 20 and term_name.lower() in item.lower():
            return item

    # 4. Generate clean, factual default based on lesson title
    title = lesson.get("title", "")
    grade = lesson.get("grade", 6)
    number = lesson.get("number", "")
    return f"Kiến thức trọng tâm về {term_name} trong {number} ({title}) môn Khoa học tự nhiên {grade} (Bộ sách Kết nối tri thức với cuộc sống)."


def update_all_lessons_files():
    paths = [
        "src/app/data/learning_lessons.json",
        "api/data/learning_lessons.json",
        "src/app/data/lessons.json",
        "api/data/lessons.json",
    ]

    for path in paths:
        if not os.path.exists(path):
            continue
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            is_dict = isinstance(data, dict)
            lessons = data.get("lessons", []) if is_dict else data

            updated_count = 0
            for lesson in lessons:
                terms = lesson.get("terms", [])
                for t in terms:
                    orig_def = t.get("definition", "")
                    cleaned = clean_term_definition(t.get("term", ""), orig_def, lesson)
                    if cleaned != orig_def:
                        t["definition"] = cleaned
                        updated_count += 1

            if is_dict:
                data["lessons"] = lessons
            else:
                data = lessons

            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            print(f"[+] Successfully updated {path} (improved {updated_count} term definitions)")
        except Exception as exc:
            print(f"[-] Error updating {path}: {exc}")

if __name__ == "__main__":
    update_all_lessons_files()
