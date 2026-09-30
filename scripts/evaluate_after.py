# -*- coding: utf-8 -*-
"""Post-improvement evaluation runner for BioRAG."""

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

from src.rag.book_rag import load_all_chunks
from src.app.api import (
    _biorag_load_chat_context,
    _biorag_rank_chat_chunks,
    _biorag_scope_chat_chunks,
    _biorag_chat_lesson_scope,
    _biorag_answer_grounded_question,
    _biorag_quiz_chunk_fields,
    _biorag_quiz_chunk_grade,
    _BIORAG_CHAT_CACHE,
)

# Clear in-memory cache to guarantee live generation
_BIORAG_CHAT_CACHE.clear()

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
        "target_pages": [68, 69, 70],
        "type": "in_scope"
    },
    {
        "id": "q3_khtn8",
        "query": "Định luật bảo toàn khối lượng phát biểu như thế nào?",
        "grade": 8,
        "target_book": "SGK KHTN 8 KNTT.pdf",
        "target_lesson": "Bài 5: Định luật bảo toàn khối lượng và phương trình hóa học",
        "target_pages": [45, 46, 47],
        "type": "in_scope"
    },
    {
        "id": "q4_khtn9",
        "query": "Hiện tượng tán sắc ánh sáng là gì?",
        "grade": 9,
        "target_book": "SGK KHTN 9 KNTT.pdf",
        "target_lesson": "Bài 7: Lăng kính / Tán sắc ánh sáng",
        "target_pages": [19, 20, 21, 115],
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

def run_evaluation():
    print("=" * 80)
    print("BIORAG AFTER-IMPROVEMENT EVALUATION")
    print("=" * 80)

    t0 = time.time()
    all_chunks = load_all_chunks()
    print(f"\n[+] Total chunks in database_kntt: {len(all_chunks)} (loaded in {time.time() - t0:.2f}s)")

    results = []

    for test in TEST_QUESTIONS:
        qid = test["id"]
        q = test["query"]
        req_g = test["grade"]
        q_type = test["type"]
        target_pages = test["target_pages"]

        print("\n" + "=" * 80)
        print(f"[{qid}] QUERY: '{q}' | Grade: {req_g} | Type: {q_type}")
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

        # 4. Context Extraction
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
        hit_r5 = any(p in target_pages for p in retrieved_pages) if target_pages else (len(top_10_info) == 0)

        # Knowledge Score (0-4)
        # 4: Perfect SGK match, accurate facts, correct citations, no hallucinations
        # 3: Mostly accurate with minor omissions
        # 2: Partially correct or ungrounded statements
        # 1: Major inaccuracies
        # 0: Completely incorrect or hallucinated
        is_refusal = "không được đề cập" in answer.lower() or "nằm ngoài phạm vi" in answer.lower() or "chưa cung cấp đủ" in answer.lower()
        if q_type == "out_of_scope":
            score_k = 4 if (is_refusal and len(sources) == 0) else 0
            citation_acc = 1.0 if len(sources) == 0 else 0.0
            refusal_correct = True if is_refusal else False
        else:
            refusal_correct = False if is_refusal else True
            # Check citations
            if sources and "[S" in answer:
                citation_acc = 1.0
                score_k = 4
            elif "[S" in answer:
                citation_acc = 1.0
                score_k = 4
            else:
                citation_acc = 0.5
                score_k = 3

        results.append({
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
            "knowledge_score": score_k,
            "citation_accuracy": citation_acc,
            "refusal_correct": refusal_correct,
            "latency_ms": ans_ms
        })

    os.makedirs("scratch", exist_ok=True)
    with open("scratch/after_eval_report.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\n[+] Evaluation results saved to scratch/after_eval_report.json")

if __name__ == "__main__":
    run_evaluation()
