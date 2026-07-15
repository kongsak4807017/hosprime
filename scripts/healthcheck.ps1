[CmdletBinding()]
param(
    [string]$EnvFile = $env:HOSPRIME_ENV_FILE
)

$ErrorActionPreference = 'Stop'
$RootDir = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if ([string]::IsNullOrWhiteSpace($EnvFile)) { $EnvFile = Join-Path $RootDir '.env' }

function Fail([string]$Message) { throw $Message }
function Read-EnvValue([string]$Key, [string]$DefaultValue) {
    $match = Get-Content -LiteralPath $EnvFile | Where-Object { $_ -match "^\s*$([regex]::Escape($Key))=" } | Select-Object -Last 1
    if (-not $match) { return $DefaultValue }
    $value = ($match -split '=', 2)[1].Trim()
    if ([string]::IsNullOrWhiteSpace($value)) { return $DefaultValue }
    return $value
}

if (-not (Test-Path -LiteralPath $EnvFile)) { Fail "Environment file not found: $EnvFile" }
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { Fail 'Docker is required.' }
& docker compose version *> $null
if ($LASTEXITCODE -ne 0) { Fail 'Docker Compose v2 is required.' }

$BackendPort = Read-EnvValue 'BACKEND_PORT' '8000'
$FrontendPort = Read-EnvValue 'FRONTEND_PORT' '80'
$BackendUrl = "http://127.0.0.1:$BackendPort"
$FrontendUrl = "http://127.0.0.1:$FrontendPort"

Push-Location $RootDir
try {
    & docker compose --env-file $EnvFile config --quiet
    if ($LASTEXITCODE -ne 0) { Fail 'Docker Compose configuration validation failed.' }

    $running = @(& docker compose --env-file $EnvFile ps --status running --services)
    if ($LASTEXITCODE -ne 0) { Fail 'Unable to inspect Compose services.' }
    foreach ($service in @('postgres', 'redis', 'neo4j', 'backend', 'frontend')) {
        if ($running -notcontains $service) { Fail "Service is not running: $service" }
    }

    $live = Invoke-RestMethod -Uri "$BackendUrl/health/live" -TimeoutSec 15
    $ready = Invoke-RestMethod -Uri "$BackendUrl/health/ready" -TimeoutSec 15
    $frontend = Invoke-WebRequest -Uri "$FrontendUrl/" -TimeoutSec 15 -UseBasicParsing

    if ($live.status -ne 'live') { Fail "Unexpected liveness status: $($live.status)" }
    if ($ready.status -ne 'ready') { Fail "Backend is not fully ready: $($ready.status)" }
    if ($ready.database_dialect -ne 'postgresql') { Fail "Expected PostgreSQL runtime; got $($ready.database_dialect)" }
    if ([string]::IsNullOrWhiteSpace($frontend.Content)) { Fail 'Frontend returned an empty response.' }

    Write-Host 'HosPrime health check passed.'
    Write-Host "Backend: $BackendUrl"
    Write-Host "Frontend: $FrontendUrl"
    & docker compose --env-file $EnvFile ps
    if ($LASTEXITCODE -ne 0) { Fail 'Unable to record Compose service state.' }
}
finally {
    Pop-Location
}
