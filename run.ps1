$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

if (-not (Test-Path ".venv\Scripts\python.exe")) {
    & ".\setup.ps1"
}

& ".\.venv\Scripts\Activate.ps1"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
