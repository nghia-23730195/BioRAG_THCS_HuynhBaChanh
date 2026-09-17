"""Builder for Lesson Plans adhering to Ministry of Education Dispatch 5512/BGDĐT-GDTrH.

Generates official Vietnamese standard Kế hoạch bài dạy (.docx) for Natural Sciences
(Khoa học tự nhiên - KHTN) Grades 6 to 9, adhering to:
- Công văn 5512/BGDĐT-GDTrH (Cấu trúc bài dạy 4 hoạt động chuẩn phương pháp tích cực).
- Nghị định 30/2020/NĐ-CP (Thể thức trình bày văn bản hành chính A4, lề, font Times New Roman).
- Khung năng lực số dành cho người học (Bộ GDĐT / UNESCO DigComp).
- Khung năng lực ứng dụng Trí tuệ nhân tạo (AI Literacy & Competence Framework).
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


# Color Palette
COLOR_PRIMARY = RGBColor(15, 45, 89)       # Dark Navy #0F2D59
COLOR_SECONDARY = RGBColor(33, 90, 148)    # Steel Blue #215A94
COLOR_BODY = RGBColor(0, 0, 0)             # Black #000000
COLOR_MUTED = RGBColor(80, 80, 80)         # Dark Gray #505050

HEX_HEADER_BG = "EBF2FA"                   # Soft Ice Blue
HEX_BORDER = "C5D3E8"                      # Soft Border
HEX_ALT_BG = "F8FAFC"                      # Clean Off-white


def _set_cell_background(cell, fill_hex: str) -> None:
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)


def _set_cell_margins(cell, top: int = 120, bottom: int = 120, left: int = 180, right: int = 180) -> None:
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


def _apply_run_font(run, font_name: str = "Times New Roman", size_pt: float = 13, bold: bool = False, italic: bool = False, color: Optional[RGBColor] = None) -> None:
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color
    # Ensure East Asian / complex fonts also map to Times New Roman
    rPr = run._element.get_or_add_rPr()
    rFonts = parse_xml(
        f'<w:rFonts {nsdecls("w")} w:ascii="{font_name}" w:hAnsi="{font_name}" w:cs="{font_name}"/>'
    )
    rPr.append(rFonts)


def _add_paragraph_styled(
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


def _add_sub_bullet(
    doc_or_cell,
    label: str,
    text: str,
    size_pt: float = 13,
    space_after_pt: float = 2.5,
    indent_cm: float = 0.5,
):
    p = doc_or_cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Cm(indent_cm)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after_pt)
    p.paragraph_format.line_spacing = 1.15

    r_lbl = p.add_run(label)
    _apply_run_font(r_lbl, "Times New Roman", size_pt, bold=True, italic=False, color=COLOR_BODY)

    r_txt = p.add_run(f" {text}")
    _apply_run_font(r_txt, "Times New Roman", size_pt, bold=False, italic=False, color=COLOR_BODY)
    return p


def build_lesson_plan_5512_doc(lesson: Dict[str, Any]) -> docx.Document:
    """Build a complete, beautifully structured Dispatch 5512 lesson plan document."""
    doc = docx.Document()

    # 1. Page Setup A4 & Margins (Decree 30/2020/NĐ-CP: Lề trái 2.5cm, còn lại 2.0cm)
    for section in doc.sections:
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.0)

    # Normalize Lesson Metadata
    grade = lesson.get("grade") or 6
    number = str(lesson.get("number") or f"Bài {grade}").strip()
    title = str(lesson.get("title") or "Kế hoạch bài dạy Khoa học tự nhiên").strip()
    topic = str(lesson.get("topic") or title).strip()
    duration = str(lesson.get("duration") or "2 tiết (90 phút)").strip()
    source_label = str(lesson.get("source_label") or f"SGK & SGV KHTN {grade} Kết nối tri thức").strip()

    # Normalize objectives
    raw_objectives = lesson.get("objectives") or []
    if isinstance(raw_objectives, str):
        objectives = [line.strip("- •* ") for line in raw_objectives.splitlines() if line.strip()]
    elif isinstance(raw_objectives, list):
        objectives = [str(o).strip("- •* ") for o in raw_objectives if str(o).strip()]
    else:
        objectives = []
    if not objectives:
        objectives = [
            f"Nêu được các khái niệm và kiến thức trọng tâm về {title}.",
            f"Nhận biết và mô tả được đặc điểm, cấu tạo hoặc quy luật liên quan đến {title}.",
            f"Vận dụng kiến thức bài học để giải thích một số hiện tượng thực tiễn trong đời sống.",
        ]

    # Normalize Warmup
    raw_warmup = lesson.get("warmup") or {}
    if isinstance(raw_warmup, dict):
        warmup_q = raw_warmup.get("question") or f"Quan sát thực tế xung quanh, em có nhận xét gì liên quan đến {topic}?"
        warmup_hint = raw_warmup.get("hint") or "Hãy chú ý đến các dấu hiệu nhận biết và hiện tượng thường gặp."
    else:
        warmup_q = str(raw_warmup)
        warmup_hint = "Hãy suy nghĩ dựa trên kiến thức đã học và quan sát thực tiễn."

    # Normalize Sections
    sections = lesson.get("sections") or []
    if not isinstance(sections, list) or not sections:
        content_text = str(lesson.get("content") or "")
        paragraphs = [p.strip() for p in content_text.split("\n\n") if p.strip()] or [content_text]
        sections = [
            {
                "title": f"1. Tìm hiểu kiến thức trọng tâm về {topic}",
                "paragraphs": paragraphs,
                "bullets": [],
                "example": "",
                "note": "",
            }
        ]

    # Normalize Quick Check
    quick_checks = lesson.get("quick_check") or []
    if not isinstance(quick_checks, list):
        quick_checks = []

    # -------------------------------------------------------------
    # HEADER: ADMINISTRATIVE NATIONAL HEADER
    # -------------------------------------------------------------
    header_table = doc.add_table(rows=1, cols=2)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    header_table.autofit = False

    cell_left = header_table.cell(0, 0)
    cell_right = header_table.cell(0, 1)
    cell_left.width = Cm(8.0)
    cell_right.width = Cm(8.5)
    _set_cell_margins(cell_left, 0, 0, 0, 0)
    _set_cell_margins(cell_right, 0, 0, 0, 0)

    # Left cell: School & Subject
    p_left_1 = _add_paragraph_styled(
        cell_left, "TRƯỜNG THCS TÂN TẠO",
        size_pt=11.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=1
    )
    p_left_2 = _add_paragraph_styled(
        cell_left, "TỔ: KHOA HỌC TỰ NHIÊN",
        size_pt=11.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=2
    )
    p_left_line = _add_paragraph_styled(
        cell_left, "—————————",
        size_pt=10, bold=False, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=4
    )
    p_left_author = _add_paragraph_styled(
        cell_left, "Họ và tên GV: .......................................",
        size_pt=11, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_after_pt=0
    )

    # Right cell: National Motto
    p_right_1 = _add_paragraph_styled(
        cell_right, "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM",
        size_pt=11, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=1
    )
    p_right_2 = _add_paragraph_styled(
        cell_right, "Độc lập - Tự do - Hạnh phúc",
        size_pt=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=2
    )
    p_right_line = _add_paragraph_styled(
        cell_right, "————————————",
        size_pt=10, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=0
    )

    # Spacing below header
    _add_paragraph_styled(doc, "", space_after_pt=8)

    # -------------------------------------------------------------
    # MAIN TITLE
    # -------------------------------------------------------------
    _add_paragraph_styled(
        doc, "KẾ HOẠCH BÀI DẠY",
        size_pt=16, bold=True, color=COLOR_PRIMARY,
        align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=3
    )
    _add_paragraph_styled(
        doc, f"MÔN: KHOA HỌC TỰ NHIÊN – LỚP {grade}",
        size_pt=13, bold=True, color=COLOR_SECONDARY,
        align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=3
    )
    _add_paragraph_styled(
        doc, f"{number.upper()}: {title.upper()}",
        size_pt=14, bold=True, color=COLOR_PRIMARY,
        align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=4
    )
    _add_paragraph_styled(
        doc, f"(Thời lượng thực hiện: {duration} · Nguồn: {source_label})",
        size_pt=11.5, italic=True, color=COLOR_MUTED,
        align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=14
    )

    # -------------------------------------------------------------
    # I. MỤC TIÊU
    # -------------------------------------------------------------
    _add_paragraph_styled(
        doc, "I. MỤC TIÊU",
        size_pt=13.5, bold=True, color=COLOR_PRIMARY,
        align=WD_ALIGN_PARAGRAPH.LEFT, space_before_pt=6, space_after_pt=4
    )

    # 1. Kiến thức
    _add_paragraph_styled(
        doc, "1. Về kiến thức:",
        size_pt=13, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_after_pt=3
    )
    for obj in objectives:
        _add_paragraph_styled(
            doc, f"- {obj}",
            size_pt=13, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after_pt=2.5, space_before_pt=0
        )

    # 2. Năng lực
    _add_paragraph_styled(
        doc, "2. Về năng lực:",
        size_pt=13, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before_pt=4, space_after_pt=3
    )
    _add_paragraph_styled(
        doc, "a) Năng lực chung hình thành và phát triển:",
        size_pt=13, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_after_pt=2
    )
    _add_sub_bullet(
        doc, "- Tự chủ và tự học:",
        f"Chủ động, tích cực nghiên cứu nội dung thông tin trong SGK và các học liệu; tự giác hoàn thành các nhiệm vụ học tập cá nhân về chủ đề '{topic}'."
    )
    _add_sub_bullet(
        doc, "- Giao tiếp và hợp tác:",
        "Tương tác tích cực, thảo luận hiệu quả theo nhóm; biết lắng nghe, tôn trọng và phản biện ý kiến của các thành viên để hoàn thành phiếu học tập."
    )
    _add_sub_bullet(
        doc, "- Giải quyết vấn đề và sáng tạo:",
        f"Phát hiện vấn đề và đề xuất giải pháp xử lý câu hỏi, tình huống thực tế liên quan đến kiến thức bài học."
    )

    _add_paragraph_styled(
        doc, "b) Năng lực đặc thù Khoa học tự nhiên:",
        size_pt=13, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before_pt=3, space_after_pt=2
    )
    _add_sub_bullet(
        doc, "- Nhận thức khoa học tự nhiên:",
        f"Trình bày, nêu và phân tích được các khái niệm, quy luật, cấu tạo cơ bản liên quan đến {title}."
    )
    _add_sub_bullet(
        doc, "- Tìm hiểu tự nhiên:",
        "Quan sát sơ đồ, tranh ảnh, mô hình hoặc tiến hành hoạt động khám phá để thu thập thông tin, rút ra nhận xét khoa học chính xác."
    )
    _add_sub_bullet(
        doc, "- Vận dụng kiến thức, kỹ năng đã học:",
        f"Bước đầu giải thích được một số hiện tượng tự nhiên thường gặp và vận dụng hiểu biết về {title} vào thực tiễn đời sống."
    )

    _add_paragraph_styled(
        doc, "c) Năng lực số (Digital Competence):",
        size_pt=13, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before_pt=3, space_after_pt=2
    )
    _add_sub_bullet(
        doc, "- Khai thác học liệu số và thông tin khoa học:",
        f"Biết tìm kiếm, tra cứu, thu thập và chọn lọc tư liệu, hình ảnh mô phỏng về '{topic}' từ nguồn học liệu số và SGK điện tử KNTT."
    )
    _add_sub_bullet(
        doc, "- Giao tiếp và hợp tác trên không gian số:",
        "Biết sử dụng công cụ số, chia sẻ thông tin học tập và làm việc nhóm trực tuyến để hoàn thiện các nhiệm vụ học tập."
    )
    _add_sub_bullet(
        doc, "- Sáng tạo sản phẩm số và an toàn thông tin:",
        f"Biết ứng dụng sơ đồ tư duy số, phần mềm đồ họa/trình diễn để thể hiện kiến thức bài học; có ý thức bảo vệ an toàn thông tin cá nhân trên môi trường mạng."
    )

    _add_paragraph_styled(
        doc, "d) Năng lực ứng dụng Trí tuệ nhân tạo (AI Literacy & Competence):",
        size_pt=13, bold=True, italic=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before_pt=3, space_after_pt=2
    )
    _add_sub_bullet(
        doc, "- Tương tác và khai thác trợ lý AI:",
        f"Biết sử dụng trợ lý AI chuyên môn (BioRAG KHTN) để giải thích thuật ngữ, tra cứu các quy luật khoa học về '{topic}' với câu lệnh (prompt) rõ ràng, đúng ngữ cảnh."
    )
    _add_sub_bullet(
        doc, "- Tư duy phản biện và thẩm định dữ liệu từ AI (AI Fact-Checking):",
        f"Có tư duy độc lập và phản biện khoa học; biết đối chiếu, so sánh thông tin do AI cung cấp với SGK Khoa học tự nhiên {grade} (Bộ Kết nối tri thức) để kiểm chứng độ chính xác."
    )
    _add_sub_bullet(
        doc, "- Đạo đức và văn hóa sử dụng AI có trách nhiệm (AI Ethics):",
        "Sử dụng AI với vai trò người trợ lý học tập (Learning Companion); trung thực học thuật, không sao chép nguyên văn câu trả lời mà phải có quá trình tự tư duy, tổng hợp kiến thức."
    )

    # 3. Phẩm chất
    _add_paragraph_styled(
        doc, "3. Về phẩm chất:",
        size_pt=13, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before_pt=4, space_after_pt=3
    )
    _add_sub_bullet(
        doc, "- Chăm chỉ:",
        "Luôn nỗ lực tìm tòi, kiên trì theo dõi bài giảng, tích cực đọc sách và hoàn thành các nhiệm vụ được giao."
    )
    _add_sub_bullet(
        doc, "- Trung thực:",
        "Khách quan, trung thực trong việc quan sát số liệu, ghi chép kết quả thảo luận và báo cáo sản phẩm nhóm."
    )
    _add_sub_bullet(
        doc, "- Trách nhiệm:",
        "Có ý thức bảo vệ tài sản lớp học, giữ gìn vệ sinh chung; có trách nhiệm với kết quả học tập của cá nhân và tập thể."
    )

    # -------------------------------------------------------------
    # II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU SỐ
    # -------------------------------------------------------------
    _add_paragraph_styled(
        doc, "II. THIẾT BỊ DẠY HỌC VÀ HỌC LIỆU SỐ",
        size_pt=13.5, bold=True, color=COLOR_PRIMARY,
        align=WD_ALIGN_PARAGRAPH.LEFT, space_before_pt=8, space_after_pt=4
    )
    _add_paragraph_styled(
        doc, "1. Đối với giáo viên:",
        size_pt=13, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_after_pt=2.5
    )
    _add_paragraph_styled(
        doc, f"- Giáo án chuẩn Công văn 5512 (Tích hợp Khung năng lực số & AI); Sách giáo khoa, Sách giáo viên Khoa học tự nhiên {grade} (Bộ Kết nối tri thức với cuộc sống).",
        size_pt=13, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after_pt=2
    )
    _add_paragraph_styled(
        doc, f"- Bài giảng điện tử đa phương tiện (PowerPoint / Canva / Video tương tác) minh họa nội dung bài học {number}.",
        size_pt=13, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after_pt=2
    )
    _add_paragraph_styled(
        doc, "- Nền tảng Trợ lý AI giáo dục BioRAG KHTN (hỗ trợ truy xuất dữ liệu chuẩn SGK Kết nối tri thức và thị giác máy tính nhận diện sơ đồ/hình ảnh).",
        size_pt=13, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after_pt=2
    )
    _add_paragraph_styled(
        doc, "- Máy vi tính, máy chiếu hoặc màn hình tivi tương tác thông minh có kết nối Internet.",
        size_pt=13, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after_pt=2
    )
    diagram_info = lesson.get("diagram")
    if isinstance(diagram_info, dict) and diagram_info.get("title"):
        _add_paragraph_styled(
            doc, f"- Sơ đồ trực quan số: '{diagram_info.get('title')}' trình chiếu hoặc in khổ lớn.",
            size_pt=13, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after_pt=2
        )
    _add_paragraph_styled(
        doc, "- Hệ thống Phiếu học tập số 1 (Hoạt động nhóm hình thành kiến thức & phản biện AI) và Phiếu học tập số 2 (Luyện tập củng cố).",
        size_pt=13, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after_pt=2
    )

    _add_paragraph_styled(
        doc, "2. Đối với học sinh:",
        size_pt=13, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT, space_before_pt=3, space_after_pt=2.5
    )
    _add_paragraph_styled(
        doc, f"- Sách giáo khoa KHTN {grade} (Kết nối tri thức), vở ghi bài, vở bài tập, bút viết, thước kẻ.",
        size_pt=13, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after_pt=2
    )
    _add_paragraph_styled(
        doc, "- Thiết bị số (máy tính phòng thực hành / điện thoại thông minh / máy tính bảng - nếu được phép sử dụng) để tra cứu học liệu số và tương tác với trợ lý AI BioRAG.",
        size_pt=13, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after_pt=2
    )
    _add_paragraph_styled(
        doc, f"- Đọc trước nội dung bài '{title}' ở nhà; có thể tra cứu nhanh các câu hỏi tò mò ban đầu bằng trợ lý AI.",
        size_pt=13, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_after_pt=4
    )

    # -------------------------------------------------------------
    # III. TIẾN TRÌNH DẠY HỌC
    # -------------------------------------------------------------
    _add_paragraph_styled(
        doc, "III. TIẾN TRÌNH DẠY HỌC",
        size_pt=13.5, bold=True, color=COLOR_PRIMARY,
        align=WD_ALIGN_PARAGRAPH.LEFT, space_before_pt=8, space_after_pt=4
    )

    # 1. Khung ma trận phân phối các hoạt động (Bảng tổng quan tiến trình 5512)
    matrix_table = doc.add_table(rows=1, cols=4)
    matrix_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    matrix_table.autofit = False
    _set_table_borders(matrix_table)

    col_widths = [Cm(5.0), Cm(4.5), Cm(3.5), Cm(3.5)]
    headers = [
        "Hoạt động học\n(Thời gian)",
        "Mục tiêu trọng tâm",
        "Phương pháp / Kỹ thuật dạy học",
        "Phương án đánh giá",
    ]
    hdr_cells = matrix_table.rows[0].cells
    for i, (text, w) in enumerate(zip(headers, col_widths)):
        hdr_cells[i].width = w
        _set_cell_background(hdr_cells[i], HEX_HEADER_BG)
        _set_cell_margins(hdr_cells[i], 120, 120, 150, 150)
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(text)
        _apply_run_font(run, size_pt=11.5, bold=True, color=COLOR_PRIMARY)

    matrix_data = [
        (
            "Hoạt động 1: Mở đầu\n(Khởi động: 5–7 phút)",
            f"Kích hoạt tư duy, tạo hứng thú vào bài học về {title}.",
            "Đặt và giải quyết vấn đề, gợi mở vấn đáp kết hợp hình ảnh/tình huống số do AI gợi ý.",
            "Đánh giá qua câu trả lời, sự chủ động và phản ứng của học sinh.",
        ),
        (
            f"Hoạt động 2: Hình thành kiến thức mới ({len(sections)} mục: 25–30 phút)",
            "Tiếp thu kiến thức mới, giải thích cấu tạo, quy luật trọng tâm; rèn tư duy phản biện AI.",
            "Dạy học hợp tác (nhóm), trực quan quan sát, tra cứu học liệu số & hỗ trợ bởi trợ lý AI BioRAG.",
            "Đánh giá kết quả trên Phiếu học tập số 1, năng lực thẩm định AI & báo cáo nhóm.",
        ),
        (
            "Hoạt động 3: Luyện tập\n(Củng cố: 8–10 phút)",
            "Khắc sâu kiến thức, rèn kỹ năng nhận biết, thông hiểu và phản xạ số.",
            "Trò chơi học tập số, trắc nghiệm tương tác, phản hồi kết quả tức thì.",
            "Đánh giá qua kết quả Phiếu học tập số 2 / bảng tương tác.",
        ),
        (
            "Hoạt động 4: Vận dụng\n(Mở rộng: 3–5 phút)",
            "Vận dụng kiến thức bài học vào thực tế đời sống; phát triển kỹ năng sáng tạo số.",
            "Dạy học giải quyết vấn đề, ứng dụng công cụ số tạo sản phẩm học tập tại nhà.",
            "Đánh giá qua sản phẩm thu hoạch thực tế / sản phẩm số ở tiết sau.",
        ),
    ]

    for row_idx, row_data in enumerate(matrix_data):
        row = matrix_table.add_row()
        _set_table_row_cant_split(row)
        bg = HEX_ALT_BG if row_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = col_widths[c_idx]
            _set_cell_background(cell, bg)
            _set_cell_margins(cell, 100, 100, 120, 120)
            align = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.JUSTIFY
            p = cell.paragraphs[0]
            p.alignment = align
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(val)
            _apply_run_font(run, size_pt=11, bold=(c_idx == 0))

    _add_paragraph_styled(doc, "", space_after_pt=6)

    # -------------------------------------------------------------
    # CHI TIẾT CÁC HOẠT ĐỘNG DẠY HỌC (CHUẨN 4 BƯỚC CÔNG VĂN 5512)
    # -------------------------------------------------------------

    def _render_activity_table(gv_content: List[str], hs_content: List[str]) -> None:
        """Render standard 2-column Dispatch 5512 activity execution table."""
        tbl = doc.add_table(rows=1, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False
        _set_table_borders(tbl)

        c_gv = tbl.cell(0, 0)
        c_hs = tbl.cell(0, 1)
        c_gv.width = Cm(8.25)
        c_hs.width = Cm(8.25)

        _set_cell_background(c_gv, HEX_HEADER_BG)
        _set_cell_background(c_hs, HEX_HEADER_BG)
        _set_cell_margins(c_gv, 100, 100, 120, 120)
        _set_cell_margins(c_hs, 100, 100, 120, 120)

        p_gv_hdr = c_gv.paragraphs[0]
        p_gv_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_gv_hdr.paragraph_format.space_after = Pt(2)
        run_gv = p_gv_hdr.add_run("HOẠT ĐỘNG CỦA GIÁO VIÊN")
        _apply_run_font(run_gv, size_pt=11.5, bold=True, color=COLOR_PRIMARY)

        p_hs_hdr = c_hs.paragraphs[0]
        p_hs_hdr.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_hs_hdr.paragraph_format.space_after = Pt(2)
        run_hs = p_hs_hdr.add_run("HOẠT ĐỘNG CỦA HỌC SINH")
        _apply_run_font(run_hs, size_pt=11.5, bold=True, color=COLOR_PRIMARY)

        # Body row
        row = tbl.add_row()
        _set_table_row_cant_split(row)
        c_gv_body = row.cells[0]
        c_hs_body = row.cells[1]
        c_gv_body.width = Cm(8.25)
        c_hs_body.width = Cm(8.25)
        _set_cell_margins(c_gv_body, 120, 120, 140, 140)
        _set_cell_margins(c_hs_body, 120, 120, 140, 140)

        # Populate GV steps
        for idx, item in enumerate(gv_content):
            p = c_gv_body.paragraphs[0] if idx == 0 else c_gv_body.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(3)
            # Detect step headers
            if item.startswith("**") and item.endswith("**"):
                clean = item.strip("*")
                run = p.add_run(clean)
                _apply_run_font(run, size_pt=11.5, bold=True, color=COLOR_SECONDARY)
            elif ":" in item and (item.startswith("Bước ") or item.startswith("*Bước ")):
                parts = item.split(":", 1)
                run_hdr = p.add_run(parts[0] + ":")
                _apply_run_font(run_hdr, size_pt=11.5, bold=True, color=COLOR_SECONDARY)
                run_bdy = p.add_run(parts[1])
                _apply_run_font(run_bdy, size_pt=11.5, bold=False, color=COLOR_BODY)
            else:
                run = p.add_run(item)
                _apply_run_font(run, size_pt=11.5, bold=False, color=COLOR_BODY)

        # Populate HS steps
        for idx, item in enumerate(hs_content):
            p = c_hs_body.paragraphs[0] if idx == 0 else c_hs_body.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(3)
            if item.startswith("**") and item.endswith("**"):
                clean = item.strip("*")
                run = p.add_run(clean)
                _apply_run_font(run, size_pt=11.5, bold=True, color=COLOR_SECONDARY)
            elif ":" in item and (item.startswith("Bước ") or item.startswith("*Bước ")):
                parts = item.split(":", 1)
                run_hdr = p.add_run(parts[0] + ":")
                _apply_run_font(run_hdr, size_pt=11.5, bold=True, color=COLOR_SECONDARY)
                run_bdy = p.add_run(parts[1])
                _apply_run_font(run_bdy, size_pt=11.5, bold=False, color=COLOR_BODY)
            else:
                run = p.add_run(item)
                _apply_run_font(run, size_pt=11.5, bold=False, color=COLOR_BODY)

        _add_paragraph_styled(doc, "", space_after_pt=6)

    # -------------------------------------------------------------
    # 1. HOẠT ĐỘNG 1: MỞ ĐẦU / KHỞI ĐỘNG
    # -------------------------------------------------------------
    _add_paragraph_styled(
        doc, "1. Hoạt động 1: Mở đầu / Khởi động (Khoảng 5–7 phút)",
        size_pt=13, bold=True, color=COLOR_SECONDARY, space_before_pt=4, space_after_pt=3
    )
    _add_paragraph_styled(
        doc, f"a) Mục tiêu: Kích thích sự tò mò, khám phá và dẫn dắt học sinh bước vào bài học '{title}'.",
        size_pt=12.5, italic=False, space_after_pt=2
    )
    _add_paragraph_styled(
        doc, f"b) Nội dung: GV đưa ra câu hỏi/tình huống kích thích tư duy: \"{warmup_q}\". HS suy nghĩ và trao đổi nhanh.",
        size_pt=12.5, italic=False, space_after_pt=2
    )
    _add_paragraph_styled(
        doc, "c) Sản phẩm: Câu trả lời, ý kiến phán đoán ban đầu của học sinh ghi ra giấy nháp hoặc phát biểu trực tiếp.",
        size_pt=12.5, italic=False, space_after_pt=2
    )
    _add_paragraph_styled(
        doc, "d) Tổ chức thực hiện:",
        size_pt=12.5, bold=True, space_after_pt=3
    )

    gv_h1 = [
        "Bước 1: Chuyển giao nhiệm vụ học tập:",
        f"- GV chiếu câu hỏi / hình ảnh tình huống: \"{warmup_q}\"",
        "- Yêu cầu HS suy nghĩ độc lập trong 2 phút, sau đó thảo luận nhanh với bạn cùng bàn trong 1 phút.",
        "Bước 4: Kết luận, nhận định và dẫn dắt vào bài:",
        "- GV lắng nghe, ghi nhận ý kiến và khen ngợi tinh thần phát biểu của học sinh.",
        f"- GV chưa vội chốt đúng sai ngay mà dẫn dắt khéo léo: \"{warmup_hint} Để hiểu rõ và giải thích chính xác điều này, chúng ta cùng tìm hiểu bài học hôm nay: {title}.\"",
    ]
    hs_h1 = [
        "Bước 2: Thực hiện nhiệm vụ học tập:",
        "- Học sinh chú ý quan sát câu hỏi tình huống trên máy chiếu.",
        "- Cá nhân suy nghĩ độc lập, huy động kiến thức đã biết và trao đổi nhanh với bạn bên cạnh.",
        "Bước 3: Báo cáo kết quả và thảo luận:",
        "- Đại diện 2–3 học sinh xung phong đứng dậy phát biểu ý kiến trả lời.",
        "- Các học sinh khác lắng nghe, nhận xét, bổ sung các suy nghĩ khác biệt.",
    ]
    _render_activity_table(gv_h1, hs_h1)

    # -------------------------------------------------------------
    # 2. HOẠT ĐỘNG 2: HÌNH THÀNH KIẾN THỨC MỚI
    # -------------------------------------------------------------
    _add_paragraph_styled(
        doc, "2. Hoạt động 2: Hình thành kiến thức mới (Khoảng 25–30 phút)",
        size_pt=13, bold=True, color=COLOR_SECONDARY, space_before_pt=6, space_after_pt=3
    )

    for s_idx, sec in enumerate(sections, start=1):
        sec_title = str(sec.get("title") or f"Mục {s_idx}").strip()
        sec_paragraphs = sec.get("paragraphs") or []
        if isinstance(sec_paragraphs, str):
            sec_paragraphs = [sec_paragraphs]
        sec_bullets = sec.get("bullets") or []
        sec_example = str(sec.get("example") or "").strip()
        sec_note = str(sec.get("note") or "").strip()

        _add_paragraph_styled(
            doc, f"2.{s_idx}. Hoạt động 2.{s_idx}: {sec_title}",
            size_pt=12.5, bold=True, color=COLOR_PRIMARY, space_before_pt=3, space_after_pt=2
        )
        _add_paragraph_styled(
            doc, f"a) Mục tiêu: Giúp học sinh tìm hiểu, tiếp thu và làm rõ nội dung kiến thức về {sec_title}.",
            size_pt=12.5, space_after_pt=2
        )
        _add_paragraph_styled(
            doc, f"b) Nội dung: HS làm việc nhóm, đọc thông tin trong SGK và quan sát hình ảnh để trả lời câu hỏi và hoàn thành Phiếu học tập số 1 (Nhiệm vụ {s_idx}).",
            size_pt=12.5, space_after_pt=2
        )
        _add_paragraph_styled(
            doc, "c) Sản phẩm: Báo cáo kết quả trên Phiếu học tập số 1 của các nhóm; nội dung kiến thức trọng tâm học sinh ghi nhận vào vở.",
            size_pt=12.5, space_after_pt=2
        )
        _add_paragraph_styled(
            doc, "d) Tổ chức thực hiện:",
            size_pt=12.5, bold=True, space_after_pt=3
        )

        gv_h2 = [
            "Bước 1: Chuyển giao nhiệm vụ học tập:",
            f"- GV yêu cầu học sinh đọc kỹ nội dung mục '{sec_title}' trong SGK.",
            f"- Chia lớp thành các nhóm (4–6 HS/nhóm) và giao nhiệm vụ hoàn thành Phiếu học tập số 1:",
        ]
        # Add questions / focus points
        for p_item in sec_paragraphs[:2]:
            gv_h2.append(f"  + Tìm hiểu: {p_item[:140]}...")
        if sec_bullets:
            gv_h2.append(f"  + Chỉ ra các đặc điểm/thành phần tiêu biểu: {', '.join(b.split(' ', 2)[-1][:50] for b in sec_bullets[:3])}.")

        gv_h2.extend([
            "- Tích hợp Năng lực số & AI: Hướng dẫn học sinh sử dụng Trợ lý BioRAG KHTN tra cứu nhanh định nghĩa thuật ngữ, quan sát hình ảnh minh họa số.",
            "- Rèn luyện tư duy phản biện AI (Fact-Checking): Yêu cầu HS đối chiếu câu trả lời của AI với SGK Kết nối tri thức, phát hiện điểm cần bổ sung hoặc đính chính.",
            "- Thời gian thảo luận nhóm: 7–10 phút.",
            "Bước 4: Đánh giá kết quả và kết luận chuẩn hóa kiến thức:",
            "- GV nhận xét tinh thần làm việc, tính chính xác và kỹ năng thẩm định thông tin AI của các nhóm.",
            "- GV chuẩn hóa kiến thức, giảng giải bổ sung và yêu cầu HS ghi nhớ nội dung cốt lõi:",
        ])
        for p_item in sec_paragraphs:
            gv_h2.append(f"  * {p_item}")
        for b_item in sec_bullets:
            gv_h2.append(f"  * {b_item}")
        if sec_example:
            gv_h2.append(f"  * Ví dụ thực tế: {sec_example}")
        if sec_note:
            gv_h2.append(f"  * Lưu ý quan trọng: {sec_note}")

        hs_h2 = [
            "Bước 2: Thực hiện nhiệm vụ học tập:",
            "- Các thành viên trong nhóm mở SGK, đọc thông tin cá nhân trong 2 phút.",
            "- Nhóm trưởng điều hành thảo luận; thành viên phụ trách công nghệ tra cứu đối chiếu trên Trợ lý BioRAG KHTN.",
            "- Cả nhóm phân tích, phản biện thông tin AI bằng dữ liệu SGK; thư ký ghi chép câu trả lời chuẩn xác vào Phiếu học tập số 1.",
            "- GV theo dõi, hỗ trợ các nhóm gặp khó khăn hoặc định hướng câu hỏi.",
            "Bước 3: Báo cáo kết quả và thảo luận:",
            "- Đại diện 1 nhóm lên bảng trình bày sản phẩm thảo luận (kèm nhận xét về dữ liệu đối chiếu AI).",
            "- Các nhóm khác chú ý theo dõi, lắng nghe, nhận xét đối chiếu và phản biện bổ sung.",
            "- Học sinh hoàn thiện nội dung chuẩn xác vào vở ghi bài cá nhân.",
        ]
        _render_activity_table(gv_h2, hs_h2)

    # -------------------------------------------------------------
    # 3. HOẠT ĐỘNG 3: LUYỆN TẬP
    # -------------------------------------------------------------
    _add_paragraph_styled(
        doc, "3. Hoạt động 3: Luyện tập (Khoảng 8–10 phút)",
        size_pt=13, bold=True, color=COLOR_SECONDARY, space_before_pt=6, space_after_pt=3
    )
    _add_paragraph_styled(
        doc, f"a) Mục tiêu: Củng cố, khắc sâu toàn bộ kiến thức vừa học về '{title}'; rèn luyện khả năng tư duy và phản xạ qua các câu hỏi trắc nghiệm.",
        size_pt=12.5, space_after_pt=2
    )
    _add_paragraph_styled(
        doc, "b) Nội dung: Học sinh hoàn thành các câu hỏi trong Phiếu học tập số 2 (hoặc tham gia trò chơi trắc nghiệm nhanh trên màn chiếu).",
        size_pt=12.5, space_after_pt=2
    )
    _add_paragraph_styled(
        doc, "c) Sản phẩm: Đáp án chọn lựa và giải thích ngắn của học sinh cho hệ thống câu hỏi kiểm tra nhanh.",
        size_pt=12.5, space_after_pt=2
    )
    _add_paragraph_styled(
        doc, "d) Tổ chức thực hiện:",
        size_pt=12.5, bold=True, space_after_pt=3
    )

    gv_h3 = [
        "Bước 1: Chuyển giao nhiệm vụ học tập:",
        "- GV phát Phiếu học tập số 2 hoặc chiếu các câu hỏi củng cố lên màn hình:",
    ]
    if quick_checks:
        for q_idx, qc in enumerate(quick_checks, start=1):
            q_txt = qc.get("question") or f"Câu hỏi {q_idx}"
            gv_h3.append(f"  Câu {q_idx}: {q_txt}")
            options = qc.get("options") or []
            labels = ["A", "B", "C", "D"]
            opt_strs = [f"{labels[oidx]}. {opt}" for oidx, opt in enumerate(options[:4])]
            gv_h3.append(f"    {' | '.join(opt_strs)}")
    else:
        gv_h3.append("  - Hoàn thành các bài tập trắc nghiệm và tự luận củng cố cuối bài trong SGK.")

    gv_h3.extend([
        "- Thời gian làm bài cá nhân: 3–5 phút.",
        "Bước 4: Đánh giá, kết luận:",
        "- GV công bố đáp án chuẩn và phân tích ngắn gọn lý do vì sao đáp án đúng:",
    ])
    if quick_checks:
        labels = ["A", "B", "C", "D"]
        for q_idx, qc in enumerate(quick_checks, start=1):
            ans_idx = int(qc.get("answer_index", 0))
            ans_label = labels[ans_idx] if 0 <= ans_idx < len(labels) else "A"
            explanation = qc.get("explanation") or ""
            gv_h3.append(f"  * Đáp án Câu {q_idx}: {ans_label} ({explanation})")
    gv_h3.append("- GV biểu dương các cá nhân có câu trả lời nhanh và chính xác nhất.")

    hs_h3 = [
        "Bước 2: Thực hiện nhiệm vụ học tập:",
        "- Từng học sinh làm việc độc lập, đọc kỹ từng câu hỏi, suy luận và chọn phương án đúng.",
        "- Ghi chép đáp án vào bảng con hoặc Phiếu học tập số 2.",
        "Bước 3: Báo cáo kết quả và thảo luận:",
        "- Khi có hiệu lệnh của GV, HS giơ bảng đáp án hoặc xung phong đứng dậy trả lời.",
        "- Giải thích ngắn gọn lý do tại sao lựa chọn phương án đó.",
        "- Lắng nghe nhận xét chuẩn hóa của giáo viên.",
    ]
    _render_activity_table(gv_h3, hs_h3)

    # -------------------------------------------------------------
    # 4. HOẠT ĐỘNG 4: VẬN DỤNG
    # -------------------------------------------------------------
    _add_paragraph_styled(
        doc, "4. Hoạt động 4: Vận dụng (Khoảng 3–5 phút trên lớp + thực hiện ở nhà)",
        size_pt=13, bold=True, color=COLOR_SECONDARY, space_before_pt=6, space_after_pt=3
    )
    _add_paragraph_styled(
        doc, f"a) Mục tiêu: Vận dụng những kiến thức đã học về '{title}' để giải thích hiện tượng thực tế đời sống; phát triển năng lực tự học và nghiên cứu khoa học.",
        size_pt=12.5, space_after_pt=2
    )
    _add_paragraph_styled(
        doc, f"b) Nội dung: Giao bài tập tình huống thực tiễn mở rộng liên quan đến {topic}.",
        size_pt=12.5, space_after_pt=2
    )
    _add_paragraph_styled(
        doc, "c) Sản phẩm: Báo cáo thu hoạch ngắn gọn (bằng bài viết vào vở hoặc tranh vẽ/ảnh chụp minh chứng) nộp vào đầu tiết sau.",
        size_pt=12.5, space_after_pt=2
    )
    _add_paragraph_styled(
        doc, "d) Tổ chức thực hiện:",
        size_pt=12.5, bold=True, space_after_pt=3
    )

    gv_h4 = [
        "Bước 1: Chuyển giao nhiệm vụ học tập:",
        "- GV nêu nhiệm vụ học tập về nhà (khuyến khích xây dựng sản phẩm học tập số hóa):",
        f"  \"Hãy tìm hiểu trong gia đình, nhà trường hoặc địa phương em những hiện tượng, ứng dụng thực tế liên quan đến '{title}'. Viết một đoạn văn ngắn hoặc thiết kế sơ đồ tư duy số / infographic giải thích hiện tượng đó dựa trên kiến thức khoa học đã học hôm nay. HS có thể tham khảo thêm ý tưởng từ Trợ lý AI BioRAG nhưng cần tự tổng hợp bằng ngôn ngữ của bản thân.\"",
        "Bước 4: Hướng dẫn tự học ở nhà:",
        "- Dặn dò HS hoàn thành bài tập vận dụng vào vở hoặc nộp sản phẩm số qua nhóm học tập trực tuyến.",
        "- Ôn lại kiến thức trọng tâm và đọc trước bài học tiếp theo trong SGK.",
    ]
    hs_h4 = [
        "Bước 2, 3: Thực hiện nhiệm vụ tại nhà và báo cáo ở tiết sau:",
        "- HS lắng nghe, ghi chép nội dung nhiệm vụ vận dụng vào vở cẩn thận.",
        "- Về nhà quan sát thực tế, trao đổi với người thân hoặc tra cứu thêm tư liệu số / trợ lý AI để mở rộng hiểu biết.",
        "- Hoàn thiện bài thu hoạch (hoặc sản phẩm số) và nộp cho GV vào đầu tiết học tiếp theo.",
    ]
    _render_activity_table(gv_h4, hs_h4)

    # -------------------------------------------------------------
    # IV. PHỤ LỤC: HỆ THỐNG PHIẾU HỌC TẬP
    # -------------------------------------------------------------
    _add_paragraph_styled(
        doc, "IV. PHỤ LỤC: HỆ THỐNG PHIẾU HỌC TẬP",
        size_pt=13.5, bold=True, color=COLOR_PRIMARY, space_before_pt=8, space_after_pt=4
    )

    # Phiếu học tập số 1
    pht1_tbl = doc.add_table(rows=1, cols=1)
    pht1_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    pht1_tbl.autofit = False
    _set_table_borders(pht1_tbl, color="A0A0A0", sz="6")
    pht1_cell = pht1_tbl.cell(0, 0)
    pht1_cell.width = Cm(16.5)
    _set_cell_background(pht1_cell, "FAFCFF")
    _set_cell_margins(pht1_cell, 150, 150, 180, 180)

    _add_paragraph_styled(
        pht1_cell, "PHIẾU HỌC TẬP SỐ 1: THẢO LUẬN NHÓM KHÁM PHÁ KIẾN THỨC",
        size_pt=12.5, bold=True, color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=2
    )
    _add_paragraph_styled(
        pht1_cell, f"Bài học: {number} – {title}",
        size_pt=11.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=3
    )
    _add_paragraph_styled(
        pht1_cell, "Nhóm số: ...................   Lớp: ...................   Các thành viên: .........................................................................",
        size_pt=11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=6
    )

    for s_idx, sec in enumerate(sections, start=1):
        _add_paragraph_styled(
            pht1_cell, f"Nhiệm vụ {s_idx}: Tìm hiểu về {sec.get('title')}",
            size_pt=11.5, bold=True, color=COLOR_SECONDARY, space_after_pt=2
        )
        p_bullets = sec.get("bullets") or []
        if p_bullets:
            for b in p_bullets[:3]:
                _add_paragraph_styled(
                    pht1_cell, f"  - {b}",
                    size_pt=11, space_after_pt=1.5
                )
        else:
            _add_paragraph_styled(
                pht1_cell, "  - Đọc thông tin SGK, nêu các đặc điểm và nội dung trọng tâm:",
                size_pt=11, space_after_pt=1.5
            )
        _add_paragraph_styled(
            pht1_cell, "  Trả lời: ..................................................................................................................................................",
            size_pt=11, italic=True, color=COLOR_MUTED, space_after_pt=1.5
        )
        _add_paragraph_styled(
            pht1_cell, "  ................................................................................................................................................................",
            size_pt=11, italic=True, color=COLOR_MUTED, space_after_pt=3
        )

    # Góc tư duy số và phản biện AI
    _add_paragraph_styled(
        pht1_cell, "★ GÓC TƯ DUY SỐ & PHẢN BIỆN AI (Dành cho nhóm ứng dụng Trợ lý BioRAG / Học liệu số):",
        size_pt=11, bold=True, color=COLOR_PRIMARY, space_before_pt=3, space_after_pt=1.5
    )
    _add_paragraph_styled(
        pht1_cell, "  - Câu lệnh / Từ khóa nhóm đã hỏi Trợ lý AI: .............................................................................................................",
        size_pt=10.5, italic=True, color=COLOR_MUTED, space_after_pt=1.5
    )
    _add_paragraph_styled(
        pht1_cell, "  - Đối chiếu với SGK Kết nối tri thức (Đúng chuẩn / Cần bổ sung / Khác biệt): .....................................................",
        size_pt=10.5, italic=True, color=COLOR_MUTED, space_after_pt=4
    )

    _add_paragraph_styled(doc, "", space_after_pt=6)

    # Phiếu học tập số 2 (Trắc nghiệm củng cố)
    if quick_checks:
        pht2_tbl = doc.add_table(rows=1, cols=1)
        pht2_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        pht2_tbl.autofit = False
        _set_table_borders(pht2_tbl, color="A0A0A0", sz="6")
        pht2_cell = pht2_tbl.cell(0, 0)
        pht2_cell.width = Cm(16.5)
        _set_cell_background(pht2_cell, "FCFBF7")
        _set_cell_margins(pht2_cell, 150, 150, 180, 180)

        _add_paragraph_styled(
            pht2_cell, "PHIẾU HỌC TẬP SỐ 2: BÀI TẬP TRẮC NGHIỆM CỦNG CỐ",
            size_pt=12.5, bold=True, color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=2
        )
        _add_paragraph_styled(
            pht2_cell, "Họ và tên học sinh: .....................................................................   Lớp: ...................",
            size_pt=11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=6
        )

        labels = ["A", "B", "C", "D"]
        for q_idx, qc in enumerate(quick_checks, start=1):
            q_txt = qc.get("question") or f"Câu hỏi {q_idx}"
            _add_paragraph_styled(
                pht2_cell, f"Câu {q_idx}: {q_txt}",
                size_pt=11.5, bold=True, space_after_pt=2
            )
            options = qc.get("options") or []
            opt_strs = [f"{labels[oidx]}. {opt}" for oidx, opt in enumerate(options[:4])]
            _add_paragraph_styled(
                pht2_cell, f"   {'        '.join(opt_strs)}",
                size_pt=11, space_after_pt=3
            )

        _add_paragraph_styled(
            pht2_cell, "BẢNG ĐIỀN ĐÁP ÁN:",
            size_pt=11, bold=True, space_before_pt=3, space_after_pt=2
        )
        ans_box_str = "    ".join([f"Câu {i}: [   ]" for i in range(1, len(quick_checks) + 1)])
        _add_paragraph_styled(
            pht2_cell, f"   {ans_box_str}",
            size_pt=11, bold=True, space_after_pt=2
        )

        _add_paragraph_styled(doc, "", space_after_pt=10)

    # -------------------------------------------------------------
    # V. KHUNG TIÊU CHÍ ĐÁNH GIÁ NĂNG LỰC SỐ VÀ AI (RUBRIC ĐÁNH GIÁ)
    # -------------------------------------------------------------
    _add_paragraph_styled(
        doc, "V. KHUNG TIÊU CHÍ ĐÁNH GIÁ NĂNG LỰC SỐ VÀ AI CỦA HỌC SINH (RUBRIC ĐÁNH GIÁ)",
        size_pt=13.5, bold=True, color=COLOR_PRIMARY, space_before_pt=8, space_after_pt=3
    )
    _add_paragraph_styled(
        doc, "Bảng tiêu chí theo dõi và đánh giá mức độ hình thành năng lực số, kỹ năng ứng dụng AI có trách nhiệm của học sinh trong giờ học Khoa học tự nhiên:",
        size_pt=12, italic=True, space_after_pt=5
    )

    rubric_tbl = doc.add_table(rows=1, cols=4)
    rubric_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    rubric_tbl.autofit = False
    _set_table_borders(rubric_tbl)

    r_col_widths = [Cm(4.0), Cm(4.0), Cm(4.2), Cm(4.3)]
    r_headers = [
        "Tiêu chí năng lực\n(Trọng số)",
        "Mức 1: Cần cố gắng\n(Dưới 5.0 điểm)",
        "Mức 2: Đạt chuẩn\n(5.0 – 7.9 điểm)",
        "Mức 3: Tốt / Xuất sắc\n(8.0 – 10.0 điểm)"
    ]
    for i, (text, w) in enumerate(zip(r_headers, r_col_widths)):
        cell = rubric_tbl.rows[0].cells[i]
        cell.width = w
        _set_cell_background(cell, HEX_HEADER_BG)
        _set_cell_margins(cell, 120, 120, 140, 140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(2)
        run = p.add_run(text)
        _apply_run_font(run, size_pt=10.5, bold=True, color=COLOR_PRIMARY)

    rubric_rows_data = [
        (
            "1. Khai thác học liệu số & dữ liệu khoa học\n(25%)",
            "Cần sự hướng dẫn trực tiếp từ GV hoặc bạn mới tìm được thông tin trên SGK điện tử / học liệu số.",
            "Tự tìm kiếm và sử dụng được tài liệu, hình ảnh minh họa về bài học trên môi trường số.",
            "Tìm kiếm nhanh, độc lập; biết chọn lọc nguồn dữ liệu chính xác, khoa học và chia sẻ hiệu quả cho nhóm."
        ),
        (
            "2. Kỹ năng tương tác và ra lệnh cho AI (Prompting)\n(25%)",
            "Câu hỏi gửi AI còn rời rạc, mơ hồ, chưa nêu rõ bối cảnh câu hỏi môn KHTN.",
            "Đặt được câu hỏi rõ ràng, có ngữ cảnh nội dung bài học để AI phản hồi đúng trọng tâm.",
            "Đặt câu hỏi thông minh, logic, có đào sâu (follow-up); biết yêu cầu AI giải thích ngắn gọn, phân tích hoặc lấy ví dụ thực tiễn."
        ),
        (
            "3. Tư duy phản biện & xác thực dữ liệu AI (Fact-Checking)\n(30%)",
            "Tin tưởng tuyệt đối vào câu trả lời của AI; sao chép nguyên văn vào phiếu học tập mà không kiểm chứng.",
            "Biết đối chiếu thông tin AI với nội dung trong SGK Kết nối tri thức; nhận ra các điểm cần chỉnh sửa.",
            "Phát hiện nhạy bén điểm thiếu sót hoặc thuật ngữ chưa chuẩn của AI; tự tin dùng dẫn chứng SGK để phản biện và bảo vệ ý kiến."
        ),
        (
            "4. Đạo đức và văn hóa sử dụng công nghệ số\n(20%)",
            "Còn phụ thuộc, ỷ lại vào công nghệ; chưa có ý thức tự giác tư duy.",
            "Xem AI là công cụ hỗ trợ tư duy; trung thực ghi nhận nguồn và tự diễn đạt lại theo cách hiểu của bản thân.",
            "Sử dụng công nghệ văn minh, tôn trọng bản quyền; tích cực giúp đỡ các bạn cùng nhóm nâng cao kỹ năng số an toàn."
        )
    ]

    for row_idx, r_data in enumerate(rubric_rows_data):
        row = rubric_tbl.add_row()
        _set_table_row_cant_split(row)
        bg = HEX_ALT_BG if row_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(r_data):
            cell = row.cells[c_idx]
            cell.width = r_col_widths[c_idx]
            _set_cell_background(cell, bg)
            _set_cell_margins(cell, 100, 100, 120, 120)
            align = WD_ALIGN_PARAGRAPH.CENTER if c_idx == 0 else WD_ALIGN_PARAGRAPH.JUSTIFY
            p = cell.paragraphs[0]
            p.alignment = align
            p.paragraph_format.line_spacing = 1.15
            p.paragraph_format.space_after = Pt(1)
            run = p.add_run(val)
            _apply_run_font(run, size_pt=10, bold=(c_idx == 0))

    _add_paragraph_styled(doc, "", space_after_pt=10)

    # -------------------------------------------------------------
    # BẢNG KÝ PHÊ DUYỆT (CUỐI GIÁO ÁN)
    # -------------------------------------------------------------
    sign_table = doc.add_table(rows=1, cols=2)
    sign_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sign_table.autofit = False

    s_left = sign_table.cell(0, 0)
    s_right = sign_table.cell(0, 1)
    s_left.width = Cm(8.0)
    s_right.width = Cm(8.5)
    _set_cell_margins(s_left, 0, 0, 0, 0)
    _set_cell_margins(s_right, 0, 0, 0, 0)

    _add_paragraph_styled(
        s_left, "DUYỆT CỦA BAN GIÁM HIỆU / TỔ CHUYÊN MÔN",
        size_pt=11.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=2
    )
    _add_paragraph_styled(
        s_left, "(Ký và ghi rõ họ tên)",
        size_pt=11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=45
    )
    _add_paragraph_styled(
        s_left, "................................................................",
        size_pt=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=0
    )

    _add_paragraph_styled(
        s_right, "Tân Tạo, ngày ..... tháng ..... năm 202...",
        size_pt=11.5, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=2
    )
    _add_paragraph_styled(
        s_right, "GIÁO VIÊN SOẠN BÀI",
        size_pt=11.5, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=2
    )
    _add_paragraph_styled(
        s_right, "(Ký và ghi rõ họ tên)",
        size_pt=11, italic=True, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=45
    )
    _add_paragraph_styled(
        s_right, "................................................................",
        size_pt=11, align=WD_ALIGN_PARAGRAPH.CENTER, space_after_pt=0
    )

    return doc


def build_lesson_plan_5512_bytes(lesson: Dict[str, Any]) -> io.BytesIO:
    """Generate Word docx and return as an in-memory byte buffer."""
    doc = build_lesson_plan_5512_doc(lesson)
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
