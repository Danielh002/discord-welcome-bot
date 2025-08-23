#!/usr/bin/env bash
set -e

VENV=".venv"

case "$1" in
  setup)
    echo "[INFO] Creating virtual environment..."
    python3 -m venv $VENV
    source $VENV/bin/activate

    echo "[INFO] Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "[INFO] Setup complete!"
    ;;

  run)
    if [ ! -d "$VENV" ]; then
      echo "[ERROR] Virtual environment not found. Run './start.sh setup' first."
      exit 1
    fi
    source $VENV/bin/activate
    echo "[INFO] Starting bot..."
    python bot.py
    ;;

  *)
    echo "Usage: ./start.sh {setup|run}"
    exit 1
    ;;
esac
