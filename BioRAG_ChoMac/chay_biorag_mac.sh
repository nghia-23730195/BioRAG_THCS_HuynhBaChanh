#!/bin/bash
set -e
cd "$(dirname "$0")"

echo "=========================================="
echo "   BIORAG - KHOI DONG TREN macOS"
echo "=========================================="
echo

if [ ! -f "main.py" ]; then
  echo "[LOI] Khong tim thay main.py. Hay dat file nay dung trong thu muc goc BioRAG_ChoMac."
  exit 1
fi

if [ ! -d "database_kntt" ]; then
  echo "[CANH BAO] Khong tim thay thu muc database_kntt."
  echo "Xem huong dan macOS (Huong_dan_trien_khai_BioRAG_macOS.md) de chep du lieu nay sang truoc."
fi

if [ ! -f ".env" ]; then
  echo "[LOI] Chua co file .env."
  echo "Hay doi ten .env.example thanh .env va dien GEMINI_API_KEY, roi chay lai."
  exit 1
fi

if [ ! -d "venv" ]; then
  echo "Lan dau chay: dang tao moi truong ao Python..."
  python3.10 -m venv venv || python3 -m venv venv
fi

source venv/bin/activate

if ! python -c "import chromadb" 2>/dev/null; then
  echo "Lan dau chay: dang cai dat thu vien can thiet (co the mat vai phut)..."
  pip install --upgrade pip
  pip install -r requirements_docker.txt
fi

PORT=${1:-5001}
echo "Dang khoi dong may chu BioRAG tren cong $PORT..."
echo "(Luu y: cong 5000 mac dinh cua macOS hay bi AirPlay Receiver chiem, nen dung $PORT)"
python main.py --api --port "$PORT" &
SERVER_PID=$!

sleep 8
open "http://127.0.0.1:$PORT/" 2>/dev/null || true

echo
echo "BioRAG dang chay tai http://127.0.0.1:$PORT/  (PID $SERVER_PID)"
echo "Nhan Ctrl+C trong cua so nay de dung server."
wait $SERVER_PID
