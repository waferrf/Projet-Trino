param(
    [switch]$SkipModel
)

$ErrorActionPreference = "Stop"
$ProjectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")

function Assert-LastCommandSucceeded {
    param([string]$Message)

    if ($LASTEXITCODE -ne 0) {
        throw $Message
    }
}

function Wait-ExternalCommand {
    param(
        [string]$Name,
        [scriptblock]$Command,
        [int]$Attempts = 60,
        [int]$DelaySeconds = 5
    )

    for ($i = 1; $i -le $Attempts; $i++) {
        try {
            & $Command
        }
        catch {
        }

        if ($LASTEXITCODE -eq 0) {
            Write-Host "$Name is ready."
            return
        }

        Write-Host "Waiting for $Name ($i/$Attempts)..."
        Start-Sleep -Seconds $DelaySeconds
    }

    throw "$Name did not become ready in time."
}

Push-Location $ProjectRoot
try {
    $ClickHouseDataset = Join-Path $ProjectRoot "data\products.csv"
    if (-not (Test-Path $ClickHouseDataset)) {
        throw "Ajoute d'abord le dataset ClickHouse ici: data\products.csv"
    }

    Write-Host "Starting the Docker stack..."
    docker compose up -d --build --remove-orphans
    Assert-LastCommandSucceeded "Docker stack startup failed."

    Write-Host "Waiting for MinIO upload job..."
    docker wait minio-init | Out-Null
    Assert-LastCommandSucceeded "Could not wait for minio-init."

    $minioExitCode = docker inspect -f "{{.State.ExitCode}}" minio-init
    if ($minioExitCode -ne "0") {
        throw "minio-init failed with exit code $minioExitCode."
    }

    Wait-ExternalCommand "ClickHouse" {
        docker compose exec -T clickhouse clickhouse-client --password clickhouse --query "SELECT 1" *> $null
    }

    Write-Host "Creating ClickHouse tables for Power BI..."
    Get-Content -Raw .\clickhouse\init\01_create_tables.sql | docker compose exec -T clickhouse clickhouse-client --password clickhouse --multiquery
    Assert-LastCommandSucceeded "ClickHouse table creation failed."

    Wait-ExternalCommand "Trino" {
        docker compose exec -T trino trino --execute "SELECT 1" *> $null
    }

    Write-Host "Creating Hive and Iceberg tables..."
    docker compose exec -T trino trino --file /project/scripts/init_lakehouse.sql
    Assert-LastCommandSucceeded "Lakehouse table creation failed."

    if (-not $SkipModel) {
        Write-Host "Pulling the local SQL model in Ollama..."
        docker compose exec -T ollama ollama pull qwen2.5-coder:1.5b
        Assert-LastCommandSucceeded "Ollama model download failed."
    }

    Write-Host "Setup complete."
}
finally {
    Pop-Location
}
