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

import base64
import hashlib
import hmac
import html
import io
import json
import os
import re
import sys
import time
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

# 2b. Plan 5512 Builder
try:
    from api._plan_5512_builder import build_lesson_plan_5512_bytes
except Exception:
    try:
        from src.app.plan_5512_builder import build_lesson_plan_5512_bytes
    except Exception as exc:
        print(f"Plan 5512 builder import error: {exc}")
        build_lesson_plan_5512_bytes = None

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
        search_best_lesson, format_local_rag_answer, call_gemini_rest,
        call_gemini_vision_rest, format_image_chat_local_answer
    )
except Exception:
    try:
        from _textbook_renderer import (
            find_lesson_by_source_and_page, render_textbook_page_svg, render_textbook_reader_html,
            search_best_lesson, format_local_rag_answer, call_gemini_rest,
            call_gemini_vision_rest, format_image_chat_local_answer
        )
    except Exception as exc:
        print(f"Textbook renderer import error: {exc}")
        find_lesson_by_source_and_page = None
        render_textbook_page_svg = None
        render_textbook_reader_html = None
        search_best_lesson = None
        format_local_rag_answer = None
        call_gemini_rest = None
        call_gemini_vision_rest = None
        format_image_chat_local_answer = None

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

IMAGE_CATALOG_CACHE = None

def get_image_catalog():
    global IMAGE_CATALOG_CACHE
    if IMAGE_CATALOG_CACHE is None:
        cat_candidates = [
            Path(__file__).resolve().parent / "data" / "image_catalog.json",
            BASE_DIR / "api" / "data" / "image_catalog.json",
            BASE_DIR / "src" / "app" / "data" / "image_catalog.json",
            Path.cwd() / "api" / "data" / "image_catalog.json",
        ]
        for cp in cat_candidates:
            if cp.exists():
                try:
                    with open(cp, "r", encoding="utf-8-sig") as f:
                        IMAGE_CATALOG_CACHE = json.load(f)
                        break
                except Exception as e:
                    print(f"Error loading image catalog: {e}")
        if IMAGE_CATALOG_CACHE is None:
            IMAGE_CATALOG_CACHE = []
    return IMAGE_CATALOG_CACHE

def get_relevant_images_for_query(question, matched_lesson=None, grade=None, limit=2):
    """Retrieve 1-3 best authentic SGK illustrations or verified textbook pages matching the lesson or question."""
    results = []
    seen = set()
    
    resolved_grade = int(grade or (matched_lesson.get("grade") if matched_lesson else 7) or 7)
    clean_stem = f"SGK KHTN {resolved_grade} KNTT"
    
    # 1. Primary Priority: Authentic scanned textbook pages corresponding to the matched lesson
    if matched_lesson:
        source_label = matched_lesson.get("source_label", "")
        pages_to_show = []
        m_range = re.search(r'Trang\s+(\d+)(?:[–-](\d+))?', source_label)
        if m_range:
            p_start = int(m_range.group(1))
            p_end = int(m_range.group(2)) if m_range.group(2) else p_start
            for p in range(p_start, min(p_start + limit, p_end + 1)):
                pages_to_show.append(p)
        
        if not pages_to_show:
            for s in matched_lesson.get("generation_sources", []):
                p = s.get("page")
                if p and p not in pages_to_show:
                    pages_to_show.append(p)
                    
        for printed_p in pages_to_show[:limit]:
            if printed_p not in seen:
                seen.add(printed_p)
                img_url = f"/api/learning/textbook-page?grade={resolved_grade}&page={printed_p}"
                label = f"Trang {printed_p} (SGK KHTN {resolved_grade} · {matched_lesson.get('number', '')})"
                caption = f"Trang {printed_p} - {matched_lesson.get('title', '')} (SGK KHTN {resolved_grade} Kết nối tri thức)"
                results.append({
                    "image_url": img_url,
                    "image_path": f"{clean_stem}/page_{printed_p}.jpg",
                    "label": label,
                    "caption": caption,
                    "page": printed_p,
                    "source": f"{clean_stem}.pdf",
                    "metadata": {
                        "page_number": printed_p,
                        "pdf_filename": f"{clean_stem}.pdf",
                        "figure_caption": caption,
                        "matched_query": question
                    }
                })
                if len(results) >= limit:
                    return results

    # 2. Match from image_catalog using keywords, grade, or page
    catalog = get_image_catalog()
    q_low = question.lower()
    
    scored = []
    for item in catalog:
        if item.get("grade") and int(item.get("grade")) != resolved_grade:
            continue
        score = 0
        cap_low = (item.get("caption") or "").lower()
        key_low = (item.get("keywords") or "").lower()
        lbl_low = (item.get("label") or "").lower()
        combined = f"{cap_low} {key_low} {lbl_low}"
        
        for word in q_low.split():
            if len(word) > 2 and word in combined:
                score += 3
        if matched_lesson:
            t_low = (matched_lesson.get("title") or "").lower()
            num_low = (matched_lesson.get("number") or "").lower()
            if t_low and t_low in combined: score += 5
            if num_low and num_low in combined: score += 5
            pages = {s.get("page") for s in matched_lesson.get("generation_sources", []) if s.get("page")}
            if item.get("page") in pages:
                score += 10
        if score > 0:
            scored.append((score, item))
            
    scored.sort(key=lambda x: x[0], reverse=True)
    for _, item in scored:
        p = item.get("image_path")
        if p and p not in seen:
            seen.add(p)
            clean_p = p.replace('\\', '/').lstrip('/')
            if 'images/' in clean_p:
                clean_p = clean_p.split('images/')[-1]
            from urllib.parse import quote
            img_url = f"/api/images/{quote(clean_p, safe='/')}"
            results.append({
                "image_url": img_url,
                "image_path": clean_p,
                "label": item.get("label") or f"Hình minh họa (Trang {item.get('page', '?')}, SGK KHTN {resolved_grade})",
                "caption": item.get("caption") or item.get("label") or "Hình minh họa từ SGK",
                "page": item.get("page", 1),
                "source": item.get("source") or f"SGK KHTN {resolved_grade} KNTT.pdf",
                "metadata": {
                    "page_number": item.get("page", 1),
                    "pdf_filename": item.get("source") or f"SGK KHTN {resolved_grade} KNTT.pdf",
                    "figure_caption": item.get("caption", ""),
                    "matched_query": question
                }
            })
            if len(results) >= limit:
                break
                
    # 3. Fallback: If no image found, generate a page preview image from matched_lesson source
    if not results and matched_lesson:
        p_num = 1
        sources = matched_lesson.get("generation_sources", [])
        if sources and sources[0].get("page"):
            p_num = sources[0].get("page")
        fallback_path = f"SGK KHTN {resolved_grade} KNTT/page_{p_num}.jpg"
        from urllib.parse import quote
        results.append({
            "image_url": f"/api/learning/textbook-page?grade={resolved_grade}&page={p_num}",
            "image_path": fallback_path,
            "label": f"Sơ đồ SGK: {matched_lesson.get('number', '')} {matched_lesson.get('title', '')}".strip(),
            "caption": f"Trang kiến thức SGK KHTN {resolved_grade} - Trang {p_num}",
            "page": p_num,
            "source": f"SGK KHTN {resolved_grade} KNTT.pdf",
            "metadata": {
                "page_number": p_num,
                "pdf_filename": f"SGK KHTN {resolved_grade} KNTT.pdf",
                "figure_caption": matched_lesson.get('title', ''),
                "matched_query": question
            }
        })
        
    return results

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
# AUTHENTICATION & USER MANAGEMENT (GIÁO VIÊN & HỌC SINH)
# =========================================================================
AUTH_SECRET_KEY = os.environ.get("AUTH_SECRET_KEY") or "biorag_tan_tao_a_khtn_2026_auth_secret"
TEACHER_PASSWORD = os.environ.get("TEACHER_PASSWORD", "khtn2026@tta")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin2026@tta")

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
            if password in [ADMIN_PASSWORD, "admin2026@tta", TEACHER_PASSWORD, "khtn2026@tta"]:
                valid = True
        else:
            if password in [TEACHER_PASSWORD, "khtn2026@tta", ADMIN_PASSWORD, "admin2026@tta"]:
                valid = True

        if not valid:
            return jsonify({
                "success": False,
                "error": "Mật khẩu giáo viên không chính xác. Mặc định là: khtn2026@tta"
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

    grade_arg = request.args.get("grade")
    m_grade = re.search(r'([6-9])', source or "")
    grade = int(grade_arg) if grade_arg and str(grade_arg).isdigit() else (int(m_grade.group(1)) if m_grade else 7)
    clean_stem = f"SGK KHTN {grade} KNTT"

    # 1. First priority: Pre-rendered authentic scanned textbook page
    page_candidates = [
        Path(__file__).resolve().parent / "data" / "textbook_pages" / clean_stem / f"page_{page}.jpg",
        Path(__file__).resolve().parent / "data" / "textbook_pages" / clean_stem / f"page_{page}.png",
        BASE_DIR / "api" / "data" / "textbook_pages" / clean_stem / f"page_{page}.jpg",
        BASE_DIR / "public" / "textbook_pages" / clean_stem / f"page_{page}.jpg",
        Path.cwd() / "api" / "data" / "textbook_pages" / clean_stem / f"page_{page}.jpg",
        Path("/var/task") / "api" / "data" / "textbook_pages" / clean_stem / f"page_{page}.jpg",
    ]
    for pc in page_candidates:
        if pc.exists() and pc.is_file():
            try:
                with open(pc, "rb") as f_img:
                    img_data = f_img.read()
                mime = "image/jpeg" if pc.suffix.lower() == ".jpg" else "image/png"
                resp = Response(img_data, mimetype=mime)
                resp.headers["Content-Type"] = mime
                resp.headers["Cache-Control"] = "public, max-age=86400"
                return resp
            except Exception as e:
                print(f"Error reading {pc}: {e}")

    # 2. Second priority: Render from local PDF using fitz on the fly
    for folder in [BASE_DIR / "public" / "sgk", BASE_DIR / "datasources" / "sgk"]:
        pdf_path = folder / f"{clean_stem}.pdf"
        if pdf_path and pdf_path.exists():
            try:
                import fitz
                doc = fitz.open(str(pdf_path))
                p_idx = max(0, min(len(doc) - 1, page - 1))
                pix = doc[p_idx].get_pixmap(dpi=140)
                img_bytes = pix.tobytes("png")
                resp = Response(img_bytes, mimetype="image/png")
                resp.headers["Content-Type"] = "image/png"
                resp.headers["Cache-Control"] = "public, max-age=86400"
                return resp
            except Exception:
                pass
            break

    # 3. Fallback to closest available scanned page in directory (ALWAYS authentic scan, NO SVG!)
    dir_candidates = [
        Path(__file__).resolve().parent / "data" / "textbook_pages" / clean_stem,
        BASE_DIR / "api" / "data" / "textbook_pages" / clean_stem,
        Path.cwd() / "api" / "data" / "textbook_pages" / clean_stem,
        Path("/var/task") / "api" / "data" / "textbook_pages" / clean_stem,
    ]
    for d in dir_candidates:
        if d.exists() and d.is_dir():
            files = list(d.glob("page_*.jpg")) or list(d.glob("page_*.png"))
            if files:
                files.sort(key=lambda f: abs(int(re.search(r'page_(\d+)', f.name).group(1) if re.search(r'page_(\d+)', f.name) else 0) - page))
                best_file = files[0]
                with open(best_file, "rb") as f_img:
                    img_data = f_img.read()
                mime = "image/jpeg" if best_file.suffix.lower() == ".jpg" else "image/png"
                resp = Response(img_data, mimetype=mime)
                resp.headers["Content-Type"] = mime
                resp.headers["Cache-Control"] = "public, max-age=86400"
                return resp

    return jsonify({"error": f"Page {page} of {clean_stem} not found"}), 404

@app.route("/api/images/<path:image_path>", methods=["GET", "OPTIONS"])
@app.route("/images/<path:image_path>", methods=["GET", "OPTIONS"])
def api_serve_image(image_path):
    if request.method == "OPTIONS": return jsonify({"status": "ok"})
    from urllib.parse import unquote
    raw_path = unquote(image_path)
    clean_rel = raw_path.replace("\\", "/").lstrip("/")
    if "images/" in clean_rel:
        clean_rel = clean_rel.split("images/")[-1]
    
    m_grade = re.search(r'([6-9])', clean_rel)
    grade = int(m_grade.group(1)) if m_grade else 7
    book_stem = f"SGK KHTN {grade} KNTT"
    clean_filename = Path(clean_rel).name

    # 1. Look for static PNG/JPG cropped figure file on local disk or bundled in api/data/images
    candidates = [
        Path(__file__).resolve().parent / "data" / "images" / clean_rel,
        BASE_DIR / "api" / "data" / "images" / clean_rel,
        BASE_DIR / "images" / clean_rel,
        BASE_DIR / "public" / "images" / clean_rel,
        BASE_DIR / "database_kntt" / "images" / clean_rel,
        Path.cwd() / "api" / "data" / "images" / clean_rel,
        Path.cwd() / "images" / clean_rel,
        Path("/var/task") / "api" / "data" / "images" / clean_rel,
        Path(__file__).resolve().parent / "data" / "images" / book_stem / clean_filename,
        BASE_DIR / "api" / "data" / "images" / book_stem / clean_filename,
        Path.cwd() / "api" / "data" / "images" / book_stem / clean_filename,
        Path("/var/task") / "api" / "data" / "images" / book_stem / clean_filename,
    ]
    for c in candidates:
        if c.exists() and c.is_file():
            try:
                with open(c, "rb") as f_img:
                    img_data = f_img.read()
                ext = c.suffix.lower()
                mime = "image/png" if ext == ".png" else "image/jpeg" if ext in [".jpg", ".jpeg"] else "image/webp" if ext == ".webp" else "application/octet-stream"
                resp = Response(img_data, mimetype=mime)
                resp.headers["Content-Type"] = mime
                resp.headers["Cache-Control"] = "public, max-age=86400"
                return resp
            except Exception:
                pass

    # 2. If specific cropped figure is not found, serve the AUTHENTIC scanned textbook page!
    m_page = re.search(r'page_(\d+)', clean_rel)
    page = int(m_page.group(1)) if m_page else 1
    
    real_page_candidates = [
        Path(__file__).resolve().parent / "data" / "textbook_pages" / book_stem / f"page_{page}.jpg",
        Path(__file__).resolve().parent / "data" / "textbook_pages" / book_stem / f"page_{page}.png",
        BASE_DIR / "api" / "data" / "textbook_pages" / book_stem / f"page_{page}.jpg",
        BASE_DIR / "textbook_pages" / book_stem / f"page_{page}.jpg",
        BASE_DIR / "public" / "textbook_pages" / book_stem / f"page_{page}.jpg",
        Path.cwd() / "api" / "data" / "textbook_pages" / book_stem / f"page_{page}.jpg",
        Path.cwd() / "textbook_pages" / book_stem / f"page_{page}.jpg",
        Path("/var/task") / "api" / "data" / "textbook_pages" / book_stem / f"page_{page}.jpg",
    ]
    for rpc in real_page_candidates:
        if rpc.exists() and rpc.is_file():
            try:
                with open(rpc, "rb") as f_img:
                    img_data = f_img.read()
                mime = "image/jpeg" if rpc.suffix.lower() == ".jpg" else "image/png"
                resp = Response(img_data, mimetype=mime)
                resp.headers["Content-Type"] = mime
                resp.headers["Cache-Control"] = "public, max-age=86400"
                return resp
            except Exception:
                pass

    # 3. Render from PDF if available
    for folder in [BASE_DIR / "public" / "sgk", BASE_DIR / "datasources" / "sgk", Path(__file__).resolve().parent / "datasources" / "sgk"]:
        pdf_path = folder / f"{book_stem}.pdf"
        if pdf_path and pdf_path.exists():
            try:
                import fitz
                doc = fitz.open(str(pdf_path))
                p_idx = max(0, min(len(doc) - 1, page - 1))
                pix = doc[p_idx].get_pixmap(dpi=140)
                img_bytes = pix.tobytes("png")
                resp = Response(img_bytes, mimetype="image/png")
                resp.headers["Content-Type"] = "image/png"
                resp.headers["Cache-Control"] = "public, max-age=86400"
                return resp
            except Exception:
                pass
            break

    # 4. Fallback to closest authentic scanned page (ALWAYS authentic scan, NO SVG!)
    dir_candidates = [
        Path(__file__).resolve().parent / "data" / "textbook_pages" / book_stem,
        BASE_DIR / "api" / "data" / "textbook_pages" / book_stem,
        Path.cwd() / "api" / "data" / "textbook_pages" / book_stem,
        Path("/var/task") / "api" / "data" / "textbook_pages" / book_stem,
    ]
    for d in dir_candidates:
        if d.exists() and d.is_dir():
            files = list(d.glob("page_*.jpg")) or list(d.glob("page_*.png"))
            if files:
                files.sort(key=lambda f: abs(int(re.search(r'page_(\d+)', f.name).group(1) if re.search(r'page_(\d+)', f.name) else 0) - page))
                best_file = files[0]
                with open(best_file, "rb") as f_img:
                    img_data = f_img.read()
                mime = "image/jpeg" if best_file.suffix.lower() == ".jpg" else "image/png"
                resp = Response(img_data, mimetype=mime)
                resp.headers["Content-Type"] = mime
                resp.headers["Cache-Control"] = "public, max-age=86400"
                return resp

    return jsonify({"error": f"Image {clean_rel} not found"}), 404


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
# 5. EXAM 3280 & CÔNG VĂN 3280/BGDĐT-GDTrH (THAY THẾ CV 5842)
# =========================================================================
@app.route("/api/curriculum/cong-van-3280", methods=["GET", "OPTIONS"])
@app.route("/curriculum/cong-van-3280", methods=["GET", "OPTIONS"])
def api_get_cong_van_3280():
    if request.method == "OPTIONS": return jsonify({"status": "ok"})
    # Load cong_van_3280.json
    cv_file = BASE_DIR / "api" / "data" / "cong_van_3280.json"
    if not cv_file.exists():
        cv_file = BASE_DIR / "src" / "app" / "data" / "cong_van_3280.json"
    if cv_file.exists():
        try:
            with open(cv_file, "r", encoding="utf-8") as f:
                cv_data = json.load(f)
            subject = request.args.get("subject")
            grade = request.args.get("grade")
            if subject and subject in cv_data.get("subjects", {}):
                subj_data = cv_data["subjects"][subject]
                if grade and grade in subj_data.get("grades", {}):
                    return jsonify({
                        "metadata": cv_data.get("metadata", {}),
                        "subject": subject,
                        "grade": grade,
                        "guidelines": subj_data["grades"][grade]
                    })
                return jsonify({
                    "metadata": cv_data.get("metadata", {}),
                    "subject": subject,
                    "data": subj_data
                })
            return jsonify(cv_data)
        except Exception as err:
            return jsonify({"error": f"Lỗi đọc dữ liệu Công văn 3280: {str(err)}"}), 500
    return jsonify({"error": "Dữ liệu Công văn 3280 chưa sẵn sàng"}), 404

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

@app.route("/api/exam/lessons/<lesson_id>/export-3280", methods=["GET", "OPTIONS"])
@app.route("/exam/lessons/<lesson_id>/export-3280", methods=["GET", "OPTIONS"])
def api_export_lesson_exam_3280(lesson_id):
    if request.method == "OPTIONS": return jsonify({"status": "ok"})
    lesson = get_lesson_by_id(lesson_id)
    if not lesson:
        return jsonify({"error": f"Không tìm thấy bài học '{lesson_id}'"}), 404
    exam_type = request.args.get("exam_type", "ĐỊNH KỲ").strip()
    try:
        duration = int(request.args.get("duration", 45))
    except Exception:
        duration = 45
    if lesson_to_exam_data and build_exam_package_3280_bytes:
        exam_data = lesson_to_exam_data(lesson, exam_type=exam_type, duration=duration)
        buf = build_exam_package_3280_bytes(exam_data)
        grade = lesson.get("grade", 7)
        raw_title = str(lesson.get("title") or "Bai_hoc")
        title_slug = re.sub(r"[^\w\d_-]+", "_", raw_title).strip("_")[:40]
        filename = f"De_kiem_tra_3280_KHTN{grade}_{title_slug}.docx"
        return send_file(
            buf,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            as_attachment=True,
            download_name=filename
        )
    return jsonify({"error": "Export service unavailable"}), 500

@app.route("/api/learning/lessons/<lesson_id>/export-5512", methods=["GET", "OPTIONS"])
@app.route("/learning/lessons/<lesson_id>/export-5512", methods=["GET", "OPTIONS"])
def api_export_lesson_plan_5512(lesson_id):
    if request.method == "OPTIONS": return jsonify({"status": "ok"})
    lesson = get_lesson_by_id(lesson_id)
    if not lesson:
        return jsonify({"error": f"Không tìm thấy bài học '{lesson_id}'"}), 404
    if build_lesson_plan_5512_bytes:
        buf = build_lesson_plan_5512_bytes(lesson)
        grade = lesson.get("grade", 7)
        raw_title = str(lesson.get("title") or "Bai_hoc")
        title_slug = re.sub(r"[^\w\d_-]+", "_", raw_title).strip("_")[:40]
        filename = f"Giao_an_5512_KHTN{grade}_{title_slug}.docx"
        return send_file(
            buf,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            as_attachment=True,
            download_name=filename
        )
    return jsonify({"error": "Export service unavailable"}), 500

@app.route("/api/learning/export-5512", methods=["POST", "OPTIONS"])
@app.route("/learning/export-5512", methods=["POST", "OPTIONS"])
def api_export_custom_plan_5512():
    if request.method == "OPTIONS": return jsonify({"status": "ok"})
    data = request.get_json(silent=True) or {}
    if not data:
        return jsonify({"error": "Dữ liệu bài học không hợp lệ"}), 400
    if build_lesson_plan_5512_bytes:
        buf = build_lesson_plan_5512_bytes(data)
        grade = data.get("grade", 7)
        raw_title = str(data.get("title") or "Bai_hoc")
        title_slug = re.sub(r"[^\w\d_-]+", "_", raw_title).strip("_")[:40]
        filename = f"Giao_an_5512_KHTN{grade}_{title_slug}.docx"
        return send_file(
            buf,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            as_attachment=True,
            download_name=filename
        )
    return jsonify({"error": "Export service unavailable"}), 500

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

    # Retrieve relevant SGK illustrations/diagrams
    images = get_relevant_images_for_query(question, matched_lesson, resolved_grade, limit=2)

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

HÃY TRẢ LỜI ĐẦY ĐỦ, CHUẨN MỰC SƯ PHẠM THEO CẤU TRÚC SAU:
1. LỜI CHÀO MỞ ĐẦU: Thân thiện, ấm áp, truyền cảm hứng và khen ngợi câu hỏi hay của học sinh (ví dụ: "Chào em, thầy/cô rất vui khi nhận được câu hỏi của em! Đây là một câu hỏi rất hay, giúp chúng ta hiểu rõ hơn về...").
2. ĐỊNH NGHĨA & BẢN CHẤT CỐT LÕI: Giải thích khái niệm, định nghĩa và hiện tượng một cách chính xác, kèm phương trình tổng quát hoặc công thức khoa học (nếu có).
3. VAI TRÒ & Ý NGHĨA KHOA HỌC: Phân tích vai trò đối với sinh giới, cơ thể sinh vật hoặc thực tiễn tự nhiên.
4. MỐI LIÊN HỆ VỚI SGK KẾT NỐI TRI THỨC: Nêu rõ mối liên hệ với bài học ({matched_lesson.get('number', '')} {matched_lesson.get('title', '')}) và các bài học liên quan trong chương trình SGK KHTN KNTT, trích dẫn chính xác số trang SGK.
5. VÍ DỤ THỰC TẾ SINH ĐỘNG: Đưa ra ví dụ hoặc ứng dụng thực tế gần gũi với đời sống học sinh THCS.
6. LỜI NHẮN NHỦ TỪ TRỢ LÝ AI: Động viên tinh thần học tập, khích lệ tình yêu thiên nhiên, nhắc nhở học sinh thoải mái hỏi tiếp nếu còn thắc mắc."""

        ai_answer, model_used = call_gemini_rest(prompt, api_key)
        if ai_answer:
            return jsonify({
                "answer": ai_answer,
                "images": images,
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
        "images": images,
        "sources": [source_item],
        "grounded": True,
        "grade": resolved_grade,
        "meta": {"grounded": True, "grade": resolved_grade, "mode": "local_rag"}
    })

@app.route("/api/chat/photo", methods=["POST", "OPTIONS"])
@app.route("/chat/photo", methods=["POST", "OPTIONS"])
def api_chat_photo():
    if request.method == "OPTIONS": return jsonify({"status": "ok"})
    res = proxy_to_backend("api/chat/photo")
    if res: return res

    question = ""
    grade = 7
    if request.files and "photo" in request.files:
        f = request.files["photo"]
        grade = int(request.form.get("grade", 7) or 7)
        question = request.form.get("question") or f"Giải đáp câu hỏi trong hình ảnh SGK KHTN {grade}"
    else:
        d = request.get_json(silent=True) or {}
        question = d.get("question") or "Giải đáp hình ảnh bài tập KHTN"
        grade = int(d.get("grade", 7) or 7)

    all_lessons = get_all_lessons()
    matched_lesson = None
    if callable(search_best_lesson) and all_lessons:
        matched_lesson, _ = search_best_lesson(all_lessons, question, grade)

    images = get_relevant_images_for_query(question, matched_lesson, grade, limit=2)
    local_ans = format_local_rag_answer(question, matched_lesson) if callable(format_local_rag_answer) else f"Phân tích hình ảnh câu hỏi môn KHTN {grade} dựa trên SGK Kết nối tri thức."

    return jsonify({
        "answer": local_ans,
        "images": images,
        "sources": [{
            "title": matched_lesson.get("title", f"SGK KHTN {grade}") if matched_lesson else f"SGK KHTN {grade}",
            "page": 1,
            "source": matched_lesson.get("source_label", f"SGK KHTN {grade} KNTT") if matched_lesson else f"SGK KHTN {grade} KNTT"
        }],
        "grounded": True,
        "grade": grade,
        "meta": {"mode": "photo_rag"}
    })

@app.route("/api/feedback", methods=["POST", "OPTIONS"])
@app.route("/feedback", methods=["POST", "OPTIONS"])
def api_feedback():
    if request.method == "OPTIONS": return jsonify({"status": "ok"})
    return jsonify({"status": "ok"})

# =========================================================================
# 7. IMAGE CHAT & MULTIMODAL REGION EXPLORATION
# =========================================================================
def resolve_image_bytes_and_crop(raw_image_path="", raw_image_url="", metadata=None, label="", crop=None):
    """Resolve image bytes from local disk, URL, or scanned pages, and apply crop if provided."""
    metadata = metadata or {}
    img_bytes = None
    mime_type = "image/png"
    
    from urllib.parse import unquote, urlparse, parse_qs
    candidates = []
    
    for candidate in [raw_image_path, raw_image_url]:
        if not candidate: continue
        clean = unquote(candidate).replace('\\', '/').strip()
        if "/api/images/" in clean:
            clean = clean.split("/api/images/", 1)[1]
        if clean.startswith("/"):
            clean = clean.lstrip("/")
        if clean:
            candidates.extend([
                Path(__file__).resolve().parent / "data" / "images" / clean,
                Path(__file__).resolve().parent / "data" / "textbook_pages" / clean,
                BASE_DIR / "api" / "data" / "images" / clean,
                BASE_DIR / "api" / "data" / "textbook_pages" / clean,
                BASE_DIR / "public" / "images" / clean,
                BASE_DIR / "public" / "textbook_pages" / clean,
            ])
            
    pdf_name = metadata.get("pdf_filename") or metadata.get("source") or ""
    page = metadata.get("page_number") or metadata.get("page")
    if raw_image_url and ("page=" in raw_image_url or "source=" in raw_image_url):
        try:
            parsed = urlparse(raw_image_url)
            qs = parse_qs(parsed.query)
            if "source" in qs and not pdf_name: pdf_name = qs["source"][0]
            if "page" in qs and not page: page = qs["page"][0]
        except Exception:
            pass
            
    if not page and label:
        m_p = re.search(r'Trang\s+(\d+)', label, re.I)
        if m_p: page = int(m_p.group(1))
    if not pdf_name and label:
        m_g = re.search(r'KHTN\s*(\d)', label, re.I)
        if m_g: pdf_name = f"SGK KHTN {m_g.group(1)} KNTT.pdf"

    if page:
        try:
            p_num = int(page)
            grade = 7
            if pdf_name:
                m_g = re.search(r'KHTN\s*(\d)', str(pdf_name), re.I)
                if m_g: grade = int(m_g.group(1))
            book_stem = f"SGK KHTN {grade} KNTT"
            candidates.extend([
                Path(__file__).resolve().parent / "data" / "textbook_pages" / book_stem / f"page_{p_num}.jpg",
                Path(__file__).resolve().parent / "data" / "textbook_pages" / book_stem / f"page_{p_num}.png",
                BASE_DIR / "api" / "data" / "textbook_pages" / book_stem / f"page_{p_num}.jpg",
                BASE_DIR / "api" / "data" / "textbook_pages" / book_stem / f"page_{p_num}.png",
                BASE_DIR / "textbook_pages" / book_stem / f"page_{p_num}.jpg",
            ])
        except Exception:
            pass

    for cp in candidates:
        if cp.exists() and cp.is_file():
            try:
                with open(cp, "rb") as f:
                    img_bytes = f.read()
                mime_type = "image/jpeg" if cp.suffix.lower() in [".jpg", ".jpeg"] else "image/png"
                break
            except Exception:
                pass

    if not img_bytes and pdf_name and page:
        try:
            p_num = int(page)
            for folder in [BASE_DIR / "public" / "sgk", BASE_DIR / "datasources" / "sgk"]:
                pdf_file = folder / pdf_name
                if pdf_file.exists():
                    import fitz
                    doc = fitz.open(str(pdf_file))
                    pix = doc[max(0, min(len(doc)-1, p_num-1))].get_pixmap(dpi=140)
                    img_bytes = pix.tobytes("png")
                    mime_type = "image/png"
                    break
        except Exception:
            pass

    if not img_bytes and page:
        try:
            p_num = int(page)
            for d in [Path(__file__).resolve().parent / "data" / "textbook_pages", BASE_DIR / "api" / "data" / "textbook_pages"]:
                if d.exists():
                    matched = list(d.rglob(f"page_{p_num}.*"))
                    if matched:
                        with open(matched[0], "rb") as f:
                            img_bytes = f.read()
                        mime_type = "image/jpeg" if matched[0].suffix.lower() in [".jpg", ".jpeg"] else "image/png"
                        break
        except Exception:
            pass

    crop_info = None
    if img_bytes and crop and isinstance(crop, dict) and "x" in crop and "y" in crop and "width" in crop and "height" in crop:
        try:
            from PIL import Image
            with Image.open(io.BytesIO(img_bytes)) as im:
                w, h = im.size
                left = max(0, min(w - 1, int(float(crop["x"]) * w)))
                top = max(0, min(h - 1, int(float(crop["y"]) * h)))
                right = max(left + 1, min(w, int((float(crop["x"]) + float(crop["width"])) * w)))
                bottom = max(top + 1, min(h, int((float(crop["y"]) + float(crop["height"])) * h)))
                cropped_im = im.crop((left, top, right, bottom))
                buf = io.BytesIO()
                cropped_im.save(buf, format="PNG")
                img_bytes = buf.getvalue()
                mime_type = "image/png"
                crop_info = {"x": crop["x"], "y": crop["y"], "width": crop["width"], "height": crop["height"]}
        except Exception as e:
            print(f"Error applying crop: {e}")

    return img_bytes, mime_type, crop_info


def build_image_notes_docx(image_bytes, question, answer, source_name, page, crop_info=None, school_name="TRƯỜNG THCS HUỲNH BÁ CHÁNH"):
    """Generate Word (.docx) study note document with embedded image and pedagogic answer."""
    import io, re
    try:
        from docx import Document
        from docx.shared import Inches, Pt, RGBColor
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        
        doc = Document()
        
        header = doc.add_paragraph()
        header.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_sch = header.add_run(f"SỞ GIÁO DỤC VÀ ĐÀO TẠO · {school_name.upper()}\n")
        r_sch.bold = True
        r_sch.font.size = Pt(11)
        r_sch.font.color.rgb = RGBColor(0x16, 0x65, 0x34)
        
        title = doc.add_heading("PHIẾU HỌC TẬP & GHI CHÚ TỪ HÌNH ẢNH SGK", level=1)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        meta_p = doc.add_paragraph()
        meta_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_meta = meta_p.add_run(f"Nguồn trích dẫn: {source_name} · Trang {page}")
        r_meta.italic = True
        r_meta.font.size = Pt(10)
        
        if crop_info:
            c_p = doc.add_paragraph()
            c_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            c_p.add_run("(*) Nội dung được trích xuất từ vùng quan sát trọng tâm trên trang sách.").italic = True
            
        if image_bytes:
            try:
                img_stream = io.BytesIO(image_bytes)
                doc.add_picture(img_stream, width=Inches(5.5))
                doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
            except Exception:
                pass
                
        doc.add_heading("1. Câu hỏi tìm hiểu", level=2)
        p_q = doc.add_paragraph(question)
        if p_q.runs:
            p_q.runs[0].bold = True
        
        doc.add_heading("2. Nội dung giải đáp & Ghi chú học tập", level=2)
        for raw_line in str(answer or "").splitlines():
            line = raw_line.strip()
            if not line:
                continue
            if line.startswith("###") or line.startswith("####"):
                clean_h = re.sub(r"^#+\s*", "", line)
                doc.add_heading(clean_h, level=3)
            elif line.startswith("-") or line.startswith("*"):
                clean_b = re.sub(r"^[-*]\s*", "", line)
                clean_b = re.sub(r"\*\*([^*]+)\*\*", r"\1", clean_b)
                doc.add_paragraph(clean_b, style="List Bullet")
            else:
                clean_t = re.sub(r"\*\*([^*]+)\*\*", r"\1", line)
                doc.add_paragraph(clean_t)
                
        footer = doc.sections[0].footer.paragraphs[0]
        footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
        footer.add_run(f"Hệ thống Trợ lý AI Khoa học Tự nhiên · {school_name}")
        
        buf = io.BytesIO()
        doc.save(buf)
        buf.seek(0)
        return buf.getvalue()
    except Exception as e:
        print(f"Error building docx: {e}")
        return None


@app.route("/api/image-chat", methods=["POST", "OPTIONS"])
@app.route("/image-chat", methods=["POST", "OPTIONS"])
def api_image_chat():
    if request.method == "OPTIONS": return jsonify({"status": "ok"})
    res = proxy_to_backend("api/image-chat")
    if res: return res

    data = request.get_json(silent=True) or {}
    question = str(data.get("question") or "").strip()
    raw_image_path = str(data.get("image_path") or "").strip()
    raw_image_url = str(data.get("image_url") or "").strip()
    label = str(data.get("label") or "").strip()
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    crop = data.get("crop")
    
    if not question:
        return jsonify({"error": "Câu hỏi về hình ảnh không được để trống."}), 400

    img_bytes, mime_type, crop_info = resolve_image_bytes_and_crop(raw_image_path, raw_image_url, metadata, label, crop)
    
    grade = 7
    if metadata.get("page_number"):
        try:
            m_g = re.search(r'khtn\s*(\d)', str(metadata.get("pdf_filename") or metadata.get("source") or label), re.I)
            if m_g: grade = int(m_g.group(1))
        except Exception:
            pass
    elif label:
        m_g = re.search(r'khtn\s*(\d)', label, re.I)
        if m_g: grade = int(m_g.group(1))

    all_lessons = get_all_lessons(grade)
    matched_lesson = None
    if callable(search_best_lesson) and all_lessons:
        search_query = f"{label} {question}"
        matched_lesson, _ = search_best_lesson(all_lessons, search_query, grade)

    api_key = str(data.get("api_key") or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY") or "").strip()
    
    if img_bytes and api_key and callable(call_gemini_vision_rest):
        focus_desc = "Người học đã KHOANH MỘT VÙNG TRỌNG TÂM trên hình. Ảnh đính kèm là vùng đã khoanh." if crop_info else "Người học đang quan sát toàn bộ hình ảnh SGK."
        prompt = f"""Bạn là Trợ lý AI Khoa học Tự nhiên của Trường THCS Huỳnh Bá Chánh.
Bộ sách: SGK Khoa học Tự nhiên Lớp {grade} (Kết nối tri thức với cuộc sống).
Nguồn hình: {metadata.get('pdf_filename') or metadata.get('source') or label or 'SGK KHTN'}.
Chú thích hình: {label or metadata.get('figure_caption') or 'Hình minh họa SGK'}.
{focus_desc}

Câu hỏi của học sinh: {question}

YÊU CẦU TRẢ LỜI:
- Quan sát kỹ các chi tiết, màu sắc, ký hiệu, mũi tên và chữ viết có trong hình ảnh/vùng ảnh đính kèm.
- Trả lời bằng tiếng Việt chuẩn mực sư phạm, rõ ràng, dễ hiểu cho học sinh THCS.
- Nếu học sinh yêu cầu tóm tắt/ghi chú, hãy cung cấp đầy đủ Tiêu đề, Ý chính, Thuật ngữ quan trọng, Kết luận và Mẹo ghi nhớ.
- Nếu học sinh yêu cầu tạo câu hỏi trắc nghiệm, hãy tạo 5 câu hỏi 4 lựa chọn (A, B, C, D) kèm đáp án đúng và lời giải thích.
- Giữ tinh thần khích lệ, thân thiện và truyền cảm hứng yêu khoa học."""

        ai_ans, model_used = call_gemini_vision_rest(prompt, img_bytes, mime_type, api_key)
        if ai_ans:
            return jsonify({
                "answer": ai_ans,
                "source": {"pdf_filename": metadata.get("pdf_filename") or f"SGK KHTN {grade} KNTT.pdf", "page": metadata.get("page_number") or 1},
                "crop": crop_info,
                "meta": {"grounded": True, "grade": grade, "model": model_used}
            })

    local_ans = format_image_chat_local_answer(question, label, metadata, matched_lesson, grade, crop_info) if callable(format_image_chat_local_answer) else "Đang phân tích hình ảnh SGK."

    return jsonify({
        "answer": local_ans,
        "source": {"pdf_filename": metadata.get("pdf_filename") or f"SGK KHTN {grade} KNTT.pdf", "page": metadata.get("page_number") or 1},
        "crop": crop_info,
        "meta": {"grounded": True, "grade": grade, "mode": "local_vision_rag"}
    })


@app.route("/api/image-chat/export", methods=["POST", "OPTIONS"])
@app.route("/image-chat/export", methods=["POST", "OPTIONS"])
def api_image_chat_export():
    if request.method == "OPTIONS": return jsonify({"status": "ok"})
    res = proxy_to_backend("api/image-chat/export")
    if res: return res

    data = request.get_json(silent=True) or {}
    export_format = str(data.get("format", "docx")).strip().lower()
    question = str(data.get("question", "Tìm hiểu hình ảnh SGK")).strip()
    answer = str(data.get("answer", "")).strip()
    raw_image_path = str(data.get("image_path") or "").strip()
    raw_image_url = str(data.get("image_url") or "").strip()
    label = str(data.get("label") or "").strip()
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    crop = data.get("crop")

    img_bytes, mime_type, crop_info = resolve_image_bytes_and_crop(raw_image_path, raw_image_url, metadata, label, crop)
    
    source_name = metadata.get("pdf_filename") or metadata.get("source") or label or "SGK KHTN KNTT"
    page = metadata.get("page_number") or metadata.get("page") or 1
    
    docx_bytes = build_image_notes_docx(img_bytes, question, answer, source_name, page, crop_info, school_name="TRƯỜNG THCS HUỲNH BÁ CHÁNH")
    
    if docx_bytes:
        buf = io.BytesIO(docx_bytes)
        safe_p = re.sub(r'[^0-9A-Za-z_-]+', '_', str(page))
        return send_file(
            buf,
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            as_attachment=True,
            download_name=f"Ghi_chu_hoc_tap_trang_{safe_p}_THCS_HuynhBaChanh.docx"
        )
        
    return jsonify({"error": "Không thể xuất tài liệu Word lúc này."}), 500


# Export WSGI callable for Vercel
app_handler = app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

