"""Four canonical complete sample lessons for the BioRAG learning area."""

from __future__ import annotations

from copy import deepcopy


COMPLETE_LESSON_VERSION = 4


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
        "order": 180,
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
        "order": 250,
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
        "order": 310,
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
        "order": 70,
        "active": True,
        "origin": "system",
        "lesson_version": COMPLETE_LESSON_VERSION,
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


def get_complete_lessons():
    return deepcopy(COMPLETE_LESSONS)
