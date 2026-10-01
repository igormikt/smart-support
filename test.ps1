$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ProjectRoot

& ".\.venv\Scripts\Activate.ps1"
python -m pytest -q
