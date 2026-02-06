# Run the API so that the `api` module is found (src is on PYTHONPATH).
Set-Location $PSScriptRoot
$env:PYTHONPATH = "src"
uv run uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
