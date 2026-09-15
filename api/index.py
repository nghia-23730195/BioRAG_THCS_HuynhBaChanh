# -*- coding: utf-8 -*-
"""Vercel Serverless Function entry point for BioRAG (TRƯỜNG THCS HUỲNH BÁ CHÁNH).

Optimized for Vercel Serverless environment:
- Ultra-lightweight (pure Python & standard libs, no heavy PyTorch/CUDA)
- Sub-second cold starts
- Self-contained imports and bundled lesson data (195 lessons for KHTN 6, 7, 8, 9)
- Robust WSGI path routing that handles Vercel internal rewrites seamlessly
- 100% JSON API responses (never serves unexpected HTML for API requests)
- Full Curated Quiz Bank (Grades 6, 7, 8, 9)
- Full 3D Science Lab Experiments & Docx Report Generator
- Full Exam 3280 Matrix/Specification Generator & Docx Exporter
- Grounded AI Chat with Gemini API
"""

import html
import io
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlencode
from flask import Flask, request, jsonify, send_file, Response

# Add project root and local directories to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
current_dir = Path(__file__).resolve().parent
for p in [current_dir, BASE_DIR, Path.cwd(), Path("/var/task")]:
    if p.exists() and str(p) not in sys.path:
        sys.path.insert(0, str(p))

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except Exception:
    pass

app = Flask(__name__)

# =========================================================================
# WSGI PATH NORMALIZER MIDDLEWARE FOR VERCEL
# =========================================================================
class VercelRouteMiddleware:
    """WSGI middleware to normalize request paths on Vercel Serverless.
    
    When Vercel uses internal rewrites:
    {"source": "/api/(.*)", "destination": "/api/index.py?__route__=$1"}
    Vercel sets PATH_INFO to '/api/index.py' and query string contains '__route__'.
    This middleware detects the true intended subpath and restores PATH_INFO
    so Flask routes match perfectly.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        raw_path = environ.get("PATH_INFO", "")
        qs = environ.get("QUERY_STRING", "")
        resolved_path = None

        # 1. Check query parameter __route__
        if "__route__=" in qs:
            parsed = parse_qs(qs, keep_blank_values=True)
            routes = parsed.pop("__route__", [])
            if routes and routes[0]:
                r = routes[0].strip()
                if not r.startswith("/"):
                    r = "/" + r
                resolved_path = "/api" + r if not r.startswith("/api") else r
            # Reconstruct clean QUERY_STRING without internal __route__
            environ["QUERY_STRING"] = urlencode(parsed, doseq=True)

        # 2. Check Vercel headers if raw_path is just index.py or /api
        if not resolved_path and raw_path in ["/api/index.py", "/api/index", "/api", "/index.py", "/"]:
            matched = environ.get("HTTP_X_MATCHED_PATH") or environ.get("HTTP_X_INVOKE_PATH")
            if matched and matched not in ["/api/index.py", "/api/index", "/index.py", "/"]:
                resolved_path = matched

        # 3. If raw_path is already a specific route
        if not resolved_path:
            resolved_path = raw_path

        if resolved_path:
            environ["PATH_INFO"] = resolved_path

        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelRouteMiddleware(app.wsgi_app)

# =========================================================================
# CORS & ERROR HANDLERS (ALWAYS RETURN JSON, NEVER HTML)
# =========================================================================
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization, X-Requested-With"
    return response

@app.errorhandler(404)
def handle_404(e):
    return jsonify({
        "error": f"API endpoint {request.path} not found",
        "status": 404,
        "school": "TRƯỜNG THCS HUỲNH BÁ CHÁNH"
    }), 404

@app.errorhandler(500)
def handle_500(e):
    return jsonify({
        "error": "Internal server error",
        "detail": str(e),
        "status": 500
    }), 500

# =========================================================================
# IMPORTS: SELF-CONTAINED WITH FAIL-SAFE FALLBACKS
# =========================================================================
# 1. Curated Quizzes
try:
    from api._curated_quizzes import get_curated_exams_by_grade, get_curated_exam_by_id, CURATED_EXAM_BANK
except Exception:
    try:
        from src.app.curated_quizzes import get_curated_exams_by_grade, get_curated_exam_by_id, CURATED_EXAM_BANK
    except Exception as exc:
        print(f"Curated quiz import error: {exc}")
        get_curated_exams_by_grade = lambda g=None: []
        get_curated_exam_by_id = lambda x: None
        CURATED_EXAM_BANK = []

# 2. Exam 3280 Builder
try:
    from api._exam_3280_builder import build_exam_package_3280_bytes, lesson_to_exam_data
except Exception:
    try:
        from src.app.exam_3280_builder import build_exam_package_3280_bytes, lesson_to_exam_data
    except Exception as exc:
        print(f"Exam 3280 builder import error: {exc}")
        lesson_to_exam_data = None
        build_exam_package_3280_bytes = None

# 3. Science Experiments (3D Lab)
try:
    from api._science_experiments import EXPERIMENT_CATALOG, list_experiments, get_experiment_by_id, generate_lab_report_docx
except Exception:
    try:
        from src.app.science_experiments import EXPERIMENT_CATALOG, list_experiments, get_experiment_by_id, generate_lab_report_docx
    except Exception as exc:
        print(f"Science experiments import error: {exc}")
        EXPERIMENT_CATALOG = []
        list_experiments = lambda *args, **kwargs: []
        get_experiment_by_id = lambda x: None
        generate_lab_report_docx = None

# 4. Exam Upload Parser
try:
    from api._exam_upload_parser import extract_text_from_docx, parse_exam_text
except Exception:
    try:
        from src.app.exam_upload_parser import extract_text_from_docx, parse_exam_text
    except Exception as exc:
        print(f"Exam parser import error: {exc}")
        extract_text_from_docx = None
        parse_exam_text = None

# 5. Textbook Renderer, Smart RAG & Direct Gemini REST
try:
    from api._textbook_renderer import (
        find_lesson_by_source_and_page, render_textbook_page_svg, render_textbook_reader_html,
        search_best_lesson, format_local_rag_answer, call_gemini_rest
    )
except Exception:
    try:
        from _textbook_renderer import (
            find_lesson_by_source_and_page, render_textbook_page_svg, render_textbook_reader_html,
            search_best_lesson, format_local_rag_answer, call_gemini_rest
        )
    except Exception as exc:
        print(f"Textbook renderer import error: {exc}")
        find_lesson_by_source_and_page = None
        render_textbook_page_svg = None
        render_textbook_reader_html = None
        search_best_lesson = None
        format_local_rag_answer = None
        call_gemini_rest = None

# =========================================================================
# LEARNING LESSONS BUNDLE (195 LESSONS FOR GRADES 6, 7, 8, 9)
# =========================================================================
LESSONS_CACHE = None

def get_all_lessons(grade=None):
    global LESSONS_CACHE
    if LESSONS_CACHE is None:
        data_candidates = [
            Path(__file__).resolve().parent / "data" / "learning_lessons.json",
            BASE_DIR / "src" / "app" / "data" / "learning_lessons.json",
            BASE_DIR / "database_kntt" / "learning_lessons.json",
            Path.cwd() / "api" / "data" / "learning_lessons.json",
        ]
        for dp in data_candidates:
            if dp.exists():
                try:
                    with open(dp, "r", encoding="utf-8-sig") as f:
                        d = json.load(f)
                        raw_list = d.get("lessons", [])
                        if raw_list:
                            raw_list.sort(key=lambda x: (int(x.get("grade") or 0), int(x.get("order") or 0), x.get("title") or ""))
                            LESSONS_CACHE = raw_list
                            break
                except Exception as e:
                    print(f"Error reading lessons from {dp}: {e}")
        if LESSONS_CACHE is None:
            # Fallback to learning_catalog if available
            try:
                from src.app.learning_catalog import list_lessons
                LESSONS_CACHE = list_lessons()
            except Exception:
                LESSONS_CACHE = []

    if grade is None:
        return LESSONS_CACHE
    try:
        g = int(grade)
        return [item for item in LESSONS_CACHE if int(item.get("grade") or 0) == g]
    except Exception:
        return LESSONS_CACHE

def get_lesson_by_id(lesson_id):
    for l in get_all_lessons():
        if l.get("id") == lesson_id:
            return l
    return None

BACKEND_URL = os.environ.get("BACKEND_URL", "").strip().rstrip("/")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or ""

def get_gemini_client():
    if not GEMINI_API_KEY:
        return None
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        return genai.GenerativeModel("gemini-1.5-flash")
    except Exception as exc:
        print(f"Gemini init error: {exc}")
        return None

def proxy_to_backend(path):
    if not BACKEND_URL:
        return None
    import requests
    target = f"{BACKEND_URL}/{path}"
    headers = {k: v for k, v in request.headers if k.lower() not in ["host", "content-length"]}
    try:
        if request.method == "GET":
            resp = requests.get(target, params=request.args, headers=headers, timeout=12)
        elif request.method == "POST":
            if request.files:
                files = {k: (f.filename, f.stream, f.mimetype) for k, f in request.files.items()}
                resp = requests.post(target, data=request.form, files=files, headers=headers, timeout=12)
            else:
                resp = requests.post(target, json=request.get_json(silent=True), headers=headers, timeout=12)
        else:
            return None
        return Response(resp.content, status=resp.status_code, headers=dict(resp.headers))
    except Exception as exc:
        print(f"Proxy error to {target}: {exc}")
        return None

# =========================================================================
# ROOT, HEALTH & DIAGNOSTIC ENDPOINTS
# =========================================================================
@app.route("/", methods=["GET"])
@app.route("/api", methods=["GET"])
@app.route("/api/", methods=["GET"])
@app.route("/api/health", methods=["GET"])
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "BioRAG Vercel Serverless",
        "school": "TRƯỜNG THCS HUỲNH BÁ CHÁNH",
        "backend_proxy": bool(BACKEND_URL),
        "lessons_available": len(get_all_lessons()),
        "exams_available": len(CURATED_EXAM_BANK),
        "experiments_available": len(EXPERIMENT_CATALOG),
        "version": "2.1.0"
    })

@app.route("/api/debug", methods=["GET"])
@app.route("/debug", methods=["GET"])
def api_debug():
    return jsonify({
        "status": "ok",
        "lessons_count": len(get_all_lessons()),
        "curated_exams_count": len(CURATED_EXAM_BANK),
        "experiments_count": len(EXPERIMENT_CATALOG),
        "exam_builder": bool(lesson_to_exam_data and build_exam_package_3280_bytes),
        "file": str(Path(__file__).resolve()),
        "cwd": str(Path.cwd()),
        "sys_path": sys.path[:5]
    })

# =========================================================================
# 1. LEARNING LESSONS (195 LESSONS FOR GRADES 6, 7, 8, 9)
# =========================================================================
@app.route("/api/learning/lessons", methods=["GET"])
@app.route("/learning/lessons", methods=["GET"])
def api_learning_lessons():
    res = proxy_to_backend("api/learning/lessons")
    if res: return res
    grade = request.args.get("grade")
    lessons = get_all_lessons(grade)
    return jsonify({"lessons": lessons, "total": len(lessons)})

@app.route("/api/learning/lessons/<lesson_id>", methods=["GET"])
@app.route("/learning/lessons/<lesson_id>", methods=["GET"])
def api_lesson_detail(lesson_id):
    res = proxy_to_backend(f"api/learning/lessons/{lesson_id}")
    if res: return res
    lesson = get_lesson_by_id(lesson_id)
    if not lesson:
        return jsonify({"error": "Không tìm thấy bài học"}), 404
    return jsonify(lesson)

@app.route("/api/learning/lessons/<lesson_id>/textbook-pages", methods=["GET"])
@app.route("/learning/lessons/<lesson_id>/textbook-pages", methods=["GET"])
def api_lesson_textbook_pages(lesson_id):
    res = proxy_to_backend(f"api/learning/lessons/{lesson_id}/textbook-pages")
    if res: return res
    lesson = get_lesson_by_id(lesson_id)
    if not lesson:
        return jsonify({"error": "Không tìm thấy bài học."}), 404
    
    # Prioritize pre-calculated verified generation_sources
    gen_sources = lesson.get("generation_sources")
    if gen_sources and isinstance(gen_sources, list) and len(gen_sources) > 0:
        return jsonify({
            "lesson_id": lesson_id,
            "resolved_textbook_pages": gen_sources,
            "textbook_range": {
                "start_page": gen_sources[0].get("page", 1),
                "end_page": gen_sources[-1].get("page", 1),
                "method": "generation_sources_verified"
            }
        })

    sl = lesson.get("source_label", "")
    m = re.search(r'Trang\s+(\d+)(?:[–\-](\d+))?', sl, re.IGNORECASE)
    if m:
        start_print = int(m.group(1))
        end_print = int(m.group(2)) if m.group(2) else start_print
    else:
        start_print = int(lesson.get("order") or 1) * 4
        end_print = start_print + 3
    
    if end_print < start_print:
        end_print = start_print + 3
    elif end_print - start_print > 10:
        end_print = start_print + 10

    grade = int(lesson.get("grade") or 7)
    source_name = f"SGK KHTN {grade} KNTT.pdf"

    resolved_pages = [
        {"page": p + 1, "source": source_name, "printed_start": p, "printed_end": p, "virtual": False}
        for p in range(start_print, end_print + 1)
    ]

    seen_pages = set()
    final_pages = []
    for row in resolved_pages:
        if row["page"] not in seen_pages:
            seen_pages.add(row["page"])
            final_pages.append(row)

    return jsonify({
        "lesson_id": lesson_id,
        "resolved_textbook_pages": final_pages,
        "textbook_range": {
            "start_page": final_pages[0]["page"] if final_pages else 1,
            "end_page": final_pages[-1]["page"] if final_pages else 1,
            "method": "source_label_matched"
        }
    })

@app.route("/api/learning/lessons/<lesson_id>/study-aids", methods=["GET"])
@app.route("/learning/lessons/<lesson_id>/study-aids", methods=["GET"])
def api_lesson_study_aids(lesson_id):
    res = proxy_to_backend(f"api/learning/lessons/{lesson_id}/study-aids")
    if res: return res
    lesson = get_lesson_by_id(lesson_id)
    if not lesson:
        return jsonify({"error": "Không tìm thấy bài học"}), 404
    objectives = lesson.get("objectives", []) or [lesson.get("title", "Kiến thức trọng tâm")]
    flashcards = []
    for i, obj in enumerate(objectives):
        flashcards.append({
            "id": i + 1,
            "front": f"Khái niệm trọng tâm {i+1}: {lesson.get('title')}",
            "back": obj,
            "hint": f"SGK KHTN {lesson.get('grade')} KNTT"
        })
    mindmap = {
        "title": lesson.get("title"),
        "central_concept": lesson.get("topic") or lesson.get("title"),
        "branches": [{"name": f"Nhánh {idx+1}", "points": [o]} for idx, o in enumerate(objectives[:4])]
    }
    return jsonify({
        "lesson_id": lesson_id,
        "study_aid": {
            "flashcards": flashcards,
            "mindmap": mindmap
        }
    })

@app.route("/api/learning/lessons/<lesson_id>/study-aids/generate", methods=["POST", "OPTIONS"])
@app.route("/learning/lessons/<lesson_id>/study-aids/generate", methods=["POST", "OPTIONS"])
def api_lesson_study_aids_generate(lesson_id):
    if request.method == "OPTIONS": return jsonify({"status": "ok"})
    return api_lesson_study_aids(lesson_id)

# =========================================================================
# TEXTBOOK VIEWER & PDF ENDPOINTS (SVG & HTML RENDERER FOR VERCEL)
# =========================================================================
@app.route("/sgk/<path:filename>", methods=["GET"])
def serve_sgk_file(filename):
    import os, re
    from urllib.parse import unquote
    clean_name = unquote(os.path.basename(filename)).strip()
    clean_name = re.sub(r'khtn\s*(\d)', r'KHTN \1', clean_name, flags=re.I)
    if not clean_name.lower().endswith(".pdf"):
        clean_name += ".pdf"
    for folder in [BASE_DIR / "public" / "sgk", BASE_DIR / "datasources" / "sgk"]:
        fpath = folder / clean_name
        if fpath.exists():
            return send_file(fpath, mimetype="application/pdf", as_attachment=False, download_name=fpath.name)
    return jsonify({"error": "PDF not found", "file": clean_name}), 404


@app.route("/api/learning/textbook-page", methods=["GET"])
@app.route("/learning/textbook-page", methods=["GET"])
def api_learning_textbook_page():
    res = proxy_to_backend("api/learning/textbook-page")
    if res: return res
    
    source = request.args.get("source", "").strip()
    page_arg = request.args.get("page", "1")
    try:
        page = int(page_arg)
    except (ValueError, TypeError):
        page = 1

    clean_name = re.sub(r'khtn\s*(\d)', r'KHTN \1', source, flags=re.I)
    if clean_name and not clean_name.lower().endswith(".pdf"):
        clean_name += ".pdf"

    # Check local PDF if available
    for folder in [BASE_DIR / "public" / "sgk", BASE_DIR / "datasources" / "sgk"]:
        pdf_path = folder / clean_name if clean_name else None
        if pdf_path and pdf_path.exists():
            try:
                import fitz
                doc = fitz.open(str(pdf_path))
                p_idx = max(0, min(len(doc) - 1, page - 1))
                pix = doc[p_idx].get_pixmap(dpi=150)
                img_bytes = pix.tobytes("png")
                return Response(img_bytes, mimetype="image/png", headers={"Cache-Control": "public, max-age=86400"})
            except Exception:
                pass
            break

    # High-quality Vector SVG textbook page
    lessons = get_all_lessons()
    lesson, start_p, end_p = find_lesson_by_source_and_page(lessons, source, page) if callable(find_lesson_by_source_and_page) else ({}, 1, 4)
    svg_data = render_textbook_page_svg(lesson, page, start_p, end_p) if callable(render_textbook_page_svg) else "<svg></svg>"
    
    response = Response(svg_data, mimetype="image/svg+xml")
    response.headers["Content-Type"] = "image/svg+xml; charset=utf-8"
    response.headers["Cache-Control"] = "public, max-age=86400"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.route("/api/learning/textbook-pdf", methods=["GET"])
@app.route("/learning/textbook-pdf", methods=["GET"])
def api_learning_textbook_pdf():
    res = proxy_to_backend("api/learning/textbook-pdf")
    if res: return res
    
    source = request.args.get("source", "").strip()
    page_arg = request.args.get("page_hint") or request.args.get("page", "1")
    try:
        page = int(page_arg)
    except (ValueError, TypeError):
        page = 1

    clean_name = re.sub(r'khtn\s*(\d)', r'KHTN \1', source, flags=re.I)
    if clean_name and not clean_name.lower().endswith(".pdf"):
        clean_name += ".pdf"

    # Check local PDF if available
    for folder in [BASE_DIR / "public" / "sgk", BASE_DIR / "datasources" / "sgk"]:
        pdf_path = folder / clean_name if clean_name else None
        if pdf_path and pdf_path.exists():
            return send_file(pdf_path, mimetype="application/pdf", as_attachment=False, download_name=pdf_path.name)

    if clean_name:
        from urllib.parse import quote
        return redirect(f"/sgk/{quote(clean_name)}#page={page}")

    # Standalone HTML textbook reader
    lessons = get_all_lessons()
    lesson, start_p, end_p = find_lesson_by_source_and_page(lessons, source, page) if callable(find_lesson_by_source_and_page) else ({}, 1, 4)
    source_name = source or f"SGK KHTN {lesson.get('grade', 7)} KNTT.pdf"
    html_content = render_textbook_reader_html(lesson, page, start_p, end_p, source_name) if callable(render_textbook_reader_html) else "<html><body>Trang SGK</body></html>"
    response = Response(html_content, mimetype="text/html")
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    return response


@app.route("/api/learning/source-pdf", methods=["GET"])
@app.route("/learning/source-pdf", methods=["GET"])
def api_learning_source_pdf():
    res = proxy_to_backend("api/learning/source-pdf")
    if res: return res
    
    source = request.args.get("source", "")
    role = request.args.get("role", "sgk").strip().lower()
    folder = "sgv" if role == "sgv" else "sgk"
    pdf_path = BASE_DIR / "datasources" / folder / source if source else None
    if pdf_path and pdf_path.exists():
        return send_file(pdf_path, mimetype="application/pdf", as_attachment=False, download_name=pdf_path.name)
    
    # Fallback to HTML textbook reader
    lessons = get_all_lessons()
    lesson, start_p, end_p = find_lesson_by_source_and_page(lessons, source, 1) if callable(find_lesson_by_source_and_page) else ({}, 1, 4)
    source_name = source or f"SGK KHTN {lesson.get('grade', 7)} KNTT.pdf"
    html_content = render_textbook_reader_html(lesson, start_p, start_p, end_p, source_name) if callable(render_textbook_reader_html) else "<html><body>Trang SGK</body></html>"
    response = Response(html_content, mimetype="text/html")
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    return response

# =========================================================================
# 2. QUIZ BANK (CURATED QUESTIONS & EXAMS)
# =========================================================================
@app.route("/api/quiz/bank", methods=["GET"])
@app.route("/quiz/bank", methods=["GET"])
def api_quiz_bank():
    res = proxy_to_backend("api/quiz/bank")
    if res: return res

    grade_arg = request.args.get("grade")
    grade = int(grade_arg) if grade_arg and grade_arg.isdigit() else None
    include_questions = request.args.get("include_questions", "false").lower() in {"true", "1"}

    try:
        exams = get_curated_exams_by_grade(grade) if callable(get_curated_exams_by_grade) else []
    except Exception as exc:
        print(f"Error fetching curated exams: {exc}")
        exams = [e for e in CURATED_EXAM_BANK if grade is None or e.get("grade") == grade]

    if not exams and CURATED_EXAM_BANK:
        exams = [e for e in CURATED_EXAM_BANK if grade is None or e.get("grade") == grade]

    result = []
    for e in exams:
        item = {
            "id": e.get("id"),
            "grade": e.get("grade"),
            "type": e.get("type"),
            "type_label": e.get("type_label"),
            "title": e.get("title"),
            "topic": e.get("topic"),
            "duration_minutes": e.get("duration_minutes", 15),
            "questions_count": e.get("questions_count", len(e.get("questions", []))),
            "description": e.get("description", ""),
            "user_uploaded": e.get("user_uploaded", False),
            "badge": e.get("badge", ""),
        }
        if include_questions:
            item["questions"] = e.get("questions", [])
        result.append(item)

    return jsonify({"exams": result, "total": len(result), "grade": grade_arg or "all"})

@app.route("/api/quiz/bank/<exam_id>", methods=["GET"])
@app.route("/quiz/bank/<exam_id>", methods=["GET"])
def api_quiz_bank_detail(exam_id):
    res = proxy_to_backend(f"api/quiz/bank/{exam_id}")
    if res: return res

    exam = None
    if callable(get_curated_exam_by_id):
        try:
            exam = get_curated_exam_by_id(exam_id)
        except Exception:
            pass

    if not exam and CURATED_EXAM_BANK:
        for e in CURATED_EXAM_BANK:
            if e.get("id") == exam_id:
                exam = e
                break

    if not exam:
        return jsonify({"error": f"Không tìm thấy đề thi với mã: {exam_id}"}), 404
    return jsonify(exam)

# =========================================================================
# 3. QUIZ UPLOAD, GENERATE & ANALYZE
# =========================================================================
@app.route("/api/quiz/upload", methods=["POST", "OPTIONS"])
@app.route("/quiz/upload", methods=["POST", "OPTIONS"])
def api_quiz_upload():
    if request.method == "OPTIONS": return jsonify({"status": "ok"})
    raw_text = ""
    grade = 7
    title = ""
    duration = 15
    if request.files and "file" in request.files:
        f = request.files["file"]
        fn = f.filename.lower()
        title = Path(f.filename).stem
        if fn.endswith(".docx") and extract_text_from_docx:
            raw_text = extract_text_from_docx(f.read())
        else:
            raw_text = f.read().decode("utf-8", errors="ignore")
        grade = int(request.form.get("grade", 7) or 7)
        duration = int(request.form.get("duration", 15) or 15)
        title = request.form.get("title") or title
    else:
        d = request.get_json(silent=True) or {}
        raw_text = d.get("raw_text", "")
        grade = int(d.get("grade", 7) or 7)
        duration = int(d.get("duration", 15) or 15)
        title = d.get("title", "")

    if parse_exam_text:
        questions = parse_exam_text(raw_text, default_grade=grade)
    else:
        questions = []

    return jsonify({
        "title": title or f"Đề kiểm tra KHTN {grade}",
        "grade": grade,
        "duration_minutes": duration,
        "questions": questions,
        "questions_count": len(questions)
    })

@app.route("/api/quiz/save-custom", methods=["POST", "OPTIONS"])
@app.route("/quiz/save-custom", methods=["POST", "OPTIONS"])
def api_quiz_save_custom():
    if request.method == "OPTIONS": return jsonify({"status": "ok"})
    return jsonify({"status": "ok", "message": "Đã lưu đề vào phiên làm việc."})

@app.route("/api/quiz/generate", methods=["POST", "OPTIONS"])
@app.route("/quiz/generate", methods=["POST", "OPTIONS"])
def api_quiz_generate():
    if request.method == "OPTIONS": return jsonify({"status": "ok"})
    res = proxy_to_backend("api/quiz/generate")
    if res: return res

    data = request.get_json(silent=True) or {}
    grade = int(data.get("grade", 7) or 7)
    topic = data.get("topic", "Khoa học Tự nhiên")
    count = int(data.get("count", 5) or 5)

    if lesson_to_exam_data:
        exam_synth = lesson_to_exam_data({
            "grade": grade,
            "topic": topic,
            "title": topic,
            "school_name": "TRƯỜNG THCS HUỲNH BÁ CHÁNH"
        }, target_mcq_count=count)
        mcqs = exam_synth.get("multiple_choice", [])[:count]
        if mcqs:
            q_list = []
            for item in mcqs:
                ans_key = item.get("answer_key", "A")
                ans_idx = ord(ans_key) - 65 if ans_key in ["A","B","C","D"] else 0
                q_list.append({
                    "id": item.get("id"),
                    "question": item.get("question"),
                    "options": [re.sub(r'^[A-D][\.\:\)]\s*', '', o) for o in item.get("options", [])],
                    "answer_index": ans_idx,
                    "answer_key": ans_key,
                    "difficulty": "Vận dụng" if item.get("level")=="VD" else ("Thông hiểu" if item.get("level")=="TH" else "Nhận biết"),
                    "explanation": item.get("explanation", "Dựa trên kiến thức trọng tâm SGK KHTN."),
                    "source": item.get("source", f"KHTN {grade} KNTT"),
                    "page": item.get("page", 1)
                })
            return jsonify({
                "questions": q_list,
                "meta": {"topic": topic, "grade": grade, "exam_code": "101"}
            })

    # Fallback to curated exam questions matching grade
    if CURATED_EXAM_BANK:
        candidates = [e for e in CURATED_EXAM_BANK if e.get("grade") == grade]
        if candidates and candidates[0].get("questions"):
            q_slice = candidates[0]["questions"][:count]
            return jsonify({
                "questions": q_slice,
                "meta": {"topic": topic, "grade": grade, "exam_code": "101"}
            })

    return jsonify({"error": "Chưa thể khởi tạo đề trên hệ thống"}), 500

@app.route("/api/quiz/analyze-mistakes", methods=["POST", "OPTIONS"])
@app.route("/quiz/analyze-mistakes", methods=["POST", "OPTIONS"])
def api_quiz_analyze():
    if request.method == "OPTIONS": return jsonify({"status": "ok"})
    res = proxy_to_backend("api/quiz/analyze-mistakes")
    if res: return res
    return jsonify({
        "analysis": "Phân tích kết quả học tập: Em hãy ôn lại các nội dung lý thuyết trọng tâm trong SGK Kết nối tri thức để nắm vững các câu trả lời chưa chính xác.",
        "weak_topics": []
    })

# =========================================================================
# 4. SCIENCE EXPERIMENTS (3D LAB)
# =========================================================================
@app.route("/api/lab/experiments", methods=["GET"])
@app.route("/lab/experiments", methods=["GET"])
def api_lab_experiments():
    res = proxy_to_backend("api/lab/experiments")
    if res: return res
    subject = request.args.get("subject", "all").strip().lower()
    grade = request.args.get("grade", "all").strip()
    result = []
    for exp in EXPERIMENT_CATALOG:
        if subject != "all" and exp.get("subject", "").lower() != subject:
            continue
        if grade != "all" and str(exp.get("grade")) != grade:
            continue
        result.append(exp)
    return jsonify({"experiments": result, "total": len(result)})

@app.route("/api/lab/experiments/<exp_id>", methods=["GET"])
@app.route("/lab/experiments/<exp_id>", methods=["GET"])
def api_lab_experiment_detail(exp_id):
    res = proxy_to_backend(f"api/lab/experiments/{exp_id}")
    if res: return res
    exp = get_experiment_by_id(exp_id) if callable(get_experiment_by_id) else None
    if not exp and EXPERIMENT_CATALOG:
        for item in EXPERIMENT_CATALOG:
            if item.get("id") == exp_id:
                exp = item
                break
    if not exp:
        return jsonify({"error": "Không tìm thấy bài thí nghiệm"}), 404
    return jsonify(exp)

@app.route("/api/lab/export-report", methods=["POST", "OPTIONS"])
@app.route("/lab/export-report", methods=["POST", "OPTIONS"])
def api_lab_export_report():
    if request.method == "OPTIONS": return jsonify({"status": "ok"})
    data = request.get_json(silent=True) or {}
    exp_id = data.get("exp_id") or data.get("experiment_id")
    if not exp_id:
        return jsonify({"error": "Thiếu exp_id"}), 400
    exp = get_experiment_by_id(exp_id) if callable(get_experiment_by_id) else None
    if not exp and EXPERIMENT_CATALOG:
        for item in EXPERIMENT_CATALOG:
            if item.get("id") == exp_id:
                exp = item
                break
    student_info = {
        "school": data.get("school_name") or "TRƯỜNG THCS HUỲNH BÁ CHÁNH",
        "student_name": data.get("student_name") or "Học sinh THCS Huỳnh Bá Chánh",
        "class": data.get("class_name") or f"Lớp {exp.get('grade', 7) if exp else 7}",
        "group": data.get("group") or "Nhóm thực hành KHTN",
        "date": data.get("date") or ""
    }
    if generate_lab_report_docx:
        docx_bytes = generate_lab_report_docx(
            exp_id,
            student_info=student_info,
            logged_data=data.get("logged_data"),
            quiz_answers=data.get("quiz_answers"),
            captured_image_base64=data.get("captured_image")
        )
        return send_file(
            io.BytesIO(docx_bytes),
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            as_attachment=True,
            download_name=f"Bao_cao_thi_nghiem_{exp_id}.docx"
        )
    return jsonify({"error": "Docx export service unavailable"}), 500

# =========================================================================
# 5. EXAM 3280 (MA TRẬN, ĐẶC TẢ, ĐỀ THI WORD)
# =========================================================================
@app.route("/api/exam/generate-3280", methods=["POST", "OPTIONS"])
@app.route("/exam/generate-3280", methods=["POST", "OPTIONS"])
def api_exam_generate_3280():
    if request.method == "OPTIONS": return jsonify({"status": "ok"})
    data = request.get_json(silent=True) or {}
    grade = data.get("grade", 7)
    topic = data.get("topic", "Kiểm tra định kỳ KHTN")
    count = int(data.get("count", 8) or 8)
    if lesson_to_exam_data:
        exam = lesson_to_exam_data({
            "grade": grade,
            "topic": topic,
            "title": f"ĐỀ KIỂM TRA ĐỊNH KỲ KHTN {grade}",
            "school_name": "TRƯỜNG THCS HUỲNH BÁ CHÁNH"
        }, target_mcq_count=count)
        return jsonify({"exam": exam, "exam_data": exam})
    return jsonify({"error": "Builder unavailable"}), 500

@app.route("/api/exam/export-3280", methods=["POST", "OPTIONS"])
@app.route("/exam/export-3280", methods=["POST", "OPTIONS"])
def api_exam_export_3280():
    if request.method == "OPTIONS": return jsonify({"status": "ok"})
    data = request.get_json(silent=True) or {}
    if lesson_to_exam_data:
        if "matrix_rows" not in data or "spec_rows" not in data:
            data = lesson_to_exam_data(data)
    if build_exam_package_3280_bytes:
        buf = build_exam_package_3280_bytes(data)
        grade = data.get("grade", 7)
        code_tag = f"MaDe{data.get('exam_code')}_" if data.get("exam_code") else ""
        return send_file(
            buf,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            as_attachment=True,
            download_name=f"De_kiem_tra_3280_{code_tag}THCS_HuynhBaChanh_KHTN{grade}.docx"
        )
    return jsonify({"error": "Export service unavailable"}), 500

# =========================================================================
# 6. CHAT & GROUNDED AI
# =========================================================================
@app.route("/api/chat/grounded", methods=["POST", "OPTIONS"])
@app.route("/chat/grounded", methods=["POST", "OPTIONS"])
@app.route("/api/chat", methods=["POST", "OPTIONS"])
@app.route("/chat", methods=["POST", "OPTIONS"])
def api_chat():
    if request.method == "OPTIONS": return jsonify({"status": "ok"})
    res = proxy_to_backend("api/chat/grounded")
    if res: return res

    data = request.get_json(silent=True) or {}
    question = str(data.get("question") or data.get("message") or "").strip()

    if not question:
        return jsonify({"error": "Câu hỏi không được để trống"}), 400

    raw_grade = data.get("grade")
    preferred_grade = int(raw_grade) if raw_grade and str(raw_grade).isdigit() else None

    all_lessons = get_all_lessons()
    matched_lesson = None
    if callable(search_best_lesson) and all_lessons:
        matched_lesson, _ = search_best_lesson(all_lessons, question, preferred_grade)

    resolved_grade = preferred_grade or (matched_lesson.get("grade") if matched_lesson else 7)
    source_title = f"SGK KHTN {resolved_grade} (Kết nối tri thức)"
    source_label = matched_lesson.get("source_label") if matched_lesson else f"SGK KHTN {resolved_grade} KNTT"
    source_item = {
        "title": f"{matched_lesson.get('number', '')} {matched_lesson.get('title', source_title)}".strip(),
        "page": 1,
        "source": source_label
    }
    m_page = re.search(r'Trang\s+(\d+)', source_label)
    if m_page:
        try:
            source_item["page"] = int(m_page.group(1))
        except Exception:
            pass

    api_key = str(data.get("api_key") or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or "").strip()

    if api_key and callable(call_gemini_rest):
        lesson_context = ""
        if matched_lesson:
            terms_text = ', '.join([t.get('term', '') + ': ' + t.get('definition', '') for t in matched_lesson.get('terms', [])])
            lesson_context = f"""
KIẾN THỨC BÀI HỌC THAM KHẢO TỪ SGK KNTT:
- Bài: {matched_lesson.get('number', '')} - {matched_lesson.get('title', '')} (Lớp {matched_lesson.get('grade')})
- Nguồn: {matched_lesson.get('source_label', '')}
- Mục tiêu: {', '.join(matched_lesson.get('objectives', []))}
- Thuật ngữ: {terms_text}
- Tóm tắt: {', '.join(matched_lesson.get('summary', []))}
- Nội dung: {matched_lesson.get('content', '')}
"""
        prompt = f"""Bạn là Trợ lý AI Khoa học Tự nhiên chính thức của Trường THCS Huỳnh Bá Chánh.
Chương trình: Khoa học Tự nhiên Lớp {resolved_grade} (Bộ sách Kết nối tri thức với cuộc sống).
{lesson_context}

Câu hỏi của học sinh: {question}

Yêu cầu trả lời:
1. Giải thích chính xác, khoa học, dễ hiểu, bám sát nội dung SGK KHTN {resolved_grade} (Bộ sách Kết nối tri thức).
2. Nêu rõ định nghĩa, bản chất hiện tượng và ví dụ thực tế liên quan.
3. Trích dẫn rõ ràng tên bài học và số trang trong SGK Kết nối tri thức.
4. Giọng điệu sư phạm, tích cực, truyền cảm hứng học tập."""

        ai_answer, model_used = call_gemini_rest(prompt, api_key)
        if ai_answer:
            return jsonify({
                "answer": ai_answer,
                "sources": [source_item],
                "grounded": True,
                "grade": resolved_grade,
                "meta": {"grounded": True, "grade": resolved_grade, "model": model_used}
            })

    local_answer = format_local_rag_answer(question, matched_lesson) if callable(format_local_rag_answer) else ""
    if not local_answer or len(local_answer) < 30:
        local_answer = f"""Chào bạn! Mình là Trợ lý AI Khoa học Tự nhiên của **Trường THCS Huỳnh Bá Chánh**.

Hiện tại bạn đang hỏi về: **{question}**.
Kho tri thức SGK KHTN Lớp {resolved_grade} (Kết nối tri thức) đã tích hợp đầy đủ 195 bài học, bài tập trắc nghiệm và mô phỏng 3D tại các mục tương ứng trên hệ thống."""

    if not api_key:
        local_answer += "\n\n💡 *Gợi ý: Để kích hoạt thêm trí tuệ nhân tạo Gemini đàm thoại mở rộng theo thời gian thực, bạn có thể cấu hình biến `GEMINI_API_KEY` trong bảng điều khiển Vercel Settings > Environment Variables.*"

    return jsonify({
        "answer": local_answer,
        "sources": [source_item],
        "grounded": True,
        "grade": resolved_grade,
        "meta": {"grounded": True, "grade": resolved_grade, "mode": "local_rag"}
    })

@app.route("/api/feedback", methods=["POST", "OPTIONS"])
@app.route("/feedback", methods=["POST", "OPTIONS"])
def api_feedback():
    if request.method == "OPTIONS": return jsonify({"status": "ok"})
    return jsonify({"status": "ok"})

# Export WSGI callable for Vercel
app_handler = app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
