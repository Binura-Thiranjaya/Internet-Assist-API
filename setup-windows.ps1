# =============================================================================
# setup-windows.ps1 — One-time setup for B1 Flask API on Windows Server / IIS
# Run this ONCE on the server as Administrator before IIS serves the site.
# =============================================================================
# Usage:
#   cd C:\inetpub\wwwroot\ia-api
#   .\setup-windows.ps1
# =============================================================================
$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "=== Internet Assist API — Windows Server Setup ===" -ForegroundColor Cyan
Write-Host ""

# 1 — Create virtual environment if it doesn't exist
if (-not (Test-Path ".\venv")) {
    Write-Host "[1/5] Creating Python virtual environment..." -ForegroundColor Yellow
    python -m venv venv
} else {
    Write-Host "[1/5] Virtual environment already exists." -ForegroundColor Green
}

# 2 — Install dependencies
Write-Host "[2/5] Installing Python dependencies..." -ForegroundColor Yellow
.\venv\Scripts\pip install --upgrade pip --quiet
.\venv\Scripts\pip install -r requirements.txt --quiet
Write-Host "      Dependencies installed." -ForegroundColor Green

# 3 — Create logs directory
if (-not (Test-Path ".\logs")) {
    New-Item -ItemType Directory -Path ".\logs" | Out-Null
    Write-Host "[3/5] Created logs\ directory." -ForegroundColor Green
} else {
    Write-Host "[3/5] logs\ directory already exists." -ForegroundColor Green
}

# 4 — Run DB migrations
Write-Host "[4/5] Running database migrations..." -ForegroundColor Yellow
$env:FLASK_APP = "wsgi:app"
.\venv\Scripts\flask db upgrade
Write-Host "      Migrations complete." -ForegroundColor Green

# 5 — Seed initial admin user (safe to run multiple times)
Write-Host "[5/5] Seeding initial data..." -ForegroundColor Yellow
try {
    .\venv\Scripts\flask seed
    Write-Host "      Seed complete." -ForegroundColor Green
} catch {
    Write-Host "      Seed skipped (already seeded or non-fatal error)." -ForegroundColor DarkYellow
}

Write-Host ""
Write-Host "=== Setup complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Copy your .env file to this directory (or set env vars in IIS application pool)"
Write-Host "  2. In IIS Manager: add a new site pointing to this folder"
Write-Host "  3. Set the application pool to 'No Managed Code'"
Write-Host "  4. Ensure HttpPlatformHandler module is installed"
Write-Host "  5. Restart IIS:  iisreset"
Write-Host ""
