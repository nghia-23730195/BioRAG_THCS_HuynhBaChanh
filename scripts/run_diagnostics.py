# -*- coding: utf-8 -*-
"""Comprehensive diagnostic runner for BioRAG retrieval & grounded answer generation."""

import os
import sys
import io
import json
import time

# Force UTF-8 on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_TELEMETRY"] = "False"

sys.path.insert(0, os.path.abspath("."))

from src.rag.book_rag import load_all_chunks
from src.app.api import (
    _biorag_load_chat_context,
    _biorag_rank_chat_chunks,
    _biorag_scope_chat_chunks,
    _biorag_chat_lesson_scope,
    _biorag_answer_grounded_question,
    _biorag_quiz_chunk_fields,
    _biorag_quiz_chunk_grade,
    _biorag_chat_tokens,
    _biorag_normalize_search_text,
)

TEST_QUESTIONS = [
    {
        "id": "q1_khtn7",
        "query": "Nhóm cây ưa sáng là gì?",
        "grade": 7,
        "target_book": "SGK KHTN 7 KNTT.pdf",
        "target_lesson": "Bài 23: Một số yếu tố ảnh hưởng đến quang hợp",
        "target_pages": [104, 105],
        "type": "in_scope"
    },
    {
        "id": "q2_khtn6",
        "query": "Tế bào nhân sơ khác tế bào nhân thực ở điểm nào?",
        "grade": 6,
        "target_book": "SGK KHTN 6 KNTT.pdf",
        "target_lesson": "Bài 19: Cấu tạo và chức năng các thành phần của tế bào",
        "target_pages": [65, 66, 67],
        "type": "in_scope"
    },
    {
        "id": "q3_khtn8",
        "query": "Định luật bảo toàn khối lượng phát biểu như thế nào?",
        "grade": 8,
        "target_book": "SGK KHTN 8 KNTT.pdf",
        "target_lesson": "Bài 5: Định luật bảo toàn khối lượng và phương trình hóa học",
        "target_pages": [24, 25],
        "type": "in_scope"
    },
    {
        "id": "q4_khtn9",
        "query": "Hiện tượng tán sắc ánh sáng là gì?",
        "grade": 9,
        "target_book": "SGK KHTN 9 KNTT.pdf",
        "target_lesson": "Bài 7: Hiện tượng tán sắc ánh sáng",
        "target_pages": [31, 32, 33, 34],
        "type": "in_scope"
    },
    {
        "id": "q5_out_of_scope",
        "query": "Thủ đô của nước Pháp là thành phố nào?",
        "grade": None,
        "target_book": None,
        "target_lesson": None,
        "target_pages": [],
        "type": "out_of_scope"
    }
]

def run_diagnostics():
    print("=" * 80)
    print("BIORAG RETRIEVAL & ANSWER GENERATION DIAGNOSTIC")
    print("=" * 80)

    t0 = time.time()
    all_chunks = load_all_chunks()
    print(f"\n[+] Total chunks in database_kntt: {len(all_chunks)} (loaded in {time.time() - t0:.2f}s)")

    diagnostics = []

    for test in TEST_QUESTIONS:
        qid = test["id"]
        q = test["query"]
        req_g = test["grade"]
        q_type = test["type"]
        target_pages = test["target_pages"]

        print("\n" + "=" * 80)
        print(f"[{qid}] QUERY: '{q}' | Grade: {req_g} | Type: {q_type}")
        print(f"Target Lesson: {test['target_lesson']} | Target Pages: {target_pages}")
        print("-" * 80)

        # 1. Lesson Scope Check
        scope = _biorag_chat_lesson_scope(q, req_g)
        print(f"[*] Detected Lesson Scope: {scope}")

        # 2. Candidate Filtering
        candidates = all_chunks
        if req_g is not None:
            candidates = [c for c in all_chunks if _biorag_quiz_chunk_grade(c) == req_g]
        print(f"[*] Candidates in grade {req_g}: {len(candidates)}")

        # 3. BM25 / Lexical Ranking - Top 10
        ranked = _biorag_rank_chat_chunks(q, candidates, lesson_scope=scope, limit=10)
        print(f"\n[*] Top {len(ranked)} Retrieved Chunks (Lexical/BM25):")
        top_10_info = []
        for rank, (score, chunk) in enumerate(ranked, 1):
            text, src, pg = _biorag_quiz_chunk_fields(chunk)
            snippet = text.replace("\n", " ").strip()[:140]
            print(f"  #{rank} [Score {score:4.1f}] {src} | Trang {pg} -> {snippet}...")
            top_10_info.append({
                "rank": rank,
                "score": score,
                "source": src,
                "page": pg,
                "snippet": snippet
            })

        # 4. Context Extraction (Blocks actually passed to LLM)
        t_ctx_start = time.time()
        context = _biorag_load_chat_context([q], req_g, lesson_scope=scope)
        t_ctx_ms = (time.time() - t_ctx_start) * 1000

        print(f"\n[*] Context Passed to LLM Context Window ({len(context)} blocks, retrieval {t_ctx_ms:.1f}ms):")
        for idx, ctx in enumerate(context, 1):
            print(f"  [S{idx}] {ctx['source']} - Trang {ctx['page']}: {ctx['text'][:100].replace(chr(10), ' ')}...")

        # 5. Full Grounded Answer Generation
        t_ans_start = time.time()
        try:
            payload, status = _biorag_answer_grounded_question(q, req_g, [])
            ans_ms = (time.time() - t_ans_start) * 1000
            answer = payload.get("answer", "")
            sources = payload.get("sources", [])
        except Exception as exc:
            ans_ms = (time.time() - t_ans_start) * 1000
            status = 500
            answer = f"ERROR: {exc}"
            sources = []

        print(f"\n[*] Answer Generation (Status: {status}, Latency: {ans_ms:.1f}ms):")
        print(f"--- GENERATED ANSWER ---\n{answer}\n------------------------")
        print(f"[*] Cited Sources: {sources}")

        # Check retrieval recall@5
        retrieved_pages = [info["page"] for info in top_10_info[:5]]
        hit_r5 = any(p in target_pages for p in retrieved_pages) if target_pages else False

        diagnostics.append({
            "id": qid,
            "query": q,
            "grade": req_g,
            "type": q_type,
            "target_lesson": test["target_lesson"],
            "target_pages": target_pages,
            "scope_detected": scope,
            "top_10_chunks": top_10_info,
            "context_blocks": [{"source": c["source"], "page": c["page"]} for c in context],
            "answer": answer,
            "sources": sources,
            "recall_at_5": hit_r5,
            "latency_ms": ans_ms
        })

    os.makedirs("scratch", exist_ok=True)
    with open("scratch/baseline_eval_report.json", "w", encoding="utf-8") as f:
        json.dump(diagnostics, f, ensure_ascii=False, indent=2)
    print("\n[+] Full diagnostic results saved to scratch/baseline_eval_report.json")

if __name__ == "__main__":
    run_diagnostics()
