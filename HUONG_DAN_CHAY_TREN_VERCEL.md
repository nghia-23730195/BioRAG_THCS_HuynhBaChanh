# 🚀 HƯỚNG DẪN TRIỂN KHAI HỆ THỐNG BIORAG LÊN VERCEL (MIỄN PHÍ 100%)

> **Đơn vị**: **TRƯỜNG THCS HUỲNH BÁ CHÁNH**  
> **Nền tảng**: **Vercel** (Serverless + Edge CDN toàn cầu)  
> **Tên miền website**: `https://thcs-huynhbachanh.vercel.app` (hoặc tên miền riêng `.id.vn`)  
> **Chi phí**: **0 VNĐ (Gói Vercel Hobby Miễn Phí)**

---

## 🎯 VÌ SAO CHỌN VERCEL?
1. **Tốc độ cực nhanh**: Tận dụng mạng lưới CDN toàn cầu của Vercel, thời gian tải trang dưới 0.5 giây.
2. **Có sẵn tên miền miễn phí**: Tên miền dạng `https://[tên-bạn-chọn].vercel.app`.
3. **Bảo mật chuẩn quốc tế**: Tự động cấp chứng chỉ SSL (HTTPS) miễn phí.
4. **Hỗ trợ tên miền riêng miễn phí**: Dễ dàng liên kết với tên miền `thcshuynhbachanh.id.vn`.

---

## 📦 CÁC FILE CẤU HÌNH ĐÃ ĐƯỢC CHUẨN BỊ SẴN CHO BẠN
Trong thư mục dự án đã có sẵn đầy đủ:
- **`vercel.json`**: Cấu hình định tuyến Serverless và phục vụ giao diện tĩnh (HTML/3D).
- **`api/index.py`**: Serverless Function Python nhẹ, tối ưu cold-start dưới 0.3s, không bị lỗi giới hạn 250MB của Vercel.
- **`api/requirements.txt`**: Khai báo các thư viện cần thiết (`Flask`, `google-generativeai`, `python-docx`).
- **`.gitignore`**: Đã loại trừ các file nặng không cần thiết (venv, cache, sqlite cục bộ) để việc upload lên Vercel siêu nhẹ và nhanh (chỉ mất vài giây).

---

## 🛠️ CÁCH 1: TRIỂN KHAI QUA GITHUB (KHUYÊN DÙNG - DỄ NHẤT)

### Bước 1: Đẩy mã nguồn lên GitHub
1. Mở Terminal / PowerShell tại thư mục `BioRAG_Final`:
```powershell
git init
git add .
git commit -m "Khoi tao he thong BioRAG THCS Huynh Ba Chanh tren Vercel"
git branch -M main
```
2. Tạo một repository mới trên GitHub (ví dụ: `BioRAG_THCS_HuynhBaChanh`).
3. Đẩy code lên:
```powershell
git remote add origin https://github.com/[tai-khoan-cua-ban]/BioRAG_THCS_HuynhBaChanh.git
git push -u origin main
```

### Bước 2: Nhập vào Vercel
1. Truy cập [https://vercel.com](https://vercel.com) và đăng nhập bằng tài khoản GitHub.
2. Bấm nút **"Add New..."** -> Chọn **"Project"**.
3. Chọn repository `BioRAG_THCS_HuynhBaChanh` vừa tạo và bấm **"Import"**.
4. Tại mục **Project Name**: Đặt tên `thcs-huynhbachanh` (để nhận tên miền `thcs-huynhbachanh.vercel.app`).
5. Tại mục **Environment Variables** (Biến môi trường), thêm khóa sau:
   - **Key**: `GEMINI_API_KEY`
   - **Value**: `[Khóa API Gemini của bạn]`
6. Bấm **"Deploy"**!
   - Vercel sẽ tự động build và xuất bản trong khoảng 1 phút.
   - Khi hoàn thành, bạn sẽ có ngay đường link:  
     👉 **`https://thcs-huynhbachanh.vercel.app`**

---

## ⚡ CÁCH 2: TRIỂN KHAI TRỰC TIẾP BẰNG LỆNH VERCEL CLI

Nếu không muốn qua GitHub, bạn có thể đẩy thẳng từ máy tính lên Vercel:

1. Mở PowerShell trong thư mục dự án:
```powershell
npx vercel
```
2. Trả lời các câu hỏi trên màn hình:
   - *Set up and deploy?* -> Gõ **Y** rồi Enter.
   - *Which scope?* -> Chọn tài khoản Vercel của bạn.
   - *Link to existing project?* -> Gõ **N**.
   - *What's your project's name?* -> Gõ **thcs-huynhbachanh**.
   - *In which directory is your code located?* -> Gõ **.** (dấu chấm) rồi Enter.
3. Thêm API Key cho Vercel:
```powershell
npx vercel env add GEMINI_API_KEY
```
*(Dán khóa Gemini API Key của bạn vào)*
4. Xuất bản chính thức ra Production:
```powershell
npx vercel --prod
```

---

## 🌐 CÁCH GẮN TÊN MIỀN RIÊNG `thcshuynhbachanh.id.vn` VÀO VERCEL
1. Trên bảng điều khiển Vercel của dự án, vào **Settings** -> **Domains**.
2. Nhập tên miền: `thcshuynhbachanh.id.vn` -> Bấm **Add**.
3. Vercel sẽ hiển thị 2 bản ghi DNS (ví dụ: `CNAME cname.vercel-dns.com` hoặc `A 76.76.21.21`).
4. Bạn chỉ cần vào trang quản lý tên miền (iNET / PA Việt Nam / Cloudflare) thêm 2 bản ghi đó vào.
5. Trong vòng 5–10 phút, tên miền riêng `https://thcshuynhbachanh.id.vn` sẽ hoạt động hoàn toàn miễn phí!
