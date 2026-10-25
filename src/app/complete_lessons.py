"""Canonical complete sample lessons for the BioRAG learning area."""

from __future__ import annotations

from copy import deepcopy


COMPLETE_LESSON_VERSION = 5


COMPLETE_LESSONS = [
    {
        "id": "k6-te-bao",
        "grade": 6,
        "number": "Bài 18",
        "title": "Tế bào – đơn vị cơ bản của sự sống",
        "topic": "Tế bào là đơn vị cơ bản của sự sống; hình dạng và kích thước tế bào",
        "duration": "35–45 phút",
        "objectives": [
            "Nêu được tế bào là đơn vị cấu tạo cơ bản của cơ thể sống.",
            "Nhận biết được sự đa dạng về hình dạng và kích thước của tế bào.",
            "Giải thích được hình dạng tế bào thường phù hợp với chức năng.",
            "Vận dụng kiến thức để nhận biết một số loại tế bào quen thuộc."
        ],
        "content": "Mọi cơ thể sống đều được cấu tạo từ tế bào. Tế bào rất nhỏ nhưng có thể thực hiện những hoạt động sống cơ bản. Tế bào có nhiều hình dạng, kích thước khác nhau và đặc điểm đó thường phù hợp với chức năng của chúng.",
        "source_label": "SGK KHTN 6 KNTT · Bài 18 · Trang 64–67",
        "warmup": {
            "question": "Cây đậu, con cá và cơ thể người rất khác nhau. Chúng có điểm cấu tạo chung nào?",
            "hint": "Hãy nghĩ đến đơn vị rất nhỏ chỉ quan sát rõ bằng kính hiển vi."
        },
        "sections": [
            {
                "title": "1. Tế bào là gì?",
                "paragraphs": [
                    "Tế bào là đơn vị cấu tạo cơ bản của mọi cơ thể sống. Có sinh vật chỉ gồm một tế bào; cũng có sinh vật gồm rất nhiều tế bào phối hợp với nhau.",
                    "Dù rất nhỏ, tế bào vẫn thực hiện các hoạt động sống như trao đổi chất, lớn lên và sinh sản."
                ],
                "example": "Vi khuẩn là cơ thể đơn bào; cây đậu và con người là cơ thể đa bào."
            },
            {
                "title": "2. Hình dạng của tế bào",
                "paragraphs": [
                    "Tế bào có thể có dạng hình cầu, hình đĩa, hình que, hình sao hoặc dạng sợi. Hình dạng thường liên quan đến nhiệm vụ mà tế bào đảm nhiệm."
                ],
                "bullets": [
                    "Tế bào hồng cầu có dạng đĩa lõm hai mặt, thuận lợi cho vận chuyển khí.",
                    "Tế bào thần kinh có nhiều nhánh dài, thuận lợi cho truyền tín hiệu.",
                    "Tế bào cơ có dạng sợi dài, phù hợp với khả năng co và giãn."
                ]
            },
            {
                "title": "3. Kích thước của tế bào",
                "paragraphs": [
                    "Phần lớn tế bào có kích thước hiển vi nên cần kính hiển vi để quan sát. Một số tế bào có thể nhìn thấy bằng mắt thường, chẳng hạn tế bào trứng của một số động vật.",
                    "Kích thước cơ thể không quyết định trực tiếp kích thước tế bào; cơ thể lớn thường có số lượng tế bào nhiều hơn."
                ],
                "note": "Không kết luận cơ thể càng lớn thì từng tế bào càng lớn."
            }
        ],
        "diagram": {
            "title": "Từ tế bào đến cơ thể sống",
            "nodes": [
                "Tế bào",
                "Mô",
                "Cơ quan",
                "Hệ cơ quan",
                "Cơ thể"
            ]
        },
        "terms": [
            {
                "term": "Tế bào",
                "definition": "Đơn vị cấu tạo cơ bản của cơ thể sống."
            },
            {
                "term": "Đơn bào",
                "definition": "Cơ thể chỉ gồm một tế bào."
            },
            {
                "term": "Đa bào",
                "definition": "Cơ thể gồm nhiều tế bào."
            },
            {
                "term": "Kính hiển vi",
                "definition": "Dụng cụ giúp quan sát vật thể rất nhỏ."
            }
        ],
        "summary": [
            "Mọi cơ thể sống đều được cấu tạo từ tế bào.",
            "Tế bào thực hiện các hoạt động sống cơ bản.",
            "Hình dạng và kích thước tế bào rất đa dạng, thường phù hợp với chức năng."
        ],
        "quick_check": [
            {
                "question": "Đơn vị cấu tạo cơ bản của cơ thể sống là gì?",
                "options": [
                    "Mô",
                    "Tế bào",
                    "Cơ quan",
                    "Hệ cơ quan"
                ],
                "answer_index": 1,
                "explanation": "Tế bào là đơn vị cấu tạo cơ bản của tất cả cơ thể sống."
            },
            {
                "question": "Vì sao tế bào thần kinh có nhiều nhánh dài?",
                "options": [
                    "Để dự trữ nước",
                    "Để truyền tín hiệu",
                    "Để tạo màu",
                    "Để tiêu hóa thức ăn"
                ],
                "answer_index": 1,
                "explanation": "Các nhánh dài giúp tế bào thần kinh tiếp nhận và truyền tín hiệu."
            },
            {
                "question": "Nhận định nào đúng?",
                "options": [
                    "Mọi tế bào đều nhìn thấy bằng mắt thường",
                    "Tất cả tế bào có cùng hình dạng",
                    "Phần lớn tế bào cần kính hiển vi để quan sát",
                    "Cơ thể lớn luôn có tế bào lớn"
                ],
                "answer_index": 2,
                "explanation": "Phần lớn tế bào có kích thước hiển vi."
            }
        ],
        "order": 180,
        "active": True,
        "origin": "system",
        "lesson_version": 4
    },
    {
        "id": "k7-ho-hap-te-bao",
        "grade": 7,
        "number": "Bài 25",
        "title": "Hô hấp tế bào",
        "topic": "Hô hấp tế bào; nguyên liệu, sản phẩm và vai trò của hô hấp tế bào",
        "duration": "35–45 phút",
        "objectives": [
            "Nêu được khái niệm hô hấp tế bào.",
            "Xác định được nguyên liệu và sản phẩm của quá trình.",
            "Trình bày được vai trò của năng lượng giải phóng đối với cơ thể.",
            "Phân biệt được tổng hợp và phân giải chất hữu cơ."
        ],
        "content": "Hô hấp tế bào là quá trình phân giải chất hữu cơ trong tế bào, thường sử dụng oxygen, tạo carbon dioxide, nước và giải phóng năng lượng cho các hoạt động sống.",
        "source_label": "SGK KHTN 7 KNTT · Bài 25 · Trang 111–112",
        "warmup": {
            "question": "Vì sao sau khi chạy nhanh, em thở gấp và cảm thấy cơ thể nóng lên?",
            "hint": "Cơ bắp đang cần nhiều năng lượng hơn khi vận động."
        },
        "sections": [
            {
                "title": "1. Khái niệm hô hấp tế bào",
                "paragraphs": [
                    "Hô hấp tế bào là chuỗi phản ứng phân giải chất hữu cơ diễn ra trong tế bào. Năng lượng hóa học trong chất hữu cơ được giải phóng và một phần được tích lũy trong ATP.",
                    "Ở nhiều sinh vật, glucose là nguyên liệu hữu cơ phổ biến và oxygen tham gia quá trình hô hấp hiếu khí."
                ]
            },
            {
                "title": "2. Nguyên liệu và sản phẩm",
                "paragraphs": [
                    "Có thể mô tả khái quát: glucose và oxygen tạo thành carbon dioxide, nước và năng lượng.",
                    "Năng lượng giải phóng được dùng cho vận động, sinh trưởng, tổng hợp chất, vận chuyển chất và duy trì nhiệt độ cơ thể."
                ],
                "note": "Hô hấp tế bào không đồng nhất với động tác hít vào – thở ra; hít thở giúp trao đổi khí, còn hô hấp tế bào diễn ra bên trong tế bào."
            },
            {
                "title": "3. Tổng hợp và phân giải chất hữu cơ",
                "paragraphs": [
                    "Quá trình tổng hợp tạo chất hữu cơ và tích lũy năng lượng; quá trình phân giải phá vỡ chất hữu cơ và giải phóng năng lượng.",
                    "Hai nhóm quá trình liên hệ chặt chẽ: sản phẩm của quá trình này có thể trở thành nguyên liệu của quá trình kia."
                ],
                "example": "Quang hợp tạo glucose và oxygen; hô hấp tế bào sử dụng chúng để giải phóng năng lượng."
            }
        ],
        "diagram": {
            "title": "Sơ đồ hô hấp tế bào",
            "nodes": [
                "Glucose + Oxygen",
                "Hô hấp tế bào",
                "Carbon dioxide + Nước + Năng lượng"
            ]
        },
        "terms": [
            {
                "term": "Hô hấp tế bào",
                "definition": "Quá trình phân giải chất hữu cơ và giải phóng năng lượng trong tế bào."
            },
            {
                "term": "ATP",
                "definition": "Dạng năng lượng tế bào có thể sử dụng trực tiếp."
            },
            {
                "term": "Phân giải",
                "definition": "Biến đổi chất phức tạp thành chất đơn giản hơn, thường giải phóng năng lượng."
            },
            {
                "term": "Tổng hợp",
                "definition": "Tạo chất phức tạp từ chất đơn giản hơn, thường cần năng lượng."
            }
        ],
        "summary": [
            "Hô hấp tế bào phân giải chất hữu cơ để giải phóng năng lượng.",
            "Nguyên liệu phổ biến là glucose và oxygen; sản phẩm gồm carbon dioxide, nước và năng lượng.",
            "Năng lượng được dùng cho mọi hoạt động sống của tế bào và cơ thể."
        ],
        "quick_check": [
            {
                "question": "Sản phẩm nào được tạo ra trong hô hấp tế bào hiếu khí?",
                "options": [
                    "Glucose và oxygen",
                    "Carbon dioxide, nước và năng lượng",
                    "Chỉ oxygen",
                    "Chỉ glucose"
                ],
                "answer_index": 1,
                "explanation": "Hô hấp tế bào sử dụng glucose và oxygen, tạo carbon dioxide, nước và giải phóng năng lượng."
            },
            {
                "question": "Vai trò trực tiếp nhất của hô hấp tế bào là gì?",
                "options": [
                    "Tạo ánh sáng",
                    "Giải phóng năng lượng",
                    "Tạo oxygen",
                    "Giảm số lượng tế bào"
                ],
                "answer_index": 1,
                "explanation": "Quá trình giải phóng năng lượng để cung cấp cho các hoạt động sống."
            },
            {
                "question": "Nhận định nào đúng?",
                "options": [
                    "Hô hấp tế bào chỉ là động tác thở",
                    "Hô hấp tế bào chỉ xảy ra khi vận động",
                    "Hô hấp tế bào diễn ra trong tế bào",
                    "Hô hấp tế bào tạo glucose"
                ],
                "answer_index": 2,
                "explanation": "Hít thở và hô hấp tế bào liên quan nhưng không phải một quá trình."
            }
        ],
        "order": 250,
        "active": True,
        "origin": "system",
        "lesson_version": 4
    },
    {
        "id": "k8-he-van-dong",
        "grade": 8,
        "number": "Bài 31",
        "title": "Hệ vận động ở người",
        "topic": "Hệ vận động ở người; xương, khớp, cơ; bảo vệ hệ vận động",
        "duration": "40–45 phút",
        "objectives": [
            "Nêu được cấu tạo và chức năng chính của hệ vận động.",
            "Giải thích được sự phối hợp giữa cơ, xương và khớp khi vận động.",
            "Nhận biết được một số bệnh, tật liên quan đến hệ vận động.",
            "Đề xuất được biện pháp bảo vệ hệ vận động trong học tập và sinh hoạt."
        ],
        "content": "Hệ vận động gồm bộ xương và hệ cơ. Xương tạo khung và bảo vệ cơ thể; khớp nối các xương; cơ bám vào xương, co và dãn để làm xương chuyển động quanh khớp.",
        "source_label": "SGK KHTN 8 KNTT · Bài 31 · Trang 125–129",
        "warmup": {
            "question": "Khi em gập cẳng tay, những bộ phận nào phối hợp để tạo ra chuyển động?",
            "hint": "Hãy quan sát cơ ở cánh tay, xương cẳng tay và khớp khuỷu."
        },
        "sections": [
            {
                "title": "1. Cấu tạo của hệ vận động",
                "paragraphs": [
                    "Bộ xương gồm xương đầu, xương thân và xương chi. Các xương nối với nhau tại khớp. Hệ cơ gồm các cơ bám vào xương nhờ mô liên kết.",
                    "Xương tạo khung nâng đỡ, định hình và bảo vệ cơ quan; cơ tạo lực; khớp là vị trí cho phép các phần xương chuyển động tương đối với nhau."
                ]
            },
            {
                "title": "2. Sự phối hợp tạo vận động",
                "paragraphs": [
                    "Khi cơ co, cơ ngắn lại và kéo xương chuyển động quanh khớp. Nhiều vận động cần các nhóm cơ đối kháng phối hợp: một cơ co trong khi cơ kia dãn."
                ],
                "example": "Khi gập cẳng tay, cơ phía trước cánh tay co và cơ phía sau dãn; khi duỗi tay, hoạt động của hai nhóm cơ đổi lại."
            },
            {
                "title": "3. Bảo vệ hệ vận động",
                "paragraphs": [
                    "Dinh dưỡng hợp lí, vận động vừa sức và tư thế đúng giúp xương, khớp, cơ phát triển khỏe mạnh. Cần khởi động trước khi luyện tập và dùng đồ bảo hộ phù hợp."
                ],
                "bullets": [
                    "Ngồi học thẳng lưng, bàn ghế phù hợp chiều cao.",
                    "Mang cặp đều hai vai, tránh mang vật quá nặng lệch một bên.",
                    "Bổ sung đủ protein, calcium, vitamin D và vận động ngoài trời hợp lí.",
                    "Khi chấn thương, hạn chế di chuyển vùng tổn thương và tìm hỗ trợ y tế."
                ],
                "note": "Không tự nắn chỉnh xương hoặc khớp khi nghi ngờ gãy xương, trật khớp."
            }
        ],
        "diagram": {
            "title": "Cơ chế tạo vận động",
            "nodes": [
                "Cơ co hoặc dãn",
                "Kéo xương",
                "Xương quay quanh khớp",
                "Cơ thể vận động"
            ]
        },
        "terms": [
            {
                "term": "Bộ xương",
                "definition": "Hệ thống xương tạo khung nâng đỡ và bảo vệ cơ thể."
            },
            {
                "term": "Khớp",
                "definition": "Nơi tiếp giáp giữa các xương."
            },
            {
                "term": "Cơ đối kháng",
                "definition": "Các cơ tạo ra những tác động ngược chiều và phối hợp trong vận động."
            },
            {
                "term": "Cong vẹo cột sống",
                "definition": "Tình trạng cột sống cong hoặc lệch bất thường."
            }
        ],
        "summary": [
            "Hệ vận động gồm bộ xương và hệ cơ; khớp nối các xương.",
            "Cơ co tạo lực kéo làm xương chuyển động quanh khớp.",
            "Tư thế đúng, dinh dưỡng và luyện tập hợp lí giúp bảo vệ hệ vận động."
        ],
        "quick_check": [
            {
                "question": "Bộ phận nào trực tiếp tạo lực kéo xương?",
                "options": [
                    "Da",
                    "Cơ",
                    "Máu",
                    "Dây thần kinh"
                ],
                "answer_index": 1,
                "explanation": "Cơ co và truyền lực kéo lên xương qua vị trí bám."
            },
            {
                "question": "Khớp có vai trò chính nào trong vận động?",
                "options": [
                    "Tạo máu",
                    "Tiêu hóa thức ăn",
                    "Nối xương và cho phép chuyển động",
                    "Trao đổi khí"
                ],
                "answer_index": 2,
                "explanation": "Khớp là nơi tiếp giáp giữa các xương và tạo điều kiện cho chuyển động."
            },
            {
                "question": "Thói quen nào giúp hạn chế cong vẹo cột sống?",
                "options": [
                    "Mang cặp lệch một vai",
                    "Ngồi học đúng tư thế",
                    "Ít vận động",
                    "Mang vật quá nặng"
                ],
                "answer_index": 1,
                "explanation": "Tư thế đúng và bàn ghế phù hợp giúp giảm tải không cân đối lên cột sống."
            }
        ],
        "order": 310,
        "active": True,
        "origin": "system",
        "lesson_version": 4
    },
    {
        "id": "k8-b32-tieu-hoa",
        "grade": 8,
        "number": "Bài 32",
        "title": "Dinh dưỡng và tiêu hóa ở người",
        "topic": "Sinh học cơ thể người",
        "duration": "3 tiết (135 phút)",
        "order": 320,
        "active": True,
        "origin": "official_curriculum",
        "lesson_version": 5,
        "source_label": "SGK KHTN 8 KNTT – Bài 32 – Trang 131–135",
        "content": "Dinh dưỡng và tiêu hóa ở người nghiên cứu cấu tạo hệ tiêu hóa gồm ống tiêu hóa và các tuyến tiêu hóa; các giai đoạn biến đổi thức ăn cơ học và hóa học tại khoang miệng, dạ dày, ruột non; sự hấp thụ chất dinh dưỡng tối đa tại ruột non và các biện pháp bảo vệ hệ tiêu hóa khỏe mạnh.",
        "warmup": "Khi chúng ta ăn một mẩu bánh mì khô, tại sao càng nhai kĩ lại càng cảm thấy có vị ngọt? Quá trình tiêu hóa và hấp thụ các chất dinh dưỡng trong cơ thể diễn ra như thế nào?",
        "objectives": [
            "Nêu được khái niệm dinh dưỡng và tiêu hóa.",
            "Trình bày được cấu tạo và chức năng của các cơ quan trong hệ tiêu hóa (ống tiêu hóa và tuyến tiêu hóa).",
            "Mô tả được quá trình tiêu hóa cơ học và tiêu hóa hóa học diễn ra ở khoang miệng, dạ dày và ruột non.",
            "Giải thích được vì sao ruột non là cơ quan tiêu hóa triệt để nhất và hấp thụ chất dinh dưỡng chủ yếu.",
            "Vận dụng kiến thức để xây dựng chế độ ăn uống khoa học, vệ sinh an toàn thực phẩm để bảo vệ hệ tiêu hóa."
        ],
        "sections": [
            {
                "title": "1. Khái niệm dinh dưỡng và tiêu hóa",
                "paragraphs": [
                    "Dinh dưỡng là quá trình thu nhận, biến đổi và sử dụng chất dinh dưỡng từ thức ăn để duy trì các hoạt động sống, phát triển cơ thể và tái tạo các tế bào bị tổn thương.",
                    "Tiêu hóa là quá trình biến đổi các chất phức tạp trong thức ăn thành các chất dinh dưỡng đơn giản mà cơ thể có thể hấp thụ được qua niêm mạc ruột vào máu và dịch bạch huyết, đồng thời thải bỏ các chất cặn bã ra ngoài."
                ],
                "bullets": [
                    "Chất dinh dưỡng gồm: chất bột đường (carbohydrate), chất đạm (protein), chất béo (lipid), vitamin, khoáng chất và nước.",
                    "Hai hoạt động tiêu hóa cơ bản: tiêu hóa cơ học (nhai, nghiền, đảo trộn) và tiêu hóa hóa học (sử dụng enzyme xúc tác phân giải liên kết hóa học)."
                ]
            },
            {
                "title": "2. Cấu tạo của hệ tiêu hóa ở người",
                "paragraphs": [
                    "Hệ tiêu hóa ở người được chia thành hai bộ phận chính: ống tiêu hóa và các tuyến tiêu hóa.",
                    "Ống tiêu hóa là một đường ống cơ rỗng kéo dài từ miệng đến hậu môn gồm: khoang miệng, hầu (họng), thực quản, dạ dày, ruột non, ruột già (kết tràng), trực tràng và hậu môn.",
                    "Tuyến tiêu hóa gồm các tuyến tiết dịch tiêu hóa chứa enzyme đổ vào ống tiêu hóa: tuyến nước bọt (ở khoang miệng), tuyến vị (ở niêm mạc dạ dày), gan (tiết dịch mật chứa trong túi mật), tuyến tụy (tiết dịch tụy) và tuyến ruột (ở niêm mạc ruột non)."
                ],
                "bullets": [
                    "Khoang miệng: răng cắn xé và nghiền thức ăn, lưỡi đảo trộn, tuyến nước bọt làm ẩm và tiêu hóa tinh bột chín.",
                    "Dạ dày: cơ quan phình to nhất của ống tiêu hóa, hình chữ J, có lớp cơ trơn rất dày và khỏe để co bóp nhào trộn thức ăn với dịch vị.",
                    "Ruột non: dài khoảng 2,8 – 3 m ở người trưởng thành, đường kính nhỏ, gấp khúc nhiều lần chiếm phần lớn khoang bụng.",
                    "Gan và tụy: hai tuyến tiêu hóa lớn nhất, tiết dịch đổ vào tá tràng (đoạn đầu của ruột non)."
                ]
            },
            {
                "title": "3. Quá trình biến đổi thức ăn ở các cơ quan tiêu hóa",
                "paragraphs": [
                    "Quá trình tiêu hóa diễn ra tuần tự qua các cơ quan của ống tiêu hóa với sự phối hợp nhịp nhàng giữa biến đổi cơ học và hóa học.",
                    "Ở khoang miệng: Thức ăn được răng cắn, xé, nghiền nhỏ và lưỡi đảo trộn thấm đều nước bọt (tiêu hóa cơ học). Enzyme amylase trong nước bọt biến đổi một phần tinh bột chín thành đường maltose (tiêu hóa hóa học). Thức ăn được vo thành viên nuốt qua hầu và thực quản xuống dạ dày.",
                    "Ở dạ dày: Nhờ các lớp cơ vòng, cơ dọc và cơ chéo co bóp mạnh mẽ, thức ăn được nghiền nhuyễn và thấm đẫm dịch vị (chứa HCl và enzyme pepsin). Môi trường acid HCl tiêu diệt vi khuẩn và hoạt hóa enzyme pepsin biến đổi một phần protein chuỗi dài thành các chuỗi peptide ngắn.",
                    "Ở ruột non: Thức ăn từ dạ dày từng đợt nhỏ xuống tá tràng được trung hòa acid nhờ dịch tụy và dịch ruột có tính kiềm. Dịch mật nhũ tương hóa lipid thành các giọt mỡ nhỏ. Hệ enzyme phong phú (trypsin, erepsin, amylase, maltase, lipase) phân giải triệt để: protein thành amino acid, carbohydrate thành glucose, lipid thành acid béo và glycerol."
                ],
                "bullets": [
                    "Tại khoang miệng: Tinh bột chín --(Amylase nước bọt)--> Đường maltose.",
                    "Tại dạ dày: Protein --(Pepsin + HCl dịch vị)--> Các chuỗi peptide ngắn.",
                    "Tại ruột non: Protein -> Amino acid; Tinh bột/Đường -> Glucose; Lipid -> Acid béo + Glycerol."
                ]
            },
            {
                "title": "4. Hấp thụ chất dinh dưỡng và thải bã",
                "paragraphs": [
                    "Ruột non là cơ quan duy nhất diễn ra sự tiêu hóa hoàn toàn triệt để và là nơi hấp thụ hầu hết (trên 95%) các chất dinh dưỡng của cơ thể.",
                    "Cấu tạo đặc biệt giúp ruột non tối ưu hóa hấp thụ: Niêm mạc ruột non có các nếp gấp, trên nếp gấp có hàng triệu nhung mao ruột, trên mỗi tế bào nhung mao lại có vô số vi nhung mao li ti. Cấu trúc này làm tăng diện tích bề mặt tiếp xúc và hấp thụ lên gấp 600 lần so với ống trơn, đạt diện tích hấp thụ khổng lồ khoảng 400 - 500 m2.",
                    "Bên trong mỗi lông nhung ruột có mạng lưới mao mạch máu và mao mạch bạch huyết dày đặc: Glucose, amino acid, nước, vitamin tan trong nước và khoáng chất hấp thụ vào mao mạch máu về gan; Acid béo và glycerol kết hợp lại thành lipid hấp thụ theo con đường mao mạch bạch huyết.",
                    "Chất cặn bã không tiêu hóa được (chủ yếu là chất xơ) chuyển qua van hồi - manh tràng xuống ruột già. Ruột già hấp thụ lại phần lớn lượng nước còn lại, cô đặc chất bã thành phân nhờ vi khuẩn lên men rồi chuyển xuống trực tràng thải ra ngoài qua hậu môn."
                ],
                "bullets": [
                    "Đặc điểm thích nghi hấp thụ: Diện tích tiếp xúc cực lớn (nếp gấp, nhung mao, vi nhung mao), thành ruột mỏng, mạng mao mạch máu và bạch huyết phong phú.",
                    "Gan đóng vai trò điều hòa nồng độ các chất dinh dưỡng trong máu và khử độc trước khi đưa về tim phân phối đi khắp cơ thể."
                ]
            },
            {
                "title": "5. Bảo vệ hệ tiêu hóa và chế độ dinh dưỡng hợp lí",
                "paragraphs": [
                    "Các bệnh thường gặp ở hệ tiêu hóa gồm: sâu răng, viêm loét dạ dày - tá tràng, trào ngược dạ dày thực quản, viêm đại tràng, tiêu chảy, táo bón và sỏi mật.",
                    "Nguyên nhân chủ yếu do ăn uống thiếu vệ sinh, nhiễm vi khuẩn HP (Helicobacter pylori), thói quen ăn uống thất thường, căng thẳng thần kinh kéo dài hoặc ăn nhiều thức ăn cay nóng, dầu mỡ."
                ],
                "bullets": [
                    "Ăn chín, uống sôi, đảm bảo vệ sinh an toàn thực phẩm.",
                    "Ăn đúng giờ, đúng bữa, không bỏ bữa, nhai kĩ no lâu.",
                    "Tạo không khí ăn uống vui vẻ, thoải mái; không vừa ăn vừa xem tivi, đọc sách hay chơi game.",
                    "Bổ sung đủ chất xơ (rau xanh, củ quả) và uống đủ nước để chống táo bón và bảo vệ niêm mạc ruột.",
                    "Đánh răng sạch sẽ sau mỗi bữa ăn và trước khi đi ngủ để phòng ngừa sâu răng."
                ]
            }
        ],
        "terms": [
            {
                "term": "Dinh dưỡng",
                "definition": "Quá trình cơ thể thu nhận, biến đổi và sử dụng các chất dinh dưỡng từ thức ăn để duy trì sự sống, phát triển và phục hồi mô."
            },
            {
                "term": "Tiêu hóa",
                "definition": "Quá trình biến đổi thức ăn thành các chất dinh dưỡng đơn giản mà cơ thể có thể hấp thụ được qua niêm mạc ruột vào máu."
            },
            {
                "term": "Enzyme tiêu hóa",
                "definition": "Các chất xúc tác sinh học đặc hiệu do tuyến tiêu hóa tiết ra để cắt nhỏ các đại phân tử thức ăn phức tạp thành các phân tử dinh dưỡng đơn giản."
            },
            {
                "term": "Nhung mao ruột",
                "definition": "Các nếp gấp li ti trên niêm mạc ruột non giúp tăng diện tích bề mặt hấp thụ chất dinh dưỡng lên gấp hàng trăm lần."
            },
            {
                "term": "Ruột non",
                "definition": "Đoạn dài nhất của ống tiêu hóa, nơi diễn ra quá trình tiêu hóa triệt để nhất và hấp thụ hầu hết các chất dinh dưỡng vào máu."
            }
        ],
        "summary": [
            "Hệ tiêu hóa gồm ống tiêu hóa (miệng, hầu, thực quản, dạ dày, ruột non, ruột già, hậu môn) và tuyến tiêu hóa (tuyến nước bọt, gan, tụy, tuyến vị, tuyến ruột).",
            "Quá trình tiêu hóa gồm tiêu hóa cơ học (cắn, xé, nhào trộn) và tiêu hóa hóa học (nhờ tác dụng xúc tác của enzyme chuyên biệt).",
            "Ở khoang miệng tiêu hóa một phần tinh bột chín; ở dạ dày tiêu hóa một phần protein; ở ruột non toàn bộ thức ăn được biến đổi triệt để thành amino acid, glucose, acid béo và glycerol.",
            "Ruột non là cơ quan hấp thụ chất dinh dưỡng chủ yếu nhờ diện tích tiếp xúc khổng lồ được tạo bởi nếp gấp niêm mạc, nhung mao và vi nhung mao.",
            "Cần duy trì thói quen ăn uống khoa học, ăn chín uống sôi, nhai kĩ và giữ vệ sinh răng miệng để bảo vệ hệ tiêu hóa."
        ],
        "quick_check": [
            {
                "id": "qc-k8-b32-01",
                "question": "Cơ quan nào trong ống tiêu hóa là nơi diễn ra quá trình tiêu hóa triệt để nhất và hấp thụ chất dinh dưỡng chủ yếu?",
                "options": [
                    "A. Dạ dày",
                    "B. Ruột non",
                    "C. Ruột già",
                    "D. Khoang miệng"
                ],
                "answer": "B",
                "explanation": "Ruột non có đầy đủ dịch tụy, dịch mật, dịch ruột chứa hệ enzyme phong phú giúp tiêu hóa triệt để mọi loại thức ăn, đồng thời có cấu tạo nhung mao giúp hấp thụ trên 95% chất dinh dưỡng."
            },
            {
                "id": "qc-k8-b32-02",
                "question": "Enzyme amylase có trong nước bọt ở khoang miệng có chức năng biến đổi chất nào sau đây?",
                "options": [
                    "A. Tinh bột chín thành đường maltose",
                    "B. Protein thành chuỗi peptide ngắn",
                    "C. Lipid thành acid béo và glycerol",
                    "D. Đường maltose thành glucose"
                ],
                "answer": "A",
                "explanation": "Tại khoang miệng, enzyme amylase trong nước bọt chỉ xúc tác biến đổi một phần tinh bột chín thành đường đôi maltose."
            },
            {
                "id": "qc-k8-b32-03",
                "question": "Dịch vị ở dạ dày có tính acid mạnh nhờ chứa chất nào sau đây?",
                "options": [
                    "A. Acid sulfuric (H2SO4)",
                    "B. Acid nitric (HNO3)",
                    "C. Acid clohydric (HCl)",
                    "D. Acid acetic (CH3COOH)"
                ],
                "answer": "C",
                "explanation": "Dịch vị ở dạ dày chứa acid clohydric (HCl) giúp sát khuẩn thức ăn và tạo môi trường acid tối ưu để hoạt hóa enzyme pepsin phân giải protein."
            },
            {
                "id": "qc-k8-b32-04",
                "question": "Đặc điểm cấu tạo nào của ruột non giúp tăng diện tích bề mặt hấp thụ chất dinh dưỡng lên gấp khoảng 600 lần?",
                "options": [
                    "A. Chiều dài ruột rất ngắn và thành ruột dày",
                    "B. Lớp cơ trơn co bóp liên tục không ngừng",
                    "C. Tiết ra lượng dịch mật và dịch tụy rất lớn",
                    "D. Niêm mạc có nhiều nếp gấp, nhung mao và vi nhung mao"
                ],
                "answer": "D",
                "explanation": "Cấu trúc nếp gấp niêm mạc kết hợp hàng triệu nhung mao và vi nhung mao giúp làm tăng diện tích bề mặt hấp thụ của ruột non lên gấp 600 lần, đạt khoảng 400 - 500 m2."
            },
            {
                "id": "qc-k8-b32-05",
                "question": "Tuyến tiêu hóa nào vừa tiết enzyme tiêu hóa đổ vào ruột non, vừa tiết hormone điều hòa lượng đường trong máu?",
                "options": [
                    "A. Tuyến tụy",
                    "B. Gan mật",
                    "C. Tuyến nước bọt",
                    "D. Tuyến vị"
                ],
                "answer": "A",
                "explanation": "Tuyến tụy là tuyến pha: phần ngoại tiết tiết dịch tụy chứa enzyme tiêu hóa đổ vào tá tràng; phần nội tiết tiết hormone insulin và glucagon điều hòa nồng độ glucose trong máu."
            },
            {
                "id": "qc-k8-b32-06",
                "question": "Hành vi nào sau đây là biện pháp khoa học để bảo vệ hệ tiêu hóa?",
                "options": [
                    "A. Vừa ăn vừa lướt mạng xã hội trên điện thoại",
                    "B. Ăn thức ăn thật nhiều ớt cay và nhiều dầu mỡ",
                    "C. Ăn chậm nhai kĩ và ăn chín uống sôi hợp vệ sinh",
                    "D. Bỏ bữa ăn sáng và ăn thật nhiều vào ban đêm"
                ],
                "answer": "C",
                "explanation": "Ăn chậm nhai kĩ giúp thức ăn được nghiền nhỏ và thấm đều enzyme; ăn chín uống sôi giúp phòng tránh ngộ độc thực phẩm và nhiễm khuẩn đường tiêu hóa."
            }
        ]
    },
    {
        "id": "k8-bai-33-mau-va-he-tuan-hoan-cua-co-the-nguoi",
        "grade": 8,
        "number": "Bài 33",
        "title": "Máu và hệ tuần hoàn của cơ thể người",
        "topic": "Thành phần của máu, miễn dịch, vaccine, nhóm máu và hệ tuần hoàn ở người",
        "duration": "40–45 phút",
        "order": 330,
        "active": True,
        "origin": "system",
        "lesson_version": 3,
        "source_label": "SGK KHTN 8 KNTT · Bài 33 · Trang 135–141",
        "content": "Máu gồm huyết tương và các tế bào máu (hồng cầu, bạch cầu, tiểu cầu). Hệ tuần hoàn gồm tim và hệ mạch máu (động mạch, mao mạch, tĩnh mạch), thực hiện vận chuyển các chất dinh dưỡng, khí oxygen đến từng tế bào và mang các chất thải, khí carbon dioxide đến các cơ quan bài tiết để thải ra ngoài.",
        "warmup": {
            "question": "Khi bị thương làm rách da chảy máu, sau một thời gian máu ngừng chảy nhờ cơ chế nào? Máu có vai trò gì đối với sự sống của cơ thể?",
            "hint": "Hãy nhớ lại các tế bào máu như tiểu cầu tham gia vào quá trình đông máu và chức năng vận chuyển chất dinh dưỡng, khí của dòng máu."
        },
        "objectives": [
            "Nêu được chức năng của máu và hệ tuần hoàn trong cơ thể người.",
            "Nêu được các thành phần của máu và chức năng của mỗi thành phần (hồng cầu, bạch cầu, tiểu cầu, huyết tương).",
            "Nêu được khái niệm miễn dịch, kháng nguyên, kháng thể và vai trò của vaccine trong việc phòng bệnh.",
            "Nêu được các nhóm máu hệ ABO và nguyên tắc truyền máu an toàn.",
            "Mô tả được cấu tạo của tim, các mạch máu và hoạt động của 2 vòng tuần hoàn (vòng tuần hoàn lớn và vòng tuần hoàn nhỏ).",
            "Đề xuất được các biện pháp bảo vệ hệ tim mạch và phòng chống các bệnh về máu, tuần hoàn."
        ],
        "sections": [
            {
                "title": "1. Máu và các thành phần của máu",
                "paragraphs": [
                    "Máu là một dạng mô liên kết lỏng lưu thông trong hệ mạch máu khắp cơ thể. Ở người trưởng thành có khoảng 4 đến 5 lít máu. Khi ly tâm hoặc để máu lắng đọng chống đông, máu tách làm hai phần rõ rệt: huyết tương (khoảng 55% thể tích) ở phía trên và các tế bào máu (khoảng 45% thể tích) lắng ở phía dưới.",
                    "Huyết tương có màu vàng nhạt, chứa khoảng 90% nước và 10% các chất dinh dưỡng (glucose, amino acid, lipid), chất khoáng, hormone, kháng thể và các chất thải (urea, acid uric). Huyết tương duy trì máu ở trạng thái lỏng để vận chuyển các chất trong cơ thể."
                ],
                "bullets": [
                    "Hồng cầu: Dạng đĩa lõm hai mặt, không có nhân ở tế bào trưởng thành, chứa huyết sắc tố (hemoglobin - Hb) có màu đỏ. Chức năng chính là vận chuyển khí oxygen (O2) từ phổi đến các tế bào và mang carbon dioxide (CO2) từ các tế bào về phổi để đào thải ra ngoài.",
                    "Bạch cầu: Kích thước lớn, có nhân, có khả năng hình thành chân giả để di chuyển xuyên qua thành mao mạch. Chức năng chính là bảo vệ cơ thể thông qua các phản ứng miễn dịch: thực bào tiêu diệt vi khuẩn, tạo kháng thể vô hiệu hóa độc tố và tiêu diệt các tế bào nhiễm bệnh.",
                    "Tiểu cầu: Là những mảnh tế bào chất không có nhân, dễ vỡ khi tiếp xúc với bề mặt gồ ghề của vết thương. Khi mạch máu bị rách, tiểu cầu giải phóng enzyme biến chất sinh sợi huyết (fibrinogen) hòa tan trong huyết tương thành mạng lưới sợi huyết (fibrin) giữ các tế bào máu lại tạo thành cục máu đông, giúp cầm máu và bảo vệ cơ thể chống mất máu."
                ]
            },
            {
                "title": "2. Miễn dịch và vai trò của vaccine",
                "paragraphs": [
                    "Kháng nguyên là những phân tử lạ (protein hoặc polysaccharide trên bề mặt vi sinh vật như vi khuẩn, virus) có khả năng kích thích cơ thể tạo ra đáp ứng miễn dịch. Kháng thể là các phân tử protein đặc hiệu do bạch cầu (tế bào lympho B) tiết ra, có khả năng liên kết chính xác với kháng nguyên tương ứng theo cơ chế chìa khóa và ổ khóa để bất hoạt hoặc tiêu diệt mầm bệnh.",
                    "Miễn dịch là khả năng của cơ thể nhận biết và tiêu diệt các tác nhân gây hại xâm nhập. Cơ thể có miễn dịch tự nhiên (bẩm sinh hoặc sau khi khỏi bệnh) và miễn dịch nhân tạo (nhờ tiêm vaccine)."
                ],
                "bullets": [
                    "Vaccine (vắc-xin): Là chế phẩm sinh học chứa mầm bệnh đã bị làm yếu, bất hoạt (chết) hoặc các kháng nguyên tinh sạch của mầm bệnh.",
                    "Cơ chế bảo vệ của vaccine: Khi tiêm vaccine vào cơ thể, hệ miễn dịch được kích thích sản sinh ra kháng thể và hình thành các tế bào nhớ (tế bào lympho nhớ). Khi mầm bệnh thật xâm nhập sau này, tế bào nhớ sẽ nhanh chóng sản xuất lượng lớn kháng thể để tiêu diệt mầm bệnh trước khi chúng kịp gây hại.",
                    "Ý nghĩa của tiêm chủng: Tiêm chủng đầy đủ và đúng lịch là biện pháp phòng bệnh chủ động hiệu quả nhất để bảo vệ bản thân và tạo miễn dịch cộng đồng."
                ]
            },
            {
                "title": "3. Nhóm máu và nguyên tắc truyền máu",
                "paragraphs": [
                    "Ở người, hệ nhóm máu ABO là quan trọng nhất, được xác định dựa trên sự có mặt của kháng nguyên A và B trên màng hồng cầu, cùng các kháng thể alpha (anti-A) và beta (anti-B) trong huyết tương.",
                    "Nguyên tắc truyền máu: Khi truyền máu, tuyệt đối không để kháng nguyên trên màng hồng cầu của người cho bị ngưng kết bởi kháng thể tương ứng trong huyết tương của người nhận (A gặp anti-A, B gặp anti-B sẽ gây ngưng kết hồng cầu, làm tắc mạch máu và đe dọa tính mạng). Do đó, an toàn nhất là truyền cùng nhóm máu. Ngoài ra, máu truyền phải được xét nghiệm nghiêm ngặt để đảm bảo không chứa mầm bệnh nguy hiểm (HIV, viêm gan B, viêm gan C, giang mai...)."
                ],
                "bullets": [
                    "Nhóm máu A: Hồng cầu chứa kháng nguyên A, huyết tương chứa kháng thể beta (anti-B).",
                    "Nhóm máu B: Hồng cầu chứa kháng nguyên B, huyết tương chứa kháng thể alpha (anti-A).",
                    "Nhóm máu AB: Hồng cầu chứa cả kháng nguyên A và B, huyết tương không có kháng thể alpha và beta.",
                    "Nhóm máu O: Hồng cầu không có cả kháng nguyên A và B, huyết tương chứa cả kháng thể alpha và beta."
                ]
            },
            {
                "title": "4. Cấu tạo và hoạt động của hệ tuần hoàn",
                "paragraphs": [
                    "Hệ tuần hoàn gồm tim và hệ thống mạch máu. Tim là cơ quan rỗng có vách ngăn chia thành 4 ngăn: hai tâm nhĩ ở trên (thành mỏng, nhận máu từ tĩnh mạch về) và hai tâm thất ở dưới (thành cơ dày, đặc biệt tâm thất trái dày nhất để tạo lực bơm máu đi khắp cơ thể). Giữa tâm nhĩ và tâm thất có van nhĩ - thất, giữa tâm thất và động mạch có van động mạch, giúp máu chỉ chảy theo một chiều nhất định.",
                    "Hệ mạch gồm có: Động mạch (dẫn máu từ tim đến các cơ quan, thành dày và đàn hồi cao), Mao mạch (nối giữa động mạch và tĩnh mạch, thành mỏng chỉ gồm một lớp tế bào nội mô để trao đổi chất và khí với tế bào mô), Tĩnh mạch (dẫn máu từ các cơ quan trở về tim, lòng rộng và có các van một chiều ở chi dưới)."
                ],
                "bullets": [
                    "Vòng tuần hoàn nhỏ (vòng phổi): Máu đỏ thẫm (giàu CO2) từ tâm thất phải -> động mạch phổi -> mao mạch phổi (thải CO2, hấp thụ O2 biến thành máu đỏ tươi) -> tĩnh mạch phổi -> tâm nhĩ trái.",
                    "Vòng tuần hoàn lớn (vòng cơ thể): Máu đỏ tươi (giàu O2 và dinh dưỡng) từ tâm thất trái -> động mạch chủ -> các cơ quan -> mao mạch các mô (cung cấp O2 và dưỡng chất, nhận CO2 và chất thải biến thành máu đỏ thẫm) -> tĩnh mạch chủ -> tâm nhĩ phải."
                ]
            },
            {
                "title": "5. Bảo vệ hệ tuần hoàn và phòng chống bệnh tim mạch",
                "paragraphs": [
                    "Hệ tuần hoàn làm việc liên tục suốt đời người. Các bệnh tim mạch như tăng huyết áp, xơ vữa động mạch, nhồi máu cơ tim, đột quỵ và thiếu máu là những nguyên nhân gây tử vong hàng đầu nếu không được phát hiện và phòng ngừa sớm."
                ],
                "bullets": [
                    "Luyện tập thể dục thể thao đều đặn, vừa sức giúp tăng cường sức co bóp của cơ tim và khả năng lưu thông máu.",
                    "Chế độ ăn uống hợp lí: Giảm bớt lượng muối ăn, hạn chế thức ăn nhiều dầu mỡ động vật (chứa nhiều cholesterol gây xơ vữa động mạch), bổ sung nhiều rau củ quả tươi giàu chất xơ và vitamin.",
                    "Tránh các chất kích thích: Tuyệt đối không hút thuốc lá (nicotin làm co mạch, tăng huyết áp), hạn chế rượu bia, tránh căng thẳng thần kinh (stress kéo dài).",
                    "Sơ cứu vết thương chảy máu: Đè chặt tay lên vết thương bằng gạc vô trùng hoặc băng ép; nếu máu chảy xối xả từ động mạch cần đặt garo phía trên vết thương và đưa ngay đến cơ sở y tế gần nhất."
                ]
            }
        ],
        "diagram": {
            "title": "Sơ đồ hệ tuần hoàn máu ở người",
            "nodes": [
                "Máu (Huyết tương + Tế bào máu)",
                "Tim (Bơm hút & đẩy máu)",
                "Vòng tuần hoàn phổi (Trao đổi khí)",
                "Vòng tuần hoàn cơ thể (Nuôi dưỡng tế bào)"
            ]
        },
        "terms": [
            {
                "term": "Huyết tương",
                "definition": "Phần dịch lỏng màu vàng của máu (chiếm khoảng 55% thể tích máu), duy trì máu ở trạng thái lỏng và vận chuyển chất dinh dưỡng, hormone, chất khoáng và chất thải."
            },
            {
                "term": "Hồng cầu",
                "definition": "Tế bào máu hình đĩa lõm hai mặt, không nhân khi trưởng thành, chứa huyết sắc tố hemoglobin có chức năng vận chuyển khí oxygen và carbon dioxide."
            },
            {
                "term": "Bạch cầu",
                "definition": "Tế bào máu có nhân, đóng vai trò then chốt trong hệ miễn dịch bảo vệ cơ thể thông qua cơ chế thực bào và tiết kháng thể tiêu diệt mầm bệnh."
            },
            {
                "term": "Tiểu cầu",
                "definition": "Những mảnh tế bào chất không nhân tham gia vào quá trình đông máu giúp bịt kín vết thương và chống mất máu."
            },
            {
                "term": "Kháng nguyên",
                "definition": "Chất lạ (thường là protein hoặc polysaccharide trên bề mặt mầm bệnh) xâm nhập vào cơ thể kích thích hệ miễn dịch tạo đáp ứng miễn dịch."
            },
            {
                "term": "Kháng thể",
                "definition": "Phân tử protein do lympho B tiết ra có khả năng liên kết đặc hiệu với kháng nguyên tương ứng theo cơ chế chìa khóa và ổ khóa để vô hiệu hóa kháng nguyên."
            },
            {
                "term": "Vaccine",
                "definition": "Chế phẩm sinh học chứa mầm bệnh đã suy yếu, bất hoạt hoặc kháng nguyên tinh sạch nhằm kích thích cơ thể chủ động tạo miễn dịch phòng bệnh."
            },
            {
                "term": "Hệ tuần hoàn",
                "definition": "Hệ cơ quan gồm tim và hệ mạch máu thực hiện vận chuyển máu mang oxygen và chất dinh dưỡng đến các tế bào, đồng thời mang chất thải và CO2 đến cơ quan bài tiết."
            }
        ],
        "summary": [
            "Máu gồm huyết tương (chiếm 55%) và các tế bào máu (hồng cầu, bạch cầu, tiểu cầu - chiếm 45%).",
            "Kháng nguyên kích thích cơ thể sinh kháng thể đặc hiệu; tiêm vaccine là biện pháp phòng bệnh chủ động hiệu quả nhất.",
            "Hệ nhóm máu ABO gồm 4 nhóm máu: A, B, AB, O; nguyên tắc truyền máu là không để kháng thể người nhận ngưng kết kháng nguyên người cho.",
            "Hệ tuần hoàn gồm tim (bơm 4 ngăn) và hệ mạch (động mạch, mao mạch, tĩnh mạch) hoạt động qua vòng tuần hoàn phổi và vòng tuần hoàn cơ thể.",
            "Luyện tập thể dục thể thao, chế độ ăn ít muối, ít dầu mỡ và lối sống lành mạnh giúp bảo vệ hệ tim mạch khỏe mạnh."
        ],
        "quick_check": [
            {
                "question": "Thành phần nào của máu đóng vai trò chính trong việc vận chuyển khí oxygen và carbon dioxide?",
                "options": [
                    "Huyết tương",
                    "Hồng cầu",
                    "Bạch cầu",
                    "Tiểu cầu"
                ],
                "answer_index": 1,
                "explanation": "Hồng cầu chứa huyết sắc tố hemoglobin có khả năng kết hợp thuận nghịch với O2 và CO2 để vận chuyển khí."
            },
            {
                "question": "Người có nhóm máu A trong huyết tương có chứa loại kháng thể nào?",
                "options": [
                    "Kháng thể alpha (anti-A)",
                    "Kháng thể beta (anti-B)",
                    "Không có kháng thể",
                    "Cả kháng thể alpha và beta"
                ],
                "answer_index": 1,
                "explanation": "Người nhóm máu A có kháng nguyên A trên hồng cầu và kháng thể beta (anti-B) trong huyết tương."
            },
            {
                "question": "Ngăn tim nào có thành cơ dày nhất để tạo lực bơm máu vào động mạch chủ đi nuôi toàn bộ cơ thể?",
                "options": [
                    "Tâm nhĩ phải",
                    "Tâm nhĩ trái",
                    "Tâm thất phải",
                    "Tâm thất trái"
                ],
                "answer_index": 3,
                "explanation": "Tâm thất trái phải tạo áp lực tống máu đi khắp vòng tuần hoàn lớn nuôi toàn bộ cơ thể nên có thành cơ dày nhất."
            }
        ]
    },
    {
        "id": "k8-b34-ho-hap",
        "grade": 8,
        "number": "Bài 34",
        "title": "Hệ hô hấp ở người",
        "topic": "Sinh học cơ thể người",
        "duration": "3 tiết (135 phút)",
        "order": 340,
        "active": True,
        "origin": "official_curriculum",
        "lesson_version": 5,
        "source_label": "SGK KHTN 8 KNTT – Bài 34 – Trang 142–146",
        "content": "Hệ hô hấp ở người gồm đường dẫn khí và hai lá phổi; thực hiện hoạt động thông khí ở phổi qua cử động hô hấp và cơ chế trao đổi khí O2 và CO2 theo nguyên lí khuếch tán tại phế nang và tế bào cơ thể.",
        "warmup": "Một người có thể nhịn ăn vài tuần, nhịn uống vài ngày, nhưng chỉ cần ngừng thở vài phút là có thể tử vong. Vì sao cơ thể chúng ta lại cần hít thở liên tục không ngừng nghỉ?",
        "objectives": [
            "Trình bày được cấu tạo và chức năng của các cơ quan trong hệ hô hấp (đường dẫn khí và phổi).",
            "Mô tả được hoạt động thông khí ở phổi thông qua cử động hít vào và thở ra.",
            "Giải thích được cơ chế trao đổi khí ở phế nang phổi và ở tế bào cơ thể theo nguyên lí khuếch tán.",
            "Nêu được tác hại của khói thuốc lá, bụi mịn và các biện pháp bảo vệ hệ hô hấp, rèn luyện đường thở khỏe mạnh."
        ],
        "sections": [
            {
                "title": "1. Cấu tạo của hệ hô hấp ở người",
                "paragraphs": [
                    "Hệ hô hấp ở người gồm hai bộ phận chính: đường dẫn khí và cơ quan trao đổi khí là hai lá phổi.",
                    "Đường dẫn khí gồm: mũi, họng (hầu), thanh quản, khí quản và phế quản. Đường dẫn khí có chức năng dẫn khí vào và ra khỏi phổi, đồng thời làm ấm, làm ẩm và làm sạch không khí hít vào nhờ lớp niêm mạc có chất nhầy, mao mạch máu dày đặc và hệ thống lông rung chuyển động liên tục.",
                    "Phổi gồm hai lá phổi (phổi phải có 3 thùy, phổi trái có 2 thùy nhường chỗ cho tim). Bề mặt phổi được bao bọc bởi màng phổi gồm hai lớp, ở giữa có lớp dịch mỏng giúp phổi trượt dễ dàng trên thành lồng ngực khi thở.",
                    "Đơn vị cấu tạo và chức năng của phổi là phế nang. Hai lá phổi chứa khoảng 700 - 800 triệu phế nang, tạo ra diện tích bề mặt trao đổi khí khổng lồ lên tới 70 - 100 m2. Thành phế nang rất mỏng (chỉ gồm một lớp tế bào biểu mô) và được bao bọc bởi mạng lưới mao mạch máu dày đặc."
                ],
                "bullets": [
                    "Mũi: có lông mũi ngăn bụi, lớp niêm mạc tiết chất nhầy giữ bụi mịn và diệt khuẩn, mạng mao mạch sưởi ấm không khí.",
                    "Nắp thanh quản (sụn thanh thiệt): tự động đậy kín đường hô hấp khi nuốt thức ăn, ngăn không cho thức ăn rơi vào khí quản.",
                    "Khí quản: ống dẫn khí cấu tạo từ 16 - 20 vòng sụn hình chữ C khuyết ở phía sau giúp đường thở luôn mở rộng.",
                    "Phế nang: các túi khí li ti là nơi diễn ra sự trao đổi khí trực tiếp giữa không khí và máu."
                ]
            },
            {
                "title": "2. Hoạt động thông khí ở phổi",
                "paragraphs": [
                    "Thông khí ở phổi là quá trình làm mới không khí liên tục trong phế nang, được thực hiện thông qua các cử động hô hấp gồm một lần hít vào và một lần thở ra.",
                    "Cơ chế hít vào (chủ động): Cơ liên sườn ngoài co nâng xương sườn lên, cơ hoành co phẳng hạ xuống làm thể tích khoang ngực tăng lên -> áp suất trong phổi giảm thấp hơn áp suất khí quyển -> không khí giàu O2 từ ngoài tràn vào phổi.",
                    "Cơ chế thở ra (thụ động khi nghỉ ngơi): Cơ liên sườn ngoài và cơ hoành dãn ra, xương sườn hạ xuống và cơ hoành nhô lên làm thể tích khoang ngực giảm -> áp suất trong phổi tăng cao hơn áp suất khí quyển -> đẩy không khí giàu CO2 từ phổi ra ngoài."
                ],
                "bullets": [
                    "Nhịp hô hấp: Số lần cử động hô hấp trong một phút (người trưởng thành bình thường khoảng 16 - 18 lần/phút).",
                    "Dung tích sống: Thể tích không khí lớn nhất mà một người có thể thở ra sau khi đã hít vào hết sức. Dung tích sống càng lớn chứng tỏ dung lượng phổi và sức khỏe hô hấp càng tốt."
                ]
            },
            {
                "title": "3. Cơ chế trao đổi khí ở phổi và ở tế bào",
                "paragraphs": [
                    "Sự trao đổi khí ở phổi (giữa phế nang và máu) và ở tế bào (giữa máu và tế bào) đều tuân theo cơ chế khuếch tán đơn thuần: chất khí khuếch tán từ nơi có nồng độ (áp suất riêng phần) cao đến nơi có nồng độ thấp.",
                    "Trao đổi khí ở phổi: Nồng độ O2 trong phế nang cao hơn trong máu mao mạch phổi nên O2 khuếch tán từ phế nang vào máu, liên kết với hemoglobin tạo oxyhemoglobin (HbO2) làm máu đỏ thẫm biến thành máu đỏ tươi. Ngược lại, nồng độ CO2 trong máu mao mạch phổi cao hơn trong phế nang nên CO2 khuếch tán từ máu vào phế nang để thải ra ngoài.",
                    "Trao đổi khí ở tế bào: Nồng độ O2 trong máu mao mạch cao hơn trong tế bào nên O2 khuếch tán từ máu vào tế bào để tham gia hô hấp tế bào tạo ATP. Ngược lại, nồng độ CO2 do chuyển hóa tế bào sinh ra cao hơn trong máu nên CO2 khuếch tán từ tế bào vào máu, làm máu đỏ tươi biến thành máu đỏ thẫm rồi theo tĩnh mạch trở về tim."
                ],
                "bullets": [
                    "Tại phế nang: O2 khuếch tán (Phế nang -> Máu); CO2 khuếch tán (Máu -> Phế nang).",
                    "Tại tế bào: O2 khuếch tán (Máu -> Tế bào); CO2 khuếch tán (Tế bào -> Máu)."
                ]
            },
            {
                "title": "4. Bảo vệ hệ hô hấp và rèn luyện đường thở",
                "paragraphs": [
                    "Các tác nhân gây hại hệ hô hấp gồm: khói thuốc lá, bụi mịn (PM2.5, PM10), khí độc (CO, SO2, NO2) và các vi sinh vật gây bệnh (virus cúm, vi khuẩn lao, virus SARS-CoV-2).",
                    "Tác hại của khói thuốc lá: Chứa nicotine làm tê liệt và phá hủy hệ thống lông rung đường thở; khí CO chiếm chỗ của O2 khi liên kết bền vững với hemoglobin làm giảm khả năng vận chuyển dưỡng khí; chất hắc ín gây viêm phế quản mạn tính và ung thư phổi."
                ],
                "bullets": [
                    "Không hút thuốc lá và tránh xa khói thuốc lá thụ động.",
                    "Đeo khẩu trang đạt chuẩn khi tham gia giao thông và làm việc ở môi trường nhiều khói bụi.",
                    "Trồng nhiều cây xanh xung quanh nhà và trường học để thanh lọc không khí.",
                    "Tập thể dục thể thao đều đặn và tập hít thở sâu để tăng dung tích sống của phổi."
                ]
            }
        ],
        "terms": [
            {
                "term": "Phế nang",
                "definition": "Đơn vị cấu tạo và chức năng của phổi, có màng siêu mỏng và mạng mao mạch dày đặc để trao đổi khí O2 và CO2."
            },
            {
                "term": "Trao đổi khí",
                "definition": "Quá trình khuếch tán O2 từ ngoài vào máu và CO2 từ máu ra ngoài diễn ra tại phế nang và tế bào."
            },
            {
                "term": "Thông khí ở phổi",
                "definition": "Quá trình hít vào và thở ra liên tục giúp làm mới không khí bên trong các phế nang phổi."
            },
            {
                "term": "Dung tích sống",
                "definition": "Lượng không khí tối đa có thể tống ra khỏi phổi sau một lần hít vào sâu tối đa."
            }
        ],
        "summary": [
            "Hệ hô hấp gồm đường dẫn khí (mũi, họng, thanh quản, khí quản, phế quản) và hai lá phổi.",
            "Đường dẫn khí có chức năng dẫn khí, làm ấm, làm ẩm và làm sạch không khí hít vào.",
            "Thông khí ở phổi nhờ cử động hít vào và thở ra làm thay đổi thể tích lồng ngực do cơ liên sườn và cơ hoành co dãn.",
            "Sự trao đổi khí ở phế nang và ở tế bào diễn ra theo cơ chế khuếch tán từ nơi nồng độ cao sang nơi nồng độ thấp.",
            "Cần giữ môi trường không khí trong lành, không hút thuốc lá và tập thở sâu để bảo vệ hệ hô hấp."
        ],
        "quick_check": [
            {
                "id": "qc-k8-b34-01",
                "question": "Sự trao đổi khí ở phế nang phổi và ở tế bào mô diễn ra theo cơ chế nào sau đây?",
                "options": [
                    "A. Vận chuyển chủ động tiêu tốn ATP",
                    "B. Cơ chế khuếch tán từ nơi nồng độ cao đến nơi nồng độ thấp",
                    "C. Thẩm thấu theo gradient nồng độ muối",
                    "D. Thực bào và xuất bào qua màng sinh chất"
                ],
                "answer": "B",
                "explanation": "Cả ở phế nang và tế bào, O2 và CO2 đều khuếch tán hoàn toàn tự nhiên từ nơi có nồng độ (phân áp) cao sang nơi có nồng độ thấp qua màng mao mạch mỏng."
            },
            {
                "id": "qc-k8-b34-02",
                "question": "Khi hít vào bình thường, cơ hoành và cơ liên sườn ngoài có trạng thái hoạt động như thế nào?",
                "options": [
                    "A. Cơ hoành co hạ xuống, cơ liên sườn co nâng lồng ngực",
                    "B. Cơ hoành dãn nâng lên, cơ liên sườn dãn hạ lồng ngực",
                    "C. Cơ hoành co nâng lên, cơ liên sườn dãn ra",
                    "D. Cả cơ hoành và cơ liên sườn đều dãn hoàn toàn"
                ],
                "answer": "A",
                "explanation": "Khi hít vào, cơ hoành co hạ phẳng xuống và cơ liên sườn co kéo xương sườn lên làm tăng thể tích lồng ngực, hạ áp suất trong phổi để hút không khí vào."
            },
            {
                "id": "qc-k8-b34-03",
                "question": "Cấu tạo nào của phổi đóng vai trò là đơn vị cấu tạo và chức năng trực tiếp thực hiện trao đổi khí?",
                "options": [
                    "A. Khí quản",
                    "B. Phế quản chính",
                    "C. Phế nang",
                    "D. Màng phổi"
                ],
                "answer": "C",
                "explanation": "Phế nang là các túi khí li ti với thành chỉ gồm một lớp tế bào và mạng mao mạch bọc ngoài, là nơi trực tiếp trao đổi khí giữa máu và không khí."
            },
            {
                "id": "qc-k8-b34-04",
                "question": "Khí độc nào trong khói thuốc lá có khả năng liên kết rất chặt với hemoglobin, chiếm chỗ của oxygen gây ngạt tế bào?",
                "options": [
                    "A. Khí Carbon dioxide (CO2)",
                    "B. Khí Sulfur dioxide (SO2)",
                    "C. Khí Nitrogen (N2)",
                    "D. Khí Carbon monoxide (CO)"
                ],
                "answer": "D",
                "explanation": "Khí CO kết hợp với hemoglobin bền gấp hơn 200 lần so với O2, làm mất khả năng vận chuyển O2 của hồng cầu, gây thiếu dưỡng khí trầm trọng cho tế bào não và tim."
            },
            {
                "id": "qc-k8-b34-05",
                "question": "Bộ phận nào của đường dẫn khí có cấu tạo sụn tự động đậy kín đường thở khi nuốt để chống sặc thức ăn?",
                "options": [
                    "A. Nắp thanh quản (sụn thanh thiệt)",
                    "B. Lông mũi",
                    "C. Vòng sụn khí quản",
                    "D. Hốc mũi"
                ],
                "answer": "A",
                "explanation": "Nắp thanh quản (sụn thanh thiệt) tự động hạ xuống đậy kín lỗ thanh quản khi nuốt thức ăn, ngăn không cho thức ăn rơi vào đường thở."
            },
            {
                "id": "qc-k8-b34-06",
                "question": "Biện pháp nào sau đây giúp rèn luyện dung tích sống của phổi đạt hiệu quả cao nhất?",
                "options": [
                    "A. Thường xuyên ngồi trong phòng điều hòa đóng kín cửa",
                    "B. Luyện tập thể thao đều đặn và tập hít thở sâu",
                    "C. Hút thuốc lá điện tử thay cho thuốc lá truyền thống",
                    "D. Thở nhanh và nông liên tục cả ngày"
                ],
                "answer": "B",
                "explanation": "Tập thể dục thể thao kết hợp hít thở sâu giúp các phế nang giãn nở tối đa, tăng cường sức co bóp của cơ hô hấp và nâng cao dung tích sống của phổi."
            }
        ]
    },
    {
        "id": "k8-b35-bai-tiet",
        "grade": 8,
        "number": "Bài 35",
        "title": "Hệ bài tiết ở người",
        "topic": "Sinh học cơ thể người",
        "duration": "2 tiết (90 phút)",
        "order": 350,
        "active": True,
        "origin": "official_curriculum",
        "lesson_version": 5,
        "source_label": "SGK KHTN 8 KNTT – Bài 35 – Trang 147–151",
        "content": "Hệ bài tiết ở người thực hiện chức năng lọc máu và thải các chất cặn bã, độc hại ra ngoài cơ thể; cấu tạo hệ bài tiết nước tiểu gồm hai quả thận, ống dẫn nước tiểu, bóng đái và ống đái; cơ chế tạo thành nước tiểu qua 3 giai đoạn tại nephron.",
        "warmup": "Mỗi ngày cơ thể chúng ta nạp vào rất nhiều thức ăn và nước uống. Các chất cặn bã sinh ra từ quá trình trao đổi chất sẽ được đào thải ra ngoài bằng những con đường nào? Vì sao thận lại được ví như 'nhà máy lọc chất độc' của cơ thể?",
        "objectives": [
            "Nêu được khái niệm bài tiết và vai trò của bài tiết đối với cơ thể sống.",
            "Mô tả được cấu tạo của hệ bài tiết nước tiểu (thận, ống dẫn nước tiểu, bóng đái, ống đái) và cấu tạo đơn vị chức năng của thận (nephron).",
            "Trình bày được 3 giai đoạn của quá trình tạo thành nước tiểu: lọc máu ở cầu thận, hấp thụ lại và bài tiết tiếp ở ống thận.",
            "Phân biệt được nước tiểu đầu và nước tiểu chính thức.",
            "Vận dụng kiến thức để giải thích nguyên nhân tạo sỏi thận và đề xuất các biện pháp bảo vệ hệ bài tiết khỏe mạnh."
        ],
        "sections": [
            {
                "title": "1. Khái niệm và vai trò của bài tiết",
                "paragraphs": [
                    "Bài tiết là quá trình lọc và thải các chất cặn bã, chất độc hại và chất dư thừa sinh ra từ các hoạt động chuyển hóa của tế bào ra khỏi cơ thể.",
                    "Các cơ quan tham gia bài tiết trong cơ thể người gồm: Phổi bài tiết khí CO2 và hơi nước; Da bài tiết mồ hôi chứa nước, muối khoáng và một ít ure; Hệ bài tiết nước tiểu là cơ quan bài tiết chủ yếu, đảm nhận thải bỏ tới 90% các sản phẩm chuyển hóa hòa tan trong máu (ure, acid uric, creatinin, muối thừa).",
                    "Vai trò của bài tiết: Giúp thanh lọc cơ thể, chống nhiễm độc nội bào và duy trì tính ổn định của các điều kiện lí - hóa trong môi trường trong (cân bằng nội môi như nồng độ ion, thể tích máu, huyết áp và độ pH)."
                ],
                "bullets": [
                    "Sản phẩm bài tiết chính: CO2 (qua phổi), mồ hôi (qua da), nước tiểu chứa ure, acid uric, muối khoáng thừa (qua thận).",
                    "Thận đóng vai trò trung tâm trong việc thanh lọc máu và duy trì cân bằng nước, điện giải."
                ]
            },
            {
                "title": "2. Cấu tạo của hệ bài tiết nước tiểu",
                "paragraphs": [
                    "Hệ bài tiết nước tiểu gồm có: hai quả thận, hai ống dẫn nước tiểu, một bóng đái (bàng quang) và một ống đái.",
                    "Hai quả thận hình hạt đậu, màu đỏ nâu, nằm ở hai bên cột sống phía sau phúc mạc khoang bụng ngang đốt sống thắt lưng. Mỗi quả thận gồm phần vỏ, phần tủy và bể thận.",
                    "Đơn vị cấu tạo và chức năng của thận là nephron. Mỗi quả thận người chứa khoảng 1 triệu nephron. Mỗi nephron gồm có ba phần liên hoàn: Cầu thận (cuộn mao mạch máu), Nang cầu thận (nang Bowman - một túi lõm hình cầu bao bọc ngoài cầu thận) và Ống thận (uốn lượn được bao quanh bởi mạng lưới mao mạch)."
                ],
                "bullets": [
                    "Thận: cơ quan lọc máu chính để tạo ra nước tiểu.",
                    "Ống dẫn nước tiểu: dẫn nước tiểu chính thức từ bể thận xuống bóng đái.",
                    "Bóng đái (bàng quang): túi cơ đàn hồi chứa nước tiểu tạm thời trước khi thải ra ngoài.",
                    "Ống đái: đường thoát nước tiểu từ bóng đái ra ngoài cơ thể."
                ]
            },
            {
                "title": "3. Quá trình tạo thành nước tiểu",
                "paragraphs": [
                    "Quá trình tạo thành nước tiểu diễn ra liên tục tại các nephron của thận qua 3 giai đoạn kế tiếp nhau:",
                    "1. Giai đoạn lọc máu ở cầu thận: Máu theo động mạch đến cầu thận với áp lực lớn. Nước và các phân tử nhỏ hòa tan được lọc qua vách mao mạch cầu thận và màng nang cầu thận vào nang Bowman để tạo thành nước tiểu đầu. Tế bào máu và protein huyết tương có kích thước lớn không qua được màng lọc nên ở lại trong máu. Mỗi ngày có khoảng 170 – 180 lít nước tiểu đầu được tạo ra.",
                    "2. Giai đoạn hấp thụ lại ở ống thận: Nước tiểu đầu chảy qua ống thận. Tại đây, các tế bào ống thận chủ động hấp thụ lại đến 99% lượng nước, toàn bộ chất dinh dưỡng (glucose, amino acid), vitamin và các ion cần thiết (Na+, Cl-, HCO3-) trở lại mạng mao mạch quanh ống thận.",
                    "3. Giai đoạn bài tiết tiếp ở ống thận: Các tế bào thành ống thận chủ động bài tiết tiếp các chất cặn bã, chất độc hại (ure, acid uric, creatinin, thuốc, chất màu) và các ion thừa (H+, K+) từ máu vào lòng ống thận. Dung dịch còn lại sau giai đoạn này là nước tiểu chính thức (khoảng 1,5 – 2 lít mỗi ngày). Nước tiểu chính thức theo ống góp đổ vào bể thận, xuống bóng đái và thải ra ngoài."
                ],
                "bullets": [
                    "So sánh nước tiểu đầu và nước tiểu chính thức:",
                    "  * Nước tiểu đầu: Nồng độ chất hòa tan loãng, còn chứa nhiều chất dinh dưỡng hữu ích (glucose, vitamin), thể tích rất lớn (170 - 180 lít/ngày).",
                    "  * Nước tiểu chính thức: Nồng độ chất cặn bã (ure, acid uric) rất đậm đặc, không còn chất dinh dưỡng, thể tích nhỏ (1,5 - 2 lít/ngày)."
                ]
            },
            {
                "title": "4. Bảo vệ hệ bài tiết và phòng chống bệnh thận",
                "paragraphs": [
                    "Một số bệnh thường gặp ở hệ bài tiết nước tiểu: sỏi thận, sỏi bàng quang, viêm cầu thận, suy thận và nhiễm khuẩn đường tiết niệu.",
                    "Nguyên nhân gây sỏi thận: Do thói quen uống quá ít nước, ăn quá mặn, ăn nhiều thực phẩm giàu oxalate, hoặc nhịn tiểu làm cho các muối khoáng (calci oxalate, phosphat, acid uric) bị cô đặc, kết tinh và lắng đọng lâu ngày tạo thành sỏi làm tắc nghẽn đường dẫn nước tiểu."
                ],
                "bullets": [
                    "Uống đủ 1,5 – 2 lít nước mỗi ngày để hòa tan chất cặn bã, tránh lắng đọng tạo sỏi.",
                    "Không nhịn tiểu khi có nhu cầu, tránh làm bóng đái bị căng giãn quá mức và ngăn vi khuẩn tích tụ gây nhiễm khuẩn ngược dòng.",
                    "Ăn uống cân đối, hạn chế ăn thức ăn quá mặn, quá chua hoặc quá nhiều dầu mỡ động vật.",
                    "Giữ vệ sinh cơ quan sinh dục ngoài sạch sẽ hàng ngày để tránh vi khuẩn xâm nhập vào đường niệu đạo.",
                    "Không lạm dụng thuốc kháng sinh và thuốc giảm đau bừa bãi tránh gây độc hại cho tế bào thận."
                ]
            }
        ],
        "terms": [
            {
                "term": "Bài tiết",
                "definition": "Quá trình lọc và thải các chất cặn bã, chất độc và chất dư thừa từ chuyển hóa nội bào ra ngoài cơ thể để duy trì cân bằng nội môi."
            },
            {
                "term": "Nephron",
                "definition": "Đơn vị cấu tạo và chức năng của thận, gồm cầu thận, nang cầu thận và ống thận, thực hiện nhiệm vụ lọc máu tạo nước tiểu."
            },
            {
                "term": "Nước tiểu đầu",
                "definition": "Chất lỏng tạo ra sau khi máu được lọc qua màng cầu thận vào nang Bowman, còn chứa nhiều nước và chất dinh dưỡng."
            },
            {
                "term": "Nước tiểu chính thức",
                "definition": "Nước tiểu đậm đặc hoàn chỉnh ở cuối ống thận sau khi đã hấp thụ lại 99% nước, dinh dưỡng và bài tiết thêm chất cặn bã."
            },
            {
                "term": "Sỏi thận",
                "definition": "Khối khoáng chất rắn kết tinh trong thận do lắng đọng muối khoáng (canxi, phosphat, oxalat) khi uống thiếu nước hoặc nhịn tiểu."
            }
        ],
        "summary": [
            "Hệ bài tiết nước tiểu gồm: 2 quả thận, 2 ống dẫn nước tiểu, bóng đái và ống đái.",
            "Mỗi quả thận chứa khoảng 1 triệu nephron (gồm cầu thận, nang cầu thận và ống thận).",
            "Quá trình tạo thành nước tiểu gồm 3 giai đoạn: lọc máu ở cầu thận (tạo nước tiểu đầu), hấp thụ lại ở ống thận (giữ lại 99% nước và dinh dưỡng) và bài tiết tiếp ở ống thận (tạo nước tiểu chính thức).",
            "Mỗi ngày tạo ra 170 - 180 lít nước tiểu đầu nhưng chỉ có khoảng 1,5 - 2 lít nước tiểu chính thức được thải ra ngoài.",
            "Cần uống đủ 1,5 - 2 lít nước mỗi ngày, không nhịn tiểu và hạn chế ăn mặn để phòng tránh sỏi thận và suy thận."
        ],
        "quick_check": [
            {
                "id": "qc-k8-b35-01",
                "question": "Mỗi nephron (đơn vị chức năng của thận) được cấu tạo từ những bộ phận nào sau đây?",
                "options": [
                    "A. Cầu thận, nang cầu thận và ống thận",
                    "B. Ống dẫn nước tiểu, bóng đái và ống đái",
                    "C. Phần vỏ, phần tủy và bể thận",
                    "D. Động mạch thận và tĩnh mạch thận"
                ],
                "answer": "A",
                "explanation": "Mỗi nephron gồm cầu thận (chùm mao mạch lọc máu), nang cầu thận (nang Bowman bao bọc ngoài) và hệ thống ống thận (uốn lượn thực hiện hấp thụ lại và bài tiết tiếp)."
            },
            {
                "id": "qc-k8-b35-02",
                "question": "Quá trình lọc máu ở cầu thận tạo ra sản phẩm nào sau đây?",
                "options": [
                    "A. Nước tiểu chính thức",
                    "B. Nước tiểu đầu",
                    "C. Dịch bạch huyết",
                    "D. Huyết tương cô đặc"
                ],
                "answer": "B",
                "explanation": "Quá trình lọc máu qua vách mao mạch cầu thận vào nang Bowman tạo ra khoảng 170 - 180 lít nước tiểu đầu mỗi ngày."
            },
            {
                "id": "qc-k8-b35-03",
                "question": "Điểm khác biệt cơ bản nhất giữa nước tiểu đầu và nước tiểu chính thức là gì?",
                "options": [
                    "A. Nước tiểu đầu có màu vàng sẫm còn nước tiểu chính thức không màu",
                    "B. Nước tiểu đầu chứa nhiều tế bào máu còn nước tiểu chính thức không có",
                    "C. Nước tiểu đầu còn chứa nhiều chất dinh dưỡng và loãng, nước tiểu chính thức đậm đặc và chứa chất thải",
                    "D. Nước tiểu đầu có thể tích nhỏ hơn rất nhiều so với nước tiểu chính thức"
                ],
                "answer": "C",
                "explanation": "Nước tiểu đầu loãng và còn chứa nhiều glucose, amino acid, nước (170-180L); sau khi qua ống thận được tái hấp thụ 99% thì nước tiểu chính thức chỉ còn 1.5-2L chứa đậm đặc ure, acid uric và chất thải."
            },
            {
                "id": "qc-k8-b35-04",
                "question": "Thói quen sinh hoạt nào sau đây là nguyên nhân trực tiếp dẫn đến nguy cơ mắc bệnh sỏi thận?",
                "options": [
                    "A. Ăn nhiều rau xanh và uống đủ 2 lít nước mỗi ngày",
                    "B. Thường xuyên tập luyện thể dục thể thao buổi sáng",
                    "C. Ngủ đủ 8 tiếng mỗi ngày và giữ tinh thần thoải mái",
                    "D. Uống quá ít nước, ăn mặn và thường xuyên nhịn tiểu"
                ],
                "answer": "D",
                "explanation": "Uống ít nước làm nước tiểu bị cô đặc, kết hợp với thói quen ăn mặn và nhịn tiểu khiến các tinh thể muối khoáng (calci oxalate, phosphat) lắng đọng kết tinh thành sỏi thận."
            },
            {
                "id": "qc-k8-b35-05",
                "question": "Ở người trưởng thành khỏe mạnh, thể tích nước tiểu chính thức được đào thải ra ngoài trung bình mỗi ngày khoảng bao nhiêu?",
                "options": [
                    "A. 1,5 – 2 lít",
                    "B. 170 – 180 lít",
                    "C. 0,2 – 0,5 lít",
                    "D. 8 – 10 lít"
                ],
                "answer": "A",
                "explanation": "Sau khi ống thận hấp thụ lại 99% lượng nước từ 170 - 180 lít nước tiểu đầu, lượng nước tiểu chính thức thải ra ngoài chỉ vào khoảng 1,5 đến 2 lít/ngày."
            },
            {
                "id": "qc-k8-b35-06",
                "question": "Cơ quan nào trong hệ bài tiết nước tiểu đóng vai trò lưu trữ nước tiểu tạm thời trước khi thải ra ngoài?",
                "options": [
                    "A. Thận",
                    "B. Bóng đái (bàng quang)",
                    "C. Ống dẫn nước tiểu",
                    "D. Bể thận"
                ],
                "answer": "B",
                "explanation": "Bóng đái (bàng quang) là một túi cơ đàn hồi có chức năng tích trữ nước tiểu tạm thời từ thận dẫn xuống, khi đạt khoảng 200 - 300 ml sẽ kích thích phản xạ đi tiểu."
            }
        ]
    },
    {
        "id": "k8-b36-moi-truong-trong",
        "grade": 8,
        "number": "Bài 36",
        "title": "Điều hòa môi trường trong của cơ thể người",
        "topic": "Sinh học cơ thể người",
        "duration": "2 tiết (90 phút)",
        "order": 360,
        "active": True,
        "origin": "official_curriculum",
        "lesson_version": 5,
        "source_label": "SGK KHTN 8 KNTT – Bài 36 – Trang 152–155",
        "content": "Môi trường trong cơ thể người gồm máu, dịch mô và dịch bạch huyết; khái niệm cân bằng nội môi và vai trò của thận, gan trong việc duy trì ổn định nồng độ các chất và độ pH của cơ thể.",
        "warmup": "Khi chúng ta ăn một bữa ăn rất ngọt hoặc chạy thể thao toát nhiều mồ hôi, tại sao sau đó cơ thể vẫn giữ được nồng độ đường trong máu và lượng nước ổn định? Cơ chế nào giúp bảo vệ cơ thể khỏi những biến động đó?",
        "objectives": [
            "Nêu được các thành phần cấu tạo nên môi trường trong cơ thể (máu, dịch mô, dịch bạch huyết).",
            "Nêu được khái niệm cân bằng môi trường trong (cân bằng nội môi) và ý nghĩa sinh học của nó.",
            "Trình bày được vai trò của gan và thận trong điều hòa nồng độ glucose, nước, muối khoáng và pH máu.",
            "Nêu được ý nghĩa của việc xét nghiệm máu và nước tiểu định kì trong chăm sóc sức khỏe."
        ],
        "sections": [
            {
                "title": "1. Các thành phần của môi trường trong cơ thể",
                "paragraphs": [
                    "Môi trường trong của cơ thể người gồm ba thành phần dịch thể lưu thông và liên hệ mật thiết với nhau: máu, dịch mô (nước mô) và dịch bạch huyết.",
                    "Sự liên hệ giữa các thành phần: Một phần huyết tương của máu thẩm thấu qua thành mao mạch vào các khe gian bào tạo thành dịch mô bao quanh trực tiếp các tế bào. Dịch mô sau khi trao đổi chất với tế bào sẽ thấm vào các mao mạch bạch huyết tạo thành dịch bạch huyết. Dịch bạch huyết lưu thông theo mạch bạch huyết rồi đổ ngược trở lại vào tĩnh mạch máu gần tim.",
                    "Vai trò của môi trường trong: Giúp tế bào thực hiện quá trình trao đổi chất (tiếp nhận O2, chất dinh dưỡng và thải CO2, chất cặn bã) với môi trường ngoài."
                ],
                "bullets": [
                    "Máu: lưu thông trong hệ mạch máu kín.",
                    "Dịch mô: lấp đầy các khe hở giữa các tế bào, tiếp xúc trực tiếp với màng tế bào.",
                    "Dịch bạch huyết: lưu thông trong hệ mạch bạch huyết và hòa nhập lại vào hệ tuần hoàn máu."
                ]
            },
            {
                "title": "2. Khái niệm cân bằng môi trường trong (Cân bằng nội môi)",
                "paragraphs": [
                    "Cân bằng môi trường trong (còn gọi là cân bằng nội môi) là sự duy trì ổn định các điều kiện lí - hóa của môi trường trong cơ thể (như nồng độ các chất hòa tan, nhiệt độ 37°C, áp suất thẩm thấu và độ pH máu từ 7,35 – 7,45).",
                    "Tính ổn định này là ổn định động: các chỉ số có thể dao động nhẹ quanh giá trị chuẩn nhưng nhanh chóng được cơ thể điều hòa đưa về mức bình thường.",
                    "Ý nghĩa: Đảm bảo điều kiện tối ưu cho các tế bào và các enzyme hoạt động bình thường. Nếu môi trường trong bị mất cân bằng kéo dài (ví dụ đường huyết quá cao, nồng độ acid tăng) sẽ gây rối loạn chuyển hóa, hủy hoại tế bào và dẫn đến tử vong."
                ],
                "bullets": [
                    "Nhiệt độ cơ thể người bình thường ổn định ở khoảng 36,5°C - 37,2°C.",
                    "Nồng độ đường glucose trong máu bình thường được duy trì ở mức 3,9 – 6,4 mmol/L (khoảng 0,1%).",
                    "Độ pH của máu dao động trong giới hạn hẹp 7,35 - 7,45."
                ]
            },
            {
                "title": "3. Vai trò của thận và gan trong điều hòa môi trường trong",
                "paragraphs": [
                    "Thận và gan là hai cơ quan chủ chốt tham gia điều hòa tính ổn định của môi trường trong cơ thể.",
                    "Vai trò của thận: Thận điều hòa thể tích nước và nồng độ các ion muối khoáng (Na+, K+, Ca2+) trong máu thông qua quá trình lọc và tái hấp thụ ở ống thận. Khi cơ thể thiếu nước (uống ít nước, toát mồ hôi nhiều), thận tăng cường hấp thụ lại nước làm nước tiểu cô đặc; khi cơ thể thừa nước, thận giảm hấp thụ nước làm nước tiểu loãng hơn. Thận cũng tham gia điều hòa độ pH máu bằng cách bài tiết bớt ion H+ hoặc tái hấp thụ ion HCO3-.",
                    "Vai trò của gan: Gan điều hòa nồng độ glucose trong máu ổn định nhờ sự phối hợp với hai hormone của tuyến tụy là insulin và glucagon. Khi đường huyết tăng (sau bữa ăn), tuyến tụy tiết insulin kích thích gan chuyển glucose thừa thành glycogen dự trữ trong gan và cơ. Khi đường huyết giảm (khi đói, vận động nặng), tuyến tụy tiết glucagon kích thích gan phân giải glycogen thành glucose giải phóng vào máu."
                ],
                "bullets": [
                    "Thận: Điều hòa thể tích nước, áp suất thẩm thấu, nồng độ muối khoáng và pH máu.",
                    "Gan: Điều hòa nồng độ glucose trong máu, chuyển hóa lipid, protein và giải độc các chất độc hại.",
                    "Tuyến tụy tiết Insulin (giúp hạ đường huyết) và Glucagon (giúp tăng đường huyết)."
                ]
            },
            {
                "title": "4. Ý nghĩa của xét nghiệm định kì các chỉ số môi trường trong",
                "paragraphs": [
                    "Việc xét nghiệm máu và xét nghiệm nước tiểu định kì là phương pháp y khoa quan trọng để theo dõi trạng thái cân bằng nội môi của cơ thể.",
                    "Khi các cơ quan trong cơ thể bị tổn thương hoặc rối loạn chức năng, nồng độ các chất trong môi trường trong sẽ biến đổi: chỉ số glucose trong máu cao cảnh báo bệnh đái tháo đường (tiểu đường); chỉ số acid uric cao cảnh báo bệnh gút (gout); nồng độ ure và creatinin tăng cao cảnh báo chức năng lọc của thận bị suy giảm; xuất hiện protein hoặc hồng cầu trong nước tiểu báo hiệu tổn thương cầu thận."
                ],
                "bullets": [
                    "Khám sức khỏe và xét nghiệm máu, nước tiểu định kì 6 tháng/lần.",
                    "Phát hiện sớm các dấu hiệu mất cân bằng nội môi để điều chỉnh chế độ ăn uống, lối sống hoặc điều trị y tế kịp thời."
                ]
            }
        ],
        "terms": [
            {
                "term": "Môi trường trong",
                "definition": "Hệ dịch thể gồm máu, dịch mô và dịch bạch huyết bao bọc xung quanh các tế bào trong cơ thể."
            },
            {
                "term": "Cân bằng nội môi",
                "definition": "Trạng thái duy trì ổn định các điều kiện lí - hóa của môi trường trong cơ thể (nhiệt độ, pH, áp suất thẩm thấu, nồng độ các chất)."
            },
            {
                "term": "Insulin",
                "definition": "Hormone do tuyến tụy tiết ra giúp hạ đường huyết bằng cách kích thích gan chuyển glucose thành glycogen dự trữ."
            },
            {
                "term": "Glucagon",
                "definition": "Hormone do tuyến tụy tiết ra giúp nâng đường huyết bằng cách kích thích gan phân giải glycogen thành glucose đưa vào máu."
            }
        ],
        "summary": [
            "Môi trường trong cơ thể gồm 3 thành phần: máu, dịch mô và dịch bạch huyết.",
            "Cân bằng nội môi là sự duy trì ổn định các chỉ số lí - hóa (nhiệt độ, pH, đường huyết, áp suất thẩm thấu) của môi trường trong.",
            "Gan điều hòa nồng độ glucose trong máu nhờ sự phối hợp của hormone insulin và glucagon.",
            "Thận điều hòa áp suất thẩm thấu, thể tích nước, nồng độ ion muối khoáng và độ pH của máu.",
            "Xét nghiệm máu và nước tiểu định kì giúp phát hiện sớm các rối loạn mất cân bằng nội môi và bệnh lí tiềm ẩn."
        ],
        "quick_check": [
            {
                "id": "qc-k8-b36-01",
                "question": "Môi trường trong của cơ thể người bao gồm những thành phần nào sau đây?",
                "options": [
                    "A. Dịch tiêu hóa, dịch mật và dịch tụy",
                    "B. Máu, dịch mô và dịch bạch huyết",
                    "C. Nước tiểu, mồ hôi và nước mắt",
                    "D. Tế bào chất, dịch nhân và dịch ti thể"
                ],
                "answer": "B",
                "explanation": "Môi trường trong cơ thể người gồm 3 thành phần dịch thể chính liên kết khép kín: máu (trong lòng mạch), dịch mô (bao quanh tế bào) và dịch bạch huyết (trong mạch bạch huyết)."
            },
            {
                "id": "qc-k8-b36-02",
                "question": "Khi nồng độ glucose trong máu tăng cao sau bữa ăn, tuyến tụy sẽ tiết ra hormone nào để kích thích gan chuyển glucose thành glycogen dự trữ?",
                "options": [
                    "A. Insulin",
                    "B. Glucagon",
                    "C. Adrenaline",
                    "D. Thyroxine"
                ],
                "answer": "A",
                "explanation": "Tuyến tụy tiết hormone insulin khi đường huyết tăng cao, kích thích các tế bào gan hấp thu glucose và tổng hợp thành glycogen dự trữ, đưa đường huyết về mức ổn định."
            },
            {
                "id": "qc-k8-b36-03",
                "question": "Cơ quan nào đóng vai trò chủ chốt trong việc điều hòa thể tích nước, nồng độ muối khoáng và pH của máu?",
                "options": [
                    "A. Dạ dày",
                    "B. Thận",
                    "C. Tuyến nước bọt",
                    "D. Phổi"
                ],
                "answer": "B",
                "explanation": "Thận điều hòa lượng nước và áp suất thẩm thấu thông qua tái hấp thụ nước ở ống thận, đồng thời bài tiết các ion thừa (H+, K+) để giữ ổn định độ pH máu."
            },
            {
                "id": "qc-k8-b36-04",
                "question": "Khi xét nghiệm máu, chỉ số nồng độ chất nào sau đây tăng cao bất thường là dấu hiệu cảnh báo bệnh đái tháo đường (tiểu đường)?",
                "options": [
                    "A. Hemoglobin",
                    "B. Cholesterol",
                    "C. Glucose",
                    "D. Canxi"
                ],
                "answer": "C",
                "explanation": "Bệnh đái tháo đường xảy ra khi tuyến tụy thiếu hụt insulin hoặc tế bào kháng insulin khiến nồng độ đường glucose trong máu tăng cao mạn tính."
            },
            {
                "id": "qc-k8-b36-05",
                "question": "Độ pH bình thường của máu người khỏe mạnh được duy trì ổn định trong khoảng giới hạn nào sau đây?",
                "options": [
                    "A. 1,0 – 2,0",
                    "B. 4,5 – 5,5",
                    "C. 7,35 – 7,45",
                    "D. 9,0 – 10,0"
                ],
                "answer": "C",
                "explanation": "Độ pH của máu người bình thường có tính kiềm rất nhẹ và được điều hòa cực kì nghiêm ngặt trong khoảng từ 7,35 đến 7,45."
            },
            {
                "id": "qc-k8-b36-06",
                "question": "Khi cơ thể bị mất nhiều nước do sốt cao hoặc tiêu chảy, thận sẽ có phản ứng điều hòa nào sau đây?",
                "options": [
                    "A. Tăng cường bài tiết nước tiểu thật nhiều và loãng",
                    "B. Tăng cường hấp thụ lại nước ở ống thận làm nước tiểu cô đặc",
                    "C. Ngừng hoàn toàn quá trình lọc máu ở cầu thận",
                    "D. Đào thải toàn bộ muối khoáng ra ngoài cơ thể"
                ],
                "answer": "B",
                "explanation": "Khi mất nước, áp suất thẩm thấu tăng kích thích tuyến yên tiết ADH làm thận tăng cường hấp thụ lại nước ở ống thận nhằm giữ nước cho cơ thể, khiến nước tiểu ít và sẫm màu."
            }
        ]
    },
    {
        "id": "k8-b37-than-kinh-giac-quan",
        "grade": 8,
        "number": "Bài 37",
        "title": "Hệ thần kinh và các giác quan ở người",
        "topic": "Sinh học cơ thể người",
        "duration": "4 tiết (180 phút)",
        "order": 370,
        "active": True,
        "origin": "official_curriculum",
        "lesson_version": 5,
        "source_label": "SGK KHTN 8 KNTT – Bài 37 – Trang 156–162",
        "content": "Hệ thần kinh và các giác quan ở người nghiên cứu cấu tạo hệ thần kinh gồm não bộ, tủy sống và dây thần kinh; phản xạ và cung phản xạ; cấu tạo cơ quan thị giác (mắt), cơ quan thính giác (tai), các tật khúc xạ và biện pháp bảo vệ hệ thần kinh.",
        "warmup": "Khi tay vô tình chạm vào vật nóng, ta lập tức rụt tay lại mà chưa cần kịp suy nghĩ. Phản ứng đó do bộ phận nào điều khiển và diễn ra nhanh như thế nào? Não bộ và các giác quan phối hợp ra sao để giúp ta nhận biết thế giới?",
        "objectives": [
            "Trình bày được cấu tạo và chức năng của hệ thần kinh (bộ phận trung ương gồm não bộ, tủy sống; bộ phận ngoại biên gồm dây thần kinh, hạch thần kinh).",
            "Nêu được khái niệm phản xạ và phân tích được 5 khâu của một cung phản xạ.",
            "Mô tả được cấu tạo của mắt và tai; giải thích được cơ chế nhìn rõ và cơ chế cảm nhận âm thanh.",
            "Phân biệt được tật cận thị và tật viễn thị (nguyên nhân, biểu hiện và cách khắc phục bằng kính thuốc).",
            "Đề xuất được các biện pháp bảo vệ hệ thần kinh, chăm sóc mắt và tai khỏe mạnh."
        ],
        "sections": [
            {
                "title": "1. Cấu tạo và chức năng của hệ thần kinh",
                "paragraphs": [
                    "Hệ thần kinh có chức năng tiếp nhận các kích thích từ môi trường ngoài và môi trường trong, phân tích và điều khiển, điều hòa, phối hợp hoạt động của tất cả các cơ quan trong cơ thể thành một khối thống nhất.",
                    "Về mặt cấu trúc, hệ thần kinh gồm: Bộ phận trung ương (não bộ nằm trong hộp sọ và tủy sống nằm trong ống xương sống) và Bộ phận ngoại biên (12 đôi dây thần kinh não, 31 đôi dây thần kinh tủy và các hạch thần kinh nằm rải rác khắp cơ thể).",
                    "Đơn vị cấu tạo và chức năng cơ bản của hệ thần kinh là nơron (tế bào thần kinh). Mỗi nơron gồm một thân chứa nhân, nhiều sợi nhánh ngắn tiếp nhận xung thần kinh và một sợi trục dài dẫn truyền xung thần kinh đi ra (sợi trục thường có bao myelin bao bọc cách điện)."
                ],
                "bullets": [
                    "Não bộ gồm: đại não (vỏ não là trung tâm thần kinh cao cấp ý thức, tư duy), não trung gian, thân não (trung khu điều hòa hô hấp, tim mạch) và tiểu não (trung khu điều hòa thăng bằng và phối hợp cử động phức tạp).",
                    "Tủy sống: trung khu của các phản xạ không điều kiện cơ bản (như phản xạ rút tay khi chạm nóng, phản xạ đầu gối).",
                    "Nơron có hai đặc tính sinh lí cơ bản: cảm ứng (phát sinh xung thần kinh khi bị kích thích) và dẫn truyền (dẫn truyền xung thần kinh theo một chiều xác định)."
                ]
            },
            {
                "title": "2. Phản xạ và cung phản xạ",
                "paragraphs": [
                    "Mọi hoạt động của hệ thần kinh đều được thực hiện thông qua phản xạ. Phản xạ là phản ứng của cơ thể trả lời các kích thích của môi trường thông qua hệ thần kinh.",
                    "Cung phản xạ là con đường mà xung thần kinh truyền từ cơ quan thụ cảm qua trung ương thần kinh đến cơ quan phản ứng.",
                    "Một cung phản xạ hoàn chỉnh bắt buộc phải có đầy đủ 5 thành phần (5 khâu):",
                    "1. Cơ quan thụ cảm (thụ quan tiếp nhận kích thích, ví dụ thụ quan nhiệt trên da).",
                    "2. Nơron hướng tâm (nơron cảm giác dẫn truyền xung thần kinh từ cơ quan thụ cảm về trung ương thần kinh).",
                    "3. Nơron trung gian (ở trung ương thần kinh não bộ hoặc tủy sống, tiếp nhận và xử lí thông tin).",
                    "4. Nơron li tâm (nơron vận động dẫn truyền xung thần kinh lệnh từ trung ương đến cơ quan phản ứng).",
                    "5. Cơ quan phản ứng (cơ co hoặc tuyến tiết dịch)."
                ],
                "bullets": [
                    "Ví dụ phản xạ tự vệ: Tay chạm vật nóng -> Thụ cảm nhiệt phát xung -> Nơron hướng tâm dẫn về tủy sống -> Nơron trung gian phát lệnh -> Nơron li tâm truyền tới cơ tay -> Cơ tay co lập tức rút tay lại."
                ]
            },
            {
                "title": "3. Cơ quan thị giác (Mắt) và các tật khúc xạ",
                "paragraphs": [
                    "Mắt là cơ quan thu nhận kích thích ánh sáng giúp ta nhìn thấy hình dạng, màu sắc và chuyển động của các vật thể.",
                    "Cấu tạo cầu mắt: Từ ngoài vào trong gồm 3 lớp màng: màng cứng (phía trước trong suốt gọi là màng giác - giác mạc), màng mạch (chứa nhiều mao mạch nuôi dưỡng và các tế bào sắc tố đen ngăn ánh sáng phản chiếu) và màng lưới (võng mạc - chứa hàng triệu tế bào thụ cảm thị giác gồm tế bào que cảm nhận ánh sáng yếu và tế bào nón cảm nhận màu sắc, ánh sáng mạnh).",
                    "Hệ thống môi trường trong suốt gồm màng giác, thủy dịch, thể thủy tinh (thấu kính hội tụ sinh học có thể thay đổi độ cong nhờ cơ thể mi để điều tiết ảnh rõ nét) và dịch thủy tinh.",
                    "Các tật khúc xạ học đường thường gặp:",
                    "- Tật cận thị: Mắt chỉ nhìn rõ vật ở gần, nhìn xa bị mờ. Nguyên nhân do cầu mắt quá dài hoặc thể thủy tinh quá phồng (do đọc sách quá gần, thiếu ánh sáng). Hậu quả: Ảnh của vật ở xa rơi ở PHÍA TRƯỚC màng lưới. Cách khắc phục: Đeo kính cận là THẤU KÍNH PHÂN KÌ để kéo ảnh lùi về đúng màng lưới.",
                    "- Tật viễn thị: Mắt nhìn rõ vật ở xa nhưng nhìn gần bị mờ. Nguyên nhân do cầu mắt quá ngắn hoặc thể thủy tinh bị xẹp/lão hóa. Hậu quả: Ảnh của vật rơi ở PHÍA SAU màng lưới. Cách khắc phục: Đeo kính viễn là THẤU KÍNH HỘI TỤ để kéo ảnh về phía trước trên màng lưới."
                ],
                "bullets": [
                    "Cận thị: Ảnh rơi TRƯỚC võng mạc -> Đeo thấu kính PHÂN KÌ.",
                    "Viễn thị: Ảnh rơi SAU võng mạc -> Đeo thấu kính HỘI TỤ.",
                    "Loạn thị: Giác mạc cong không đều -> Ảnh bị nhòe méo -> Đeo kính trụ."
                ]
            },
            {
                "title": "4. Cơ quan thính giác (Tai) và cảm thụ âm thanh",
                "paragraphs": [
                    "Tai là cơ quan thụ cảm thính giác có chức năng thu nhận sóng âm thanh và cảm nhận sự thăng bằng của cơ thể.",
                    "Cấu tạo tai gồm ba phần: Tai ngoài (vành tai hứng sóng âm, ống tai ngoài dẫn sóng âm và màng nhĩ chắn ở cuối); Tai giữa (chứa chuỗi 3 xương tai nhỏ: xương búa, xương đe, xương bàn đạp và vòi nhĩ nối với hầu giúp cân bằng áp suất); Tai trong (gồm ốc tai chứa dịch và cơ quan Corti với các tế bào thụ cảm thính giác, cùng hệ thống tiền đình và các ống bán khuyên giúp cảm nhận thăng bằng).",
                    "Cơ chế cảm thụ âm thanh: Sóng âm thanh -> Vành tai hứng -> Ống tai truyền vào làm rung màng nhĩ -> Rung chuỗi xương tai (khuếch đại âm) -> Rung dịch ốc tai -> Kích thích tế bào thụ cảm thính giác ở cơ quan Corti phát xung thần kinh -> Dây thần kinh thính giác truyền lên vùng thính giác ở thùy thái dương của vỏ não cho ta cảm nhận âm thanh."
                ],
                "bullets": [
                    "Tai ngoài: Vành tai, ống tai ngoài, màng nhĩ.",
                    "Tai giữa: Chuỗi xương tai (búa, đe, bàn đạp), vòi nhĩ.",
                    "Tai trong: Ốc tai (cơ quan Corti thụ cảm âm thanh), tiền đình và ống bán khuyên (giữ thăng bằng)."
                ]
            },
            {
                "title": "5. Vệ sinh hệ thần kinh và bảo vệ các giác quan",
                "paragraphs": [
                    "Hệ thần kinh làm việc liên tục điều khiển cơ thể nên rất dễ bị suy nhược và tổn thương nếu bị căng thẳng thần kinh kéo dài hoặc thiếu ngủ.",
                    "Giấc ngủ có ý nghĩa sống còn: Trong giấc ngủ, các tế bào não được nghỉ ngơi, phục hồi năng lượng và đào thải các độc tố tích tụ trong ngày. Học sinh THCS cần ngủ đủ 8 – 9 tiếng mỗi ngày."
                ],
                "bullets": [
                    "Đảm bảo giấc ngủ đủ và đúng giờ, phòng ngủ thông thoáng, yên tĩnh.",
                    "Học tập và giải trí hợp lí, tránh căng thẳng thần kinh; ngồi học đúng tư thế, giữ khoảng cách mắt từ 25 - 30 cm với sách vở.",
                    "Đảm bảo đủ ánh sáng khi đọc sách; không nhìn màn hình điện thoại, máy tính quá 2 giờ liên tục.",
                    "Vệ sinh tai mũi họng thường xuyên, không dùng vật cứng nhọn ngoáy tai tránh thủng màng nhĩ; tránh tiếp xúc với tiếng ồn quá lớn.",
                    "Tuyệt đối nói không với chất kích thích và chất gây nghiện (rượu bia, thuốc lá, ma túy, bóng cười)."
                ]
            }
        ],
        "terms": [
            {
                "term": "Nơron",
                "definition": "Đơn vị cấu tạo và chức năng cơ bản của hệ thần kinh, có đặc tính cảm ứng và dẫn truyền xung thần kinh."
            },
            {
                "term": "Phản xạ",
                "definition": "Phản ứng của cơ thể trả lời các kích thích của môi trường thông qua sự điều khiển của hệ thần kinh."
            },
            {
                "term": "Cung phản xạ",
                "definition": "Con đường dẫn truyền xung thần kinh khép kín gồm 5 khâu: cơ quan thụ cảm, nơron hướng tâm, nơron trung gian, nơron li tâm và cơ quan phản ứng."
            },
            {
                "term": "Cận thị",
                "definition": "Tật khúc xạ của mắt khiến ảnh của vật ở xa rơi ở phía trước màng lưới, cần đeo thấu kính phân kì để khắc phục."
            },
            {
                "term": "Viễn thị",
                "definition": "Tật khúc xạ của mắt khiến ảnh của vật ở gần rơi ở phía sau màng lưới, cần đeo thấu kính hội tụ để khắc phục."
            }
        ],
        "summary": [
            "Hệ thần kinh gồm bộ phận trung ương (não bộ, tủy sống) và bộ phận ngoại biên (dây thần kinh, hạch thần kinh).",
            "Mọi hoạt động thần kinh đều thông qua phản xạ; một cung phản xạ hoàn chỉnh gồm đủ 5 khâu liên hoàn.",
            "Cầu mắt có màng lưới chứa tế bào que và tế bào nón; thể thủy tinh điều tiết để hội tụ ảnh trên màng lưới.",
            "Cận thị (ảnh rơi trước màng lưới) đeo thấu kính phân kì; Viễn thị (ảnh rơi sau màng lưới) đeo thấu kính hội tụ.",
            "Tai gồm tai ngoài, tai giữa và tai trong (ốc tai chứa tế bào thụ cảm thính giác).",
            "Cần ngủ đủ 8 tiếng mỗi ngày, ngồi học đủ ánh sáng, đúng tư thế và tránh các chất kích thích để bảo vệ hệ thần kinh."
        ],
        "quick_check": [
            {
                "id": "qc-k8-b37-01",
                "question": "Một cung phản xạ hoàn chỉnh bắt buộc phải bao gồm đầy đủ bao nhiêu thành phần (khâu)?",
                "options": [
                    "A. 3 thành phần",
                    "B. 4 thành phần",
                    "C. 5 thành phần",
                    "D. 6 thành phần"
                ],
                "answer": "C",
                "explanation": "Một cung phản xạ gồm đủ 5 thành phần: 1. Cơ quan thụ cảm, 2. Nơron hướng tâm, 3. Nơron trung gian (trung ương thần kinh), 4. Nơron li tâm, 5. Cơ quan phản ứng."
            },
            {
                "id": "qc-k8-b37-02",
                "question": "Học sinh bị tật cận thị khi nhìn vật ở xa thì ảnh của vật sẽ hội tụ ở vị trí nào so với màng lưới (võng mạc)?",
                "options": [
                    "A. Rơi ở phía trước màng lưới",
                    "B. Rơi đúng trên màng lưới",
                    "C. Rơi ở phía sau màng lưới",
                    "D. Không hội tụ thành ảnh"
                ],
                "answer": "A",
                "explanation": "Ở mắt cận thị, do cầu mắt quá dài hoặc thể thủy tinh quá phồng nên chùm sáng hội tụ quá sớm, ảnh của vật ở xa rơi ở phía trước màng lưới khiến mắt nhìn mờ."
            },
            {
                "id": "qc-k8-b37-03",
                "question": "Để khắc phục tật cận thị học đường, người bệnh cần đeo loại kính thuốc nào sau đây?",
                "options": [
                    "A. Kính có thấu kính hội tụ",
                    "B. Kính râm chống tia cực tím",
                    "C. Kính có thấu kính phân kì",
                    "D. Kính 2 tròng đổi màu"
                ],
                "answer": "C",
                "explanation": "Thấu kính phân kì có tác dụng làm chùm tia sáng loe rộng ra trước khi vào mắt, giúp đưa ảnh từ phía trước lùi về đúng trên màng lưới của mắt."
            },
            {
                "id": "qc-k8-b37-04",
                "question": "Bộ phận nào của tai chứa cơ quan Corti với các tế bào thụ cảm thính giác trực tiếp tiếp nhận dao động âm thanh?",
                "options": [
                    "A. Ốc tai (ở tai trong)",
                    "B. Chuỗi xương tai (ở tai giữa)",
                    "C. Màng nhĩ",
                    "D. Vành tai (ở tai ngoài)"
                ],
                "answer": "A",
                "explanation": "Ốc tai nằm ở tai trong chứa dịch ốc tai và cơ quan Corti với các tế bào có lông thụ cảm thính giác, khi dịch dao động sẽ kích thích tế bào phát xung thần kinh lên não."
            },
            {
                "id": "qc-k8-b37-05",
                "question": "Đơn vị cấu tạo và chức năng cơ bản của hệ thần kinh là gì?",
                "options": [
                    "A. Tế bào cơ vân",
                    "B. Phế nang",
                    "C. Nephron",
                    "D. Nơron (tế bào thần kinh)"
                ],
                "answer": "D",
                "explanation": "Nơron (tế bào thần kinh) là đơn vị cấu tạo và chức năng của hệ thần kinh, có thân, sợi nhánh và sợi trục đảm nhiệm chức năng cảm ứng và dẫn truyền xung thần kinh."
            },
            {
                "id": "qc-k8-b37-06",
                "question": "Thời gian ngủ nghỉ tối ưu mỗi ngày của học sinh lứa tuổi THCS để bảo vệ hệ thần kinh và phục hồi trí não là bao nhiêu?",
                "options": [
                    "A. Khoảng 4 – 5 tiếng",
                    "B. Khoảng 8 – 9 tiếng",
                    "C. Khoảng 12 – 14 tiếng",
                    "D. Càng ít càng tốt để dành thời gian học"
                ],
                "answer": "B",
                "explanation": "Lứa tuổi THCS đang trong giai đoạn phát triển thể chất và hoạt động trí não cao, cần ngủ đủ 8 – 9 tiếng mỗi ngày để các tế bào thần kinh đại não được phục hồi hoàn toàn."
            }
        ]
    },
    {
        "id": "k9-tan-sac-anh-sang",
        "grade": 9,
        "number": "Bài 7",
        "title": "Lăng kính và tán sắc ánh sáng",
        "topic": "Lăng kính; tán sắc ánh sáng trắng; ánh sáng đơn sắc; màu sắc của vật",
        "duration": "40–45 phút",
        "objectives": [
            "Mô tả được cấu tạo cơ bản của lăng kính.",
            "Mô tả và giải thích được hiện tượng tán sắc ánh sáng trắng.",
            "Phân biệt được ánh sáng trắng và ánh sáng đơn sắc.",
            "Vận dụng kiến thức để giải thích cầu vồng và màu sắc của vật."
        ],
        "content": "Lăng kính là khối trong suốt có hai mặt phẳng không song song. Khi ánh sáng trắng đi qua lăng kính, các thành phần màu bị lệch khác nhau và tách thành dải màu liên tục.",
        "source_label": "SGK KHTN 9 KNTT · Bài 7 · Trang 34–36",
        "warmup": {
            "question": "Vì sao một chùm ánh sáng trắng qua lăng kính lại tạo thành nhiều màu?",
            "hint": "Các ánh sáng màu thành phần bị lệch với mức độ khác nhau."
        },
        "sections": [
            {
                "title": "1. Lăng kính",
                "paragraphs": [
                    "Lăng kính là một khối chất trong suốt, đồng chất, thường có dạng lăng trụ tam giác. Hai mặt bên dùng cho ánh sáng truyền qua không song song với nhau.",
                    "Tia sáng đổi hướng khi truyền qua các mặt phân cách giữa không khí và lăng kính do hiện tượng khúc xạ."
                ]
            },
            {
                "title": "2. Tán sắc ánh sáng trắng",
                "paragraphs": [
                    "Khi chùm ánh sáng trắng hẹp đi qua lăng kính, nó tách thành dải nhiều màu liên tục, thường quan sát theo thứ tự đỏ, da cam, vàng, lục, lam, chàm, tím.",
                    "Hiện tượng ánh sáng trắng bị phân tách thành các ánh sáng màu thành phần được gọi là tán sắc ánh sáng."
                ],
                "note": "Trong điều kiện thí nghiệm điển hình, tia đỏ lệch ít hơn và tia tím lệch nhiều hơn."
            },
            {
                "title": "3. Ánh sáng đơn sắc và màu sắc của vật",
                "paragraphs": [
                    "Ánh sáng đơn sắc có một màu xác định và không bị tách thành nhiều màu khi truyền qua lăng kính. Ánh sáng trắng là hỗn hợp của nhiều ánh sáng màu.",
                    "Màu ta nhìn thấy phụ thuộc vào ánh sáng chiếu tới và khả năng hấp thụ, phản xạ ánh sáng của vật."
                ],
                "example": "Cầu vồng hình thành khi ánh sáng Mặt Trời bị khúc xạ, tán sắc và phản xạ trong các giọt nước nhỏ."
            }
        ],
        "diagram": {
            "title": "Tán sắc qua lăng kính",
            "nodes": [
                "Ánh sáng trắng",
                "Lăng kính",
                "Đỏ → Da cam → Vàng → Lục → Lam → Chàm → Tím"
            ]
        },
        "terms": [
            {
                "term": "Lăng kính",
                "definition": "Khối trong suốt có hai mặt khúc xạ không song song."
            },
            {
                "term": "Tán sắc",
                "definition": "Sự phân tách ánh sáng trắng thành các ánh sáng màu thành phần."
            },
            {
                "term": "Ánh sáng trắng",
                "definition": "Hỗn hợp của nhiều ánh sáng màu."
            },
            {
                "term": "Ánh sáng đơn sắc",
                "definition": "Ánh sáng có một màu xác định và không bị tách màu qua lăng kính."
            }
        ],
        "summary": [
            "Lăng kính làm tia sáng đổi hướng do khúc xạ.",
            "Ánh sáng trắng qua lăng kính bị tách thành dải nhiều màu.",
            "Các màu lệch khác nhau; đỏ lệch ít hơn tím trong thí nghiệm điển hình.",
            "Màu sắc quan sát được phụ thuộc ánh sáng chiếu tới và ánh sáng vật phản xạ."
        ],
        "quick_check": [
            {
                "question": "Hiện tượng tán sắc là gì?",
                "options": [
                    "Ánh sáng bị phản xạ hoàn toàn",
                    "Ánh sáng trắng tách thành nhiều màu",
                    "Âm thanh đổi tần số",
                    "Vật phát nhiệt"
                ],
                "answer_index": 1,
                "explanation": "Tán sắc là sự phân tách ánh sáng trắng thành các ánh sáng màu thành phần."
            },
            {
                "question": "Trong dải màu qua lăng kính, màu nào thường lệch ít hơn?",
                "options": [
                    "Đỏ",
                    "Tím",
                    "Chàm",
                    "Lam"
                ],
                "answer_index": 0,
                "explanation": "Trong thí nghiệm điển hình, tia đỏ lệch ít nhất và tia tím lệch nhiều nhất."
            },
            {
                "question": "Ánh sáng đơn sắc qua lăng kính sẽ thế nào?",
                "options": [
                    "Tách thành bảy màu",
                    "Không truyền qua",
                    "Bị lệch nhưng không tách thành nhiều màu",
                    "Luôn phản xạ trở lại"
                ],
                "answer_index": 2,
                "explanation": "Ánh sáng đơn sắc có một màu nên không bị phân tách thành dải nhiều màu."
            }
        ],
        "order": 70,
        "active": True,
        "origin": "system",
        "lesson_version": 4
    },
    {
        "id": "k9-bai-43-nguyen-phan-va-giam-phan",
        "grade": 9,
        "number": "Bài 43",
        "title": "Nguyên phân và giảm phân",
        "topic": "Cơ chế, diễn biến các kì, ý nghĩa và ứng dụng của nguyên phân và giảm phân trong di truyền học",
        "duration": "90 phút (2 tiết)",
        "order": 430,
        "active": True,
        "origin": "system",
        "lesson_version": 4,
        "objectives": [
            "Nêu được khái niệm nguyên phân và giảm phân; trình bày được diễn biến cơ bản của các kì trong nguyên phân và giảm phân.",
            "Phân biệt được nguyên phân và giảm phân về loại tế bào, số lần phân chia, số lượng và bộ NST trong các tế bào con.",
            "Nêu được ý nghĩa của nguyên phân, giảm phân và mối quan hệ giữa nguyên phân, giảm phân, thụ tinh trong việc duy trì bộ NST đặc trưng của loài.",
            "Giải thích được nguyên phân là cơ sở của sinh sản vô tính và giảm phân tạo giao tử cho sinh sản hữu tính.",
            "Nêu được một số ứng dụng của nguyên phân và giảm phân trong thực tiễn chọn giống và nhân giống vô tính."
        ],
        "warmup": {
            "title": "Khởi động: Kì diệu của sự phân chia tế bào",
            "question": "Từ một hợp tử ban đầu vô cùng nhỏ bé, làm thế nào có thể phát triển thành một cơ thể đa bào hoàn chỉnh gồm hàng tỉ tế bào? Quá trình nào đã tạo ra các giao tử (tinh trùng, trứng) để duy trì nòi giống qua các thế hệ?",
            "context": "Mọi sinh vật đa bào đều bắt đầu từ một tế bào đơn lẻ (hợp tử). Nhờ quá trình nguyên phân liên tiếp kết hợp với sự biệt hóa tế bào mà cơ thể lớn lên. Đồng thời, quá trình giảm phân tạo ra các giao tử đơn bội để chuẩn bị cho sự thụ tinh.",
            "hint": "Nguyên phân tạo ra các tế bào sinh dưỡng giống hệt tế bào mẹ giúp cơ thể lớn lên; giảm phân tạo ra các giao tử mang bộ NST giảm một nửa giúp duy trì bộ NST qua các thế hệ sinh sản hữu tính."
        },
        "sections": [
            {
                "title": "1. Khái niệm và diễn biến của quá trình nguyên phân",
                "paragraphs": [
                    "Nguyên phân (mitosis) là hình thức phân chia của tế bào sinh dưỡng và tế bào sinh dục sơ khai. Trước khi bước vào phân bào, ở kì trung gian, các nhiễm sắc thể (NST) nhân đôi tạo thành NST kép gồm hai nhiễm sắc tử chị em (chromatid) đính với nhau ở tâm động.",
                    "Quá trình phân chia nhân diễn ra qua 4 kì liên tiếp: Kì đầu (các NST kép bắt đầu co xoắn, màng nhân và nhân con tiêu biến, thoi phân bào xuất hiện); Kì giữa (các NST kép co xoắn cực đại và tập trung thành một hàng trên mặt phẳng xích đạo của thoi phân bào); Kì sau (hai chromatid của từng NST kép tách nhau ở tâm động thành 2 NST đơn và phân li đồng đều về hai cực tế bào nhờ sự co rút của sợi tơ phân bào); Kì cuối (các NST đơn dãn xoắn, màng nhân và nhân con xuất hiện lại, phân chia tế bào chất hoàn tất).",
                    "Kết quả: Từ một tế bào mẹ (2n) qua một lần nguyên phân tạo ra hai tế bào con có bộ NST giống nhau và giống hệt tế bào mẹ (2n)."
                ],
                "bullets": [
                    "Nơi xảy ra: Tế bào sinh dưỡng và tế bào sinh dục sơ khai.",
                    "Nhân đôi NST: 1 lần ở kì trung gian.",
                    "Số lần phân bào: 1 lần (qua 4 kì: đầu, giữa, sau, cuối).",
                    "Đặc điểm kì giữa: NST co xoắn cực đại, xếp thành 1 hàng ở mặt phẳng xích đạo.",
                    "Đặc điểm kì sau: Các chromatid tách nhau ở tâm động thành NST đơn di chuyển về 2 cực.",
                    "Kết quả: 1 tế bào mẹ (2n) -> 2 tế bào con (2n)."
                ],
                "example": "Khi hạt ngô nảy mầm, các tế bào phôi nguyên phân liên tục làm rễ và chồi vươn dài; các tế bào da người liên tục nguyên phân thay thế lớp biểu bì bong tróc.",
                "note": "Ở kì giữa, NST co xoắn cực đại có hình thái và kích thước rõ rệt nhất, là thời điểm thuận lợi nhất để quan sát và đếm số lượng NST dưới kính hiển vi."
            },
            {
                "title": "2. Ý nghĩa của quá trình nguyên phân",
                "paragraphs": [
                    "Đối với cơ thể đa bào: Nguyên phân làm tăng số lượng tế bào, giúp cơ thể sinh trưởng và phát triển từ hợp tử thành cơ thể trưởng thành. Đồng thời giúp tái tạo các mô, cơ quan bị tổn thương (như liền sẹo vết thương, mọc lại đuôi thằn lằn) và thay thế các tế bào già chết đi.",
                    "Đối với sinh vật sinh sản vô tính: Nguyên phân là phương thức sinh sản tạo ra các cá thể con có kiểu gen hoàn toàn giống với cá thể mẹ.",
                    "Trong thực tiễn nông nghiệp: Nguyên phân là cơ sở khoa học của các phương pháp nhân giống sinh dưỡng như giâm cành, chiết cành, ghép cành và phương pháp nuôi cấy mô tế bào in vitro để nhân nhanh các giống cây trồng quý hiếm, sạch bệnh."
                ],
                "bullets": [
                    "Giúp cơ thể lớn lên và tái sinh các phần mô bị tổn thương.",
                    "Đảm bảo sự truyền đạt ổn định bộ NST của loài qua các thế hệ tế bào trong cơ thể.",
                    "Là cơ sở của sinh sản vô tính ở sinh vật nhân thực.",
                    "Ứng dụng nhân giống sinh dưỡng: giâm, chiết, ghép cành và nuôi cấy mô."
                ],
                "example": "Từ một mẩu mô lá hoặc đỉnh sinh trưởng của cây lan gấm, qua kĩ thuật nuôi cấy mô tế bào (dựa trên nguyên phân), có thể tạo ra hàng triệu cây lan con giống hệt cây mẹ.",
                "note": "Cần phân biệt: Nguyên phân diễn ra ở sinh vật nhân thực (có thoi phân bào), còn vi khuẩn (nhân sơ) phân chia bằng hình thức trực phân."
            },
            {
                "title": "3. Khái niệm và diễn biến của quá trình giảm phân",
                "paragraphs": [
                    "Giảm phân (meiosis) là hình thức phân chia tế bào đặc biệt diễn ra ở các tế bào sinh dục chín trong thời kì phát sinh giao tử. Khác với nguyên phân, giảm phân gồm một lần nhân đôi NST nhưng trải qua hai lần phân chia liên tiếp (Giảm phân I và Giảm phân II).",
                    "Giảm phân I (Phân bào giảm nhiễm): Ở kì đầu I diễn ra sự tiếp hợp và có thể trao đổi đoạn (trao đổi chéo) giữa hai chromatid khác nguồn trong cặp NST tương đồng, tạo ra biến dị tổ hợp. Ở kì giữa I, các cặp NST kép tương đồng xếp thành hai hàng trên mặt phẳng xích đạo. Ở kì sau I, mỗi NST kép trong cặp tương đồng phân li độc lập về một cực tế bào. Kết thúc kì cuối I, tạo 2 tế bào con mang bộ NST kép giảm đi một nửa (n kép).",
                    "Giảm phân II (Phân bào nguyên nhiễm): Diễn ra tương tự nguyên phân nhưng không có nhân đôi NST trước đó. Ở kì sau II, hai chromatid của mỗi NST kép tách nhau ở tâm động thành 2 NST đơn phân li về hai cực. Kết thúc kì cuối II, tạo ra các tế bào con mang bộ NST đơn bội (n).",
                    "Kết quả: Từ một tế bào mẹ (2n) qua giảm phân tạo ra bốn tế bào con có bộ NST giảm đi một nửa (n), sau đó phát triển thành các giao tử (tinh trùng ở cá thể đực hoặc trứng ở cá thể cái)."
                ],
                "bullets": [
                    "Nơi xảy ra: Tế bào sinh dục chín.",
                    "Gồm 2 lần phân chia liên tiếp nhưng NST chỉ nhân đôi 1 lần ở kì trung gian trước GP I.",
                    "Kì đầu I: Tiếp hợp và có thể xảy ra trao đổi chéo giữa các NST tương đồng.",
                    "Kì giữa I: Các cặp NST kép xếp thành 2 hàng trên mặt phẳng xích đạo.",
                    "Kì sau I: Các NST kép trong cặp tương đồng phân li độc lập về 2 cực.",
                    "Kết quả: 1 tế bào mẹ (2n) -> 4 tế bào con có bộ NST đơn bội (n)."
                ],
                "example": "Ở người, tế bào sinh dục chín có 2n = 46 NST, qua giảm phân tạo ra tinh trùng hoặc tế bào trứng chỉ mang n = 23 NST.",
                "note": "Hiện tượng tiếp hợp trao đổi chéo ở kì đầu I và phân li độc lập ở kì sau I là hai cơ chế then chốt tạo nên sự đa dạng phong phú của các giao tử và biến dị tổ hợp."
            },
            {
                "title": "4. So sánh nguyên phân và giảm phân",
                "paragraphs": [
                    "Nguyên phân và giảm phân đều là các hình thức phân bào có tơ ở sinh vật nhân thực, đều có sự nhân đôi NST một lần ở kì trung gian và đều trải qua các kì phân chia nhân: kì đầu, kì giữa, kì sau, kì cuối.",
                    "Tuy nhiên, hai quá trình có các điểm khác biệt bản chất: Nguyên phân chỉ có 1 lần phân chia, diễn ra ở tế bào sinh dưỡng/sinh dục sơ khai, giữ nguyên bộ NST (2n -> 2n), tạo 2 tế bào con giống hệt mẹ. Giảm phân có 2 lần phân chia liên tiếp, diễn ra ở tế bào sinh dục chín, giảm bộ NST đi một nửa (2n -> n), tạo 4 tế bào con mang vật chất di truyền biến dị phong phú."
                ],
                "bullets": [
                    "Giống nhau: Đều nhân đôi NST 1 lần; đều có thoi phân bào và trải qua 4 kì phân chia.",
                    "Số lần phân bào: Nguyên phân 1 lần; Giảm phân 2 lần liên tiếp.",
                    "Xếp hàng ở kì giữa: Nguyên phân xếp 1 hàng; Giảm phân I xếp 2 hàng.",
                    "Phân li ở kì sau: Kì sau nguyên phân tách chromatid; Kì sau I giảm phân phân li NST kép tương đồng.",
                    "Kết quả số lượng tế bào: Nguyên phân tạo 2 tế bào con; Giảm phân tạo 4 tế bào con.",
                    "Bộ NST tế bào con: Nguyên phân giữ nguyên (2n); Giảm phân giảm một nửa (n)."
                ],
                "example": "Từ 1 tế bào ruồi giấm 2n = 8: qua nguyên phân tạo 2 tế bào con 2n = 8; qua giảm phân tạo 4 giao tử n = 4.",
                "note": "Giảm phân II bản chất là một lần nguyên phân của tế bào có bộ NST đơn bội kép (n kép -> n đơn)."
            },
            {
                "title": "5. Mối quan hệ giữa nguyên phân, giảm phân, thụ tinh và ứng dụng thực tiễn",
                "paragraphs": [
                    "Trong tự nhiên, ở các loài sinh vật sinh sản hữu tính, sự kết hợp của ba quá trình nguyên phân, giảm phân và thụ tinh có vai trò đặc biệt quan trọng: Giảm phân tạo ra các giao tử đơn bội (n); Thụ tinh kết hợp giao tử đực (n) và cái (n) phục hồi bộ NST lưỡng bội (2n) ở hợp tử; Nguyên phân giúp hợp tử phát triển thành cơ thể mới. Nhờ đó bộ NST đặc trưng của loài được duy trì ổn định qua các thế hệ.",
                    "Đồng thời, giảm phân kết hợp với thụ tinh tạo ra vô số biến dị tổ hợp, cung cấp nguồn nguyên liệu phong phú cho chọn giống và tiến hóa.",
                    "Ứng dụng: Con người vận dụng nguyên phân trong giâm, chiết, ghép, nuôi cấy mô tế bào để nhân giống cây trồng nhanh chóng, giữ nguyên đặc tính tốt của cây mẹ; vận dụng giảm phân và thụ tinh trong lai hữu tính để tạo các giống cây trồng, vật nuôi có năng suất cao, phẩm chất tốt."
                ],
                "bullets": [
                    "Sự phối hợp 3 quá trình duy trì bộ NST 2n ổn định qua các thế hệ sinh vật.",
                    "Biến dị tổ hợp từ giảm phân và thụ tinh là nền tảng cho công tác lai tạo giống.",
                    "Ứng dụng nguyên phân: nhân giống vô tính (giâm, chiết, ghép, vi nhân giống invitro).",
                    "Ứng dụng giảm phân: lai giống hữu tính, chọn lọc các tổ hợp gen ưu tú."
                ],
                "example": "Nhờ nuôi cấy mô (nguyên phân), các vườn ươm có thể sản xuất đồng loạt hàng vạn cây giống chuối cấy mô sạch bệnh, sinh trưởng đồng đều.",
                "note": "Bảo vệ môi trường và hạn chế tác nhân đột biến (hóa chất, phóng xạ) để tránh rối loạn quá trình phân bào nguyên phân và giảm phân."
            }
        ],
        "diagram": {
            "title": "Sơ đồ quá trình Nguyên phân và Giảm phân",
            "nodes": [
                "Tế bào mẹ (2n)",
                "Kì trung gian (NST nhân đôi thành NST kép)",
                "Nguyên phân (1 lần phân bào) -> 2 tế bào con (2n)",
                "Giảm phân (2 lần phân bào) -> 4 giao tử (n)",
                "Thụ tinh (n + n) -> Hợp tử (2n) duy trì ổn định bộ NST"
            ]
        },
        "terms": [
            {
                "term": "Nguyên phân (Mitosis)",
                "definition": "Hình thức phân chia tế bào sinh dưỡng và sinh dục sơ khai, qua 1 lần nhân đôi và 1 lần phân chia tạo ra 2 tế bào con có bộ NST (2n) giống nhau và giống hệt tế bào mẹ."
            },
            {
                "term": "Giảm phân (Meiosis)",
                "definition": "Hình thức phân chia tế bào sinh dục chín gồm 1 lần nhân đôi và 2 lần phân bào liên tiếp, tạo ra 4 tế bào con mang bộ NST đơn bội (n) giảm một nửa so với tế bào mẹ."
            },
            {
                "term": "Kì giữa (Metaphase)",
                "definition": "Kì mà các nhiễm sắc thể co xoắn cực đại có hình thái rõ nhất, xếp thành 1 hàng (nguyên phân) hoặc 2 hàng (giảm phân I) trên mặt phẳng xích đạo của thoi phân bào."
            },
            {
                "term": "Kì sau (Anaphase)",
                "definition": "Kì phân li: Trong nguyên phân các chromatid tách nhau ở tâm động thành NST đơn đi về 2 cực; trong giảm phân I các NST kép trong cặp tương đồng phân li độc lập về 2 cực."
            },
            {
                "term": "Giao tử (Gamete)",
                "definition": "Tế bào sinh dục mang bộ NST đơn bội (n) tạo ra từ giảm phân, gồm tinh trùng ở con đực và trứng ở con cái, có khả năng thụ tinh tạo hợp tử."
            },
            {
                "term": "Biến dị tổ hợp",
                "definition": "Sự xuất hiện các kiểu hình mới ở đời con do sự tái tổ hợp vật chất di truyền của bố mẹ thông qua trao đổi chéo ở giảm phân I và tổ hợp tự do khi thụ tinh."
            }
        ],
        "summary": [
            "Nguyên phân gồm 1 lần nhân đôi NST và 1 lần phân bào, từ 1 tế bào mẹ (2n) tạo ra 2 tế bào con có bộ NST (2n) giống hệt nhau và giống tế bào mẹ.",
            "Nguyên phân giúp cơ thể lớn lên, thay thế tế bào tổn thương và là cơ sở của các phương pháp nhân giống vô tính (giâm, chiết, ghép, nuôi cấy mô).",
            "Giảm phân diễn ra ở tế bào sinh dục chín, gồm 1 lần nhân đôi NST và 2 lần phân chia liên tiếp, từ 1 tế bào mẹ (2n) tạo ra 4 tế bào con mang bộ NST đơn bội (n).",
            "Sự tiếp hợp trao đổi chéo ở kì đầu I và phân li độc lập ở kì sau I trong giảm phân tạo ra nguồn biến dị tổ hợp phong phú cho tiến hóa và chọn giống.",
            "Sự phối hợp nguyên phân, giảm phân và thụ tinh giúp duy trì ổn định bộ NST lưỡng bội (2n) đặc trưng của loài sinh sản hữu tính qua các thế hệ."
        ],
        "quick_check": [
            {
                "question": "Kết quả của quá trình nguyên phân từ một tế bào mẹ (2n) qua một lần phân bào là tạo ra",
                "options": [
                    "2 tế bào con có bộ NST lưỡng bội (2n) giống hệt tế bào mẹ",
                    "4 tế bào con có bộ NST đơn bội (n)",
                    "2 tế bào con có bộ NST đơn bội (n)",
                    "4 tế bào con có bộ NST lưỡng bội (2n)"
                ],
                "answer_index": 0,
                "explanation": "Qua 1 lần nguyên phân, từ 1 tế bào mẹ (2n) tạo ra 2 tế bào con có bộ NST lưỡng bội (2n) giống nhau và giống hệt tế bào mẹ."
            },
            {
                "question": "Ở kì nào của quá trình nguyên phân, các nhiễm sắc thể kép co xoắn cực đại và tập trung thành một hàng trên mặt phẳng xích đạo của thoi phân bào?",
                "options": [
                    "Kì đầu",
                    "Kì giữa",
                    "Kì sau",
                    "Kì cuối"
                ],
                "answer_index": 1,
                "explanation": "Ở kì giữa của nguyên phân, các NST kép co xoắn cực đại và xếp thành một hàng trên mặt phẳng xích đạo của thoi vô sắc."
            },
            {
                "question": "Trong quá trình giảm phân, các nhiễm sắc thể nhân đôi bao nhiêu lần và tế bào trải qua bao nhiêu lần phân chia liên tiếp?",
                "options": [
                    "Nhân đôi 1 lần và phân chia 1 lần",
                    "Nhân đôi 2 lần và phân chia 2 lần",
                    "Nhân đôi 1 lần và phân chia 2 lần liên tiếp",
                    "Nhân đôi 2 lần và phân chia 1 lần"
                ],
                "answer_index": 2,
                "explanation": "Giảm phân gồm 1 lần nhân đôi NST (ở kì trung gian trước giảm phân I) và 2 lần phân chia liên tiếp (Giảm phân I và Giảm phân II)."
            },
            {
                "question": "Ý nghĩa di truyền học của việc các nhiễm sắc tử chị em tách nhau ở tâm động và di chuyển về hai cực ở kì sau nguyên phân là gì?",
                "options": [
                    "Giúp phân chia đồng đều vật chất di truyền cho hai tế bào con",
                    "Làm giảm bộ NST của tế bào con đi một nửa",
                    "Tạo ra các biến dị tổ hợp phong phú ở đời con",
                    "Nhân đôi lượng vật chất di truyền trong nhân tế bào"
                ],
                "answer_index": 0,
                "explanation": "Việc tách nhau ở tâm động và di chuyển về 2 cực giúp 2 tế bào con nhận được bộ NST hoàn toàn giống nhau và giống hệt tế bào mẹ."
            },
            {
                "question": "Một tế bào sinh dục chín của một loài sinh vật có bộ NST 2n = 8 tiến hành giảm phân. Kết thúc giảm phân, số tế bào con tạo thành và số lượng NST trong mỗi tế bào con lần lượt là:",
                "options": [
                    "4 tế bào con, mỗi tế bào có 4 NST",
                    "2 tế bào con, mỗi tế bào có 8 NST",
                    "4 tế bào con, mỗi tế bào có 8 NST",
                    "2 tế bào con, mỗi tế bào có 4 NST"
                ],
                "answer_index": 0,
                "explanation": "Kết thúc giảm phân, 1 tế bào mẹ (2n = 8) tạo ra 4 tế bào con mang bộ NST giảm một nửa (n = 2n / 2 = 4 NST)."
            },
            {
                "question": "Hiện tượng con cái sinh ra có nhiều đặc điểm khác bố mẹ hoặc kết hợp đặc điểm của cả bố và mẹ là nhờ sự kết hợp của những quá trình nào sau đây?",
                "options": [
                    "Chỉ nguyên phân",
                    "Giảm phân và thụ tinh",
                    "Nguyên phân và thụ tinh",
                    "Chỉ nhân đôi DNA"
                ],
                "answer_index": 1,
                "explanation": "Quá trình giảm phân tạo ra nhiều loại giao tử khác nhau nhờ trao đổi chéo và phân li độc lập. Khi thụ tinh, các giao tử kết hợp ngẫu nhiên tạo ra các biến dị tổ hợp phong phú."
            }
        ]
    }
]


def get_complete_lessons() -> list[dict]:
    """Return a deep copy of all canonical complete lessons."""
    return deepcopy(COMPLETE_LESSONS)


def get_complete_lesson(grade: int, number: str) -> dict | None:
    """Find a canonical complete lesson by grade and lesson number."""
    target_num = number.strip().lower()
    for lesson in COMPLETE_LESSONS:
        if lesson.get("grade") == grade and lesson.get("number", "").strip().lower() == target_num:
            return deepcopy(lesson)
    return None
