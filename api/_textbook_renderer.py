# -*- coding: utf-8 -*-
import html
import json
import re
import sys
import urllib.request
from pathlib import Path

def wrap_text(text, max_chars=68):
    if not text:
        return []
    words = text.split()
    lines = []
    curr = []
    curr_len = 0
    for w in words:
        if curr_len + len(w) + (1 if curr else 0) > max_chars:
            lines.append(" ".join(curr))
            curr = [w]
            curr_len = len(w)
        else:
            curr.append(w)
            curr_len += len(w) + (1 if curr else 0)
    if curr:
        lines.append(" ".join(curr))
    return lines

def find_lesson_by_source_and_page(lessons, source, page):
    try:
        page = int(page)
    except (ValueError, TypeError):
        page = 1
    
    m_grade = re.search(r'(?:khtn|sgk|lớp)\s*([6-9])', str(source or ""), re.IGNORECASE)
    grade = int(m_grade.group(1)) if m_grade else 7
    candidates = [l for l in lessons if int(l.get('grade') or 0) == grade]
    if not candidates:
        candidates = lessons

    best_lesson = None
    best_range = (1, 4)
    best_diff = 99999

    for l in candidates:
        sl = l.get('source_label', '')
        m = re.search(r'Trang\s+(\d+)(?:[–\-](\d+))?', sl, re.IGNORECASE)
        if m:
            s = int(m.group(1))
            e = int(m.group(2)) if m.group(2) else s
            if s <= page <= e:
                return l, s, e
            diff = min(abs(page - s), abs(page - e))
            if diff < best_diff:
                best_diff = diff
                best_lesson = l
                best_range = (s, e)

    if best_lesson:
        return best_lesson, best_range[0], best_range[1]
    fallback = candidates[0] if candidates else {}
    return fallback, 1, 4

def render_textbook_page_svg(lesson, page, start_page, end_page):
    grade = lesson.get("grade", 7)
    theme_colors = {
        6: {"primary": "#059669", "light": "#ecfdf5", "border": "#a7f3d0", "dark": "#065f46"},
        7: {"primary": "#0284c7", "light": "#f0f9ff", "border": "#bae6fd", "dark": "#0369a1"},
        8: {"primary": "#4f46e5", "light": "#eef2ff", "border": "#c7d2fe", "dark": "#3730a3"},
        9: {"primary": "#7c3aed", "light": "#f5f3ff", "border": "#ddd6fe", "dark": "#5b21b6"},
    }
    tc = theme_colors.get(grade, theme_colors[7])
    
    number_str = lesson.get("number", "BÀI HỌC")
    title_str = lesson.get("title", "")
    topic_str = lesson.get("topic", "")
    source_label = lesson.get("source_label", f"SGK KHTN {grade} KNTT")
    
    objectives = lesson.get("objectives", [])
    if not objectives:
        objectives = [title_str, f"Khám phá kiến thức cốt lõi môn Khoa học tự nhiên {grade}"]

    content_str = lesson.get("content", "")
    if not content_str or "Đọc đầy đủ" in content_str:
        content_str = f"Nội dung trọng tâm bài học {title_str}. Học sinh nghiên cứu các khái niệm, quy luật tự nhiên và ứng dụng thực tiễn trong đời sống."
    
    total_pages = max(1, end_page - start_page + 1)
    page_index = max(0, min(total_pages - 1, page - start_page))
    
    esc_number = html.escape(number_str.upper())
    esc_title = html.escape(title_str)
    esc_topic = html.escape(topic_str)
    esc_source = html.escape(source_label)

    title_lines = wrap_text(title_str, max_chars=48)
    
    svg_parts = []
    svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 1200" width="100%" height="auto">
  <defs>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{tc['primary']}" />
      <stop offset="100%" stop-color="{tc['dark']}" />
    </linearGradient>
    <filter id="cardShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.06"/>
    </filter>
  </defs>

  <rect width="850" height="1200" fill="#ffffff" rx="10"/>
  <rect x="2" y="2" width="846" height="1196" fill="none" stroke="#e2e8f0" stroke-width="2" rx="10"/>
  <rect x="0" y="0" width="850" height="12" fill="url(#headerGrad)" rx="6"/>

  <g transform="translate(50, 42)">
    <rect x="0" y="0" width="34" height="34" rx="7" fill="{tc['primary']}"/>
    <text x="17" y="23" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="900" fill="#ffffff" text-anchor="middle">HBC</text>
    
    <text x="44" y="16" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="{tc['dark']}" letter-spacing="1">TRƯỜNG THCS HUỲNH BÁ CHÁNH · ĐÀ NẴNG</text>
    <text x="44" y="32" font-family="'Segoe UI', Roboto, sans-serif" font-size="10" font-weight="500" fill="#64748b">BỘ GIÁO DỤC VÀ ĐÀO TẠO · KHOA HỌC TỰ NHIÊN {grade} (KẾT NỐI TRI THỨC)</text>

    <rect x="630" y="0" width="120" height="32" rx="16" fill="{tc['light']}" stroke="{tc['border']}" stroke-width="1.5"/>
    <text x="690" y="21" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="{tc['dark']}" text-anchor="middle">TRANG {page}</text>
  </g>

  <line x1="50" y1="92" x2="800" y2="92" stroke="#e2e8f0" stroke-width="1.5"/>

  <!-- Lesson Title Section -->
  <g transform="translate(50, 125)">
    <rect x="0" y="0" width="750" height="95" rx="8" fill="{tc['light']}" stroke="{tc['border']}" stroke-width="1"/>
    <rect x="0" y="0" width="8" height="95" fill="{tc['primary']}" rx="4"/>
    
    <text x="24" y="24" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="{tc['primary']}" letter-spacing="0.5">CHỦ ĐỀ: {esc_topic[:70].upper()}</text>
    
    <text x="24" y="52" font-family="'Segoe UI', Roboto, sans-serif" font-size="20" font-weight="800" fill="#0f172a">
      <tspan fill="{tc['dark']}">{esc_number}: </tspan>
      {html.escape(title_lines[0] if title_lines else '')}
    </text>
''')
    if len(title_lines) > 1:
        svg_parts.append(f'''    <text x="24" y="76" font-family="'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="800" fill="#0f172a">{html.escape(title_lines[1])}</text>''')
    else:
        svg_parts.append(f'''    <text x="24" y="74" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="500" fill="#64748b">Vị trí bài học trong sách: {esc_source}</text>''')
    
    svg_parts.append('  </g>\n')

    # Section 1: Objectives Box
    svg_parts.append(f'''
  <!-- Section 1: Objectives Box -->
  <g transform="translate(50, 236)">
    <rect x="0" y="0" width="750" height="150" rx="8" fill="#f8fafc" stroke="#e2e8f0" stroke-width="1"/>
    <rect x="18" y="14" width="160" height="24" rx="4" fill="{tc['primary']}"/>
    <text x="26" y="30" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#ffffff">🎯 YÊU CẦU CẦN ĐẠT</text>
''')
    obj_y = 58
    for idx, obj in enumerate(objectives[:3]):
        obj_lines = wrap_text(obj, max_chars=72)
        bullet_icon = "•"
        first_line = obj_lines[0] if obj_lines else ""
        svg_parts.append(f'''    <text x="24" y="{obj_y}" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="{tc['dark']}">{bullet_icon}</text>''')
        svg_parts.append(f'''    <text x="38" y="{obj_y}" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="500" fill="#334155">{html.escape(first_line)}</text>''')
        obj_y += 18
        if len(obj_lines) > 1:
            svg_parts.append(f'''    <text x="38" y="{obj_y}" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="500" fill="#334155">{html.escape(obj_lines[1])}</text>''')
            obj_y += 18
    svg_parts.append('  </g>\n')

    # Section 2: Core Knowledge Box
    svg_parts.append(f'''
  <!-- Section 2: Key Knowledge / Content -->
  <g transform="translate(50, 402)">
    <rect x="0" y="0" width="750" height="420" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1" filter="url(#cardShadow)"/>
    
    <rect x="0" y="0" width="750" height="40" rx="8" fill="{tc['light']}"/>
    <rect x="0" y="32" width="750" height="8" fill="{tc['light']}"/>
    <line x1="0" y1="40" x2="750" y2="40" stroke="{tc['border']}" stroke-width="1"/>
    
    <text x="24" y="26" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="800" fill="{tc['dark']}">📖 KIẾN THỨC BÀI HỌC (PHẦN {page_index + 1} / {total_pages})</text>
    <text x="600" y="25" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="600" fill="#64748b" text-anchor="end">SGK KNTT {grade} · Trang {page}</text>
''')
    
    para_y = 66
    svg_parts.append(f'''    <text x="24" y="{para_y}" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#0f172a">1. Khái niệm và Hiện tượng Khoa học</text>''')
    para_y += 24
    
    body_lines = wrap_text(content_str, max_chars=74)
    for line in body_lines[:4]:
        svg_parts.append(f'''    <text x="24" y="{para_y}" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="400" fill="#334155">{html.escape(line)}</text>''')
        para_y += 20

    para_y += 10
    svg_parts.append(f'''    <text x="24" y="{para_y}" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#0f172a">2. Hoạt động Khám phá &amp; Quan sát</text>''')
    para_y += 24
    
    guide_lines = [
        f"Trong bài học '{title_str}', học sinh quan sát hình ảnh, làm thí nghiệm và rút ra kết luận.",
        f"Hãy đối chiếu các hiện tượng quan sát được với các định luật khoa học đã học.",
        f"Thảo luận cùng bạn bè và ghi chép các số liệu hoặc đặc điểm nổi bật vào vở thực hành."
    ]
    for gl in guide_lines:
        for line in wrap_text(gl, max_chars=74):
            svg_parts.append(f'''    <text x="24" y="{para_y}" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="400" fill="#334155">{html.escape(line)}</text>''')
            para_y += 20

    para_y += 10
    svg_parts.append(f'''
    <rect x="24" y="{para_y}" width="702" height="110" rx="6" fill="{tc['light']}" stroke="{tc['border']}" stroke-dasharray="4,4"/>
    <text x="375" y="{para_y + 35}" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="{tc['dark']}" text-anchor="middle">🔬 SƠ ĐỒ / HÌNH MINH HỌA BÀI HỌC</text>
    <text x="375" y="{para_y + 60}" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="500" fill="#64748b" text-anchor="middle">Xem chi tiết tại thẻ '✦ Nội dung hỗ trợ' hoặc thẻ '3D Thí nghiệm ảo'</text>
    <text x="375" y="{para_y + 80}" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="600" fill="{tc['primary']}" text-anchor="middle">Trường THCS Huỳnh Bá Chánh · Phòng Thí nghiệm Khoa học Tự nhiên</text>
''')

    svg_parts.append('  </g>\n')

    # Section 3: Summary / Inquiry Box
    svg_parts.append(f'''
  <!-- Section 3: Key Takeaway & Activity -->
  <g transform="translate(50, 838)">
    <rect x="0" y="0" width="750" height="260" rx="8" fill="#fffbeb" stroke="#fde68a" stroke-width="1.5"/>
    <rect x="18" y="14" width="190" height="24" rx="4" fill="#d97706"/>
    <text x="26" y="30" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#ffffff">💡 EM CÓ BIẾT &amp; GHI NHỚ</text>
    
    <text x="24" y="66" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#92400e">Câu hỏi gợi ý thảo luận:</text>
    <text x="24" y="88" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="500" fill="#78350f">1. Em hãy nêu ý nghĩa thực tiễn của kiến thức trong bài học này đối với cuộc sống hàng ngày?</text>
    <text x="24" y="108" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="500" fill="#78350f">2. Vận dụng kiến thức đã học để giải thích một hiện tượng tự nhiên quen thuộc xung quanh em.</text>
    
    <line x1="24" y1="130" x2="726" y2="130" stroke="#fde68a" stroke-width="1"/>
    <text x="24" y="152" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="#92400e">Tự đánh giá sau bài học:</text>
    <text x="38" y="174" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="500" fill="#78350f">☑ Đã đọc và nắm vững các mục tiêu cần đạt của bài học.</text>
    <text x="38" y="194" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="500" fill="#78350f">☑ Đã hoàn thành các câu hỏi luyện tập và bài tập trắc nghiệm trong BioRAG.</text>
    <text x="38" y="214" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="500" fill="#78350f">☑ Có thể trình bày lại sơ đồ tư duy tóm tắt kiến thức của bài.</text>
  </g>
''')

    # Bottom Footer
    svg_parts.append(f'''
  <!-- Footer Bar -->
  <line x1="50" y1="1120" x2="800" y2="1120" stroke="#e2e8f0" stroke-width="1"/>
  <g transform="translate(50, 1145)">
    <text x="0" y="0" font-family="'Segoe UI', Roboto, sans-serif" font-size="10" font-weight="600" fill="#64748b">HỆ THỐNG BIORAG · TRƯỜNG THCS HUỲNH BÁ CHÁNH</text>
    
    <circle cx="375" cy="-4" r="16" fill="{tc['primary']}"/>
    <text x="375" y="1" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="800" fill="#ffffff" text-anchor="middle">{page}</text>
    
    <text x="750" y="0" font-family="'Segoe UI', Roboto, sans-serif" font-size="10" font-weight="500" fill="#94a3b8" text-anchor="end">SGK KNTT {grade} · Bản quyền Bộ GD&amp;ĐT</text>
  </g>
</svg>
''')
    return "".join(svg_parts)

def render_textbook_reader_html(lesson, current_page, start_page, end_page, source_name):
    grade = lesson.get("grade", 7)
    title = lesson.get("title", "")
    number = lesson.get("number", "Bài học")
    topic = lesson.get("topic", "")
    objectives = lesson.get("objectives", [])
    content = lesson.get("content", "")
    
    pages = list(range(start_page, end_page + 1))
    if current_page not in pages:
        current_page = pages[0] if pages else start_page
        
    page_buttons_html = "".join([
        f'<a href="?source={html.escape(source_name)}&page={p}" class="page-btn {"active" if p == current_page else ""}">Trang {p}</a>'
        for p in pages
    ])

    prev_page = current_page - 1 if current_page > start_page else None
    next_page = current_page + 1 if current_page < end_page else None

    prev_link = f'<a href="?source={html.escape(source_name)}&page={prev_page}" class="nav-btn">← Trang trước ({prev_page})</a>' if prev_page else '<span class="nav-btn disabled">← Trang trước</span>'
    next_link = f'<a href="?source={html.escape(source_name)}&page={next_page}" class="nav-btn">Trang sau ({next_page}) →</a>' if next_page else '<span class="nav-btn disabled">Trang sau →</span>'

    obj_html = "".join([f'<li>{html.escape(o)}</li>' for o in objectives])

    svg_img_url = f"/api/learning/textbook-page?source={html.escape(source_name)}&page={current_page}"

    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{html.escape(number)}: {html.escape(title)} - SGK KHTN {grade} | THCS Huỳnh Bá Chánh</title>
  <style>
    :root {{
      --primary: #0284c7;
      --primary-dark: #0369a1;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --border: #e2e8f0;
      --text: #0f172a;
      --text-muted: #64748b;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.6;
    }}
    .topbar {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: #ffffff;
      border-bottom: 1px solid var(--border);
      box-shadow: 0 2px 10px rgba(0,0,0,0.05);
      padding: 10px 20px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 15px;
      flex-wrap: wrap;
    }}
    .brand {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .logo-badge {{
      background: #059669;
      color: #ffffff;
      font-weight: 900;
      font-size: 14px;
      padding: 6px 10px;
      border-radius: 8px;
    }}
    .brand-title h1 {{
      font-size: 14px;
      font-weight: 700;
      color: #1e293b;
    }}
    .brand-title p {{
      font-size: 11px;
      color: var(--text-muted);
    }}
    .nav-controls {{
      display: flex;
      align-items: center;
      gap: 8px;
      flex-wrap: wrap;
    }}
    .page-btn {{
      display: inline-block;
      padding: 5px 10px;
      border-radius: 6px;
      text-decoration: none;
      font-size: 12px;
      font-weight: 600;
      color: #334155;
      background: #f1f5f9;
      border: 1px solid #cbd5e1;
      transition: all 0.15s ease;
    }}
    .page-btn:hover {{
      background: #e2e8f0;
    }}
    .page-btn.active {{
      background: var(--primary);
      color: #ffffff;
      border-color: var(--primary-dark);
    }}
    .action-btn {{
      padding: 6px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      text-decoration: none;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      border: 1px solid #cbd5e1;
      background: #ffffff;
      color: #1e293b;
    }}
    .action-btn.print {{
      background: #0284c7;
      color: #ffffff;
      border-color: #0369a1;
    }}
    .nav-btn {{
      padding: 5px 10px;
      font-size: 12px;
      text-decoration: none;
      color: var(--primary-dark);
      font-weight: 600;
    }}
    .nav-btn.disabled {{
      color: #cbd5e1;
      pointer-events: none;
    }}
    .main-container {{
      max-width: 960px;
      margin: 20px auto;
      padding: 0 15px 40px;
    }}
    .reader-card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.06);
      overflow: hidden;
      margin-bottom: 25px;
    }}
    .svg-stage {{
      padding: 15px;
      background: #f1f5f9;
      text-align: center;
      border-bottom: 1px solid var(--border);
    }}
    .svg-stage img {{
      max-width: 100%;
      height: auto;
      border-radius: 6px;
      box-shadow: 0 4px 15px rgba(0,0,0,0.1);
      background: #ffffff;
    }}
    .text-summary-pane {{
      padding: 24px;
    }}
    .text-summary-pane h2 {{
      font-size: 18px;
      margin-bottom: 12px;
      color: #0f172a;
    }}
    .text-summary-pane ul {{
      margin-left: 20px;
      margin-bottom: 16px;
    }}
    .text-summary-pane li {{
      margin-bottom: 6px;
    }}
    .text-summary-pane p {{
      margin-bottom: 14px;
      color: #334155;
    }}
    @media print {{
      .topbar, .nav-controls, .action-btn {{
        display: none !important;
      }}
      body {{
        background: #ffffff;
      }}
      .main-container {{
        max-width: 100%;
        margin: 0;
        padding: 0;
      }}
      .reader-card {{
        border: none;
        box-shadow: none;
      }}
      .svg-stage {{
        background: #ffffff;
        padding: 0;
      }}
    }}
  </style>
</head>
<body>
  <header class="topbar">
    <div class="brand">
      <div class="logo-badge">HBC</div>
      <div class="brand-title">
        <h1>TRƯỜNG THCS HUỲNH BÁ CHÁNH · SGK ĐIỆN TỬ</h1>
        <p>Khoa học tự nhiên {grade} (Kết nối tri thức) · {html.escape(number)}</p>
      </div>
    </div>
    <div class="nav-controls">
      {prev_link}
      <div class="page-list">
        {page_buttons_html}
      </div>
      {next_link}
    </div>
    <div>
      <button class="action-btn print" onclick="window.print()">🖨 In / Lưu PDF</button>
      <button class="action-btn" onclick="window.close()">✕ Đóng</button>
    </div>
  </header>

  <main class="main-container">
    <div class="reader-card">
      <div class="svg-stage">
        <img src="{svg_img_url}" alt="Trang {current_page} - {html.escape(title)}">
      </div>
      <div class="text-summary-pane">
        <h2>{html.escape(number)}: {html.escape(title)}</h2>
        <p><strong>Chủ đề:</strong> {html.escape(topic)}</p>
        <h3 style="font-size: 15px; margin: 15px 0 8px;">🎯 Yêu cầu cần đạt:</h3>
        <ul>{obj_html}</ul>
        <h3 style="font-size: 15px; margin: 15px 0 8px;">📖 Nội dung tóm tắt:</h3>
        <p>{html.escape(content)}</p>
      </div>
    </div>
  </main>
</body>
</html>"""

def search_best_lesson(lessons_or_question, question_or_grade=None, preferred_grade=None):
    if isinstance(lessons_or_question, list):
        lessons = lessons_or_question
        question = question_or_grade or ""
    else:
        lessons = None
        question = lessons_or_question or ""
        preferred_grade = question_or_grade

    if lessons is None:
        try:
            from api.index import get_all_lessons
            lessons = get_all_lessons()
        except Exception:
            lessons = []

    stop_words = {'là', 'gì', 'thế', 'nào', 'sao', 'hãy', 'cho', 'biết', 'của', 'và', 'các', 'những', 'trong', 'với', 'tìm', 'hiểu', 'về', 'hỏi', 'giúp'}
    words = [w.lower() for w in re.findall(r'[\w]+', question) if len(w) > 1 and w.lower() not in stop_words]
    
    best_lesson = None
    best_score = 0
    
    for l in lessons:
        score = 0
        l_grade = int(l.get("grade") or 0)
        if preferred_grade and l_grade == preferred_grade:
            score += 5
            
        title = l.get("title", "").lower()
        topic = l.get("topic", "").lower()
        content = l.get("content", "").lower()
        objectives = " ".join(l.get("objectives", [])).lower()
        sections = " ".join([" ".join(s.get("paragraphs", [])) for s in l.get("sections", [])]).lower()
        terms = " ".join([t.get("term", "") + " " + t.get("definition", "") for t in l.get("terms", [])]).lower()
        summary = " ".join(l.get("summary", [])).lower()
        
        full_text = f"{title} {topic} {terms} {summary} {objectives} {sections} {content}"
        
        # Check phrase match
        q_phrase = " ".join(words)
        if q_phrase and q_phrase in title:
            score += 60
        elif q_phrase and q_phrase in terms:
            score += 45
        elif q_phrase and q_phrase in full_text:
            score += 30
            
        for w in words:
            if w in title:
                score += 16
            elif w in terms:
                score += 14
            elif w in topic:
                score += 8
            elif w in summary:
                score += 6
            elif w in full_text:
                score += 3
                
        if score > best_score:
            best_score = score
            best_lesson = l
            
    return best_lesson, best_score

def format_local_rag_answer(question, lesson):
    if not lesson:
        return "Xin lỗi, hiện tại mình chưa tìm thấy thông tin phù hợp trong 195 bài học SGK KHTN 6–9."
    
    grade = lesson.get("grade", 7)
    number = lesson.get("number", "Bài học")
    title = lesson.get("title", "")
    source_label = lesson.get("source_label", f"SGK KHTN {grade} KNTT")
    
    lines = [f"Chào bạn! Dưới đây là kiến thức chuẩn từ **{source_label}**:\n"]
    lines.append(f"### 📖 {number}: {title}\n")
    
    # Check if there are specific matching terms
    terms = lesson.get("terms", [])
    matching_terms = []
    q_lower = question.lower()
    for t in terms:
        if t.get("term", "").lower() in q_lower or any(w in t.get("term", "").lower() for w in q_lower.split()):
            matching_terms.append(f"- **{t.get('term')}**: {t.get('definition')}")
            
    if matching_terms:
        lines.append("**Khái niệm trọng tâm:**")
        lines.extend(matching_terms)
        lines.append("")
        
    # Check sections
    sections = lesson.get("sections", [])
    if sections:
        for s in sections[:2]:
            lines.append(f"**{s.get('title')}:**")
            for p in s.get("paragraphs", [])[:2]:
                lines.append(p)
            if s.get("note"):
                lines.append(f"*Lưu ý:* {s.get('note')}")
            lines.append("")
    elif lesson.get("content") and "Đọc đầy đủ" not in lesson.get("content"):
        lines.append(lesson.get("content"))
        lines.append("")
        
    # Summary
    summary = lesson.get("summary", [])
    if summary:
        lines.append("**Ghi nhớ:**")
        for sm in summary[:3]:
            lines.append(f"✓ {sm}")
        lines.append("")
        
    # Objectives if little content
    if not sections and not matching_terms:
        objs = lesson.get("objectives", [])
        if objs:
            lines.append("**Mục tiêu và yêu cầu cần đạt:**")
            for o in objs:
                lines.append(f"- {o}")
            lines.append("")
            
    lines.append(f"\n📚 *Nguồn trích dẫn: {source_label} · Trường THCS Huỳnh Bá Chánh*")
    return "\n".join(lines)

def call_gemini_rest(prompt, api_key):
    models = ["gemini-3.6-flash", "gemini-2.5-flash", "gemini-1.5-flash"]
    for m in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
        payload = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 1024
            }
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["candidates"][0]["content"]["parts"][0]["text"]
                return text.strip(), m
        except Exception as e:
            continue
    return None, None
