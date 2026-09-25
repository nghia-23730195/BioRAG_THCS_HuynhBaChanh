@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"

title BioRAG - THCS Huỳnh Bá Chánh

echo ==========================================
echo   HỆ THỐNG BIORAG - THCS HUỲNH BÁ CHÁNH
echo   (Khởi động một chạm - Máy chủ cục bộ)
echo ==========================================
echo.

set "PORT=5000"
set "PYTHONUTF8=1"
set "RAG_DATABASE_DIR=database_kntt"
set "RAG_DATA_DIR=datasources"

REM ---------- 1. Kiểm tra file gốc dự án ----------
if not exist "main.py" (
    echo [LỖI] Không tìm thấy main.py.
    echo Hãy đặt file .bat này ngay trong thư mục gốc BioRAG_THCS_HuynhBaChanh rồi chạy lại.
    pause
    exit /b 1
)

REM ---------- 2. Kiểm tra Python đã cài chưa ----------
where python >nul 2>&1
if errorlevel 1 (
    echo [LỖI] Máy tính chưa cài Python.
    echo Vui lòng tải và cài Python 3.10+ tại: https://www.python.org/downloads/
    echo Lưu ý: khi cài đặt phải TICK vào ô "Add Python to PATH".
    pause
    exit /b 1
)

REM ---------- 3. Tạo virtual environment nếu chưa có ----------
if not exist "venv\Scripts\python.exe" (
    echo Lần đầu chạy: đang tạo môi trường ảo Python...
    python -m venv venv
    if errorlevel 1 (
        echo [LỖI] Không tạo được môi trường ảo (venv).
        pause
        exit /b 1
    )
)

REM ---------- 4. Cài thư viện nếu chưa cài ----------
if not exist "venv\Lib\site-packages\flask" (
    echo Lần đầu chạy: đang cài đặt thư viện cần thiết...
    echo (Bước này có thể mất 1-2 phút, chỉ chạy 1 lần duy nhất)
    echo.
    "venv\Scripts\python.exe" -m pip install --upgrade pip
    "venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [LỖI] Cài đặt thư viện thất bại. Kiểm tra lại kết nối mạng rồi chạy lại file này.
        pause
        exit /b 1
    )
)

REM ---------- 5. Kiểm tra file .env, tạo mẫu nếu chưa có ----------
if not exist ".env" (
    echo Chưa có file .env, đang tạo file mẫu...
    (
        echo GEMINI_API_KEY=
        echo RAG_DATABASE_DIR=database_kntt
        echo RAG_DATA_DIR=datasources
        echo USE_GPU=false
    ) > ".env"
    echo.
    echo [CẦN LÀM] File .env mới tạo còn thiếu GEMINI_API_KEY.
    echo Notepad sẽ mở ra - hãy dán API key của bạn vào dòng GEMINI_API_KEY=, lưu lại rồi chạy lại file này.
    notepad ".env"
    pause
    exit /b 1
)

REM ---------- 6. Dọn dẹp tiến trình cũ trên cổng PORT ----------
echo Đang dọn dẹp tiến trình cũ trên cổng %PORT% (nếu có)...
for /f "tokens=5" %%P in ('netstat -ano ^| findstr ":%PORT%" ^| findstr "LISTENING"') do (
    taskkill /PID %%P /F >nul 2>&1
)
timeout /t 2 /nobreak >nul

REM ---------- 7. Khởi động máy chủ ----------
echo Đang khởi động máy chủ BioRAG - THCS Huỳnh Bá Chánh trên cổng %PORT%...
start "BioRAG Server - THCS Huỳnh Bá Chánh" "%ComSpec%" /k ""%CD%\venv\Scripts\python.exe" "%CD%\main.py" --api --port %PORT%"

echo Đang chờ máy chủ nạp dữ liệu (khoảng 3-5 giây)...
timeout /t 4 /nobreak >nul

echo Đang mở trình duyệt...
start "" "http://127.0.0.1:%PORT%/"

echo.
echo ==========================================
echo   BIORAG - THCS HUỲNH BÁ CHÁNH ĐÃ SẴN SÀNG!
echo   Địa chỉ: http://127.0.0.1:%PORT%/
echo   KHÔNG ĐÓNG cửa sổ "BioRAG Server - THCS Huỳnh Bá Chánh" khi đang sử dụng.
echo ==========================================
echo.
pause
exit /b 0
