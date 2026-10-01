# -*- coding: utf-8 -*-
import sys
import io
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

df = pd.read_excel('Bo_cau_hoi_phan_loai_hoan_chinh (2).xlsx', sheet_name='Cau hoi')
print(f'Total questions: {len(df)}')
for idx, row in df.iterrows():
    m = row.get('Mã câu', idx+1)
    k = row.get('Khối lớp', '')
    nhom = row.get('Nhóm câu hỏi', '')
    q = row.get('Câu hỏi', '')
    src = row.get('Sách nguồn', '')
    pg = row.get('Trang nguồn', '')
    gt = row.get('Đáp án chuẩn', '')
    print(f"{m} | Lớp {k} | {nhom} | {q}")
    print(f"   Nguồn: {src} - Trang {pg}")
    print(f"   Đáp án chuẩn: {gt}")
    print("-" * 60)
