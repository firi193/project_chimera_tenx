# Run backend tests (from repo root or backend/)
Set-Location $PSScriptRoot\..\backend
$env:PYTHONPATH = "src"
python -m pytest tests -v @args
