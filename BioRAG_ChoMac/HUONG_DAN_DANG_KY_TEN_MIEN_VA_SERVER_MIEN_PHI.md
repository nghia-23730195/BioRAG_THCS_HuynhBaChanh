# 🌐 HƯỚNG DẪN ĐẨY HỆ THỐNG BIORAG LÊN WEBSITE VỚI TÊN MIỀN THCS HUỲNH BÁ CHÁNH (SERVER MIỄN PHÍ)

> **Dự án**: Hệ thống Trợ lý RAG AI & Phòng Thí nghiệm Ảo KHTN 6–9  
> **Đơn vị**: **TRƯỜNG THCS HUỲNH BÁ CHÁNH**  
> **Chi phí triển khai**: **0 VNĐ (Hoàn toàn Miễn Phí)**

---

## 📌 TỔNG QUAN VỀ ĐẶC ĐIỂM HỆ THỐNG
Hệ thống **BioRAG** tích hợp:
1. **Frontend**: Giao diện Web học tập tương tác cao, thí nghiệm 3D Three.js, làm đề trắc nghiệm chuẩn Công văn 3280.
2. **Backend**: Python Flask API, ChromaDB (Vector Database chứa toàn bộ SGK KNTT Lớp 6, 7, 8, 9), mô hình Embeddings `paraphrase-multilingual-MiniLM-L12-v2`, kết nối Gemini 3.1 Flash Lite API.
3. **Yêu cầu phần cứng**: Cần tối thiểu **1.5 GB – 2 GB RAM** để nạp mô hình ngôn ngữ và cơ sở dữ liệu tri thức. Do đó, các nền tảng miễn phí có cấu hình quá yếu như Render hay Vercel (chỉ cho 512 MB RAM) sẽ bị tràn bộ nhớ (Out of Memory).

Dưới đây là **3 giải pháp tối ưu nhất** để phát hành hệ thống lên Internet với tên miền **THCS HUỲNH BÁ CHÁNH** mà **không tốn một đồng chi phí nào**.

---

## 🚀 CÁCH 1: PHÁT HÀNH ONLINE TRỰC TIẾP TỪ MÁY TÍNH (1 CÚ CLICK - KHUYÊN DÙNG NGAY)

Đây là cách nhanh nhất, không cần cài đặt thêm phần mềm máy chủ phức tạp, tận dụng chính sức mạnh máy tính hiện tại của bạn làm Server.

### 1. Thao tác khởi động
1. Vào thư mục dự án `BioRAG_Final`.
2. Bấm đúp chuột vào file:  
   👉 **`CHAY_ONLINE_THCS_HUYNH_BA_CHANH.bat`**
3. Hệ thống sẽ tự động:
   - Khởi động backend Flask API (cổng 5000).
   - Nạp toàn bộ kho ngữ liệu SGK và mô hình AI.
   - Lấy IP mạng công khai làm mã khóa bảo mật.
   - Thiết lập đường hầm bảo mật công khai toàn cầu.

### 2. Địa chỉ Website chính thức
- 🌐 **Đường link Website**: `https://thcs-huynhbachanh.loca.lt`
- 🔑 **Mật khẩu truy cập (Tunnel Password)**: Cửa sổ màu đen sẽ hiển thị dãy số IP của bạn (ví dụ: `113.185.42.10`).

### 3. Hướng dẫn cho Học sinh và Giáo viên khi truy cập
1. Dùng điện thoại hoặc máy tính truy cập: `https://thcs-huynhbachanh.loca.lt`
2. Tại màn hình màu xanh yêu cầu nhập mật khẩu bảo vệ, dán dãy số IP được cấp vào ô **"Tunnel Password"**.
3. Bấm **"Click to Submit"** là sẽ vào ngay trang chủ BioRAG của Trường THCS Huỳnh Bá Chánh!

---

## 🏷️ CÁCH 2: ĐĂNG KÝ TÊN MIỀN QUỐC GIA `.id.vn` HOÀN TOÀN MIỄN PHÍ (BỘ TT&TT)

Nếu bạn muốn có một tên miền riêng chuyên nghiệp dạng:  
👉 **`thcshuynhbachanh.id.vn`** hoặc **`khtn-huynhbachanh.id.vn`**

Trung tâm Internet Việt Nam (**VNNIC** - Bộ Thông tin & Truyền thông) đang triển khai chương trình phổ cập tên miền số quốc gia: **Cấp MIỄN PHÍ 100% lệ phí đăng ký và duy trì trong 2 năm cho học sinh, thanh niên (18-23 tuổi) và các đề tài giáo dục**.

### Các bước nhận tên miền 0đ:
1. Truy cập vào một trong các nhà đăng ký chính thức của VNNIC:
   - **iNET**: [https://inet.vn](https://inet.vn)
   - **PA Việt Nam**: [https://pavietnam.vn](https://pavietnam.vn)
   - **Mắt Bão**: [https://matbao.net](https://matbao.net)
2. Gõ tìm kiếm: `thcshuynhbachanh.id.vn`.
3. Chọn đăng ký -> Tích chọn ưu đãi theo chương trình của Bộ TT&TT (giá hiển thị sẽ giảm về **0 VNĐ**).
4. Xác thực CCCD / Thẻ học sinh theo hướng dẫn trực tuyến (chỉ mất 2 phút duyệt tự động).
5. **Kết nối tên miền vào máy chủ**:
   - Sử dụng **Cloudflare Zero Trust (Cloudflare Tunnel)** hoàn toàn miễn phí.
   - Trỏ tên miền `thcshuynhbachanh.id.vn` về cổng 5000 của máy tính.
   - Khi đó, bất kỳ ai cũng có thể truy cập thẳng bằng địa chỉ `https://thcshuynhbachanh.id.vn` mà không cần nhập mật khẩu IP!

---

## ☁️ CÁCH 3: ĐƯA LÊN CLOUD SERVER MIỄN PHÍ 24/7 (HUGGING FACE SPACES)

Nếu bạn muốn hệ thống chạy liên tục trên mạng Internet 24/24 mà **không cần bật máy tính ở trường**, nền tảng đám mây tốt nhất thế giới hiện nay cho AI mã nguồn mở là **Hugging Face Spaces**.

### Tại sao chọn Hugging Face Spaces?
- **Cấu hình miễn phí 100%**: **16 GB RAM + 2 vCPU + 50 GB ổ cứng**.
- Không bao giờ bị lỗi thiếu RAM như Render hay Railway.
- Có sẵn chứng chỉ bảo mật HTTPS (SSL).
- Tên miền website miễn phí: `https://[ten-tai-khoan]-thcs-huynh-ba-chanh.hf.space`.

### Các bước đưa lên Hugging Face Spaces:
1. Đăng ký tài khoản miễn phí tại [https://huggingface.co](https://huggingface.co).
2. Bấm **New Space** -> Đặt tên: `thcs-huynh-ba-chanh`.
3. Chọn Space SDK: **Docker** (Blank) -> Chọn gói phần cứng: **CPU basic (Free, 16GB RAM)**.
4. Clone repo của Space về máy tính hoặc kéo thả các file sau lên:
   - Thư mục `src/`
   - Thư mục `database_kntt/`
   - File `index.html`
   - File `main.py`
   - File `Dockerfile` (đã được tạo sẵn trong dự án)
   - File `.env` (chứa API KEY Gemini của bạn)
5. Hugging Face sẽ tự động build và chạy trang web lên Internet vĩnh viễn 24/7!

---

## 📋 TÓM TẮT ĐỀ XUẤT THỰC HIỆN

| Nhu cầu | Giải pháp đề xuất | Tên miền đạt được | Chi phí | Thời gian thiết lập |
| :--- | :--- | :--- | :--- | :--- |
| **Dùng ngay hôm nay để chấm thi / báo cáo** | Chạy file `CHAY_ONLINE_THCS_HUYNH_BA_CHANH.bat` | `https://thcs-huynhbachanh.loca.lt` | **0 đ** | **30 giây** |
| **Có tên miền thương hiệu trường học** | Đăng ký miễn phí tên miền quốc gia `.id.vn` của VNNIC | `https://thcshuynhbachanh.id.vn` | **0 đ** | **1 ngày duyệt** |
| **Chạy online 24/24 không cần bật máy** | Đưa lên Hugging Face Spaces (16GB RAM) | `https://[user]-thcs-huynh-ba-chanh.hf.space` | **0 đ** | **15 phút** |

*(Tất cả mã nguồn trong hệ thống đã được cập nhật chuẩn nhận diện tên Trường THCS Huỳnh Bá Chánh)*.
