@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

title BioRAG - KHTN THCS Huynh Ba Chanh (Online Server)

echo ======================================================================
echo     HE THONG BIORAG KHTN - TRUONG THCS HUYNH BA CHANH (ONLINE)
echo ======================================================================
echo.

if not exist "main.py" goto ERROR_MAIN
if not exist "venv\Scripts\python.exe" goto ERROR_PYTHON

set "RAG_DATABASE_DIR=database_kntt"
set "RAG_DATA_DIR=datasources"
set "PYTHONUTF8=1"
set "BIORAG_PORT=5000"
set "SUBDOMAIN=thcs-huynhbachanh"

echo 1. Don dep tien trinh cu tren cong %BIORAG_PORT% (neu co)...
for /f "tokens=5" %%P in ('netstat -ano ^| findstr ":%BIORAG_PORT%" ^| findstr "LISTENING"') do (
    taskkill /PID %%P /F >nul 2>&1
)
timeout /t 2 /nobreak >nul

echo 2. Khoi dong may chu BioRAG Backend (Cong %BIORAG_PORT%)...
start "BioRAG Backend - THCS Huynh Ba Chanh" "%ComSpec%" /k ""%CD%\venv\Scripts\python.exe" "%CD%\main.py" --api --port %BIORAG_PORT%"

echo 3. Dang cho may chu nap mo hinh AI va co so du lieu (khoang 25-35 giay)...
timeout /t 30 /nobreak >nul

echo 4. Lay dia chi IP mang cong khai lam mat khau bao mat Tunnel...
for /f %%a in ('powershell -Command "try { (Invoke-RestMethod -Uri https://api.ipify.org -TimeoutSec 5).Trim() } catch { (Invoke-RestMethod -Uri https://ipv4.icanhazip.com -TimeoutSec 5).Trim() }"') do set "PUBLIC_IP=%%a"

echo 5. Ket noi phat hanh ten mien cong khai: https://%SUBDOMAIN%.loca.lt ...
start "BioRAG Online Tunnel" "%ComSpec%" /k "npx -y localtunnel --port %BIORAG_PORT% --subdomain %SUBDOMAIN%"

timeout /t 3 /nobreak >nul

echo.
echo ======================================================================
echo          HE THONG DA DUOC PHAT HANH ONLINE THANH CONG!
echo ======================================================================
echo.
echo  DIA CHI WEBSITE:       https://%SUBDOMAIN%.loca.lt
echo  MAT KHAU MO KHOA (IP): %PUBLIC_IP%
echo.
echo  HUONG DAN TRUY CAP CHO HOC SINH VA GIAO VIEN:
echo   Buoc 1: Mo trinh duyet va truy cap: https://%SUBDOMAIN%.loca.lt
echo   Buoc 2: Trang bao mat hien thi o 'Tunnel Password', dan ma: %PUBLIC_IP%
echo   Buoc 3: Bam nut 'Click to Submit' de vao he thong BioRAG!
echo.
echo ======================================================================
echo  (Vui long GIU NGUYEN 2 cua so chay ngam de he thong duy tri hoat dong)
echo ======================================================================
echo.
pause
exit /b 0

:ERROR_MAIN
echo [LOI] Khong tim thay file main.py trong thu muc goc.
pause
exit /b 1

:ERROR_PYTHON
echo [LOI] Khong tim thay moi truong ao Python venv\Scripts\python.exe
pause
exit /b 1
