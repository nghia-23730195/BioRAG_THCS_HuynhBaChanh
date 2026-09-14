@echo off
setlocal
cd /d "%~dp0"

title Khoi dong BioRAG

echo ==========================================
echo            KHOI DONG BIORAG
echo ==========================================
echo.

if not exist "main.py" goto ERROR_MAIN
if not exist "venv\Scripts\python.exe" goto ERROR_PYTHON
if not exist "database_kntt" goto ERROR_DATABASE
if not exist "datasources" goto ERROR_DATASOURCES

set "RAG_DATABASE_DIR=database_kntt"
set "PYTHONUTF8=1"
set "BIORAG_URL=http://127.0.0.1:5000/?v=36"

echo Dang dong may chu BioRAG cu (neu co) de tranh chay nham code cu...
taskkill /FI "WINDOWTITLE eq BioRAG Server*" /T /F >nul 2>&1
for /f "tokens=5" %%P in ('netstat -ano ^| findstr ":5000" ^| findstr "LISTENING"') do (
    taskkill /PID %%P /F >nul 2>&1
)
timeout /t 2 /nobreak >nul

echo Dang khoi dong may chu BioRAG...
start "BioRAG Server" "%ComSpec%" /k ""%CD%\venv\Scripts\python.exe" "%CD%\main.py" --api --port 5000"

echo Dang cho may chu san sang...
timeout /t 8 /nobreak >nul

echo Dang mo trinh duyet...
start "" "%BIORAG_URL%"

echo.
echo BioRAG da duoc khoi dong.
echo Khong dong cua so BioRAG Server khi dang su dung.
echo.
pause
exit /b 0

:ERROR_MAIN
echo [LOI] Khong tim thay main.py
goto END_ERROR

:ERROR_PYTHON
echo [LOI] Khong tim thay venv\Scripts\python.exe
echo Hay tao lai moi truong ao Python.
goto END_ERROR

:ERROR_DATABASE
echo [LOI] Khong tim thay thu muc database_kntt
goto END_ERROR

:ERROR_DATASOURCES
echo [LOI] Khong tim thay thu muc datasources
goto END_ERROR

:END_ERROR
echo.
echo BioRAG chua duoc khoi dong.
pause
exit /b 1