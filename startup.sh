#!/bin/bash
# Azure App Service startup script
set -e

VENV="/home/site/wwwroot/antenv"
if [ -d "$VENV" ]; then
    source "$VENV/bin/activate"
    echo "[startup] Activated virtualenv: $VENV"
else
    echo "[startup] WARNING: antenv not found, using system Python"
fi

export FLASK_APP=wsgi:app

echo "[startup] Python: $(python --version 2>&1)"
echo "[startup] Flask: $(flask --version 2>&1)"
echo "[startup] DATABASE_URL set: $([ -n "$DATABASE_URL" ] && echo YES || echo NO)"

echo "[startup] Running DB migrations..."
flask db upgrade 2>&1 || { echo "[startup] MIGRATION FAILED"; exit 1; }

echo "[startup] Seeding initial data..."
flask seed 2>&1 || { echo "[startup] SEED FAILED (non-fatal)"; }

echo "[startup] Starting gunicorn on port ${PORT:-8000}..."
exec gunicorn wsgi:app \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers 2 \
  --threads 4 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
