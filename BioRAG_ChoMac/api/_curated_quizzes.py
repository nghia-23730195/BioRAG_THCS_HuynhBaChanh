# -*- coding: utf-8 -*-
"""Ngân hàng Đề thi Trắc nghiệm mẫu chuẩn SGK Kết nối tri thức với cuộc sống (THCS Tân Tạo).

Cung cấp các bộ đề kiểm tra 15 phút và đề kiểm tra Giữa kỳ chuẩn cho cả 4 khối lớp 6, 7, 8, 9
để học sinh và giáo viên có thể làm bài và ôn tập tức thì mà không cần chờ AI khởi tạo.
"""

CURATED_EXAM_BANK = [
    # =========================================================================
    # LỚP 6
    # =========================================================================
    {
        "id": "k6-15p-te-bao",
        "grade": 6,
        "type": "15p",
        "type_label": "Kiểm tra 15 phút",
        "title": "Kiểm tra 15 phút: Tế bào – Đơn vị cơ bản của sự sống",
        "topic": "Tế bào - Đơn vị cơ bản của sự sống",
        "duration_minutes": 15,
        "questions_count": 10,
        "description": "Đánh giá mức độ nhận biết và thông hiểu về cấu tạo tế bào, chức năng màng sinh chất, tế bào chất, nhân tế bào và sự lớn lên, phân chia tế bào.",
        "questions": [
            {
                "id": 1,
                "difficulty": "Nhận biết",
                "question": "Đơn vị cấu trúc và chức năng cơ bản của mọi cơ thể sinh vật là gì?",
                "options": ["Mô", "Tế bào", "Cơ quan", "Hệ cơ quan"],
                "answer_index": 1,
                "explanation": "Tất cả các sinh vật sống từ đơn bào đến đa bào đều được cấu tạo từ một hoặc nhiều tế bào.",
                "evidence": "Tế bào là đơn vị cơ bản cấu tạo nên mọi cơ thể sinh vật.",
                "source": "KHTN 6 KNTT",
                "page": 58
            },
            {
                "id": 2,
                "difficulty": "Nhận biết",
                "question": "Thành phần nào sau đây có ở tế bào thực vật mà không có ở tế bào động vật?",
                "options": ["Màng tế bào và nhân", "Thành tế bào và lục lạp", "Tế bào chất và ti thể", "Không bào và màng sinh chất"],
                "answer_index": 1,
                "explanation": "Tế bào thực vật có thành tế bào bằng cellulose giúp duy trì hình dạng cố định và lục lạp chứa diệp lục để quang hợp, tế bào động vật không có hai thành phần này.",
                "evidence": "Thành tế bào và lục lạp chỉ có ở tế bào thực vật.",
                "source": "KHTN 6 KNTT",
                "page": 60
            },
            {
                "id": 3,
                "difficulty": "Thông hiểu",
                "question": "Bào quan nào đóng vai trò là trung tâm điều khiển mọi hoạt động sống của tế bào?",
                "options": ["Lục lạp", "Tế bào chất", "Nhân tế bào (hoặc vùng nhân)", "Màng tế bào"],
                "answer_index": 2,
                "explanation": "Nhân tế bào chứa vật chất di truyền (DNA) điều khiển mọi quá trình trao đổi chất và hoạt động sống của tế bào.",
                "evidence": "Nhân là trung tâm điều khiển mọi hoạt động sống của tế bào.",
                "source": "KHTN 6 KNTT",
                "page": 61
            },
            {
                "id": 4,
                "difficulty": "Thông hiểu",
                "question": "Màng sinh chất (màng tế bào) đảm nhận chức năng nào sau đây?",
                "options": [
                    "Nơi diễn ra mọi hoạt động sống của tế bào",
                    "Bảo vệ và kiểm soát sự trao đổi chất giữa tế bào với môi trường",
                    "Chứa chất diệp lục hấp thu năng lượng ánh sáng",
                    "Tạo hình dạng cố định vững chắc cho tế bào thực vật"
                ],
                "answer_index": 1,
                "explanation": "Màng sinh chất bao bọc tế bào chất, bảo vệ và kiểm soát có chọn lọc các chất đi vào hoặc đi ra khỏi tế bào.",
                "evidence": "Màng tế bào giúp bảo vệ và kiểm soát các chất ra vào tế bào.",
                "source": "KHTN 6 KNTT",
                "page": 59
            },
            {
                "id": 5,
                "difficulty": "Nhận biết",
                "question": "Tế bào nhân sơ khác với tế bào nhân thực ở đặc điểm cơ bản nào sau đây?",
                "options": [
                    "Không có màng tế bào",
                    "Chưa có màng nhân bao bọc vật chất di truyền",
                    "Không có tế bào chất",
                    "Kích thước lớn hơn rất nhiều so với tế bào nhân thực"
                ],
                "answer_index": 1,
                "explanation": "Tế bào nhân sơ (như vi khuẩn) chỉ có vùng nhân chứa vật chất di truyền chưa có màng nhân bao bọc, trong khi tế bào nhân thực đã có màng nhân hoàn chỉnh.",
                "evidence": "Tế bào nhân sơ chưa có màng nhân, vật chất di truyền nằm tự do trong tế bào chất.",
                "source": "KHTN 6 KNTT",
                "page": 62
            },
            {
                "id": 6,
                "difficulty": "Nhận biết",
                "question": "Sinh vật nào sau đây thuộc nhóm sinh vật đơn bào?",
                "options": ["Cây ngô", "Con thỏ", "Trùng roi xanh", "Cây rêu"],
                "answer_index": 2,
                "explanation": "Trùng roi xanh là sinh vật đơn bào, cơ thể chỉ gồm đúng một tế bào nhưng thực hiện được đầy đủ các hoạt động sống.",
                "evidence": "Trùng roi, trùng giày, vi khuẩn là các cơ thể đơn bào.",
                "source": "KHTN 6 KNTT",
                "page": 66
            },
            {
                "id": 7,
                "difficulty": "Thông hiểu",
                "question": "Quá trình lớn lên và phân chia của tế bào có ý nghĩa sinh học gì đối với cơ thể đa bào?",
                "options": [
                    "Làm tăng kích thước và khối lượng của cơ thể, thay thế các tế bào già chết",
                    "Giúp cơ thể di chuyển nhanh nhẹn hơn trong môi trường",
                    "Chỉ để sinh ra nhiệt lượng làm ấm cơ thể",
                    "Giúp cơ thể không cần lấy thức ăn và nước uống từ bên ngoài"
                ],
                "answer_index": 0,
                "explanation": "Sự lớn lên và phân chia liên tục của tế bào giúp cơ thể tăng trưởng về kích thước, khối lượng và phục hồi các mô bị tổn thương.",
                "evidence": "Sự lớn lên và phân chia của tế bào giúp cơ thể sinh vật lớn lên và thay thế tế bào bị tổn thương.",
                "source": "KHTN 6 KNTT",
                "page": 64
            },
            {
                "id": 8,
                "difficulty": "Thông hiểu",
                "question": "Lục lạp trong tế bào thực vật có vai trò chính là gì?",
                "options": [
                    "Tiêu hóa thức ăn lấy từ ngoài vào",
                    "Hấp thụ ánh sáng mặt trời để quang hợp tổng hợp chất hữu cơ",
                    "Chứa thông tin di truyền của loài",
                    "Vận chuyển nước và muối khoáng"
                ],
                "answer_index": 1,
                "explanation": "Lục lạp chứa sắc tố quang hợp là diệp lục, có khả năng hấp thu năng lượng ánh sáng mặt trời để tổng hợp chất hữu cơ nuôi cây.",
                "evidence": "Lục lạp chứa diệp lục, là bào quan thực hiện quá trình quang hợp.",
                "source": "KHTN 6 KNTT",
                "page": 60
            },
            {
                "id": 9,
                "difficulty": "Vận dụng",
                "question": "Khi làm tiêu bản quan sát tế bào biểu bì vảy hành, vì sao người ta thường nhỏ một giọt dung dịch iodine hoặc Lugol lên mẫu vật?",
                "options": [
                    "Để giữ cho tế bào sống lâu hơn",
                    "Để nhuộm màu các cấu trúc tế bào (đặc biệt là nhân), giúp dễ quan sát dưới kính hiển vi",
                    "Để hòa tan bớt thành tế bào",
                    "Để khử trùng cho mẫu vật không bị mốc"
                ],
                "answer_index": 1,
                "explanation": "Dung dịch iodine/Lugol có tính bắt màu các chất hữu cơ trong nhân và tế bào chất, tạo độ tương phản cao giúp nhìn rõ các chi tiết tế bào.",
                "evidence": "Nhỏ một giọt dung dịch iodine để nhuộm màu tế bào giúp quan sát rõ nhân và tế bào chất.",
                "source": "KHTN 6 KNTT",
                "page": 69
            },
            {
                "id": 10,
                "difficulty": "Vận dụng",
                "question": "Từ 1 tế bào mẹ ban đầu, sau 3 lần phân chia liên tiếp sẽ tạo ra bao nhiêu tế bào con?",
                "options": ["3 tế bào", "6 tế bào", "8 tế bào", "16 tế bào"],
                "answer_index": 2,
                "explanation": "Sau mỗi lần phân chia, số tế bào tăng gấp đôi theo công thức $2^n$. Sau 3 lần phân chia: $2^3 = 8$ tế bào con.",
                "evidence": "Từ một tế bào ban đầu, sau n lần phân chia liên tiếp tạo ra 2^n tế bào con.",
                "source": "KHTN 6 KNTT",
                "page": 64
            }
        ]
    },
    {
        "id": "k6-midterm-tong-hop",
        "grade": 6,
        "type": "midterm",
        "type_label": "Kiểm tra Giữa kỳ 1",
        "title": "Kiểm tra Giữa kỳ 1 KHTN 6: Tế bào, Đa dạng sinh học & Lực",
        "topic": "Từ tế bào đến cơ thể, Nấm và vi khuẩn, Lực và chuyển động",
        "duration_minutes": 45,
        "questions_count": 20,
        "description": "Đề kiểm tra định kỳ giữa học kỳ 1 tích hợp các nội dung Sinh học (tế bào, cơ thể đơn bào/đa bào, nấm) và Vật lý (lực, trọng lực, lực ma sát).",
        "questions": [
            {
                "id": 1,
                "difficulty": "Nhận biết",
                "question": "Cấp độ tổ chức cơ thể nào sau đây đứng ngay sau tế bào trong cơ thể đa bào?",
                "options": ["Cơ quan", "Mô", "Hệ cơ quan", "Cơ thể"],
                "answer_index": 1,
                "explanation": "Thứ tự tổ chức cơ thể đa bào: Tế bào → Mô → Cơ quan → Hệ cơ quan → Cơ thể.",
                "evidence": "Tập hợp các tế bào giống nhau cùng thực hiện một chức năng gọi là mô.",
                "source": "KHTN 6 KNTT",
                "page": 73
            },
            {
                "id": 2,
                "difficulty": "Nhận biết",
                "question": "Hệ cơ quan nào ở người có chức năng vận chuyển máu đi khắp cơ thể?",
                "options": ["Hệ tiêu hóa", "Hệ hô hấp", "Hệ tuần hoàn", "Hệ bài tiết"],
                "answer_index": 2,
                "explanation": "Hệ tuần hoàn gồm tim và các mạch máu có chức năng vận chuyển máu, cung cấp oxy và dưỡng chất tới các tế bào.",
                "evidence": "Hệ tuần hoàn gồm tim và mạch máu có chức năng vận chuyển các chất.",
                "source": "KHTN 6 KNTT",
                "page": 77
            },
            {
                "id": 3,
                "difficulty": "Nhận biết",
                "question": "Vi khuẩn thuộc nhóm sinh vật nào sau đây?",
                "options": ["Sinh vật nhân thực đa bào", "Sinh vật nhân sơ đơn bào", "Động vật nguyên sinh", "Thực vật bậc thấp"],
                "answer_index": 1,
                "explanation": "Vi khuẩn là những cơ thể đơn bào có kích thước hiển vi, chưa có màng nhân (nhân sơ).",
                "evidence": "Vi khuẩn là những sinh vật đơn bào, nhân sơ, có kích thước rất nhỏ.",
                "source": "KHTN 6 KNTT",
                "page": 82
            },
            {
                "id": 4,
                "difficulty": "Thông hiểu",
                "question": "Nấm có đặc điểm nào khác biệt cơ bản với thực vật?",
                "options": [
                    "Nấm không có thành tế bào",
                    "Nấm không chứa chất diệp lục nên sống dị dưỡng",
                    "Nấm không có tế bào chất",
                    "Nấm luôn luôn là sinh vật đơn bào"
                ],
                "answer_index": 1,
                "explanation": "Nấm không có diệp lục nên không thể tự tổng hợp chất hữu cơ bằng quang hợp, chúng sống dị dưỡng (hoại sinh hoặc ký sinh).",
                "evidence": "Nấm không có diệp lục, sống dị dưỡng bằng cách hoại sinh hoặc ký sinh.",
                "source": "KHTN 6 KNTT",
                "page": 88
            },
            {
                "id": 5,
                "difficulty": "Nhận biết",
                "question": "Đơn vị đo của lực trong hệ đo lường quốc tế (SI) là gì?",
                "options": ["Kilôgam (kg)", "Mét (m)", "Niu-tơn (N)", "Jun (J)"],
                "answer_index": 2,
                "explanation": "Lực được đo bằng đơn vị Niu-tơn, ký hiệu là N.",
                "evidence": "Đơn vị đo lực là niu-tơn, kí hiệu là N.",
                "source": "KHTN 6 KNTT",
                "page": 134
            },
            {
                "id": 6,
                "difficulty": "Thông hiểu",
                "question": "Lực nào sau đây là lực tiếp xúc?",
                "options": [
                    "Lực hút của Trái Đất tác dụng lên quả táo rụng",
                    "Lực đẩy của tay người khi đẩy chiếc xe đẩy hàng",
                    "Lực hút giữa hai thanh nam châm đặt cách xa nhau",
                    "Lực tĩnh điện giữa hai quả cầu nhiễm điện"
                ],
                "answer_index": 1,
                "explanation": "Lực đẩy của tay xuất hiện khi tay tiếp xúc trực tiếp với bề mặt xe đẩy hàng.",
                "evidence": "Lực tiếp xúc xuất hiện khi vật gây ra lực có sự tiếp xúc với vật chịu tác dụng của lực.",
                "source": "KHTN 6 KNTT",
                "page": 140
            },
            {
                "id": 7,
                "difficulty": "Nhận biết",
                "question": "Trọng lượng của một vật là gì?",
                "options": [
                    "Lượng chất chứa trong vật đó",
                    "Độ lớn lực hút của Trái Đất tác dụng lên vật đó",
                    "Thể tích không gian mà vật đó chiếm chỗ",
                    "Khả năng cản trở chuyển động của vật"
                ],
                "answer_index": 1,
                "explanation": "Trọng lượng là độ lớn của trọng lực (lực hút của Trái Đất) tác dụng lên vật.",
                "evidence": "Trọng lượng là độ lớn lực hút của Trái Đất tác dụng lên vật.",
                "source": "KHTN 6 KNTT",
                "page": 146
            },
            {
                "id": 8,
                "difficulty": "Vận dụng",
                "question": "Một vật có khối lượng $m = 2\\text{ kg}$ thì có trọng lượng gần bằng bao nhiêu trên bề mặt Trái Đất?",
                "options": ["2 N", "10 N", "20 N", "200 N"],
                "answer_index": 2,
                "explanation": "Công thức liên hệ trọng lượng và khối lượng: $P = 10 \\times m = 10 \\times 2 = 20\\text{ N}$.",
                "evidence": "Trọng lượng P và khối lượng m liên hệ với nhau theo công thức P = 10m.",
                "source": "KHTN 6 KNTT",
                "page": 147
            },
            {
                "id": 9,
                "difficulty": "Thông hiểu",
                "question": "Lực ma sát trượt xuất hiện khi nào?",
                "options": [
                    "Khi một vật trượt trên bề mặt của vật khác",
                    "Khi một vật đứng yên trên mặt phẳng nghiêng",
                    "Khi một vật đang rơi tự do trong chân không",
                    "Khi hai vật chưa hề tiếp xúc với nhau"
                ],
                "answer_index": 0,
                "explanation": "Lực ma sát trượt xuất hiện ở mặt tiếp xúc giữa hai vật khi vật này trượt trên bề mặt vật kia và cản trở chuyển động trượt.",
                "evidence": "Lực ma sát trượt xuất hiện khi một vật trượt trên bề mặt của vật khác.",
                "source": "KHTN 6 KNTT",
                "page": 152
            },
            {
                "id": 10,
                "difficulty": "Vận dụng",
                "question": "Biện pháp nào sau đây có tác dụng làm TĂNG ma sát có lợi trong đời sống?",
                "options": [
                    "Tra dầu mỡ bôi trơn vào xích xe đạp",
                    "Khía rãnh sâu trên lốp xe và đế giày",
                    "Mài nhẵn bề mặt các ổ bi xe cộ",
                    "Lắp bánh xe dưới chân tủ đồ để dễ đẩy"
                ],
                "answer_index": 1,
                "explanation": "Khía rãnh trên đế giày và lốp xe làm tăng độ bám, chống trơn trượt hiệu quả.",
                "evidence": "Rãnh khía trên lốp xe và đế giày giúp tăng ma sát để không bị trơn trượt.",
                "source": "KHTN 6 KNTT",
                "page": 154
            },
            {
                "id": 11,
                "difficulty": "Nhận biết",
                "question": "Bào quan ti thể trong tế bào nhân thực có chức năng chính là gì?",
                "options": [
                    "Quang hợp tổng hợp đường",
                    "Hô hấp tế bào giải phóng năng lượng ATP",
                    "Bảo vệ tế bào",
                    "Dự trữ nước và muối khoáng"
                ],
                "answer_index": 1,
                "explanation": "Ti thể là nhà máy năng lượng của tế bào, nơi diễn ra quá trình hô hấp tế bào giải phóng năng lượng.",
                "evidence": "Ti thể là nơi diễn ra hô hấp tế bào giải phóng năng lượng cho hoạt động sống.",
                "source": "KHTN 6 KNTT",
                "page": 61
            },
            {
                "id": 12,
                "difficulty": "Thông hiểu",
                "question": "Khi bóp quả bóng cao su, hiện tượng gì xảy ra với quả bóng chứng tỏ lực đã tác dụng?",
                "options": [
                    "Quả bóng bị biến dạng",
                    "Quả bóng đổi màu sắc",
                    "Khối lượng quả bóng tăng lên",
                    "Nhiệt độ quả bóng giảm đột ngột"
                ],
                "answer_index": 0,
                "explanation": "Tác dụng của lực có thể làm biến đổi chuyển động hoặc làm biến dạng vật.",
                "evidence": "Lực tác dụng lên vật có thể làm thay đổi chuyển động hoặc làm biến dạng vật.",
                "source": "KHTN 6 KNTT",
                "page": 136
            },
            {
                "id": 13,
                "difficulty": "Nhận biết",
                "question": "Nấm men (yeast) thường được ứng dụng trong hoạt động thực tiễn nào?",
                "options": [
                    "Làm sạch dầu mỡ trên biển",
                    "Lên men làm bánh mì nở xốp và nấu bia rượu",
                    "Sản xuất phân bón hóa học",
                    "Nhuộm màu sợi vải"
                ],
                "answer_index": 1,
                "explanation": "Nấm men chuyển hóa đường thành khí CO2 giúp bột bánh nở phồng và tạo cồn trong sản xuất đồ uống lên men.",
                "evidence": "Nấm men được ứng dụng trong sản xuất bánh mì, bia, rượu.",
                "source": "KHTN 6 KNTT",
                "page": 90
            },
            {
                "id": 14,
                "difficulty": "Thông hiểu",
                "question": "Vì sao thức ăn để lâu ngày ở nhiệt độ phòng ẩm ướt dễ bị ôi thiu?",
                "options": [
                    "Do vi khuẩn và nấm mốc trong môi trường xâm nhập, sinh sôi và phân hủy chất hữu cơ",
                    "Do thức ăn tự bốc hơi nước",
                    "Do ánh sáng mặt trời biến đổi thức ăn",
                    "Do không khí làm thức ăn cứng lại"
                ],
                "answer_index": 0,
                "explanation": "Nhiệt độ ẩm và ấm áp là điều kiện lý tưởng cho vi khuẩn và nấm hoại sinh phát triển nhanh chóng làm hỏng thực phẩm.",
                "evidence": "Vi khuẩn và nấm hoại sinh làm thức ăn bị thối rữa, ôi thiu.",
                "source": "KHTN 6 KNTT",
                "page": 84
            },
            {
                "id": 15,
                "difficulty": "Nhận biết",
                "question": "Dụng cụ dùng để đo lực trong phòng thực hành là gì?",
                "options": ["Cân đồng hồ", "Thước cuộn", "Lực kế", "Nhiệt kế"],
                "answer_index": 2,
                "explanation": "Lực kế lò xo là dụng cụ chuyên dụng dùng để đo độ lớn của lực.",
                "evidence": "Người ta dùng lực kế để đo lực.",
                "source": "KHTN 6 KNTT",
                "page": 135
            },
            {
                "id": 16,
                "difficulty": "Thông hiểu",
                "question": "Trong các trường hợp sau, trường hợp nào lực ma sát là CÓ HẠI?",
                "options": [
                    "Ma sát giữa má phanh và vành xe khi bóp phanh",
                    "Ma sát làm mòn đế giày và lốp xe sau thời gian dài sử dụng",
                    "Ma sát giữa bàn chân và mặt đất khi bước đi",
                    "Ma sát giữa que diêm và vỏ bao diêm khi quẹt diêm"
                ],
                "answer_index": 1,
                "explanation": "Ma sát làm mài mòn các chi tiết máy, lốp xe và đế giày là ma sát có hại cần giảm thiểu.",
                "evidence": "Ma sát làm mòn các chi tiết máy, lốp xe và đế giày là ma sát có hại.",
                "source": "KHTN 6 KNTT",
                "page": 155
            },
            {
                "id": 17,
                "difficulty": "Vận dụng",
                "question": "Khi một vận động viên ném quả bóng rổ lên cao, độ lớn vận tốc của quả bóng giảm dần khi đi lên là do tác dụng của:",
                "options": [
                    "Lực ma sát nghỉ",
                    "Trọng lực (hướng ngược chiều chuyển động)",
                    "Lực đẩy của không khí",
                    "Lực đàn hồi của quả bóng"
                ],
                "answer_index": 1,
                "explanation": "Khi bóng bay lên, trọng lực hút quả bóng hướng xuống dưới ngược chiều chuyển động làm vận tốc của quả bóng giảm dần.",
                "evidence": "Trọng lực luôn có phương thẳng đứng và chiều hướng về phía tâm Trái Đất.",
                "source": "KHTN 6 KNTT",
                "page": 146
            },
            {
                "id": 18,
                "difficulty": "Nhận biết",
                "question": "Thực vật lấy nước và chất khoáng chủ yếu qua bộ phận nào?",
                "options": ["Lỗ khí ở lá", "Lông hút ở rễ", "Vỏ thân cây", "Cánh hoa"],
                "answer_index": 1,
                "explanation": "Lông hút ở rễ cây là cơ quan chính hấp thụ nước và các ion khoáng từ dung dịch đất.",
                "evidence": "Lông hút ở rễ là cơ quan chủ yếu hút nước và muối khoáng.",
                "source": "KHTN 6 KNTT",
                "page": 75
            },
            {
                "id": 19,
                "difficulty": "Thông hiểu",
                "question": "Treo một vật nặng vào đầu dưới của một lò xo xoắn, lò xo bị dãn dài ra. Lực mà lò xo tác dụng ngược lại lên vật là:",
                "options": ["Lực đàn hồi", "Lực ma sát trượt", "Lực từ", "Trọng lực"],
                "answer_index": 0,
                "explanation": "Khi lò xo bị biến dạng dãn, lực đàn hồi xuất hiện ở hai đầu lò xo chống lại sự biến dạng đó.",
                "evidence": "Lực đàn hồi xuất hiện khi vật đàn hồi bị biến dạng và có xu hướng lấy lại hình dạng ban đầu.",
                "source": "KHTN 6 KNTT",
                "page": 149
            },
            {
                "id": 20,
                "difficulty": "Vận dụng",
                "question": "Để bảo quản rau củ quả tươi lâu trong gia đình, cách làm nào sau đây là KHOA HỌC nhất?",
                "options": [
                    "Phơi trực tiếp ngoài nắng gắt cho héo",
                    "Ngâm ngập hoàn toàn trong chậu nước muối đậm đặc",
                    "Cho vào túi thoáng khí hoặc hộp kín rồi bảo quản trong ngăn mát tủ lạnh",
                    "Để gần bếp ga ấm nóng"
                ],
                "answer_index": 2,
                "explanation": "Nhiệt độ thấp trong ngăn mát tủ lạnh làm giảm cường độ hô hấp của tế bào rau quả và ức chế vi khuẩn phát triển, giúp giữ độ tươi lâu.",
                "evidence": "Nhiệt độ thấp làm giảm hô hấp tế bào và ức chế vi khuẩn giúp bảo quản nông sản.",
                "source": "KHTN 6 KNTT",
                "page": 86
            }
        ]
    },

    # =========================================================================
    # LỚP 7
    # =========================================================================
    {
        "id": "k7-15p-quang-hop-ho-hap",
        "grade": 7,
        "type": "15p",
        "type_label": "Kiểm tra 15 phút",
        "title": "Kiểm tra 15 phút: Quang hợp và Hô hấp tế bào",
        "topic": "Quang hợp ở thực vật, Hô hấp tế bào",
        "duration_minutes": 15,
        "questions_count": 10,
        "description": "Kiểm tra bản chất, nguyên liệu, sản phẩm, phương trình hóa học và ý nghĩa thực tiễn của quang hợp và hô hấp tế bào.",
        "questions": [
            {
                "id": 1,
                "difficulty": "Nhận biết",
                "question": "Bào quan thực hiện quá trình quang hợp ở tế bào thực vật là:",
                "options": ["Ti thể", "Lục lạp", "Ribosome", "Không bào"],
                "answer_index": 1,
                "explanation": "Lục lạp chứa chất diệp lục có khả năng hấp thu năng lượng ánh sáng để quang hợp.",
                "evidence": "Quang hợp diễn ra chủ yếu ở lục lạp của tế bào lá cây.",
                "source": "KHTN 7 KNTT",
                "page": 94
            },
            {
                "id": 2,
                "difficulty": "Nhận biết",
                "question": "Sản phẩm của quá trình quang hợp ở thực vật gồm:",
                "options": [
                    "Glucose (chất hữu cơ) và khí oxygen",
                    "Nước và khí carbon dioxide",
                    "Khí nitrogen và nước",
                    "Muối khoáng và năng lượng nhiệt"
                ],
                "answer_index": 0,
                "explanation": "Quang hợp sử dụng CO2 và nước dưới tác dụng của ánh sáng tạo ra glucose và giải phóng oxygen.",
                "evidence": "Sản phẩm của quang hợp là chất hữu cơ (glucose) và khí oxygen.",
                "source": "KHTN 7 KNTT",
                "page": 95
            },
            {
                "id": 3,
                "difficulty": "Thông hiểu",
                "question": "Nguyên liệu đầu vào của quá trình hô hấp tế bào gồm:",
                "options": [
                    "Carbon dioxide và Nước",
                    "Chất hữu cơ (Glucose) và khí Oxygen",
                    "Ánh sáng và Diệp lục",
                    "Khí Nitrogen và Muối khoáng"
                ],
                "answer_index": 1,
                "explanation": "Hô hấp tế bào phân giải chất hữu cơ với sự tham gia của oxygen để giải phóng năng lượng.",
                "evidence": "Nguyên liệu của hô hấp tế bào là chất hữu cơ và khí oxygen.",
                "source": "KHTN 7 KNTT",
                "page": 102
            },
            {
                "id": 4,
                "difficulty": "Nhận biết",
                "question": "Nơi diễn ra chủ yếu của quá trình hô hấp tế bào ở sinh vật nhân thực là:",
                "options": ["Lục lạp", "Ti thể", "Màng sinh chất", "Nhân tế bào"],
                "answer_index": 1,
                "explanation": "Ti thể là bào quan chuyên trách thực hiện quá trình hô hấp tế bào tạo năng lượng ATP.",
                "evidence": "Ở sinh vật nhân thực, hô hấp tế bào diễn ra chủ yếu trong ti thể.",
                "source": "KHTN 7 KNTT",
                "page": 103
            },
            {
                "id": 5,
                "difficulty": "Thông hiểu",
                "question": "Năng lượng giải phóng trong quá trình hô hấp tế bào được tích lũy chủ yếu dưới dạng nào?",
                "options": ["Năng lượng ATP", "Quang năng", "Hóa năng trong tinh bột", "Thế năng hấp dẫn"],
                "answer_index": 0,
                "explanation": "Năng lượng từ liên kết hóa học của chất hữu cơ được chuyển sang dạng liên kết cao năng trong phân tử ATP để cung cấp cho hoạt động sống.",
                "evidence": "Năng lượng giải phóng ra được tích lũy trong các phân tử ATP để cung cấp cho hoạt động sống.",
                "source": "KHTN 7 KNTT",
                "page": 103
            },
            {
                "id": 6,
                "difficulty": "Thông hiểu",
                "question": "Khí khổng ở mặt dưới của lá mở ra giúp ích gì cho quá trình quang hợp?",
                "options": [
                    "Giúp rễ hút thêm muối khoáng",
                    "Giúp khí $CO_2$ khuếch tán vào trong lá và giải phóng khí $O_2$ ra môi trường",
                    "Ngăn cản ánh sáng mặt trời chiếu vào lá",
                    "Ngăn chặn sự thoát hơi nước"
                ],
                "answer_index": 1,
                "explanation": "Khí khổng là cửa ngõ trao đổi khí chủ yếu, cho CO2 đi vào phục vụ quang hợp và thoát O2 cùng hơi nước.",
                "evidence": "Khí khổng mở giúp khí carbon dioxide khuếch tán vào lá và khí oxygen thoát ra ngoài.",
                "source": "KHTN 7 KNTT",
                "page": 97
            },
            {
                "id": 7,
                "difficulty": "Vận dụng",
                "question": "Vì sao ban đêm không nên đặt nhiều chậu hoa hoặc cây cảnh trong phòng ngủ đóng kín cửa?",
                "options": [
                    "Vì ban đêm cây xanh không quang hợp mà chỉ hô hấp, lấy đi $O_2$ và thải ra nhiều $CO_2$ gây ngạt khí",
                    "Vì ban đêm cây tỏa ra nhiệt lượng rất lớn làm phòng nóng bức",
                    "Vì ban đêm cây xanh thải ra nhiều khí độc hại như lưu huỳnh",
                    "Vì mùi hương của lá cây thu hút nhiều loài côn trùng có hại"
                ],
                "answer_index": 0,
                "explanation": "Vào ban đêm không có ánh sáng, cây chỉ diễn ra quá trình hô hấp làm giảm nồng độ O2 và tăng nồng độ CO2 trong không gian kín.",
                "evidence": "Vào ban đêm cây không quang hợp mà chỉ hô hấp lấy oxygen và thải carbon dioxide.",
                "source": "KHTN 7 KNTT",
                "page": 105
            },
            {
                "id": 8,
                "difficulty": "Thông hiểu",
                "question": "Mối quan hệ giữa quang hợp và hô hấp tế bào ở thực vật là:",
                "options": [
                    "Hai quá trình hoàn toàn độc lập, không liên quan đến nhau",
                    "Quang hợp tổng hợp chất hữu cơ tích lũy năng lượng, hô hấp phân giải chất hữu cơ giải phóng năng lượng",
                    "Quang hợp và hô hấp đều giải phóng cùng một loại khí giống nhau",
                    "Quang hợp chỉ xảy ra ở rễ, hô hấp chỉ xảy ra ở lá cây"
                ],
                "answer_index": 1,
                "explanation": "Quang hợp và hô hấp là hai mặt đối lập nhưng thống nhất mật thiết trong quá trình trao đổi chất và chuyển hóa năng lượng.",
                "evidence": "Quang hợp tạo ra chất hữu cơ và oxygen là nguyên liệu cho hô hấp; ngược lại hô hấp tạo ra CO2 và nước cho quang hợp.",
                "source": "KHTN 7 KNTT",
                "page": 106
            },
            {
                "id": 9,
                "difficulty": "Vận dụng",
                "question": "Khi bảo quản nông sản (hạt thóc, ngô, đậu), việc phơi khô hạt trước khi cất trữ nhằm mục đích chính là gì?",
                "options": [
                    "Làm hạt nhẹ hơn để dễ vận chuyển",
                    "Giảm hàm lượng nước trong hạt để ức chế hô hấp tế bào, tránh hao hụt chất dinh dưỡng và ẩm mốc",
                    "Tăng tốc độ nảy mầm của hạt giống",
                    "Làm hạt có màu sắc đẹp mắt hơn"
                ],
                "answer_index": 1,
                "explanation": "Độ ẩm thấp làm giảm thiểu cường độ hô hấp tế bào của phôi hạt về mức tối thiểu, giúp duy trì sức sống lâu dài.",
                "evidence": "Phơi khô hạt làm giảm độ ẩm nhằm hạn chế hô hấp tế bào, giúp bảo quản hạt lâu dài.",
                "source": "KHTN 7 KNTT",
                "page": 107
            },
            {
                "id": 10,
                "difficulty": "Thông hiểu",
                "question": "Cường độ quang hợp của cây xanh thường đạt mức tối ưu trong điều kiện nào?",
                "options": [
                    "Nhiệt độ đóng băng dưới $0^\circ\\text{C}$",
                    "Ánh sáng phù hợp, đủ nước, nồng độ $CO_2$ vừa phải và nhiệt độ thích hợp ($25 - 35^\circ\\text{C}$)",
                    "Trong bóng tối hoàn toàn kéo dài nhiều ngày",
                    "Khi độ ẩm không khí giảm về $0\\%$"
                ],
                "answer_index": 1,
                "explanation": "Quang hợp phụ thuộc chặt chẽ vào ánh sáng, nồng độ CO2, hàm lượng nước và nhiệt độ tối ưu của enzym quang hợp.",
                "evidence": "Các yếu tố ánh sáng, nồng độ carbon dioxide, nước và nhiệt độ ảnh hưởng trực tiếp đến quang hợp.",
                "source": "KHTN 7 KNTT",
                "page": 99
            }
        ]
    },
    {
        "id": "k7-midterm-tong-hop",
        "grade": 7,
        "type": "midterm",
        "type_label": "Kiểm tra Giữa kỳ 1",
        "title": "Kiểm tra Giữa kỳ 1 KHTN 7: Trao đổi chất, Năng lượng, Từ trường & Tốc độ",
        "topic": "Trao đổi chất và năng lượng, Tốc độ chuyển động, Từ trường",
        "duration_minutes": 45,
        "questions_count": 20,
        "description": "Đề kiểm tra giữa kì 1 tích hợp Sinh học (quang hợp, hô hấp, trao đổi nước) và Vật lý (tốc độ, đồ thị quãng đường - thời gian, từ trường nam châm).",
        "questions": [
            {
                "id": 1,
                "difficulty": "Nhận biết",
                "question": "Công thức tính tốc độ chuyển động của một vật là gì?",
                "options": ["$v = s \\times t$", "$v = \\frac{s}{t}$", "$v = \\frac{t}{s}$", "$v = s + t$"],
                "answer_index": 1,
                "explanation": "Tốc độ $v$ bằng quãng đường $s$ chia cho thời gian $t$ đi hết quãng đường đó.",
                "evidence": "Tốc độ được tính bằng công thức v = s / t.",
                "source": "KHTN 7 KNTT",
                "page": 38
            },
            {
                "id": 2,
                "difficulty": "Thông hiểu",
                "question": "Một người đi xe đạp đi được quãng đường $s = 36\\text{ km}$ trong thời gian $t = 2\\text{ giờ}$. Tốc độ của người đó là:",
                "options": ["$18\\text{ km/h}$", "$72\\text{ km/h}$", "$38\\text{ km/h}$", "$12\\text{ km/h}$"],
                "answer_index": 0,
                "explanation": "$v = \\frac{s}{t} = \\frac{36}{2} = 18\\text{ km/h}$.",
                "evidence": "Tốc độ bằng quãng đường chia cho thời gian: v = s / t.",
                "source": "KHTN 7 KNTT",
                "page": 39
            },
            {
                "id": 3,
                "difficulty": "Nhận biết",
                "question": "Đơn vị hợp pháp của tốc độ trong hệ SI là:",
                "options": ["km/h", "m/s", "cm/s", "m/phút"],
                "answer_index": 1,
                "explanation": "Đơn vị đo tốc độ trong hệ SI là mét trên giây (m/s).",
                "evidence": "Đơn vị đo tốc độ trong hệ SI là mét trên giây (m/s).",
                "source": "KHTN 7 KNTT",
                "page": 39
            },
            {
                "id": 4,
                "difficulty": "Thông hiểu",
                "question": "Đổi tốc độ $10\\text{ m/s}$ sang đơn vị $\\text{km/h}$ ta được kết quả là:",
                "options": ["$10\\text{ km/h}$", "$18\\text{ km/h}$", "$36\\text{ km/h}$", "$100\\text{ km/h}$"],
                "answer_index": 2,
                "explanation": "$1\\text{ m/s} = 3.6\\text{ km/h} \\implies 10\\text{ m/s} = 36\\text{ km/h}$.",
                "evidence": "1 m/s = 3.6 km/h.",
                "source": "KHTN 7 KNTT",
                "page": 40
            },
            {
                "id": 5,
                "difficulty": "Nhận biết",
                "question": "Nam châm vĩnh cửu có hai cực từ là:",
                "options": ["Cực âm và Cực dương", "Cực Bắc (N) và Cực Nam (S)", "Cực nóng và Cực lạnh", "Cực đẩy và Cực hút"],
                "answer_index": 1,
                "explanation": "Mỗi nam châm luôn có hai cực từ: Cực Bắc (kí hiệu N - North) và Cực Nam (kí hiệu S - South).",
                "evidence": "Mỗi nam châm đều có hai cực: cực Bắc (N) và cực Nam (S).",
                "source": "KHTN 7 KNTT",
                "page": 80
            },
            {
                "id": 6,
                "difficulty": "Thông hiểu",
                "question": "Khi đặt hai cực cùng tên của hai nam châm lại gần nhau thì chúng sẽ:",
                "options": ["Hút nhau", "Đẩy nhau", "Không tương tác gì", "Lúc hút lúc đẩy"],
                "answer_index": 1,
                "explanation": "Quy tắc tương tác từ: các cực cùng tên đẩy nhau, các cực khác tên hút nhau.",
                "evidence": "Các cực từ cùng tên thì đẩy nhau, khác tên thì hút nhau.",
                "source": "KHTN 7 KNTT",
                "page": 81
            },
            {
                "id": 7,
                "difficulty": "Nhận biết",
                "question": "Từ trường tồn tại ở không gian nào sau đây?",
                "options": [
                    "Xung quanh nam châm hoặc xung quanh dòng điện",
                    "Chỉ trong lòng đất sâu",
                    "Chỉ xung quanh các vật nhiễm điện đứng yên",
                    "Chỉ ở môi trường chân không tuyệt đối"
                ],
                "answer_index": 0,
                "explanation": "Từ trường là dạng vật chất tồn tại xung quanh nam châm hoặc dòng điện và tác dụng lực từ lên nam châm khác đặt trong nó.",
                "evidence": "Không gian xung quanh nam châm, xung quanh dòng điện có từ trường.",
                "source": "KHTN 7 KNTT",
                "page": 83
            },
            {
                "id": 8,
                "difficulty": "Thông hiểu",
                "question": "Đường sức từ ở bên ngoài thanh nam châm có chiều quy ước là:",
                "options": [
                    "Vào cực Bắc, Ra cực Nam",
                    "Ra cực Bắc (N), Vào cực Nam (S)",
                    "Luôn hướng thẳng đứng lên trên",
                    "Chạy vòng tròn không xác định cực"
                ],
                "answer_index": 1,
                "explanation": "Quy ước chiều đường sức từ bên ngoài nam châm: \"Vào Nam, Ra Bắc\" (Đi ra từ cực Bắc N và đi vào ở cực Nam S).",
                "evidence": "Bên ngoài nam châm, đường sức từ đi ra từ cực Bắc và đi vào ở cực Nam.",
                "source": "KHTN 7 KNTT",
                "page": 85
            },
            {
                "id": 9,
                "difficulty": "Nhận biết",
                "question": "Nước và chất khoáng được vận chuyển từ rễ lên lá cây qua cấu trúc nào?",
                "options": ["Mạch rây", "Mạch gỗ", "Tế bào biểu bì", "Không bào"],
                "answer_index": 1,
                "explanation": "Mạch gỗ (xylem) chuyên chở dòng nhựa nguyên gồm nước và muối khoáng từ rễ lên lá.",
                "evidence": "Nước và chất khoáng được vận chuyển từ rễ lên thân và lá nhờ mạch gỗ.",
                "source": "KHTN 7 KNTT",
                "page": 110
            },
            {
                "id": 10,
                "difficulty": "Thông hiểu",
                "question": "Dòng chất hữu cơ do lá quang hợp tạo ra được vận chuyển xuống các cơ quan khác nhờ:",
                "options": ["Mạch gỗ", "Mạch rây", "Lông hút", "Khí khổng"],
                "answer_index": 1,
                "explanation": "Mạch rây (phloem) vận chuyển dòng nhựa luyện chứa đường và hợp chất hữu cơ từ lá đến các bộ phận sử dụng hoặc dự trữ.",
                "evidence": "Các chất hữu cơ tổng hợp ở lá được vận chuyển đến các bộ phận khác nhờ mạch rây.",
                "source": "KHTN 7 KNTT",
                "page": 111
            },
            {
                "id": 11,
                "difficulty": "Thông hiểu",
                "question": "Động lực chính thúc đẩy dòng nước và ion khoáng di chuyển liên tục từ rễ lên đỉnh ngọn cây là:",
                "options": [
                    "Lực thoát hơi nước ở lá cây",
                    "Lực ma sát của thân cây",
                    "Trọng lực của Trái Đất",
                    "Sự chuyển động của gió ngoài môi trường"
                ],
                "answer_index": 0,
                "explanation": "Sự thoát hơi nước qua khí khổng tạo ra sức hút nước cực mạnh từ trên ngọn kéo dòng nước trong mạch gỗ lên cao.",
                "evidence": "Thoát hơi nước ở lá tạo động lực đầu trên kéo dòng nước và muối khoáng từ rễ lên.",
                "source": "KHTN 7 KNTT",
                "page": 113
            },
            {
                "id": 12,
                "difficulty": "Nhận biết",
                "question": "Dụng cụ dùng để xác định phương hướng dựa trên từ trường của Trái Đất là:",
                "options": ["Lực kế", "La bàn", "Tốc kế", "Nhiệt kế"],
                "answer_index": 1,
                "explanation": "La bàn có kim nam châm tự do luôn định hướng theo trục Bắc - Nam từ trường Trái Đất.",
                "evidence": "La bàn dùng để xác định phương hướng dựa vào từ trường Trái Đất.",
                "source": "KHTN 7 KNTT",
                "page": 87
            },
            {
                "id": 13,
                "difficulty": "Vận dụng",
                "question": "Một xe ô tô chạy trên đường cao tốc với tốc độ $90\\text{ km/h}$. Thời gian để xe chạy hết quãng đường $45\\text{ km}$ là:",
                "options": ["$0.5\\text{ giờ}$ (30 phút)", "$2\\text{ giờ}$", "$1.5\\text{ giờ}$", "$45\\text{ phút}$"],
                "answer_index": 0,
                "explanation": "$t = \\frac{s}{v} = \\frac{45}{90} = 0.5\\text{ giờ} = 30\\text{ phút}$.",
                "evidence": "Thời gian được tính bằng t = s / v.",
                "source": "KHTN 7 KNTT",
                "page": 41
            },
            {
                "id": 14,
                "difficulty": "Thông hiểu",
                "question": "Nam châm điện có cấu tạo cơ bản gồm:",
                "options": [
                    "Một thanh thép vĩnh cửu",
                    "Một cuộn dây dẫn quấn quanh lõi sắt non có dòng điện chạy qua",
                    "Hai thanh đồng đặt song song",
                    "Một lá nhôm mỏng gắn pin"
                ],
                "answer_index": 1,
                "explanation": "Khi có dòng điện chạy qua cuộn dây có lõi sắt non, lõi sắt bị từ hóa tạo thành nam châm điện có lực hút từ rất mạnh.",
                "evidence": "Nam châm điện gồm cuộn dây dẫn quấn quanh lõi sắt non khi có dòng điện chạy qua.",
                "source": "KHTN 7 KNTT",
                "page": 89
            },
            {
                "id": 15,
                "difficulty": "Vận dụng",
                "question": "Ưu điểm lớn nhất của nam châm điện so với nam châm vĩnh cửu trong ứng dụng công nghiệp là gì?",
                "options": [
                    "Không bao giờ bị hỏng",
                    "Có thể bật/tắt từ tính dễ dàng bằng cách đóng/ngắt dòng điện và điều chỉnh được độ mạnh yếu của lực từ",
                    "Không cần dùng kim loại",
                    "Luôn luôn có kích thước nhỏ gọn hơn"
                ],
                "answer_index": 1,
                "explanation": "Chỉ cần ngắt dòng điện là nam châm điện mất từ tính, rất thuận tiện để bốc thả hàng ngàn tấn phế liệu kim loại trong các nhà máy.",
                "evidence": "Từ tính của nam châm điện có thể thay đổi bằng cách thay đổi cường độ dòng điện hoặc ngắt điện.",
                "source": "KHTN 7 KNTT",
                "page": 90
            },
            {
                "id": 16,
                "difficulty": "Nhận biết",
                "question": "Yếu tố nào sau đây kích thích sự mở ra của khí khổng ở lá cây vào ban ngày?",
                "options": ["Bóng tối", "Ánh sáng", "Nhiệt độ rất lạnh", "Không khí thiếu oxygen"],
                "answer_index": 1,
                "explanation": "Khi có ánh sáng, tế bào hạt đậu hút nước no trương làm khí khổng mở ra để thực hiện quang hợp và trao đổi khí.",
                "evidence": "Ánh sáng là yếu tố quan trọng kích thích khí khổng mở ra vào ban ngày.",
                "source": "KHTN 7 KNTT",
                "page": 98
            },
            {
                "id": 17,
                "difficulty": "Thông hiểu",
                "question": "Đồ thị quãng đường - thời gian của một vật chuyển động với tốc độ không đổi là một đường:",
                "options": ["Đường tròn", "Đường thẳng nằm nghiêng", "Đường parabol", "Đường gợn sóng"],
                "answer_index": 1,
                "explanation": "Khi tốc độ không đổi, quãng đường tỉ lệ thuận với thời gian nên đồ thị biểu diễn là một đường thẳng xiên góc.",
                "evidence": "Đồ thị quãng đường - thời gian của chuyển động với tốc độ không đổi là một đường thẳng.",
                "source": "KHTN 7 KNTT",
                "page": 44
            },
            {
                "id": 18,
                "difficulty": "Vận dụng",
                "question": "Khi tưới cây trong những ngày hè nắng gắt giữa trưa, vì sao không nên tưới nước trực tiếp lên mặt lá?",
                "options": [
                    "Vì các giọt nước đọng trên lá có tác dụng như thấu kính hội tụ ánh sáng mặt trời làm cháy lá, đồng thời nước bốc hơi nhanh làm tăng nhiệt độ xung quanh",
                    "Vì nước làm tan rã chất diệp lục ngay lập tức",
                    "Vì nước ngăn cản rễ cây phát triển",
                    "Vì lá cây sẽ hút quá nhiều nước làm vỡ tế bào"
                ],
                "answer_index": 0,
                "explanation": "Giọt nước trên mặt lá như thấu kính hội tụ chùm sáng mặt trời đốt cháy mô lá; ngoài ra đất đang nóng gặp nước lạnh gây sốc nhiệt cho rễ.",
                "evidence": "Tưới nước giữa trưa nắng gắt làm cây bị sốc nhiệt và giọt nước đọng gây cháy lá.",
                "source": "KHTN 7 KNTT",
                "page": 116
            },
            {
                "id": 19,
                "difficulty": "Nhận biết",
                "question": "Âm thanh truyền được trong những môi trường nào sau đây?",
                "options": [
                    "Chất rắn, chất lỏng và chất khí",
                    "Chỉ trong chất khí",
                    "Chất rắn, chất lỏng, chất khí và cả chân không",
                    "Chỉ trong môi trường chân không"
                ],
                "answer_index": 0,
                "explanation": "Âm thanh là sự lan truyền dao động cơ học nên bắt buộc phải có môi trường vật chất (rắn, lỏng, khí), không truyền được trong chân không.",
                "evidence": "Âm truyền được trong các môi trường chất rắn, chất lỏng, chất khí và không truyền được trong chân không.",
                "source": "KHTN 7 KNTT",
                "page": 58
            },
            {
                "id": 20,
                "difficulty": "Thông hiểu",
                "question": "Vận tốc truyền âm trong các môi trường được sắp xếp theo thứ tự giảm dần là:",
                "options": [
                    "Chất rắn > Chất lỏng > Chất khí",
                    "Chất khí > Chất lỏng > Chất rắn",
                    "Chất lỏng > Chất rắn > Chất khí",
                    "Chất khí > Chất rắn > Chất lỏng"
                ],
                "answer_index": 0,
                "explanation": "Mật độ phân tử chất rắn dày đặc nhất nên dao động truyền đi nhanh nhất, kế đến là chất lỏng và chậm nhất là chất khí.",
                "evidence": "Tốc độ truyền âm trong chất rắn lớn hơn trong chất lỏng, trong chất lỏng lớn hơn trong chất khí.",
                "source": "KHTN 7 KNTT",
                "page": 59
            }
        ]
    },

    # =========================================================================
    # LỚP 8
    # =========================================================================
    {
        "id": "k8-15p-tuan-hoan-ho-hap",
        "grade": 8,
        "type": "15p",
        "type_label": "Kiểm tra 15 phút",
        "title": "Kiểm tra 15 phút: Hệ tuần hoàn máu và Hệ hô hấp ở người",
        "topic": "Máu và hệ tuần hoàn ở người, Hệ hô hấp ở người",
        "duration_minutes": 15,
        "questions_count": 10,
        "description": "Kiểm tra cấu tạo và chức năng của máu, tim, hệ mạch, nguyên tắc truyền máu và sự trao đổi khí ở phổi.",
        "questions": [
            {
                "id": 1,
                "difficulty": "Nhận biết",
                "question": "Máu ở người trưởng thành gồm hai thành phần chính nào?",
                "options": [
                    "Huyết tương và các tế bào máu",
                    "Nước và muối khoáng",
                    "Hồng cầu và bạch cầu",
                    "Kháng thể và chất dinh dưỡng"
                ],
                "answer_index": 0,
                "explanation": "Máu gồm 55% huyết tương (chủ yếu là nước và chất hòa tan) và 45% các tế bào máu (hồng cầu, bạch cầu, tiểu cầu).",
                "evidence": "Máu gồm hai thành phần chính là huyết tương và các tế bào máu.",
                "source": "KHTN 8 KNTT",
                "page": 125
            },
            {
                "id": 2,
                "difficulty": "Nhận biết",
                "question": "Loại tế bào máu nào chiếm số lượng lớn nhất và có chức năng vận chuyển khí $O_2$ và $CO_2$?",
                "options": ["Bạch cầu", "Hồng cầu", "Tiểu cầu", "Tế bào lympho"],
                "answer_index": 1,
                "explanation": "Hồng cầu chứa huyết sắc tố hemoglobin có khả năng kết hợp thuận nghịch với O2 và CO2.",
                "evidence": "Hồng cầu chứa hemoglobin có chức năng vận chuyển oxygen và carbon dioxide.",
                "source": "KHTN 8 KNTT",
                "page": 126
            },
            {
                "id": 3,
                "difficulty": "Thông hiểu",
                "question": "Tiểu cầu đóng vai trò then chốt trong quá trình sinh học nào sau đây?",
                "options": [
                    "Vận chuyển chất dinh dưỡng",
                    "Đông máu giúp bảo vệ cơ thể chống mất máu khi bị thương",
                    "Tiêu diệt vi khuẩn gây bệnh bằng thực bào",
                    "Điều hòa thân nhiệt"
                ],
                "answer_index": 1,
                "explanation": "Tiểu cầu giải phóng enzym thrombokinase kích hoạt chuỗi phản ứng hình thành khối máu đông bịt kín vết thương.",
                "evidence": "Tiểu cầu tham gia vào quá trình đông máu để bảo vệ cơ thể chống mất máu.",
                "source": "KHTN 8 KNTT",
                "page": 128
            },
            {
                "id": 4,
                "difficulty": "Nhận biết",
                "question": "Tim người có cấu tạo gồm mấy ngăn?",
                "options": ["2 ngăn", "3 ngăn", "4 ngăn (2 tâm nhĩ, 2 tâm thất)", "5 ngăn"],
                "answer_index": 2,
                "explanation": "Tim người gồm 4 ngăn: tâm nhĩ phải, tâm nhĩ trái ở trên; tâm thất phải, tâm thất trái ở dưới.",
                "evidence": "Tim người gồm có bốn ngăn: hai tâm nhĩ ở trên và hai tâm thất ở dưới.",
                "source": "KHTN 8 KNTT",
                "page": 130
            },
            {
                "id": 5,
                "difficulty": "Thông hiểu",
                "question": "Mạch máu nào mang máu giàu oxy ($O_2$) từ tim đi nuôi dưỡng tất cả các cơ quan trong cơ thể?",
                "options": ["Động mạch phổi", "Động mạch chủ", "Tĩnh mạch chủ", "Tĩnh mạch phổi"],
                "answer_index": 1,
                "explanation": "Tâm thất trái co bóp đẩy máu đỏ tươi giàu O2 vào động mạch chủ để phân phối tới các cơ quan trong vòng tuần hoàn lớn.",
                "evidence": "Động mạch chủ dẫn máu giàu oxygen từ tâm thất trái đi nuôi cơ thể.",
                "source": "KHTN 8 KNTT",
                "page": 131
            },
            {
                "id": 6,
                "difficulty": "Thông hiểu",
                "question": "Theo hệ nhóm máu ABO, người mang nhóm máu O có thể truyền máu an toàn cho người mang nhóm máu nào?",
                "options": [
                    "Chỉ người nhóm máu O",
                    "Chỉ người nhóm máu AB",
                    "Tất cả các nhóm máu A, B, AB và O",
                    "Chỉ người nhóm máu A và B"
                ],
                "answer_index": 2,
                "explanation": "Hồng cầu nhóm máu O không có kháng nguyên A và B trên bề mặt nên không bị ngưng kết bởi kháng thể trong huyết tương người nhận.",
                "evidence": "Nhóm máu O là nhóm máu chuyên cho, có thể truyền cho các nhóm máu A, B, AB, O.",
                "source": "KHTN 8 KNTT",
                "page": 129
            },
            {
                "id": 7,
                "difficulty": "Nhận biết",
                "question": "Quá trình trao đổi khí giữa máu và không khí diễn ra tại cấu trúc nào của phổi?",
                "options": ["Phế quản", "Khí quản", "Các phế nang", "Thanh quản"],
                "answer_index": 2,
                "explanation": "Phế nang có thành mỏng và được bao bọc bởi mạng lưới mao mạch dày đặc, nơi diễn ra khuếch tán O2 và CO2.",
                "evidence": "Sự trao đổi khí ở phổi diễn ra tại các phế nang.",
                "source": "KHTN 8 KNTT",
                "page": 138
            },
            {
                "id": 8,
                "difficulty": "Thông hiểu",
                "question": "Huyết áp là gì?",
                "options": [
                    "Áp lực của dòng máu tác dụng lên thành mạch máu khi tim co bóp và giãn",
                    "Tốc độ chảy của máu trong tĩnh mạch",
                    "Số lần đập của tim trong một phút",
                    "Lượng máu bơm ra trong một chu kì"
                ],
                "answer_index": 0,
                "explanation": "Huyết áp là áp lực máu tác động lên thành mạch, gồm huyết áp tâm thu (tối đa) và huyết áp tâm trương (tối thiểu).",
                "evidence": "Huyết áp là áp lực của máu tác dụng lên thành mạch.",
                "source": "KHTN 8 KNTT",
                "page": 133
            },
            {
                "id": 9,
                "difficulty": "Vận dụng",
                "question": "Một người có chỉ số huyết áp đo được là 155/95 mmHg thì người đó có nguy cơ mắc bệnh gì?",
                "options": ["Huyết áp thấp", "Tăng huyết áp (Cao huyết áp)", "Thiếu máu", "Hạ đường huyết"],
                "answer_index": 1,
                "explanation": "Huyết áp bình thường khoảng 110-120/70-80 mmHg. Huyết áp tâm thu $\\ge 140\\text{ mmHg}$ hoặc tâm trương $\\ge 90\\text{ mmHg}$ là dấu hiệu cao huyết áp.",
                "evidence": "Người có huyết áp tâm thu từ 140 mmHg trở lên hoặc tâm trương từ 90 mmHg trở lên bị cao huyết áp.",
                "source": "KHTN 8 KNTT",
                "page": 134
            },
            {
                "id": 10,
                "difficulty": "Vận dụng",
                "question": "Vì sao khi lao động nặng hoặc chạy cự li dài, nhịp thở và nhịp tim của con người đều tăng mạnh?",
                "options": [
                    "Để tế bào cơ bắp nhận được nhiều oxy và dinh dưỡng hơn, đồng thời nhanh chóng đào thải $CO_2$ và nhiệt năng ra ngoài",
                    "Để cơ thể không bị mất nước",
                    "Để giảm bớt huyết áp trong cơ thể",
                    "Để làm tăng lượng hồng cầu trong tủy xương ngay lập tức"
                ],
                "answer_index": 0,
                "explanation": "Khi vận động mạnh, các tế bào cơ tiêu hao năng lượng và O2 nhiều gấp bội, đòi hỏi tim phải bơm máu nhanh hơn và phổi thở dồn dập hơn.",
                "evidence": "Khi vận động mạnh, tim đập nhanh và thở sâu để đáp ứng nhu cầu oxygen và đào thải CO2 của tế bào.",
                "source": "KHTN 8 KNTT",
                "page": 135
            }
        ]
    },
    {
        "id": "k8-midterm-tong-hop",
        "grade": 8,
        "type": "midterm",
        "type_label": "Kiểm tra Giữa kỳ 1",
        "title": "Kiểm tra Giữa kỳ 1 KHTN 8: Phản ứng hóa học, Bảo toàn khối lượng & Áp suất",
        "topic": "Phản ứng hóa học, Định luật bảo toàn khối lượng, Áp suất",
        "duration_minutes": 45,
        "questions_count": 20,
        "description": "Đề kiểm tra giữa kì 1 tích hợp Hóa học (biến đổi chất, PTHH, định luật bảo toàn khối lượng, mol) và Vật lý (áp lực, áp suất chất lỏng, áp suất khí quyển).",
        "questions": [
            {
                "id": 1,
                "difficulty": "Nhận biết",
                "question": "Hiện tượng nào sau đây là hiện tượng hóa học?",
                "options": [
                    "Băng tan thành nước lỏng ở nhiệt độ phòng",
                    "Đinh sắt để ngoài không khí ẩm bị gỉ sét màu nâu đỏ",
                    "Hòa tan đường vào nước được dung dịch nước đường",
                    "Cồn bay hơi khi mở nắp lọ"
                ],
                "answer_index": 1,
                "explanation": "Đinh sắt bị gỉ tạo thành chất mới là gỉ sắt (oxit sắt), đó là hiện tượng hóa học.",
                "evidence": "Hiện tượng chất biến đổi tạo ra chất mới gọi là hiện tượng hóa học.",
                "source": "KHTN 8 KNTT",
                "page": 12
            },
            {
                "id": 2,
                "difficulty": "Nhận biết",
                "question": "Định luật bảo toàn khối lượng phát biểu rằng: Trong một phản ứng hóa học,",
                "options": [
                    "Tổng khối lượng các chất sản phẩm bằng tổng khối lượng các chất tham gia phản ứng",
                    "Khối lượng các chất sản phẩm luôn lớn hơn chất tham gia",
                    "Khối lượng các chất sản phẩm luôn nhỏ hơn chất tham gia",
                    "Số lượng phân tử sản phẩm luôn bằng số phân tử tham gia"
                ],
                "answer_index": 0,
                "explanation": "Nguyên tử chỉ sắp xếp lại liên kết, số lượng từng loại nguyên tử không đổi nên tổng khối lượng được bảo toàn tuyệt đối.",
                "evidence": "Trong một phản ứng hóa học, tổng khối lượng của các chất sản phẩm bằng tổng khối lượng của các chất tham gia phản ứng.",
                "source": "KHTN 8 KNTT",
                "page": 18
            },
            {
                "id": 3,
                "difficulty": "Thông hiểu",
                "question": "Đốt cháy hoàn toàn $6\\text{ g}$ kim loại magie (Mg) trong khí oxy ($O_2$) thu được $10\\text{ g}$ magie oxit (MgO). Khối lượng khí oxy đã phản ứng là:",
                "options": ["$16\\text{ g}$", "$4\\text{ g}$", "$8\\text{ g}$", "$2\\text{ g}$"],
                "answer_index": 1,
                "explanation": "$m_{\\text{Mg}} + m_{O_2} = m_{\\text{MgO}} \\implies m_{O_2} = 10 - 6 = 4\\text{ g}$.",
                "evidence": "Theo định luật bảo toàn khối lượng: m_tham gia = m_sản phẩm.",
                "source": "KHTN 8 KNTT",
                "page": 19
            },
            {
                "id": 4,
                "difficulty": "Nhận biết",
                "question": "Một mol chất chứa bao nhiêu nguyên tử hoặc phân tử chất đó?",
                "options": [
                    "$6.022 \\times 10^{23}$ hạt (Hằng số Avogadro $N_A$)",
                    "$6.022 \\times 10^{22}$ hạt",
                    "$10^{23}$ hạt",
                    "$3.14 \\times 10^{23}$ hạt"
                ],
                "answer_index": 0,
                "explanation": "Mol là lượng chất chứa $N_A \\approx 6.022 \\times 10^{23}$ nguyên tử hoặc phân tử của chất đó.",
                "evidence": "Mol là lượng chất có chứa 6.022 x 10^23 nguyên tử hoặc phân tử của chất đó.",
                "source": "KHTN 8 KNTT",
                "page": 24
            },
            {
                "id": 5,
                "difficulty": "Thông hiểu",
                "question": "Ở điều kiện chuẩn ($25^\\circ\\text{C}$ và $1\\text{ bar}$), thể tích của $1\\text{ mol}$ chất khí bất kì bằng bao nhiêu?",
                "options": ["$22.4\\text{ lít}$", "$24.79\\text{ lít}$", "$2.479\\text{ lít}$", "$24\\text{ lít}$"],
                "answer_index": 1,
                "explanation": "Theo chương trình GDPT 2018 KNTT, ở điều kiện chuẩn ($25^\circ\\text{C}, 1\\text{ bar}$), $1\\text{ mol}$ khí chiếm thể tích $24.79\\text{ lít}$.",
                "evidence": "Ở điều kiện chuẩn (25 độ C và 1 bar), 1 mol chất khí bất kì đều chiếm thể tích là 24.79 lít.",
                "source": "KHTN 8 KNTT",
                "page": 26
            },
            {
                "id": 6,
                "difficulty": "Vận dụng",
                "question": "Thể tích của $0.5\\text{ mol}$ khí $CO_2$ ở điều kiện chuẩn ($25^\\circ\\text{C}, 1\\text{ bar}$) là:",
                "options": ["$12.395\\text{ lít}$", "$11.2\\text{ lít}$", "$24.79\\text{ lít}$", "$49.58\\text{ lít}$"],
                "answer_index": 0,
                "explanation": "$V = n \\times 24.79 = 0.5 \\times 24.79 = 12.395\\text{ lít}$.",
                "evidence": "Công thức tính thể tích khí ở điều kiện chuẩn: V = n x 24.79.",
                "source": "KHTN 8 KNTT",
                "page": 27
            },
            {
                "id": 7,
                "difficulty": "Nhận biết",
                "question": "Áp lực là gì?",
                "options": [
                    "Lực ép có phương vuông góc với mặt bị ép",
                    "Lực ma sát cản trở chuyển động",
                    "Lực hút của Trái Đất",
                    "Lực kéo tiếp tuyến với mặt tiếp xúc"
                ],
                "answer_index": 0,
                "explanation": "Áp lực là lực ép có phương vuông góc với bề mặt bị ép.",
                "evidence": "Áp lực là lực ép có phương vuông góc với mặt bị ép.",
                "source": "KHTN 8 KNTT",
                "page": 64
            },
            {
                "id": 8,
                "difficulty": "Thông hiểu",
                "question": "Công thức tính áp suất là gì?",
                "options": ["$p = F \\times S$", "$p = \\frac{F}{S}$", "$p = \\frac{S}{F}$", "$p = F + S$"],
                "answer_index": 1,
                "explanation": "Áp suất $p$ được tính bằng độ lớn áp lực $F$ trên một đơn vị diện tích bị ép $S$: $p = \\frac{F}{S}$.",
                "evidence": "Áp suất được tính bằng công thức p = F / S.",
                "source": "KHTN 8 KNTT",
                "page": 65
            },
            {
                "id": 9,
                "difficulty": "Nhận biết",
                "question": "Đơn vị đo của áp suất trong hệ SI là:",
                "options": ["Niu-tơn (N)", "Pas-can (Pa) hoặc $\\text{N/m}^2$", "Jun (J)", "Kilôgam (kg)"],
                "answer_index": 1,
                "explanation": "Đơn vị áp suất là Pascal ($1\\text{ Pa} = 1\\text{ N/m}^2$).",
                "evidence": "Đơn vị của áp suất là paxcan, kí hiệu là Pa (1 Pa = 1 N/m^2).",
                "source": "KHTN 8 KNTT",
                "page": 65
            },
            {
                "id": 10,
                "difficulty": "Vận dụng",
                "question": "Một người có trọng lượng $600\\text{ N}$ đứng bằng hai chân trên sàn, diện tích tiếp xúc của cả hai bàn chân là $0.03\\text{ m}^2$. Áp suất người đó tác dụng lên sàn là:",
                "options": ["$200\\text{ Pa}$", "$18000\\text{ Pa}$", "$20000\\text{ Pa}$", "$2000\\text{ Pa}$"],
                "answer_index": 2,
                "explanation": "$p = \\frac{F}{S} = \\frac{600}{0.03} = 20000\\text{ Pa}$.",
                "evidence": "Áp suất tính bằng p = F / S.",
                "source": "KHTN 8 KNTT",
                "page": 66
            },
            {
                "id": 11,
                "difficulty": "Thông hiểu",
                "question": "Vì sao lưỡi dao, mũi kim, lưỡi kéo đều được mài rất sắc và nhọn?",
                "options": [
                    "Để giảm khối lượng của dao, kéo",
                    "Để làm giảm diện tích bị ép $S$, từ đó làm tăng áp suất giúp cắt gọt dễ dàng",
                    "Để tăng diện tích tiếp xúc $S$",
                    "Để làm giảm áp lực tác dụng lên vật"
                ],
                "answer_index": 1,
                "explanation": "Khi $S$ rất nhỏ, cùng một lực ép $F$ nhỏ sẽ tạo ra áp suất $p = \\frac{F}{S}$ rất lớn làm xuyên thủng hoặc cắt đứt vật dễ dàng.",
                "evidence": "Giảm diện tích bị ép giúp làm tăng áp suất tác dụng lên vật.",
                "source": "KHTN 8 KNTT",
                "page": 67
            },
            {
                "id": 12,
                "difficulty": "Nhận biết",
                "question": "Áp suất chất lỏng tác dụng lên một vật chìm trong nó có đặc điểm gì?",
                "options": [
                    "Chỉ tác dụng theo phương thẳng đứng từ trên xuống",
                    "Chỉ tác dụng theo phương ngang",
                    "Tác dụng theo mọi phương lên các vật đặt trong lòng chất lỏng",
                    "Chỉ tác dụng lên đáy bình chứa"
                ],
                "answer_index": 2,
                "explanation": "Chất lỏng gây áp suất theo mọi phương lên đáy bình, thành bình và các vật nhúng trong lòng nó.",
                "evidence": "Chất lỏng gây áp suất theo mọi phương lên các vật trong lòng nó.",
                "source": "KHTN 8 KNTT",
                "page": 70
            },
            {
                "id": 13,
                "difficulty": "Thông hiểu",
                "question": "Càng xuống sâu trong lòng nước biển, áp suất chất lỏng thay đổi như thế nào?",
                "options": [
                    "Càng giảm dần",
                    "Càng tăng dần tỉ lệ thuận với độ sâu",
                    "Không thay đổi",
                    "Tăng giảm thất thường"
                ],
                "answer_index": 1,
                "explanation": "Công thức áp suất chất lỏng $p = d \\times h$, độ sâu $h$ càng lớn thì áp suất chất lỏng càng lớn.",
                "evidence": "Càng xuống sâu trong chất lỏng thì áp suất chất lỏng càng tăng.",
                "source": "KHTN 8 KNTT",
                "page": 71
            },
            {
                "id": 14,
                "difficulty": "Vận dụng",
                "question": "Vì sao thợ lặn chuyên nghiệp khi lặn sâu dưới đáy đại dương bắt buộc phải mặc bộ đồ lặn chịu áp lực cao?",
                "options": [
                    "Để bơi nhanh hơn",
                    "Để chống lại áp suất cực lớn của nước biển ở độ sâu lớn ép vào cơ thể",
                    "Để giữ cho cơ thể không bị chìm",
                    "Để ngụy trang tránh cá mập"
                ],
                "answer_index": 1,
                "explanation": "Ở độ sâu hàng trăm mét, áp suất nước biển lên tới hàng chục atm có thể ép vỡ lồng ngực nếu không có đồ lặn chịu áp lực bảo vệ.",
                "evidence": "Người thợ lặn phải mặc áo lặn chịu áp suất để bảo vệ cơ thể khi lặn sâu.",
                "source": "KHTN 8 KNTT",
                "page": 72
            },
            {
                "id": 15,
                "difficulty": "Nhận biết",
                "question": "Lực đẩy Archimedes tác dụng lên một vật nhúng chìm trong chất lỏng có phương và chiều như thế nào?",
                "options": [
                    "Phương ngang, chiều từ trái sang phải",
                    "Phương thẳng đứng, chiều từ dưới lên trên",
                    "Phương thẳng đứng, chiều từ trên xuống dưới",
                    "Phương xiên theo dòng chảy"
                ],
                "answer_index": 1,
                "explanation": "Lực đẩy Ác-si-mét có phương thẳng đứng, chiều hướng từ dưới lên trên ngược với chiều trọng lực.",
                "evidence": "Lực đẩy Acsimet có phương thẳng đứng, chiều hướng từ dưới lên trên.",
                "source": "KHTN 8 KNTT",
                "page": 76
            },
            {
                "id": 16,
                "difficulty": "Thông hiểu",
                "question": "Độ lớn lực đẩy Archimedes phụ thuộc vào hai yếu tố nào?",
                "options": [
                    "Trọng lượng riêng của chất lỏng và Thể tích phần chất lỏng bị vật chiếm chỗ ($F_A = d \\times V$)",
                    "Khối lượng của vật và Hình dạng của vật",
                    "Độ sâu của vật và Nhiệt độ môi trường",
                    "Chất liệu làm nên vật và Vận tốc rơi của vật"
                ],
                "answer_index": 0,
                "explanation": "$F_A = d \\times V$, trong đó $d$ là trọng lượng riêng chất lỏng và $V$ là thể tích phần vật chìm trong chất lỏng.",
                "evidence": "Độ lớn của lực đẩy Acsimet bằng trọng lượng của phần chất lỏng bị vật chiếm chỗ: F_A = d.V.",
                "source": "KHTN 8 KNTT",
                "page": 77
            },
            {
                "id": 17,
                "difficulty": "Nhận biết",
                "question": "Tỉ khối của khí A đối với khí B ($d_{A/B}$) được tính theo công thức:",
                "options": [
                    "$d_{A/B} = \\frac{M_A}{M_B}$",
                    "$d_{A/B} = M_A \\times M_B$",
                    "$d_{A/B} = \\frac{M_B}{M_A}$",
                    "$d_{A/B} = M_A - M_B$"
                ],
                "answer_index": 0,
                "explanation": "Tỉ khối giữa hai chất khí bằng tỉ số giữa khối lượng mol của khí A và khối lượng mol của khí B.",
                "evidence": "Công thức tính tỉ khối của khí A đối với khí B: d_(A/B) = M_A / M_B.",
                "source": "KHTN 8 KNTT",
                "page": 28
            },
            {
                "id": 18,
                "difficulty": "Thông hiểu",
                "question": "Khí metan ($CH_4$, có $M = 16\\text{ g/mol}$) nặng hay nhẹ hơn không khí (xem $M_{\\text{kk}} \\approx 29\\text{ g/mol}$)?",
                "options": [
                    "Nặng hơn không khí",
                    "Nhẹ hơn không khí (khoảng $0.55$ lần)",
                    "Nặng bằng không khí",
                    "Không so sánh được"
                ],
                "answer_index": 1,
                "explanation": "$d_{CH_4/\\text{kk}} = \\frac{16}{29} \\approx 0.55 < 1$, do đó khí metan nhẹ hơn không khí và bay lên cao.",
                "evidence": "Khí có khối lượng mol nhỏ hơn 29 thì nhẹ hơn không khí.",
                "source": "KHTN 8 KNTT",
                "page": 29
            },
            {
                "id": 19,
                "difficulty": "Nhận biết",
                "question": "Dung dịch là gì?",
                "options": [
                    "Hỗn hợp đồng nhất giữa dung môi và chất tan",
                    "Chất lỏng nguyên chất không có tạp chất",
                    "Hỗn hợp không đồng nhất gồm các hạt chất rắn lơ lửng trong chất lỏng",
                    "Hỗn hợp gồm các giọt chất lỏng nhỏ phân tán trong chất lỏng khác"
                ],
                "answer_index": 0,
                "explanation": "Dung dịch là hỗn hợp đồng nhất giữa chất tan và dung môi (ví dụ: nước muối, nước đường).",
                "evidence": "Dung dịch là hỗn hợp đồng nhất của chất tan và dung môi.",
                "source": "KHTN 8 KNTT",
                "page": 32
            },
            {
                "id": 20,
                "difficulty": "Vận dụng",
                "question": "Hòa tan $20\\text{ g}$ muối ăn ($NaCl$) vào $80\\text{ g}$ nước cất. Nồng độ phần trăm ($C\\%$) của dung dịch nước muối thu được là:",
                "options": ["$20\\%$", "$25\\%$", "$16.7\\%$", "$80\\%$"],
                "answer_index": 0,
                "explanation": "$m_{\\text{dd}} = m_{\\text{ct}} + m_{\\text{dm}} = 20 + 80 = 100\\text{ g}$. Nồng độ $C\\% = \\frac{20}{100} \\times 100\\% = 20\\%$.",
                "evidence": "Nồng độ phần trăm C% = (m_ct / m_dd) x 100%.",
                "source": "KHTN 8 KNTT",
                "page": 35
            }
        ]
    },

    # =========================================================================
    # LỚP 9
    # =========================================================================
    {
        "id": "k9-15p-khuc-xa-tan-sac",
        "grade": 9,
        "type": "15p",
        "type_label": "Kiểm tra 15 phút",
        "title": "Kiểm tra 15 phút: Khúc xạ và Tán sắc ánh sáng",
        "topic": "Hiện tượng khúc xạ ánh sáng, Tán sắc ánh sáng",
        "duration_minutes": 15,
        "questions_count": 10,
        "description": "Kiểm tra định luật khúc xạ ánh sáng, hiện tượng tán sắc qua lăng kính, màu sắc ánh sáng và hiện tượng quang học thực tiễn.",
        "questions": [
            {
                "id": 1,
                "difficulty": "Nhận biết",
                "question": "Hiện tượng tia sáng bị đổi phương truyền (gãy khúc) khi truyền xiên góc qua mặt phân cách giữa hai môi trường trong suốt gọi là:",
                "options": [
                    "Hiện tượng phản xạ ánh sáng",
                    "Hiện tượng khúc xạ ánh sáng",
                    "Hiện tượng tán sắc ánh sáng",
                    "Hiện tượng giao thoa ánh sáng"
                ],
                "answer_index": 1,
                "explanation": "Khúc xạ ánh sáng là hiện tượng chùm tia sáng bị gãy khúc tại mặt phân cách giữa hai môi trường trong suốt khác nhau.",
                "evidence": "Hiện tượng tia sáng bị gãy khúc khi truyền xiên góc qua mặt phân cách giữa hai môi trường trong suốt gọi là hiện tượng khúc xạ ánh sáng.",
                "source": "KHTN 9 KNTT",
                "page": 22
            },
            {
                "id": 2,
                "difficulty": "Thông hiểu",
                "question": "Khi tia sáng truyền từ không khí vào nước với góc tới $i > 0^\\circ$, so sánh giữa góc khúc xạ $r$ và góc tới $i$:",
                "options": ["$r > i$", "$r < i$", "$r = i$", "$r = 2i$"],
                "answer_index": 1,
                "explanation": "Do chiết suất của nước lớn hơn không khí ($n_{\\text{nước}} > n_{\\text{kk}} = 1$) nên tia sáng bị bẻ gập về phía pháp tuyến, góc khúc xạ nhỏ hơn góc tới ($r < i$).",
                "evidence": "Khi tia sáng truyền từ không khí vào nước, góc khúc xạ nhỏ hơn góc tới (r < i).",
                "source": "KHTN 9 KNTT",
                "page": 23
            },
            {
                "id": 3,
                "difficulty": "Nhận biết",
                "question": "Khi tia sáng chiếu vuông góc với mặt phân cách giữa hai môi trường trong suốt ($i = 0^\\circ$) thì:",
                "options": [
                    "Tia sáng bị gãy một góc $90^\\circ$",
                    "Tia sáng truyền thẳng, không bị đổi phương ($r = 0^\\circ$)",
                    "Tia sáng bị phản xạ hoàn toàn",
                    "Tia sáng bị tán sắc thành cầu vồng"
                ],
                "answer_index": 1,
                "explanation": "Khi tia sáng tới vuông góc với mặt phân cách ($i = 0^\circ$), tia khúc xạ tiếp tục truyền thẳng ($r = 0^\circ$).",
                "evidence": "Khi góc tới bằng 0 độ, tia sáng truyền thẳng không bị khúc xạ.",
                "source": "KHTN 9 KNTT",
                "page": 24
            },
            {
                "id": 4,
                "difficulty": "Nhận biết",
                "question": "Lăng kính là một khối đồng chất trong suốt có hình dạng lăng trụ tam giác, có tác dụng:",
                "options": [
                    "Hút các hạt bụi trong không khí",
                    "Làm khúc xạ và tán sắc chùm ánh sáng trắng thành dải màu biến thiên liên tục",
                    "Biến đổi mọi ánh sáng thành ánh sáng đơn sắc màu vàng",
                    "Tạo ra từ trường mạnh"
                ],
                "answer_index": 1,
                "explanation": "Lăng kính thủy tinh phân tách chùm sáng trắng phức tạp thành các chùm sáng đơn sắc có màu sắc khác nhau.",
                "evidence": "Lăng kính có tác dụng tán sắc chùm ánh sáng trắng thành dải nhiều màu.",
                "source": "KHTN 9 KNTT",
                "page": 30
            },
            {
                "id": 5,
                "difficulty": "Nhận biết",
                "question": "Dải màu tán sắc của ánh sáng trắng thu được qua lăng kính gồm các màu biến thiên liên tục từ:",
                "options": ["Đỏ đến Tím", "Vàng đến Xanh", "Trắng đến Đen", "Hồng đến Cam"],
                "answer_index": 0,
                "explanation": "Dải quang phổ ánh sáng trắng biến thiên liên tục từ màu đỏ, da cam, vàng, lục, lam, chàm đến tím.",
                "evidence": "Dải màu cầu vồng biến thiên liên tục từ đỏ đến tím.",
                "source": "KHTN 9 KNTT",
                "page": 31
            },
            {
                "id": 6,
                "difficulty": "Thông hiểu",
                "question": "Trong các màu đơn sắc sau đây, màu nào bị lăng kính làm LỆCH NHIỀU NHẤT về phía đáy lăng kính?",
                "options": ["Màu Đỏ", "Màu Vàng", "Màu Tím", "Màu Lục"],
                "answer_index": 2,
                "explanation": "Chiết suất của lăng kính đối với ánh sáng tím lớn nhất nên tia tím bị lệch nhiều nhất; chiết suất với ánh sáng đỏ nhỏ nhất nên tia đỏ bị lệch ít nhất.",
                "evidence": "Ánh sáng đỏ bị lệch ít nhất, ánh sáng tím bị lệch nhiều nhất khi đi qua lăng kính.",
                "source": "KHTN 9 KNTT",
                "page": 32
            },
            {
                "id": 7,
                "difficulty": "Thông hiểu",
                "question": "Ánh sáng đơn sắc là ánh sáng có đặc điểm gì?",
                "options": [
                    "Bị tán sắc thành 7 màu khi qua lăng kính",
                    "Có một màu nhất định và không bị tán sắc khi truyền qua lăng kính",
                    "Chỉ có thể nhìn thấy vào ban đêm",
                    "Bị hấp thụ hoàn toàn trong nước"
                ],
                "answer_index": 1,
                "explanation": "Ánh sáng đơn sắc có bước sóng xác định, khi đi qua lăng kính chỉ bị khúc xạ lệch phương chứ không bị phân tách thành màu khác.",
                "evidence": "Ánh sáng đơn sắc có màu xác định và không bị tán sắc khi qua lăng kính.",
                "source": "KHTN 9 KNTT",
                "page": 33
            },
            {
                "id": 8,
                "difficulty": "Vận dụng",
                "question": "Cắm một chiếc đũa thẳng nghiêng trong bát nước trong suốt, ta nhìn thấy chiếc đũa như bị gãy khúc tại mặt nước là do:",
                "options": [
                    "Chiếc đũa bị nước làm gãy thật sự",
                    "Hiện tượng khúc xạ ánh sáng từ phần đũa trong nước truyền vào mắt qua mặt nước",
                    "Hiện tượng phản xạ toàn phần",
                    "Hiện tượng ảo ảnh nhiệt"
                ],
                "answer_index": 1,
                "explanation": "Tia sáng từ các điểm trên đũa ngập trong nước bị khúc xạ tại mặt phân cách nước - không khí trước khi tới mắt người quan sát, làm mắt thấy ảnh ảo ở vị trí nông hơn.",
                "evidence": "Chiếc đũa trông như bị gãy do hiện tượng khúc xạ ánh sáng tại mặt nước.",
                "source": "KHTN 9 KNTT",
                "page": 25
            },
            {
                "id": 9,
                "difficulty": "Thông hiểu",
                "question": "Hiện tượng cầu vồng xuất hiện sau cơn mưa rào có nắng là kết quả của hiện tượng quang học nào?",
                "options": [
                    "Sự khúc xạ, phản xạ toàn phần và tán sắc ánh sáng mặt trời qua vô số giọt nước mưa lơ lửng trong không khí",
                    "Sự bốc hơi nước của mây",
                    "Do mặt đất phát ra các tia sáng màu",
                    "Do sấm sét tạo ra ánh sáng màu"
                ],
                "answer_index": 0,
                "explanation": "Mỗi giọt nước mưa hoạt động như một lăng kính siêu nhỏ làm khúc xạ, phản xạ trong và tán sắc ánh sáng trắng từ Mặt Trời tạo nên dải cầu vồng hình vòng cung tuyệt đẹp.",
                "evidence": "Cầu vồng được tạo ra do sự khúc xạ và tán sắc ánh sáng mặt trời qua các giọt nước mưa.",
                "source": "KHTN 9 KNTT",
                "page": 34
            },
            {
                "id": 10,
                "difficulty": "Vận dụng",
                "question": "Khi chiếu chùm ánh sáng trắng qua một tấm kính lọc màu xanh lục, chùm ánh sáng đi ra sau tấm lọc có màu gì?",
                "options": ["Màu trắng", "Màu xanh lục", "Màu đỏ", "Không có ánh sáng nào đi qua"],
                "answer_index": 1,
                "explanation": "Tấm lọc màu xanh lục có tính chất cho ánh sáng xanh lục đi qua và hấp thụ hầu hết các màu ánh sáng đơn sắc khác.",
                "evidence": "Tấm lọc màu nào thì cho ánh sáng màu đó đi qua và hấp thụ các màu khác.",
                "source": "KHTN 9 KNTT",
                "page": 35
            }
        ]
    },
    {
        "id": "k9-midterm-tong-hop",
        "grade": 9,
        "type": "midterm",
        "type_label": "Kiểm tra Giữa kỳ 1",
        "title": "Kiểm tra Giữa kỳ 1 KHTN 9: Di truyền học Mendel, Nhiễm sắc thể & Hóa học hữu cơ",
        "topic": "Di truyền Mendel, Nhiễm sắc thể, Khúc xạ ánh sáng, Hợp chất hữu cơ",
        "duration_minutes": 45,
        "questions_count": 20,
        "description": "Đề kiểm tra giữa kì 1 KHTN 9 bao quát Sinh học di truyền (Mendel, NST, nguyên phân), Vật lý quang học (khúc xạ, thấu kính) và Hóa học hữu cơ căn bản.",
        "questions": [
            {
                "id": 1,
                "difficulty": "Nhận biết",
                "question": "Gregor Mendel đã chọn đối tượng nghiên cứu thực nghiệm chủ yếu nào để phát hiện các quy luật di truyền?",
                "options": ["Cây ngô", "Đậu hà lan (Pisum sativum)", "Ruồi giấm", "Chuột bạch"],
                "answer_index": 1,
                "explanation": "Đậu hà lan là loài tự thụ phấn nghiêm ngặt, có vòng đời ngắn và nhiều cặp tính trạng tương phản rõ rệt.",
                "evidence": "Menđen đã chọn cây đậu hà lan làm đối tượng nghiên cứu các quy luật di truyền.",
                "source": "KHTN 9 KNTT",
                "page": 142
            },
            {
                "id": 2,
                "difficulty": "Thông hiểu",
                "question": "Theo quy luật phân li của Mendel, khi lai hai bố mẹ thuần chủng khác nhau về một cặp tính trạng tương phản (hoa đỏ x hoa trắng), ở thế hệ $F_2$ thu được tỉ lệ phân li kiểu hình là:",
                "options": [
                    "$100\\%$ hoa đỏ",
                    "3 trội : 1 lặn (3 hoa đỏ : 1 hoa trắng)",
                    "1 trội : 1 lặn",
                    "9 : 3 : 3 : 1"
                ],
                "answer_index": 1,
                "explanation": "Ở thế hệ $F_1$ đồng tính trội (100% Aa - hoa đỏ). Cho $F_1$ tự thụ phấn: $\\text{Aa} \\times \\text{Aa} \\implies 1\\text{AA} : 2\\text{Aa} : 1\\text{aa}$, cho tỉ lệ kiểu hình 3 đỏ : 1 trắng.",
                "evidence": "F2 có tỉ lệ phân li kiểu hình xấp xỉ 3 trội : 1 lặn.",
                "source": "KHTN 9 KNTT",
                "page": 144
            },
            {
                "id": 3,
                "difficulty": "Nhận biết",
                "question": "Bộ nhiễm sắc thể lưỡng bội ở người bình thường gồm bao nhiêu chiếc?",
                "options": ["23 chiếc", "46 chiếc (23 cặp)", "48 chiếc", "44 chiếc"],
                "answer_index": 1,
                "explanation": "Bộ NST lưỡng bội ($2n$) ở người gồm 46 chiếc, trong đó có 22 cặp NST thường và 1 cặp NST giới tính (XX ở nữ hoặc XY ở nam).",
                "evidence": "Bộ nhiễm sắc thể lưỡng bội của người có 46 chiếc (2n = 46).",
                "source": "KHTN 9 KNTT",
                "page": 150
            },
            {
                "id": 4,
                "difficulty": "Thông hiểu",
                "question": "Ý nghĩa sinh học quan trọng nhất của quá trình nguyên phân là gì?",
                "options": [
                    "Giúp duy trì bộ NST đặc trưng của loài ổn định qua các thế hệ tế bào và giúp cơ thể lớn lên",
                    "Làm giảm một nửa số lượng NST trong giao tử",
                    "Tạo ra vô số biến dị tổ hợp phong phú",
                    "Phân chia đều tế bào chất cho các cơ quan"
                ],
                "answer_index": 0,
                "explanation": "Nguyên phân tạo ra 2 tế bào con có bộ NST y hệt tế bào mẹ ($2n \\to 2n$), đảm bảo sự ổn định di truyền của cơ thể.",
                "evidence": "Nguyên phân duy trì ổn định bộ nhiễm sắc thể đặc trưng của loài qua các thế hệ tế bào.",
                "source": "KHTN 9 KNTT",
                "page": 155
            },
            {
                "id": 5,
                "difficulty": "Nhận biết",
                "question": "Hợp chất hữu cơ là hợp chất của nguyên tố nào (trừ $CO, CO_2, H_2CO_3$, muối cacbonat...)?",
                "options": ["Carbon (C)", "Oxygen (O)", "Nitrogen (N)", "Hydrogen (H)"],
                "answer_index": 0,
                "explanation": "Hợp chất hữu cơ là hợp chất của cacbon (trừ một số chất vô cơ đơn giản như CO, CO2, muối cacbonat kim loại...).",
                "evidence": "Hợp chất hữu cơ là hợp chất của carbon (trừ một số oxit cacbon, muối cacbonat...).",
                "source": "KHTN 9 KNTT",
                "page": 96
            },
            {
                "id": 6,
                "difficulty": "Thông hiểu",
                "question": "Hiđrocacbon (Hydrocarbon) là hợp chất hữu cơ có thành phần phân tử chỉ chứa:",
                "options": [
                    "Carbon và Hydrogen",
                    "Carbon, Hydrogen và Oxygen",
                    "Carbon, Nitrogen và Lưu huỳnh",
                    "Chỉ có nguyên tố Carbon"
                ],
                "answer_index": 0,
                "explanation": "Hiđrocacbon là nhóm hợp chất hữu cơ đơn giản nhất, trong phân tử chỉ chứa 2 nguyên tố C và H (ví dụ: $CH_4, C_2H_4, C_2H_2$).",
                "evidence": "Hydrocarbon là hợp chất hữu cơ mà phân tử chỉ gồm hai nguyên tố carbon và hydrogen.",
                "source": "KHTN 9 KNTT",
                "page": 98
            },
            {
                "id": 7,
                "difficulty": "Nhận biết",
                "question": "Khí metan ($CH_4$) là thành phần chính của loại nhiên liệu nào trong tự nhiên?",
                "options": ["Khí thiên nhiên và khí bioga", "Than đá", "Khí cười ($N_2O$)", "Khí clo"],
                "answer_index": 0,
                "explanation": "Khí metan chiếm 85-95% thành phần của khí thiên nhiên, khí mỏ dầu và khí sinh học bioga.",
                "evidence": "Methane là thành phần chính của khí thiên nhiên, khí mỏ dầu và khí biogas.",
                "source": "KHTN 9 KNTT",
                "page": 102
            },
            {
                "id": 8,
                "difficulty": "Thông hiểu",
                "question": "Thấu kính hội tụ có đặc điểm hình học là:",
                "options": [
                    "Phần rìa mỏng hơn phần giữa",
                    "Phần rìa dày hơn phần giữa",
                    "Bề dày đồng đều ở mọi điểm",
                    "Có mặt kính lõm sâu ở giữa"
                ],
                "answer_index": 0,
                "explanation": "Thấu kính hội tụ (thấu kính rìa mỏng) có phần trung tâm dày và mỏng dần về phía mép rìa.",
                "evidence": "Thấu kính hội tụ có phần rìa mỏng hơn phần giữa.",
                "source": "KHTN 9 KNTT",
                "page": 38
            },
            {
                "id": 9,
                "difficulty": "Thông hiểu",
                "question": "Một chùm tia sáng song song với trục chính của thấu kính hội tụ sau khi đi qua thấu kính sẽ:",
                "options": [
                    "Hội tụ tại tiêu điểm chính $F$ của thấu kính",
                    "Loe rộng ra thành chùm phân kì",
                    "Tiếp tục truyền song song không đổi phương",
                    "Bị phản xạ ngược trở lại"
                ],
                "answer_index": 0,
                "explanation": "Tia tới song song với trục chính thì tia ló đi qua tiêu điểm chính của thấu kính hội tụ.",
                "evidence": "Tia tới song song với trục chính cho tia ló đi qua tiêu điểm của thấu kính hội tụ.",
                "source": "KHTN 9 KNTT",
                "page": 39
            },
            {
                "id": 10,
                "difficulty": "Vận dụng",
                "question": "Đặt một vật sáng $AB$ vuông góc với trục chính của một thấu kính hội tụ có tiêu cự $f = 12\\text{ cm}$, vật cách thấu kính $d = 24\\text{ cm}$ ($d = 2f$). Ảnh thu được có tính chất gì?",
                "options": [
                    "Ảnh thật, ngược chiều và có độ cao bằng vật ($A'B' = AB$)",
                    "Ảnh ảo, cùng chiều và lớn hơn vật",
                    "Ảnh thật, nhỏ hơn vật rất nhiều",
                    "Không tạo được ảnh"
                ],
                "answer_index": 0,
                "explanation": "Khi vật đặt tại vị trí cách thấu kính đúng bằng $2f$, thấu kính hội tụ cho ảnh thật, ngược chiều và kích thước bằng đúng vật.",
                "evidence": "Vật đặt cách thấu kính một khoảng d = 2f cho ảnh thật, ngược chiều và bằng vật.",
                "source": "KHTN 9 KNTT",
                "page": 43
            },
            {
                "id": 11,
                "difficulty": "Nhận biết",
                "question": "Gen là gì?",
                "options": [
                    "Một đoạn của phân tử DNA mang thông tin mã hóa cho một chuỗi polypeptide hoặc một phân tử RNA",
                    "Một bào quan nằm trong tế bào chất",
                    "Một phân tử lipid dự trữ năng lượng",
                    "Một chuỗi carbohydrate"
                ],
                "answer_index": 0,
                "explanation": "Gen là đơn vị chức năng cơ bản của di truyền học, bản chất là một đoạn phân tử DNA mang thông tin di truyền.",
                "evidence": "Gen là một đoạn của phân tử DNA mang thông tin mã hóa cho một sản phẩm xác định.",
                "source": "KHTN 9 KNTT",
                "page": 147
            },
            {
                "id": 12,
                "difficulty": "Thông hiểu",
                "question": "Phân tử DNA được cấu tạo theo nguyên tắc đa phân mà đơn phân là:",
                "options": [
                    "4 loại nuclêôtit: A, T, G, C (Adenine, Thymine, Guanine, Cytosine)",
                    "20 loại amino acid",
                    "Các phân tử glucose",
                    "Axit béo và glycerol"
                ],
                "answer_index": 0,
                "explanation": "DNA là chuỗi xoắn kép gồm các đơn phân nucleotit thuộc 4 loại A, T, G, C liên kết với nhau.",
                "evidence": "DNA cấu tạo theo nguyên tắc đa phân với 4 loại đơn phân là A, T, G, C.",
                "source": "KHTN 9 KNTT",
                "page": 148
            },
            {
                "id": 13,
                "difficulty": "Thông hiểu",
                "question": "Theo nguyên tắc bổ sung trong cấu trúc xoắn kép của phân tử DNA, các bazơ liên kết với nhau theo cặp:",
                "options": [
                    "A liên kết với T (bằng 2 liên kết hiđro), G liên kết với C (bằng 3 liên kết hiđro)",
                    "A liên kết với G, T liên kết với C",
                    "A liên kết với C, T liên kết với G",
                    "Tất cả các bazơ liên kết tự do"
                ],
                "answer_index": 0,
                "explanation": "Nguyên tắc bổ sung: Adenine chỉ liên kết với Thymine, Guanine chỉ liên kết với Cytosine.",
                "evidence": "Các nucleotide liên kết theo nguyên tắc bổ sung: A liên kết với T, G liên kết với C.",
                "source": "KHTN 9 KNTT",
                "page": 149
            },
            {
                "id": 14,
                "difficulty": "Vận dụng",
                "question": "Một đoạn mạch DNA có trình tự các nucleotide như sau: $- \\text{A - T - G - C - A - T} -$. Trình tự đoạn mạch bổ sung với nó là:",
                "options": [
                    "$- \\text{T - A - C - G - T - A} -$",
                    "$- \\text{A - T - G - C - A - T} -$",
                    "$- \\text{U - A - C - G - U - A} -$",
                    "$- \\text{C - G - T - A - C - G} -$"
                ],
                "answer_index": 0,
                "explanation": "Theo nguyên tắc bổ sung: $\\text{A} \\to \\text{T}$, $\\text{T} \\to \\text{A}$, $\\text{G} \\to \\text{C}$, $\\text{C} \\to \\text{G}$. Đoạn bổ sung là: $- \\text{T - A - C - G - T - A} -$.",
                "evidence": "Trình tự mạch bổ sung được xác định theo nguyên tắc A-T và G-C.",
                "source": "KHTN 9 KNTT",
                "page": 149
            },
            {
                "id": 15,
                "difficulty": "Nhận biết",
                "question": "Phản ứng đặc trưng của ankan (như metan $CH_4$) là:",
                "options": ["Phản ứng thế", "Phản ứng cộng", "Phản ứng trùng hợp", "Phản ứng tráng bạc"],
                "answer_index": 0,
                "explanation": "Metan chỉ có liên kết đơn C-H bền vững nên phản ứng hóa học đặc trưng là phản ứng thế (ví dụ thế clo khi có ánh sáng).",
                "evidence": "Methane có phản ứng thế đặc trưng với chlorine khi có ánh sáng.",
                "source": "KHTN 9 KNTT",
                "page": 103
            },
            {
                "id": 16,
                "difficulty": "Thông hiểu",
                "question": "Khí etilen ($C_2H_4$) làm mất màu dung dịch brom ($Br_2$) màu da cam là do trong phân tử etilen có chứa:",
                "options": [
                    "Liên kết đôi $C=C$ kém bền dễ bị bẻ gãy tham gia phản ứng cộng",
                    "Nguyên tử oxygen",
                    "Liên kết ba $C \\equiv C$",
                    "Chỉ toàn liên kết đơn bền vững"
                ],
                "answer_index": 0,
                "explanation": "Liên kết đôi trong phân tử etilen gồm 1 liên kết $\\sigma$ bền và 1 liên kết $\\pi$ kém bền dễ bị đứt ra để cộng với phân tử halogen.",
                "evidence": "Ethylene làm mất màu dung dịch bromine do có liên kết đôi tham gia phản ứng cộng.",
                "source": "KHTN 9 KNTT",
                "page": 106
            },
            {
                "id": 17,
                "difficulty": "Vận dụng",
                "question": "Trong nông nghiệp, người ta thường xếp một vài quả chuối chín cùng với các quả xanh trong sọt để quả mau chín là do:",
                "options": [
                    "Quả chín phát sinh ra một lượng nhỏ khí etilen ($C_2H_4$) kích thích quá trình chín của quả xanh xung quanh",
                    "Quả chín hút bớt nước của quả xanh",
                    "Quả chín làm tăng nhiệt độ sọt quả",
                    "Quả chín tiêu diệt nấm mốc"
                ],
                "answer_index": 0,
                "explanation": "Khí etilen là một phytohormone thực vật dạng khí có tác dụng thúc đẩy quá trình chín của quả và rụng lá.",
                "evidence": "Ethylene được ứng dụng để làm quả mau chín trong đời sống.",
                "source": "KHTN 9 KNTT",
                "page": 108
            },
            {
                "id": 18,
                "difficulty": "Nhận biết",
                "question": "Mắt cận thị là tật khúc xạ của mắt mà người mắc tật này:",
                "options": [
                    "Nhìn rõ các vật ở gần nhưng không nhìn rõ các vật ở xa",
                    "Nhìn rõ các vật ở xa nhưng không nhìn rõ các vật ở gần",
                    "Không nhìn rõ cả vật ở gần lẫn ở xa",
                    "Không phân biệt được màu sắc"
                ],
                "answer_index": 0,
                "explanation": "Mắt cận thị có thể tích nhãn cầu dài hoặc thể thủy tinh quá phồng khiến điểm hội tụ ảnh nằm trước màng lưới, chỉ nhìn rõ vật gần.",
                "evidence": "Mắt cận thị chỉ nhìn rõ các vật ở gần, không nhìn rõ các vật ở xa.",
                "source": "KHTN 9 KNTT",
                "page": 48
            },
            {
                "id": 19,
                "difficulty": "Thông hiểu",
                "question": "Để khắc phục tật cận thị, người cận thị cần đeo kính cận là loại thấu kính nào?",
                "options": [
                    "Thấu kính phân kì có độ tụ thích hợp",
                    "Thấu kính hội tụ",
                    "Kính hai tròng màu đen",
                    "Thấu kính phẳng không số"
                ],
                "answer_index": 0,
                "explanation": "Thấu kính phân kì làm chùm tia sáng loe rộng ra trước khi vào mắt, giúp đẩy ảnh lùi ra sau rơi đúng lên màng lưới để nhìn rõ vật ở xa.",
                "evidence": "Để khắc phục tật cận thị, người cận thị phải đeo kính là thấu kính phân kì thích hợp.",
                "source": "KHTN 9 KNTT",
                "page": 49
            },
            {
                "id": 20,
                "difficulty": "Vận dụng",
                "question": "Lai phân tích là phép lai giữa cá thể mang tính trạng trội cần xác định kiểu gen với cá thể mang kiểu gen:",
                "options": [
                    "Đồng hợp lặn (ví dụ aa)",
                    "Đồng hợp trội (AA)",
                    "Dị hợp tử (Aa)",
                    "Bất kì cá thể nào"
                ],
                "answer_index": 0,
                "explanation": "Lai phân tích với cá thể đồng hợp lặn giúp xác định kiểu gen của cá thể trội: nếu đời con đồng tính thì cá thể là AA, nếu phân tính thì cá thể là Aa.",
                "evidence": "Lai phân tích là phép lai giữa cá thể mang tính trạng trội với cá thể mang tính trạng lặn để kiểm tra kiểu gen.",
                "source": "KHTN 9 KNTT",
                "page": 145
            }
        ]
    }
]


import json
from pathlib import Path

USER_EXAMS_FILE = Path(__file__).resolve().parent.parent.parent / "database_kntt" / "user_exams.json"


def load_user_exams():
    """Tải danh sách các đề thi do người dùng/giáo viên tải lên và đã lưu."""
    try:
        if USER_EXAMS_FILE.exists():
            with open(USER_EXAMS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
    except Exception as e:
        print(f"[curated_quizzes] Lỗi đọc {USER_EXAMS_FILE}: {e}")
    return []


def save_user_exam(exam_data):
    """Lưu đề thi mới do người dùng tải lên vào kho đề tùy chỉnh."""
    try:
        exams = load_user_exams()
        # Đảm bảo có nhãn phân biệt
        exam_data["user_uploaded"] = True
        if not exam_data.get("badge"):
            exam_data["badge"] = "👤 Đề tải lên"

        existing_idx = next((i for i, ex in enumerate(exams) if ex.get("id") == exam_data.get("id")), None)
        if existing_idx is not None:
            exams[existing_idx] = exam_data
        else:
            exams.insert(0, exam_data)

        USER_EXAMS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(USER_EXAMS_FILE, "w", encoding="utf-8") as f:
            json.dump(exams, f, ensure_ascii=False, indent=2)
        return True, exam_data.get("id")
    except Exception as e:
        print(f"[curated_quizzes] Lỗi lưu user exam: {e}")
        return False, str(e)


def get_curated_exams_by_grade(grade=None):
    """Lấy danh sách các đề thi mẫu chuẩn KNTT và đề thi do người dùng tải lên theo khối lớp."""
    user_exams = load_user_exams()
    all_exams = user_exams + CURATED_EXAM_BANK
    if grade is None:
        return all_exams
    try:
        grade_int = int(grade)
        return [exam for exam in all_exams if exam.get("grade") == grade_int]
    except Exception:
        return all_exams


def get_curated_exam_by_id(exam_id):
    """Lấy chi tiết một bộ đề thi mẫu theo ID (bao gồm cả đề tải lên)."""
    user_exams = load_user_exams()
    for exam in user_exams:
        if exam.get("id") == exam_id:
            return exam
    for exam in CURATED_EXAM_BANK:
        if exam.get("id") == exam_id:
            return exam
    return None

