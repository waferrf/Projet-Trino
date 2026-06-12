$ErrorActionPreference = "Stop"
$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

Push-Location $ProjectRoot
try {
    docker compose exec -T trino trino --file /project/scripts/demo_queries.sql
    if ($LASTEXITCODE -ne 0) {
        throw "Demo queries failed."
    }
}
finally {
    Pop-Location
}
