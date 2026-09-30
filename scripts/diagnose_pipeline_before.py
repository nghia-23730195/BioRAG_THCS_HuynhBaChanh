# -*- coding: utf-8 -*-
"""Diagnostic script to test retrieval and answer generation on the baseline RAG pipeline."""

import os
import sys
import io
import json
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Ensure root is in sys.path
sys.path.insert(0, os.path.abspath("."))

from src.rag.book_rag import load_all_chunks
from src.app.api import (
    _biorag_load_chat_context,
    _biorag_chat_tokens,
    _biorag_normalize_search_text,
    _biorag_rank_chat_chunks,
    _biorag_chat_lesson_scope,
    _biorag_answer_grounded_question,
    _biorag_quiz_chunk_fields,
    _biorag_quiz_chunk_grade,
)
from src.rag.vectorstore import VectorDB

TEST_QUESTIONS = [
    {"query": "Nhóm cây ưa sáng là gì?", "grade": 7, "expected_topic": "Bài 23 KHTN 7 (Trang 104-107)", "type": "in_scope"},
    {"query": "Tế bào nhân sơ khác tế bào nhân thực ở điểm nào?", "grade": 6, "expected_topic": "Bài 19 KHTN 6 (Trang 65-68)", "type": "in_scope"},
    {"query": "Định luật bảo toàn khối lượng phát biểu như thế nào?", "grade": 8, "expected_topic": "Bài 5 KHTN 8 (Trang 24-27)", "type": "in_scope"},
    {"query": "Hiện tượng tán sắc ánh sáng là gì?", "grade": 9, "expected_topic": "Bài 7 KHTN 9 (Trang 31-34)", "type": "in_scope"},
    {"query": "Thủ đô của nước Pháp là thành phố nào?", "grade": None, "expected_topic": "Ngoài phạm vi SGK", "type": "out_of_scope"},
]

def run_diagnostics():
    print("="*80, flush=True)
    print("BIORAG PIPELINE DIAGNOSTIC (BASELINE)", flush=True)
    print("="*80, flush=True)

    # 1. Inspect ChromaDB Text Collection Chunks
    all_chunks = load_all_chunks()
    print(f"\n[1] ChromaDB Status: Total chunks loaded = {len(all_chunks)}", flush=True)
    
    grade_counts = {}
    for c in all_chunks:
        g = _biorag_quiz_chunk_grade(c)
        grade_counts[g] = grade_counts.get(g, 0) + 1
    print(f"    Grade distribution: {grade_counts}", flush=True)

    # 2. Test VectorDB
    try:
        vector_db = VectorDB()
        print(f"    VectorDB loaded successfully. Collection count = {vector_db.db._collection.count()}", flush=True)
    except Exception as exc:
        print(f"    VectorDB loading error: {exc}", flush=True)
        vector_db = None

    results = []

    for item in TEST_QUESTIONS:
        q = item["query"]
        req_g = item["grade"]
        q_type = item["type"]
        expected = item["expected_topic"]

        print("\n" + "="*80, flush=True)
        print(f"TEST QUERY: '{q}' (Grade: {req_g}, Type: {q_type})", flush=True)
        print(f"Expected: {expected}", flush=True)
        print("="*80, flush=True)

        # A. Test Lesson Scope detection
        scope = _biorag_chat_lesson_scope(q, req_g)
        print(f"[*] Detected Lesson Scope: {scope}", flush=True)

        # B. Test Lexical / BM25 Ranking
        candidates = all_chunks
        if req_g is not None:
            candidates = [c for c in all_chunks if _biorag_quiz_chunk_grade(c) == req_g]
        
        ranked = _biorag_rank_chat_chunks(q, candidates, lesson_scope=scope, limit=10)
        print(f"\n[*] Top {len(ranked)} Lexical/BM25 Retrieved Chunks:", flush=True)
        for idx, (score, chunk) in enumerate(ranked, 1):
            text, src, pg = _biorag_quiz_chunk_fields(chunk)
            snippet = text.replace("\n", " ")[:120]
            print(f"    [{idx}] Score={score:.1f} | Source={src} | Page={pg} | Text={snippet}...", flush=True)

        # C. Test Vector / Embedding Search if available
        if vector_db:
            try:
                retriever = vector_db.get_retriever({"k": 5})
                v_docs = retriever.invoke(q)
                print(f"\n[*] Top {len(v_docs)} Vector (Embedding) Retrieved Docs:", flush=True)
                for idx, doc in enumerate(v_docs[:5], 1):
                    src = doc.metadata.get("source") or doc.metadata.get("pdf_filename") or "SGK"
                    pg = doc.metadata.get("page") or doc.metadata.get("page_number") or "?"
                    snippet = doc.page_content.replace("\n", " ")[:120]
                    print(f"    [{idx}] Source={src} | Page={pg} | Text={snippet}...", flush=True)
            except Exception as ve:
                print(f"    Vector retrieval failed: {ve}", flush=True)

        # D. Test Context Loading in _biorag_load_chat_context
        start_t = time.time()
        context = _biorag_load_chat_context([q], req_g, lesson_scope=scope)
        retrieval_ms = (time.time() - start_t) * 1000
        print(f"\n[*] Context Selected for LLM ({len(context)} blocks, retrieval time {retrieval_ms:.1f}ms):", flush=True)
        for idx, ctx in enumerate(context, 1):
            print(f"    [S{idx} | {ctx['source']} | Trang {ctx['page']}]: {ctx['text'][:100].replace(chr(10), ' ')}...", flush=True)

        # E. Test Full Grounded Answer Generation
        start_ans_t = time.time()
        payload, status = _biorag_answer_grounded_question(q, req_g, [])
        total_ms = (time.time() - start_ans_t) * 1000

        print(f"\n[*] HTTP Status: {status} | Total Latency: {total_ms:.1f}ms", flush=True)
        print(f"[*] Generated Answer:\n{payload.get('answer', '')}\n", flush=True)
        print(f"[*] Sources Cited: {payload.get('sources', [])}", flush=True)
        
        results.append({
            "question": q,
            "grade": req_g,
            "type": q_type,
            "expected": expected,
            "top_10_chunks": [
                {
                    "rank": idx,
                    "score": float(score),
                    "source": str(_biorag_quiz_chunk_fields(chunk)[1]),
                    "page": str(_biorag_quiz_chunk_fields(chunk)[2]),
                    "text": str(_biorag_quiz_chunk_fields(chunk)[0])[:200]
                }
                for idx, (score, chunk) in enumerate(ranked, 1)
            ],
            "context_sent_to_model": [
                {"source": c["source"], "page": c["page"], "text": c["text"][:200]}
                for c in context
            ],
            "answer": payload.get("answer", ""),
            "sources": payload.get("sources", []),
            "latency_ms": total_ms
        })

    os.makedirs("scratch", exist_ok=True)
    with open("scratch/baseline_diagnostic_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\nSaved baseline diagnostics to scratch/baseline_diagnostic_results.json", flush=True)

if __name__ == "__main__":
    run_diagnostics()
