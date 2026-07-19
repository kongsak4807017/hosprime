[CmdletBinding()]
param(
    [switch]$SkipBuild,
    [string]$EnvFile = $env:HOSPRIME_ENV_FILE,
    [string]$ProjectName = $env:HOSPRIME_COMPOSE_PROJECT_NAME
)

$ErrorActionPreference = 'Stop'
$RootDir = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if ([string]::IsNullOrWhiteSpace($EnvFile)) { $EnvFile = Join-Path $RootDir '.env' }
if ([string]::IsNullOrWhiteSpace($ProjectName)) { $ProjectName = 'hosprime' }

function Fail([string]$Message) { throw $Message }
function Invoke-Compose([Parameter(ValueFromRemainingArguments = $true)][string[]]$Arguments) {
    & docker compose --project-name $ProjectName --env-file $EnvFile @Arguments
    return $LASTEXITCODE
}

if ($ProjectName -notmatch '^[a-z0-9][a-z0-9_-]*$') { Fail 'ProjectName must match ^[a-z0-9][a-z0-9_-]*$.' }
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { Fail 'Docker is required.' }
& docker info *> $null
if ($LASTEXITCODE -ne 0) { Fail 'Docker daemon is not available.' }
& docker compose version *> $null
if ($LASTEXITCODE -ne 0) { Fail 'Docker Compose v2 is required.' }

Push-Location $RootDir
try {
    if (-not (Test-Path -LiteralPath $EnvFile)) {
        Copy-Item -LiteralPath (Join-Path $RootDir '.env.example') -Destination $EnvFile
        Write-Host "Created $EnvFile from .env.example. Replace every CHANGE_ME value, then run this command again."
        exit 2
    }

    $placeholderLine = Get-Content -LiteralPath $EnvFile | Where-Object {
        $_ -notmatch '^\s*(#|$)' -and $_ -match 'CHANGE_ME'
    } | Select-Object -First 1
    if ($null -ne $placeholderLine) {
        Fail "$EnvFile still contains CHANGE_ME placeholders."
    }

    $status = Invoke-Compose config --quiet
    if ($status -ne 0) { Fail 'Docker Compose configuration validation failed.' }

    if (-not $SkipBuild) {
        $status = Invoke-Compose build
        if ($status -ne 0) { Fail 'Docker image build failed.' }
    }

    $status = Invoke-Compose up --detach --wait --wait-timeout 240
    if ($status -ne 0) { Fail 'HosPrime stack did not become healthy.' }

    & (Join-Path $PSScriptRoot 'healthcheck.ps1') -EnvFile $EnvFile -ProjectName $ProjectName
    if ($LASTEXITCODE -ne 0) { Fail 'HosPrime health check failed.' }
    Write-Host "HosPrime local stack is ready (Compose project: $ProjectName)."
}
finally {
    Pop-Location
}
