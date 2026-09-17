"""Four canonical complete sample lessons for the BioRAG learning area."""

from __future__ import annotations

from copy import deepcopy


COMPLETE_LESSON_VERSION = 2


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
            "Vận dụng kiến thức để nhận biết một số loại tế bào quen thuộc.",
        ],
        "content": (
            "Mọi cơ thể sống đều được cấu tạo từ tế bào. Tế bào rất nhỏ nhưng có thể "
            "thực hiện những hoạt động sống cơ bản. Tế bào có nhiều hình dạng, kích thước "
            "khác nhau và đặc điểm đó thường phù hợp với chức năng của chúng."
        ),
        "source_label": "SGK KHTN 6 KNTT · Bài 18 · Trang 64–67",
        "warmup": {
            "question": "Cây đậu, con cá và cơ thể người rất khác nhau. Chúng có điểm cấu tạo chung nào?",
            "hint": "Hãy nghĩ đến đơn vị rất nhỏ chỉ quan sát rõ bằng kính hiển vi.",
        },
        "sections": [
            {
                "title": "1. Tế bào là gì?",
                "paragraphs": [
                    "Tế bào là đơn vị cấu tạo cơ bản của mọi cơ thể sống. Có sinh vật chỉ gồm một tế bào; cũng có sinh vật gồm rất nhiều tế bào phối hợp với nhau.",
                    "Dù rất nhỏ, tế bào vẫn thực hiện các hoạt động sống như trao đổi chất, lớn lên và sinh sản.",
                ],
                "example": "Vi khuẩn là cơ thể đơn bào; cây đậu và con người là cơ thể đa bào.",
            },
            {
                "title": "2. Hình dạng của tế bào",
                "paragraphs": [
                    "Tế bào có thể có dạng hình cầu, hình đĩa, hình que, hình sao hoặc dạng sợi. Hình dạng thường liên quan đến nhiệm vụ mà tế bào đảm nhiệm.",
                ],
                "bullets": [
                    "Tế bào hồng cầu có dạng đĩa lõm hai mặt, thuận lợi cho vận chuyển khí.",
                    "Tế bào thần kinh có nhiều nhánh dài, thuận lợi cho truyền tín hiệu.",
                    "Tế bào cơ có dạng sợi dài, phù hợp với khả năng co và giãn.",
                ],
            },
            {
                "title": "3. Kích thước của tế bào",
                "paragraphs": [
                    "Phần lớn tế bào có kích thước hiển vi nên cần kính hiển vi để quan sát. Một số tế bào có thể nhìn thấy bằng mắt thường, chẳng hạn tế bào trứng của một số động vật.",
                    "Kích thước cơ thể không quyết định trực tiếp kích thước tế bào; cơ thể lớn thường có số lượng tế bào nhiều hơn.",
                ],
                "note": "Không kết luận cơ thể càng lớn thì từng tế bào càng lớn.",
            },
        ],
        "diagram": {
            "title": "Từ tế bào đến cơ thể sống",
            "nodes": ["Tế bào", "Mô", "Cơ quan", "Hệ cơ quan", "Cơ thể"],
        },
        "terms": [
            {"term": "Tế bào", "definition": "Đơn vị cấu tạo cơ bản của cơ thể sống."},
            {"term": "Đơn bào", "definition": "Cơ thể chỉ gồm một tế bào."},
            {"term": "Đa bào", "definition": "Cơ thể gồm nhiều tế bào."},
            {"term": "Kính hiển vi", "definition": "Dụng cụ giúp quan sát vật thể rất nhỏ."},
        ],
        "summary": [
            "Mọi cơ thể sống đều được cấu tạo từ tế bào.",
            "Tế bào thực hiện các hoạt động sống cơ bản.",
            "Hình dạng và kích thước tế bào rất đa dạng, thường phù hợp với chức năng.",
        ],
        "quick_check": [
            {
                "question": "Đơn vị cấu tạo cơ bản của cơ thể sống là gì?",
                "options": ["Mô", "Tế bào", "Cơ quan", "Hệ cơ quan"],
                "answer_index": 1,
                "explanation": "Tế bào là đơn vị cấu tạo cơ bản của tất cả cơ thể sống.",
            },
            {
                "question": "Vì sao tế bào thần kinh có nhiều nhánh dài?",
                "options": ["Để dự trữ nước", "Để truyền tín hiệu", "Để tạo màu", "Để tiêu hóa thức ăn"],
                "answer_index": 1,
                "explanation": "Các nhánh dài giúp tế bào thần kinh tiếp nhận và truyền tín hiệu.",
            },
            {
                "question": "Nhận định nào đúng?",
                "options": ["Mọi tế bào đều nhìn thấy bằng mắt thường", "Tất cả tế bào có cùng hình dạng", "Phần lớn tế bào cần kính hiển vi để quan sát", "Cơ thể lớn luôn có tế bào lớn"],
                "answer_index": 2,
                "explanation": "Phần lớn tế bào có kích thước hiển vi.",
            },
        ],
        "order": 10,
        "active": True,
        "origin": "system",
        "lesson_version": COMPLETE_LESSON_VERSION,
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
            "Phân biệt được tổng hợp và phân giải chất hữu cơ.",
        ],
        "content": (
            "Hô hấp tế bào là quá trình phân giải chất hữu cơ trong tế bào, thường sử dụng "
            "oxygen, tạo carbon dioxide, nước và giải phóng năng lượng cho các hoạt động sống."
        ),
        "source_label": "SGK KHTN 7 KNTT · Bài 25 · Trang 111–112",
        "warmup": {
            "question": "Vì sao sau khi chạy nhanh, em thở gấp và cảm thấy cơ thể nóng lên?",
            "hint": "Cơ bắp đang cần nhiều năng lượng hơn khi vận động.",
        },
        "sections": [
            {
                "title": "1. Khái niệm hô hấp tế bào",
                "paragraphs": [
                    "Hô hấp tế bào là chuỗi phản ứng phân giải chất hữu cơ diễn ra trong tế bào. Năng lượng hóa học trong chất hữu cơ được giải phóng và một phần được tích lũy trong ATP.",
                    "Ở nhiều sinh vật, glucose là nguyên liệu hữu cơ phổ biến và oxygen tham gia quá trình hô hấp hiếu khí.",
                ],
            },
            {
                "title": "2. Nguyên liệu và sản phẩm",
                "paragraphs": [
                    "Có thể mô tả khái quát: glucose và oxygen tạo thành carbon dioxide, nước và năng lượng.",
                    "Năng lượng giải phóng được dùng cho vận động, sinh trưởng, tổng hợp chất, vận chuyển chất và duy trì nhiệt độ cơ thể.",
                ],
                "note": "Hô hấp tế bào không đồng nhất với động tác hít vào – thở ra; hít thở giúp trao đổi khí, còn hô hấp tế bào diễn ra bên trong tế bào.",
            },
            {
                "title": "3. Tổng hợp và phân giải chất hữu cơ",
                "paragraphs": [
                    "Quá trình tổng hợp tạo chất hữu cơ và tích lũy năng lượng; quá trình phân giải phá vỡ chất hữu cơ và giải phóng năng lượng.",
                    "Hai nhóm quá trình liên hệ chặt chẽ: sản phẩm của quá trình này có thể trở thành nguyên liệu của quá trình kia.",
                ],
                "example": "Quang hợp tạo glucose và oxygen; hô hấp tế bào sử dụng chúng để giải phóng năng lượng.",
            },
        ],
        "diagram": {
            "title": "Sơ đồ hô hấp tế bào",
            "nodes": ["Glucose + Oxygen", "Hô hấp tế bào", "Carbon dioxide + Nước + Năng lượng"],
        },
        "terms": [
            {"term": "Hô hấp tế bào", "definition": "Quá trình phân giải chất hữu cơ và giải phóng năng lượng trong tế bào."},
            {"term": "ATP", "definition": "Dạng năng lượng tế bào có thể sử dụng trực tiếp."},
            {"term": "Phân giải", "definition": "Biến đổi chất phức tạp thành chất đơn giản hơn, thường giải phóng năng lượng."},
            {"term": "Tổng hợp", "definition": "Tạo chất phức tạp từ chất đơn giản hơn, thường cần năng lượng."},
        ],
        "summary": [
            "Hô hấp tế bào phân giải chất hữu cơ để giải phóng năng lượng.",
            "Nguyên liệu phổ biến là glucose và oxygen; sản phẩm gồm carbon dioxide, nước và năng lượng.",
            "Năng lượng được dùng cho mọi hoạt động sống của tế bào và cơ thể.",
        ],
        "quick_check": [
            {
                "question": "Sản phẩm nào được tạo ra trong hô hấp tế bào hiếu khí?",
                "options": ["Glucose và oxygen", "Carbon dioxide, nước và năng lượng", "Chỉ oxygen", "Chỉ glucose"],
                "answer_index": 1,
                "explanation": "Hô hấp tế bào sử dụng glucose và oxygen, tạo carbon dioxide, nước và giải phóng năng lượng.",
            },
            {
                "question": "Vai trò trực tiếp nhất của hô hấp tế bào là gì?",
                "options": ["Tạo ánh sáng", "Giải phóng năng lượng", "Tạo oxygen", "Giảm số lượng tế bào"],
                "answer_index": 1,
                "explanation": "Quá trình giải phóng năng lượng để cung cấp cho các hoạt động sống.",
            },
            {
                "question": "Nhận định nào đúng?",
                "options": ["Hô hấp tế bào chỉ là động tác thở", "Hô hấp tế bào chỉ xảy ra khi vận động", "Hô hấp tế bào diễn ra trong tế bào", "Hô hấp tế bào tạo glucose"],
                "answer_index": 2,
                "explanation": "Hít thở và hô hấp tế bào liên quan nhưng không phải một quá trình.",
            },
        ],
        "order": 10,
        "active": True,
        "origin": "system",
        "lesson_version": COMPLETE_LESSON_VERSION,
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
            "Đề xuất được biện pháp bảo vệ hệ vận động trong học tập và sinh hoạt.",
        ],
        "content": (
            "Hệ vận động gồm bộ xương và hệ cơ. Xương tạo khung và bảo vệ cơ thể; khớp nối "
            "các xương; cơ bám vào xương, co và dãn để làm xương chuyển động quanh khớp."
        ),
        "source_label": "SGK KHTN 8 KNTT · Bài 31 · Trang 125–129",
        "warmup": {
            "question": "Khi em gập cẳng tay, những bộ phận nào phối hợp để tạo ra chuyển động?",
            "hint": "Hãy quan sát cơ ở cánh tay, xương cẳng tay và khớp khuỷu.",
        },
        "sections": [
            {
                "title": "1. Cấu tạo của hệ vận động",
                "paragraphs": [
                    "Bộ xương gồm xương đầu, xương thân và xương chi. Các xương nối với nhau tại khớp. Hệ cơ gồm các cơ bám vào xương nhờ mô liên kết.",
                    "Xương tạo khung nâng đỡ, định hình và bảo vệ cơ quan; cơ tạo lực; khớp là vị trí cho phép các phần xương chuyển động tương đối với nhau.",
                ],
            },
            {
                "title": "2. Sự phối hợp tạo vận động",
                "paragraphs": [
                    "Khi cơ co, cơ ngắn lại và kéo xương chuyển động quanh khớp. Nhiều vận động cần các nhóm cơ đối kháng phối hợp: một cơ co trong khi cơ kia dãn.",
                ],
                "example": "Khi gập cẳng tay, cơ phía trước cánh tay co và cơ phía sau dãn; khi duỗi tay, hoạt động của hai nhóm cơ đổi lại.",
            },
            {
                "title": "3. Bảo vệ hệ vận động",
                "paragraphs": [
                    "Dinh dưỡng hợp lí, vận động vừa sức và tư thế đúng giúp xương, khớp, cơ phát triển khỏe mạnh. Cần khởi động trước khi luyện tập và dùng đồ bảo hộ phù hợp.",
                ],
                "bullets": [
                    "Ngồi học thẳng lưng, bàn ghế phù hợp chiều cao.",
                    "Mang cặp đều hai vai, tránh mang vật quá nặng lệch một bên.",
                    "Bổ sung đủ protein, calcium, vitamin D và vận động ngoài trời hợp lí.",
                    "Khi chấn thương, hạn chế di chuyển vùng tổn thương và tìm hỗ trợ y tế.",
                ],
                "note": "Không tự nắn chỉnh xương hoặc khớp khi nghi ngờ gãy xương, trật khớp.",
            },
        ],
        "diagram": {
            "title": "Cơ chế tạo vận động",
            "nodes": ["Cơ co hoặc dãn", "Kéo xương", "Xương quay quanh khớp", "Cơ thể vận động"],
        },
        "terms": [
            {"term": "Bộ xương", "definition": "Hệ thống xương tạo khung nâng đỡ và bảo vệ cơ thể."},
            {"term": "Khớp", "definition": "Nơi tiếp giáp giữa các xương."},
            {"term": "Cơ đối kháng", "definition": "Các cơ tạo ra những tác động ngược chiều và phối hợp trong vận động."},
            {"term": "Cong vẹo cột sống", "definition": "Tình trạng cột sống cong hoặc lệch bất thường."},
        ],
        "summary": [
            "Hệ vận động gồm bộ xương và hệ cơ; khớp nối các xương.",
            "Cơ co tạo lực kéo làm xương chuyển động quanh khớp.",
            "Tư thế đúng, dinh dưỡng và luyện tập hợp lí giúp bảo vệ hệ vận động.",
        ],
        "quick_check": [
            {
                "question": "Bộ phận nào trực tiếp tạo lực kéo xương?",
                "options": ["Da", "Cơ", "Máu", "Dây thần kinh"],
                "answer_index": 1,
                "explanation": "Cơ co và truyền lực kéo lên xương qua vị trí bám.",
            },
            {
                "question": "Khớp có vai trò chính nào trong vận động?",
                "options": ["Tạo máu", "Tiêu hóa thức ăn", "Nối xương và cho phép chuyển động", "Trao đổi khí"],
                "answer_index": 2,
                "explanation": "Khớp là nơi tiếp giáp giữa các xương và tạo điều kiện cho chuyển động.",
            },
            {
                "question": "Thói quen nào giúp hạn chế cong vẹo cột sống?",
                "options": ["Mang cặp lệch một vai", "Ngồi học đúng tư thế", "Ít vận động", "Mang vật quá nặng"],
                "answer_index": 1,
                "explanation": "Tư thế đúng và bàn ghế phù hợp giúp giảm tải không cân đối lên cột sống.",
            },
        ],
        "order": 10,
        "active": True,
        "origin": "system",
        "lesson_version": COMPLETE_LESSON_VERSION,
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
            "Vận dụng kiến thức để giải thích cầu vồng và màu sắc của vật.",
        ],
        "content": (
            "Lăng kính là khối trong suốt có hai mặt phẳng không song song. Khi ánh sáng trắng "
            "đi qua lăng kính, các thành phần màu bị lệch khác nhau và tách thành dải màu liên tục."
        ),
        "source_label": "SGK KHTN 9 KNTT · Bài 7 · Trang 34–36",
        "warmup": {
            "question": "Vì sao một chùm ánh sáng trắng qua lăng kính lại tạo thành nhiều màu?",
            "hint": "Các ánh sáng màu thành phần bị lệch với mức độ khác nhau.",
        },
        "sections": [
            {
                "title": "1. Lăng kính",
                "paragraphs": [
                    "Lăng kính là một khối chất trong suốt, đồng chất, thường có dạng lăng trụ tam giác. Hai mặt bên dùng cho ánh sáng truyền qua không song song với nhau.",
                    "Tia sáng đổi hướng khi truyền qua các mặt phân cách giữa không khí và lăng kính do hiện tượng khúc xạ.",
                ],
            },
            {
                "title": "2. Tán sắc ánh sáng trắng",
                "paragraphs": [
                    "Khi chùm ánh sáng trắng hẹp đi qua lăng kính, nó tách thành dải nhiều màu liên tục, thường quan sát theo thứ tự đỏ, da cam, vàng, lục, lam, chàm, tím.",
                    "Hiện tượng ánh sáng trắng bị phân tách thành các ánh sáng màu thành phần được gọi là tán sắc ánh sáng.",
                ],
                "note": "Trong điều kiện thí nghiệm điển hình, tia đỏ lệch ít hơn và tia tím lệch nhiều hơn.",
            },
            {
                "title": "3. Ánh sáng đơn sắc và màu sắc của vật",
                "paragraphs": [
                    "Ánh sáng đơn sắc có một màu xác định và không bị tách thành nhiều màu khi truyền qua lăng kính. Ánh sáng trắng là hỗn hợp của nhiều ánh sáng màu.",
                    "Màu ta nhìn thấy phụ thuộc vào ánh sáng chiếu tới và khả năng hấp thụ, phản xạ ánh sáng của vật.",
                ],
                "example": "Cầu vồng hình thành khi ánh sáng Mặt Trời bị khúc xạ, tán sắc và phản xạ trong các giọt nước nhỏ.",
            },
        ],
        "diagram": {
            "title": "Tán sắc qua lăng kính",
            "nodes": ["Ánh sáng trắng", "Lăng kính", "Đỏ → Da cam → Vàng → Lục → Lam → Chàm → Tím"],
        },
        "terms": [
            {"term": "Lăng kính", "definition": "Khối trong suốt có hai mặt khúc xạ không song song."},
            {"term": "Tán sắc", "definition": "Sự phân tách ánh sáng trắng thành các ánh sáng màu thành phần."},
            {"term": "Ánh sáng trắng", "definition": "Hỗn hợp của nhiều ánh sáng màu."},
            {"term": "Ánh sáng đơn sắc", "definition": "Ánh sáng có một màu xác định và không bị tách màu qua lăng kính."},
        ],
        "summary": [
            "Lăng kính làm tia sáng đổi hướng do khúc xạ.",
            "Ánh sáng trắng qua lăng kính bị tách thành dải nhiều màu.",
            "Các màu lệch khác nhau; đỏ lệch ít hơn tím trong thí nghiệm điển hình.",
            "Màu sắc quan sát được phụ thuộc ánh sáng chiếu tới và ánh sáng vật phản xạ.",
        ],
        "quick_check": [
            {
                "question": "Hiện tượng tán sắc là gì?",
                "options": ["Ánh sáng bị phản xạ hoàn toàn", "Ánh sáng trắng tách thành nhiều màu", "Âm thanh đổi tần số", "Vật phát nhiệt"],
                "answer_index": 1,
                "explanation": "Tán sắc là sự phân tách ánh sáng trắng thành các ánh sáng màu thành phần.",
            },
            {
                "question": "Trong dải màu qua lăng kính, màu nào thường lệch ít hơn?",
                "options": ["Đỏ", "Tím", "Chàm", "Lam"],
                "answer_index": 0,
                "explanation": "Trong thí nghiệm điển hình, tia đỏ lệch ít nhất và tia tím lệch nhiều nhất.",
            },
            {
                "question": "Ánh sáng đơn sắc qua lăng kính sẽ thế nào?",
                "options": ["Tách thành bảy màu", "Không truyền qua", "Bị lệch nhưng không tách thành nhiều màu", "Luôn phản xạ trở lại"],
                "answer_index": 2,
                "explanation": "Ánh sáng đơn sắc có một màu nên không bị phân tách thành dải nhiều màu.",
            },
        ],
        "order": 10,
        "active": True,
        "origin": "system",
        "lesson_version": COMPLETE_LESSON_VERSION,
    },
]


def get_complete_lessons():
    return deepcopy(COMPLETE_LESSONS)
