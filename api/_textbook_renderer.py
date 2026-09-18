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

    # 1. Match directly against generation_sources (which has exact PDF page numbers)
    for l in candidates:
        for gen in l.get("generation_sources", []):
            if gen.get("page") == page:
                pages = [g.get("page") for g in l.get("generation_sources", []) if g.get("page")]
                return l, min(pages) if pages else page, max(pages) if pages else page

    best_lesson = None
    best_range = (1, 4)
    best_diff = 99999

    for l in candidates:
        sl = l.get('source_label', '')
        m = re.search(r'Trang\s+(\d+)(?:[–\-](\d+))?', sl, re.IGNORECASE)
        if m:
            s_print = int(m.group(1))
            e_print = int(m.group(2)) if m.group(2) else s_print
            s = s_print + 1
            e = e_print + 1
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

def render_textbook_page_svg(lesson, page, start_page, end_page, school_name=None):
    school_name = school_name or os.environ.get("SCHOOL_NAME") or lesson.get("school_name") or "TRƯỜNG THCS TÂN TẠO A"
    school_code = "TTA" if "TÂN TẠO" in school_name.upper() else ("HBC" if "HUỲNH BÁ" in school_name.upper() else "KHTN")
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

    title_lines = wrap_text(title_str, max_chars=40)
    
    svg_parts = []
    svg_parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 1200" width="850" height="1200">
  <defs>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{tc['primary']}"/>
      <stop offset="100%" stop-color="{tc['dark']}"/>
    </linearGradient>
    <filter id="cardShadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#000000" flood-opacity="0.06"/>
    </filter>
  </defs>

  <rect width="850" height="1200" fill="#ffffff" rx="10"/>
  <rect x="2" y="2" width="846" height="1196" fill="none" stroke="#e2e8f0" stroke-width="2" rx="10"/>
  <rect x="0" y="0" width="850" height="12" fill="url(#headerGrad)" rx="6"/>

  <g transform="translate(50, 42)">
    <rect x="0" y="0" width="34" height="34" rx="7" fill="{tc['primary']}"/>
    <text x="17" y="23" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="900" fill="#ffffff" text-anchor="middle">{school_code}</text>
    
    <text x="44" y="16" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="{tc['dark']}" letter-spacing="1">{html.escape(school_name.upper())} · TPHCM</text>
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
    sections = lesson.get("sections", [])
    current_sec = None
    if sections:
        sec_idx = min(page_index, len(sections) - 1)
        current_sec = sections[sec_idx]

    sec_title = current_sec.get("title", "1. Nội dung trọng tâm bài học") if current_sec else "1. Nội dung trọng tâm bài học"
    sec_paras = current_sec.get("paragraphs", []) if current_sec else []
    sec_bullets = current_sec.get("bullets", []) if current_sec else []

    svg_parts.append(f'''    <text x="24" y="{para_y}" font-family="'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="700" fill="#0f172a">{html.escape(sec_title[:75])}</text>''')
    para_y += 24

    if not sec_paras and content_str:
        sec_paras = [content_str]

    rendered_paras = 0
    for p in sec_paras:
        p_lines = wrap_text(p, max_chars=74)
        for line in p_lines[:3]:
            svg_parts.append(f'''    <text x="24" y="{para_y}" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="400" fill="#334155">{html.escape(line)}</text>''')
            para_y += 20
        para_y += 6
        rendered_paras += 1
        if para_y > 220 or rendered_paras >= 2:
            break

    if sec_bullets:
        para_y += 4
        svg_parts.append(f'''    <text x="24" y="{para_y}" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="{tc['dark']}">Chi tiết và số liệu quan trọng:</text>''')
        para_y += 20
        for b in sec_bullets[:2]:
            b_lines = wrap_text(f"• {b}", max_chars=74)
            for bl in b_lines[:2]:
                svg_parts.append(f'''    <text x="24" y="{para_y}" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="500" fill="#334155">{html.escape(bl)}</text>''')
                para_y += 18
            if para_y > 280:
                break

    card_h = min(100, 390 - para_y)
    if card_h > 40:
        svg_parts.append(f'''
    <rect x="24" y="{para_y + 10}" width="702" height="{card_h}" rx="6" fill="{tc['light']}" stroke="{tc['border']}" stroke-dasharray="4,4"/>
    <text x="375" y="{para_y + 35}" font-family="'Segoe UI', Roboto, sans-serif" font-size="12" font-weight="700" fill="{tc['dark']}" text-anchor="middle">🔬 BẢNG DỮ LIỆU &amp; HÌNH MINH HỌA SGK TRANG {page}</text>
    <text x="375" y="{para_y + 55}" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="500" fill="#64748b" text-anchor="middle">Chi tiết đầy đủ tại thẻ '✦ Nội dung hỗ trợ' · Mô phỏng 2D tại '🧪 Thí nghiệm ảo'</text>
''')

    svg_parts.append('  </g>\n')

    # Section 3: Summary / Inquiry Box
    svg_parts.append(f'''
  <!-- Section 3: Key Takeaway & Activity -->
  <g transform="translate(50, 838)">
    <rect x="0" y="0" width="750" height="260" rx="8" fill="#fffbeb" stroke="#fde68a" stroke-width="1.5"/>
    <rect x="18" y="14" width="190" height="24" rx="4" fill="#d97706"/>
    <text x="26" y="30" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#ffffff">💡 EM ĐÃ HỌC &amp; GHI NHỚ</text>
''')
    sum_y = 66
    summaries = lesson.get("summary", [])
    if not summaries:
        summaries = [
            f"Nắm vững các khái niệm và hiện tượng khoa học trong bài học {title_str}.",
            f"Vận dụng kiến thức bài học để giải thích hiện tượng tự nhiên và ứng dụng trong đời sống."
        ]
    for s_item in summaries[:3]:
        s_lines = wrap_text(f"• {s_item}", max_chars=74)
        for sl in s_lines[:2]:
            svg_parts.append(f'''    <text x="24" y="{sum_y}" font-family="'Segoe UI', Roboto, sans-serif" font-size="11.5" font-weight="500" fill="#78350f">{html.escape(sl)}</text>''')
            sum_y += 18
        sum_y += 4
        if sum_y > 170:
            break

    svg_parts.append(f'''
    <line x1="24" y1="{max(sum_y, 160)}" x2="726" y2="{max(sum_y, 160)}" stroke="#fde68a" stroke-width="1"/>
    <text x="24" y="{max(sum_y + 22, 182)}" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="700" fill="#92400e">Mục tiêu củng cố bài học:</text>
    <text x="38" y="{max(sum_y + 40, 200)}" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="500" fill="#78350f">☑ Nắm chắc khái niệm: Nhấn '✦ Tạo flashcard &amp; Sơ đồ tư duy' ở thẻ bên để tự kiểm tra.</text>
    <text x="38" y="{max(sum_y + 58, 218)}" font-family="'Segoe UI', Roboto, sans-serif" font-size="11" font-weight="500" fill="#78350f">☑ Làm bài tập: Nhấn '⚡ Làm bài kiểm tra' hoặc '✓ Câu hỏi luyện tập' để đánh giá năng lực.</text>
  </g>
''')

    # Bottom Footer
    svg_parts.append(f'''
  <!-- Footer Bar -->
  <line x1="50" y1="1120" x2="800" y2="1120" stroke="#e2e8f0" stroke-width="1"/>
  <g transform="translate(50, 1145)">
    <text x="0" y="0" font-family="'Segoe UI', Roboto, sans-serif" font-size="10" font-weight="600" fill="#64748b">HỆ THỐNG BIORAG · {html.escape(school_name.upper())}</text>
    
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
  <title>{html.escape(number)}: {html.escape(title)} - SGK KHTN {grade} | THCS Tân Tạo A</title>
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

    generic_attr_ngrams = {'vai trò', 'đặc điểm', 'ý nghĩa', 'tác dụng', 'cấu tạo', 'khái niệm', 'phân loại'}
    stop_words = {'là', 'gì', 'thế', 'nào', 'sao', 'hãy', 'cho', 'biết', 'của', 'và', 'các', 'những', 'trong', 'với', 'tìm', 'hiểu', 'về', 'hỏi', 'giúp', 'như', 'có'}
    words = [w.lower() for w in re.findall(r'[\w]+', question) if len(w) > 1 and w.lower() not in stop_words]
    
    ngrams = []
    if len(words) >= 2:
        for i in range(len(words)-1):
            ngrams.append(f'{words[i]} {words[i+1]}')
    if len(words) >= 3:
        for i in range(len(words)-2):
            ngrams.append(f'{words[i]} {words[i+1]} {words[i+2]}')
            
    best_lesson = None
    best_score = 0
    
    for l in lessons:
        score = 0
        l_grade = int(l.get("grade") or 0)
        if preferred_grade and l_grade == preferred_grade:
            score += 100
            
        title = l.get("title", "").lower()
        topic = l.get("topic", "").lower()
        content = l.get("content", "").lower()
        objectives = " ".join(l.get("objectives", [])).lower()
        sections = " ".join([" ".join(s.get("paragraphs", [])) for s in l.get("sections", [])]).lower()
        terms = " ".join([t.get("term", "") + " " + t.get("definition", "") for t in l.get("terms", [])]).lower()
        summary = " ".join(l.get("summary", [])).lower()
        
        full_text = f"{title} {topic} {terms} {summary} {objectives} {sections} {content}"
        
        for ng in ngrams:
            is_attr = ng in generic_attr_ngrams
            weight = 20 if is_attr else 80
            if ng in title:
                score += weight
            elif ng in terms:
                score += (15 if is_attr else 35)
            elif ng in topic:
                score += (10 if is_attr else 25)
            elif ng in full_text:
                score += (5 if is_attr else 10)
                
        for w in words:
            if w in title:
                score += 15
            elif w in terms:
                score += 10
            elif w in topic:
                score += 6
            elif w in summary:
                score += 4
            elif w in full_text:
                score += 2
                
        if score > best_score:
            best_score = score
            best_lesson = l
            
    return best_lesson, best_score

def format_local_rag_answer(question, lesson):
    if not lesson:
        return "Chào em, thầy/cô rất vui khi nhận được câu hỏi của em! Hiện tại hệ thống chưa tìm thấy bài học phù hợp trong 195 bài học SGK KHTN. Em hãy thử đặt câu hỏi cụ thể hơn nhé!"
    
    grade = lesson.get("grade", 7)
    number = lesson.get("number", "Bài học")
    title = lesson.get("title", "")
    source_label = lesson.get("source_label", f"SGK KHTN {grade} KNTT")
    
    lines = []
    # 1. Warm pedagogical greeting
    lines.append(f"Chào em, thầy/cô rất vui khi nhận được câu hỏi của em! Đây là một câu hỏi rất hay và mang tính khám phá cao, giúp chúng ta mở ra cánh cửa tìm hiểu về kiến thức kỳ diệu trong chương trình **Khoa học tự nhiên lớp {grade}** (Bộ sách *Kết nối tri thức với cuộc sống*).\n")
    lines.append("Dưới đây là lời giải đáp dành cho em:\n")
    
    # 2. 1. Definition & Core concepts
    terms = lesson.get("terms", [])
    matching_terms = []
    q_lower = question.lower()
    for t in terms:
        if t.get("term", "").lower() in q_lower or any(w in t.get("term", "").lower() for w in q_lower.split()):
            matching_terms.append(f"- **{t.get('term')}**: {t.get('definition')}")
            
    lines.append("### 1. Định nghĩa & Bản chất cốt lõi")
    if matching_terms:
        lines.extend(matching_terms)
    elif terms:
        for t in terms[:2]:
            lines.append(f"- **{t.get('term')}**: {t.get('definition')}")
    else:
        lines.append(f"- **Khái niệm**: Bản chất cốt lõi của bài học {title} giúp giải thích các quy luật và hiện tượng tự nhiên.")
    
    content = lesson.get("content", "")
    if content and "Đọc đầy đủ" not in content:
        lines.append(f"\n{content}")
    lines.append("")

    # 3. 2. Role & Scientific Significance
    lines.append("### 2. Vai trò & Ý nghĩa khoa học")
    summary = lesson.get("summary", [])
    if summary:
        for sm in summary[:2]:
            lines.append(f"- {sm}")
    else:
        lines.append(f"- Giúp con người hiểu rõ các quy luật vận động của vật chất, năng lượng và sự sống trong tự nhiên, từ đó ứng dụng vào thực tiễn đời sống và sản xuất.")
    lines.append("")

    # 4. 3. Connection to SGK KNTT
    lines.append("### 3. Mối liên hệ với SGK Kết nối tri thức với cuộc sống")
    lines.append(f"Nội dung này được trình bày chi tiết tại **{number}: {title}** ({source_label}).")
    objectives = lesson.get("objectives", [])
    if objectives:
        for obj in objectives[:2]:
            lines.append(f"- {obj}")
    lines.append("")

    # 5. 4. Vivid Real-world Examples
    lines.append("### 4. Ví dụ thực tế sinh động")
    lines.append(f"Trong cuộc sống hàng ngày, chúng ta có thể dễ dàng quan sát hiện tượng liên quan đến **{title}** thông qua các biến đổi tự nhiên xung quanh hoặc trong các thí nghiệm thực hành tại phòng bộ môn KHTN.")
    lines.append("")

    # 6. 5. AI Guidance note
    lines.append("### 5. Lời nhắn nhủ từ Trợ lý AI")
    lines.append(f"Thầy/cô rất khen ngợi tinh thần ham học hỏi của em! Khoa học tự nhiên luôn ẩn chứa những điều kỳ diệu ngay trong cuộc sống quanh ta. Hãy luôn giữ sự tò mò này để khám phá thế giới nhé. Nếu em còn bất kỳ thắc mắc nào, đừng ngần ngại đặt câu hỏi cho thầy/cô. Chúc em có những giờ học thật thú vị và bổ ích tại **Trường THCS Tân Tạo A**!\n")
    lines.append(f"📖 *Nguồn trích dẫn: {source_label} · Trường THCS Tân Tạo A*")
    return "\n".join(lines)

def call_gemini_rest(prompt, api_key):
    models = ["gemini-3.1-flash-lite", "gemini-3.5-flash", "gemini-3.6-flash", "gemma-4-26b-a4b-it"]
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
                candidate = data.get("candidates", [{}])[0]
                parts = candidate.get("content", {}).get("parts", [])
                texts = [p.get("text", "") for p in parts if not p.get("thought") and p.get("text")]
                if not texts:
                    texts = [p.get("text", "") for p in parts if p.get("text")]
                text = "\n".join(texts).strip()
                if text:
                    return text, m
        except Exception:
            continue
    return None, None


def call_gemini_vision_rest(prompt, image_bytes, mime_type="image/jpeg", api_key=None):
    """Call Gemini Vision Multimodal API directly with image bytes."""
    if not api_key:
        return None, None
    import base64
    encoded_img = base64.b64encode(image_bytes).decode("ascii")
    mime = mime_type or "image/jpeg"
    models = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.0-flash", "gemini-3.1-flash-lite", "gemini-3.5-flash"]
    for m in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
        payload = json.dumps({
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inlineData": {
                            "mimeType": mime,
                            "data": encoded_img
                        }
                    }
                ]
            }],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 2048
            }
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                candidate = data.get("candidates", [{}])[0]
                parts = candidate.get("content", {}).get("parts", [])
                texts = [p.get("text", "") for p in parts if not p.get("thought") and p.get("text")]
                if not texts:
                    texts = [p.get("text", "") for p in parts if p.get("text")]
                text = "\n".join(texts).strip()
                if text:
                    return text, m
        except Exception:
            continue
    return None, None


def format_image_chat_local_answer(question, label="", metadata=None, lesson=None, grade=7, crop_info=None):
    """Comprehensive offline pedagogic answer for SGK image exploration."""
    metadata = metadata or {}
    fig_title = label or metadata.get("figure_caption") or metadata.get("matched_query") or "Hình ảnh minh họa SGK"
    source = metadata.get("pdf_filename") or metadata.get("source") or f"SGK KHTN {grade} (Kết nối tri thức)"
    page = metadata.get("page_number") or metadata.get("page") or "?"
    
    lesson_title = lesson.get("title", "") if lesson else ""
    lesson_number = lesson.get("number", "") if lesson else ""
    terms = lesson.get("terms", []) if lesson else []
    summary = lesson.get("summary", []) if lesson else []
    
    q_low = question.lower()
    
    # 1. Notes / Tóm tắt ghi chú
    if "tóm tắt" in q_low or "ghi chú" in q_low or "dễ ôn" in q_low:
        res = [
            f"### 📝 GHI CHÚ HỌC TẬP TỪ HÌNH ẢNH SGK",
            f"**Nguồn:** {source} · Trang {page}",
            f"**Đối tượng quan sát:** {fig_title}",
            "",
            "#### 1. Ý chính & Diễn biến trong hình",
        ]
        if crop_info:
            res.append(f"- *Vùng ảnh quan sát:* Khu vực trọng tâm được khoanh vùng trên trang sách ({round(crop_info.get('width', 1)*100)}% × {round(crop_info.get('height', 1)*100)}%).")
        
        if "khoai tây" in fig_title.lower() or "sinh trưởng" in fig_title.lower() or "21.1" in fig_title:
            res.extend([
                "- Hình thể hiện toàn bộ **vòng đời sinh trưởng và phát triển** của cây khoai tây từ củ mầm đến khi thu hoạch củ mới.",
                "- **Các giai đoạn rõ rệt:** Củ mọc mầm ➔ Cây con phát triển rễ, thân, lá ➔ Cây trưởng thành ra hoa ➔ Hình thành củ dưới đất ➔ Cây già cỗi và tàn lụi, để lại các củ khoai tây thế hệ mới.",
                "- **Mối liên hệ hai chiều:** *Sinh trưởng* (tăng số lượng, kích thước cành lá, rễ, củ) diễn ra đan xen và làm tiền đề cho *phát triển* (phân hóa chồi, ra hoa, tạo củ mới)."
            ])
        else:
            if summary:
                for s in summary[:3]:
                    res.append(f"- {s}")
            else:
                res.append(f"- Sơ đồ minh họa trực quan cấu tạo, cơ chế và mối liên hệ khoa học trong bài học **{lesson_number} {lesson_title}**.")
        
        res.extend([
            "",
            "#### 2. Thuật ngữ quan trọng cần nhớ",
        ])
        if terms:
            for t in terms[:3]:
                res.append(f"- **{t.get('term')}:** {t.get('definition')}")
        else:
            res.extend([
                "- **Sinh trưởng:** Sự tăng lên về kích thước và khối lượng cơ thể do tăng số lượng và kích thước tế bào.",
                "- **Phát triển:** Quá trình biến đổi bao gồm sinh trưởng, phân hóa tế bào và phát sinh hình thái các cơ quan mới."
            ])
            
        res.extend([
            "",
            "#### 3. Kết luận khoa học",
            f"- Các cơ quan và giai đoạn biến đổi trong hình tuân theo quy luật phát triển tự nhiên của sinh vật, gắn liền với chương trình KHTN Lớp {grade}.",
            "",
            "#### 💡 Mẹo ghi nhớ nhanh",
            "👉 *'Sinh trưởng là LỚN LÊN (tăng lượng, tăng cỡ) — Phát triển là THAY ĐỔI CHẤT (sinh cơ quan mới như lá, hoa, quả, củ)'*."
        ])
        return "\n".join(res)
        
    # 2. Tạo trắc nghiệm
    elif "trắc nghiệm" in q_low or "câu hỏi" in q_low:
        res = [
            f"### 🎯 BỘ 5 CÂU HỎI TRẮC NGHIỆM TỪ HÌNH ẢNH ({fig_title})",
            f"*Nguồn: {source} (Trang {page})*",
            "",
            "**Câu 1:** Hình ảnh trên minh họa cho quá trình nào ở sinh vật?",
            "A. Quá trình trao đổi chất và chuyển hóa năng lượng.",
            "B. Quá trình sinh trưởng và phát triển qua các giai đoạn.",
            "C. Quá trình cảm ứng và thích nghi với môi trường.",
            "D. Quá trình sinh sản vô tính nhân tạo.",
            "👉 **Đáp án đúng: B.** *Giải thích: Hình biểu diễn các giai đoạn biến đổi hình thái, kích thước và cơ quan theo thời gian.*",
            "",
            "**Câu 2:** Hiện tượng cây tăng về chiều cao thân và kích thước rễ thuộc về quá trình nào?",
            "A. Phát triển.",
            "B. Cảm ứng.",
            "C. Sinh trưởng.",
            "D. Phân hóa.",
            "👉 **Đáp án đúng: C.** *Giải thích: Sự gia tăng về kích thước và khối lượng là biểu hiện của sinh trưởng.*",
            "",
            "**Câu 3:** Giai đoạn cây ra hoa và kết quả/củ thể hiện rõ nhất đặc trưng của quá trình nào?",
            "A. Sinh trưởng.",
            "B. Phát triển (phân hóa cơ quan sinh sản).",
            "C. Quang hợp tích lũy chất.",
            "D. Thoát hơi nước.",
            "👉 **Đáp án đúng: B.** *Giải thích: Sự phát sinh cơ quan mới (hoa, quả, củ) là biểu hiện của quá trình phát triển.*",
            "",
            "**Câu 4:** Mối quan hệ giữa sinh trưởng và phát triển được thể hiện như thế nào?",
            "A. Hoàn toàn độc lập và không liên quan nhau.",
            "B. Diễn ra song hành, sinh trưởng tạo tiền đề cho phát triển.",
            "C. Sinh trưởng kết thúc thì phát triển mới bắt đầu.",
            "D. Chỉ xảy ra ở động vật, không có ở thực vật.",
            "👉 **Đáp án đúng: B.** *Giải thích: Sinh vật phải sinh trưởng tích lũy đủ khối lượng vật chất mới bước sang giai đoạn phát triển mới.*",
            "",
            "**Câu 5:** Vận dụng thực tiễn: Muốn thu hoạch củ đạt năng suất cao nhất, người trồng cần chú ý điều gì?",
            "A. Bẻ hết lá ngay khi cây vừa mọc mầm.",
            "B. Chăm sóc, cung cấp đủ nước và dinh dưỡng ở giai đoạn cây sinh trưởng mạnh tạo củ.",
            "C. Không tưới nước trong toàn bộ vòng đời của cây.",
            "D. Thu hoạch khi cây vừa nảy mầm.",
            "👉 **Đáp án đúng: B.** *Giải thích: Cung cấp đầy đủ điều kiện dinh dưỡng giúp củ phát triển to và tích lũy nhiều tinh bột.*"
        ]
        return "\n".join(res)
        
    # 3. Giải thích cho từng lớp học
    elif "giải thích" in q_low or "lớp" in q_low:
        res = [
            f"### 🔬 GIẢI THÍCH CHI TIẾT DÀNH CHO HỌC SINH LỚP {grade}",
            f"**Hình quan sát:** {fig_title} (SGK KHTN {grade} - Kết nối tri thức, Trang {page})",
            "",
            "#### 1. Khái niệm & Hiện tượng quan sát được",
            f"Quan sát hình vẽ, chúng ta thấy sự chuyển tiếp tuần tự giữa các trạng thái của đối tượng qua từng thời kỳ. Mỗi giai đoạn đều có những đặc điểm hình thái và cấu trúc thích nghi với chức năng sinh học cụ thể.",
            "",
            "#### 2. Bản chất khoa học",
            f"Hiện tượng này là minh chứng rõ nét cho quy luật vận động và biến đổi vật chất trong tự nhiên, nằm trong chương trình trọng tâm của **{lesson_number} {lesson_title}**.",
            "",
            "#### 3. Câu hỏi tự kiểm tra",
            "❓ *Em hãy nêu 2 dấu hiệu chứng minh sự khác nhau giữa sinh trưởng (tăng kích thước) và phát triển (phân hóa cơ quan) trên hình vẽ này nhé!*"
        ]
        return "\n".join(res)

    # 4. Trả lời câu hỏi tổng quát
    else:
        res = [
            f"### 🔍 PHÂN TÍCH HÌNH ẢNH: {fig_title}",
            f"*Trích dẫn: {source} (Trang {page})*",
            "",
            f"Chào em! Thầy/cô xin giải đáp câu hỏi **'{question}'** dựa trên hình ảnh SGK như sau:",
            "",
            "#### 1. Chi tiết nhìn thấy trên hình",
            f"- Hình ảnh cung cấp thông tin trực quan về cấu trúc, sơ đồ hoặc diễn biến của đối tượng trong bài học **{lesson_number} {lesson_title}**.",
            "- Các mũi tên và ký hiệu trên hình giúp người học theo dõi chiều hướng diễn biến và mối quan hệ nhân - quả giữa các thành phần.",
            "",
            "#### 2. Ý nghĩa bài học & Vận dụng",
            "- Giúp học sinh khắc sâu kiến thức lý thuyết bằng sơ đồ hóa trực quan.",
            "- Rèn luyện năng lực quan sát, nhận biết và suy luận khoa học trong môn Khoa học tự nhiên.",
            "",
            "💡 *Nếu em muốn phân tích kỹ một chi tiết cụ thể, hãy dùng công cụ **'Khoanh vùng'** để khoanh trực tiếp vùng ảnh cần tìm hiểu nhé!*"
        ]
        return "\n".join(res)


