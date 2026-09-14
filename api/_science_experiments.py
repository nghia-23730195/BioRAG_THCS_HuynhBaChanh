# -*- coding: utf-8 -*-
"""Ngân hàng Thí nghiệm Ảo KHTN: Vật lý & Hóa học (Bộ sách Kết nối tri thức).

Cung cấp dữ liệu chi tiết cho các bài thực hành, thí nghiệm trọng tâm
của chương trình KHTN lớp 6, 7, 8, 9 phục vụ mô phỏng tương tác 2D
và tự động xuất Báo cáo thực hành chuẩn ra Word (.docx).
"""

import io
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

EXPERIMENT_CATALOG = [
    {
        "id": "k6-phy-bien-dang-lo-xo",
        "grade": 6,
        "subject": "physics",
        "subject_label": "Vật lý",
        "title": "Khảo sát Độ biến dạng của Lò xo và Lực đàn hồi",
        "lesson_ref": "KHTN 6 · Bài 42: Biến dạng của lò xo",
        "topic": "Lực và Sự biến dạng của vật",
        "duration_minutes": 35,
        "difficulty": "Cơ bản",
        "badge": "⚡ Vật lý 6",
        "summary": "Khảo sát mối quan hệ giữa độ dãn của lò xo treo thẳng đứng với khối lượng của các quả nặng móc vào đầu dưới lò xo.",
        "simulation_type": "spring_stretch",
        "default_params": {
            "mass_g": 100,
            "spring_k": 25,
            "original_length_cm": 12
        },
        "safety_notes": [
            "Treo quả nặng nhẹ nhàng, không kéo dãn lò xo quá mức giới hạn đàn hồi làm hỏng hoặc biến dạng vĩnh viễn lò xo.",
            "Cẩn thận khi móc các quả cân kim loại, tránh làm rơi vào chân hoặc làm vỡ mặt kính bàn thí nghiệm."
        ],
        "equipment": [
            "Giá thí nghiệm thẳng đứng có gắn thước đo chiều dài chia vạch milimet (0 - 30 cm)",
            "Lò xo xoắn ốc bằng thép có gắn kim chỉ thị ở đầu dưới (chiều dài tự nhiên l0 = 12 cm)",
            "Hộp quả nặng chuẩn (4 quả, mỗi quả có khối lượng 50g, trọng lượng P = 0,5 N)",
            "Móc treo quả nặng"
        ],
        "procedure_steps": [
            "Bước 1: Lắp lò xo vào giá thí nghiệm thẳng đứng. Đọc và ghi lại chiều dài ban đầu l0 của lò xo khi chưa treo quả nặng.",
            "Bước 2: Móc 1 quả nặng 50g (P1 = 0,5N) vào đầu dưới của lò xo. Đợi lò xo đứng yên, đọc chiều dài l1 và tính độ dãn Δl1 = l1 - l0.",
            "Bước 3: Lần lượt móc thêm quả nặng thứ 2 (100g, P2 = 1,0N), quả thứ 3 (150g, P3 = 1,5N), quả thứ 4 (200g, P4 = 2,0N). Đọc và ghi lại chiều dài l tương ứng.",
            "Bước 4: Tính độ dãn Δl = l - l0 cho từng lần đo và ghi vào bảng số liệu.",
            "Bước 5: Vẽ đồ thị biểu diễn mối liên hệ giữa độ dãn Δl và khối lượng m của các quả nặng treo vào."
        ],
        "expected_phenomenon": "Khi móc thêm các quả nặng vào đầu dưới của lò xo, lò xo bị dãn dài thêm ra. Khi khối lượng quả nặng tăng lên 2 lần, 3 lần, 4 lần thì độ dãn của lò xo cũng tăng lên tương ứng 2 lần, 3 lần, 4 lần. Khi tháo hết quả nặng ra, lò xo co lại trở về đúng chiều dài ban đầu l0.",
        "scientific_explanation": "Độ dãn của lò xo treo thẳng đứng tỉ lệ thuận với khối lượng (trọng lượng) của vật treo: Δl = l - l0 ~ m (hoặc F_đh = P = k · Δl, trong đó k là độ cứng của lò xo). Lực đàn hồi xuất hiện khi lò xo bị biến dạng và có xu hướng chống lại nguyên nhân gây ra biến dạng, đưa lò xo trở lại hình dạng ban đầu.",
        "formula": "Δl = l - l0 ~ m ⇔ F_đh = k · Δl = P = m · g",
        "sample_data": [
            {
                "trial": 1,
                "mass": "50 g",
                "force": "0,5 N",
                "length": "14,0 cm",
                "delta_l": "2,0 cm"
            },
            {
                "trial": 2,
                "mass": "100 g",
                "force": "1,0 N",
                "length": "16,0 cm",
                "delta_l": "4,0 cm"
            },
            {
                "trial": 3,
                "mass": "150 g",
                "force": "1,5 N",
                "length": "18,0 cm",
                "delta_l": "6,0 cm"
            },
            {
                "trial": 4,
                "mass": "200 g",
                "force": "2,0 N",
                "length": "20,0 cm",
                "delta_l": "8,0 cm"
            }
        ],
        "practice_questions": [
            {
                "question": "Độ dãn của lò xo treo thẳng đứng có mối quan hệ như thế nào với khối lượng quả nặng treo vào lò xo?",
                "options": [
                    "Tỉ lệ nghịch với khối lượng quả nặng",
                    "Tỉ lệ thuận với khối lượng quả nặng",
                    "Không phụ thuộc vào khối lượng quả nặng",
                    "Tăng giảm ngẫu nhiên"
                ],
                "answer_index": 1,
                "explanation": "Khi tăng khối lượng quả nặng lên bao nhiêu lần thì độ dãn của lò xo cũng tăng lên bấy nhiêu lần (tỉ lệ thuận)."
            },
            {
                "question": "Một lò xo có chiều dài tự nhiên l0 = 12 cm. Khi treo quả nặng 50g lò xo dài 14 cm. Khi treo quả nặng 150g thì chiều dài của lò xo là bao nhiêu?",
                "options": [
                    "16 cm",
                    "18 cm",
                    "20 cm",
                    "22 cm"
                ],
                "answer_index": 1,
                "explanation": "Khi treo 50g lò xo dãn Δl = 14 - 12 = 2 cm. Khi treo 150g (gấp 3 lần) lò xo dãn 2 x 3 = 6 cm. Chiều dài mới: l = 12 + 6 = 18 cm."
            },
            {
                "question": "Dụng cụ đo lực (lực kế lò xo) hoạt động dựa trên nguyên lý nào?",
                "options": [
                    "Độ dãn của lò xo tỉ lệ thuận với lực tác dụng",
                    "Sự dẫn nhiệt nhanh của kim loại lò xo",
                    "Sự bay hơi của chất lỏng",
                    "Định luật phản xạ ánh sáng"
                ],
                "answer_index": 0,
                "explanation": "Lực kế lò xo cấu tạo dựa trên tính chất độ dãn của lò xo tỉ lệ thuận với lực kéo tác dụng vào nó."
            }
        ]
    },
    {
        "id": "k7-phy-phan-xa-anh-sang",
        "grade": 7,
        "subject": "physics",
        "subject_label": "Vật lý",
        "title": "Khảo sát Định luật phản xạ ánh sáng",
        "lesson_ref": "KHTN 7 · Bài 16: Sự phản xạ ánh sáng",
        "topic": "Ánh sáng và Gương phẳng",
        "duration_minutes": 35,
        "difficulty": "Cơ bản",
        "badge": "⚡ Vật lý 7",
        "summary": "Khảo sát mối quan hệ giữa góc phản xạ và góc tới khi chiếu chùm sáng hẹp vào bề mặt gương phẳng.",
        "simulation_type": "light_reflection",
        "default_params": {
            "incident_angle": 45,
            "show_normals": True,
            "show_protractor": True,
            "mirror_surface": "flat"
        },
        "safety_notes": [
            "Không chiếu trực tiếp chùm tia laser hoặc đèn rọi công suất cao vào mắt bạn học.",
            "Cẩn thận khi cầm gương phẳng bằng thủy tinh, tránh làm rơi vỡ gây đứt tay."
        ],
        "equipment": [
            "Đèn phát chùm sáng hẹp (đèn laser hoặc đèn sợi đốt có khe hẹp)",
            "Gương phẳng gắn trên giá đỡ thẳng đứng",
            "Bảng chia độ (thước đo góc 180° gắn trên mặt phẳng)",
            "Nguồn điện 6V - 12V hoặc pin tiểu"
        ],
        "procedure_steps": [
            "Bước 1: Đặt bảng chia độ nằm ngang trên mặt bàn, cắm gương phẳng vuông góc với mặt phẳng bảng chia độ tại vạch số 0° (trục pháp tuyến).",
            "Bước 2: Bật nguồn đèn, chiếu chùm sáng hẹp đi là là trên mặt bảng chia độ tới điểm tới O trên gương với góc tới i = 30°.",
            "Bước 3: Quan sát tia phản xạ, đọc và ghi lại số đo góc phản xạ i' trên thước đo góc.",
            "Bước 4: Lần lượt thay đổi góc tới i = 45°, 60° rồi lặp lại việc đo góc phản xạ i'.",
            "Bước 5: So sánh giá trị góc phản xạ i' với góc tới i để rút ra kết luận."
        ],
        "expected_phenomenon": "Tia sáng phản xạ luôn nằm trong cùng mặt phẳng tới chứa tia tới và pháp tuyến của gương tại điểm tới. Góc phản xạ i' luôn có số đo bằng góc tới i (i' = i). Khi tăng góc tới thì góc phản xạ cũng tăng tương ứng.",
        "scientific_explanation": "Định luật phản xạ ánh sáng phát biểu: (1) Tia sáng phản xạ nằm trong mặt phẳng tới (mặt phẳng chứa tia tới và pháp tuyến của gương tại điểm tới); (2) Góc phản xạ bằng góc tới: i' = i.",
        "formula": "i' = i (Góc phản xạ = Góc tới)",
        "sample_data": [
            {
                "trial": 1,
                "incident_angle": "30°",
                "reflection_angle": "30°",
                "difference": "0°"
            },
            {
                "trial": 2,
                "incident_angle": "45°",
                "reflection_angle": "45°",
                "difference": "0°"
            },
            {
                "trial": 3,
                "incident_angle": "60°",
                "reflection_angle": "60°",
                "difference": "0°"
            }
        ],
        "practice_questions": [
            {
                "question": "Khi chiếu một tia sáng tới gương phẳng với góc tới i = 40°, góc phản xạ i' có giá trị là bao nhiêu?",
                "options": [
                    "20°",
                    "40°",
                    "50°",
                    "80°"
                ],
                "answer_index": 1,
                "explanation": "Theo định luật phản xạ ánh sáng, góc phản xạ luôn bằng góc tới: i' = i = 40°."
            },
            {
                "question": "Nếu tia tới hợp với mặt gương phẳng một góc 30°, góc phản xạ bằng bao nhiêu?",
                "options": [
                    "30°",
                    "60°",
                    "90°",
                    "120°"
                ],
                "answer_index": 1,
                "explanation": "Pháp tuyến vuông góc với mặt gương (90°). Góc tới i = 90° - 30° = 60°. Suy ra góc phản xạ i' = i = 60°."
            },
            {
                "question": "Tia sáng phản xạ nằm trong mặt phẳng nào?",
                "options": [
                    "Vuông góc với mặt phẳng tới",
                    "Mặt phẳng tới (chứa tia tới và pháp tuyến tại điểm tới)",
                    "Mặt phẳng của gương phẳng",
                    "Mặt phẳng bất kỳ tùy thuộc độ nhẵn của gương"
                ],
                "answer_index": 1,
                "explanation": "Theo định luật phản xạ ánh sáng, tia phản xạ luôn nằm trong mặt phẳng tới."
            }
        ]
    },
    {
        "id": "k8-phy-don-bay",
        "grade": 8,
        "subject": "physics",
        "subject_label": "Vật lý",
        "title": "Khảo sát Tác dụng làm quay của lực và Đòn bẩy",
        "lesson_ref": "KHTN 8 · Bài 19: Đòn bẩy",
        "topic": "Lực và Chuyển động quay",
        "duration_minutes": 40,
        "difficulty": "Thông hiểu",
        "badge": "⚡ Vật lý 8",
        "summary": "Nghiên cứu điều kiện cân bằng của đòn bẩy khi chịu tác dụng của các lực ở hai phía trục quay.",
        "simulation_type": "lever_balance",
        "default_params": {
            "left_weight": 2,
            "left_distance": 3,
            "right_weight": 3,
            "right_distance": 2,
            "show_forces": True
        },
        "safety_notes": [
            "Các quả cân bằng kim loại nặng cần móc cẩn thận, tránh làm rơi vào chân hoặc làm gãy thanh đòn bẩy.",
            "Đặt giá thí nghiệm trên mặt bàn bằng phẳng, chắc chắn."
        ],
        "equipment": [
            "Thanh đòn bẩy có chia vạch đều đối xứng qua trục quay O",
            "Giá đỡ có trục quay nhẹ, ma sát nhỏ",
            "Hộp quả nặng chuẩn (loại 50g mỗi quả, P = 0,5N)",
            "Lực kế lò xo 5N (nếu đo lực kéo thay thế)"
        ],
        "procedure_steps": [
            "Bước 1: Gắn thanh đòn bẩy lên giá đỡ, chỉnh ốc cân bằng sao cho thanh nằm ngang khi chưa treo quả nặng.",
            "Bước 2: Móc vào bên trái trục quay O tại khoảng cách d1 = 6 cm một chùm quả nặng gồm 2 quả (F1 = 1,0 N).",
            "Bước 3: Móc vào bên phải trục quay O các quả nặng (F2) tại khoảng cách d2 khác nhau cho đến khi thanh đòn bẩy thăng bằng nằm ngang.",
            "Bước 4: Ghi lại giá trị F1, d1, F2, d2 và tính các tích F1.d1 và F2.d2.",
            "Bước 5: Lặp lại với các cặp lực và khoảng cách khác (ví dụ: F1 = 1,5 N tại d1 = 4 cm)."
        ],
        "expected_phenomenon": "Khi đòn bẩy thăng bằng nằm ngang, tích của độ lớn lực tác dụng F1 với khoảng cách từ trục quay đến giá của lực d1 luôn xấp xỉ bằng tích F2.d2 (tổng momen lực làm quay cùng chiều kim đồng hồ bằng tổng momen lực làm quay ngược chiều).",
        "scientific_explanation": "Quy tắc momen lực và điều kiện cân bằng đòn bẩy: Đòn bẩy ở trạng thái cân bằng khi tích của lực tác dụng với cánh tay đòn ở hai bên trục quay bằng nhau: F1.d1 = F2.d2. Nhờ đó, nếu muốn nâng một vật nặng (F1 lớn) bằng một lực nhỏ (F2 nhỏ), ta cần làm cánh tay đòn d2 dài hơn d1.",
        "formula": "F1 · d1 = F2 · d2",
        "sample_data": [
            {
                "trial": 1,
                "F1": "1,0 N",
                "d1": "6 cm",
                "F1_x_d1": "6 N.cm",
                "F2": "1,5 N",
                "d2": "4 cm",
                "F2_x_d2": "6 N.cm"
            },
            {
                "trial": 2,
                "F1": "1,0 N",
                "d1": "9 cm",
                "F1_x_d1": "9 N.cm",
                "F2": "3,0 N",
                "d2": "3 cm",
                "F2_x_d2": "9 N.cm"
            },
            {
                "trial": 3,
                "F1": "2,0 N",
                "d1": "4 cm",
                "F1_x_d1": "8 N.cm",
                "F2": "1,0 N",
                "d2": "8 cm",
                "F2_x_d2": "8 N.cm"
            }
        ],
        "practice_questions": [
            {
                "question": "Để đòn bẩy thăng bằng nằm ngang, nếu cánh tay đòn d2 dài gấp 3 lần cánh tay đòn d1 thì lực F2 cần độ lớn bằng bao nhiêu lần F1?",
                "options": [
                    "Gấp 3 lần F1",
                    "Bằng 1/3 lần F1",
                    "Gấp 9 lần F1",
                    "Bằng F1"
                ],
                "answer_index": 1,
                "explanation": "Từ F1.d1 = F2.d2 suy ra F2 = F1.(d1/d2) = F1/3. Cánh tay đòn dài gấp 3 thì lực cần tác dụng giảm đi 3 lần (được lợi 3 lần về lực)."
            },
            {
                "question": "Dụng cụ nào sau đây là ứng dụng của đòn bẩy có điểm tựa nằm giữa điểm đặt của hai lực?",
                "options": [
                    "Xe cút kít",
                    "Kéo cắt giấy",
                    "Cái mở nắp chai bia",
                    "Kẹp gắp than"
                ],
                "answer_index": 1,
                "explanation": "Cái kéo có trục quay (điểm tựa) ở giữa, tay cầm tác dụng lực ở một đầu và lưỡi kéo cắt giấy ở đầu đối diện."
            }
        ]
    },
    {
        "id": "k8-phy-luc-day-archimedes",
        "grade": 8,
        "subject": "physics",
        "subject_label": "Vật lý",
        "title": "Khảo sát Lực đẩy Archimedes trong chất lỏng",
        "lesson_ref": "KHTN 8 · Bài 17: Lực đẩy Archimedes",
        "topic": "Áp suất và Lực đẩy chất lỏng",
        "duration_minutes": 40,
        "difficulty": "Thông hiểu",
        "badge": "⚡ Vật lý 8",
        "summary": "Đo độ lớn lực đẩy Archimedes tác dụng lên vật nhúng chìm trong nước và so sánh với trọng lượng của phần nước bị chiếm chỗ.",
        "simulation_type": "archimedes",
        "default_params": {
            "object_volume_cm3": 50,
            "liquid_density": 1000,
            "submerged_percent": 100
        },
        "safety_notes": [
            "Tránh làm đổ nước ra sàn gây trơn trượt.",
            "Lau khô vật và cốc đo sau khi kết thúc thí nghiệm."
        ],
        "equipment": [
            "Lực kế 0 - 5N có độ chia nhỏ nhất 0,1N",
            "Vật nặng bằng kim loại (nhôm hoặc đồng) có móc treo",
            "Bình tràn và bình chia độ đựng nước",
            "Cốc chứa nước và giá thí nghiệm"
        ],
        "procedure_steps": [
            "Bước 1: Treo vật nặng vào lực kế, đọc và ghi trọng lượng P của vật trong không khí.",
            "Bước 2: Đổ nước vào bình tràn cho tới đúng miệng vòi tràn, đặt cốc hứng rỗng dưới vòi tràn.",
            "Bước 3: Nhúng vật nặng chìm hoàn toàn vào bình tràn (không để chạm đáy hoặc thành bình). Đọc số chỉ P1 của lực kế.",
            "Bước 4: Tính độ lớn lực đẩy Archimedes thực nghiệm: FA = P - P1.",
            "Bước 5: Đổ lượng nước tràn ra vào bình chia độ, xác định thể tích V và cân trọng lượng Pnước tràn. So sánh FA với Pnước tràn."
        ],
        "expected_phenomenon": "Số chỉ lực kế khi nhúng chìm vật trong nước giảm đi so với khi đo trong không khí (P1 < P). Lượng giảm này đúng bằng trọng lượng của lượng nước tràn ra cốc hứng (FA = P - P1 = Pnước tràn).",
        "scientific_explanation": "Một vật nhúng trong chất lỏng bị chất lỏng tác dụng một lực đẩy hướng thẳng đứng từ dưới lên, gọi là lực đẩy Archimedes. Độ lớn của lực đẩy Archimedes bằng trọng lượng của phần chất lỏng bị vật chiếm chỗ: FA = d . V = rho . g . V.",
        "formula": "FA = d · V = ρ · g · V (FA = P - P1)",
        "sample_data": [
            {
                "trial": 1,
                "P_air": "1,5 N",
                "P_liquid": "1,0 N",
                "FA_measured": "0,5 N",
                "V_displaced": "50 cm³",
                "P_water": "0,5 N"
            },
            {
                "trial": 2,
                "P_air": "2,4 N",
                "P_liquid": "1,6 N",
                "FA_measured": "0,8 N",
                "V_displaced": "80 cm³",
                "P_water": "0,8 N"
            }
        ],
        "practice_questions": [
            {
                "question": "Lực đẩy Archimedes phụ thuộc vào những yếu tố nào sau đây?",
                "options": [
                    "Trọng lượng riêng của chất lỏng và thể tích phần chất lỏng bị vật chiếm chỗ",
                    "Khối lượng của vật và độ sâu của vật trong chất lỏng",
                    "Hình dạng của vật và diện tích mặt thoáng chất lỏng",
                    "Trọng lượng của vật và vận tốc của vật"
                ],
                "answer_index": 0,
                "explanation": "Công thức FA = d . V, trong đó d là trọng lượng riêng của chất lỏng, V là thể tích phần vật chìm trong chất lỏng."
            },
            {
                "question": "Một vật có thể tích 0,002 m³ nhúng chìm hoàn toàn trong nước (trọng lượng riêng d = 10 000 N/m³). Lực đẩy Archimedes tác dụng lên vật là:",
                "options": [
                    "5 N",
                    "20 N",
                    "200 N",
                    "50 N"
                ],
                "answer_index": 1,
                "explanation": "FA = d . V = 10 000 N/m³ x 0,002 m³ = 20 N."
            }
        ],
        "lesson_id": "k8-bai-17-luc-day-archimedes"
    },
    {
        "id": "k9-phy-dinh-luat-ohm",
        "grade": 9,
        "subject": "physics",
        "subject_label": "Vật lý",
        "title": "Khảo sát Định luật Ohm cho đoạn mạch điện",
        "lesson_ref": "KHTN 9 · Bài 11: Điện trở. Định luật Ohm",
        "topic": "Điện học - Định luật Ohm",
        "duration_minutes": 45,
        "difficulty": "Vận dụng",
        "badge": "⚡ Vật lý 9",
        "summary": "Khảo sát sự phụ thuộc của cường độ dòng điện vào hiệu điện thế đặt vào hai đầu dây dẫn và xác định điện trở của vật dẫn.",
        "simulation_type": "circuit_ohm",
        "default_params": {
            "voltage": 6.0,
            "resistance": 20.0,
            "switch_state": True
        },
        "safety_notes": [
            "Kiểm tra mạch điện trước khi đóng khóa K, không để xảy ra đoản mạch (chập mạch).",
            "Mắc đúng cực dương (+) và cực âm (-) của ampe kế và vôn kế.",
            "Chọn thang đo của ampe kế và vôn kế phù hợp với giá trị cần đo."
        ],
        "equipment": [
            "Nguồn điện một chiều 0 - 12V có thể điều chỉnh điện áp",
            "Điện trở mẫu R = 20 Ω gắn trên bảng lắp ráp",
            "Ampe kế một chiều (0 - 1A) đo dòng điện I",
            "Vôn kế một chiều (0 - 15V) đo hiệu điện thế U",
            "Khóa K, các dây dẫn nối mạch có đầu kẹp cá sấu"
        ],
        "procedure_steps": [
            "Bước 1: Mắc mạch điện theo sơ đồ: Nguồn -> Khóa K -> Ampe kế -> Đoạn dây điện trở R -> Nguồn; Vôn kế mắc song song với R.",
            "Bước 2: Mở khóa K, điều chỉnh nguồn điện về 0V. Đóng khóa K.",
            "Bước 3: Lần lượt điều chỉnh điện áp nguồn để vôn kế chỉ U = 2V, 4V, 6V, 8V, 10V.",
            "Bước 4: Đọc số chỉ tương ứng của ampe kế I (A) tại mỗi giá trị U.",
            "Bước 5: Tính tỉ số U/I cho từng lần đo và vẽ đồ thị biểu diễn sự phụ thuộc của I vào U."
        ],
        "expected_phenomenon": "Khi hiệu điện thế U giữa hai đầu dây dẫn tăng lên bao nhiêu lần thì cường độ dòng điện I chạy qua dây dẫn cũng tăng bấy nhiêu lần. Đồ thị I theo U là một đường thẳng đi qua gốc tọa độ O(0,0). Tỉ số U/I là không đổi và bằng giá trị điện trở R.",
        "scientific_explanation": "Định luật Ohm phát biểu: Cường độ dòng điện chạy qua một dây dẫn tỉ lệ thuận với hiệu điện thế đặt vào hai đầu dây và tỉ lệ nghịch với điện trở của dây: I = U / R. Điện trở R đặc trưng cho mức độ cản trở dòng điện của vật dẫn.",
        "formula": "I = U / R ⇔ R = U / I",
        "sample_data": [
            {
                "trial": 1,
                "voltage": "2,0 V",
                "current": "0,10 A",
                "resistance_calc": "20,0 Ω"
            },
            {
                "trial": 2,
                "voltage": "4,0 V",
                "current": "0,20 A",
                "resistance_calc": "20,0 Ω"
            },
            {
                "trial": 3,
                "voltage": "6,0 V",
                "current": "0,30 A",
                "resistance_calc": "20,0 Ω"
            },
            {
                "trial": 4,
                "voltage": "8,0 V",
                "current": "0,40 A",
                "resistance_calc": "20,0 Ω"
            }
        ],
        "practice_questions": [
            {
                "question": "Đặt hiệu điện thế U = 12V vào hai đầu dây dẫn có điện trở R = 30 Ω. Cường độ dòng điện chạy qua dây là:",
                "options": [
                    "0,25 A",
                    "0,4 A",
                    "2,5 A",
                    "360 A"
                ],
                "answer_index": 1,
                "explanation": "Theo định luật Ohm: I = U / R = 12 / 30 = 0,4 A."
            },
            {
                "question": "Đồ thị biểu diễn mối quan hệ giữa cường độ dòng điện I và hiệu điện thế U qua một điện trở cố định có dạng là:",
                "options": [
                    "Đường cong hyperbol",
                    "Đường thẳng đi qua gốc tọa độ O",
                    "Đường tròn đồng tâm",
                    "Đường thẳng song song với trục hoành"
                ],
                "answer_index": 1,
                "explanation": "Vì I tỉ lệ thuận với U (I = (1/R).U) nên đồ thị là đường thẳng đi qua gốc tọa độ."
            }
        ],
        "lesson_id": "k9-bai-11-dien-tro-dinh-luat-ohm"
    },
    {
        "id": "k9-phy-thau-kinh-hoi-tu",
        "grade": 9,
        "subject": "physics",
        "subject_label": "Vật lý",
        "title": "Tạo ảnh của một vật qua Thấu kính hội tụ",
        "lesson_ref": "KHTN 9 · Bài 8 & 9: Thấu kính - Tiêu cự thấu kính hội tụ",
        "topic": "Quang hình học - Thấu kính hội tụ",
        "duration_minutes": 45,
        "difficulty": "Vận dụng",
        "badge": "⚡ Vật lý 9",
        "summary": "Khảo sát vị trí, tính chất và kích thước của ảnh tạo bởi thấu kính hội tụ khi vật ở các khoảng cách khác nhau.",
        "simulation_type": "lens_convex",
        "default_params": {
            "focal_length": 10,
            "object_distance": 25,
            "object_height": 5
        },
        "safety_notes": [
            "Tránh chạm tay vào bề mặt quang học của thấu kính.",
            "Cẩn thận với nguồn nhiệt từ đèn chiếu hoặc nến thí nghiệm."
        ],
        "equipment": [
            "Giá quang học thẳng dài 1 mét có vạch chia milimet",
            "Thấu kính hội tụ mỏng có tiêu cự f = 10 cm gắn trên giá trượt",
            "Vật sáng (ngọn nến hoặc bảng chữ F phát sáng bằng đèn LED)",
            "Màn hứng ảnh màu trắng gắn trên giá trượt"
        ],
        "procedure_steps": [
            "Bước 1: Lắp thấu kính ở giữa giá quang học, lắp vật sáng và màn hứng ảnh ở hai bên thấu kính sao cho cùng trục quang học.",
            "Bước 2: Đặt vật ở rất xa thấu kính (d > 2f = 20 cm, ví dụ d = 25 cm). Dịch màn hứng để quan sát ảnh rõ nét.",
            "Bước 3: Ghi nhận tính chất ảnh (thật hay ảo, cùng chiều hay ngược chiều, lớn hơn hay nhỏ hơn vật).",
            "Bước 4: Di chuyển vật đến vị trí f < d < 2f (ví dụ d = 15 cm), tìm ảnh trên màn.",
            "Bước 5: Di chuyển vật vào trong khoảng tiêu cự d < f (ví dụ d = 6 cm), quan sát trực tiếp qua thấu kính để tìm ảnh ảo."
        ],
        "expected_phenomenon": "Khi vật ở ngoài khoảng tiêu cự (d > f): Cho ảnh thật, ngược chiều với vật, hứng được trên màn. Khi d > 2f ảnh nhỏ hơn vật; khi f < d < 2f ảnh lớn hơn vật. Khi vật ở trong khoảng tiêu cự (d < f): Cho ảnh ảo, cùng chiều và lớn hơn vật, nhìn thấy khi đặt mắt sau thấu kính.",
        "scientific_explanation": "Công thức thấu kính mỏng: 1/f = 1/d + 1/d'. Hai tia sáng đặc biệt: (1) Tia tới song song với trục chính cho tia ló đi qua tiêu điểm F'; (2) Tia tới đi qua quang tâm O truyền thẳng không đổi hướng.",
        "formula": "1/f = 1/d + 1/d' ⇔ d' = (d · f) / (d - f)",
        "sample_data": [
            {
                "trial": 1,
                "d": "30 cm",
                "f": "10 cm",
                "d_prime": "15,0 cm",
                "nature": "Ảnh thật, ngược chiều, nhỏ hơn vật"
            },
            {
                "trial": 2,
                "d": "20 cm (2f)",
                "f": "10 cm",
                "d_prime": "20,0 cm",
                "nature": "Ảnh thật, ngược chiều, bằng vật"
            },
            {
                "trial": 3,
                "d": "15 cm",
                "f": "10 cm",
                "d_prime": "30,0 cm",
                "nature": "Ảnh thật, ngược chiều, lớn hơn vật"
            }
        ],
        "practice_questions": [
            {
                "question": "Một thấu kính hội tụ có tiêu cự f = 12 cm. Đặt vật sáng vuông góc với trục chính cách thấu kính d = 6 cm. Ảnh tạo bởi thấu kính có đặc điểm gì?",
                "options": [
                    "Ảnh thật, ngược chiều, nhỏ hơn vật",
                    "Ảnh ảo, cùng chiều, lớn hơn vật",
                    "Ảnh thật, ngược chiều, lớn hơn vật",
                    "Ảnh ảo, ngược chiều, nhỏ hơn vật"
                ],
                "answer_index": 1,
                "explanation": "Vì vật nằm trong khoảng tiêu cự (d = 6 cm < f = 12 cm) nên thấu kính hội tụ cho ảnh ảo, cùng chiều và lớn hơn vật."
            }
        ],
        "lesson_id": "k9-bai-8-thau-kinh"
    },
    {
        "id": "k6-che-tach-chat",
        "grade": 6,
        "subject": "chemistry",
        "subject_label": "Hóa học",
        "title": "Tách muối ăn khỏi hỗn hợp cát và nước",
        "lesson_ref": "KHTN 6 · Bài 17: Tách chất khỏi hỗn hợp",
        "topic": "Các phương pháp tách chất (Lọc và Cô cạn)",
        "duration_minutes": 35,
        "difficulty": "Cơ bản",
        "badge": "🧪 Hóa học 6",
        "summary": "Áp dụng phương pháp lọc để tách chất rắn không tan (cát) và phương pháp cô cạn để thu hồi chất tan (muối ăn NaCl).",
        "simulation_type": "filtration_evaporation",
        "default_params": {
            "salt_amount_g": 5,
            "sand_amount_g": 5,
            "water_ml": 50,
            "step": "mix"
        },
        "safety_notes": [
            "Cẩn thận khi đun dung dịch trên đèn cồn, dùng kẹp gắp bát sứ, không sờ tay trực tiếp vào dụng cụ nóng.",
            "Tắt đèn cồn bằng cách đậy nắp, tuyệt đối không dùng miệng thổi."
        ],
        "equipment": [
            "Hỗn hợp cát sạch và muối ăn (NaCl)",
            "Cốc thủy tinh chịu nhiệt 100ml, đũa thủy tinh",
            "Phễu thủy tinh, giấy lọc tròn",
            "Bát sứ chịu nhiệt, đèn cồn, kiềng đun và lưới thép amiăng"
        ],
        "procedure_steps": [
            "Bước 1 (Hòa tan): Cho hỗn hợp cát và muối vào cốc thủy tinh, thêm 40ml nước cất, dùng đũa thủy tinh khuấy đều cho muối tan hết; cát không tan lắng xuống đáy.",
            "Bước 2 (Gấp và đặt giấy lọc): Gấp giấy lọc hình nón, đặt vào phễu, làm ướt giấy bằng vài giọt nước để giấy áp sát thành phễu.",
            "Bước 3 (Lọc): Rót từ từ hỗn hợp trong cốc dọc theo đũa thủy tinh vào phễu lọc. Cát bị giữ lại trên giấy lọc; nước lọc trong suốt chảy vào bình tam giác bên dưới.",
            "Bước 4 (Cô cạn): Rót phần nước lọc trong suốt vào bát sứ, đặt lên kiềng đun bằng đèn cồn và khuấy nhẹ.",
            "Bước 5: Khi nước bay hơi gần hết, tắt đèn cồn. Tinh thể muối ăn màu trắng kết tinh bám ở đáy bát sứ."
        ],
        "expected_phenomenon": "Sau khi lọc thu được chất rắn màu vàng nâu trên giấy lọc (cát) và dung dịch trong suốt không màu chảy xuống dưới (nước muối). Sau khi cô cạn trên ngọn lửa đèn cồn, nước bay hơi hết thu được các tinh thể màu trắng dạng hạt mịn là muối ăn.",
        "scientific_explanation": "Phương pháp lọc dựa trên sự khác nhau về tính tan và kích thước hạt: Cát không tan trong nước và kích thước hạt lớn hơn lỗ xốp giấy lọc nên bị giữ lại. Phương pháp cô cạn dựa trên độ bay hơi khác nhau: Nước có nhiệt độ sôi thấp (100°C) bay hơi trước, muối ăn NaCl có nhiệt độ nóng chảy và sôi rất cao (801°C) nên kết tinh lại.",
        "formula": "NaCl (dd) —(đun nóng)→ NaCl (r) + H2O (hơi)",
        "sample_data": [
            {
                "step_name": "Trước khi hòa tan",
                "phenomenon": "Hỗn hợp hạt cát vàng và hạt muối trắng lẫn lộn"
            },
            {
                "step_name": "Sau khi lọc qua phễu",
                "phenomenon": "Cát ướt giữ lại trên giấy lọc, nước lọc thu được trong suốt"
            },
            {
                "step_name": "Sau khi cô cạn bát sứ",
                "phenomenon": "Nước bay hơi hoàn toàn, để lại tinh thể muối ăn trắng tinh khiết"
            }
        ],
        "practice_questions": [
            {
                "question": "Phương pháp lọc dùng để tách riêng hỗn hợp nào sau đây?",
                "options": [
                    "Chất rắn không tan ra khỏi chất lỏng",
                    "Chất rắn tan ra khỏi dung dịch",
                    "Hai chất lỏng hòa tan vào nhau",
                    "Các chất khí có khối lượng khác nhau"
                ],
                "answer_index": 0,
                "explanation": "Phương pháp lọc dùng để tách chất rắn không tan ra khỏi chất lỏng (ví dụ cát trong nước)."
            },
            {
                "question": "Tại sao không thể dùng phương pháp lọc để tách muối ăn tan trong nước?",
                "options": [
                    "Vì muối ăn làm rách giấy lọc",
                    "Vì các phân tử/ion muối tan có kích thước rất nhỏ lọt qua lỗ xốp của giấy lọc cùng nước",
                    "Vì muối ăn phản ứng với giấy lọc",
                    "Vì nước muối bay hơi nhanh hơn nước cất"
                ],
                "answer_index": 1,
                "explanation": "Muối ăn tan tạo thành dung dịch đồng nhất, các ion Na+ và Cl- lọt qua lỗ lọc cùng phân tử nước."
            }
        ],
        "lesson_id": "k6-bai-17-tach-chat-khoi-hon-hop"
    },
    {
        "id": "k7-che-mo-hinh-phan-tu",
        "grade": 7,
        "subject": "chemistry",
        "subject_label": "Hóa học",
        "title": "Khảo sát Mô hình Phân tử & Liên kết Hóa học",
        "lesson_ref": "KHTN 7 · Bài 5 & 6: Phân tử & Liên kết hóa học",
        "topic": "Phân tử - Đơn chất, Hợp chất và Liên kết hóa học",
        "duration_minutes": 40,
        "difficulty": "Thông hiểu",
        "badge": "🧪 Hóa học 7",
        "summary": "Khảo sát cấu tạo phân tử của đơn chất (H2, O2, N2) và hợp chất (H2O, CH4, CO2, NaCl); mô phỏng cơ chế góp chung electron để tạo liên kết cộng hóa trị hoặc cho-nhận electron tạo liên kết ion.",
        "simulation_type": "molecule_bonding",
        "default_params": {
            "selected_molecule": "H2O",
            "view_mode": "bohr_shared"
        },
        "safety_notes": [
            "Khi lắp ráp các mô hình quả cầu và que nối kim loại/nhựa, thao tác cẩn thận tránh để các đầu que nhọn chọc vào tay.",
            "Sau khi thực hành xong, tháo rời và phân loại quả cầu theo đúng màu sắc quy ước vào các ngăn hộp."
        ],
        "equipment": [
            "Bộ mô hình phân tử hóa học gồm các quả cầu nguyên tử (H: trắng, O: đỏ, C: đen/xám, N: xanh lam, Na: tím, Cl: xanh lục)",
            "Hộp thanh nối ngắn (liên kết đơn) và thanh nối lò xo uốn cong (liên kết đôi, liên kết ba)",
            "Bảng mô hình cấu tạo lớp vỏ electron của các nguyên tử (mô hình Rutherford - Bohr)"
        ],
        "procedure_steps": [
            "Bước 1: Chọn phân tử cần khảo sát trên giao diện mô phỏng (H2, O2, H2O, CH4, CO2, NaCl).",
            "Bước 2: Quan sát số lượng electron ở lớp ngoài cùng của từng nguyên tử tự do trước khi tạo liên kết.",
            "Bước 3: Nhấn nút liên kết để các nguyên tử tiến lại gần nhau và góp chung các cặp electron (hoặc chuyển giao electron tạo ion).",
            "Bước 4: Đếm số cặp electron dùng chung (1 cặp = liên kết đơn, 2 cặp = liên kết đôi, 3 cặp = liên kết ba) và kiểm tra quy tắc octet (8 electron lớp ngoài cùng bền vững).",
            "Bước 5: Xác định khối lượng phân tử (Phân tử khối) bằng cách tính tổng khối lượng của các nguyên tử cấu thành (đơn vị amu)."
        ],
        "expected_phenomenon": "Phân tử H2: 2 nguyên tử H góp chung 1 cặp e (liên kết đơn H-H). Phân tử O2: 2 nguyên tử O góp chung 2 cặp e (liên kết đôi O=O). Phân tử H2O: Nguyên tử O góp chung 2 cặp e với 2 nguyên tử H tạo phân tử dạng góc (H-O-H). Phân tử CH4: Nguyên tử C góp chung 4 cặp e với 4 nguyên tử H tạo dạng tứ diện đều. Phân tử NaCl: Na nhường 1e cho Cl tạo ion Na+ và Cl- hút nhau.",
        "scientific_explanation": "Các nguyên tử liên kết với nhau để đạt được cấu hình electron bền vững của khí hiếm ở lớp ngoài cùng (2 electron đối với He/H; 8 electron octet đối với các nguyên tố khác). Liên kết cộng hóa trị hình thành bằng các cặp electron dùng chung giữa các phi kim. Liên kết ion hình thành do lực hút tĩnh điện giữa các ion mang điện tích trái dấu sau khi kim loại nhường electron cho phi kim.",
        "formula": "Khối lượng phân tử = Σ (Số nguyên tử × Khối lượng nguyên tử) (amu)",
        "sample_data": [
            {
                "molecule": "Hydrogen (H2)",
                "type": "Đơn chất",
                "formula": "H-H",
                "bonding": "1 cặp electron dùng chung (Cộng hóa trị)",
                "mol_mass": "2 amu"
            },
            {
                "molecule": "Oxygen (O2)",
                "type": "Đơn chất",
                "formula": "O=O",
                "bonding": "2 cặp electron dùng chung (Cộng hóa trị)",
                "mol_mass": "32 amu"
            },
            {
                "molecule": "Nước (H2O)",
                "type": "Hợp chất",
                "formula": "H-O-H",
                "bonding": "2 cặp electron dùng chung (Cộng hóa trị)",
                "mol_mass": "18 amu"
            },
            {
                "molecule": "Methane (CH4)",
                "type": "Hợp chất",
                "formula": "CH4",
                "bonding": "4 cặp electron dùng chung (Cộng hóa trị)",
                "mol_mass": "16 amu"
            },
            {
                "molecule": "Carbon dioxide (CO2)",
                "type": "Hợp chất",
                "formula": "O=C=O",
                "bonding": "4 cặp electron dùng chung (2 liên kết đôi)",
                "mol_mass": "44 amu"
            },
            {
                "molecule": "Sodium chloride (NaCl)",
                "type": "Hợp chất ion",
                "formula": "Na+ Cl-",
                "bonding": "Lực hút tĩnh điện giữa ion Na+ và Cl-",
                "mol_mass": "58,5 amu"
            }
        ],
        "practice_questions": [
            {
                "question": "Trong phân tử nước (H2O), liên kết giữa nguyên tử oxygen và các nguyên tử hydrogen là loại liên kết gì?",
                "options": [
                    "Liên kết ion",
                    "Liên kết cộng hóa trị",
                    "Liên kết kim loại",
                    "Liên kết hydro"
                ],
                "answer_index": 1,
                "explanation": "Trong phân tử H2O, nguyên tử O góp chung với mỗi nguyên tử H một cặp electron để tạo nên liên kết cộng hóa trị."
            },
            {
                "question": "Hai nguyên tử oxygen (O) trong phân tử khí oxygen (O2) liên kết với nhau bằng bao nhiêu cặp electron dùng chung?",
                "options": [
                    "1 cặp electron",
                    "2 cặp electron",
                    "3 cặp electron",
                    "4 cặp electron"
                ],
                "answer_index": 1,
                "explanation": "Mỗi nguyên tử O có 6 electron lớp ngoài cùng, cần thêm 2 electron nên hai nguyên tử O góp chung 2 cặp electron hình thành liên kết đôi O=O."
            },
            {
                "question": "Khối lượng phân tử của khí Carbon dioxide (CO2) biết C = 12 amu, O = 16 amu là:",
                "options": [
                    "28 amu",
                    "32 amu",
                    "44 amu",
                    "56 amu"
                ],
                "answer_index": 2,
                "explanation": "Khối lượng phân tử CO2 = 1 x 12 + 2 x 16 = 44 amu."
            }
        ]
    },
    {
        "id": "k8-che-thang-do-ph",
        "grade": 8,
        "subject": "chemistry",
        "subject_label": "Hóa học",
        "title": "Thang đo pH và nhận biết môi trường bằng chất chỉ thị",
        "lesson_ref": "KHTN 8 · Bài 9: Base - Thang pH",
        "topic": "Dung dịch Acid - Base và Thang pH",
        "duration_minutes": 35,
        "difficulty": "Cơ bản",
        "badge": "🧪 Hóa học 8",
        "summary": "Sử dụng giấy quỳ tím và giấy chỉ thị pH vạn năng để xác định tính acid, base hoặc trung tính của các dung dịch quen thuộc.",
        "simulation_type": "ph_indicator",
        "default_params": {
            "selected_sample": "lemon_juice",
            "indicator": "litmus"
        },
        "safety_notes": [
            "Không nếm hoặc chạm tay trực tiếp vào các hóa chất thí nghiệm (đặc biệt dung dịch vôi trong, xà phòng).",
            "Nếu hóa chất bắn vào da, rửa ngay dưới vòi nước sạch nhiều lần."
        ],
        "equipment": [
            "Hộp giấy quỳ tím và bảng màu chuẩn giấy chỉ thị pH vạn năng (thang 1 - 14)",
            "Ống nhỏ giọt, đĩa sứ thủy tinh (giá đựng ống nghiệm)",
            "Các mẫu thử: Nước cốt chanh, Giấm ăn, Nước cất, Nước xà phòng, Dung dịch nước vôi trong Ca(OH)2, Dung dịch baking soda (NaHCO3)"
        ],
        "procedure_steps": [
            "Bước 1: Cắt nhỏ giấy chỉ thị pH và giấy quỳ tím đặt lên mặt kính đồng hồ sạch.",
            "Bước 2: Dùng ống hút nhỏ giọt lấy từng mẫu thử nhỏ 1 - 2 giọt lên mẩu giấy chỉ thị.",
            "Bước 3: Quan sát sự đổi màu của giấy chỉ thị ngay sau khi nhỏ giọt.",
            "Bước 4: So sánh màu của giấy chỉ thị với bảng màu thang pH chuẩn để đọc giá trị pH tương ứng.",
            "Bước 5: Phân loại dung dịch theo môi trường: pH < 7 (môi trường acid), pH = 7 (môi trường trung tính), pH > 7 (môi trường base)."
        ],
        "expected_phenomenon": "Nước cốt chanh và giấm làm quỳ tím hóa đỏ (pH ~ 2 - 3); Nước cất quỳ tím không đổi màu (pH = 7); Nước vôi trong, xà phòng và baking soda làm quỳ tím hóa xanh đậm (pH ~ 8 - 12).",
        "scientific_explanation": "Độ pH là chỉ số biểu thị nồng độ ion H+ trong dung dịch. Dung dịch acid có nồng độ H+ cao (pH < 7), dung dịch base có nồng độ OH- cao (pH > 7), nước tinh khiết trung tính có pH = 7. Chất chỉ thị màu đổi màu theo cấu trúc hóa học phụ thuộc vào môi trường ion của dung dịch.",
        "formula": "pH < 7: Môi trường Acid | pH = 7: Môi trường Trung tính | pH > 7: Môi trường Base",
        "sample_data": [
            {
                "sample": "Nước cốt chanh",
                "litmus_color": "Hóa đỏ",
                "ph_value": "2,5",
                "environment": "Acid"
            },
            {
                "sample": "Giấm ăn",
                "litmus_color": "Hóa đỏ nhạt",
                "ph_value": "3,0",
                "environment": "Acid"
            },
            {
                "sample": "Nước tinh khiết",
                "litmus_color": "Không đổi màu",
                "ph_value": "7,0",
                "environment": "Trung tính"
            },
            {
                "sample": "Baking soda",
                "litmus_color": "Hóa xanh nhạt",
                "ph_value": "8,5",
                "environment": "Base"
            },
            {
                "sample": "Nước vôi trong",
                "litmus_color": "Hóa xanh đậm",
                "ph_value": "11,5",
                "environment": "Base"
            }
        ],
        "practice_questions": [
            {
                "question": "Dung dịch có pH = 4 làm quỳ tím chuyển sang màu gì và thuộc môi trường nào?",
                "options": [
                    "Màu đỏ, môi trường acid",
                    "Màu xanh, môi trường base",
                    "Màu tím, môi trường trung tính",
                    "Màu vàng, môi trường muối"
                ],
                "answer_index": 0,
                "explanation": "Dung dịch có pH < 7 có môi trường acid và làm quỳ tím chuyển sang màu đỏ."
            },
            {
                "question": "Dung dịch nào sau đây có giá trị pH lớn hơn 7?",
                "options": [
                    "Nước cam ép",
                    "Dung dịch NaOH",
                    "Dung dịch HCl",
                    "Nước mưa chua"
                ],
                "answer_index": 1,
                "explanation": "NaOH là một dung dịch kiềm (base) mạnh, có pH > 7 (thường khoảng 12 - 14)."
            }
        ]
    },
    {
        "id": "k8-che-kim-loai-acid",
        "grade": 8,
        "subject": "chemistry",
        "subject_label": "Hóa học",
        "title": "Phản ứng của Kim loại với Acid sinh khí Hydrogen",
        "lesson_ref": "KHTN 8 · Bài 8: Acid",
        "topic": "Tính chất hóa học của Acid",
        "duration_minutes": 40,
        "difficulty": "Thông hiểu",
        "badge": "🧪 Hóa học 8",
        "summary": "Khảo sát phản ứng giữa các kim loại khác nhau (Kẽm, Sắt, Đồng) với dung dịch hydrochloric acid (HCl).",
        "simulation_type": "metal_acid",
        "default_params": {
            "metal": "Zn",
            "acid": "HCl",
            "acid_concentration": "1M"
        },
        "safety_notes": [
            "Dung dịch acid HCl có tính ăn mòn, tuyệt đối không để rớt vào da hoặc quần áo.",
            "Khí Hydrogen (H2) sinh ra dễ cháy nổ khi trộn lẫn với oxy không khí, thử que đóm cách xa bình hóa chất."
        ],
        "equipment": [
            "3 ống nghiệm sạch gắn trên giá đỡ",
            "Ống nhỏ giọt, kẹp gỗ gắp ống nghiệm",
            "Các mẫu kim loại: Hạt kẽm (Zn), mạt sắt (Fe), phoi đồng (Cu)",
            "Dung dịch hydrochloric acid (HCl 1M - 2M)",
            "Que đóm, bật lửa để thử khí"
        ],
        "procedure_steps": [
            "Bước 1: Đánh số 3 ống nghiệm (1, 2, 3). Cho vào ống 1 một hạt kẽm (Zn), ống 2 một ít mạt sắt (Fe), ống 3 một mẩu đồng (Cu).",
            "Bước 2: Dùng ống nhỏ giọt lấy khoảng 2 - 3ml dung dịch HCl rót vào từng ống nghiệm.",
            "Bước 3: Quan sát hiện tượng bề mặt kim loại, tốc độ bọt khí thoát ra và nhiệt độ thành ống nghiệm.",
            "Bước 4: Đưa que đóm đang cháy lại gần miệng ống nghiệm số 1 (chứa Zn + HCl) để thử khí thoát ra.",
            "Bước 5: So sánh mức độ phản ứng của 3 kim loại và viết phương trình hóa học."
        ],
        "expected_phenomenon": "Ống 1 (Zn): Kẽm tan dần, bọt khí không màu thoát ra nhanh và mạnh, dung dịch ấm lên; thử que đóm có tiếng nổ 'pốp' êm tai đặc trưng của khí H2. Ống 2 (Fe): Sắt tan chậm hơn, bọt khí thoát ra từ từ, dung dịch chuyển dần sang xanh nhạt (FeCl2). Ống 3 (Cu): Không có hiện tượng gì, mẩu đồng vẫn giữ nguyên màu đỏ, không có bọt khí.",
        "scientific_explanation": "Kẽm và Sắt đứng trước Hydrogen trong dãy hoạt động hóa học nên tác dụng được với dung dịch acid HCl giải phóng khí H2 và tạo muối clorua. Đồng đứng sau Hydrogen nên không phản ứng với dung dịch HCl loãng.",
        "formula": "Zn + 2HCl → ZnCl2 + H2↑ | Fe + 2HCl → FeCl2 + H2↑",
        "sample_data": [
            {
                "metal": "Kẽm (Zn)",
                "reaction_rate": "Nhanh, sủi bọt mạnh",
                "gas_test": "Que đóm nổ 'pốp', cháy ngọn lửa xanh nhạt",
                "conclusion": "Zn hoạt động mạnh hơn H"
            },
            {
                "metal": "Sắt (Fe)",
                "reaction_rate": "Trung bình, bọt khí đều",
                "gas_test": "Có khí H2 thoát ra",
                "conclusion": "Fe đứng trước H"
            },
            {
                "metal": "Đồng (Cu)",
                "reaction_rate": "Không sủi bọt, không tan",
                "gas_test": "Không có khí",
                "conclusion": "Cu đứng sau H, không phản ứng"
            }
        ],
        "practice_questions": [
            {
                "question": "Kim loại nào sau đây KHÔNG tác dụng với dung dịch hydrochloric acid (HCl) giải phóng khí H2?",
                "options": [
                    "Al",
                    "Fe",
                    "Cu",
                    "Mg"
                ],
                "answer_index": 2,
                "explanation": "Đồng (Cu) đứng sau hydrogen trong dãy hoạt động hóa học nên không tác dụng với dung dịch HCl loãng."
            },
            {
                "question": "Khi cho 6,5 gam kẽm (Zn = 65) phản ứng hoàn toàn với dung dịch HCl dư, thể tích khí H2 (đktc) thu được là:",
                "options": [
                    "1,12 lít",
                    "2,24 lít",
                    "3,36 lít",
                    "4,48 lít"
                ],
                "answer_index": 1,
                "explanation": "n_Zn = 6,5 / 65 = 0,1 mol. Phương trình: Zn + 2HCl -> ZnCl2 + H2. n_H2 = n_Zn = 0,1 mol. V_H2 = 0,1 x 22,4 = 2,24 lít (hoặc 2,479 lít ở đkc chuẩn mới)."
            }
        ],
        "lesson_id": "k8-bai-8-acid"
    },
    {
        "id": "k8-che-trung-hoa-acid-base",
        "grade": 8,
        "subject": "chemistry",
        "subject_label": "Hóa học",
        "title": "Phản ứng trung hòa giữa Acid và Base",
        "lesson_ref": "KHTN 8 · Bài 9 & 11: Base và Muối (Phản ứng trung hòa)",
        "topic": "Phản ứng trung hòa Acid - Base",
        "duration_minutes": 40,
        "difficulty": "Thông hiểu",
        "badge": "🧪 Hóa học 8",
        "summary": "Thực hiện phản ứng trung hòa giữa dung dịch acid HCl và dung dịch base NaOH có dùng chỉ thị phenolphthalein.",
        "simulation_type": "acid_base_neutralization",
        "default_params": {
            "hcl_volume_ml": 20,
            "naoh_added_ml": 0,
            "indicator": "phenolphthalein"
        },
        "safety_notes": [
            "NaOH đặc có tính ăn mòn da rất mạnh, sử dụng găng tay bảo hộ.",
            "Không để hóa chất vương vãi ra bàn cân hoặc quần áo."
        ],
        "equipment": [
            "Buret 25ml kẹp trên giá sắt thẳng đứng",
            "Bình tam giác 100ml (Erlenmeyer flask)",
            "Dung dịch sodium hydroxide NaOH 0,1M",
            "Dung dịch hydrochloric acid HCl 0,1M",
            "Dung dịch chỉ thị màu phenolphthalein 0,1%"
        ],
        "procedure_steps": [
            "Bước 1: Rót dung dịch NaOH 0,1M vào buret, điều chỉnh van để mức dung dịch chạm vạch 0.",
            "Bước 2: Lấy chính xác 10ml dung dịch HCl 0,1M vào bình tam giác, nhỏ thêm 1 - 2 giọt dung dịch phenolphthalein (dung dịch trong suốt không màu).",
            "Bước 3: Mở nhẹ khóa buret, cho từng giọt NaOH rơi vào bình tam giác, tay vừa lắc đều bình.",
            "Bước 4: Quan sát màu sắc dung dịch. Khi dung dịch xuất hiện màu hồng nhạt bền vững trong khoảng 30 giây thì khóa van buret.",
            "Bước 5: Đọc thể tích NaOH đã dùng trên buret và xác định điểm tương đương."
        ],
        "expected_phenomenon": "Ban đầu dung dịch trong bình tam giác chứa HCl và phenolphthalein không có màu. Khi nhỏ giọt NaOH vào và lắc đều, màu hồng thoáng hiện rồi biến mất. Khi phản ứng trung hòa vừa kết thúc (điểm tương đương, pH = 7), chỉ cần thêm nửa giọt NaOH dư, toàn bộ dung dịch chuyển sang màu hồng nhạt bền vững.",
        "scientific_explanation": "Phản ứng giữa dung dịch acid (HCl) và dung dịch base (NaOH) là phản ứng trung hòa, tạo thành muối (NaCl) và nước (H2O). Phenolphthalein không màu trong môi trường acid và trung tính, nhưng chuyển sang màu hồng tím khi dung dịch có tính base (pH > 8,3).",
        "formula": "HCl + NaOH → NaCl + H2O (ΔH < 0, phản ứng tỏa nhiệt)",
        "sample_data": [
            {
                "V_HCl": "10,0 ml",
                "V_NaOH_used": "10,1 ml",
                "color_before": "Không màu",
                "color_after": "Hồng nhạt bền",
                "pH_endpoint": "7,0 - 8,2"
            }
        ],
        "practice_questions": [
            {
                "question": "Sản phẩm của phản ứng trung hòa giữa dung dịch acid và dung dịch base luôn gồm có:",
                "options": [
                    "Muối và nước",
                    "Muối và khí hydrogen",
                    "Kim loại và nước",
                    "Oxide base và acid"
                ],
                "answer_index": 0,
                "explanation": "Phản ứng trung hòa: Acid + Base -> Muối + Nước."
            },
            {
                "question": "Chất chỉ thị phenolphthalein chuyển sang màu gì khi tiếp xúc với môi trường kiềm (base)?",
                "options": [
                    "Màu xanh lam",
                    "Màu hồng / đỏ tím",
                    "Màu vàng cam",
                    "Không đổi màu"
                ],
                "answer_index": 1,
                "explanation": "Phenolphthalein không màu trong acid và trung tính, chuyển sang màu hồng hoặc đỏ tím trong môi trường kiềm (base)."
            }
        ],
        "lesson_id": "k8-bai-11-muoi"
    },
    {
        "id": "k9-che-day-hoat-dong-kim-loai",
        "grade": 9,
        "subject": "chemistry",
        "subject_label": "Hóa học",
        "title": "Dãy hoạt động hóa học của Kim loại (Fe tác dụng CuSO4)",
        "lesson_ref": "KHTN 9 · Bài 19: Dãy hoạt động hoá học",
        "topic": "Tính chất hóa học của Kim loại",
        "duration_minutes": 40,
        "difficulty": "Thông hiểu",
        "badge": "🧪 Hóa học 9",
        "summary": "Khảo sát phản ứng của sắt (Fe) với dung dịch copper(II) sulfate (CuSO4) để kiểm chứng quy luật kim loại hoạt động mạnh đẩy kim loại yếu hơn ra khỏi muối.",
        "simulation_type": "metal_displacement",
        "default_params": {
            "metal": "Fe",
            "solution": "CuSO4",
            "time_elapsed_min": 10
        },
        "safety_notes": [
            "Muối đồng CuSO4 có tính độc đối với thủy sinh, không đổ trực tiếp ra cống rãnh.",
            "Dùng kẹp gắp đinh sắt, lau khô tay sau khi thao tác."
        ],
        "equipment": [
            "Đinh sắt (Fe) sạch gỉ, đã đánh bóng bằng giấy nhám",
            "Dung dịch copper(II) sulfate (CuSO4 0,5M) màu xanh lam",
            "Ống nghiệm to hoặc cốc thủy tinh 50ml",
            "Dây chỉ buộc đinh sắt và kẹp thí nghiệm"
        ],
        "procedure_steps": [
            "Bước 1: Rót khoảng 5ml dung dịch CuSO4 màu xanh lam vào ống nghiệm.",
            "Bước 2: Buộc chỉ vào một chiếc đinh sắt đã được cạo sạch gỉ, thả từ từ vào ống nghiệm sao cho đinh ngập một phần trong dung dịch.",
            "Bước 3: Để yên ống nghiệm trong khoảng 5 - 10 phút, quan sát màu sắc trên bề mặt đinh sắt.",
            "Bước 4: Nhấc nhẹ đinh sắt ra, quan sát lớp kim loại bám ngoài đinh và màu sắc của dung dịch trong ống nghiệm.",
            "Bước 5: Viết phương trình hóa học và rút ra kết luận về tính khử của Fe so với Cu."
        ],
        "expected_phenomenon": "Có một lớp kim loại màu đỏ gạch (đồng Cu) bám ngoài phần đinh sắt nhúng trong dung dịch. Màu xanh lam của dung dịch CuSO4 nhạt dần, chuyển sang màu xanh lục rất nhạt của dung dịch muối sắt(II) sulfate (FeSO4).",
        "scientific_explanation": "Trong dãy hoạt động hóa học của kim loại, sắt (Fe) đứng trước đồng (Cu) nên có tính kim loại (tính khử) mạnh hơn đồng. Sắt đã khử ion Cu2+ trong dung dịch thành kim loại Cu tự do bám vào đinh, đồng thời Fe bị oxi hóa thành ion Fe2+ tan vào dung dịch.",
        "formula": "Fe + CuSO4 → FeSO4 + Cu↓ (Đỏ gạch bám ngoài)",
        "sample_data": [
            {
                "time": "0 phút",
                "nail_surface": "Kim loại màu xám sáng bóng",
                "solution_color": "Màu xanh lam đặc trưng"
            },
            {
                "time": "5 phút",
                "nail_surface": "Lớp đồng đỏ bắt đầu xuất hiện",
                "solution_color": "Màu xanh lam nhạt bớt"
            },
            {
                "time": "15 phút",
                "nail_surface": "Lớp đồng đỏ bao phủ dày",
                "solution_color": "Xanh lam nhạt chuyển dần sang lục nhạt"
            }
        ],
        "practice_questions": [
            {
                "question": "Khi ngâm một lá kẽm (Zn) vào dung dịch CuSO4 màu xanh, hiện tượng quan sát được là gì?",
                "options": [
                    "Không có hiện tượng gì xảy ra",
                    "Lớp kim loại màu đỏ bám trên lá kẽm, màu xanh dung dịch nhạt dần",
                    "Có bọt khí không màu thoát ra mãnh liệt",
                    "Dung dịch chuyển sang màu đỏ đậm"
                ],
                "answer_index": 1,
                "explanation": "Kẽm hoạt động mạnh hơn đồng nên đẩy đồng ra khỏi muối: Zn + CuSO4 -> ZnSO4 + Cu (đồng màu đỏ bám trên lá kẽm, dung dịch nhạt màu dần)."
            },
            {
                "question": "Cặp chất nào sau đây KHÔNG xảy ra phản ứng hóa học?",
                "options": [
                    "Fe + dung dịch CuSO4",
                    "Cu + dung dịch AgNO3",
                    "Cu + dung dịch FeSO4",
                    "Al + dung dịch CuCl2"
                ],
                "answer_index": 2,
                "explanation": "Đồng (Cu) đứng sau sắt (Fe) trong dãy hoạt động hóa học nên Cu không thể đẩy Fe ra khỏi dung dịch muối FeSO4."
            }
        ],
        "lesson_id": "k9-bai-19-day-hoat-dong-hoa-hoc"
    },
    {
        "id": "k6-phy-luc-ma-sat",
        "grade": 6,
        "subject": "physics",
        "subject_label": "Vật lý",
        "title": "Khảo sát Lực Ma sát Trượt và Lực Ma sát Lăn trên các Bề mặt",
        "lesson_ref": "KHTN 6 · Bài 44: Lực ma sát",
        "topic": "Lực và Chuyển động",
        "duration_minutes": 35,
        "difficulty": "Cơ bản",
        "badge": "⚡ Vật lý 6",
        "summary": "Khảo sát độ lớn của lực ma sát tác dụng lên khối gỗ khi trượt hoặc lăn trên các bề mặt khác nhau (gỗ nhẵn, giấy nhám ráp, và đặt trên các con lăn) bằng lực kế lò xo.",
        "simulation_type": "friction_force",
        "default_params": {
            "mass_g": 200,
            "surface": "wood",
            "rolling": False,
            "speed": 1.0
        },
        "safety_notes": [
            "Kéo lực kế từ từ theo phương nằm ngang song song với mặt bàn.",
            "Đọc số chỉ của lực kế khi khối gỗ vừa chuyển động thẳng đều ổn định."
        ],
        "equipment": [
            "Lực kế lò xo giới hạn đo 5N, độ chia nhỏ nhất 0,1N",
            "Khối gỗ hình hộp chữ nhật có gắn móc kéo (khối lượng 200g)",
            "Các bề mặt thí nghiệm: Bàn gỗ phẳng nhẵn, tấm giấy ráp (nhám), mặt bàn có rải con lăn/bi lăn",
            "Bộ quả nặng gia tải (50g, 100g)"
        ],
        "procedure_steps": [
            "Bước 1: Đặt khối gỗ (200g) nằm trên mặt bàn gỗ nhẵn. Móc lực kế vào khối gỗ.",
            "Bước 2: Kéo lực kế từ từ theo phương ngang sao cho khối gỗ chuyển động thẳng đều. Đọc số chỉ lực kế F_ms1 (đây chính là độ lớn lực ma sát trượt trên mặt gỗ).",
            "Bước 3: Lặp lại thí nghiệm với mặt giấy ráp (giấy nhám), ghi lại số chỉ lực kế F_ms2.",
            "Bước 4: Đặt các con lăn hình trụ tròn dưới khối gỗ, kéo chuyển động thẳng đều và ghi số chỉ lực kế F_ms3 (lực ma sát lăn).",
            "Bước 5: Đặt thêm quả nặng lên khối gỗ (tăng áp lực N) và quan sát sự thay đổi độ lớn của lực ma sát."
        ],
        "expected_phenomenon": "Số chỉ của lực kế lớn nhất khi kéo khối gỗ trên mặt giấy ráp (ma sát trượt nhám > ma sát trượt nhẵn). Khi đặt trên các con lăn, số chỉ lực kế giảm đi rất nhiều (lực ma sát lăn nhỏ hơn ma sát trượt hàng chục lần). Khi tăng khối lượng quả nặng, lực ma sát tăng theo.",
        "scientific_explanation": "Lực ma sát trượt xuất hiện ở mặt tiếp xúc cản trở chuyển động trượt của vật. Độ lớn F_ms phụ thuộc vào bản chất và tình trạng bề mặt tiếp xúc (càng gồ ghề ráp thì ma sát càng lớn) và tỉ lệ thuận với áp lực N vuông góc với bề mặt. Lực ma sát lăn nhỏ hơn rất nhiều so với lực ma sát trượt cùng điều kiện, do đó việc sử dụng ổ bi hay con lăn giúp giảm đáng kể lực cản.",
        "formula": "F_ms = μ · N = μ · P = μ · (m · g)  (μ_lăn ≪ μ_trượt)",
        "sample_data": [
            {
                "surface": "Mặt gỗ phẳng nhẵn",
                "mass": "200g",
                "type": "Ma sát trượt",
                "force_N": "0.6 N"
            },
            {
                "surface": "Mặt giấy ráp (nhám)",
                "mass": "200g",
                "type": "Ma sát trượt",
                "force_N": "1.4 N"
            },
            {
                "surface": "Mặt gỗ có con lăn",
                "mass": "200g",
                "type": "Ma sát lăn",
                "force_N": "0.08 N"
            },
            {
                "surface": "Mặt gỗ nhẵn + quả cân 200g",
                "mass": "400g",
                "type": "Ma sát trượt",
                "force_N": "1.2 N"
            }
        ],
        "practice_questions": [
            {
                "question": "Để giảm lực ma sát có hại trong trục quay của quạt điện, máy móc, người ta thường áp dụng biện pháp nào?",
                "options": [
                    "Làm tăng độ nhám bề mặt",
                    "Lắp thêm ổ bi (con lăn) và tra dầu mỡ bôi trơn",
                    "Tăng tải trọng đè lên trục quay",
                    "Dùng dây cao su kéo chặt"
                ],
                "answer_index": 1,
                "explanation": "Lắp thêm ổ bi giúp biến ma sát trượt thành ma sát lăn (giảm ma sát nhiều chục lần), kết hợp dầu mỡ bôi trơn làm giảm đáng kể hao mòn và cản trở chuyển động."
            },
            {
                "question": "Lực ma sát trượt phụ thuộc vào yếu tố nào sau đây?",
                "options": [
                    "Diện tích bề mặt tiếp xúc",
                    "Tốc độ chuyển động của vật",
                    "Tình trạng bề mặt tiếp xúc và độ lớn của áp lực",
                    "Hình dạng khối vật"
                ],
                "answer_index": 2,
                "explanation": "Độ lớn lực ma sát trượt không phụ thuộc diện tích tiếp xúc mà chỉ phụ thuộc vào tính chất (độ gồ ghề, vật liệu) của bề mặt và áp lực vuông góc N tác dụng lên bề mặt."
            }
        ],
        "lesson_id": "k6-bai-44-luc-ma-sat"
    },
    {
        "id": "k7-phy-tu-truong-nam-cham",
        "grade": 7,
        "subject": "physics",
        "subject_label": "Vật lý",
        "title": "Khảo sát Từ trường của Nam châm & Từ phổ Mạt sắt",
        "lesson_ref": "KHTN 7 · Bài 19: Từ trường",
        "topic": "Từ trường và Nam châm",
        "duration_minutes": 40,
        "difficulty": "Cơ bản",
        "badge": "⚡ Vật lý 7",
        "summary": "Quan sát hình ảnh đường sức từ (từ phổ) tạo bởi mạt sắt xung quanh nam châm thẳng và sự định hướng theo quy tắc 'Vào cực Nam - Ra cực Bắc' của kim la bàn mini.",
        "simulation_type": "magnetic_field",
        "default_params": {
            "magnet_type": "bar",
            "iron_filings": True,
            "compass_active": True,
            "field_strength": 1.0
        },
        "safety_notes": [
            "Không để các nam châm va đập mạnh làm giảm từ tính.",
            "Tránh để mạt sắt rơi vào mắt hoặc dính vào kẽ các thiết bị điện tử."
        ],
        "equipment": [
            "Nam châm thẳng (sơn 2 màu: cực Bắc N màu đỏ, cực Nam S màu xanh)",
            "Tấm kính trong suốt hoặc bìa nhựa phẳng đặt trên nam châm",
            "Hộp mạt sắt mịn rải đều",
            "Bộ 8 kim nam châm thử (la bàn mini) có trục quay tự do"
        ],
        "procedure_steps": [
            "Bước 1: Đặt thanh nam châm thẳng nằm ngang trên mặt bàn phẳng.",
            "Bước 2: Đặt tấm nhựa trong suốt lên phía trên nam châm. Rắc đều một lớp mạt sắt mịn lên tấm nhựa.",
            "Bước 3: Gõ nhẹ vào tấm nhựa và quan sát sự sắp xếp của mạt sắt thành các đường cong nối hai cực nam châm (hình ảnh từ phổ).",
            "Bước 4: Đặt các kim nam châm thử tại các vị trí khác nhau xung quanh thanh nam châm và quan sát hướng chỉ của cực Bắc - Nam của kim la bàn.",
            "Bước 5: Vẽ chiều của đường sức từ theo quy ước: Đi ra từ cực Bắc (N) và đi vào cực Nam (S)."
        ],
        "expected_phenomenon": "Mạt sắt sắp xếp thành các đường cong khép kín nối từ cực này sang cực kia của nam châm. Ở hai đầu cực của nam châm, các đường mạt sắt tập trung mau (dày đặc) nhất, chứng tỏ từ trường ở hai cực là mạnh nhất. Kim la bàn luôn quay định hướng dọc theo tiếp tuyến của đường sức từ: Cực Nam (S) của kim bị cực Bắc (N) của nam châm hút và ngược lại.",
        "scientific_explanation": "Không gian xung quanh nam châm có từ trường. Từ trường tác dụng lực từ lên kim nam châm đặt trong nó. Hình ảnh các đường mạt sắt xếp liền nhau gọi là từ phổ. Đường sức từ cho phép hình dung trực quan từ trường: Nơi nào từ trường mạnh thì đường sức từ mau, nơi nào từ trường yếu thì đường sức từ thưa. Chiều quy ước của đường sức từ bên ngoài nam châm: Ra cực Bắc, Vào cực Nam.",
        "formula": "Đường sức từ ngoài nam châm: Cực Bắc (North - N) ──> Cực Nam (South - S)",
        "sample_data": [
            {
                "position": "Tại hai đầu cực (N và S)",
                "field_density": "Rất mau (dày đặc)",
                "compass_direction": "Chỉ thẳng vào/ra dọc theo trục nam châm",
                "relative_strength": "Mạnh nhất"
            },
            {
                "position": "Vùng chính giữa thân nam châm",
                "field_density": "Thưa hơn",
                "compass_direction": "Song song với thân thanh nam châm",
                "relative_strength": "Trung bình"
            },
            {
                "position": "Xa nam châm (> 15cm)",
                "field_density": "Rất thưa, phân tán",
                "compass_direction": "Định hướng theo từ trường Trái Đất (Bắc - Nam địa lý)",
                "relative_strength": "Yếu"
            }
        ],
        "practice_questions": [
            {
                "question": "Quy ước về chiều của đường sức từ ở bên ngoài thanh nam châm là:",
                "options": [
                    "Đi ra từ cực Nam, đi vào cực Bắc",
                    "Đi ra từ cực Bắc, đi vào cực Nam",
                    "Đi vòng tròn xung quanh thân nam châm",
                    "Không có chiều cố định"
                ],
                "answer_index": 1,
                "explanation": "Theo quy ước quốc tế và SGK KHTN: Ở bên ngoài nam châm, đường sức từ đi ra từ cực Bắc (N) và đi vào cực Nam (S) - khẩu quyết: 'Vào Nam Ra Bắc'."
            },
            {
                "question": "Tại vị trí nào xung quanh một thanh nam châm thẳng thì từ trường có độ mạnh lớn nhất?",
                "options": [
                    "Ở chính giữa thanh nam châm",
                    "Tại hai đầu cực Bắc và cực Nam của nam châm",
                    "Ở phía trên mặt phẳng chứa nam châm",
                    "Mọi điểm có từ trường mạnh như nhau"
                ],
                "answer_index": 1,
                "explanation": "Từ trường mạnh nhất tại hai đầu cực của nam châm (nơi các đường mạt sắt tập trung dày đặc nhất) và yếu nhất ở chính giữa thân nam châm."
            }
        ]
    },
    {
        "id": "k8-phy-ap-suat-chat-long",
        "grade": 8,
        "subject": "physics",
        "subject_label": "Vật lý",
        "title": "Khảo sát Áp suất Chất lỏng theo Độ sâu & Áp kế chữ U",
        "lesson_ref": "KHTN 8 · Bài 16: Áp suất chất lỏng. Áp suất khí quyển",
        "topic": "Áp suất và Áp lực",
        "duration_minutes": 40,
        "difficulty": "Trung bình",
        "badge": "⚡ Vật lý 8",
        "summary": "Khảo sát quy luật tăng áp suất chất lỏng tỉ lệ thuận với độ sâu h (p = d · h) bằng áp kế màng cao su nối ống chữ U chứa chất lỏng màu.",
        "simulation_type": "liquid_pressure",
        "default_params": {
            "depth_cm": 15,
            "liquid_type": "water",
            "sensor_angle_deg": 0
        },
        "safety_notes": [
            "Thao tác nhúng đầu dò từ từ, tránh giật mạnh làm tràn chất lỏng màu ra khỏi ống chữ U.",
            "Kiểm tra độ kín của các khớp nối ống cao su trước khi đo."
        ],
        "equipment": [
            "Bình trụ thủy tinh chia vạch chiều sâu (0 - 40 cm) chứa nước (hoặc nước muối)",
            "Áp kế chữ U bằng thủy tinh chứa nước màu chỉ thị độ chênh lệch cột áp Δh",
            "Đầu dò cảm biến áp suất có bịt màng cao su mỏng đàn hồi nối với áp kế chữ U qua ống cao su mềm",
            "Thước đo độ sâu"
        ],
        "procedure_steps": [
            "Bước 1: Đặt bình trụ chứa nước lên bàn thí nghiệm. Kiểm tra hai nhánh ống áp kế chữ U cân bằng cùng mực chất lỏng màu (h1 = h2).",
            "Bước 2: Nhúng từ từ đầu dò cảm biến vào trong nước ở độ sâu h = 5 cm. Quan sát và ghi nhận độ chênh lệch mực chất lỏng Δh trên áp kế chữ U.",
            "Bước 3: Tiếp tục hạ sâu đầu dò xuống các mức h = 10 cm, 15 cm, 20 cm, 25 cm. Đọc và ghi lại độ chênh lệch mực nước màu Δh.",
            "Bước 4: Giữ nguyên đầu dò ở cùng độ sâu h = 15 cm, xoay màng cao su theo các hướng khác nhau (lên trên, xuống dưới, sang ngang) và quan sát Δh.",
            "Bước 5: Lặp lại thí nghiệm với dung dịch nước muối đậm đặc (trọng lượng riêng d lớn hơn) để so sánh áp suất ở cùng độ sâu."
        ],
        "expected_phenomenon": "Khi nhúng đầu dò càng xuống sâu trong nước, màng cao su bị ép lõm vào càng nhiều, làm cho cột chất lỏng ở hai nhánh áp kế chữ U chênh lệch càng lớn (Δh tăng tuyến tính theo h). Ở cùng một độ sâu, khi xoay màng cao su theo các hướng khác nhau thì độ chênh lệch Δh không đổi. Trong nước muối, độ chênh lệch Δh lớn hơn trong nước nguyên chất ở cùng độ sâu.",
        "scientific_explanation": "Chất lỏng gây ra áp suất theo mọi phương lên đáy bình, thành bình và các vật ở trong lòng nó. Ở cùng một độ sâu, áp suất chất lỏng theo mọi hướng là như nhau. Khi xuống càng sâu, độ cao cột chất lỏng phía trên càng lớn nên áp suất càng tăng theo công thức p = d · h (trong đó d là trọng lượng riêng của chất lỏng, h là độ sâu tính từ mặt thoáng).",
        "formula": "p = d · h = ρ · g · h  (Pa; N/m²)",
        "sample_data": [
            {
                "depth_h": "5 cm",
                "liquid": "Nước (d = 10000 N/m³)",
                "sensor_dir": "Hướng xuống",
                "u_tube_diff": "5.0 cm",
                "calculated_p": "500 Pa"
            },
            {
                "depth_h": "10 cm",
                "liquid": "Nước (d = 10000 N/m³)",
                "sensor_dir": "Hướng xuống",
                "u_tube_diff": "10.0 cm",
                "calculated_p": "1000 Pa"
            },
            {
                "depth_h": "15 cm",
                "liquid": "Nước (d = 10000 N/m³)",
                "sensor_dir": "Hướng xuống",
                "u_tube_diff": "15.0 cm",
                "calculated_p": "1500 Pa"
            },
            {
                "depth_h": "15 cm",
                "liquid": "Nước (d = 10000 N/m³)",
                "sensor_dir": "Xoay ngang / Hướng lên",
                "u_tube_diff": "15.0 cm",
                "calculated_p": "1500 Pa"
            },
            {
                "depth_h": "15 cm",
                "liquid": "Nước muối (d = 11000 N/m³)",
                "sensor_dir": "Hướng xuống",
                "u_tube_diff": "16.5 cm",
                "calculated_p": "1650 Pa"
            }
        ],
        "practice_questions": [
            {
                "question": "Công thức tính áp suất chất lỏng tại một điểm có độ sâu h so với mặt thoáng là gì?",
                "options": [
                    "p = F / S",
                    "p = d · h",
                    "p = d / h",
                    "p = m · g · h"
                ],
                "answer_index": 1,
                "explanation": "Công thức tính áp suất chất lỏng là p = d · h (trong đó d là trọng lượng riêng của chất lỏng đo bằng N/m³, h là độ sâu tính từ điểm xét đến mặt thoáng chất lỏng đo bằng m)."
            },
            {
                "question": "Tàu ngầm lặn càng sâu dưới lòng biển thì vỏ tàu chịu áp lực từ nước biển thay đổi như thế nào?",
                "options": [
                    "Càng tăng lên do độ sâu h tăng",
                    "Càng giảm đi do nước biển loãng hơn",
                    "Không đổi vì nước biển không nén được",
                    "Giảm về 0 khi chạm đáy biển"
                ],
                "answer_index": 0,
                "explanation": "Vì p = d · h, khi tàu ngầm lặn càng sâu (h càng lớn) thì áp suất nước biển tác dụng lên vỏ tàu càng tăng mạnh, đòi hỏi vỏ tàu phải chế tạo bằng thép hợp kim siêu bền chịu lực."
            }
        ]
    },
    {
        "id": "k9-phy-khuc-xa-anh-sang",
        "grade": 9,
        "subject": "physics",
        "subject_label": "Vật lý",
        "title": "Khảo sát Hiện tượng Khúc xạ Ánh sáng & Phản xạ Toàn phần",
        "lesson_ref": "KHTN 9 · Bài 5: Khúc xạ ánh sáng",
        "topic": "Quang học",
        "duration_minutes": 40,
        "difficulty": "Nâng cao",
        "badge": "⚡ Vật lý 9",
        "summary": "Khảo sát đường truyền của tia sáng từ không khí vào khối thủy tinh bán nguyệt (i > r) và hiện tượng phản xạ toàn phần khi tia sáng truyền ngược từ thủy tinh ra không khí với góc tới i ≥ igh.",
        "simulation_type": "light_refraction",
        "default_params": {
            "angle_i_deg": 30,
            "direction": "air_to_glass",
            "n_medium": 1.5,
            "laser_power": 1.0
        },
        "safety_notes": [
            "Tuyệt đối không nhìn trực tiếp vào chùm tia laser phát ra hoặc chiếu tia laser vào mắt bạn học."
        ],
        "equipment": [
            "Hộp nguồn sáng phát chùm tia laser hẹp đơn sắc màu đỏ hoặc xanh",
            "Bán nguyệt thủy tinh (chiết suất n = 1,5) hoặc nhựa trong suốt",
            "Đĩa tròn quang học có chia vạch góc 0° - 360° tâm trùng tâm mặt cong bán nguyệt",
            "Giá đỡ quang học"
        ],
        "procedure_steps": [
            "Bước 1: Đặt khối bán nguyệt thủy tinh lên đĩa quang học sao cho tâm cong O của khối trùng đúng tâm 0° của đĩa chia độ.",
            "Bước 2: Chiếu chùm laser từ không khí vào mặt phẳng của khối bán nguyệt tới tâm O với góc tới i = 30°. Đọc số đo góc khúc xạ r trên đĩa.",
            "Bước 3: Lần lượt thay đổi góc tới i = 45°, 60° rồi ghi lại góc khúc xạ r tương ứng. Tính tỉ số sin(i) / sin(r).",
            "Bước 4: Đổi hướng chiếu: Chiếu laser từ trong chất bán nguyệt đi qua tâm O ra ngoài không khí. Tăng dần góc tới i.",
            "Bước 5: Tìm góc tới giới hạn igh khi tia khúc xạ đi là là sát mặt phân cách (r = 90°). Khi tăng i > igh, quan sát hiện tượng chùm sáng bị phản xạ hoàn toàn trở lại khối thủy tinh (phản xạ toàn phần)."
        ],
        "expected_phenomenon": "Khi chiếu từ không khí vào thủy tinh: Tia sáng bị gãy khúc tại mặt phân cách, góc khúc xạ r luôn nhỏ hơn góc tới i (r < i). Khi tăng i thì r cũng tăng nhưng sin(i)/sin(r) = n ≈ 1,5 không đổi. Khi chiếu từ thủy tinh ra không khí: r luôn lớn hơn i. Khi góc tới đạt giá trị igh ≈ 41,8°, tia khúc xạ đi là là mặt phân cách. Khi i > igh, không còn tia khúc xạ ra không khí nữa mà toàn bộ tia sáng bị phản xạ lại vào thủy tinh (phản xạ toàn phần).",
        "scientific_explanation": "Khúc xạ ánh sáng là hiện tượng tia sáng bị đổi phương (gãy khúc) đột ngột khi truyền xiên góc qua mặt phân cách giữa hai môi trường trong suốt khác nhau. Định luật khúc xạ: Tia khúc xạ nằm trong mặt phẳng tới, sin(i)/sin(r) = n2/n1 = n21 (hằng số). Hiện tượng phản xạ toàn phần xảy ra khi: (1) Tia sáng truyền từ môi trường chiết quang hơn sang môi trường chiết quang kém (n1 > n2); (2) Góc tới i lớn hơn hoặc bằng góc giới hạn: i ≥ igh với sin(igh) = n2 / n1.",
        "formula": "Định luật Snell: n1 · sin(i) = n2 · sin(r)  |  Phản xạ toàn phần: sin(igh) = 1 / n  (khi i ≥ igh)",
        "sample_data": [
            {
                "direction": "Không khí (n1=1) -> Thủy tinh (n2=1.5)",
                "angle_i": "30°",
                "angle_r": "19.5°",
                "sin_i_div_sin_r": "1.50",
                "phenomenon": "Tia khúc xạ đi sâu vào thủy tinh (r < i)"
            },
            {
                "direction": "Không khí (n1=1) -> Thủy tinh (n2=1.5)",
                "angle_i": "60°",
                "angle_r": "35.3°",
                "sin_i_div_sin_r": "1.50",
                "phenomenon": "Góc khúc xạ r tăng theo góc tới i"
            },
            {
                "direction": "Thủy tinh (n1=1.5) -> Không khí (n2=1)",
                "angle_i": "30°",
                "angle_r": "48.6°",
                "sin_i_div_sin_r": "0.67",
                "phenomenon": "Tia khúc xạ lệch xa pháp tuyến (r > i)"
            },
            {
                "direction": "Thủy tinh (n1=1.5) -> Không khí (n2=1)",
                "angle_i": "41.8° (igh)",
                "angle_r": "90.0°",
                "sin_i_div_sin_r": "0.67",
                "phenomenon": "Tia khúc xạ đi là là sát mặt phân cách"
            },
            {
                "direction": "Thủy tinh (n1=1.5) -> Không khí (n2=1)",
                "angle_i": "55° (> igh)",
                "angle_r": "Không có",
                "sin_i_div_sin_r": "--",
                "phenomenon": "Phản xạ toàn phần 100% trong khối thủy tinh"
            }
        ],
        "practice_questions": [
            {
                "question": "Khi ánh sáng truyền xiên góc từ không khí vào nước (nước có chiết suất n = 4/3), mối quan hệ giữa góc tới i và góc khúc xạ r là gì?",
                "options": [
                    "r > i",
                    "r < i",
                    "r = i",
                    "r + i = 90°"
                ],
                "answer_index": 1,
                "explanation": "Vì nước chiết quang hơn không khí (n2 > n1), nên sin(r) = sin(i) / n < sin(i), do đó góc khúc xạ r luôn nhỏ hơn góc tới i."
            },
            {
                "question": "Điều kiện để xảy ra hiện tượng phản xạ toàn phần là gì?",
                "options": [
                    "Tia sáng truyền từ môi trường chiết quang kém sang môi trường chiết quang hơn",
                    "Tia sáng truyền từ môi trường chiết quang hơn sang môi trường chiết quang kém và góc tới i ≥ igh",
                    "Ánh sáng chiếu vuông góc với mặt phân cách",
                    "Góc tới i phải luôn nhỏ hơn 30°"
                ],
                "answer_index": 1,
                "explanation": "Phản xạ toàn phần chỉ xảy ra khi ánh sáng truyền từ môi trường chiết quang hơn sang môi trường chiết quang kém (n1 > n2) và góc tới i phải lớn hơn hoặc bằng góc tới giới hạn: i ≥ igh (với sin igh = n2/n1)."
            }
        ]
    },
    {
        "id": "k6-che-thanh-phan-khong-khi",
        "grade": 6,
        "subject": "chemistry",
        "subject_label": "Hóa học",
        "title": "Xác định Tỉ lệ Thể tích Khí Oxygen trong Không khí",
        "lesson_ref": "KHTN 6 · Bài 11: Oxygen. Không khí",
        "topic": "Không khí và Khí quyển",
        "duration_minutes": 35,
        "difficulty": "Cơ bản",
        "badge": "🧪 Hóa học 6",
        "summary": "Xác định phần trăm thể tích của khí oxygen chiếm trong không khí (khoảng 1/5 hay 21%) bằng cách đốt cháy ngọn nến hoặc phốt pho trong ống đong thủy tinh úp ngược trên chậu nước màu.",
        "simulation_type": "air_oxygen_fraction",
        "default_params": {
            "cylinder_volume_ml": 100,
            "burning_time_s": 15,
            "is_capped": True
        },
        "safety_notes": [
            "Cẩn thận khi châm lửa đốt nến, không chạm tay vào sáp nóng chảy.",
            "Úp ống đong nhanh chóng, thẳng đứng và ngập mép ống trong nước để tránh khí thoát ra ngoài."
        ],
        "equipment": [
            "Ống đong chia vạch thủy tinh (dung tích 100ml chia đều 5 phần bằng nhau)",
            "Chậu thủy tinh chứa nước pha màu thực phẩm (để dễ quan sát mực nước dâng)",
            "Ngọn nến nhỏ (hoặc muỗng sắt chứa phốt pho đỏ P)",
            "Bật lửa hoặc diêm quẹt",
            "Thước đo chia vạch"
        ],
        "procedure_steps": [
            "Bước 1: Chia chiều cao cột không khí trong ống đong thành 5 phần bằng nhau (đánh dấu từ vạch 0 đến vạch 5).",
            "Bước 2: Đặt ngọn nến nhỏ vào đĩa hoặc đế nổi trên chậu nước màu rồi châm nến cháy sáng đều.",
            "Bước 3: Lấy ống đong thủy tinh úp nhanh chụp lên ngọn nến sao cho miệng ống ngập trong nước.",
            "Bước 4: Quan sát ngọn nến cháy yếu dần rồi tắt hẳn, đồng thời quan sát mực nước trong ống đong dâng lên.",
            "Bước 5: Chờ cho không khí trong ống nguội hẳn về nhiệt độ phòng, đọc vạch mực nước dâng lên và tính phần trăm thể tích khí đã phản ứng."
        ],
        "expected_phenomenon": "Sau khi úp ống đong, ngọn nến tiếp tục cháy trong vài giây rồi lụi dần và tắt hẳn. Mực nước màu trong chậu dâng lên chiếm đúng khoảng 1 vạch (tương ứng 1/5 thể tích ống đong, khoảng 20% - 21%). 4/5 thể tích còn lại trong ống là chất khí không duy trì sự cháy (chủ yếu là khí Nitrogen).",
        "scientific_explanation": "Khí oxygen là chất khí duy trì sự cháy. Khi úp ống đong kín, ngọn nến cháy đã tiêu thụ hết toàn bộ lượng khí oxygen có trong ống để biến thành CO2 và nước (CO2 tan một phần và hơi nước ngưng tụ). Áp suất khí bên trong ống giảm xuống, làm cho áp suất khí quyển bên ngoài ép nước dâng lên chiếm chỗ lượng oxygen đã mất. Thể tích nước dâng lên đúng bằng thể tích khí oxygen đã tham gia phản ứng, chiếm xấp xỉ 1/5 thể tích không khí (khoảng 21%).",
        "formula": "% V_O2 = (V_nước dâng / V_không khí ban đầu) · 100% ≈ 21% (~ 1/5 thể tích)",
        "sample_data": [
            {
                "stage": "Trước khi úp ống",
                "flame_state": "Nến cháy sáng bình thường",
                "water_level_in_tube": "Vạch 0 (Mép miệng ống)",
                "oxygen_percent": "21% (Không khí tự nhiên)"
            },
            {
                "stage": "Sau khi úp 5 giây",
                "flame_state": "Lửa lụi dần, có khói",
                "water_level_in_tube": "Bắt đầu dâng lên",
                "oxygen_percent": "Khoảng 8% - 12%"
            },
            {
                "stage": "Sau khi nến tắt hoàn toàn và nguội",
                "flame_state": "Tắt hẳn",
                "water_level_in_tube": "Dâng lên vạch 1 (chiếm đúng 1/5 thể tích)",
                "oxygen_percent": "0% (Đã tiêu thụ hết O2)"
            }
        ],
        "practice_questions": [
            {
                "question": "Trong không khí, khí oxygen chiếm khoảng bao nhiêu phần trăm về thể tích?",
                "options": [
                    "Khoảng 78%",
                    "Khoảng 21% (gần 1/5 thể tích)",
                    "Khoảng 50%",
                    "Khoảng 1%"
                ],
                "answer_index": 1,
                "explanation": "Thành phần không khí gồm khoảng 78% Nitrogen, khoảng 21% Oxygen về thể tích, còn lại 1% là khí hiếm Argon, CO2 và hơi nước."
            },
            {
                "question": "Khí chiếm tỉ lệ thể tích lớn nhất trong không khí (khoảng 78%) và không duy trì sự cháy là khí nào?",
                "options": [
                    "Khí Carbon dioxide (CO2)",
                    "Khí Oxygen (O2)",
                    "Khí Nitrogen (N2)",
                    "Khí Hydrogen (H2)"
                ],
                "answer_index": 2,
                "explanation": "Khí Nitrogen (N2) trơ ở nhiệt độ thường, chiếm khoảng 78% thể tích không khí, không duy trì sự cháy và sự sống."
            }
        ],
        "lesson_id": "k6-bai-11-oxygen-khong-khi"
    },
    {
        "id": "k7-che-cau-tao-nguyen-tu",
        "grade": 7,
        "subject": "chemistry",
        "subject_label": "Hóa học",
        "title": "Khảo sát Cấu tạo Nguyên tử theo Mô hình Bohr & Các Lớp Electron",
        "lesson_ref": "KHTN 7 · Bài 2: Nguyên tử",
        "topic": "Chất và Biến đổi của chất",
        "duration_minutes": 40,
        "difficulty": "Cơ bản",
        "badge": "🧪 Hóa học 7",
        "summary": "Mô phỏng cấu tạo nguyên tử Rutherford - Bohr với hạt nhân (proton, neutron) mang điện tích dương và các electron chuyển động trên các lớp quỹ đạo đồng tâm cho 20 nguyên tố đầu tiên của Bảng tuần hoàn.",
        "simulation_type": "atomic_structure",
        "default_params": {
            "element_symbol": "Na",
            "atomic_number": 11,
            "show_orbitals": True,
            "animate_motion": True
        },
        "safety_notes": [
            "Ghi nhớ quy tắc số electron tối đa: Lớp 1 chứa tối đa 2e, Lớp 2 chứa tối đa 8e, Lớp 3 chứa tối đa 8e (đối với các nguyên tố từ Z=1 đến 20)."
        ],
        "equipment": [
            "Mô hình 3D tương tác cấu tạo nguyên tử Rutherford - Bohr",
            "Bảng tuần hoàn các nguyên tố hóa học",
            "Bảng tra cứu số proton, neutron và cấu hình electron của 20 nguyên tố đầu"
        ],
        "procedure_steps": [
            "Bước 1: Chọn một nguyên tố trong bảng chọn (ví dụ: Hydrogen H (Z=1), Carbon C (Z=6), Oxygen O (Z=8), Sodium Na (Z=11)).",
            "Bước 2: Quan sát hạt nhân trung tâm gồm các hạt proton (mang điện dương +) và neutron (không mang điện). Đọc số hiệu nguyên tử Z = số proton = số electron.",
            "Bước 3: Đếm số electron quay xung quanh hạt nhân và số lượng electron phân bố trên từng lớp (vỏ K, L, M).",
            "Bước 4: Xác định số electron ở lớp ngoài cùng (electron hóa trị quyết định tính chất hóa học của nguyên tố: kim loại, phi kim hay khí hiếm).",
            "Bước 5: Thử nghiệm thay đổi số hạt proton/neutron để quan sát sự chuyển đổi sang nguyên tố khác hoặc đồng vị."
        ],
        "expected_phenomenon": "Nguyên tử trung hòa về điện: Số hạt proton trong hạt nhân luôn bằng đúng tổng số hạt electron quay trên các lớp vỏ. Các electron chuyển động không ngừng trên các quỹ đạo hình tròn đồng tâm: Lớp trong cùng (lớp 1) chứa tối đa 2e; lớp thứ hai chứa tối đa 8e; lớp thứ ba chứa tối đa 8e (với Z ≤ 20). Các nguyên tố kim loại (như Na, Mg, Al) có 1, 2, 3e lớp ngoài cùng; phi kim (như N, O, F) có 5, 6, 7e lớp ngoài cùng; khí hiếm (như He, Ne, Ar) có lớp vỏ bão hòa 8e (hoặc 2e đối với He).",
        "scientific_explanation": "Nguyên tử là hạt vô cùng nhỏ bé và trung hòa về điện. Nguyên tử gồm hạt nhân ở tâm mang điện tích dương và vỏ nguyên tử gồm các electron mang điện tích âm chuyển động rất nhanh xung quanh hạt nhân. Khối lượng của nguyên tử hầu như tập trung ở hạt nhân (vì khối lượng electron vô cùng nhỏ bé: m_e ≈ 0,00055 amu, có thể bỏ qua).",
        "formula": "Số hạt Z = Số p = Số e | Khối lượng nguyên tử A ≈ Số p + Số n (amu)",
        "sample_data": [
            {
                "element": "Hydrogen (H)",
                "Z": 1,
                "protons": 1,
                "neutrons": 0,
                "electrons": 1,
                "config": "1",
                "outer_e": 1,
                "type": "Phi kim"
            },
            {
                "element": "Carbon (C)",
                "Z": 6,
                "protons": 6,
                "neutrons": 6,
                "electrons": 6,
                "config": "2, 4",
                "outer_e": 4,
                "type": "Phi kim"
            },
            {
                "element": "Oxygen (O)",
                "Z": 8,
                "protons": 8,
                "neutrons": 8,
                "electrons": 8,
                "config": "2, 6",
                "outer_e": 6,
                "type": "Phi kim"
            },
            {
                "element": "Neon (Ne)",
                "Z": 10,
                "protons": 10,
                "neutrons": 10,
                "electrons": 10,
                "config": "2, 8",
                "outer_e": 8,
                "type": "Khí hiếm (Bền vững)"
            },
            {
                "element": "Sodium (Na)",
                "Z": 11,
                "protons": 11,
                "neutrons": 12,
                "electrons": 11,
                "config": "2, 8, 1",
                "outer_e": 1,
                "type": "Kim loại kiềm"
            }
        ],
        "practice_questions": [
            {
                "question": "Hạt mang điện tích âm trong nguyên tử là loại hạt nào?",
                "options": [
                    "Proton",
                    "Neutron",
                    "Electron",
                    "Hạt nhân"
                ],
                "answer_index": 2,
                "explanation": "Trong nguyên tử: Proton mang điện tích dương (+1), Electron mang điện tích âm (-1), còn Neutron không mang điện."
            },
            {
                "question": "Một nguyên tử có 11 proton trong hạt nhân thì có bao nhiêu electron ở lớp vỏ ngoài cùng?",
                "options": [
                    "1 electron",
                    "2 electron",
                    "7 electron",
                    "8 electron"
                ],
                "answer_index": 0,
                "explanation": "Nguyên tử có Z = 11 (Sodium Na), cấu hình phân bố electron theo lớp là: Lớp 1 có 2e, Lớp 2 có 8e, Lớp 3 có 1e -> Lớp ngoài cùng có 1 electron."
            }
        ]
    },
    {
        "id": "k8-che-bao-toan-khoi-luong",
        "grade": 8,
        "subject": "chemistry",
        "subject_label": "Hóa học",
        "title": "Kiểm chứng Định luật Bảo toàn Khối lượng trên Cân điện tử",
        "lesson_ref": "KHTN 8 · Bài 5: Định luật bảo toàn khối lượng và phương trình hóa học",
        "topic": "Phản ứng hóa học",
        "duration_minutes": 40,
        "difficulty": "Trung bình",
        "badge": "🧪 Hóa học 8",
        "summary": "Kiểm chứng định luật bảo toàn khối lượng của Lomonosov và Lavoisier bằng phản ứng giữa dung dịch Barium chloride (BaCl2) và Sodium sulfate (Na2SO4) tạo kết tủa trắng BaSO4 trên cân điện tử chính xác.",
        "simulation_type": "mass_conservation",
        "default_params": {
            "v_bacl2_ml": 20,
            "v_na2so4_ml": 20,
            "is_mixed": False,
            "tare_scale": True
        },
        "safety_notes": [
            "Muối bari (BaCl2) là chất độc nếu nuốt phải, đeo găng tay khi làm thí nghiệm.",
            "Không được làm đổ vỡ hóa chất ra mặt cân điện tử."
        ],
        "equipment": [
            "Cân điện tử hiện số có độ chính xác đến 0,01g",
            "Hai cốc thủy tinh 50ml (hoặc bình tam giác có nút kín và ống nghiệm nhỏ đặt bên trong)",
            "Dung dịch barium chloride (BaCl2 0,5M)",
            "Dung dịch sodium sulfate (Na2SO4 0,5M)",
            "Ống nhỏ giọt bóp cao su"
        ],
        "procedure_steps": [
            "Bước 1: Rót khoảng 15ml dung dịch BaCl2 không màu vào cốc thủy tinh thứ nhất (A). Rót khoảng 15ml dung dịch Na2SO4 không màu vào cốc thứ hai (B).",
            "Bước 2: Đặt cả hai cốc A và B lên đĩa cân điện tử. Đọc và ghi lại tổng khối lượng m1 ban đầu của cả hai cốc hóa chất trước phản ứng.",
            "Bước 3: Nhấc cốc B đổ toàn bộ dung dịch Na2SO4 vào cốc A chứa dung dịch BaCl2. Quan sát hiện tượng tạo kết tủa trắng xuất hiện tức thì.",
            "Bước 4: Đặt lại cả hai chiếc cốc lên đĩa cân điện tử (cốc A chứa hỗn hợp phản ứng và cốc B rỗng). Đọc và ghi lại khối lượng m2 sau phản ứng.",
            "Bước 5: So sánh giá trị m1 và m2, giải thích kết quả và viết phương trình hóa học."
        ],
        "expected_phenomenon": "Khi trộn hai dung dịch trong suốt không màu với nhau, ngay lập tức xuất hiện chất kết tủa màu trắng đục lắng dần xuống đáy cốc (đó là barium sulfate BaSO4 không tan). Số chỉ của cân điện tử trước và sau phản ứng hoàn toàn không thay đổi: m1 = m2 (sai số thực nghiệm < 0,01g).",
        "scientific_explanation": "Trong phản ứng hóa học, liên kết giữa các nguyên tử bị phá vỡ và các liên kết mới được hình thành, chỉ có sự biến đổi phân tử này thành phân tử khác chứ số lượng và loại nguyên tử của mỗi nguyên tố hoàn toàn được giữ nguyên không đổi. Do khối lượng của mỗi nguyên tử không đổi nên tổng khối lượng của các chất sản phẩm sinh ra luôn bằng đúng tổng khối lượng của các chất tham gia phản ứng: m(BaCl2) + m(Na2SO4) = m(BaSO4) + m(NaCl).",
        "formula": "BaCl2 + Na2SO4 → BaSO4↓ (Trắng đục) + 2NaCl  |  m_trước = m_sau",
        "sample_data": [
            {
                "step": "Trước phản ứng",
                "scale_reading_g": "156.48 g",
                "substances": "Cốc A: Dung dịch BaCl2 (trong suốt) + Cốc B: Dung dịch Na2SO4 (trong suốt)",
                "visual": "Chưa có hiện tượng biến đổi màu"
            },
            {
                "step": "Đang trộn phản ứng",
                "scale_reading_g": "156.48 g",
                "substances": "Dung dịch tiếp xúc nhau",
                "visual": "Xuất hiện vẩn đục màu trắng đục tức thì"
            },
            {
                "step": "Sau phản ứng hoàn toàn",
                "scale_reading_g": "156.48 g",
                "substances": "Cốc A: Kết tủa trắng BaSO4 lắng dưới + dung dịch NaCl; Cốc B: Rỗng",
                "visual": "m1 = m2 = 156.48 g (Bảo toàn tuyệt đối)"
            }
        ],
        "practice_questions": [
            {
                "question": "Phát biểu nào sau đây đúng với Định luật bảo toàn khối lượng?",
                "options": [
                    "Trong một phản ứng hóa học, tổng khối lượng của các chất sản phẩm bằng tổng khối lượng của các chất tham gia phản ứng",
                    "Khối lượng của các chất sản phẩm luôn lớn hơn khối lượng các chất tham gia",
                    "Khối lượng các chất luôn giảm đi sau phản ứng hóa học do tỏa nhiệt",
                    "Khối lượng chỉ bảo toàn trong các phản ứng không tạo ra kết tủa"
                ],
                "answer_index": 0,
                "explanation": "Định luật bảo toàn khối lượng: Trong một phản ứng hóa học, tổng khối lượng của các chất sản phẩm bằng tổng khối lượng của các chất tham gia phản ứng."
            },
            {
                "question": "Cho 10,6g Na2CO3 tác dụng hết với dung dịch chứa 7,3g HCl sinh ra 11,7g NaCl, 1,8g H2O và giải phóng khí CO2. Khối lượng khí CO2 bay ra là bao nhiêu?",
                "options": [
                    "2,2 g",
                    "4,4 g",
                    "8,8 g",
                    "17,9 g"
                ],
                "answer_index": 1,
                "explanation": "Áp dụng ĐL bảo toàn khối lượng: m(Na2CO3) + m(HCl) = m(NaCl) + m(H2O) + m(CO2) => 10,6 + 7,3 = 11,7 + 1,8 + m(CO2) => m(CO2) = 17,9 - 13,5 = 4,4g."
            }
        ],
        "lesson_id": "k8-bai-5-dinh-luat-bao-toan-khoi-luong-va-phuong-trinh-hoa-hoc"
    },
    {
        "id": "k9-che-phan-biet-hidrocacbon",
        "grade": 9,
        "subject": "chemistry",
        "subject_label": "Hóa học",
        "title": "Phân biệt Methane (CH4) và Ethylene (C2H4) bằng Dung dịch Bromine",
        "lesson_ref": "KHTN 9 · Bài 23 & 24: Alkane & Alkene (Methane và Ethylene)",
        "topic": "Hợp chất hữu cơ và Hydrocarbon",
        "duration_minutes": 40,
        "difficulty": "Nâng cao",
        "badge": "🧪 Hóa học 9",
        "summary": "Khảo sát phản ứng cộng đặc trưng của liên kết đôi C=C trong phân tử ethylene (C2H4) làm mất màu dung dịch nước bromine da cam, so sánh với methane (CH4) chỉ có liên kết đơn C-C không phản ứng ở điều kiện thường.",
        "simulation_type": "hydrocarbon_bromine",
        "default_params": {
            "gas_type": "C2H4",
            "flow_rate": 1.0,
            "br2_concentration": 0.05,
            "reaction_time_s": 10
        },
        "safety_notes": [
            "Hơi bromine độc và gây kích ứng niêm mạc mũi họng mạnh, tiến hành trong tủ hút hoặc nơi thoáng gió.",
            "Các khí hydrocarbon dễ bắt lửa gây nổ, tuyệt đối không để gần ngọn lửa trần."
        ],
        "equipment": [
            "Bình điều chế và ống dẫn khí methane (CH4) sạch",
            "Bình điều chế và ống dẫn khí ethylene (C2H4) sạch",
            "2 ống nghiệm thủy tinh chứa dung dịch bromine (Br2) trong nước màu vàng da cam",
            "Giá để ống nghiệm, ống dẫn khí vuốt nhọn có khóa kẹp"
        ],
        "procedure_steps": [
            "Bước 1: Chuẩn bị hai ống nghiệm (1) và (2), mỗi ống chứa khoảng 3ml dung dịch nước bromine màu vàng da cam.",
            "Bước 2: Dẫn dòng khí methane (CH4) từ từ sục qua dung dịch bromine ở ống nghiệm (1). Quan sát màu sắc dung dịch trong 3 - 5 phút.",
            "Bước 3: Dẫn dòng khí ethylene (C2H4) từ từ sục qua dung dịch bromine ở ống nghiệm (2). Quan sát màu sắc dung dịch.",
            "Bước 4: So sánh màu sắc giữa hai ống nghiệm và giải thích sự khác biệt dựa trên cấu tạo liên kết hóa học của phân tử.",
            "Bước 5: Viết phương trình hóa học phản ứng cộng phân tử Br2 vào liên kết đôi của ethylene."
        ],
        "expected_phenomenon": "Ở ống nghiệm (1) dẫn khí methane CH4: Dung dịch nước bromine vẫn giữ nguyên màu vàng da cam đặc trưng, không có hiện tượng gì xảy ra. Ở ống nghiệm (2) dẫn khí ethylene C2H4: Dung dịch nước bromine màu vàng da cam nhạt dần rồi mất màu hoàn toàn trở nên trong suốt.",
        "scientific_explanation": "Trong phân tử methane (CH4), giữa nguyên tử C và các nguyên tử H chỉ có liên kết đơn C-H rất bền vững, không phản ứng với dung dịch bromine ở điều kiện thường. Trong phân tử ethylene (C2H4), có một liên kết đôi C=C gồm một liên kết bền và một liên kết kém bền. Liên kết kém bền này dễ dàng bị đứt ra trong phản ứng cộng với phân tử bromine tạo thành hợp chất không màu 1,2-dibromoethane (CH2Br-CH2Br), làm mất màu da cam của dung dịch bromine. Đây là phản ứng đặc trưng để nhận biết hydrocarbon không no có liên kết đôi.",
        "formula": "CH2=CH2 (Không màu) + Br2 (Da cam) → CH2Br–CH2Br (Không màu)  |  CH4 + Br2 (dd) ──x Không phản ứng",
        "sample_data": [
            {
                "gas": "Methane (CH4)",
                "structure": "4 liên kết đơn C-H bền vững",
                "initial_color": "Dung dịch Bromine vàng da cam",
                "after_color": "Vẫn giữ nguyên màu vàng da cam",
                "conclusion": "Không phản ứng với dung dịch Br2 ở điều kiện thường"
            },
            {
                "gas": "Ethylene (C2H4)",
                "structure": "1 liên kết đôi C=C (có 1 LK kém bền)",
                "initial_color": "Dung dịch Bromine vàng da cam",
                "after_color": "Mất màu hoàn toàn (dung dịch trong suốt)",
                "conclusion": "Xảy ra phản ứng cộng làm đứt liên kết kém bền: CH2=CH2 + Br2 -> CH2Br-CH2Br"
            }
        ],
        "practice_questions": [
            {
                "question": "Hóa chất thuận tiện nhất để phân biệt hai chất khí không màu methane (CH4) và ethylene (C2H4) là gì?",
                "options": [
                    "Dung dịch nước vôi trong Ca(OH)2",
                    "Dung dịch bromine (Br2)",
                    "Nước cất",
                    "Quỳ tím ẩm"
                ],
                "answer_index": 1,
                "explanation": "Dung dịch bromine có màu vàng da cam đặc trưng. Khi sục qua dung dịch bromine, ethylene phản ứng làm mất màu dung dịch còn methane không phản ứng."
            },
            {
                "question": "Nguyên nhân khiến ethylene (C2H4) có khả năng làm mất màu dung dịch bromine còn methane (CH4) thì không là gì?",
                "options": [
                    "Phân tử ethylene có liên kết đôi C=C, trong đó có một liên kết kém bền dễ bị đứt ra",
                    "Ethylene tan nhiều trong nước hơn methane",
                    "Khối lượng phân tử của ethylene lớn hơn methane",
                    "Ethylene chứa nhiều nguyên tử hydrogen hơn"
                ],
                "answer_index": 0,
                "explanation": "Trong liên kết đôi C=C của ethylene có một liên kết kém bền dễ bị bẻ gãy khi tham gia phản ứng cộng với phân tử Br2, trong khi methane chỉ có các liên kết đơn C-H bền vững."
            }
        ],
        "lesson_id": "k9-bai-23-alkane"
    }
]


def list_experiments(grade=None, subject=None):
    """Lấy danh sách các bài thí nghiệm, lọc theo khối lớp hoặc phân môn."""
    items = EXPERIMENT_CATALOG
    if grade:
        try:
            grade_int = int(grade)
            items = [item for item in items if item["grade"] == grade_int]
        except (ValueError, TypeError):
            pass
    if subject:
        subj_str = str(subject).strip().lower()
        if subj_str in {"physics", "vatly", "ly"}:
            items = [item for item in items if item["subject"] == "physics"]
        elif subj_str in {"chemistry", "hoahoc", "hoa"}:
            items = [item for item in items if item["subject"] == "chemistry"]
    return items


EXP_ALIASES = {
    "k8-che-kim-loai-axit": "k8-che-kim-loai-acid",
    "k8-che-ph-chi-thi": "k8-che-thang-do-ph",
    "k8-che-trung-hoa-axit-bazo": "k8-che-trung-hoa-acid-base",
    "k9-che-day-hoat-dong-hoa-hoc": "k9-che-day-hoat-dong-kim-loai"
}


def get_experiment_by_id(exp_id):
    """Lấy thông tin chi tiết của một bài thí nghiệm theo mã id."""
    if not exp_id:
        return None
    exp_id = str(exp_id).strip()
    target_id = EXP_ALIASES.get(exp_id, exp_id)
    item = next((exp for exp in EXPERIMENT_CATALOG if exp["id"] == target_id), None)
    if not item:
        return None
    res = dict(item)
    res["simulation"] = {
        "sim_type": res.get("simulation_type"),
        "default_params": res.get("default_params", {})
    }
    res["objectives"] = [res.get("summary")] if res.get("summary") else [res.get("title")]
    res["procedure"] = res.get("procedure_steps", [])
    res["expected_phenomena"] = res.get("expected_phenomenon", "")
    res["explanation"] = res.get("scientific_explanation", "")
    res["equations"] = [res.get("formula")] if res.get("formula") else []
    res["harvest_questions"] = [q.get("question") if isinstance(q, dict) else str(q) for q in res.get("practice_questions", [])]
    return res


def _set_cell_background(cell, fill_hex):
    """Đặt màu nền cho một ô trong bảng Word."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))


def generate_lab_report_docx(exp_id, student_info=None, logged_data=None, quiz_answers=None, captured_image_base64=None):
    """Tạo tệp Báo cáo thực hành thí nghiệm chuẩn Bộ GD&ĐT ra file Word (.docx)."""
    exp = get_experiment_by_id(exp_id)
    if not exp:
        raise ValueError(f"Không tìm thấy thí nghiệm với mã: {exp_id}")

    student_info = student_info or {}
    school_name = student_info.get("school", "TRƯỜNG THCS TÂN TẠO")
    student_name = student_info.get("student_name", "...........................................................")
    student_class = student_info.get("class", f"Lớp {exp['grade']}...")
    date_str = student_info.get("date", "Ngày ..... tháng ..... năm 202...")
    group_name = student_info.get("group", "Nhóm: .............")

    doc = Document()

    # Đặt lề trang
    for s in doc.sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.9)
        s.right_margin = Inches(0.8)

    # Tiêu ngữ
    header_tbl = doc.add_table(rows=1, cols=2)
    header_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_left = header_tbl.cell(0, 0)
    c_right = header_tbl.cell(0, 1)

    p_l = c_left.paragraphs[0]
    p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_school = p_l.add_run(school_name.upper() + "\n")
    r_school.bold = True
    r_school.font.size = Pt(10)
    r_sub = p_l.add_run("TỔ KHOA HỌC TỰ NHIÊN")
    r_sub.font.size = Pt(9.5)
    r_sub.italic = True

    p_r = c_right.paragraphs[0]
    p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cộng = p_r.add_run("CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM\n")
    r_cộng.bold = True
    r_cộng.font.size = Pt(10)
    r_độc = p_r.add_run("Độc lập – Tự do – Hạnh phúc")
    r_độc.bold = True
    r_độc.font.size = Pt(10)

    p_line = doc.add_paragraph()
    p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sep = p_line.add_run("----------***----------")
    r_sep.font.color.rgb = RGBColor(100, 100, 100)

    # Tên báo cáo
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run("BÁO CÁO KẾT QUẢ THỰC HÀNH THÍ NGHIỆM\n")
    r_t.bold = True
    r_t.font.size = Pt(16)
    r_t.font.color.rgb = RGBColor(18, 70, 50)

    r_exp = p_title.add_run(f"BÀI THỰC HÀNH: {exp['title'].upper()}")
    r_exp.bold = True
    r_exp.font.size = Pt(13)
    r_exp.font.color.rgb = RGBColor(23, 107, 77)

    # Thông tin học sinh
    p_info = doc.add_paragraph()
    p_info.paragraph_format.space_before = Pt(8)
    p_info.paragraph_format.space_after = Pt(8)
    r_i = p_info.add_run(
        f"• Họ và tên học sinh: {student_name}      • Lớp: {student_class}\n"
        f"• {group_name}                          • Thời gian thực hiện: {date_str}\n"
        f"• Môn học: Khoa học tự nhiên {exp['grade']} ({exp['subject_label']})     • Bài học: {exp['lesson_ref']}"
    )
    r_i.font.size = Pt(10.5)

    # I. MỤC TIÊU THÍ NGHIỆM
    h1 = doc.add_paragraph()
    r_h1 = h1.add_run("I. MỤC TIÊU BÀI THỰC HÀNH")
    r_h1.bold = True
    r_h1.font.size = Pt(12)
    r_h1.font.color.rgb = RGBColor(18, 70, 50)

    p_obj = doc.add_paragraph()
    r_o = p_obj.add_run(f"• {exp['summary']}\n• Rèn luyện kỹ năng thao tác thiết bị, quan sát hiện tượng và phân tích số liệu thực nghiệm.")
    r_o.font.size = Pt(10.5)

    # II. DỤNG CỤ VÀ HÓA CHẤT
    h2 = doc.add_paragraph()
    r_h2 = h2.add_run("II. DỤNG CỤ VÀ HÓA CHẤT ĐÃ SỬ DỤNG")
    r_h2.bold = True
    r_h2.font.size = Pt(12)
    r_h2.font.color.rgb = RGBColor(18, 70, 50)

    for eq in exp.get("equipment", []):
        p_eq = doc.add_paragraph(style='List Bullet')
        p_eq.add_run(eq).font.size = Pt(10.5)

    if exp.get("safety_notes"):
        p_safe = doc.add_paragraph()
        r_sf = p_safe.add_run("⚠️ Lưu ý an toàn phòng thực hành: ")
        r_sf.bold = True
        r_sf.font.color.rgb = RGBColor(180, 50, 20)
        r_sft = p_safe.add_run(" ".join(exp["safety_notes"]))
        r_sft.italic = True
        r_sft.font.size = Pt(10)

    # III. CÁC BƯỚC TIẾN HÀNH
    h3 = doc.add_paragraph()
    r_h3 = h3.add_run("III. TIẾN TRÌNH THỰC HIỆN")
    r_h3.bold = True
    r_h3.font.size = Pt(12)
    r_h3.font.color.rgb = RGBColor(18, 70, 50)

    for step in exp.get("procedure_steps", []):
        p_st = doc.add_paragraph()
        r_st = p_st.add_run(step)
        r_st.font.size = Pt(10.5)

    # IV. KẾT QUẢ ĐO ĐẠC VÀ BẢNG SỐ LIỆU QUAN SÁT
    h4 = doc.add_paragraph()
    r_h4 = h4.add_run("IV. KẾT QUẢ QUAN SÁT VÀ BẢNG SỐ LIỆU ĐO ĐẠC")
    r_h4.bold = True
    r_h4.font.size = Pt(12)
    r_h4.font.color.rgb = RGBColor(18, 70, 50)

    if logged_data and isinstance(logged_data, list) and len(logged_data) > 0:
        p_log = doc.add_paragraph()
        r_lp = p_log.add_run("1. Bảng số liệu do học sinh trực tiếp đo đạc và ghi nhận từ mô phỏng:")
        r_lp.bold = True
        r_lp.font.size = Pt(10.5)
        r_lp.font.color.rgb = RGBColor(15, 80, 150)

        log_keys = list(logged_data[0].keys())
        tbl_log = doc.add_table(rows=len(logged_data) + 1, cols=len(log_keys))
        tbl_log.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl_log.style = 'Table Grid'

        for c_idx, key in enumerate(log_keys):
            cell = tbl_log.cell(0, c_idx)
            _set_cell_background(cell, "E0F2FE")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(key.replace("_", " ").upper())
            run.bold = True
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(3, 105, 161)

        for r_idx, row_dict in enumerate(logged_data, 1):
            for c_idx, key in enumerate(log_keys):
                cell = tbl_log.cell(r_idx, c_idx)
                p = cell.paragraphs[0]
                run = p.add_run(str(row_dict.get(key, "")))
                run.font.size = Pt(9.5)

        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(8)
        r_ref = p_ref.add_run("2. Bảng số liệu đối chứng / mẫu chuẩn SGK:")
        r_ref.bold = True
        r_ref.font.size = Pt(10.5)

    sample_data = exp.get("sample_data", [])
    if sample_data and isinstance(sample_data, list):
        keys = list(sample_data[0].keys())
        tbl = doc.add_table(rows=len(sample_data) + 1, cols=len(keys))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.style = 'Table Grid'

        # Tiêu đề bảng
        for c_idx, key in enumerate(keys):
            cell = tbl.cell(0, c_idx)
            _set_cell_background(cell, "EAF5EE")
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(key.replace("_", " ").upper())
            run.bold = True
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(15, 60, 40)

        # Dữ liệu bảng
        for r_idx, row_dict in enumerate(sample_data, 1):
            for c_idx, key in enumerate(keys):
                cell = tbl.cell(r_idx, c_idx)
                p = cell.paragraphs[0]
                run = p.add_run(str(row_dict.get(key, "")))
                run.font.size = Pt(9.5)

    if captured_image_base64:
        try:
            import base64
            img_data = captured_image_base64
            if "," in img_data:
                img_data = img_data.split(",", 1)[1]
            img_bytes = base64.b64decode(img_data)
            img_stream = io.BytesIO(img_bytes)

            p_img_t = doc.add_paragraph()
            p_img_t.paragraph_format.space_before = Pt(8)
            r_it = p_img_t.add_run("• Ảnh chụp hiện trường thao tác thực hành 3D của học sinh:")
            r_it.bold = True
            r_it.font.size = Pt(10.5)

            p_pic = doc.add_paragraph()
            p_pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_pic.paragraph_format.space_before = Pt(4)
            p_pic.paragraph_format.space_after = Pt(2)
            run_pic = p_pic.add_run()
            run_pic.add_picture(img_stream, width=Inches(5.0))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r_cap = p_cap.add_run("(Hình: Minh chứng kết quả thực nghiệm trên phòng thí nghiệm ảo thời gian thực)")
            r_cap.italic = True
            r_cap.font.size = Pt(9)
            r_cap.font.color.rgb = RGBColor(100, 116, 139)
        except Exception as exc:
            pass

    p_phenom = doc.add_paragraph()
    p_phenom.paragraph_format.space_before = Pt(8)
    r_ph1 = p_phenom.add_run("• Hiện tượng quan sát được: ")
    r_ph1.bold = True
    p_phenom.add_run(exp.get("expected_phenomenon", "")).font.size = Pt(10.5)

    if exp.get("formula"):
        p_form = doc.add_paragraph()
        r_f1 = p_form.add_run("• Công thức / Phương trình hóa học: ")
        r_f1.bold = True
        r_f2 = p_form.add_run(exp["formula"])
        r_f2.bold = True
        r_f2.font.color.rgb = RGBColor(15, 80, 150)

    # V. GIẢI THÍCH VÀ KẾT LUẬN
    h5 = doc.add_paragraph()
    r_h5 = h5.add_run("V. GIẢI THÍCH VÀ KẾT LUẬN")
    r_h5.bold = True
    r_h5.font.size = Pt(12)
    r_h5.font.color.rgb = RGBColor(18, 70, 50)

    p_exp = doc.add_paragraph()
    p_exp.add_run(exp.get("scientific_explanation", "")).font.size = Pt(10.5)

    # VI. CÂU HỎI THU HOẠCH
    questions = exp.get("practice_questions", [])
    if questions:
        h6 = doc.add_paragraph()
        r_h6 = h6.add_run("VI. CÂU HỎI THU HOẠCH VÀ BÀI TẬP CỦNG CỐ")
        r_h6.bold = True
        r_h6.font.size = Pt(12)
        r_h6.font.color.rgb = RGBColor(18, 70, 50)

        if quiz_answers and isinstance(quiz_answers, dict):
            correct_cnt = 0
            total_answered = 0
            for q_idx, q in enumerate(questions):
                ans = quiz_answers.get(str(q_idx))
                if ans is not None:
                    total_answered += 1
                    try:
                        if int(ans) == q.get("answer_index", -1):
                            correct_cnt += 1
                    except (ValueError, TypeError):
                        pass
            if total_answered > 0:
                p_score = doc.add_paragraph()
                p_score.paragraph_format.space_before = Pt(4)
                r_sc1 = p_score.add_run(f"★ KẾT QUẢ TRẢ LỜI CỦA HỌC SINH: {correct_cnt}/{len(questions)} câu đúng")
                r_sc1.bold = True
                r_sc1.font.size = Pt(11)
                r_sc1.font.color.rgb = RGBColor(22, 101, 52) if correct_cnt == len(questions) else RGBColor(180, 83, 9)

        for q_idx, q in enumerate(questions, 1):
            p_q = doc.add_paragraph()
            p_q.paragraph_format.space_before = Pt(6)
            r_qn = p_q.add_run(f"Câu {q_idx}: {q['question']}\n")
            r_qn.bold = True
            r_qn.font.size = Pt(10.5)

            student_choice = None
            if quiz_answers and isinstance(quiz_answers, dict):
                val = quiz_answers.get(str(q_idx - 1))
                if val is not None:
                    try:
                        student_choice = int(val)
                    except (ValueError, TypeError):
                        pass

            for opt_idx, opt in enumerate(q.get("options", [])):
                letter = chr(65 + opt_idx)
                is_correct = opt_idx == q.get("answer_index", -1)
                is_student_pick = (student_choice is not None and opt_idx == student_choice)

                if is_student_pick:
                    if is_correct:
                        mark = " [✓] "
                        suffix = "  <-- Học sinh đã chọn (CHÍNH XÁC)"
                        color = RGBColor(22, 101, 52)
                    else:
                        mark = " [✗] "
                        suffix = "  <-- Học sinh đã chọn (CHƯA ĐÚNG)"
                        color = RGBColor(220, 38, 38)
                elif is_correct and student_choice is not None:
                    mark = " [✓] "
                    suffix = "  <-- Đáp án đúng chuẩn SGK"
                    color = RGBColor(22, 101, 52)
                elif is_correct:
                    mark = " [x] "
                    suffix = ""
                    color = RGBColor(15, 23, 42)
                else:
                    mark = " [ ] "
                    suffix = ""
                    color = RGBColor(71, 85, 105)

                p_opt = doc.add_paragraph()
                p_opt.paragraph_format.left_indent = Inches(0.2)
                p_opt.paragraph_format.space_before = Pt(0)
                p_opt.paragraph_format.space_after = Pt(2)
                r_opt = p_opt.add_run(f"{mark}{letter}. {opt}{suffix}")
                r_opt.font.size = Pt(10)
                r_opt.font.color.rgb = color
                if is_correct or is_student_pick:
                    r_opt.bold = True

            if q.get("explanation"):
                p_ans = doc.add_paragraph()
                p_ans.paragraph_format.left_indent = Inches(0.2)
                r_ans = p_ans.add_run(f"-> Lời giải thích: {q['explanation']}")
                r_ans.italic = True
                r_ans.font.size = Pt(9.5)
                r_ans.font.color.rgb = RGBColor(60, 90, 75)

    # Chữ ký đánh giá của giáo viên và học sinh
    doc.add_paragraph().paragraph_format.space_before = Pt(15)
    sig_tbl = doc.add_table(rows=1, cols=2)
    sig_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_s1 = sig_tbl.cell(0, 0)
    c_s2 = sig_tbl.cell(0, 1)

    p_s1 = c_s1.paragraphs[0]
    p_s1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_gv = p_s1.add_run("GIÁO VIÊN CHẤM ĐIỂM / NHẬN XÉT\n")
    r_gv.bold = True
    r_gv.font.size = Pt(10.5)
    p_s1.add_run("(Ký và ghi rõ họ tên)\n\n\n\n...........................................................")

    p_s2 = c_s2.paragraphs[0]
    p_s2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_hs = p_s2.add_run("HỌC SINH LÀM BÁO CÁO\n")
    r_hs.bold = True
    r_hs.font.size = Pt(10.5)
    p_s2.add_run("(Ký và ghi rõ họ tên)\n\n\n\n...........................................................")

    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer.getvalue()
