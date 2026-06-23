#!/usr/bin/env sh
set -eu

python database/init_postgres.py

exec streamlit run app.py \
  --server.address=0.0.0.0 \
  --server.port="${PORT:-10000}" \
  --server.headless=true
