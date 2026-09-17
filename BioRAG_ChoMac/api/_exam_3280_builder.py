"""Builder for Exam Packages adhering to Ministry of Education Dispatch 3280/BGDĐT-GDTrH.

Generates official Vietnamese standard Exam Packages (.docx) for Natural Sciences (KHTN),
containing all 4 mandatory components:
1. Khung Ma trận Đề kiểm tra định kỳ (Matrix Table 4 cognitive levels: NB, TH, VD, VDC).
2. Bản đặc tả Ma trận Đề kiểm tra (Specification Table linking learning outcomes to questions).
3. Đề kiểm tra chính thức (Exam Paper with Student Box, Score Box, Bubble Sheet, TNKQ & TL).
4. Đáp án và Hướng dẫn chấm chi tiết (Answer Key & Step-by-step Grading Rubric).
"""

from __future__ import annotations

import io
import re
from typing import Any, Dict, List, Optional

import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn


# Color Palette (Consistent with Ministry & School Official Documents)
COLOR_PRIMARY = RGBColor(15, 45, 89)       # Dark Navy #0F2D59
COLOR_SECONDARY = RGBColor(30, 64, 175)    # Royal Blue #1E40AF
COLOR_BODY = RGBColor(0, 0, 0)             # Pure Black #000000
COLOR_MUTED = RGBColor(80, 80, 80)         # Gray #505050

HEX_HEADER_BG = "EBF2FA"                   # Soft Ice Blue
HEX_BORDER = "B8CCE4"                      # Soft Elegant Border
HEX_ALT_BG = "F8FAFC"                      # Clean Off-white
HEX_NOTE_BG = "FFFBEB"                     # Soft Amber Note


def _set_cell_background(cell, fill_hex: str) -> None:
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def _set_cell_margins(cell, top: int = 100, bottom: int = 100, left: int = 140, right: int = 140) -> None:
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def _set_table_borders(table, color: str = HEX_BORDER, sz: str = "4", val: str = "single") -> None:
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'</w:tblBorders>'
        )
        tblPr[0].append(borders)


def _set_table_row_cant_split(row) -> None:
    trPr = row._element.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))


def _apply_run_font(
    run,
    font_name: str = "Times New Roman",
    size_pt: float = 13,
    bold: bool = False,
    italic: bool = False,
    color: Optional[RGBColor] = None,
) -> None:
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color
    rPr = run._element.get_or_add_rPr()
    rFonts = parse_xml(
        f'<w:rFonts {nsdecls("w")} w:ascii="{font_name}" w:hAnsi="{font_name}" w:cs="{font_name}"/>'
    )
    rPr.append(rFonts)


def _add_p_styled(
    doc_or_cell,
    text: str = "",
    font_name: str = "Times New Roman",
    size_pt: float = 13,
    bold: bool = False,
    italic: bool = False,
    color: Optional[RGBColor] = None,
    align: WD_ALIGN_PARAGRAPH = WD_ALIGN_PARAGRAPH.JUSTIFY,
    space_before_pt: float = 0,
    space_after_pt: float = 3,
    line_spacing: float = 1.15,
):
    p = doc_or_cell.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before_pt)
    p.paragraph_format.space_after = Pt(space_after_pt)
    p.paragraph_format.line_spacing = line_spacing

    if text:
        run = p.add_run(text)
        _apply_run_font(run, font_name, size_pt, bold, italic, color)
    return p


def build_exam_package_3280_doc(exam_data: Dict[str, Any]) -> docx.Document:
    """Build a complete, professionally formatted Dispatch 3280 exam document."""
    doc = docx.Document()

    # 1. Page Setup A4 & Margins (Decree 30/2020/NĐ-CP: Lề trái 2.5cm, còn lại 2.0cm)
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.0)

    # Normalize Metadata
    grade = exam_data.get("grade") or 6
    school_name = str(exam_data.get("school_name") or "TRƯỜNG THCS HUỲNH BÁ CHÁNH").strip()
    department = str(exam_data.get("department") or "TỔ: KHOA HỌC TỰ NHIÊN").strip()
    school_year = str(exam_data.get("school_year") or "2025 - 2026").strip()
    semester = str(exam_data.get("semester") or "HỌC KỲ I").strip()
    exam_type = str(exam_data.get("exam_type") or "ĐỊNH KỲ").strip().upper()
    duration_min = exam_data.get("duration_minutes") or 45
    title = str(exam_data.get("title") or f"ĐỀ KIỂM TRA {exam_type} MÔN KHOA HỌC TỰ NHIÊN {grade}").strip()
    topic = str(exam_data.get("topic") or "Kiến thức trọng tâm Khoa học tự nhiên").strip()

    multiple_choice = exam_data.get("multiple_choice") or []
    essay = exam_data.get("essay") or []

    # Calculate scores & percentages
    tn_count = len(multiple_choice)
    tl_count = len(essay)

    tn_total_score = sum(float(q.get("score") or 0.25) for q in multiple_choice)
    tl_total_score = sum(float(q.get("score") or 1.5) for q in essay)
    total_score = tn_total_score + tl_total_score
    if total_score == 0:
        total_score = 10.0

    ratio_tn_pct = round((tn_total_score / total_score) * 100)
    ratio_tl_pct = 100 - ratio_tn_pct

    # =========================================================================
    # PHẦN 1: KHUNG MA TRẬN ĐỀ KIỂM TRA ĐỊNH KỲ (CÔNG VĂN 3280/BGDĐT-GDTrH)
    # =========================================================================
    _add_p_styled(
        doc, f"{school_name.upper()} — {department.upper()}",
        size_pt=11, bold=True, color=COLOR_MUTED, align=WD_ALIGN_PARAGRAPH.LEFT, space_after_pt=2
    )
    _add_p_styled(
        doc, f"KHUNG MA TRẬN ĐỀ KIỂM TRA {exam_type} MÔN KHOA HỌC TỰ NHIÊN – LỚP {grade}",
        size_pt=14, bold=True, color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=3
    )
    _add_p_styled(
        doc, f"Năm học: {school_year} · Thời gian làm bài: {duration_min} phút · Tỉ lệ: {ratio_tn_pct}% Trắc nghiệm ({tn_total_score:.1f}đ) + {ratio_tl_pct}% Tự luận ({tl_total_score:.1f}đ)",
        size_pt=11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=10
    )

    # Matrix Table Setup
    matrix_table = doc.add_table(rows=2, cols=12)
    matrix_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    matrix_table.autofit = False
    _set_table_borders(matrix_table)

    # Merge header cells
    matrix_table.cell(0, 0).merge(matrix_table.cell(1, 0))  # TT
    matrix_table.cell(0, 1).merge(matrix_table.cell(1, 1))  # Chủ đề
    matrix_table.cell(0, 2).merge(matrix_table.cell(0, 3))  # Nhận biết
    matrix_table.cell(0, 4).merge(matrix_table.cell(0, 5))  # Thông hiểu
    matrix_table.cell(0, 6).merge(matrix_table.cell(0, 7))  # Vận dụng
    matrix_table.cell(0, 8).merge(matrix_table.cell(1, 8))  # Vận dụng cao
    matrix_table.cell(0, 9).merge(matrix_table.cell(0, 10)) # Tổng số câu
    matrix_table.cell(0, 11).merge(matrix_table.cell(1, 11))# Tổng điểm

    col_widths = [
        Cm(1.0), Cm(4.0),
        Cm(1.1), Cm(1.1),
        Cm(1.1), Cm(1.1),
        Cm(1.1), Cm(1.1),
        Cm(1.2),
        Cm(1.1), Cm(1.1),
        Cm(1.6)
    ]

    r0 = matrix_table.rows[0].cells
    r1 = matrix_table.rows[1].cells

    # Labels for Row 0
    r0[0].paragraphs[0].text = "TT"
    r0[1].paragraphs[0].text = "Chủ đề / Đơn vị kiến thức"
    r0[2].paragraphs[0].text = "Nhận biết\n(40%)"
    r0[4].paragraphs[0].text = "Thông hiểu\n(30%)"
    r0[6].paragraphs[0].text = "Vận dụng\n(20%)"
    r0[8].paragraphs[0].text = "Vận dụng cao\n(10%)"
    r0[9].paragraphs[0].text = "Tổng số câu"
    r0[11].paragraphs[0].text = "Tổng điểm\n(Tỉ lệ %)"

    # Sub-labels for Row 1
    r1[2].paragraphs[0].text = "TNKQ"
    r1[3].paragraphs[0].text = "TL"
    r1[4].paragraphs[0].text = "TNKQ"
    r1[5].paragraphs[0].text = "TL"
    r1[6].paragraphs[0].text = "TNKQ"
    r1[7].paragraphs[0].text = "TL"
    r1[9].paragraphs[0].text = "TNKQ"
    r1[10].paragraphs[0].text = "TL"

    # Style Header Rows
    for r_idx, row in enumerate(matrix_table.rows[:2]):
        _set_table_row_cant_split(row)
        for c_idx, cell in enumerate(row.cells):
            cell.width = col_widths[c_idx]
            _set_cell_background(cell, HEX_HEADER_BG)
            _set_cell_margins(cell, 80, 80, 60, 60)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(1)
            for run in p.runs:
                _apply_run_font(run, size_pt=9.5, bold=True, color=COLOR_PRIMARY)

    # Matrix Data Rows
    matrix_rows = exam_data.get("matrix_rows")
    if not matrix_rows:
        # Auto compute matrix rows from questions
        nb_tn = sum(1 for q in multiple_choice if q.get("level") == "NB")
        th_tn = sum(1 for q in multiple_choice if q.get("level") == "TH")
        vd_tn = sum(1 for q in multiple_choice if q.get("level") in ("VD", "VDC"))
        if nb_tn + th_tn + vd_tn == 0 and tn_count > 0:
            nb_tn = round(tn_count * 0.5)
            th_tn = round(tn_count * 0.35)
            vd_tn = tn_count - nb_tn - th_tn

        vd_tl = sum(1 for q in essay if q.get("level") in ("VD", "TH"))
        vdc_tl = sum(1 for q in essay if q.get("level") == "VDC")
        if vd_tl + vdc_tl == 0 and tl_count > 0:
            vd_tl = max(1, tl_count - 1)
            vdc_tl = 1 if tl_count > 1 else 0

        matrix_rows = [
            {
                "stt": 1,
                "topic": topic,
                "nb_tn": nb_tn, "nb_tl": 0,
                "th_tn": th_tn, "th_tl": 0,
                "vd_tn": vd_tn, "vd_tl": vd_tl,
                "vdc_tn": 0, "vdc_tl": vdc_tl,
                "total_tn": tn_count, "total_tl": tl_count,
                "total_score": total_score
            }
        ]

    for m_idx, row_data in enumerate(matrix_rows, start=1):
        row = matrix_table.add_row()
        _set_table_row_cant_split(row)
        bg = HEX_ALT_BG if m_idx % 2 == 1 else "FFFFFF"
        cells = row.cells
        cells[0].paragraphs[0].text = str(row_data.get("stt") or m_idx)
        cells[1].paragraphs[0].text = str(row_data.get("topic") or topic)
        cells[2].paragraphs[0].text = str(row_data.get("nb_tn") or "-")
        cells[3].paragraphs[0].text = str(row_data.get("nb_tl") or "-")
        cells[4].paragraphs[0].text = str(row_data.get("th_tn") or "-")
        cells[5].paragraphs[0].text = str(row_data.get("th_tl") or "-")
        cells[6].paragraphs[0].text = str(row_data.get("vd_tn") or "-")
        cells[7].paragraphs[0].text = str(row_data.get("vd_tl") or "-")
        cells[8].paragraphs[0].text = str(row_data.get("vdc_tl") or "-")
        cells[9].paragraphs[0].text = str(row_data.get("total_tn") or tn_count)
        cells[10].paragraphs[0].text = str(row_data.get("total_tl") or tl_count)
        cells[11].paragraphs[0].text = f"{float(row_data.get('total_score') or total_score):.1f} đ"

        for c_idx, cell in enumerate(cells):
            cell.width = col_widths[c_idx]
            _set_cell_background(cell, bg)
            _set_cell_margins(cell, 60, 60, 60, 60)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if c_idx == 1 else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.line_spacing = 1.05
            p.paragraph_format.space_after = Pt(1)
            for run in p.runs:
                _apply_run_font(run, size_pt=9.5, bold=(c_idx in (0, 11)))

    # Matrix Summary Row
    sum_row = matrix_table.add_row()
    _set_table_row_cant_split(sum_row)
    sum_cells = sum_row.cells
    sum_cells[0].paragraphs[0].text = ""
    sum_cells[1].paragraphs[0].text = "TỔNG SỐ CÂU / TỔNG ĐIỂM"
    nb_sum = sum(int(r.get("nb_tn") or 0) for r in matrix_rows)
    th_sum = sum(int(r.get("th_tn") or 0) for r in matrix_rows)
    vd_tn_sum = sum(int(r.get("vd_tn") or 0) for r in matrix_rows)
    vd_tl_sum = sum(int(r.get("vd_tl") or 0) for r in matrix_rows)
    vdc_tl_sum = sum(int(r.get("vdc_tl") or 0) for r in matrix_rows)

    sum_cells[2].paragraphs[0].text = str(nb_sum)
    sum_cells[3].paragraphs[0].text = "-"
    sum_cells[4].paragraphs[0].text = str(th_sum)
    sum_cells[5].paragraphs[0].text = "-"
    sum_cells[6].paragraphs[0].text = str(vd_tn_sum)
    sum_cells[7].paragraphs[0].text = str(vd_tl_sum)
    sum_cells[8].paragraphs[0].text = str(vdc_tl_sum)
    sum_cells[9].paragraphs[0].text = str(tn_count)
    sum_cells[10].paragraphs[0].text = str(tl_count)
    sum_cells[11].paragraphs[0].text = f"{total_score:.1f} đ\n(100%)"

    for c_idx, cell in enumerate(sum_cells):
        cell.width = col_widths[c_idx]
        _set_cell_background(cell, HEX_HEADER_BG)
        _set_cell_margins(cell, 70, 70, 60, 60)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.space_after = Pt(1)
        for run in p.runs:
            _apply_run_font(run, size_pt=9.5, bold=True, color=COLOR_PRIMARY)

    _add_p_styled(doc, "", space_after_pt=14)

    # =========================================================================
    # PHẦN 2: BẢN ĐẶC TẢ MA TRẬN ĐỀ KIỂM TRA (CÔNG VĂN 3280/BGDĐT-GDTrH)
    # =========================================================================
    _add_p_styled(
        doc, f"BẢN ĐẶC TẢ MA TRẬN ĐỀ KIỂM TRA {exam_type} MÔN KHTN – LỚP {grade}",
        size_pt=13.5, bold=True, color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=3
    )
    _add_p_styled(
        doc, f"(Quy định chi tiết Yêu cầu cần đạt chuẩn GDPT 2018 tương ứng từng câu hỏi)",
        size_pt=11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=8
    )

    spec_table = doc.add_table(rows=1, cols=6)
    spec_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    spec_table.autofit = False
    _set_table_borders(spec_table)

    spec_widths = [Cm(1.0), Cm(3.5), Cm(2.2), Cm(6.3), Cm(1.7), Cm(1.8)]
    spec_headers = [
        "TT",
        "Chủ đề / Đơn vị kiến thức",
        "Mức độ nhận thức",
        "Yêu cầu cần đạt\n(Theo chương trình GDPT 2018)",
        "Số câu hỏi\n(TNKQ/TL)",
        "Câu hỏi số\n(Mã câu)"
    ]

    for c_idx, (text, w) in enumerate(zip(spec_headers, spec_widths)):
        cell = spec_table.rows[0].cells[c_idx]
        cell.width = w
        _set_cell_background(cell, HEX_HEADER_BG)
        _set_cell_margins(cell, 80, 80, 70, 70)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.05
        p.paragraph_format.space_after = Pt(1)
        run = p.add_run(text)
        _apply_run_font(run, size_pt=10, bold=True, color=COLOR_PRIMARY)

    spec_rows = exam_data.get("spec_rows")
    if not spec_rows:
        # Default specification layout based on topic
        spec_rows = [
            {
                "stt": 1,
                "topic": topic,
                "level": "Nhận biết",
                "requirement": f"Nhận biết và nêu được các khái niệm, định nghĩa, đặc điểm hoặc cấu tạo cơ bản liên quan đến {topic}.",
                "question_type": f"{round(tn_count * 0.5)} TNKQ",
                "question_refs": f"Câu 1 – Câu {round(tn_count * 0.5)}"
            },
            {
                "stt": 2,
                "topic": topic,
                "level": "Thông hiểu",
                "requirement": f"Giải thích được nguyên lý, phân biệt các dấu hiệu, mối quan hệ nhân quả và cơ chế hoạt động trong {topic}.",
                "question_type": f"{round(tn_count * 0.35)} TNKQ",
                "question_refs": f"Câu {round(tn_count * 0.5) + 1} – Câu {round(tn_count * 0.85)}"
            },
            {
                "stt": 3,
                "topic": topic,
                "level": "Vận dụng",
                "requirement": f"Vận dụng kiến thức bài học để giải thích hiện tượng thực tế, giải quyết tình huống học tập hoặc bài tập tính toán định lượng.",
                "question_type": f"{max(1, tn_count - round(tn_count * 0.85))} TNKQ + 1 TL",
                "question_refs": f"Câu {round(tn_count * 0.85) + 1} – {tn_count} (TN), Câu 1 (TL)"
            },
            {
                "stt": 4,
                "topic": topic,
                "level": "Vận dụng cao",
                "requirement": f"Đề xuất giải pháp, phân tích hiện tượng thực tiễn nâng cao, liên hệ bảo vệ sức khỏe, môi trường hoặc thí nghiệm sáng tạo.",
                "question_type": "1 TL",
                "question_refs": "Câu 2 (TL)"
            }
        ]

    for s_idx, row_data in enumerate(spec_rows, start=1):
        row = spec_table.add_row()
        _set_table_row_cant_split(row)
        bg = HEX_ALT_BG if s_idx % 2 == 1 else "FFFFFF"
        cells = row.cells
        cells[0].paragraphs[0].text = str(row_data.get("stt") or s_idx)
        cells[1].paragraphs[0].text = str(row_data.get("topic") or topic)
        cells[2].paragraphs[0].text = str(row_data.get("level") or "Nhận biết")
        cells[3].paragraphs[0].text = str(row_data.get("requirement") or "")
        cells[4].paragraphs[0].text = str(row_data.get("question_type") or "TNKQ")
        cells[5].paragraphs[0].text = str(row_data.get("question_refs") or f"Câu {s_idx}")

        for c_idx, cell in enumerate(cells):
            cell.width = spec_widths[c_idx]
            _set_cell_background(cell, bg)
            _set_cell_margins(cell, 70, 70, 70, 70)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if c_idx in (1, 3) else WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.line_spacing = 1.12
            p.paragraph_format.space_after = Pt(2)
            for run in p.runs:
                _apply_run_font(run, size_pt=9.5, bold=(c_idx in (0, 2)))

    # Page Break for Exam Paper
    doc.add_page_break()

    # =========================================================================
    # PHẦN 3: ĐỀ KIỂM TRA CHÍNH THỨC
    # =========================================================================
    exam_head_table = doc.add_table(rows=1, cols=2)
    exam_head_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    exam_head_table.autofit = False

    c_left = exam_head_table.cell(0, 0)
    c_right = exam_head_table.cell(0, 1)
    c_left.width = Cm(8.0)
    c_right.width = Cm(8.5)
    _set_cell_margins(c_left, 0, 0, 0, 0)
    _set_cell_margins(c_right, 0, 0, 0, 0)

    _add_p_styled(c_left, school_name.upper(), size_pt=11.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=1)
    _add_p_styled(c_left, department.upper(), size_pt=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=2)
    _add_p_styled(c_left, "—————————", size_pt=10, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=4)
    _add_p_styled(c_left, f"ĐỀ KIỂM TRA {exam_type}", size_pt=12, bold=True, color=COLOR_SECONDARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=1)
    exam_code = str(exam_data.get("exam_code") or "").strip()
    if exam_code:
        _add_p_styled(c_left, f"MÃ ĐỀ THI: {exam_code}", size_pt=11, bold=True, color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=1)
    _add_p_styled(c_left, "(Đề thi gồm có 02 trang)", size_pt=10, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=0)

    _add_p_styled(c_right, f"MÔN: KHOA HỌC TỰ NHIÊN – LỚP {grade}", size_pt=12, bold=True, color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=1)
    _add_p_styled(c_right, f"Năm học: {school_year} – {semester}", size_pt=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=2)
    _add_p_styled(c_right, f"Thời gian làm bài: {duration_min} phút", size_pt=11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=1)
    _add_p_styled(c_right, "(Không kể thời gian phát đề)", size_pt=10, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=0)

    _add_p_styled(doc, "", space_after_pt=6)

    # Student Info & Score Table
    score_table = doc.add_table(rows=2, cols=2)
    score_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    score_table.autofit = False
    _set_table_borders(score_table, color="7F7F7F", sz="6")

    # Row 0: Student Info Bar
    s_r0 = score_table.rows[0].cells
    s_r0[0].merge(s_r0[1])
    s_r0[0].width = Cm(16.5)
    _set_cell_background(s_r0[0], "FDFDFD")
    _set_cell_margins(s_r0[0], 100, 100, 140, 140)
    p_info = s_r0[0].paragraphs[0]
    p_info.paragraph_format.line_spacing = 1.2
    p_info.paragraph_format.space_after = Pt(2)
    run_info = p_info.add_run(
        "Họ và tên học sinh: ............................................................................   Lớp: .....................   SBD: ....................."
    )
    _apply_run_font(run_info, size_pt=11.5, bold=False)

    # Row 1: Score & Teacher Feedback
    s_r1 = score_table.rows[1].cells
    s_r1[0].width = Cm(4.5)
    s_r1[1].width = Cm(12.0)
    _set_cell_margins(s_r1[0], 80, 80, 100, 100)
    _set_cell_margins(s_r1[1], 80, 80, 100, 100)

    p_score_hdr = s_r1[0].paragraphs[0]
    p_score_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_score_hdr.paragraph_format.space_after = Pt(30)
    run_sc_hdr = p_score_hdr.add_run("ĐIỂM SỐ\n\n\n")
    _apply_run_font(run_sc_hdr, size_pt=11, bold=True)

    p_fb_hdr = s_r1[1].paragraphs[0]
    p_fb_hdr.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_fb_hdr.paragraph_format.space_after = Pt(30)
    run_fb_hdr = p_fb_hdr.add_run("LỜI NHẬN XÉT CỦA THẦY / CÔ GIÁO:\n\n\n")
    _apply_run_font(run_fb_hdr, size_pt=11, bold=True, italic=True)

    _add_p_styled(doc, "", space_after_pt=6)

    # Section I: TRẮC NGHIỆM KHÁCH QUAN
    _add_p_styled(
        doc, f"I. PHẦN TRẮC NGHIỆM KHÁCH QUAN ({tn_total_score:.1f} điểm)",
        size_pt=13, bold=True, color=COLOR_PRIMARY, space_before_pt=4, space_after_pt=2
    )
    _add_p_styled(
        doc, f"Em hãy chọn một phương án trả lời đúng nhất (A, B, C hoặc D) và điền vào Bảng trả lời trắc nghiệm dưới đây:",
        size_pt=11.5, italic=True, space_after_pt=4
    )

    # Bubble Answer Sheet Table (Grid 10 columns per row to fit A4 width)
    if tn_count > 0:
        chunk_size = 10
        for chunk_idx in range(0, tn_count, chunk_size):
            chunk = multiple_choice[chunk_idx:chunk_idx + chunk_size]
            num_cols = len(chunk)
            ans_grid = doc.add_table(rows=2, cols=num_cols)
            ans_grid.alignment = WD_TABLE_ALIGNMENT.CENTER
            ans_grid.autofit = False
            _set_table_borders(ans_grid, color="999999", sz="4")
            w_col = Cm(16.5 / max(num_cols, 10))

            for i in range(num_cols):
                q_num = chunk_idx + i + 1
                # Header: C1, C2...
                c_h = ans_grid.rows[0].cells[i]
                c_h.width = w_col
                _set_cell_background(c_h, HEX_HEADER_BG)
                _set_cell_margins(c_h, 50, 50, 30, 30)
                p = c_h.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_after = Pt(0)
                run = p.add_run(f"C{q_num}")
                _apply_run_font(run, size_pt=9.0, bold=True, color=COLOR_PRIMARY)

                # Box to fill: [   ]
                c_b = ans_grid.rows[1].cells[i]
                c_b.width = w_col
                _set_cell_margins(c_b, 60, 60, 30, 30)
                pb = c_b.paragraphs[0]
                pb.alignment = WD_ALIGN_PARAGRAPH.CENTER
                pb.paragraph_format.space_after = Pt(0)
                run_b = pb.add_run("")
                _apply_run_font(run_b, size_pt=10, bold=True)

            _add_p_styled(doc, "", space_after_pt=2)

        _add_p_styled(doc, "", space_after_pt=4)

    # Multiple Choice Questions List
    for q_idx, q in enumerate(multiple_choice, start=1):
        q_text = q.get("question") or f"Câu hỏi {q_idx}"
        q_score = float(q.get("score") or 0.25)
        p_q = _add_p_styled(
            doc, f"Câu {q_idx} ({q_score:.2f} điểm): {q_text}",
            size_pt=12, bold=True, space_before_pt=3, space_after_pt=2
        )

        options = q.get("options") or []
        labels = ["A", "B", "C", "D"]
        for opt_idx, opt in enumerate(options[:4]):
            clean_opt = str(opt).strip()
            # If option doesn't start with letter label, add it
            if not re.match(r"^[A-D][\.\:\)]", clean_opt):
                clean_opt = f"{labels[opt_idx]}. {clean_opt}"
            _add_p_styled(
                doc, f"    {clean_opt}",
                size_pt=11.5, space_after_pt=1.5, align=WD_ALIGN_PARAGRAPH.LEFT
            )

    _add_p_styled(doc, "", space_after_pt=6)

    # Section II: TỰ LUẬN
    if tl_count > 0:
        _add_p_styled(
            doc, f"II. PHẦN TỰ LUẬN ({tl_total_score:.1f} điểm)",
            size_pt=13, bold=True, color=COLOR_PRIMARY, space_before_pt=6, space_after_pt=3
        )
        _add_p_styled(
            doc, "Học sinh trình bày câu trả lời chi tiết vào giấy làm bài:",
            size_pt=11.5, italic=True, space_after_pt=4
        )

        for e_idx, eq in enumerate(essay, start=1):
            eq_text = eq.get("question") or f"Câu hỏi tự luận {e_idx}"
            eq_score = float(eq.get("score") or 1.5)
            _add_p_styled(
                doc, f"Câu {e_idx} ({eq_score:.1f} điểm): {eq_text}",
                size_pt=12, bold=True, space_before_pt=4, space_after_pt=3
            )
            # Add dotted lines for answer writing
            _add_p_styled(doc, "    Bài làm: ...................................................................................................................................................", size_pt=11, italic=True, color=COLOR_MUTED, space_after_pt=2)
            _add_p_styled(doc, "    .................................................................................................................................................................", size_pt=11, italic=True, color=COLOR_MUTED, space_after_pt=2)
            _add_p_styled(doc, "    .................................................................................................................................................................", size_pt=11, italic=True, color=COLOR_MUTED, space_after_pt=6)

    # Page Break for Answer Key
    doc.add_page_break()

    # =========================================================================
    # PHẦN 4: ĐÁP ÁN VÀ HƯỚNG DẪN CHẤM
    # =========================================================================
    _add_p_styled(
        doc, f"ĐÁP ÁN VÀ HƯỚNG DẪN CHẤM ĐỀ KIỂM TRA {exam_type}",
        size_pt=14, bold=True, color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=2
    )
    _add_p_styled(
        doc, f"MÔN: KHOA HỌC TỰ NHIÊN – LỚP {grade} · Năm học: {school_year}",
        size_pt=12, bold=True, color=COLOR_SECONDARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=2 if exam_code else 8
    )
    if exam_code:
        _add_p_styled(
            doc, f"MÃ ĐỀ: {exam_code}",
            size_pt=11.5, bold=True, color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=8
        )

    # 1. Đáp án Trắc nghiệm
    _add_p_styled(
        doc, f"I. ĐÁP ÁN PHẦN TRẮC NGHIỆM KHÁCH QUAN ({tn_total_score:.1f} điểm)",
        size_pt=12.5, bold=True, color=COLOR_PRIMARY, space_before_pt=4, space_after_pt=3
    )

    if tn_count > 0:
        chunk_size = 10
        labels = ["A", "B", "C", "D"]
        for chunk_idx in range(0, tn_count, chunk_size):
            chunk = multiple_choice[chunk_idx:chunk_idx + chunk_size]
            num_cols = len(chunk)
            ans_table = doc.add_table(rows=2, cols=num_cols)
            ans_table.alignment = WD_TABLE_ALIGNMENT.CENTER
            ans_table.autofit = False
            _set_table_borders(ans_table)

            w_col = Cm(16.5 / max(num_cols, 10))
            for i, q in enumerate(chunk):
                q_num = chunk_idx + i + 1
                # Header
                c_h = ans_table.rows[0].cells[i]
                c_h.width = w_col
                _set_cell_background(c_h, HEX_HEADER_BG)
                _set_cell_margins(c_h, 50, 50, 30, 30)
                p = c_h.paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p.paragraph_format.space_after = Pt(0)
                run = p.add_run(f"Câu {q_num}")
                _apply_run_font(run, size_pt=9.0, bold=True, color=COLOR_PRIMARY)

                # Answer
                ans_key = str(q.get("answer_key") or "").strip().upper()
                if not ans_key and "answer_index" in q:
                    try:
                        a_idx = int(q["answer_index"])
                        if 0 <= a_idx < len(labels):
                            ans_key = labels[a_idx]
                    except Exception:
                        pass
                if not ans_key:
                    ans_key = "A"

                c_b = ans_table.rows[1].cells[i]
                c_b.width = w_col
                _set_cell_margins(c_b, 50, 50, 30, 30)
                pb = c_b.paragraphs[0]
                pb.alignment = WD_ALIGN_PARAGRAPH.CENTER
                pb.paragraph_format.space_after = Pt(0)
                run_b = pb.add_run(ans_key)
                _apply_run_font(run_b, size_pt=11, bold=True, color=COLOR_SECONDARY)

            _add_p_styled(doc, "", space_after_pt=2)

        _add_p_styled(doc, "", space_after_pt=4)

        # Brief explanation table or list
        _add_p_styled(doc, "* Hướng dẫn giải thích chi tiết trắc nghiệm:", size_pt=11, bold=True, italic=True, space_after_pt=2)
        for q_i, q in enumerate(multiple_choice, start=1):
            expl = q.get("explanation") or "Dựa trên ngữ liệu sách giáo khoa KNTT."
            ans_key = str(q.get("answer_key") or "").strip().upper()
            if not ans_key and "answer_index" in q:
                try:
                    a_idx = int(q["answer_index"])
                    if 0 <= a_idx < len(labels):
                        ans_key = labels[a_idx]
                except Exception:
                    pass
            if not ans_key:
                ans_key = "A"
            _add_p_styled(
                doc, f"  - Câu {q_i} (Đáp án {ans_key}): {expl}",
                size_pt=10.5, space_after_pt=1.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY
            )

    _add_p_styled(doc, "", space_after_pt=6)

    # 2. Hướng dẫn chấm Tự luận
    if tl_count > 0:
        _add_p_styled(
            doc, f"II. HƯỚNG DẪN CHẤM PHẦN TỰ LUẬN ({tl_total_score:.1f} điểm)",
            size_pt=12.5, bold=True, color=COLOR_PRIMARY, space_before_pt=6, space_after_pt=3
        )

        rubric_table = doc.add_table(rows=1, cols=3)
        rubric_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        rubric_table.autofit = False
        _set_table_borders(rubric_table)

        r_widths = [Cm(2.0), Cm(12.5), Cm(2.0)]
        r_headers = ["Câu hỏi", "Nội dung yêu cầu cần đạt / Hướng dẫn chấm", "Điểm số"]

        for c_idx, (text, w) in enumerate(zip(r_headers, r_widths)):
            cell = rubric_table.rows[0].cells[c_idx]
            cell.width = w
            _set_cell_background(cell, HEX_HEADER_BG)
            _set_cell_margins(cell, 80, 80, 80, 80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(text)
            _apply_run_font(run, size_pt=10, bold=True, color=COLOR_PRIMARY)

        for e_idx, eq in enumerate(essay, start=1):
            rubric_steps = eq.get("rubric") or []
            eq_score = float(eq.get("score") or 1.5)
            if not rubric_steps:
                rubric_steps = [{"step": str(eq.get("question") or ""), "score": eq_score}]

            for s_i, step in enumerate(rubric_steps):
                row = rubric_table.add_row()
                _set_table_row_cant_split(row)
                cells = row.cells
                cells[0].paragraphs[0].text = f"Câu {e_idx}" if s_i == 0 else ""
                cells[1].paragraphs[0].text = str(step.get("step") or "")
                cells[2].paragraphs[0].text = f"{float(step.get('score') or 0.5):.2f} đ"

                for c_idx, cell in enumerate(cells):
                    cell.width = r_widths[c_idx]
                    _set_cell_margins(cell, 60, 60, 70, 70)
                    p = cell.paragraphs[0]
                    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY if c_idx == 1 else WD_ALIGN_PARAGRAPH.CENTER
                    p.paragraph_format.line_spacing = 1.12
                    p.paragraph_format.space_after = Pt(2)
                    for run in p.runs:
                        _apply_run_font(run, size_pt=10, bold=(c_idx in (0, 2) and s_i == 0))

        _add_p_styled(doc, "", space_after_pt=12)

    # Signature Table
    sign_table = doc.add_table(rows=1, cols=2)
    sign_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sign_table.autofit = False

    s_left = sign_table.cell(0, 0)
    s_right = sign_table.cell(0, 1)
    s_left.width = Cm(8.0)
    s_right.width = Cm(8.5)
    _set_cell_margins(s_left, 0, 0, 0, 0)
    _set_cell_margins(s_right, 0, 0, 0, 0)

    _add_p_styled(s_left, "DUYỆT CỦA TỔ TRƯỞNG CHUYÊN MÔN", size_pt=11.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=2)
    _add_p_styled(s_left, "(Ký và ghi rõ họ tên)", size_pt=11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=45)
    _add_p_styled(s_left, "................................................................", size_pt=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=0)

    _add_p_styled(s_right, "Ngày ..... tháng ..... năm 202...", size_pt=11.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=2)
    _add_p_styled(s_right, "GIÁO VIÊN RA ĐỀ", size_pt=11.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=2)
    _add_p_styled(s_right, "(Ký và ghi rõ họ tên)", size_pt=11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=45)
    _add_p_styled(s_right, "................................................................", size_pt=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=0)

    return doc


def build_exam_package_3280_bytes(exam_data: Dict[str, Any]) -> io.BytesIO:
    """Generate Word docx and return as an in-memory byte buffer."""
    doc = build_exam_package_3280_doc(exam_data)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


def lesson_to_exam_data(
    lesson: Dict[str, Any],
    exam_type: str = "ĐỊNH KỲ",
    duration: int = 45,
    school_name: str = "TRƯỜNG THCS HUỲNH BÁ CHÁNH",
    department: str = "TỔ: KHOA HỌC TỰ NHIÊN",
    school_year: str = "2025 - 2026",
    target_mcq_count: int = 0,
) -> Dict[str, Any]:
    """Convert any lesson structure into a complete Dispatch 3280 exam package dictionary."""
    grade = lesson.get("grade") or 6
    raw_title = str(lesson.get("title") or "Kiểm tra KHTN").strip()
    topic = str(lesson.get("topic") or raw_title).strip()
    objectives = lesson.get("objectives") or []
    if isinstance(objectives, str):
        objectives = [o.strip("- •* ") for o in objectives.splitlines() if o.strip()]
    sections = lesson.get("sections") or []
    quick_checks = lesson.get("quick_check") or []
    content_str = str(lesson.get("content") or "")

    existing_mcqs = lesson.get("multiple_choice") or []
    target_count = target_mcq_count if target_mcq_count > 0 else (int(lesson.get("count", 0)) or (len(existing_mcqs) if existing_mcqs else 8))
    if target_count < 3:
        target_count = 8
    q_score = 0.25 if target_count >= 20 else 0.5
    labels = ["A", "B", "C", "D"]

    # Build Multiple Choice Questions
    mcqs = []
    if existing_mcqs:
        for idx, q_raw in enumerate(existing_mcqs, start=1):
            opts = q_raw.get("options") or []
            formatted_opts = []
            for o_i, opt in enumerate(opts[:4]):
                clean = str(opt).strip()
                if not re.match(r"^[A-D][\.\:\)]", clean):
                    clean = f"{labels[o_i]}. {clean}"
                formatted_opts.append(clean)
            ans_key = str(q_raw.get("answer_key") or "").strip().upper()
            if not ans_key and "answer_index" in q_raw:
                try:
                    a_idx = int(q_raw["answer_index"])
                    if 0 <= a_idx < len(labels):
                        ans_key = labels[a_idx]
                except Exception:
                    pass
            if not ans_key:
                ans_key = "A"
            mcqs.append({
                "id": idx,
                "level": q_raw.get("level") or ("NB" if idx <= round(target_count * 0.4) else ("TH" if idx <= round(target_count * 0.7) else "VD")),
                "question": q_raw.get("question") or f"Câu hỏi {idx}",
                "options": formatted_opts,
                "answer_key": ans_key,
                "score": float(q_raw.get("score") or q_score),
                "explanation": q_raw.get("explanation") or f"Dựa trên kiến thức {topic} SGK KHTN {grade}."
            })
    else:
        for idx, qc in enumerate(quick_checks, start=1):
            ans_idx = int(qc.get("answer_index", 0))
            ans_key = labels[ans_idx] if 0 <= ans_idx < len(labels) else "A"
            level = "NB" if idx == 1 else "TH" if idx == 2 else "VD"
            options = qc.get("options") or []
            formatted_opts = []
            for o_i, opt in enumerate(options[:4]):
                clean = str(opt).strip()
                if not re.match(r"^[A-D][\.\:\)]", clean):
                    clean = f"{labels[o_i]}. {clean}"
                formatted_opts.append(clean)
            mcqs.append({
                "id": idx,
                "level": level,
                "question": qc.get("question") or f"Câu hỏi {idx}",
                "options": formatted_opts,
                "answer_key": ans_key,
                "score": q_score,
                "explanation": qc.get("explanation") or f"Dựa trên kiến thức {topic} SGK KHTN {grade}."
            })

    # Expand if needed to reach target_count
    if len(mcqs) < target_count:
        knowledge_facts = []
        for obj in objectives:
            if len(obj) > 10:
                knowledge_facts.append(obj)
        for sec in sections:
            sec_title = sec.get("title", "")
            for b in sec.get("bullets") or []:
                if len(b) > 8:
                    knowledge_facts.append(f"{sec_title}: {b}" if sec_title else b)
            for p in sec.get("paragraphs") or []:
                for sent in re.split(r"[\.\;\n]", p):
                    s = sent.strip()
                    if 20 <= len(s) <= 150:
                        knowledge_facts.append(s)
        if content_str:
            for sent in re.split(r"[\.\;\n]", content_str):
                s = sent.strip()
                if 15 <= len(s) <= 150:
                    knowledge_facts.append(s)

        is_random_composite = any(kw in str(topic).lower() for kw in [
            "ngẫu nhiên", "ngau nhien", "tổng hợp", "tong hop", "toàn bộ", "toan bo",
            "học kỳ", "hoc ky", "thi thử", "thi thu", "ôn tập cuối kỳ", "on tap cuoi ky", "random"
        ])

        if is_random_composite or len(knowledge_facts) < 15:
            try:
                from src.rag.book_rag import find_relevant_chunks, load_all_chunks
                chunks = load_all_chunks()
                g_chunks = [c for c in chunks if f"KHTN {grade}" in str(c.get("source", "")) or f"KHTN{grade}" in str(c.get("source", ""))]
                if is_random_composite:
                    g_sorted = sorted(g_chunks, key=lambda c: int(c.get("page") or 0))
                    step = max(1, len(g_sorted) // 16)
                    rel = [g_sorted[i] for i in range(0, len(g_sorted), step)][:16]
                else:
                    rel = find_relevant_chunks(topic, g_chunks or chunks, 10)
                for c in rel:
                    for sent in re.split(r"[\.\;\n]", c.get("text", "")):
                        s = sent.strip()
                        if 20 <= len(s) <= 160 and not s.startswith("Hình") and not s.startswith("Bảng"):
                            knowledge_facts.append(s)
            except Exception:
                pass

        templates = [
            ("NB", "Khẳng định nào sau đây là ĐÚNG khi nói về {subject}?",
             "Luôn có đặc tính ngược lại với thực tế tự nhiên",
             "Không tham gia vào quá trình trao đổi chất hay hoạt động sống",
             "Có cấu trúc hoàn toàn ngẫu nhiên và không có chức năng xác định"),
            ("NB", "Theo chương trình Khoa học tự nhiên {grade}, {subject} có đặc điểm nào sau đây?",
             "Chỉ tồn tại ở dạng nhân tạo do con người tổng hợp",
             "Không chịu tác động của bất kỳ yếu tố môi trường nào",
             "Biến mất hoàn toàn khi điều kiện nhiệt độ thay đổi nhẹ"),
            ("TH", "Nội dung nào sau đây phản ánh CHÍNH XÁC bản chất của {subject}?",
             "Chỉ đóng vai trò thứ yếu và có thể loại bỏ mà không ảnh hưởng",
             "Diễn ra độc lập hoàn toàn mà không cần vật chất hay năng lượng",
             "Luôn tạo ra sản phẩm độc hại cho các sinh vật xung quanh"),
            ("TH", "Khi giải thích về cơ chế hoạt động của {subject}, nhận định nào sau đây là đúng?",
             "Xảy ra theo quy luật tự phát không tuân theo các nguyên lý khoa học",
             "Không có sự biến đổi giữa các dạng vật chất và năng lượng",
             "Mọi đối tượng sinh học đều có cùng một tốc độ phản ứng như nhau"),
            ("VD", "Ứng dụng thực tiễn nào sau đây phù hợp với kiến thức về {subject}?",
             "Lạm dụng hóa chất cực mạnh để thay đổi hoàn toàn tự nhiên",
             "Bỏ qua các nguyên tắc an toàn khi quan sát và thực hành",
             "Ngăn chặn mọi sự tiếp xúc của sinh vật với môi trường sống"),
            ("VD", "Biện pháp nào sau đây giúp vận dụng hiệu quả hiểu biết về {subject} vào đời sống?",
             "Hạn chế tối đa việc cung cấp chất dinh dưỡng và nước",
             "Sử dụng năng lượng lãng phí không có kế hoạch kiểm soát",
             "Loại bỏ hoàn toàn các loài thực vật và vi sinh vật có ích"),
            ("VDC", "Để giải quyết vấn đề thực tiễn liên quan đến {subject}, học sinh nên đề xuất giải pháp nào?",
             "Phá vỡ cân bằng sinh thái để tăng năng suất ngắn hạn",
             "Chỉ can thiệp khi hiện tượng suy thoái đã ở mức nghiêm trọng nhất",
             "Dừng toàn bộ các hoạt động bảo vệ môi trường xung quanh"),
            ("VDC", "Trong một dự án tìm hiểu về {subject}, việc làm nào sau đây thể hiện thái độ khoa học đúng đắn?",
             "Tự ý thay đổi số liệu thực nghiệm để có kết quả như mong muốn",
             "Bỏ qua các bước kiểm chứng và kết luận vội vàng",
             "Không tuân thủ hướng dẫn an toàn trong phòng thí nghiệm")
        ]

        curr_id = len(mcqs) + 1
        fact_idx = 0
        while curr_id <= target_count:
            t_idx = (curr_id - 1) % len(templates)
            level, q_pattern, d1, d2, d3 = templates[t_idx]

            if knowledge_facts:
                fact = knowledge_facts[fact_idx % len(knowledge_facts)]
                fact_idx += 1
                clean_fact = fact[:110].strip()
            else:
                clean_fact = f"{topic} đóng vai trò quan trọng trong tự nhiên và đời sống con người"

            subject = topic if len(topic) <= 40 else topic[:40]
            q_text = q_pattern.format(subject=subject, grade=grade)

            correct_pos = (curr_id - 1) % 4
            opts = [d1, d2, d3]
            opts.insert(correct_pos, clean_fact)

            formatted_opts = [f"{labels[i]}. {opts[i]}" for i in range(4)]
            mcqs.append({
                "id": curr_id,
                "level": level,
                "question": q_text,
                "options": formatted_opts,
                "answer_key": labels[correct_pos],
                "score": q_score,
                "explanation": f"Theo SGK Khoa học tự nhiên {grade}: {clean_fact}."
            })
            curr_id += 1

    tn_score = round(sum(float(q.get("score") or q_score) for q in mcqs), 2)
    essay_score = round(max(0.0, 10.0 - tn_score), 2)

    # Build Essay Questions
    essays = []
    if essay_score >= 1.0:
        e1_score = round(essay_score * 0.5, 1)
        e2_score = round(essay_score - e1_score, 1)
        essays = [
            {
                "id": 1,
                "level": "VD",
                "question": f"Dựa trên kiến thức về {topic}, em hãy phân tích mối quan hệ giữa cấu tạo/đặc điểm và chức năng của các thành phần trong bài học. Nêu ít nhất hai ví dụ cụ thể để làm rõ.",
                "score": e1_score,
                "rubric": [
                    {"step": "- Nêu được mối quan hệ cơ bản: Cấu tạo thường phù hợp tối ưu với chức năng đảm nhiệm để duy trì sự sống.", "score": round(e1_score * 0.4, 2)},
                    {"step": "- Trình bày ví dụ 1 cụ thể (như đặc điểm hình dạng, cấu trúc phù hợp chức năng trao đổi chất/truyền dẫn...).", "score": round(e1_score * 0.3, 2)},
                    {"step": "- Trình bày ví dụ 2 cụ thể và rút ra nhận xét khoa học chính xác.", "score": round(e1_score * 0.3, 2)}
                ]
            },
            {
                "id": 2,
                "level": "VDC",
                "question": f"Vận dụng kiến thức đã học về {topic}, em hãy giải thích một hiện tượng thực tế đời sống liên quan (hoặc tình huống bảo vệ sức khỏe / môi trường sống). Từ đó đề xuất 2 biện pháp học tập, rèn luyện phù hợp cho học sinh THCS.",
                "score": e2_score,
                "rubric": [
                    {"step": "- Phân tích đúng bản chất hiện tượng thực tiễn dựa trên cơ sở khoa học đã học.", "score": round(e2_score * 0.5, 2)},
                    {"step": "- Đề xuất được 2 biện pháp cụ thể, khả thi và có ý nghĩa thực tế đối với lứa tuổi học sinh THCS.", "score": round(e2_score * 0.5, 2)}
                ]
            }
        ]

    # Build Matrix
    nb_count = sum(1 for q in mcqs if q.get("level") == "NB")
    th_count = sum(1 for q in mcqs if q.get("level") == "TH")
    vd_tn_count = sum(1 for q in mcqs if q.get("level") == "VD")
    vdc_tn_count = sum(1 for q in mcqs if q.get("level") == "VDC")
    tl_vd = 1 if len(essays) >= 1 else 0
    tl_vdc = 1 if len(essays) >= 2 else 0

    matrix_rows = [
        {
            "stt": 1,
            "topic": topic,
            "nb_tn": nb_count, "nb_tl": 0,
            "th_tn": th_count, "th_tl": 0,
            "vd_tn": vd_tn_count, "vd_tl": tl_vd,
            "vdc_tn": vdc_tn_count, "vdc_tl": tl_vdc,
            "total_tn": len(mcqs), "total_tl": len(essays),
            "total_score": 10.0
        }
    ]

    # Build Specifications
    spec_rows = [
        {
            "stt": 1,
            "topic": topic,
            "level": "Nhận biết",
            "requirement": objectives[0] if objectives else f"Nêu được các khái niệm và đặc điểm cơ bản về {topic}.",
            "question_type": f"{nb_count} TNKQ",
            "question_refs": f"Câu 1 – Câu {nb_count}" if nb_count else "-"
        },
        {
            "stt": 2,
            "topic": topic,
            "level": "Thông hiểu",
            "requirement": objectives[1] if len(objectives) > 1 else f"Giải thích được nguyên lý và cơ chế liên quan đến {topic}.",
            "question_type": f"{th_count} TNKQ",
            "question_refs": f"Câu {nb_count + 1} – Câu {nb_count + th_count}" if th_count else "-"
        },
        {
            "stt": 3,
            "topic": topic,
            "level": "Vận dụng",
            "requirement": objectives[2] if len(objectives) > 2 else f"Vận dụng kiến thức bài học để giải quyết câu hỏi tình huống và bài tập.",
            "question_type": f"{vd_tn_count} TNKQ" + (" + 1 TL" if tl_vd else ""),
            "question_refs": f"Câu {nb_count + th_count + 1} – Câu {nb_count + th_count + vd_tn_count}" + (", Câu 1 (TL)" if tl_vd else "")
        },
        {
            "stt": 4,
            "topic": topic,
            "level": "Vận dụng cao",
            "requirement": f"Vận dụng kiến thức {topic} để giải thích các vấn đề thực tiễn đời sống, sức khỏe và đề xuất giải pháp bảo vệ môi trường.",
            "question_type": (f"{vdc_tn_count} TNKQ" if vdc_tn_count else "") + (" + 1 TL" if tl_vdc else ("1 TL" if tl_vdc else "-")),
            "question_refs": f"Câu 2 (TL)" if tl_vdc else "-"
        }
    ]

    return {
        "grade": grade,
        "school_name": school_name,
        "department": department,
        "school_year": school_year,
        "semester": "HỌC KỲ I",
        "exam_type": exam_type,
        "title": f"ĐỀ KIỂM TRA {exam_type} MÔN KHOA HỌC TỰ NHIÊN {grade}",
        "topic": topic,
        "exam_code": str(lesson.get("exam_code") or "").strip(),
        "duration_minutes": duration,
        "multiple_choice": mcqs,
        "essay": essays,
        "matrix_rows": matrix_rows,
        "spec_rows": spec_rows
    }

