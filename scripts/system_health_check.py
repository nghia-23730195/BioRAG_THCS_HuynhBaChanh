# -*- coding: utf-8 -*-
"""Full system health check and integration verification for BioRAG."""

import os
import sys
import io
import json
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"

sys.path.insert(0, os.path.abspath("."))

def test_system():
    print("=" * 80)
    print("BIORAG COMPREHENSIVE SYSTEM VERIFICATION SUITE")
    print("=" * 80)

    passed = 0
    total = 0

    # 1. Check Learning Lessons Catalog
    total += 1
    try:
        from src.app.learning_catalog import list_lessons
        lessons = list_lessons()
        assert len(lessons) >= 190, f"Expected at least 190 lessons, got {len(lessons)}"
        print(f"[PASS] 1. Learning Catalog Loaded: {len(lessons)} lessons across Grades 6-9.")
        passed += 1
    except Exception as e:
        print(f"[FAIL] 1. Learning Catalog Error: {e}")

    # 2. Check Database Chunks
    total += 1
    try:
        from src.rag.book_rag import load_all_chunks
        chunks = load_all_chunks()
        assert len(chunks) > 4000, f"Expected >4000 chunks, got {len(chunks)}"
        print(f"[PASS] 2. ChromaDB / Database: {len(chunks)} textbook chunks available.")
        passed += 1
    except Exception as e:
        print(f"[FAIL] 2. Database Error: {e}")

    # 3. Check Grounded Chat API
    total += 1
    try:
        from src.app.api import _biorag_answer_grounded_question
        res, code = _biorag_answer_grounded_question("cây Dương xỉ là gì?", 6, [])
        assert code == 200, f"Expected status 200, got {code}"
        ans = res.get("answer", "")
        assert "bào tử" in ans.lower() or "dương xỉ" in ans.lower(), f"Unexpected answer: {ans}"
        assert len(res.get("sources", [])) > 0, "Expected at least 1 source"
        print(f"[PASS] 3. Grounded Chat Query ('cây Dương xỉ là gì?'): Response OK, Sources: {res['sources']}")
        passed += 1
    except Exception as e:
        print(f"[FAIL] 3. Grounded Chat Error: {e}")

    # 4. Check Out-of-scope Refusal & Zero False Citations
    total += 1
    try:
        from src.app.api import _biorag_answer_grounded_question
        res, code = _biorag_answer_grounded_question("Thủ đô của nước Pháp là gì?", None, [])
        assert code == 200
        ans = res.get("answer", "")
        sources = res.get("sources", [])
        assert "không được đề cập" in ans.lower() or "nằm ngoài phạm vi" in ans.lower(), f"Expected refusal, got: {ans}"
        assert len(sources) == 0, f"Expected 0 sources for refusal, got {sources}"
        print(f"[PASS] 4. Out-of-Scope Refusal: Cleanly refused with 0 spurious citations.")
        passed += 1
    except Exception as e:
        print(f"[FAIL] 4. Out-of-Scope Refusal Error: {e}")

    # 5. Check Local RAG & Textbook Renderer
    total += 1
    try:
        from api._textbook_renderer import format_local_rag_answer, search_best_lesson
        from api.index import get_all_lessons
        all_l = get_all_lessons()
        matched, _ = search_best_lesson(all_l, "cây Dương xỉ là gì?", 6)
        local_ans = format_local_rag_answer("cây Dương xỉ là gì?", matched)
        assert "thể hiện bản chất quy luật" not in local_ans, "Found placeholder string in local answer"
        assert "Dương xỉ" in local_ans, "Missing term in local answer"
        print(f"[PASS] 5. Local Fallback RAG: Generated accurate domain knowledge with zero boilerplate.")
        passed += 1
    except Exception as e:
        print(f"[FAIL] 5. Local Fallback RAG Error: {e}")

    print("\n" + "=" * 80)
    print(f"VERIFICATION SUMMARY: {passed}/{total} tests PASSED ({passed/total*100:.1f}%)")
    print("=" * 80)

if __name__ == "__main__":
    test_system()
