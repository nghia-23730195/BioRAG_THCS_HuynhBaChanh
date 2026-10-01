# -*- coding: utf-8 -*-
import sys
import io
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

df = pd.read_excel('Bo_cau_hoi_phan_loai_hoan_chinh (2).xlsx', sheet_name='Cau hoi')

queries_to_find = [
    "Tế bào là gì",
    "Nêu các thành phần chính của tế bào",
    "Tế bào thực vật và tế bào động vật khác nhau",
    "Cơ thể đơn bào là gì",
    "Vì sao cần phân loại thế giới sống",
    "Vi khuẩn có những vai trò nào trong đời sống",
    "Quang hợp là gì",
    "Quá trình quang hợp cần những yếu tố nào",
    "Nhóm cây ưa sáng là gì",
    "Ánh sáng ảnh hưởng đến quang hợp như thế nào",
    "Hô hấp tế bào là gì",
    "Quang hợp và hô hấp tế bào khác nhau như thế nào",
    "Hệ vận động ở người gồm những thành phần",
    "Hồng cầu có chức năng gì",
    "Tim có vai trò gì trong hệ tuần hoàn",
    "Thức ăn đi qua những cơ quan nào của ống tiêu hóa",
    "Thận có vai trò gì trong hệ bài tiết nước tiểu",
    "Nêu các biện pháp bảo vệ mắt được trình bày trong SGK",
    "DNA là gì",
]

for idx, row in df.iterrows():
    q = str(row.get('Câu hỏi', ''))
    for target in queries_to_find:
        if target.lower() in q.lower():
            print(f"Row {idx+1}: {row.get('Mã câu')} | Lớp {row.get('Khối lớp')} | {q}")
            print(f"   SGK: {row.get('Sách nguồn')} - Trang {row.get('Trang nguồn')}")
            print(f"   Đáp án chuẩn: {row.get('Đáp án chuẩn')}")
            print("-" * 50)
            break
