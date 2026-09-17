# Hướng dẫn chạy BioRAG local trên macOS

Dự án hiện đang phát triển trên Windows (`G:\SMLab_KHKT\...\BioRAG_Final`, có file `.bat`,
`TESSERACT_CMD`/`POPPLER_PATH` kiểu Windows). macOS không có các thứ đó, và **không có
CUDA GPU** (kể cả Apple Silicon chỉ có MPS, transformers chưa hỗ trợ tốt cho pipeline này),
nên cách chạy tối ưu trên Mac là: **dùng Gemini API làm LLM** (bỏ qua việc tải Qwen2.5-3B
chạy local) và **dùng vector DB đã build sẵn** (không chạy lại ETL/OCR) — giống hệt cách
dự án đã chạy ổn trên Docker/Render/Hugging Face Spaces (cũng chỉ chạy CPU, không GPU).

---

## 1. Yêu cầu

- macOS (Intel hoặc Apple Silicon đều được)
- [Homebrew](https://brew.sh)
- Python **3.10** (đúng version Dockerfile đang dùng, tránh lỗi tương thích gói)

```bash
# Cài Homebrew nếu chưa có
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Công cụ hệ thống cần cho OCR/PDF (chỉ dùng nếu bạn xử lý PDF mới; SGK đã OCR sẵn thì vẫn nên cài phòng khi cần)
brew install python@3.10 tesseract tesseract-lang poppler git
```

`tesseract-lang` cài kèm gói ngôn ngữ (có tiếng Việt `vie.traineddata`).

---

## 2. Chuyển mã nguồn từ máy Windows sang Mac

**Cách A — qua GitHub (khuyên dùng):** trên máy Windows đã có sẵn hướng dẫn push Git trong
`HUONG_DAN_CHAY_TREN_VERCEL.md`. Trên Mac chỉ cần `git clone` lại.

**Cách B — chép trực tiếp (USB / AirDrop / Google Drive):** chép cả thư mục `BioRAG_Final`,
có thể bỏ qua để nhẹ: `venv/`, `__pycache__/`, `.git/`, `_BACKUP_before_groupA_20260911/`.

⚠️ **Quan trọng:** file `.gitignore` của dự án loại trừ khỏi Git:
```
database_kntt/, database_kntt_v2/, datasources/, datasources_kntt8_fix/, .env
```
Nếu bạn dùng Cách A (GitHub), **4 thứ này sẽ không có trên Mac** — phải chép tay riêng
(USB/AirDrop/Drive) nếu muốn dùng ngay dữ liệu SGK đã xử lý sẵn (~13.7k đoạn văn bản +
ảnh minh họa đã trích xuất), nếu không bạn sẽ phải chạy lại toàn bộ ETL (rất lâu vì phải
OCR lại 4 cuốn SGK).

---

## 3. Tạo môi trường Python & cài thư viện

```bash
cd BioRAG_Final
python3.10 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements_docker.txt
```

`requirements_docker.txt` là bộ gói **đã chứng minh chạy được không cần GPU** (chính là bộ
Dockerfile dùng để deploy Render/HF Spaces) — gồm chromadb, langchain, sentence-transformers
(tự kéo theo torch + transformers CPU cho phần embedding text/ảnh CLIP), google-generativeai...
Bộ này **đủ để chạy API phục vụ RAG + chatbot + soạn giáo án/đề thi + quiz + lab ảo** dựa trên
DB đã build sẵn.

Bạn **không cần** cài `paddleocr`/`paddlepaddle` (dễ lỗi trên Apple Silicon) trừ khi muốn
chạy lại ETL để nạp SGK mới — xem mục 7.

---

## 4. Tạo file `.env` trên Mac

Đừng chép nguyên `.env` từ Windows nếu nó chứa đường dẫn kiểu `C:\...`. Tạo file `.env`
mới trong thư mục `BioRAG_Final` với nội dung (điền key thật của bạn):

```env
GEMINI_API_KEY=<khoa_gemini_cua_ban>
# hoặc nhiều key để xoay vòng tránh rate-limit:
# GEMINI_API_KEYS=key1,key2,key3

TESSERACT_CMD=tesseract
POPPLER_PATH=

USE_GPU=false

RAG_DATA_DIR=datasources
RAG_DATABASE_DIR=database_kntt

AUTH_SECRET_KEY=<tuy_chon_doi_lai_cho_bao_mat>
TEACHER_PASSWORD=<tuy_chon>
ADMIN_PASSWORD=<tuy_chon>
```

Giải thích khác Windows:
- `POPPLER_PATH` để **trống** — Homebrew cài poppler thẳng vào PATH, không cần chỉ đường dẫn thủ công như Windows.
- `TESSERACT_CMD=tesseract` — cũng nhờ Homebrew đưa vào PATH sẵn.
- `USE_GPU=false` — Mac không có CUDA.

---

## 5. Đặt dữ liệu đã build sẵn đúng chỗ

Sau khi chép `database_kntt/` (hoặc `database_kntt_v2/`) và `datasources/` (PDF SGK) từ
Windows sang, đặt đúng cấu trúc thư mục gốc dự án:

```
BioRAG_Final/
  database_kntt/       ← vector DB Chroma đã build
  datasources/          ← PDF gốc dùng cho ETL/tham chiếu
  public/sgk/*.pdf       ← PDF hiển thị trực tiếp trên web (đã có sẵn trong repo)
```

---

## 6. Chạy thử

```bash
source venv/bin/activate
python main.py --api --port 5001
```

⚠️ **Lưu ý riêng cho macOS:** cổng **5000 mặc định đã bị chiếm bởi "AirPlay Receiver"**
của macOS (System Settings → General → AirDrop & Handoff → tắt AirPlay Receiver), nên
dùng cổng khác (`5001`, `8000`...) như ví dụ trên cho chắc.

Mở trình duyệt: **http://localhost:5001**

---

## 7. (Tuỳ chọn) Script khởi động nhanh kiểu `.bat` cho Mac

Tạo file `chay_biorag.sh` trong thư mục dự án:

```bash
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python main.py --api --port 5001
```

```bash
chmod +x chay_biorag.sh
./chay_biorag.sh
```

---

## 8. Nếu muốn chạy lại ETL/OCR trên Mac (nạp SGK mới)

Đây là phần nặng, chỉ cần nếu bạn thêm sách mới chứ không chỉ "chạy thử":
- Cần thêm: `pymupdf`, `pdf2image`, `pytesseract`, `opencv-python`, `rapidocr-onnxruntime`, `vietocr`.
- Dự án **đã tự né PaddleOCR gốc** (rất khó cài ổn định trên Apple Silicon) bằng cách dùng
  RapidOCR (ONNX) + VietOCR (PyTorch) trong `src/etl/paddle_vietocr.py` — cả hai chạy CPU
  tốt trên cả Intel lẫn Apple Silicon, không cần bản build riêng cho ARM.
- Chạy: `python main.py --etl` (đầy đủ) hoặc `--text-only` / `--image-only`.

---

## 9. Việc mình chưa làm được từ đây

Vì Mac của bạn chưa được kết nối với phiên Claude này (chỉ máy Windows admin-pc đang nối),
mình không thể tự copy file/chạy lệnh trực tiếp trên Mac. Nếu bạn mở lại tác vụ này bằng
Claude desktop app **trên chính máy Mac**, mình có thể làm trực tiếp các bước 2–6 giúp bạn
(clone/copy code, tạo venv, cài gói, sửa `.env`, chạy thử và soát lỗi).
