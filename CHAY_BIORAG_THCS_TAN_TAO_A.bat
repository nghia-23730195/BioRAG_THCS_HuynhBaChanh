@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
cd /d "%~dp0"

title BioRAG - THCS Tan Tao A

echo ==========================================
echo   HE THONG BIORAG - THCS TAN TAO A
echo   (Khoi dong mot cham)
echo ==========================================
echo.

set "PORT=5000"
set "PYTHONUTF8=1"
set "RAG_DATABASE_DIR=database_kntt"
set "RAG_DATA_DIR=datasources"

REM ---------- 1. Kiem tra file goc du an ----------
if not exist "main.py" (
    echo [LOI] Khong tim thay main.py.
    echo Hay dat file .bat nay ngay trong thu muc goc BioRAG_Final roi chay lai.
    pause
    exit /b 1
)

if not exist "database_kntt" (
    echo [CANH BAO] Khong tim thay thu muc database_kntt.
    echo He thong van chay duoc nhung se khong co du lieu SGK da xu ly san.
    echo.
)

REM ---------- 2. Kiem tra Python da cai chua ----------
where python >nul 2>&1
if errorlevel 1 (
    echo [LOI] May tinh chua cai Python.
    echo Vui long tai va cai Python 3.10 tai: https://www.python.org/downloads/
    echo Luu y: khi cai dat phai TICK vao o "Add Python to PATH".
    pause
    exit /b 1
)

REM ---------- 3. Tao virtual environment neu chua co ----------
if not exist "venv\Scripts\python.exe" (
    echo Lan dau chay: dang tao moi truong ao Python...
    python -m venv venv
    if errorlevel 1 (
        echo [LOI] Khong tao duoc moi truong ao ^(venv^).
        pause
        exit /b 1
    )
)

REM ---------- 4. Cai thu vien neu chua cai ----------
if not exist "venv\Lib\site-packages\chromadb" (
    echo Lan dau chay: dang cai dat thu vien can thiet...
    echo ^(Buoc nay co the mat vai phut, chi chay 1 lan duy nhat^)
    echo.
    "venv\Scripts\python.exe" -m pip install --upgrade pip
    "venv\Scripts\python.exe" -m pip install -r requirements_docker.txt
    if errorlevel 1 (
        echo [LOI] Cai dat thu vien that bai. Kiem tra lai ket noi mang roi chay lai file nay.
        pause
        exit /b 1
    )
)

REM ---------- 5. Kiem tra file .env, tao mau neu chua co ----------
if not exist ".env" (
    echo Chua co file .env, dang tao file mau...
    (
        echo GEMINI_API_KEY=
        echo TESSERACT_CMD=tesseract
        echo POPPLER_PATH=
        echo RAG_DATABASE_DIR=database_kntt
        echo RAG_DATA_DIR=datasources
        echo USE_GPU=false
    ) > ".env"
    echo.
    echo [CAN LAM] File .env moi tao con thieu GEMINI_API_KEY.
    echo Notepad se mo ra - hay dan API key cua ban vao dong GEMINI_API_KEY=, luu lai roi chay lai file nay.
    notepad ".env"
    pause
    exit /b 1
)

REM ---------- 6. Don dep tien trinh cu tren cong PORT ----------
echo Dang don dep tien trinh cu tren cong %PORT% ^(neu co^)...
for /f "tokens=5" %%P in ('netstat -ano ^| findstr ":%PORT%" ^| findstr "LISTENING"') do (
    taskkill /PID %%P /F >nul 2>&1
)
timeout /t 2 /nobreak >nul

REM ---------- 7. Khoi dong may chu ----------
echo Dang khoi dong may chu BioRAG - THCS Tan Tao A tren cong %PORT%...
start "BioRAG Server - THCS Tan Tao A" "%ComSpec%" /k ""%CD%\venv\Scripts\python.exe" "%CD%\main.py" --api --port %PORT%"

echo Dang cho may chu nap du lieu ^(khoang 10-30 giay^)...
timeout /t 12 /nobreak >nul

echo Dang mo trinh duyet...
start "" "http://127.0.0.1:%PORT%/"

echo.
echo ==========================================
echo   BIORAG - THCS TAN TAO A DA SAN SANG
echo   Dia chi: http://127.0.0.1:%PORT%/
echo   KHONG DONG cua so "BioRAG Server - THCS Tan Tao A" khi dang su dung.
echo ==========================================
echo.
pause
exit /b 0
