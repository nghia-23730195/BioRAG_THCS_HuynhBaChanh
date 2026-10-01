# -*- coding: utf-8 -*-
"""Fast and resilient 24-question benchmark runner."""

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

from src.app.api import (
    _biorag_load_chat_context,
    _biorag_chat_sources,
    _biorag_clean_vietnamese_answer,
    _biorag_extract_message_text,
    _biorag_chat_tokens,
    _biorag_chat_lesson_scope,
)
from src.app.dependencies import AppServices

QUESTIONS = [
    # Lớp 6
    {
        "id": "Q01",
        "grade": 6,
        "type": "Khái niệm",
        "question": "Tế bào là gì?",
        "sgk_lesson": "Bài 17: Tế bào",
        "sgk_page": "SGK KHTN 6 (KNTT) - Trang 62",
        "sgk_keypoints": "Tế bào là đơn vị cơ bản cấu tạo nên mọi cơ thể sống; thực hiện các hoạt động sống cơ bản như trao đổi chất, lớn lên, phân chia và cảm ứng."
    },
    {
        "id": "Q02",
        "grade": 6,
        "type": "Liệt kê",
        "question": "Nêu các thành phần chính của tế bào.",
        "sgk_lesson": "Bài 18 & 19: Cấu tạo tế bào",
        "sgk_page": "SGK KHTN 6 (KNTT) - Trang 65–70",
        "sgk_keypoints": "Gồm 3 thành phần chính: (1) Màng tế bào (bảo vệ, kiểm soát chất ra vào); (2) Tế bào chất (chứa bào quan, diễn ra hoạt động sống); (3) Nhân hoặc vùng nhân (chứa vật chất di truyền, điều khiển hoạt động sống)."
    },
    {
        "id": "Q03",
        "grade": 6,
        "type": "So sánh",
        "question": "Tế bào thực vật và tế bào động vật khác nhau ở những điểm nào?",
        "sgk_lesson": "Bài 19: Cấu tạo và chức năng các thành phần của tế bào",
        "sgk_page": "SGK KHTN 6 (KNTT) - Trang 69",
        "sgk_keypoints": "Tế bào thực vật có: thành tế bào (cellulose), lục lạp (quang hợp), và không bào trung tâm lớn. Tế bào động vật không có thành tế bào, không có lục lạp, không bào nhỏ hoặc không có."
    },
    {
        "id": "Q04",
        "grade": 6,
        "type": "Khái niệm",
        "question": "Cơ thể đơn bào là gì?",
        "sgk_lesson": "Bài 20: Cơ thể đơn bào và cơ thể đa bào",
        "sgk_page": "SGK KHTN 6 (KNTT) - Trang 71",
        "sgk_keypoints": "Cơ thể đơn bào là cơ thể chỉ được cấu tạo từ một tế bào duy nhất, nhưng tế bào đó thực hiện đầy đủ các quá trình sống của một cơ thể hoàn chỉnh (ví dụ: trùng roi, trùng giày, vi khuẩn, tảo lục đơn bào)."
    },
    {
        "id": "Q05",
        "grade": 6,
        "type": "Giải thích",
        "question": "Vì sao cần phân loại thế giới sống?",
        "sgk_lesson": "Bài 22: Phân loại thế giới sống",
        "sgk_page": "SGK KHTN 6 (KNTT) - Trang 77",
        "sgk_keypoints": "Phân loại giúp nhận biết, gọi tên chính xác sinh vật; xác định vị trí và mối quan hệ họ hàng tiến hóa giữa các nhóm sinh vật; hỗ trợ tìm hiểu, bảo tồn và sử dụng hiệu quả sinh vật."
    },
    {
        "id": "Q06",
        "grade": 6,
        "type": "Vận dụng",
        "question": "Vi khuẩn có những vai trò nào trong đời sống?",
        "sgk_lesson": "Bài 27: Vi khuẩn",
        "sgk_page": "SGK KHTN 6 (KNTT) - Trang 94–95",
        "sgk_keypoints": "Vai trò có ích: phân hủy xác sinh vật làm sạch môi trường, tạo mùn; cố định đạm cho cây; chế biến thực phẩm lên men (sữa chua, muối dưa, phô mai); sản xuất kháng sinh/chế phẩm sinh học. Tác hại: gây bệnh cho người/vật/cây, làm thiu thối thực phẩm."
    },

    # Lớp 7
    {
        "id": "Q07",
        "grade": 7,
        "type": "Khái niệm",
        "question": "Quang hợp là gì?",
        "sgk_lesson": "Bài 22: Quang hợp ở thực vật",
        "sgk_page": "SGK KHTN 7 (KNTT) - Trang 101–102",
        "sgk_keypoints": "Quang hợp là quá trình lá cây thu nhận năng lượng ánh sáng mặt trời để tổng hợp chất hữu cơ (glucose/tinh bột) từ nước và khí carbon dioxide, đồng thời giải phóng khí oxygen."
    },
    {
        "id": "Q08",
        "grade": 7,
        "type": "Liệt kê",
        "question": "Quá trình quang hợp cần những yếu tố nào?",
        "sgk_lesson": "Bài 22 & 23: Quang hợp và các yếu tố ảnh hưởng",
        "sgk_page": "SGK KHTN 7 (KNTT) - Trang 102, 105–107",
        "sgk_keypoints": "Các yếu tố nguyên liệu và điều kiện cần thiết: Ánh sáng, Nước, Khí Carbon dioxide (CO2), Diệp lục (trong lục lạp), và Nhiệt độ môi trường thích hợp."
    },
    {
        "id": "Q09",
        "grade": 7,
        "type": "Khái niệm",
        "question": "Nhóm cây ưa sáng là gì?",
        "sgk_lesson": "Bài 23: Một số yếu tố ảnh hưởng đến quang hợp",
        "sgk_page": "SGK KHTN 7 (KNTT) - Trang 105",
        "sgk_keypoints": "Cây ưa sáng là những cây có nhu cầu chiếu sáng cao, sống ở nơi quang đãng hoặc có cường độ ánh sáng mạnh (ví dụ: phi lao, thông, ngô, dừa, hoa giấy,...)."
    },
    {
        "id": "Q10",
        "grade": 7,
        "type": "Giải thích",
        "question": "Ánh sáng ảnh hưởng đến quang hợp như thế nào?",
        "sgk_lesson": "Bài 23: Một số yếu tố ảnh hưởng đến quang hợp",
        "sgk_page": "SGK KHTN 7 (KNTT) - Trang 105",
        "sgk_keypoints": "Cường độ ánh sáng tăng thì hiệu quả quang hợp tăng đến điểm bão hòa; ánh sáng quá yếu quang hợp kém; ánh sáng quá gay gắt đốt nóng lá làm giảm quang hợp. Thực vật thích nghi thành cây ưa sáng và cây ưa bóng."
    },
    {
        "id": "Q11",
        "grade": 7,
        "type": "Khái niệm",
        "question": "Hô hấp tế bào là gì?",
        "sgk_lesson": "Bài 24: Hô hấp tế bào",
        "sgk_page": "SGK KHTN 7 (KNTT) - Trang 108–109",
        "sgk_keypoints": "Hô hấp tế bào là quá trình phân giải chất hữu cơ (chủ yếu là glucose) với sự tham gia của oxygen, tạo ra năng lượng ATP cung cấp cho hoạt động sống, đồng thời thải ra khí carbon dioxide và nước."
    },
    {
        "id": "Q12",
        "grade": 7,
        "type": "So sánh",
        "question": "Quang hợp và hô hấp tế bào khác nhau như thế nào?",
        "sgk_lesson": "Bài 24: Hô hấp tế bào",
        "sgk_page": "SGK KHTN 7 (KNTT) - Trang 110",
        "sgk_keypoints": "Quang hợp: tổng hợp chất hữu cơ, tích lũy năng lượng, cần CO2 và nước, thải O2, diễn ra ở lục lạp khi có ánh sáng. Hô hấp tế bào: phân giải chất hữu cơ, giải phóng năng lượng ATP, cần O2 và chất hữu cơ, thải CO2 và nước, diễn ra ở ty thể suốt ngày đêm."
    },

    # Lớp 8
    {
        "id": "Q13",
        "grade": 8,
        "type": "Liệt kê",
        "question": "Hệ vận động ở người gồm những thành phần chính nào?",
        "sgk_lesson": "Bài 29: Khái quát cơ thể người & Bài 30: Hệ vận động ở người",
        "sgk_page": "SGK KHTN 8 (KNTT) - Trang 123–126",
        "sgk_keypoints": "Gồm 3 thành phần chính: (1) Bộ xương (xương đầu, xương thân, xương chi); (2) Hệ cơ (các cơ vân bám xương); (3) Các khớp xương (khớp động, khớp bán động, khớp bất động)."
    },
    {
        "id": "Q14",
        "grade": 8,
        "type": "Chức năng",
        "question": "Hồng cầu có chức năng gì?",
        "sgk_lesson": "Bài 31: Máu và hệ tuần hoàn ở người",
        "sgk_page": "SGK KHTN 8 (KNTT) - Trang 128",
        "sgk_keypoints": "Hồng cầu chứa huyết sắc tố (hemoglobin) có chức năng vận chuyển khí oxygen (O2) từ phổi đến các tế bào và vận chuyển khí carbon dioxide (CO2) từ tế bào về phổi để thải ra ngoài."
    },
    {
        "id": "Q15",
        "grade": 8,
        "type": "Chức năng",
        "question": "Tim có vai trò gì trong hệ tuần hoàn?",
        "sgk_lesson": "Bài 31: Máu và hệ tuần hoàn ở người",
        "sgk_page": "SGK KHTN 8 (KNTT) - Trang 130–131",
        "sgk_keypoints": "Tim hoạt động như một chiếc bơm hút và đẩy máu liên tục qua hệ thống mạch máu, tạo động lực chính để lưu thông máu trong vòng tuần hoàn lớn và vòng tuần hoàn nhỏ khắp cơ thể."
    },
    {
        "id": "Q16",
        "grade": 8,
        "type": "Quá trình",
        "question": "Thức ăn đi qua những cơ quan nào của ống tiêu hóa?",
        "sgk_lesson": "Bài 32: Hệ tiêu hóa ở người",
        "sgk_page": "SGK KHTN 8 (KNTT) - Trang 134",
        "sgk_keypoints": "Thức ăn lần lượt đi qua các cơ quan: Miệng -> Hầu -> Thực quản -> Dạ dày -> Ruột non -> Ruột già -> Trực tràng -> Hậu môn."
    },
    {
        "id": "Q17",
        "grade": 8,
        "type": "Chức năng",
        "question": "Thận có vai trò gì trong hệ bài tiết nước tiểu?",
        "sgk_lesson": "Bài 34: Hệ bài tiết ở người",
        "sgk_page": "SGK KHTN 8 (KNTT) - Trang 141–142",
        "sgk_keypoints": "Thận là cơ quan bài tiết chủ yếu, có chức năng lọc máu, loại bỏ các chất cặn bã, chất độc hại và nước thừa để hình thành nước tiểu; duy trì ổn định thể tích, thành phần máu và cân bằng nội môi."
    },
    {
        "id": "Q18",
        "grade": 8,
        "type": "Vận dụng",
        "question": "Nêu các biện pháp bảo vệ mắt được trình bày trong SGK.",
        "sgk_lesson": "Bài 36: Điều hòa môi trường trong và các giác quan",
        "sgk_page": "SGK KHTN 8 (KNTT) - Trang 150–152",
        "sgk_keypoints": "Giữ khoảng cách đọc sách/màn hình hợp lý (30–40 cm); đủ ánh sáng, không đọc khi xe rung lắc; không nhìn màn hình liên tục quá lâu; bổ sung vitamin A; đeo kính bảo hộ khi lao động; khám mắt định kỳ."
    },

    # Lớp 9
    {
        "id": "Q19",
        "grade": 9,
        "type": "Khái niệm",
        "question": "DNA là gì?",
        "sgk_lesson": "Bài 38: DNA và RNA",
        "sgk_page": "SGK KHTN 9 (KNTT) - Trang 160–162",
        "sgk_keypoints": "DNA (deoxyribonucleic acid) là đại phân tử sinh học cấu tạo theo nguyên tắc đa phân gồm các đơn phân là 4 loại nucleotide (A, T, G, C); mang thông tin di truyền quy định cấu trúc và chức năng của sinh vật."
    },
    {
        "id": "Q20",
        "grade": 9,
        "type": "Cấu trúc & Chức năng",
        "question": "Nêu cấu trúc không gian và chức năng của phân tử DNA.",
        "sgk_lesson": "Bài 38: DNA và RNA",
        "sgk_page": "SGK KHTN 9 (KNTT) - Trang 161–163",
        "sgk_keypoints": "Cấu trúc: xoắn kép gồm 2 mạch polynucleotide song song ngược chiều, liên kết theo nguyên tắc bổ sung (A-T bằng 2 liên kết H, G-C bằng 3 liên kết H). Chức năng: lưu giữ, bảo quản và truyền đạt thông tin di truyền qua các thế hệ tế bào và cơ thể."
    },
    {
        "id": "Q21",
        "grade": 9,
        "type": "Khái niệm",
        "question": "Gene là gì?",
        "sgk_lesson": "Bài 39: Gene và quá trình truyền đạt thông tin di truyền",
        "sgk_page": "SGK KHTN 9 (KNTT) - Trang 165",
        "sgk_keypoints": "Gene là một đoạn của phân tử DNA mang thông tin mã hóa cho một sản phẩm xác định (chuỗi polypeptide hoặc phân tử RNA); là đơn vị chức năng cơ bản của di truyền."
    },
    {
        "id": "Q22",
        "grade": 9,
        "type": "Khái niệm & Liệt kê",
        "question": "Đột biến gene là gì và có những dạng nào?",
        "sgk_lesson": "Bài 41: Đột biến gene",
        "sgk_page": "SGK KHTN 9 (KNTT) - Trang 173–175",
        "sgk_keypoints": "Đột biến gene là những biến đổi trong cấu trúc của gene, liên quan đến một hoặc một số cặp nucleotide. Các dạng đột biến điểm cơ bản: thay thế một cặp nucleotide, thêm một cặp nucleotide, mất một cặp nucleotide."
    },
    {
        "id": "Q23",
        "grade": 9,
        "type": "Cấu trúc & Vai trò",
        "question": "Nhiễm sắc thể là gì và có vai trò gì trong di truyền?",
        "sgk_lesson": "Bài 42: Nhiễm sắc thể và bộ nhiễm sắc thể",
        "sgk_page": "SGK KHTN 9 (KNTT) - Trang 177–179",
        "sgk_keypoints": "Nhiễm sắc thể là cấu trúc nằm trong nhân tế bào, được cấu tạo từ DNA và protein (chủ yếu là histone). Vai trò: lưu giữ thông tin di truyền, phân chia đồng đều vật chất di truyền cho các tế bào con qua nguyên phân/giảm phân."
    },
    {
        "id": "Q24",
        "grade": 9,
        "type": "Khái niệm & Phân loại",
        "question": "Đột biến nhiễm sắc thể là gì?",
        "sgk_lesson": "Bài 45: Đột biến nhiễm sắc thể",
        "sgk_page": "SGK KHTN 9 (KNTT) - Trang 189–192",
        "sgk_keypoints": "Đột biến nhiễm sắc thể là những biến đổi về cấu trúc hoặc số lượng của nhiễm sắc thể trong tế bào. Gồm 2 nhóm chính: đột biến cấu trúc NST (mất đoạn, lặp đoạn, đảo đoạn, chuyển đoạn) và đột biến số lượng NST (lệch bội, đa bội)."
    }
]

def generate_rag_answer(item, llm):
    q = item["question"]
    g = item["grade"]
    scope = _biorag_chat_lesson_scope(q, g)
    context = _biorag_load_chat_context([q], g, lesson_scope=scope)
    
    if not context:
        return "Thông tin này không được đề cập trong sách giáo khoa KHTN hoặc nằm ngoài phạm vi tài liệu tra cứu.", []

    context_blocks = [
        f"[S{idx} | {c['source']} | trang {c['page']}]\n{c['text']}"
        for idx, c in enumerate(context, 1)
    ]
    evidence_block = "\n\n".join(context_blocks)
    
    prompt = f"""Bạn là trợ lý giải đáp Khoa học tự nhiên THCS (lớp 6-9) chính xác theo Sách giáo khoa Kết nối tri thức.

[CÂU HỎI]:
{q}

[NGỮ LIỆU SGK KNTT]:
{evidence_block}

QUY TẮC BẮT BUỘC:
1. Trả lời trực tiếp, cô đọng, súc tích, chính xác theo NGỮ LIỆU SGK KNTT.
2. Mọi khẳng định khoa học phải kèm mã nguồn [S1], [S2] ở cuối câu.
3. Không chào hỏi, không dùng câu dẫn rập khuôn.
"""
    draft = _biorag_extract_message_text(llm.invoke(prompt))
    ans = _biorag_clean_vietnamese_answer(draft)
    sources = _biorag_chat_sources(context, answer=ans)
    return ans, sources

def run():
    print("Khởi tạo LLM...", flush=True)
    llm = AppServices.get_instance().llm
    results = []
    os.makedirs("scratch", exist_ok=True)
    
    for i, item in enumerate(QUESTIONS, 1):
        qid = item["id"]
        q = item["question"]
        g = item["grade"]
        print(f"[{i:02d}/24] {qid} (Lớp {g}): '{q}'...", end=" ", flush=True)
        t0 = time.time()
        try:
            ans, sources = generate_rag_answer(item, llm)
            code = 200
        except Exception as e:
            ans = f"Error: {e}"
            sources = []
            code = 500
        ms = (time.time() - t0) * 1000
        print(f"OK ({ms:.1f}ms)", flush=True)

        results.append({
            "id": qid,
            "grade": g,
            "type": item["type"],
            "question": q,
            "sgk_lesson": item["sgk_lesson"],
            "sgk_page": item["sgk_page"],
            "sgk_keypoints": item["sgk_keypoints"],
            "rag_answer": ans,
            "rag_sources": sources,
            "latency_ms": ms
        })

        # Save incremental progress
        with open("scratch/benchmark_24_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)

    print("\n[+] Đã hoàn thành 24/24 câu hỏi và lưu vào scratch/benchmark_24_results.json", flush=True)

if __name__ == "__main__":
    run()
