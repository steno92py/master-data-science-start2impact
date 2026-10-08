#!/bin/zsh
set -eu
ecobot_dir="$(cd "$(dirname "$0")" && pwd)"
cd "$ecobot_dir"
exec ../../.venv-agenti-ai/bin/python -m streamlit run app.py --server.address 127.0.0.1 --server.port 8518 --browser.gatherUsageStats false
