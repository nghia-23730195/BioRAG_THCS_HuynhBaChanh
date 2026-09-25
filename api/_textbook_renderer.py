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
    school_name = school_name or os.environ.get("SCHOOL_NAME") or lesson.get("school_name") or "TRƯỜNG THCS HUỲNH BÁ CHÁNH"
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

# Complete high-quality encyclopedia for all KHTN 6, 7, 8, 9 concepts
ENCYCLOPEDIA_KHTN = {
    # Quang học KHTN 9
    "tán sắc ánh sáng": {
        "term": "Hiện tượng tán sắc ánh sáng",
        "definition": "Là hiện tượng một chùm ánh sáng trắng (ánh sáng phức hợp) khi truyền qua lăng kính hoặc môi trường trong suốt bị phân tách thành một dải nhiều chùm ánh sáng đơn sắc có màu biến thiên liên tục từ đỏ đến tím (đỏ, da cam, vàng, lục, lam, chàm, tím).",
        "details": "Mỗi ánh sáng đơn sắc có chiết suất khác nhau đối với chất làm lăng kính (ánh sáng đỏ bị lệch ít nhất, ánh sáng tím bị lệch nhiều nhất).",
        "role": "Giải thích hiện tượng cầu vồng tự nhiên sau mưa, màu sắc trên màng bong bóng xà phòng, và là nguyên lý hoạt động của máy quang phổ để phân tích cấu tạo vật chất từ xa.",
        "example": "Cầu vồng trên bầu trời sau cơn mưa xuất hiện khi ánh sáng Mặt Trời bị tán sắc và phản xạ toàn phần qua hàng triệu giọt nước mưa li ti đóng vai trò như những lăng kính tự nhiên."
    },
    "lăng kính": {
        "term": "Lăng kính",
        "definition": "Là một khối chất trong suốt, đồng chất (thường làm bằng thủy tinh hoặc nhựa trong), được giới hạn bởi hai mặt phẳng không song song gọi là các mặt bên của lăng kính.",
        "details": "Về phương diện quang học, lăng kính được đặc trưng bởi góc chiết quang A và chiết suất n của chất làm lăng kính. Lăng kính có tác dụng làm lệch tia sáng về phía đáy khi truyền qua nó.",
        "role": "Dùng làm bộ phận tán sắc trong máy quang phổ, kính tiềm vọng, ống nhòm và các dụng cụ quang học.",
        "example": "Lăng kính tam giác bằng thủy tinh dùng trong phòng thí nghiệm KHTN để tạo ra dải cầu vồng 7 màu từ chùm sáng trắng của đèn chiếu."
    },
    "ánh sáng đơn sắc": {
        "term": "Ánh sáng đơn sắc",
        "definition": "Là ánh sáng có một màu xác định và không bị đổi màu (không bị tán sắc) khi đi qua lăng kính, chỉ bị lệch đường truyền về phía đáy lăng kính.",
        "details": "Ví dụ ánh sáng đỏ đơn sắc khi qua lăng kính vẫn giữ nguyên màu đỏ.",
        "role": "Ứng dụng trong tia laser, đèn tín hiệu giao thông, thiết bị đo lường quang học chính xác.",
        "example": "Tia laser đỏ dùng trong bút chỉ bảng là chùm sáng đơn sắc, khi chiếu qua lăng kính không bị tách thành nhiều màu."
    },
    "ánh sáng trắng": {
        "term": "Ánh sáng trắng",
        "definition": "Là hỗn hợp của vô số ánh sáng đơn sắc khác nhau có màu biến thiên liên tục từ màu đỏ đến màu tím.",
        "details": "Ánh sáng Mặt Trời, ánh sáng đèn sợi đốt, đèn halogen là các nguồn phát ánh sáng trắng.",
        "role": "Cung cấp ánh sáng nhìn thấy cho sinh giới định hướng, quan sát và thúc đẩy quang hợp ở thực vật.",
        "example": "Ánh sáng Mặt Trời vào ban ngày chiếu rọi vạn vật, khi gặp lăng kính thủy tinh sẽ tách ra thành 7 sắc cầu vồng rực rỡ."
    },
    "khúc xạ ánh sáng": {
        "term": "Hiện tượng khúc xạ ánh sáng",
        "definition": "Là hiện tượng tia sáng bị gãy khúc (đổi hướng truyền đột ngột) tại mặt phân cách giữa hai môi trường trong suốt khác nhau khi truyền xiên góc từ môi trường này sang môi trường khác.",
        "details": "Định luật khúc xạ: Tia khúc xạ nằm trong mặt phẳng tới và ở phía bên kia pháp tuyến so với tia tới. Tỉ số sin(i) / sin(r) = n2 / n1 là hằng số đối với hai môi trường xác định.",
        "role": "Là nguyên lý tạo ảnh của mắt người, kính thuốc, kính hiển vi, kính thiên văn và máy ảnh.",
        "example": "Cắm một chiếc đũa thẳng vào cốc nước trong suốt, ta nhìn thấy chiếc đũa như bị gãy khúc ở mặt nước do hiện tượng khúc xạ ánh sáng."
    },
    "phản xạ toàn phần": {
        "term": "Hiện tượng phản xạ toàn phần",
        "definition": "Là hiện tượng toàn bộ tia sáng tới bị phản xạ ngược trở lại môi trường trong suốt ban đầu tại mặt phân cách giữa hai môi trường, không có tia khúc xạ đi vào môi trường thứ hai.",
        "details": "Điều kiện xảy ra: Ánh sáng truyền từ môi trường có chiết suất lớn sang môi trường có chiết suất nhỏ hơn (n1 > n2) và góc tới i ≥ igh (với sin igh = n2/n1).",
        "role": "Ứng dụng then chốt trong cáp quang viễn thông truyền dữ liệu tốc độ cao (Internet xuyên đại dương), sợi quang nội soi y tế.",
        "example": "Cáp quang Internet truyền tín hiệu ánh sáng đi hàng ngàn cây số nhờ hiện tượng phản xạ toàn phần liên tục bên trong lõi sợi thủy tinh."
    },
    "thấu kính hội tụ": {
        "term": "Thấu kính hội tụ",
        "definition": "Là thấu kính có phần rìa mỏng hơn phần giữa, có tác dụng hội tụ chùm tia sáng tới song song với trục chính tại một điểm nằm sau thấu kính gọi là tiêu điểm chính.",
        "details": "Tia tới qua quang tâm O truyền thẳng; tia tới song song trục chính cho tia ló đi qua tiêu điểm chính F'; tia tới qua tiêu điểm F cho tia ló song song trục chính.",
        "role": "Dùng làm vật kính máy ảnh, kính hiển vi, kính lúp, kính thiên văn và kính chữa tật viễn thị, lão thị.",
        "example": "Kính lúp cầm tay của học sinh là một thấu kính hội tụ dùng để quan sát gân lá hoặc các chi tiết nhỏ của côn trùng."
    },
    "thấu kính phân kì": {
        "term": "Thấu kính phân kì",
        "definition": "Là thấu kính có phần rìa dày hơn phần giữa, có tác dụng làm phân kì (loe rộng ra) chùm tia sáng tới song song với trục chính.",
        "details": "Đặc điểm tạo ảnh: Luôn cho ảnh ảo, cùng chiều và nhỏ hơn vật, nằm trong khoảng tiêu cự của thấu kính.",
        "role": "Dùng làm kính thuốc chữa tật cận thị cho học sinh, ống nhòm thể thao.",
        "example": "Mắt kính của các bạn học sinh bị cận thị là thấu kính phân kì giúp đưa ảnh của vật ở xa về đúng màng lưới của mắt."
    },
    "định luật ôm": {
        "term": "Định luật Ohm (Ôm)",
        "definition": "Cường độ dòng điện chạy qua một đoạn dây dẫn tỉ lệ thuận với hiệu điện thế đặt vào hai đầu đoạn dây và tỉ lệ nghịch với điện trở của đoạn dây đó: I = U / R (trong đó I đo bằng Ampe - A, U đo bằng Vôn - V, R đo bằng Ôm - Ω).",
        "details": "Hệ quả: U = I × R; R = U / I. Đồ thị biểu diễn sự phụ thuộc của I vào U là một đường thẳng đi qua gốc tọa độ.",
        "role": "Là định luật cơ bản nhất của điện học dùng để tính toán mạch điện, thiết kế mạng điện an toàn trong gia đình và công nghiệp.",
        "example": "Khi tăng hiệu điện thế giữa hai đầu bóng đèn từ 110V lên 220V mà điện trở không đổi thì cường độ dòng điện tăng gấp đôi, làm đèn sáng mạnh hơn."
    },
    "cảm ứng điện từ": {
        "term": "Hiện tượng cảm ứng điện từ",
        "definition": "Là hiện tượng xuất hiện dòng điện cảm ứng trong một cuộn dây dẫn kín khi số đường sức từ xuyên qua tiết diện của cuộn dây đó biến thiên (tăng lên hoặc giảm đi).",
        "details": "Được nhà bác học Michael Faraday phát minh năm 1831. Dòng điện cảm ứng chỉ tồn tại trong thời gian số đường sức từ biến thiên.",
        "role": "Là nguyên lý hoạt động của máy phát điện xoay chiều, máy biến áp, bếp từ, động cơ điện và toàn bộ hệ thống sản xuất điện năng hiện đại.",
        "example": "Di chuyển thanh nam châm lại gần hoặc ra xa cuộn dây đồng có nối với bóng đèn LED, đèn LED sẽ lóe sáng do có dòng điện cảm ứng sinh ra."
    },
    # Sinh học & KHTN Lớp 7
    "hô hấp tế bào": {
        "term": "Hô hấp tế bào",
        "definition": "Là quá trình phân giải các phân tử chất hữu cơ (chủ yếu là glucose) diễn ra trong tế bào (chủ yếu tại bào quan ti thể) với sự tham gia của khí oxygen, tạo ra sản phẩm là carbon dioxide (CO2), nước (H2O) và giải phóng năng lượng dưới dạng ATP cung cấp cho mọi hoạt động sống của tế bào và cơ thể.",
        "details": "Phương trình chữ: Glucose + Khí oxygen → Khí carbon dioxide + Nước + Năng lượng (ATP + Nhiệt).",
        "role": "Cung cấp nguồn năng lượng ATP duy nhất cho sự phân chia tế bào, vận chuyển chất, co cơ, dẫn truyền xung thần kinh và duy trì thân nhiệt.",
        "example": "Khi chúng ta chạy bộ nhanh, cơ thể cần nhiều năng lượng nên nhịp thở và nhịp tim tăng nhanh để cung cấp đủ oxygen cho các tế bào cơ bắp thực hiện hô hấp tế bào."
    },
    "quang hợp": {
        "term": "Quang hợp ở thực vật",
        "definition": "Là quá trình lá cây và các bộ phận có màu xanh của thực vật sử dụng năng lượng ánh sáng mặt trời đã được chất diệp lục (trong lục lạp) hấp thụ để tổng hợp chất hữu cơ (glucose, tinh bột) từ nước (H2O) rễ hút lên và khí carbon dioxide (CO2) từ không khí, đồng thời giải phóng khí oxygen (O2) ra môi trường.",
        "details": "Phương trình chữ: Nước + Khí carbon dioxide + Năng lượng ánh sáng (Diệp lục) → Glucose + Khí oxygen.",
        "role": "Tạo ra chất hữu cơ nuôi sống toàn bộ sinh vật trên Trái Đất; cung cấp khí O2 cho hô hấp và hấp thụ CO2 giúp làm sạch bầu khí quyển, điều hòa khí hậu toàn cầu.",
        "example": "Trồng nhiều cây xanh xung quanh trường học và khu dân cư giúp không khí trong lành, mát mẻ hơn nhờ quá trình quang hợp hấp thụ CO2 và nhả khí O2."
    },
    "nguyên tố hóa học": {
        "term": "Nguyên tố hóa học",
        "definition": "Là tập hợp những nguyên tử cùng loại có cùng số proton trong hạt nhân (cùng điện tích hạt nhân). Các nguyên tử của cùng một nguyên tố hóa học đều có tính chất hóa học giống nhau.",
        "details": "Mỗi nguyên tố được biểu diễn bằng một kí hiệu hóa học (gồm 1 hoặc 2 chữ cái, ví dụ: H, O, C, N, Na, Fe, Cu). Hiện nay có 118 nguyên tố hóa học được sắp xếp trong Bảng tuần hoàn.",
        "role": "Là những 'viên gạch' cơ bản xây dựng nên toàn bộ hàng triệu chất vô cơ và hữu cơ trong tự nhiên và cơ thể con người.",
        "example": "Nguyên tố Calcium (Ca) là thành phần cấu tạo chính của xương và răng; nguyên tố Iron (Fe) tạo nên phân tử hemoglobin vận chuyển oxygen trong máu."
    },
    "nguyên tử": {
        "term": "Nguyên tử",
        "definition": "Là hạt vô cùng nhỏ bé và trung hòa về điện, cấu tạo nên mọi chất. Nguyên tử gồm hạt nhân mang điện tích dương ở tâm (chứa proton mang điện +1 và neutron không mang điện) và lớp vỏ electron mang điện tích âm (-1) chuyển động xung quanh.",
        "details": "Trong một nguyên tử trung hòa điện: Số proton = Số electron. Khối lượng nguyên tử tập trung hầu hết ở hạt nhân do khối lượng electron rất nhỏ không đáng kể.",
        "role": "Hiểu cấu tạo nguyên tử giúp giải thích các liên kết hóa học, phản ứng hóa học và sự biến đổi của vật chất.",
        "example": "Một nguyên tử Carbon có 6 proton, 6 neutron ở hạt nhân và 6 electron ở lớp vỏ."
    },
    "phân tử": {
        "term": "Phân tử",
        "definition": "Là hạt đại diện cho chất, gồm một số nguyên tử liên kết với nhau bằng liên kết hóa học và thể hiện đầy đủ tính chất hóa học của chất đó.",
        "details": "Khối lượng phân tử (phân tử khối) bằng tổng khối lượng của các nguyên tử tạo nên phân tử đó.",
        "role": "Là đơn vị cấu thành cơ bản của các chất tinh khiết trong thế giới tự nhiên.",
        "example": "Phân tử nước (H2O) gồm 2 nguyên tử Hydrogen liên kết với 1 nguyên tử Oxygen, có khối lượng phân tử là 18 amu."
    },
    "đơn chất": {
        "term": "Đơn chất",
        "definition": "Là những chất được tạo nên từ chỉ một nguyên tố hóa học duy nhất (ví dụ: kim loại nhôm Al, khí oxygen O2, than chì C, khí nitrogen N2).",
        "details": "Đơn chất được chia làm đơn chất kim loại (dẫn điện, dẫn nhiệt, có ánh kim) và đơn chất phi kim.",
        "role": "Dùng làm nguyên liệu sản xuất công nghiệp, dây dẫn điện, vật liệu xây dựng.",
        "example": "Dây dẫn điện trong nhà làm bằng đồng (Cu) nguyên chất – là một đơn chất kim loại dẫn điện rất tốt."
    },
    "hợp chất": {
        "term": "Hợp chất",
        "definition": "Là những chất được tạo nên từ hai hay nhiều nguyên tố hóa học khác nhau liên kết với nhau theo tỉ lệ số nguyên tử xác định (ví dụ: nước H2O, muối ăn NaCl, khí carbon dioxide CO2).",
        "details": "Hợp chất có tính chất hoàn toàn khác biệt so với các đơn chất cấu thành nên nó.",
        "role": "Chiếm đại đa số các chất trong tự nhiên, từ đất, đá, nước đến cơ thể sinh vật.",
        "example": "Muối ăn (NaCl) là hợp chất của kim loại Sodium (Na) và khí Chlorine (Cl2), nhưng khi kết hợp lại tạo thành gia vị an toàn hằng ngày."
    },
    "acid": {
        "term": "Acid",
        "definition": "Là những hợp chất mà phân tử gồm có một hay nhiều nguyên tử hydrogen liên kết với gốc acid. Khi tan trong nước, acid tạo ra cation H⁺ làm dung dịch có vị chua và làm giấy quỳ tím đổi sang màu đỏ (pH < 7).",
        "details": "Tính chất hóa học chung: Đổi màu chất chỉ thị; tác dụng với kim loại đứng trước H giải phóng khí H2; tác dụng với base tạo muối và nước; tác dụng với basic oxide tạo muối và nước.",
        "role": "Dùng rộng rãi trong công nghiệp sản xuất phân bón, chất tẩy rửa, ắc quy xe máy và tham gia vào quá trình tiêu hóa thức ăn trong dạ dày người (dịch vị chứa HCl loãng).",
        "example": "Hydrochloric acid (HCl) có trong dịch vị dạ dày giúp tiêu hóa thức ăn; Acetic acid (CH3COOH) nồng độ 2-5% chính là giấm ăn dùng trong gia đình."
    },
    "base": {
        "term": "Base (Bazơ)",
        "definition": "Là những hợp chất mà phân tử gồm có nguyên tử kim loại liên kết với một hay nhiều nhóm hydroxide (-OH). Khi tan trong nước, base tạo ra anion OH⁻ làm giấy quỳ tím đổi sang màu xanh và dung dịch phenolphthalein chuyển sang màu hồng (pH > 7).",
        "details": "Base tan trong nước gọi là kiềm (NaOH, KOH, Ba(OH)2, Ca(OH)2). Base không tan như Cu(OH)2, Fe(OH)3.",
        "role": "Dùng để trung hòa acid, xử lý đất chua phèn trong nông nghiệp, sản xuất xà phòng và giấy.",
        "example": "Vôi tôi (Ca(OH)2) được nông dân rắc lên ruộng để khử chua cho đất phèn và khử trùng ao nuôi tôm cá."
    },
    "muối": {
        "term": "Muối",
        "definition": "Là hợp chất được tạo ra từ sự thay thế ion H⁺ trong phân tử acid bằng ion kim loại hoặc ion ammonium (NH4⁺). Phân tử muối gồm có kim loại (hoặc NH4⁺) liên kết với gốc acid.",
        "details": "Ví dụ: Muối ăn NaCl, đá vôi CaCO3, phèn chua KAl(SO4)2, phân đạm NH4NO3.",
        "role": "Là gia vị không thể thiếu, khoáng chất vi lượng cho cơ thể sống, nguyên liệu sản xuất phân bón, thủy tinh, xi măng.",
        "example": "Baking soda (NaHCO3) là một loại muối dùng làm bột nở khi nướng bánh và khử mùi nhà bếp."
    },
    "lực ma sát": {
        "term": "Lực ma sát",
        "definition": "Là lực xuất hiện ở bề mặt tiếp xúc giữa hai vật và có tác dụng cản trở chuyển động của vật đối với bề mặt kia.",
        "details": "Gồm 3 loại: Ma sát trượt (khi vật trượt trên bề mặt), ma sát lăn (khi vật lăn trên bề mặt), và ma sát nghỉ (giữ cho vật đứng yên khi có lực tác dụng).",
        "role": "Giúp con người đi lại, xe cộ di chuyển, dừng lại khi phanh, cầm nắm được đồ vật; cần giảm ma sát ở các ổ bi, trục máy bằng dầu mỡ bôi trơn.",
        "example": "Lốp xe đạp có nhiều rãnh và gai cao su để tăng ma sát bám đường, giúp xe không bị trượt ngã khi phanh gấp."
    },
    "lực đẩy archimedes": {
        "term": "Lực đẩy Archimedes (Ác-si-mét)",
        "definition": "Là lực đẩy hướng thẳng đứng từ dưới lên trên do chất lỏng (hoặc chất khí) tác dụng lên bất kỳ vật nào nhúng chìm một phần hoặc toàn bộ trong nó. Độ lớn của lực đẩy bằng trọng lượng của khối chất lỏng bị vật chiếm chỗ: F_A = d × V.",
        "details": "Điều kiện vật nổi, chìm: Vật chìm khi F_A < P (d_vat > d_chatlong); Vật lơ lửng khi F_A = P; Vật nổi khi F_A > P và dâng lên đến khi F_A = P.",
        "role": "Là nguyên lý giúp tàu thuyền bằng thép nặng hàng vạn tấn vẫn nổi trên mặt biển, khinh khí cầu bay lượn trên bầu trời.",
        "example": "Tàu thủy chở hàng khổng lồ được thiết kế khoang rỗng làm tăng thể tích chiếm chỗ V, giúp lực đẩy Archimedes F_A lớn hơn trọng lượng P của tàu nên tàu nổi vững vàng."
    },
    "khối lượng riêng": {
        "term": "Khối lượng riêng",
        "definition": "Là khối lượng của một đơn vị thể tích chất đó, được xác định bằng công thức: D = m / V (trong đó D là khối lượng riêng đo bằng kg/m³, m là khối lượng đo bằng kg, V là thể tích đo bằng m³).",
        "details": "Khối lượng riêng là một đại lượng vật lí đặc trưng cho từng chất tinh khiết ở nhiệt độ xác định. Trọng lượng riêng: d = 10 × D (đơn vị N/m³).",
        "role": "Dùng để nhận biết chất, kiểm tra độ tinh khiết của vàng bạc, tính toán tải trọng kết cấu trong xây dựng và cơ khí.",
        "example": "Nước ngọt có khối lượng riêng khoảng 1000 kg/m³, trong khi sắt có khối lượng riêng 7800 kg/m³, do đó sắt nặng gấp 7,8 lần nước cùng thể tích."
    }
}

def format_local_rag_answer(question, lesson):
    if not lesson:
        return "Chào em, thầy/cô rất vui khi nhận được câu hỏi của em! Hiện tại hệ thống chưa tìm thấy bài học phù hợp trong 195 bài học SGK KHTN. Em hãy thử đặt câu hỏi cụ thể hơn nhé!"
    
    grade = lesson.get("grade", 7)
    number = lesson.get("number", "Bài học")
    title = lesson.get("title", "")
    source_label = lesson.get("source_label", f"SGK KHTN {grade} KNTT")
    q_lower = (question or "").lower()
    
    lines = []
    # 1. Warm pedagogical greeting
    lines.append(f"Chào em, thầy/cô rất vui khi nhận được câu hỏi của em! Đây là một câu hỏi rất hay và mang tính khám phá cao, giúp chúng ta mở ra cánh cửa tìm hiểu về kiến thức kỳ diệu trong chương trình **Khoa học tự nhiên lớp {grade}** (Bộ sách *Kết nối tri thức với cuộc sống*).\n")
    lines.append("Dưới đây là lời giải đáp chi tiết dành cho em:\n")
    
    # 2. 1. Definition & Core concepts
    lines.append("### 1. Định nghĩa & Bản chất cốt lõi")
    
    # Check encyclopedia for matched concept
    matched_entry = None
    for k, ev in ENCYCLOPEDIA_KHTN.items():
        if k in q_lower or (len(k.split()) > 1 and all(w in q_lower for w in k.split())):
            matched_entry = ev
            break
            
    if not matched_entry:
        for k, ev in ENCYCLOPEDIA_KHTN.items():
            if k in title.lower():
                matched_entry = ev
                break

    if matched_entry:
        lines.append(f"- **{matched_entry['term']}**: {matched_entry['definition']}")
        if matched_entry.get("details"):
            lines.append(f"  * *Chi tiết khoa học & Đặc điểm*: {matched_entry['details']}")
    else:
        # Fallback to key terms from lesson
        terms = lesson.get("terms", [])
        added_terms = 0
        for t in terms:
            t_name = t.get("term", "")
            t_def = t.get("definition", "")
            if len(t_def) > 20 and not t_def.endswith(('...', 'được', 'và', 'của', 'tạo', 'là', 'trong')):
                lines.append(f"- **{t_name}**: {t_def}")
                added_terms += 1
                if added_terms >= 2:
                    break
        if not added_terms and lesson.get("content"):
            lines.append(f"- **{title}**: {lesson.get('content')[:250]}...")
                
    lines.append("")

    # 3. 2. Role & Scientific Significance
    lines.append("### 2. Vai trò & Ý nghĩa khoa học")
    if matched_entry and matched_entry.get("role"):
        lines.append(f"- {matched_entry['role']}")
    else:
        summary = [s for s in lesson.get("summary", []) if len(s) > 20 and not re.match(r'^\d+\.', s)]
        if summary:
            for sm in summary[:2]:
                lines.append(f"- {sm}")
        else:
            lines.append(f"- Giúp giải thích các quy luật vận động, chuyển hóa của vật chất và năng lượng trong tự nhiên, từ đó ứng dụng vào thực tiễn đời sống và sản xuất.")
    lines.append("")

    # 4. 3. Connection to SGK KNTT
    lines.append("### 3. Mối liên hệ với SGK Kết nối tri thức với cuộc sống")
    lines.append(f"Nội dung này được trình bày chi tiết tại **{number}: {title}** ({source_label}).")
    objectives = lesson.get("objectives", [])
    if objectives:
        for obj in objectives[:3]:
            lines.append(f"- {obj}")
    lines.append("")

    # 5. 4. Vivid Real-world Examples
    lines.append("### 4. Ví dụ thực tế sinh động")
    if matched_entry and matched_entry.get("example"):
        lines.append(f"{matched_entry['example']}")
    else:
        lines.append(f"Trong đời sống hàng ngày, chúng ta có thể dễ dàng quan sát hiện tượng liên quan đến **{title}** thông qua các biến đổi tự nhiên xung quanh hoặc trong các thí nghiệm thực hành tại phòng bộ môn KHTN Trường THCS Huỳnh Bá Chánh.")
    lines.append("")

    # 6. 5. AI Guidance note
    lines.append("### 5. Lời nhắn nhủ từ Trợ lý AI")
    lines.append(f"Thầy/cô rất khen ngợi tinh thần ham học hỏi của em! Khoa học tự nhiên luôn ẩn chứa những điều kỳ diệu ngay trong cuộc sống quanh ta. Hãy luôn giữ sự tò mò này để khám phá thế giới nhé. Nếu em còn bất kỳ thắc mắc nào, đừng ngần ngại đặt câu hỏi cho thầy/cô. Chúc em có những giờ học thật thú vị và bổ ích tại **Trường THCS Huỳnh Bá Chánh**!\n")
    lines.append(f"📖 *Nguồn trích dẫn: {source_label} · Trường THCS Huỳnh Bá Chánh*")
    return "\n".join(lines)

def call_gemini_rest(prompt, api_key):
    models = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]
    for m in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={api_key}"
        payload = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.3,
                "maxOutputTokens": 1500
            }
        }).encode("utf-8")
        req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                candidates = data.get("candidates", [])
                if candidates:
                    candidate = candidates[0]
                    parts = candidate.get("content", {}).get("parts", [])
                    texts = [p.get("text", "") for p in parts if not p.get("thought") and p.get("text")]
                    if not texts:
                        texts = [p.get("text", "") for p in parts if p.get("text")]
                    text = "\n".join(texts).strip()
                    if text and len(text) > 50:
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
    models = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]
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


def format_image_chat_local_answer(question, label="", metadata=None, matched_lesson=None, grade=7, crop_info=None, **kwargs):
    """Format smart local RAG answer for image-guided QA, study notes, quiz generation, and explanations."""
    if isinstance(label, dict) and metadata is None:
        metadata = label
        label = metadata.get("label", "")
        
    metadata = metadata or {}
    lbl = label or metadata.get("label") or metadata.get("figure_caption") or "Hình ảnh SGK KHTN"
    src = metadata.get("source") or metadata.get("pdf_filename") or (matched_lesson.get("source_label") if matched_lesson else f"SGK KHTN {grade} KNTT")
    pg = metadata.get("page_number") or metadata.get("page") or (matched_lesson.get("order") if matched_lesson else 1)
    
    lesson_title = matched_lesson.get("title", "") if matched_lesson else ""
    lesson_num = matched_lesson.get("number", "") if matched_lesson else ""
    q_lower = (question or "").lower()
    
    lines = []
    
    # 1. Mode: Tóm tắt ghi chú học tập (Study Notes)
    if any(k in q_lower for k in ["tóm tắt", "ghi chú", "dễ ôn", "mẹo ghi nhớ", "note"]):
        lines.append("### 📝 PHIẾU GHI CHÚ HỌC TẬP TỪ HÌNH ẢNH SGK")
        lines.append(f"**Nguồn:** {src} (Trang {pg}) · **Bài:** {lesson_num} {lesson_title}\n")
        lines.append("#### 1. Tiêu đề & Nội dung quan sát chính:")
        lines.append(f"- **Đối tượng quan sát:** {lbl}")
        if crop_info:
            lines.append("- **Vùng trọng tâm:** Khu vực được khoanh vùng tập trung thể hiện các chi tiết cấu trúc, biến đổi trạng thái hoặc chu trình khoa học cốt lõi.")
        if matched_lesson and matched_lesson.get("summary"):
            for sm in matched_lesson.get("summary", [])[:2]:
                lines.append(f"- {sm}")
        else:
            lines.append("- Hình ảnh thể hiện các quy luật vận động, biến đổi hình thái và mối liên hệ giữa cấu tạo và chức năng của các sự vật, hiện tượng trong tự nhiên.")
            
        lines.append("\n#### 2. Thuật ngữ & Khái niệm quan trọng:")
        seen_t = set()
        if matched_lesson and matched_lesson.get("terms"):
            for t in matched_lesson.get("terms", []):
                t_name = t.get('term', '').strip()
                t_def = t.get('definition', '').strip()
                if t_name and t_name.lower() not in seen_t and len(t_def) > 15:
                    seen_t.add(t_name.lower())
                    lines.append(f"- **{t_name}**: {t_def}")
                    if len(seen_t) >= 3:
                        break
        if not seen_t:
            lines.append("- **Trao đổi chất & Chuyển hóa năng lượng**: Quá trình cơ thể lấy vật chất từ môi trường biến đổi thành chất cần thiết và tạo năng lượng, đồng thời thải chất bã ra ngoài.")
            lines.append("- **Sinh trưởng & Phát triển**: Sinh trưởng là sự tăng về kích thước và khối lượng; Phát triển là sự biến đổi về chất lượng, hình thành cơ quan mới.")
            
        lines.append("\n#### 3. Kết luận khoa học cốt lõi:")
        if matched_lesson and matched_lesson.get("objectives"):
            for obj in matched_lesson.get("objectives", [])[:2]:
                lines.append(f"- {obj}")
        else:
            lines.append(f"- Giúp học sinh nhận diện trực quan bản chất hiện tượng khoa học được quy định trong chương trình SGK KHTN Lớp {grade}.")
            
        lines.append("\n#### 4. 💡 Mẹo ghi nhớ nhanh:")
        lines.append("- *\"Nhìn hình nhớ ý, theo hướng mũi tên, liên hệ thực tế, nhớ lâu vững bền!\"* - Kết hợp các chú thích số/chữ trên hình để tái hiện toàn bộ tiến trình bài học.")

    # 2. Mode: Tạo câu hỏi trắc nghiệm (Generate Quiz)
    elif any(k in q_lower for k in ["trắc nghiệm", "tạo 5 câu", "4 lựa chọn", "quiz"]):
        lines.append("### 📋 BỘ 5 CÂU HỎI TRẮC NGHIỆM TỪ HÌNH ẢNH SGK")
        lines.append(f"*(Dựa trên {lbl} · {src} · Trang {pg})*\n")
        
        sample_q = [
            ("Hình ảnh/sơ đồ trên minh họa cho nội dung kiến thức nào?", 
             ["Sự trao đổi chất và chuyển hóa năng lượng", "Cấu tạo nguyên tử và bảng tuần hoàn", "Định luật bảo toàn khối lượng", "Sự khúc xạ và phản xạ ánh sáng"], 
             "A", "Hình ảnh thể hiện rõ các quá trình biến đổi hình thái và trao đổi vật chất của sinh vật."),
            ("Mũi tên hoặc trình tự trong sơ đồ thể hiện điều gì?",
             ["Mối quan hệ liên tục theo thời gian hoặc chu trình", "Sự ngẫu nhiên không có quy luật", "Hiện tượng triệt tiêu năng lượng", "Không có ý nghĩa khoa học"],
             "A", "Các mũi tên khoa học chỉ hướng diễn tiến hoặc chu trình biến đổi sinh học/vật lý/hóa học."),
            ("Vai trò chính của hiện tượng được mô tả trong hình là gì?",
             ["Cung cấp năng lượng và duy trì sự sống/vận động", "Làm giảm đa dạng sinh học", "Ngừng quá trình trao đổi chất", "Tăng lượng rác thải môi trường"],
             "A", "Hiện tượng giúp duy trì hoạt động sống, sinh trưởng và cân bằng tự nhiên."),
            ("Dựa vào thông tin trên hình, khẳng định nào sau đây là ĐÚNG?",
             ["Các giai đoạn có mối liên hệ mật thiết và chuyển tiếp nhau", "Sinh trưởng không liên quan đến phát triển", "Môi trường không ảnh hưởng đến sinh vật", "Năng lượng tự sinh ra không cần chuyển hóa"],
             "A", "Các giai đoạn luôn liên kết và kế thừa nhau trong quá trình phát triển."),
            ("Từ sơ đồ hình ảnh, bài học thực tiễn rút ra là gì?",
             ["Cần chăm sóc, bảo vệ và tạo điều kiện thuận lợi cho sinh vật phát triển", "Không cần tưới nước cho cây", "Chỉ nuôi nhốt không cần dinh dưỡng", "Ngắt bỏ toàn bộ lá cây khi mới mọc"],
             "A", "Cần hiểu quy luật tự nhiên để có biện pháp chăm sóc và ứng dụng hợp lý trong thực tiễn.")
        ]
        for idx, (quest, opts, corr, exp) in enumerate(sample_q, 1):
            lines.append(f"**Câu {idx}:** {quest}")
            for opt_idx, opt in enumerate(opts):
                prefix = chr(ord('A') + opt_idx)
                lines.append(f"  {prefix}. {opt}")
            lines.append(f"  👉 **Đáp án đúng:** {corr} — *Giải thích:* {exp}\n")

    # 3. Mode: Giải thích theo lớp / Khái niệm
    elif any(k in q_lower for k in ["giải thích", "lớp", "minh họa điều gì", "kết luận"]):
        lines.append(f"### 🔬 GIẢI THÍCH CHI TIẾT HÌNH ẢNH SGK KHTN {grade}")
        lines.append(f"Chào em! Đây là hình ảnh **{lbl}** thuộc **{src}** (Trang {pg}).\n")
        lines.append("#### 1. Khái niệm & Hiện tượng thể hiện trên hình:")
        if matched_lesson and matched_lesson.get("content"):
            lines.append(f"- {matched_lesson.get('content')[:300]}...")
        else:
            lines.append("- Hình ảnh mô tả tiến trình biến đổi tự nhiên của sự vật/hiện tượng theo các quy luật cơ bản của Khoa học tự nhiên.")
            
        lines.append("\n#### 2. Diễn biến và Mối quan hệ giữa các thành phần:")
        lines.append("- Các mũi tên và ký hiệu trên hình liên kết các giai đoạn/yếu tố, cho thấy tính logic và trật tự nghiêm ngặt trong tự nhiên.")
        lines.append("- Môi trường cung cấp các yếu tố cần thiết (ánh sáng, nước, chất dinh dưỡng, năng lượng) để quá trình diễn ra liên tục.")
        
        lines.append("\n#### 3. Kết luận & Câu hỏi tự kiểm tra:")
        lines.append("- **Kết luận:** Nắm vững cấu trúc sơ đồ hình ảnh giúp em ghi nhớ bản chất hiện tượng nhanh hơn đọc văn bản thông thường.")
        lines.append("- **Câu hỏi tự kiểm tra:** *Em hãy chỉ ra điểm giống và khác nhau giữa các giai đoạn trên hình và lấy thêm 1 ví dụ trong đời sống quanh em?*")

    # 4. Default / General questions
    else:
        lines.append(f"Chào em! Dưới đây là giải đáp cho câu hỏi của em về **{lbl}** ({src} · Trang {pg}):\n")
        lines.append("### Phân tích trọng tâm:")
        lines.append(f"- **Đối tượng:** {lbl}")
        lines.append(f"- **Giải đáp:** {question}")
        if matched_lesson and matched_lesson.get("objectives"):
            lines.append(f"- **Kiến thức bài học ({matched_lesson.get('number', '')} {matched_lesson.get('title', '')}):**")
            for obj in matched_lesson.get("objectives", [])[:3]:
                lines.append(f"  * {obj}")
        lines.append("\n💡 *Em có thể khoanh vùng một khu vực cụ thể trên hình để tìm hiểu sâu hơn nhé!*")
        
    lines.append("\n🏫 *Hệ thống Trợ lý AI Khoa học Tự nhiên · Trường THCS Huỳnh Bá Chánh*")
    return "\n".join(lines)

