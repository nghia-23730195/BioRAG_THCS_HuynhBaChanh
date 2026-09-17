# Đọc trước khi chạy trên Mac

Đây là bản **chỉ chứa mã nguồn + cấu hình** (~16MB), đã loại bỏ `venv/`, `__pycache__/`,
`.git/`, các file `.bat` (chỉ chạy được trên Windows), và các file backup/nháp không cần thiết.

## 3 thứ bạn phải tự chép thêm vào thư mục này trước khi chạy

Các thư mục/file này **quá nặng hoặc quá nhạy cảm** để chuyển qua được bằng công cụ hiện tại,
nên không có sẵn trong gói này — hãy tự chép trực tiếp từ máy Windows sang (USB / AirDrop /
Google Drive...), giữ nguyên tên, đặt ngay trong thư mục `BioRAG_ChoMac` này:

1. **`database_kntt/`** (hoặc `database_kntt_v2/`) — vector DB ChromaDB đã build sẵn từ 4 cuốn SGK.
   Không có thư mục này thì hệ thống sẽ không tìm được nội dung SGK để trả lời.
2. **`datasources/`** — các PDF gốc dùng làm nguồn dữ liệu (chỉ cần nếu bạn muốn chạy lại ETL；
   nếu chỉ dùng DB đã build sẵn ở trên thì có thể bỏ qua).
3. **`.env`** — đổi tên file `.env.example` (đã có sẵn trong gói) thành `.env` rồi điền
   `GEMINI_API_KEY` thật của bạn vào.

> Gói này **đã có sẵn** `public/sgk/*.pdf` không? → **Chưa** — 4 file PDF hiển thị trực tiếp
> trên web (`public/sgk/`) cũng nặng (30–40MB/file) nên chưa được chép vào. Hãy chép luôn
> thư mục `public/sgk/` từ máy Windows sang thư mục `public/` trong gói này nếu muốn học sinh
> xem được trang SGK gốc trên web.

## Cách chạy

Xem chi tiết đầy đủ trong `Huong_dan_trien_khai_BioRAG_macOS.md` (đã kèm trong gói).
Tóm tắt nhanh sau khi đã chép đủ 3 thứ trên:

```bash
chmod +x chay_biorag_mac.sh
./chay_biorag_mac.sh
```

Lần đầu chạy sẽ tự tạo `venv` + cài thư viện (mất vài phút), các lần sau chạy ngay.
Trình duyệt tự mở tại `http://127.0.0.1:5001/`.
