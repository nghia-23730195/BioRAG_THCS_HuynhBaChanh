@echo off
setlocal
cd /d "%~dp0"

title BioRAG - KHTN THCS Tan Tao (Online Server)

echo =======================================================
echo     KHOI DONG HE THONG BIORAG KHTN THCS TAN TAO
echo =======================================================
echo.

if not exist "main.py" goto ERROR_MAIN
if not exist "venv\Scripts\python.exe" goto ERROR_PYTHON

set "RAG_DATABASE_DIR=database_kntt"
set "RAG_DATA_DIR=datasources"
set "PYTHONUTF8=1"
set "BIORAG_PORT=5000"
set "SUBDOMAIN=khtn-thcs-tantao"

echo 1. Kiem tra va khoi dong may chu BioRAG Backend (Port %BIORAG_PORT%)...
start "BioRAG Backend Server" "%ComSpec%" /k ""%CD%\venv\Scripts\python.exe" "%CD%\main.py" --api --port %BIORAG_PORT%"

echo 2. Dang cho may chu backend nap xong mo hinh (khoang 40 giay)...
timeout /t 35 /nobreak >nul

echo 3. Lay dia chi IP mang hien tai lam mat khau Tunnel...
for /f %%a in ('powershell -Command "(Invoke-RestMethod -Uri https://api.ipify.org -TimeoutSec 5).Trim()"') do set "PUBLIC_IP=%%a"

echo 4. Dang ket noi ten mien cong khai: https://%SUBDOMAIN%.loca.lt ...
start "BioRAG Online Tunnel" "%ComSpec%" /k "npx -y localtunnel --port %BIORAG_PORT% --subdomain %SUBDOMAIN%"

echo.
echo =======================================================
echo      HE THONG DA DUOC PHAT ONLINE THANH CONG!
echo =======================================================
echo  - Dia chi website:  https://%SUBDOMAIN%.loca.lt
echo  - Mat khau mo khoa (Tunnel Password): %PUBLIC_IP%
echo.
echo  Luu y khi truy cap lan dau:
echo   1. Mo link https://%SUBDOMAIN%.loca.lt tren trinh duyet
echo   2. Nhap mat khau vao o "Tunnel Password": %PUBLIC_IP%
echo   3. Nhan nut "Click to Submit" de vao trang chu BioRAG.
echo =======================================================
echo.
echo Khong dong cac cua so chay ngam khi dang su dung.
pause
exit /b 0

:ERROR_MAIN
echo [LOI] Khong tim thay file main.py
pause
exit /b 1

:ERROR_PYTHON
echo [LOI] Khong tim thay venv\Scripts\python.exe
pause
exit /b 1
