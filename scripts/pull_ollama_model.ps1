$ErrorActionPreference = "Stop"
$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

Push-Location $ProjectRoot
try {
    docker compose exec -T ollama ollama pull qwen2.5-coder:1.5b
    if ($LASTEXITCODE -ne 0) {
        throw "Ollama model download failed."
    }
}
finally {
    Pop-Location
}
