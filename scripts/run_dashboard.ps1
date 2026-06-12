$ErrorActionPreference = "Stop"
$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

Push-Location $ProjectRoot
try {
    $PythonPath = Join-Path $ProjectRoot ".venv\Scripts\python.exe"

    if (-not (Test-Path $PythonPath)) {
        python -m venv .venv
        if ($LASTEXITCODE -ne 0) {
            throw "Could not create the Python virtual environment."
        }
    }

    & $PythonPath -m pip install --upgrade pip
    if ($LASTEXITCODE -ne 0) {
        throw "Could not upgrade pip."
    }

    & $PythonPath -m pip install -r streamlit_app\requirements.txt
    if ($LASTEXITCODE -ne 0) {
        throw "Could not install Streamlit dependencies."
    }

    & $PythonPath -m streamlit run streamlit_app\Accueil.py
}
finally {
    Pop-Location
}
